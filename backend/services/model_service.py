
import joblib
try:
    import shap
except ImportError:
    shap = None
import numpy as np
import pandas as pd
import torch
from pathlib import Path

from federated.model import FraudDNN


class FraudModelService:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        models_dir = self.base_dir / "models"

        self.model_path = models_dir / "fedprox_global_dnn.pth"
        self.medians = joblib.load(
            models_dir / "fedprox_train_medians.pkl"
        )
        self.category_mappings = joblib.load(
            models_dir / "fedprox_category_mappings.pkl"
        )
        self.scaler = joblib.load(
            models_dir / "fedprox_scaler.pkl"
        )

        # Load expected feature order from the training dataset.
        self.feature_names = list(
            pd.read_pickle(
                self.base_dir / "data" / "processed" / "X_train.pkl"
            ).columns
        )

        self.device = torch.device("cpu")
        self.model = FraudDNN(input_size=len(self.feature_names))
        state = torch.load(self.model_path, map_location=self.device)
        self.model.load_state_dict(state)
        self.model.eval()

        self.threshold = 0.85

        # SHAP background data using the same preprocessing pipeline (optional)
        if shap is not None:
            X_train = pd.read_pickle(
                self.base_dir / "data" / "processed" / "X_train.pkl"
            )
            background_df = X_train.sample(
                n=min(30, len(X_train)),
                random_state=42
            )
            background = self.preprocess_dataframe(background_df)
            background_tensor = torch.tensor(
                background, dtype=torch.float32
            )
            self.shap_explainer = shap.GradientExplainer(
                self.model,
                background_tensor
            )
        else:
            self.shap_explainer = None

        print("FedProx model loaded successfully.")
        print("Number of features:", len(self.feature_names))
        print("Fraud threshold:", self.threshold)

    def preprocess_dataframe(self, df):
        if df.empty:
            raise ValueError("The uploaded CSV contains no transaction rows.")

        # Normalize column names and support common aliases.
        df = df.copy()
        df.columns = df.columns.astype(str).str.strip()
        aliases = {
            "transaction_id": "TransactionID",
            "transactionid": "TransactionID",
            "transaction_amount": "TransactionAmt",
            "transactionamt": "TransactionAmt",
            "amount": "TransactionAmt",
            "transaction_time": "TransactionDT",
            "transactiondt": "TransactionDT",
            "product_code": "ProductCD",
            "productcd": "ProductCD",
        }
        rename_map = {}
        for column in df.columns:
            normalized = column.strip().lower().replace(" ", "_")
            if normalized in aliases:
                rename_map[column] = aliases[normalized]
        df = df.rename(columns=rename_map)

        # Reject duplicate columns created by alias mapping.
        if df.columns.duplicated().any():
            duplicates = df.columns[df.columns.duplicated()].tolist()
            raise ValueError(
                f"CSV contains duplicate columns after name mapping: {duplicates}"
            )

        # Require meaningful overlap with the model's expected schema.
        matching = set(df.columns).intersection(self.feature_names)
        if len(matching) < 3:
            raise ValueError(
                "This CSV does not contain enough recognizable transaction features. "
                "Upload an IEEE-CIS-compatible CSV containing fields such as "
                "TransactionAmt, TransactionDT, ProductCD, or card information. "
                "Unrelated CSV files cannot be reliably converted into this model's inputs."
            )

        X = pd.DataFrame(index=df.index)

        for col in self.feature_names:
            if col in df.columns:
                X[col] = df[col]
            else:
                X[col] = np.nan

        # Apply saved category mappings. Unknown values become -1.
        for col, mapping in self.category_mappings.items():
            if col in X.columns:
                X[col] = X[col].map(
                    lambda value: mapping.get(value, -1)
                    if pd.notna(value) else -1
                )

        # Convert all features to numeric and impute missing values.
        for col in self.feature_names:
            X[col] = pd.to_numeric(X[col], errors="coerce")

        X = X.fillna(self.medians)
        X = X.fillna(0)

        # Apply the same scaler used for training.
        scaled = self.scaler.transform(X[self.feature_names])
        return np.asarray(scaled, dtype=np.float32)

    def explain_transaction(self, scaled_row, top_k=5):
        tensor = torch.tensor(
            scaled_row.reshape(1, -1),
            dtype=torch.float32
        )
        # If SHAP explainer is unavailable, skip explanation
        if self.shap_explainer is None:
            return []
        shap_values = self.shap_explainer.shap_values(tensor)
        values = np.asarray(shap_values).squeeze()
        if values.ndim != 1 or len(values) != len(self.feature_names):
            raise ValueError(
                f"Unexpected SHAP output shape: {np.asarray(shap_values).shape}"
            )
        top_indices = np.argsort(np.abs(values))[::-1][:top_k]
        return [
            {
                "feature": self.feature_names[index],
                "shap_value": round(float(values[index]), 6),
                "direction": (
                    "increases_model_output"
                    if values[index] > 0
                    else "decreases_model_output"
                    if values[index] < 0
                    else "neutral"
                )
            }
            for index in top_indices
        ]

    def predict_dataframe(self, df):
        X = self.preprocess_dataframe(df)
        tensor = torch.tensor(X, dtype=torch.float32)

        with torch.no_grad():
            logits = self.model(tensor).squeeze(-1)
            probabilities = torch.sigmoid(logits).cpu().numpy()

        predictions = (probabilities >= self.threshold).astype(int)

        transactions = []
        for i, probability in enumerate(probabilities):
            if probability >= 0.90:
                risk = "HIGH"
            elif probability >= 0.50:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            raw_id = df.iloc[i].get("TransactionID", f"TXN{i + 1:04d}")
            amount = df.iloc[i].get(
                "TransactionAmt", df.iloc[i].get("amount")
            )

            explanation = self.explain_transaction(X[i])

            transactions.append({
                "transaction_id": str(raw_id),
                "amount": float(amount) if pd.notna(amount) else None,
                "fraud_probability": round(float(probability), 4),
                "prediction": int(predictions[i]),
                "risk_level": risk,
                "explanation": explanation,
                "raw_features": {
                    key: str(value)
                    for key, value in df.iloc[i].items()
                    if pd.notna(value)
                }
            })

        fraud_count = int(predictions.sum())
        total = len(df)

        return {
            "success": True,
            "summary": {
                "total_transactions": total,
                "fraudulent_transactions": fraud_count,
                "legitimate_transactions": total - fraud_count,
                "fraud_rate": round(fraud_count / total * 100, 2)
            },
            "model_info": {
                "model": "FedProx DNN",
                "num_features": len(self.feature_names),
                "threshold": self.threshold
            },
            "transactions": transactions
        }



fraud_model = FraudModelService()

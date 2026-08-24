import joblib
import pickle
import numpy as np
import pandas as pd
from pathlib import Path


class FraudModelService:

    CATEGORICAL_COLS = [
        "ProductCD", "card4", "card6",
        "P_emaildomain", "R_emaildomain",
        "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",
        "DeviceType", "DeviceInfo",
        "id_12", "id_15", "id_16", "id_23", "id_27", "id_28",
        "id_29", "id_30", "id_31", "id_33", "id_34", "id_35",
        "id_36", "id_37", "id_38",
    ]

    def __init__(self):
        # Project root
        BASE_DIR = Path(__file__).resolve().parents[2]

        # Models folder
        models_dir = BASE_DIR / "models"

        model_path = models_dir / "lightgbm_fraud_model.pkl"
        feature_info_path = models_dir / "feature_info.pkl"

        print("Loading fraud detection model...")

        # Model was saved using joblib
        self.model = joblib.load(model_path)

        # Feature information was saved using pickle
        with open(feature_info_path, "rb") as f:
            self.feature_info = pickle.load(f)

        self.feature_names = self.feature_info["feature_names"]
        self.threshold = float(self.feature_info.get("threshold", 0.20))

        print("Model loaded successfully!")
        print("Number of features:", len(self.feature_names))
        print("Fraud threshold:", self.threshold)

    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validates and preprocesses an input transaction DataFrame to match
        the exact 421 feature columns expected by the LightGBM model.
        """
        if df.empty:
            raise ValueError("The uploaded CSV file contains no data rows.")

        # Check overlap between input columns and model feature names
        matching_cols = set(df.columns).intersection(set(self.feature_names))
        if len(matching_cols) < 3 and "TransactionAmt" not in df.columns and "amount" not in df.columns:
            raise ValueError(
                "Unable to analyze file. The uploaded CSV does not contain required transaction feature columns."
            )

        # Construct DataFrame with exact 421 features in exact order efficiently
        data_dict = {}
        for col in self.feature_names:
            if col in df.columns:
                data_dict[col] = df[col].values
            else:
                data_dict[col] = np.full(len(df), np.nan)

        X = pd.DataFrame(data_dict, index=df.index)

        # Convert categorical columns to 'category' dtype
        for col in self.CATEGORICAL_COLS:
            if col in X.columns:
                X[col] = X[col].astype("category")

        # Downcast numerical columns to float32
        numeric_cols = X.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            X[col] = X[col].astype("float32", copy=False)

        return X

    def predict(self, X):
        probabilities = self.model.predict_proba(X)[:, 1]

        predictions = (
            probabilities >= self.threshold
        ).astype(int)

        return probabilities, predictions

    def predict_dataframe(self, df: pd.DataFrame) -> dict:
        """
        Full prediction pipeline for an uploaded DataFrame.
        """
        X = self.preprocess_dataframe(df)
        probabilities, predictions = self.predict(X)

        total_txns = len(df)
        fraud_count = int((predictions == 1).sum())
        legit_count = total_txns - fraud_count
        fraud_rate = round((fraud_count / total_txns * 100), 2) if total_txns > 0 else 0.0

        transactions = []
        for i in range(total_txns):
            prob = round(float(probabilities[i]), 4)
            pred = int(predictions[i])

            if prob >= 0.70:
                risk_level = "HIGH"
            elif prob >= self.threshold:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            # Determine transaction ID
            if "TransactionID" in df.columns and pd.notnull(df.iloc[i]["TransactionID"]):
                raw_id = df.iloc[i]["TransactionID"]
                if isinstance(raw_id, float) and raw_id.is_integer():
                    txn_id = f"TXN{int(raw_id)}"
                else:
                    txn_id = str(raw_id)
            else:
                txn_id = f"TXN{i + 1:04d}"

            # Determine transaction amount
            amount = None
            if "TransactionAmt" in df.columns and pd.notnull(df.iloc[i]["TransactionAmt"]):
                amount = float(df.iloc[i]["TransactionAmt"])
            elif "amount" in df.columns and pd.notnull(df.iloc[i]["amount"]):
                amount = float(df.iloc[i]["amount"])

            # Extract raw non-null features for detail drawer
            row_dict = {}
            for col in df.columns:
                val = df.iloc[i][col]
                if pd.notnull(val):
                    if isinstance(val, (np.integer, int)):
                        row_dict[col] = int(val)
                    elif isinstance(val, (np.floating, float)):
                        row_dict[col] = round(float(val), 4)
                    else:
                        row_dict[col] = str(val)

            transactions.append({
                "transaction_id": txn_id,
                "amount": amount,
                "fraud_probability": prob,
                "prediction": pred,
                "risk_level": risk_level,
                "raw_features": row_dict
            })

        return {
            "success": True,
            "summary": {
                "total_transactions": total_txns,
                "fraudulent_transactions": fraud_count,
                "legitimate_transactions": legit_count,
                "fraud_rate": fraud_rate
            },
            "model_info": {
                "model": "LightGBM",
                "num_features": len(self.feature_names),
                "threshold": self.threshold
            },
            "transactions": transactions
        }


# Create one model instance
fraud_model = FraudModelService()
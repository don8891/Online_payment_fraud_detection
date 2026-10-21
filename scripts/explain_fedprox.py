
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import torch

from backend.services.model_service import fraud_model

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
FIG_DIR = BASE_DIR / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Load original training data
X_train = pd.read_pickle(DATA_DIR / "X_train.pkl")

# Apply exactly the same preprocessing as the backend
background_df = X_train.sample(
    n=min(30, len(X_train)), random_state=42
)
background = fraud_model.preprocess_dataframe(background_df)

# Explain a few test transactions
X_test = pd.read_pickle(DATA_DIR / "X_test.pkl")
examples_df = X_test.sample(
    n=min(3, len(X_test)), random_state=42
)
examples = fraud_model.preprocess_dataframe(examples_df)

background_tensor = torch.tensor(background, dtype=torch.float32)
examples_tensor = torch.tensor(examples, dtype=torch.float32)

# Explain model logits, the values before sigmoid
model = fraud_model.model
model.eval()

explainer = shap.GradientExplainer(model, background_tensor)
shap_values = explainer.shap_values(examples_tensor)

values = np.asarray(shap_values)
values = np.squeeze(values)

# Normalize the result shape for a single-output DNN
if values.ndim == 1:
    values = values.reshape(1, -1)

if values.shape != examples.shape:
    raise ValueError(
        f"Unexpected SHAP shape {values.shape}; "
        f"expected {examples.shape}. "
        "Inspect the SHAP output shape before plotting."
    )

# Calculate mean absolute SHAP values for the 3 examples
importance = np.mean(np.abs(values), axis=0)

importance_df = pd.DataFrame({
    "feature": fraud_model.feature_names,
    "mean_abs_shap": importance,
}).sort_values("mean_abs_shap", ascending=False)

csv_path = FIG_DIR / "fedprox_shap_feature_importance.csv"
importance_df.to_csv(csv_path, index=False)

# Plot the top 20 features
top = importance_df.head(20).sort_values("mean_abs_shap")

plt.figure(figsize=(10, 8))
plt.barh(top["feature"], top["mean_abs_shap"])
plt.xlabel("Mean absolute SHAP value (logit output)")
plt.ylabel("Feature")
plt.title("FedProx DNN: Top 20 SHAP Features")
plt.tight_layout()

png_path = FIG_DIR / "fedprox_shap_feature_importance.png"
plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.close()

# Display the explained transactions' model outputs
with torch.no_grad():
    probabilities = torch.sigmoid(
        model(examples_tensor).squeeze(-1)
    ).cpu().numpy()

print("SHAP analysis completed.")
print("\nExplained transaction fraud probabilities:")
for i, probability in enumerate(probabilities):
    print(f"Transaction {i + 1}: {probability:.4f}")

print("\nTop 10 features for these examples:")
print(importance_df.head(10).to_string(index=False))
print(f"\nChart saved to: {png_path}")
print(f"Feature importance saved to: {csv_path}")

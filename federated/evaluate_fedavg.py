# ============================================================
# federated/evaluate_fedavg.py
#
# Evaluate the FedAvg global DNN on the held-out test set.
# ============================================================

import numpy as np
import pandas as pd
import torch
from pathlib import Path

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
)

from federated.model import FraudDNN


# --------------------------------------------------
# Paths
# --------------------------------------------------
DATA_DIR   = Path("data/processed")
MODEL_PATH = Path("models/fedavg_global_dnn.pth")

print("Loading test data...")
X_test_dnn = pd.read_pickle(DATA_DIR / "X_test_dnn.pkl")
y_test     = pd.read_pickle(DATA_DIR / "y_test_dnn.pkl")

print(f"  X_test_dnn : {X_test_dnn.shape}")
print(f"  y_test     : {y_test.shape}")

# --------------------------------------------------
# Load FedAvg global model
# --------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

model = FraudDNN(input_size=421).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

print("Model loaded successfully.")

# --------------------------------------------------
# Inference
# --------------------------------------------------
X_tensor = torch.tensor(X_test_dnn.to_numpy(), dtype=torch.float32).to(device)

with torch.no_grad():
    logits = model(X_tensor)
    probabilities = torch.sigmoid(logits).squeeze().cpu().numpy()

# --------------------------------------------------
# Metrics: ROC-AUC & PR-AUC
# --------------------------------------------------
roc_auc = roc_auc_score(y_test, probabilities)
pr_auc  = average_precision_score(y_test, probabilities)

print("======================================")
print(f"Test ROC-AUC: {roc_auc:.4f}")
print(f"Test PR-AUC:  {pr_auc:.4f}")

# --------------------------------------------------
# Classification using threshold = 0.95
# --------------------------------------------------
threshold = 0.95
predictions = (probabilities >= threshold).astype(int)

# --------------------------------------------------
# Classification report
# --------------------------------------------------
print()
print("Classification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Fraud"],
        digits=2
    )
)

# --------------------------------------------------
# Confusion matrix
# --------------------------------------------------
cm = confusion_matrix(y_test, predictions)
print("Confusion Matrix:")
print(cm)

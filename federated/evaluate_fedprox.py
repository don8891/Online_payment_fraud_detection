# ============================================================
# federated/evaluate_fedprox.py
#
# Evaluate the FedProx global DNN on the held-out test set.
# ============================================================

import sys
import os
sys.path.append(os.path.abspath('.'))

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

DATA_DIR = Path("data/processed")
MODEL_PATH = Path("models/fedprox_global_dnn.pth")

print("Loading validation and test data...")

X_val_dnn = pd.read_pickle(DATA_DIR / "X_val_dnn.pkl")
y_val = pd.read_pickle(DATA_DIR / "y_val_dnn.pkl")

X_test_dnn = pd.read_pickle(DATA_DIR / "X_test_dnn.pkl")
y_test = pd.read_pickle(DATA_DIR / "y_test_dnn.pkl")

# --------------------------------------------------
# Load FedProx global model
# --------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Device: {device}")

model = FraudDNN(input_size=421).to(device)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.eval()

print("FedProx model loaded successfully.")



# --------------------------------------------------
# Inference on validation and test data
# --------------------------------------------------

X_val_tensor = torch.tensor(
    X_val_dnn.to_numpy(), dtype=torch.float32
).to(device)

X_test_tensor = torch.tensor(
    X_test_dnn.to_numpy(), dtype=torch.float32
).to(device)

with torch.no_grad():
    val_logits = model(X_val_tensor)
    val_probabilities = (
        torch.sigmoid(val_logits).squeeze().cpu().numpy()
    )

    test_logits = model(X_test_tensor)
    probabilities = (
        torch.sigmoid(test_logits).squeeze().cpu().numpy()
    )

# --------------------------------------------------
# Select threshold using validation data only
# --------------------------------------------------

from sklearn.metrics import f1_score

thresholds = np.arange(0.05, 0.96, 0.05)

best_threshold = 0.05
best_f1 = -1

for candidate in thresholds:
    val_predictions = (val_probabilities >= candidate).astype(int)
    score = f1_score(y_val, val_predictions, zero_division=0)

    if score > best_f1:
        best_f1 = score
        best_threshold = candidate

print(f"Best validation threshold: {best_threshold:.2f}")
print(f"Best validation F1-score: {best_f1:.4f}")

# Apply the selected threshold to the test set
threshold = best_threshold
predictions = (probabilities >= threshold).astype(int)

# --------------------------------------------------
# Metrics using the selected validation threshold
# --------------------------------------------------
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
)

roc_auc = roc_auc_score(y_test, probabilities)
pr_auc = average_precision_score(y_test, probabilities)

print("======================================")
print(f"Test ROC-AUC: {roc_auc:.4f}")
print(f"Test PR-AUC:  {pr_auc:.4f}")
print(f"Decision threshold: {threshold:.2f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Fraud"],
        digits=4,
        zero_division=0,
    )
)

cm = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:")
print(cm)


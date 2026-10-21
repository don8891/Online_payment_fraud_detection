
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
)

from federated.model import FraudDNN

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"
FIG_DIR = BASE_DIR / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

X_test = pd.read_pickle(DATA_DIR / "X_test_dnn.pkl")
y_test = pd.read_pickle(DATA_DIR / "y_test_dnn.pkl").to_numpy()

device = torch.device("cpu")
X_tensor = torch.tensor(X_test.to_numpy(), dtype=torch.float32)

model_files = {
    "FedAvg": MODEL_DIR / "fedavg_global_dnn.pth",
    "FedProx": MODEL_DIR / "fedprox_global_dnn.pth",
}

scores = {}

for name, path in model_files.items():
    model = FraudDNN(input_size=X_test.shape[1]).to(device)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()

    with torch.no_grad():
        logits = model(X_tensor)
        probabilities = torch.sigmoid(logits).squeeze().numpy()

    scores[name] = probabilities
    print(
        name,
        "ROC-AUC:", round(roc_auc_score(y_test, probabilities), 4),
        "PR-AUC:", round(average_precision_score(y_test, probabilities), 4),
    )

# ROC curves
plt.figure(figsize=(8, 6))
for name, probabilities in scores.items():
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    auc = roc_auc_score(y_test, probabilities)
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.4f})")

plt.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve: Federated Models")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(FIG_DIR / "roc_curve_federated.png", dpi=300)
plt.close()

# Precision-recall curves
plt.figure(figsize=(8, 6))
for name, probabilities in scores.items():
    precision, recall, _ = precision_recall_curve(y_test, probabilities)
    ap = average_precision_score(y_test, probabilities)
    plt.plot(recall, precision, label=f"{name} (AP={ap:.4f})")

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve: Federated Models")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(FIG_DIR / "precision_recall_federated.png", dpi=300)
plt.close()

print("\nSaved figures to:", FIG_DIR)

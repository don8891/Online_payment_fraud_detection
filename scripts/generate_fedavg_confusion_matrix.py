
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
FIG_DIR = BASE_DIR / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# FedAvg confusion matrix from the latest evaluation
# Rows: actual classes
# Columns: predicted classes
cm = np.array([
    [82988, 2510],
    [1895, 1188]
])

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt=",d",
    cmap="Blues",
    xticklabels=["Legitimate", "Fraud"],
    yticklabels=["Legitimate", "Fraud"],
    cbar=True
)

plt.title("FedAvg Confusion Matrix (Threshold = 0.90)")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.tight_layout()

output_path = FIG_DIR / "fedavg_confusion_matrix.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"FedAvg confusion matrix saved to: {output_path}")

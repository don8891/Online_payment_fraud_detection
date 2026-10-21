
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
FIGURES_DIR = BASE_DIR / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Metrics from the evaluation outputs shared so far
models = ["Centralized DNN", "FedAvg", "FedProx"]
roc_auc = [0.8491, 0.8413, 0.8479]
pr_auc = [0.2650, 0.2220, 0.3451]

# Figure 1: ROC-AUC and PR-AUC comparison
x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - width / 2, roc_auc, width, label="ROC-AUC")
ax.bar(x + width / 2, pr_auc, width, label="PR-AUC")

ax.set_ylabel("Score")
ax.set_title("Model Performance Comparison")
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 1)
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "model_performance_comparison.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

# Figure 2: FedProx confusion matrix from the latest output
# Rows: actual class [Legitimate, Fraud]
# Columns: predicted class [Legitimate, Fraud]
cm = np.array([
    [83495, 2003],
    [1938, 1145]
])

fig, ax = plt.subplots(figsize=(6, 5))
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Legitimate", "Fraud"]
)
display.plot(ax=ax, values_format=",d", colorbar=False)

ax.set_title("FedProx DNN Confusion Matrix")
fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "fedprox_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

print("Figures saved to:", FIGURES_DIR)
print("1. model_performance_comparison.png")
print("2. fedprox_confusion_matrix.png")

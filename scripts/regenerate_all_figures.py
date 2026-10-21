"""
scripts/regenerate_all_figures.py
===================================
Regenerate all research figures from the CURRENT model checkpoints.

Figures produced:
  reports/figures/fedprox_confusion_matrix.png
  reports/figures/fedavg_confusion_matrix.png
  reports/figures/roc_curve_federated.png
  reports/figures/precision_recall_federated.png
  reports/figures/model_performance_comparison.png
  reports/figures/fedprox_shap_feature_importance.png
  reports/figures/fedprox_shap_feature_importance.csv
"""

import sys, os
sys.path.insert(0, os.path.abspath("."))

import numpy as np
import pandas as pd
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.metrics import (
    roc_curve, roc_auc_score,
    precision_recall_curve, average_precision_score,
    confusion_matrix, classification_report,
    f1_score, precision_score, recall_score,
)

from federated.model import FraudDNN

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR  = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"
FIG_DIR   = BASE_DIR / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load data
print("Loading data ...")
X_val  = pd.read_pickle(DATA_DIR / "X_val_dnn.pkl")
y_val  = pd.read_pickle(DATA_DIR / "y_val_dnn.pkl")
X_test = pd.read_pickle(DATA_DIR / "X_test_dnn.pkl")
y_test = pd.read_pickle(DATA_DIR / "y_test_dnn.pkl")

X_val_t  = torch.tensor(X_val.to_numpy(),  dtype=torch.float32).to(DEVICE)
X_test_t = torch.tensor(X_test.to_numpy(), dtype=torch.float32).to(DEVICE)

y_val_np  = np.array(y_val)
y_test_np = np.array(y_test)

print(f"  Val  : {X_val.shape[0]:,} rows | Fraud rate: {y_val_np.mean():.4f}")
print(f"  Test : {X_test.shape[0]:,} rows | Fraud rate: {y_test_np.mean():.4f}")


def load_and_score(path, tensor, val_tensor, y_val_np):
    model = FraudDNN(input_size=tensor.shape[1]).to(DEVICE)
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.eval()
    with torch.no_grad():
        val_probs  = torch.sigmoid(model(val_tensor)).squeeze().cpu().numpy()
        test_probs = torch.sigmoid(model(tensor)).squeeze().cpu().numpy()
    best_thresh, best_f1 = 0.5, -1
    for t in np.arange(0.05, 0.96, 0.05):
        f = f1_score(y_val_np, (val_probs >= t).astype(int), zero_division=0)
        if f > best_f1:
            best_f1, best_thresh = f, t
    print(f"  [{path.stem}]  val best-threshold={best_thresh:.2f}  val-F1={best_f1:.4f}")
    return model, test_probs, best_thresh


print("\nScoring FedProx ...")
fedprox_model, fedprox_probs, fedprox_thresh = load_and_score(
    MODEL_DIR / "fedprox_global_dnn.pth", X_test_t, X_val_t, y_val_np
)

fedavg_path = MODEL_DIR / "fedavg_global_dnn.pth"
has_fedavg = fedavg_path.exists()
if has_fedavg:
    print("Scoring FedAvg ...")
    _, fedavg_probs, fedavg_thresh = load_and_score(fedavg_path, X_test_t, X_val_t, y_val_np)
else:
    print("FedAvg model not found — skipping FedAvg figures.")
    fedavg_probs = None
    fedavg_thresh = None

fedprox_preds = (fedprox_probs >= fedprox_thresh).astype(int)
if has_fedavg:
    fedavg_preds = (fedavg_probs >= fedavg_thresh).astype(int)

fedprox_roc = roc_auc_score(y_test_np, fedprox_probs)
fedprox_pr  = average_precision_score(y_test_np, fedprox_probs)
if has_fedavg:
    fedavg_roc = roc_auc_score(y_test_np, fedavg_probs)
    fedavg_pr  = average_precision_score(y_test_np, fedavg_probs)

print("\n=== Test Metrics ===")
print(f"FedProx  ROC-AUC={fedprox_roc:.4f}  PR-AUC={fedprox_pr:.4f}  threshold={fedprox_thresh:.2f}")
if has_fedavg:
    print(f"FedAvg   ROC-AUC={fedavg_roc:.4f}  PR-AUC={fedavg_pr:.4f}  threshold={fedavg_thresh:.2f}")

print("\nFedProx Classification Report:")
print(classification_report(y_test_np, fedprox_preds,
      target_names=["Legitimate", "Fraud"], digits=4, zero_division=0))

# ─── Styles ──────────────────────────────────────────
C_FEDPROX = "#2563eb"
C_FEDAVG  = "#d97706"
C_RANDOM  = "#94a3b8"
LSTYLE    = dict(linewidth=2.2)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.right": False,
    "axes.spines.top":   False,
})


def plot_cm(cm, title, filepath, cmap="Blues"):
    labels = ["Legitimate", "Fraud"]
    fig, ax = plt.subplots(figsize=(5, 4.5))
    im = ax.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set(xticks=[0, 1], yticks=[0, 1],
           xticklabels=labels, yticklabels=labels,
           xlabel="Predicted Label", ylabel="True Label", title=title)
    thresh = cm.max() / 2.
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{cm[i,j]:,}", ha="center", va="center",
                    fontsize=14, fontweight="bold",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {filepath}")


# 1. Confusion matrices
print("\n--- Confusion Matrices ---")
plot_cm(confusion_matrix(y_test_np, fedprox_preds),
        f"FedProx DNN — Confusion Matrix\n(threshold >= {fedprox_thresh:.2f})",
        FIG_DIR / "fedprox_confusion_matrix.png", cmap="Blues")

if has_fedavg:
    plot_cm(confusion_matrix(y_test_np, fedavg_preds),
            f"FedAvg DNN — Confusion Matrix\n(threshold >= {fedavg_thresh:.2f})",
            FIG_DIR / "fedavg_confusion_matrix.png", cmap="Oranges")

# 2. ROC curves
print("\n--- ROC Curves ---")
fig, ax = plt.subplots(figsize=(7, 5.5))
fpr_fp, tpr_fp, _ = roc_curve(y_test_np, fedprox_probs)
ax.plot(fpr_fp, tpr_fp, color=C_FEDPROX,
        label=f"FedProx DNN (AUC = {fedprox_roc:.4f})", **LSTYLE)
if has_fedavg:
    fpr_fa, tpr_fa, _ = roc_curve(y_test_np, fedavg_probs)
    ax.plot(fpr_fa, tpr_fa, color=C_FEDAVG,
            label=f"FedAvg DNN (AUC = {fedavg_roc:.4f})", **LSTYLE)
ax.plot([0, 1], [0, 1], "--", color=C_RANDOM,
        label="Random Baseline (AUC = 0.5000)", linewidth=1.4)
ax.set(xlabel="False Positive Rate", ylabel="True Positive Rate",
       title="ROC Curve — Federated Models (IEEE-CIS Test Set)")
ax.legend(loc="lower right", fontsize=9)
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(FIG_DIR / "roc_curve_federated.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {FIG_DIR / 'roc_curve_federated.png'}")

# 3. Precision-Recall curves
print("\n--- Precision-Recall Curves ---")
fig, ax = plt.subplots(figsize=(7, 5.5))
prec_fp, rec_fp, _ = precision_recall_curve(y_test_np, fedprox_probs)
ax.plot(rec_fp, prec_fp, color=C_FEDPROX,
        label=f"FedProx DNN (AP = {fedprox_pr:.4f})", **LSTYLE)
if has_fedavg:
    prec_fa, rec_fa, _ = precision_recall_curve(y_test_np, fedavg_probs)
    ax.plot(rec_fa, prec_fa, color=C_FEDAVG,
            label=f"FedAvg DNN (AP = {fedavg_pr:.4f})", **LSTYLE)
baseline = y_test_np.mean()
ax.axhline(baseline, color=C_RANDOM, linestyle="--", linewidth=1.4,
           label=f"Random Baseline (AP = {baseline:.4f})")
ax.set(xlabel="Recall", ylabel="Precision",
       title="Precision-Recall Curve — Federated Models (IEEE-CIS Test Set)")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(FIG_DIR / "precision_recall_federated.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {FIG_DIR / 'precision_recall_federated.png'}")

# 4. Performance comparison bar chart
print("\n--- Model Performance Comparison ---")


def get_metrics(y_true, probs, thresh):
    preds = (probs >= thresh).astype(int)
    return {
        "ROC-AUC":   roc_auc_score(y_true, probs),
        "PR-AUC":    average_precision_score(y_true, probs),
        "F1":        f1_score(y_true, preds, zero_division=0),
        "Precision": precision_score(y_true, preds, zero_division=0),
        "Recall":    recall_score(y_true, preds, zero_division=0),
    }


metrics_fp = get_metrics(y_test_np, fedprox_probs, fedprox_thresh)
print("FedProx metrics:", {k: round(v, 4) for k, v in metrics_fp.items()})

metric_names = ["ROC-AUC", "PR-AUC", "F1", "Precision", "Recall"]
x = np.arange(len(metric_names))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5.5))
if has_fedavg:
    metrics_fa = get_metrics(y_test_np, fedavg_probs, fedavg_thresh)
    print("FedAvg metrics :", {k: round(v, 4) for k, v in metrics_fa.items()})
    bars_fp = ax.bar(x - width / 2, [metrics_fp[m] for m in metric_names],
                     width, label="FedProx DNN", color=C_FEDPROX, alpha=0.88)
    bars_fa = ax.bar(x + width / 2, [metrics_fa[m] for m in metric_names],
                     width, label="FedAvg DNN",  color=C_FEDAVG,  alpha=0.88)
    for bar in list(bars_fp) + list(bars_fa):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.005,
                f"{bar.get_height():.3f}", ha="center", va="bottom",
                fontsize=7.5, fontweight="bold")
else:
    bars_fp = ax.bar(x, [metrics_fp[m] for m in metric_names],
                     width * 1.5, label="FedProx DNN", color=C_FEDPROX, alpha=0.88)
    for bar in bars_fp:
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.005,
                f"{bar.get_height():.3f}", ha="center", va="bottom",
                fontsize=8, fontweight="bold")

ax.set(xticks=x, xticklabels=metric_names, ylabel="Score", ylim=(0, 1.12),
       title="Model Performance Comparison — Federated Learning (IEEE-CIS Test Set)")
ax.legend(loc="upper right", fontsize=9)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(FIG_DIR / "model_performance_comparison.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {FIG_DIR / 'model_performance_comparison.png'}")

# 5. SHAP Feature Importance
print("\n--- SHAP Feature Importance ---")
try:
    import shap

    rng = np.random.RandomState(42)
    bg_idx = rng.choice(len(X_test), min(100, len(X_test)), replace=False)
    ex_idx = rng.choice(len(X_test), min(50,  len(X_test)), replace=False)

    bg_tensor = torch.tensor(X_test.iloc[bg_idx].to_numpy(), dtype=torch.float32).to(DEVICE)
    ex_tensor = torch.tensor(X_test.iloc[ex_idx].to_numpy(), dtype=torch.float32).to(DEVICE)

    fedprox_model.eval()
    explainer   = shap.GradientExplainer(fedprox_model, bg_tensor)
    shap_values = explainer.shap_values(ex_tensor)

    vals = np.squeeze(np.asarray(shap_values))
    if vals.ndim == 1:
        vals = vals.reshape(1, -1)

    importance = np.mean(np.abs(vals), axis=0)
    imp_df = pd.DataFrame({
        "feature":       list(X_test.columns),
        "mean_abs_shap": importance,
    }).sort_values("mean_abs_shap", ascending=False)

    csv_path = FIG_DIR / "fedprox_shap_feature_importance.csv"
    imp_df.to_csv(csv_path, index=False)
    print(f"  Saved CSV: {csv_path}")

    top = imp_df.head(20).sort_values("mean_abs_shap")
    colors = plt.cm.Blues(np.linspace(0.35, 0.9, len(top)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top["feature"], top["mean_abs_shap"], color=colors)
    ax.set(xlabel="Mean |SHAP value| (logit output)", ylabel="Feature",
           title="FedProx DNN — Top 20 Most Important Features\n"
                 "(SHAP GradientExplainer, IEEE-CIS Test Set)")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    png_path = FIG_DIR / "fedprox_shap_feature_importance.png"
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved PNG: {png_path}")

    print("\nTop 10 features by mean |SHAP|:")
    print(imp_df.head(10).to_string(index=False))

except ImportError:
    print("  shap not installed. Skipping. Install with: pip install shap")
except Exception as e:
    import traceback
    print(f"  SHAP failed: {e}")
    traceback.print_exc()

print("\n" + "="*55)
print("All figures regenerated successfully.")
print(f"Output directory: {FIG_DIR}")

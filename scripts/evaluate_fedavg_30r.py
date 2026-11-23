# ============================================================
# scripts/evaluate_fedavg_30r.py
#
# Fair, side-by-side evaluation of:
#   1. models/fedavg_global_dnn_30r.pth  (new FedAvg checkpoint)
#   2. models/fedprox_global_dnn.pth     (existing FedProx checkpoint)
#
# Protocol (research-compliant):
#   • Thresholds are selected using VALIDATION data only.
#   • Test data is used ONLY for final metric reporting.
#   • Both models share identical preprocessing, feature order,
#     validation set, and test set.
#   • ROC-AUC and PR-AUC are computed from continuous probability
#     scores, NOT from thresholded binary predictions.
#   • No target accuracy / AUC is promised or manipulated.
#
# Deliverables produced:
#   reports/figures/fedavg_30r_vs_fedprox_comparison.md
#   reports/figures/roc_curve_30r_comparison.png
#   reports/figures/pr_curve_30r_comparison.png
#   reports/figures/confusion_matrix_fedavg_30r.png
#   reports/figures/confusion_matrix_fedprox_30r.png
# ============================================================

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import math
import numpy as np
import pandas as pd
import torch
import warnings
from pathlib import Path

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
)

from federated.model import FraudDNN

# ── Paths ──────────────────────────────────────────────────────
DATA_DIR        = Path("data/processed")
MODEL_DIR       = Path("models")
FIG_DIR         = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

FEDAVG_30R_PATH = MODEL_DIR / "fedavg_global_dnn_30r.pth"
FEDPROX_PATH    = MODEL_DIR / "fedprox_global_dnn.pth"
INPUT_SIZE      = 421

# ── Load data (identical for both models) ─────────────────────
print("=" * 65)
print("  Loading validation and test data …")
print("=" * 65)

X_val = pd.read_pickle(DATA_DIR / "X_val_dnn.pkl")
y_val = pd.read_pickle(DATA_DIR / "y_val_dnn.pkl")
X_test = pd.read_pickle(DATA_DIR / "X_test_dnn.pkl")
y_test = pd.read_pickle(DATA_DIR / "y_test_dnn.pkl")

X_val_arr  = X_val.to_numpy(dtype="float32")
y_val_arr  = np.asarray(y_val).reshape(-1).astype(int)
X_test_arr = X_test.to_numpy(dtype="float32")
y_test_arr = np.asarray(y_test).reshape(-1).astype(int)

print(f"  Validation : {len(y_val_arr):>8,} rows  |  fraud = {y_val_arr.sum():>5,}  ({y_val_arr.mean()*100:.2f}%)")
print(f"  Test       : {len(y_test_arr):>8,} rows  |  fraud = {y_test_arr.sum():>5,}  ({y_test_arr.mean()*100:.2f}%)")
print()

# ── Feature order guard ────────────────────────────────────────
val_cols  = list(X_val.columns)
test_cols = list(X_test.columns)
assert val_cols == test_cols, (
    "Validation and test feature columns differ – check preprocessing."
)
print(f"  Feature count: {len(val_cols)}  (identical for val and test)  ✓")
print()


# ── Helper: load model and run inference ──────────────────────

def load_and_infer(model_path: Path, X: np.ndarray) -> np.ndarray:
    """Load FraudDNN checkpoint, run sigmoid inference, return probs."""
    if not model_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {model_path}")

    model = FraudDNN(input_size=INPUT_SIZE)
    state = torch.load(model_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()

    X_tensor = torch.tensor(X, dtype=torch.float32)
    with torch.no_grad():
        logits = model(X_tensor).squeeze(-1)
        probs  = torch.sigmoid(logits).numpy()

    # Sanity checks
    assert probs.shape == (len(X),), f"Output shape mismatch: {probs.shape}"
    if not np.all(np.isfinite(probs)):
        raise RuntimeError(f"Non-finite probabilities from {model_path.name}")
    if probs.std() < 1e-6:
        warnings.warn(
            f"{model_path.name}: probability std < 1e-6 "
            "(outputs may be nearly constant).",
            RuntimeWarning,
        )
    return probs


# ── Helper: select threshold on VALIDATION data only ──────────

def select_threshold_val(val_probs: np.ndarray, y_val: np.ndarray) -> float:
    """
    Sweep thresholds 0.05 → 0.95 (step 0.01).
    Return the threshold that maximises F1 on the VALIDATION set.
    Test data is never touched during this search.
    """
    best_t, best_f1 = 0.5, -1.0
    for t in np.arange(0.05, 0.96, 0.01):
        preds = (val_probs >= t).astype(int)
        f = f1_score(y_val, preds, zero_division=0)
        if f > best_f1:
            best_f1, best_t = f, float(t)
    return best_t


# ── Helper: full metric suite ──────────────────────────────────

def evaluate(
    label: str,
    model_path: Path,
    X_val: np.ndarray,
    y_val: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict:

    print(f"\n{'='*65}")
    print(f"  Evaluating: {label}")
    print(f"  Checkpoint: {model_path}")
    print(f"{'='*65}")

    # Inference
    val_probs  = load_and_infer(model_path, X_val)
    test_probs = load_and_infer(model_path, X_test)

    print(f"  Val  prob distribution  — mean={val_probs.mean():.4f}  "
          f"std={val_probs.std():.4f}  min={val_probs.min():.4f}  max={val_probs.max():.4f}")
    print(f"  Test prob distribution  — mean={test_probs.mean():.4f}  "
          f"std={test_probs.std():.4f}  min={test_probs.min():.4f}  max={test_probs.max():.4f}")

    # Threshold selection (validation only)
    best_t = select_threshold_val(val_probs, y_val)
    val_preds_best = (val_probs >= best_t).astype(int)
    val_f1 = f1_score(y_val, val_preds_best, zero_division=0)
    print(f"\n  Selected threshold (val F1-max) : {best_t:.2f}  (val F1={val_f1:.4f})")

    # Apply threshold to TEST set
    test_preds = (test_probs >= best_t).astype(int)

    # Metrics from continuous scores (ROC-AUC, PR-AUC)
    roc_auc  = roc_auc_score(y_test, test_probs)
    pr_auc   = average_precision_score(y_test, test_probs)

    # Metrics from thresholded predictions
    acc      = accuracy_score(y_test, test_preds)
    prec     = precision_score(y_test, test_preds, zero_division=0)
    rec      = recall_score(y_test, test_preds, zero_division=0)
    f1       = f1_score(y_test, test_preds, zero_division=0)
    cm       = confusion_matrix(y_test, test_preds)

    print(f"\n  Test ROC-AUC        : {roc_auc:.4f}   (from continuous scores)")
    print(f"  Test PR-AUC         : {pr_auc:.4f}   (from continuous scores)")
    print(f"  Test Accuracy       : {acc:.4f}")
    print(f"  Fraud Precision     : {prec:.4f}")
    print(f"  Fraud Recall        : {rec:.4f}")
    print(f"  Fraud F1-score      : {f1:.4f}")
    print(f"\n  Confusion Matrix (threshold={best_t:.2f}):")
    print(f"    TN={cm[0,0]:>6,}   FP={cm[0,1]:>5,}")
    print(f"    FN={cm[1,0]:>6,}   TP={cm[1,1]:>5,}")
    print()
    print(classification_report(
        y_test, test_preds,
        target_names=["Legitimate", "Fraud"],
        digits=4, zero_division=0,
    ))

    # ROC curve arrays
    fpr, tpr, _ = roc_curve(y_test, test_probs)
    # PR curve arrays
    prec_curve, rec_curve, _ = precision_recall_curve(y_test, test_probs)

    return {
        "label":       label,
        "threshold":   best_t,
        "roc_auc":     roc_auc,
        "pr_auc":      pr_auc,
        "accuracy":    acc,
        "precision":   prec,
        "recall":      rec,
        "f1":          f1,
        "cm":          cm,
        "fpr":         fpr,
        "tpr":         tpr,
        "prec_curve":  prec_curve,
        "rec_curve":   rec_curve,
        "test_probs":  test_probs,
        "val_probs":   val_probs,
    }


# ── Run evaluations ────────────────────────────────────────────

results_fedavg  = evaluate(
    label="FedAvg (30 rounds)",
    model_path=FEDAVG_30R_PATH,
    X_val=X_val_arr,  y_val=y_val_arr,
    X_test=X_test_arr, y_test=y_test_arr,
)

results_fedprox = evaluate(
    label="FedProx (30 rounds)",
    model_path=FEDPROX_PATH,
    X_val=X_val_arr,  y_val=y_val_arr,
    X_test=X_test_arr, y_test=y_test_arr,
)


# ── Comparison table ───────────────────────────────────────────

def print_comparison(r1: dict, r2: dict):
    print("\n" + "=" * 65)
    print("  COMPARISON TABLE")
    print("=" * 65)
    hdr = f"  {'Metric':<24}  {r1['label']:>20}  {r2['label']:>20}"
    sep = f"  {'-'*24}  {'-'*20}  {'-'*20}"
    print(hdr)
    print(sep)

    rows = [
        ("ROC-AUC",         "roc_auc"),
        ("PR-AUC",          "pr_auc"),
        ("Accuracy",        "accuracy"),
        ("Fraud Precision",  "precision"),
        ("Fraud Recall",     "recall"),
        ("Fraud F1",         "f1"),
        ("Val Threshold",    "threshold"),
    ]
    for name, key in rows:
        v1 = r1[key]
        v2 = r2[key]
        print(f"  {name:<24}  {v1:>20.4f}  {v2:>20.4f}")

    print(sep)
    # Confusion matrix side-by-side
    cm1, cm2 = r1["cm"], r2["cm"]
    print(f"  {'Confusion Matrix':<24}")
    print(f"    {'TN':<6} {cm1[0,0]:>7,}  FP {cm1[0,1]:>6,}    |    TN {cm2[0,0]:>7,}  FP {cm2[0,1]:>6,}")
    print(f"    {'FN':<6} {cm1[1,0]:>7,}  TP {cm1[1,1]:>6,}    |    FN {cm2[1,0]:>7,}  TP {cm2[1,1]:>6,}")
    print("=" * 65)


print_comparison(results_fedavg, results_fedprox)


# ── Plots ──────────────────────────────────────────────────────

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib.colors import LinearSegmentedColormap
    import itertools

    # ── 1. ROC Curve comparison ────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 6))
    for res, color in [
        (results_fedavg,  "#2563EB"),
        (results_fedprox, "#DC2626"),
    ]:
        ax.plot(
            res["fpr"], res["tpr"],
            linewidth=2.0, color=color,
            label=f"{res['label']}  (AUC={res['roc_auc']:.4f})",
        )
    ax.plot([0, 1], [0, 1], "k--", linewidth=1.0, label="Random (AUC=0.5)")
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curve Comparison – FedAvg 30R vs FedProx", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    roc_path = FIG_DIR / "roc_curve_30r_comparison.png"
    fig.tight_layout()
    fig.savefig(roc_path, dpi=150)
    plt.close(fig)
    print(f"\nROC curve saved → {roc_path}")

    # ── 2. Precision-Recall Curve comparison ───────────────────
    fig, ax = plt.subplots(figsize=(8, 6))
    for res, color in [
        (results_fedavg,  "#2563EB"),
        (results_fedprox, "#DC2626"),
    ]:
        ax.plot(
            res["rec_curve"], res["prec_curve"],
            linewidth=2.0, color=color,
            label=f"{res['label']}  (PR-AUC={res['pr_auc']:.4f})",
        )
    # Baseline = fraud prevalence
    baseline = y_test_arr.mean()
    ax.axhline(baseline, color="gray", linestyle="--", linewidth=1.0,
               label=f"Random baseline (prevalence={baseline:.4f})")
    ax.set_xlabel("Recall", fontsize=12)
    ax.set_ylabel("Precision", fontsize=12)
    ax.set_title("Precision-Recall Curve – FedAvg 30R vs FedProx", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    pr_path = FIG_DIR / "pr_curve_30r_comparison.png"
    fig.tight_layout()
    fig.savefig(pr_path, dpi=150)
    plt.close(fig)
    print(f"PR curve saved → {pr_path}")

    # ── 3. Confusion matrices ──────────────────────────────────
    def plot_cm(cm: np.ndarray, title: str, save_path: Path):
        labels = ["Legitimate", "Fraud"]
        fig, ax = plt.subplots(figsize=(5, 4))
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        fig.colorbar(im, ax=ax)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(labels, fontsize=11)
        ax.set_yticklabels(labels, fontsize=11)
        ax.set_xlabel("Predicted label", fontsize=11)
        ax.set_ylabel("True label", fontsize=11)
        ax.set_title(title, fontsize=12)
        thresh = cm.max() / 2.0
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            ax.text(
                j, i, f"{cm[i, j]:,}",
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=12,
            )
        fig.tight_layout()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
        plt.close(fig)
        print(f"Confusion matrix saved → {save_path}")

    plot_cm(
        results_fedavg["cm"],
        f"FedAvg 30R – Confusion Matrix (threshold={results_fedavg['threshold']:.2f})",
        FIG_DIR / "confusion_matrix_fedavg_30r.png",
    )
    plot_cm(
        results_fedprox["cm"],
        f"FedProx – Confusion Matrix (threshold={results_fedprox['threshold']:.2f})",
        FIG_DIR / "confusion_matrix_fedprox_30r.png",
    )

    print("\nAll figures saved to:", FIG_DIR)

except ImportError:
    print("\nWARNING: matplotlib not available – plots skipped.")
except Exception as exc:
    print(f"\nWARNING: Plot generation failed: {exc}")


# ── Markdown comparison report ─────────────────────────────────

def write_comparison_report(r1: dict, r2: dict, out_path: Path):
    cm1, cm2 = r1["cm"], r2["cm"]
    lines = [
        "# FedAvg 30R vs FedProx – Model Comparison Report",
        "",
        f"> Generated on run of `scripts/evaluate_fedavg_30r.py`",
        "",
        "## Evaluation Protocol",
        "",
        "- **Validation set**: used only to select the decision threshold (max-F1 sweep 0.05 → 0.95).",
        "- **Test set**: used only for final metric reporting.",
        "- **ROC-AUC** and **PR-AUC** are computed from continuous probability scores, not thresholded predictions.",
        "- Both models share identical preprocessing, feature order, and data splits.",
        "- No target accuracy / AUC was guaranteed or manipulated.",
        "",
        "## Metric Comparison",
        "",
        f"| Metric | {r1['label']} | {r2['label']} |",
        "|--------|-------------|-------------|",
        f"| ROC-AUC | {r1['roc_auc']:.4f} | {r2['roc_auc']:.4f} |",
        f"| PR-AUC | {r1['pr_auc']:.4f} | {r2['pr_auc']:.4f} |",
        f"| Accuracy | {r1['accuracy']:.4f} | {r2['accuracy']:.4f} |",
        f"| Fraud Precision | {r1['precision']:.4f} | {r2['precision']:.4f} |",
        f"| Fraud Recall | {r1['recall']:.4f} | {r2['recall']:.4f} |",
        f"| Fraud F1-score | {r1['f1']:.4f} | {r2['f1']:.4f} |",
        f"| Val Threshold | {r1['threshold']:.2f} | {r2['threshold']:.2f} |",
        "",
        "## Confusion Matrices",
        "",
        f"### {r1['label']}  (threshold = {r1['threshold']:.2f})",
        "",
        "| | Pred Legit | Pred Fraud |",
        "|---|---|---|",
        f"| **True Legit** | {cm1[0,0]:,} | {cm1[0,1]:,} |",
        f"| **True Fraud** | {cm1[1,0]:,} | {cm1[1,1]:,} |",
        "",
        f"### {r2['label']}  (threshold = {r2['threshold']:.2f})",
        "",
        "| | Pred Legit | Pred Fraud |",
        "|---|---|---|",
        f"| **True Legit** | {cm2[0,0]:,} | {cm2[0,1]:,} |",
        f"| **True Fraud** | {cm2[1,0]:,} | {cm2[1,1]:,} |",
        "",
        "## Notes on Figures",
        "",
        "- `reports/figures/roc_curve_30r_comparison.png` – overlaid ROC curves.",
        "- `reports/figures/pr_curve_30r_comparison.png` – overlaid PR curves.",
        "- `reports/figures/confusion_matrix_fedavg_30r.png` – FedAvg confusion matrix.",
        "- `reports/figures/confusion_matrix_fedprox_30r.png` – FedProx confusion matrix.",
        "- `reports/figures/fedavg_30r_training_loss.png` – per-round aggregated eval loss.",
        "",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Comparison report saved → {out_path}")


REPORT_PATH = Path("reports/figures") / "fedavg_30r_vs_fedprox_comparison.md"
write_comparison_report(results_fedavg, results_fedprox, REPORT_PATH)

print("\n" + "=" * 65)
print("  Evaluation complete.")
print("=" * 65)


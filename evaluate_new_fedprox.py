"""
evaluate_new_fedprox.py
=======================
Evaluates the newly retrained fedprox_global_dnn.pth against the old
backup checkpoint on the held-out X_val_dnn.pkl set.

Metrics reported:
  - ROC-AUC
  - PR-AUC (average precision)
  - Precision / Recall / F1 at optimal threshold (maximises F1 on val set)
  - Prediction probability distribution (mean, std, min, max)
  - Confusion matrix

The old backup filename is inferred from the backup created before training.
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import glob
import numpy as np
import pandas as pd
import torch
from pathlib import Path
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)

from federated.model import FraudDNN

DATA_DIR   = Path("data/processed")
MODEL_DIR  = Path("models")
NEW_PATH   = MODEL_DIR / "fedprox_global_dnn.pth"

# ── Find the backup created immediately before this run ───────────────────────
backups = sorted(glob.glob(str(MODEL_DIR / "fedprox_global_dnn.pth.bak_*")))
if not backups:
    print("WARNING: no backup checkpoint found; old-model comparison skipped.")
    OLD_PATH = None
else:
    OLD_PATH = Path(backups[-1])
    print(f"Comparing against backup: {OLD_PATH.name}")

# ── Load validation data ──────────────────────────────────────────────────────
print("Loading validation data…")
X_val = pd.read_pickle(DATA_DIR / "X_val_dnn.pkl")
y_val = pd.read_pickle(DATA_DIR / "y_val_dnn.pkl")
X_arr = X_val.to_numpy(dtype="float32")
y_arr = np.asarray(y_val).reshape(-1).astype(int)

print(f"  Validation rows : {len(y_arr):,}")
print(f"  Fraud cases     : {y_arr.sum():,}  ({y_arr.mean()*100:.2f}%)")


# ── Helper: evaluate one checkpoint ──────────────────────────────────────────
def evaluate_checkpoint(path: Path, label: str) -> dict:
    model = FraudDNN(input_size=421)
    state = torch.load(path, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()

    X_t = torch.tensor(X_arr)
    with torch.no_grad():
        logits = model(X_t).squeeze(-1)
        probs  = torch.sigmoid(logits).numpy()

    # Select threshold that maximises F1 on the same val set
    best_t, best_f1 = 0.5, -1.0
    for t in np.arange(0.05, 0.96, 0.01):
        preds = (probs >= t).astype(int)
        f = f1_score(y_arr, preds, zero_division=0)
        if f > best_f1:
            best_f1, best_t = f, t

    preds_best = (probs >= best_t).astype(int)
    roc   = roc_auc_score(y_arr, probs)
    prauc = average_precision_score(y_arr, probs)
    prec  = precision_score(y_arr, preds_best, zero_division=0)
    rec   = recall_score(y_arr, preds_best, zero_division=0)
    f1    = f1_score(y_arr, preds_best, zero_division=0)
    cm    = confusion_matrix(y_arr, preds_best)

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Prob distribution — mean: {probs.mean():.4f}  std: {probs.std():.4f}"
          f"  min: {probs.min():.4f}  max: {probs.max():.4f}")
    print(f"  ROC-AUC : {roc:.4f}")
    print(f"  PR-AUC  : {prauc:.4f}")
    print(f"  Best threshold (max-F1 on val): {best_t:.2f}")
    print(f"  Precision: {prec:.4f}  Recall: {rec:.4f}  F1: {f1:.4f}")
    print(f"  Confusion matrix (TN FP / FN TP):")
    print(f"    TN={cm[0,0]:>6,}  FP={cm[0,1]:>5,}")
    print(f"    FN={cm[1,0]:>6,}  TP={cm[1,1]:>5,}")
    print()
    print(classification_report(
        y_arr, preds_best,
        target_names=["Legitimate", "Fraud"],
        digits=4, zero_division=0,
    ))
    return {"roc_auc": roc, "pr_auc": prauc, "f1": f1, "prob_std": float(probs.std())}


# ── Evaluate new checkpoint ───────────────────────────────────────────────────
new_results = evaluate_checkpoint(NEW_PATH, f"NEW  — {NEW_PATH.name}")

# ── Evaluate old checkpoint ───────────────────────────────────────────────────
old_results = None
if OLD_PATH:
    old_results = evaluate_checkpoint(OLD_PATH, f"OLD  — {OLD_PATH.name}")

# ── Comparison summary ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  COMPARISON SUMMARY")
print("="*60)
print(f"  {'Metric':<20}  {'OLD':>10}  {'NEW':>10}  {'Change':>10}")
print(f"  {'-'*20}  {'-'*10}  {'-'*10}  {'-'*10}")

metrics = ["roc_auc", "pr_auc", "f1", "prob_std"]
labels  = ["ROC-AUC", "PR-AUC", "F1", "Prob std"]
for m, l in zip(metrics, labels):
    old_v = old_results[m] if old_results else float("nan")
    new_v = new_results[m]
    chg   = new_v - old_v
    arrow = "+" if chg > 0 else ""
    print(f"  {l:<20}  {old_v:>10.4f}  {new_v:>10.4f}  {arrow}{chg:>9.4f}")

print()
if new_results["roc_auc"] > 0.70:
    print("  RESULT: FIX SUCCEEDED — model produces discriminative predictions.")
elif new_results["roc_auc"] > 0.55:
    print("  RESULT: PARTIAL IMPROVEMENT — model has some discrimination but needs more training.")
elif new_results["roc_auc"] <= 0.50:
    print("  RESULT: NO IMPROVEMENT — investigate next likely cause.")
else:
    print(f"  RESULT: ROC-AUC = {new_results['roc_auc']:.4f} — marginal improvement.")

print("="*60)

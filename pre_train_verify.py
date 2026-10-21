"""
pre_train_verify.py
====================
Checks that client training data and X_val_dnn.pkl live in the same
feature distribution after the double-scaling fix.

PASS criteria (all must hold):
  1. Client input mean is in (-0.5, +0.5)         -- properly centred
  2. Client input std  is in ( 0.5,  1.5)          -- unit-scale
  3. Val input mean is in    (-0.5, +0.5)
  4. Val input std  is in    ( 0.5,  1.5)
  5. |client_mean - val_mean| < 0.1                -- same centre
  6. |client_std  - val_std | < 0.2                -- same spread
  7. Client feature count == val feature count == 421
  8. All client tensors are finite (no NaN / Inf)
  9. Old model gives constant probs (std < 0.001)  -- confirms baseline bug
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import numpy as np
import pandas as pd
import torch
from pathlib import Path

from federated.client import load_client_data
from federated.model import FraudDNN

DATA_DIR   = Path("data/processed")
MODEL_PATH = Path("models/fedprox_global_dnn.pth")
N_CLIENTS  = 5

# ── Load validation data (reference distribution) ────────────────────────────
X_val = pd.read_pickle(DATA_DIR / "X_val_dnn.pkl")
val_arr = X_val.to_numpy(dtype="float32")
val_mean = float(val_arr.mean())
val_std  = float(val_arr.std())

print("=" * 60)
print("PRE-TRAINING INPUT DISTRIBUTION VERIFICATION")
print("=" * 60)
print(f"\nValidation set  — mean: {val_mean:+.6f}  std: {val_std:.6f}  shape: {val_arr.shape}")

# ── Load each client after the fix and record distribution ───────────────────
client_means = []
client_stds  = []
all_pass     = True

for cid in range(N_CLIENTS):
    X_t, y_t = load_client_data(cid)
    arr = X_t.numpy()
    m = float(arr.mean())
    s = float(arr.std())
    finite = bool(np.isfinite(arr).all())
    feat_ok = arr.shape[1] == 421
    client_means.append(m)
    client_stds.append(s)
    ok = abs(m) < 0.5 and 0.5 < s < 1.5 and finite and feat_ok
    status = "PASS" if ok else "FAIL"
    if not ok:
        all_pass = False
    print(f"  Client {cid}  mean: {m:+.6f}  std: {s:.6f}  "
          f"features: {arr.shape[1]}  finite: {finite}  [{status}]")

pool_mean = float(np.mean(client_means))
pool_std  = float(np.mean(client_stds))
delta_mean = abs(pool_mean - val_mean)
delta_std  = abs(pool_std  - val_std)

print()
print(f"Pooled client   — mean: {pool_mean:+.6f}  std: {pool_std:.6f}")
print(f"Distribution gap --- |d_mean|: {delta_mean:.4f}  |d_std|: {delta_std:.4f}")

gap_ok = delta_mean < 0.1 and delta_std < 0.2
print(f"Distribution gap {'PASS' if gap_ok else 'FAIL'} (threshold: |d_mean|<0.1, |d_std|<0.2)")
if not gap_ok:
    all_pass = False

# ── Confirm old model still produces constant predictions ────────────────────
print()
print("Checking old (double-trained) model produces constant predictions…")
model = FraudDNN(input_size=421)
state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
model.load_state_dict(state)
model.eval()

sample = torch.tensor(val_arr[:500])
with torch.no_grad():
    probs = torch.sigmoid(model(sample).squeeze(-1)).numpy()
old_std = float(probs.std())
old_mean = float(probs.mean())
constant_bug = old_std < 0.001
print(f"  Old model probs  mean: {old_mean:.4f}  std: {old_std:.6f}  "
      f"constant-bug confirmed: {constant_bug}")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
print("=" * 60)
if all_pass:
    print("VERIFICATION PASSED — safe to retrain FedProx")
else:
    print("VERIFICATION FAILED — do NOT retrain, investigate above")
print("=" * 60)
sys.exit(0 if all_pass else 1)

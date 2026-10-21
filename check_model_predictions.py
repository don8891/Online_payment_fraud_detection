import numpy as np
import pandas as pd
import torch
from pathlib import Path
from sklearn.metrics import roc_auc_score, average_precision_score
from federated.model import FraudDNN

root = Path(".")
data = root / "data" / "processed"
model_path = root / "models" / "fedprox_global_dnn.pth"

X_val = pd.read_pickle(data / "X_val_dnn.pkl")
y_val = pd.read_pickle(data / "y_val_dnn.pkl")

X = X_val.to_numpy(dtype=np.float32)
y = np.asarray(y_val).reshape(-1).astype(int)

model = FraudDNN(input_size=X.shape[1])
state = torch.load(model_path, map_location="cpu", weights_only=True)
model.load_state_dict(state)
model.eval()

with torch.no_grad():
    logits = model(torch.tensor(X, dtype=torch.float32)).squeeze(-1)
    probs = torch.sigmoid(logits).numpy()

print("=== VALIDATION LABELS ===")
print("Rows:", len(y))
print("Fraud cases:", int(y.sum()))
print("Fraud rate:", round(float(y.mean()), 4))

print("\n=== MODEL PROBABILITIES ===")
print("Min:", float(probs.min()))
print("Max:", float(probs.max()))
print("Mean:", float(probs.mean()))
print("Std:", float(probs.std()))
print("Unique rounded probabilities:", len(np.unique(np.round(probs, 4))))
print("First 20:", np.round(probs[:20], 4))

print("\n=== VALIDATION METRICS ===")
if len(np.unique(y)) == 2:
    print("ROC-AUC:", round(roc_auc_score(y, probs), 4))
    print("PR-AUC (average precision):",
          round(average_precision_score(y, probs), 4))
else:
    print("Cannot calculate metrics: validation labels contain only one class.")

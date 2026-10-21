
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
)
from sklearn.metrics import confusion_matrix
from federated.model import FraudDNN

# Load validation data
X_val = pd.read_pickle("data/processed/X_val.pkl")
y_val = pd.read_pickle("data/processed/y_val.pkl")

# Convert categorical columns consistently if necessary.
# Prefer the already-preprocessed DNN validation data.
try:
    X_val = pd.read_pickle("data/processed/X_val_dnn.pkl")
except FileNotFoundError:
    # X_val_dnn.pkl does not exist — fall back to X_val.pkl which
    # was already loaded above.  Ensure it uses the same feature
    # order and scaling as the data the clients were trained on.
    print(
        "[INFO] X_val_dnn.pkl not found – "
        "using X_val.pkl as validation features."
    )

try:
    y_val = pd.read_pickle("data/processed/y_val_dnn.pkl")
except FileNotFoundError:
    # The original validation labels are suitable if aligned.
    pass

if isinstance(y_val, pd.DataFrame):
    y_val = y_val.iloc[:, 0]

X = torch.tensor(
    X_val.to_numpy(dtype=np.float32),
    dtype=torch.float32
)

device = torch.device("cpu")
model = FraudDNN(input_size=X.shape[1]).to(device)

state = torch.load(
    "models/fedprox_global_dnn.pth",
    map_location=device,
    weights_only=True
)
model.load_state_dict(state)
model.eval()

with torch.no_grad():
    probabilities = torch.sigmoid(model(X).squeeze(1)).numpy()

y_true = np.asarray(y_val).reshape(-1).astype(int)

print("Validation ROC-AUC:", round(roc_auc_score(y_true, probabilities), 4))
print("Validation PR-AUC :", round(average_precision_score(y_true, probabilities), 4))
print("\nThreshold  Precision  Recall  F1")

for threshold in [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]:
    predictions = (probabilities >= threshold).astype(int)
    precision = precision_score(y_true, predictions, zero_division=0)
    recall = recall_score(y_true, predictions, zero_division=0)
    f1 = f1_score(y_true, predictions, zero_division=0)

    print(
        f"{threshold:>9.2f}  "
        f"{precision:>9.4f}  "
        f"{recall:>6.4f}  "
        f"{f1:>6.4f}"
    )

best_threshold = 0.90
print(f"\nSelected FedProx threshold: {best_threshold}")


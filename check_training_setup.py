import joblib
import pandas as pd
import torch
from pathlib import Path
from federated.model import FraudDNN

root = Path(".")
models = root / "models"
data = root / "data" / "processed"

X_train = pd.read_pickle(data / "X_train.pkl")
y_train = pd.read_pickle(data / "y_train.pkl")
X_val = pd.read_pickle(data / "X_val_dnn.pkl")
y_val = pd.read_pickle(data / "y_val_dnn.pkl")
X_test = pd.read_pickle(data / "X_test_dnn.pkl")
y_test = pd.read_pickle(data / "y_test_dnn.pkl")

medians = joblib.load(models / "fedprox_train_medians.pkl")
scaler = joblib.load(models / "fedprox_scaler.pkl")
mappings = joblib.load(models / "fedprox_category_mappings.pkl")

print("=== Dataset shapes ===")
print("X_train:", X_train.shape, "| y_train:", y_train.shape)
print("X_val:  ", X_val.shape, "| y_val:  ", y_val.shape)
print("X_test: ", X_test.shape, "| y_test: ", y_test.shape)

print("\n=== Training data ===")
print("Numeric columns:", len(X_train.select_dtypes(include="number").columns))
print("Non-numeric columns:", len(X_train.select_dtypes(exclude="number").columns))
print("Missing values:", int(X_train.isna().sum().sum()))
print("Training label counts:")
print(y_train.value_counts(dropna=False))

print("\n=== Preprocessing artifacts ===")
print("Median entries:", len(medians))
print("Category mapping entries:", len(mappings))
print("Scaler feature count:", getattr(scaler, "n_features_in_", "unknown"))

print("\n=== Feature compatibility ===")
print("Train feature count:", X_train.shape[1])
print("Validation feature count:", X_val.shape[1])
print("Test feature count:", X_test.shape[1])
print("Validation columns match train:", list(X_val.columns) == list(X_train.columns))
print("Test columns match train:", list(X_test.columns) == list(X_train.columns))

print("\n=== Model checkpoint ===")
model = FraudDNN(input_size=X_train.shape[1])
try:
    state = torch.load(models / "fedprox_global_dnn.pth", map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    print("Checkpoint matches model architecture: YES")
except Exception as exc:
    print("Checkpoint loading error:", repr(exc))

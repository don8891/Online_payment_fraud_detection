import joblib
import pandas as pd
import numpy as np
from pathlib import Path

root = Path(".")
models = root / "models"
data = root / "data" / "processed"

X_train = pd.read_pickle(data / "X_train.pkl")
medians = joblib.load(models / "fedprox_train_medians.pkl")
mappings = joblib.load(models / "fedprox_category_mappings.pkl")
scaler = joblib.load(models / "fedprox_scaler.pkl")

print("=== SCALER ===")
print("Feature count:", scaler.n_features_in_)
print("Mean values (first 10):", scaler.mean_[:10])
print("Scale values (first 10):", scaler.scale_[:10])

print("\n=== CATEGORY MAPPINGS ===")
for col, mapping in mappings.items():
    print(f"{col}: {len(mapping)} mapped categories")

print("\n=== MEDIANS ===")
print("Median count:", len(medians))
print("First 10 medians:")
print(medians.head(10))

print("\n=== TRAINING DATA BEFORE PREPROCESSING ===")
print("Shape:", X_train.shape)
print("Missing values:", int(X_train.isna().sum().sum()))
print("Categorical columns:", len(
    X_train.select_dtypes(exclude="number").columns
))

print("\n=== MAPPING COVERAGE ===")
for col, mapping in mappings.items():
    if col in X_train.columns:
        values = X_train[col].dropna()
        mapped = values.isin(mapping.keys()).mean() if len(values) else 0
        print(f"{col}: {mapped:.2%} of non-null values found in mapping")

print("\n=== VALIDATION MATRIX ===")
X_val = pd.read_pickle(data / "X_val_dnn.pkl")
print("Shape:", X_val.shape)
print("All numeric:", all(pd.api.types.is_numeric_dtype(t) for t in X_val.dtypes))
print("Missing values:", int(X_val.isna().sum().sum()))
print("Feature names match:", list(X_val.columns) == list(X_train.columns))

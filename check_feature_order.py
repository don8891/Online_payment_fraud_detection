import pandas as pd

data = "data/processed/"

X_train = pd.read_pickle(data + "X_train.pkl")
X_val = pd.read_pickle(data + "X_val_dnn.pkl")
X_test = pd.read_pickle(data + "X_test_dnn.pkl")

train_cols = list(X_train.columns)
val_cols = list(X_val.columns)
test_cols = list(X_test.columns)

print("=== First 15 training columns ===")
print(train_cols[:15])

print("\n=== First 15 validation columns ===")
print(val_cols[:15])

print("\n=== Validation columns in a different position ===")
for i, (a, b) in enumerate(zip(train_cols, val_cols)):
    if a != b:
        print(f"Position {i}: train={a!r}, validation={b!r}")
        if i >= 20:
            break

print("\n=== Columns missing from validation ===")
print([c for c in train_cols if c not in val_cols][:30])

print("\n=== Columns only in validation ===")
print([c for c in val_cols if c not in train_cols][:30])

print("\n=== Non-numeric training columns ===")
print(X_train.select_dtypes(exclude="number").columns.tolist())

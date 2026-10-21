import pandas as pd
from pathlib import Path

data = Path("data/processed")

X_train = pd.read_pickle(data / "X_train.pkl")
train_columns = list(X_train.columns)

for filename in ["X_val_dnn.pkl", "X_test_dnn.pkl"]:
    path = data / filename
    X = pd.read_pickle(path)

    if X.shape[1] != len(train_columns):
        raise ValueError(
            f"{filename}: {X.shape[1]} columns; "
            f"expected {len(train_columns)}. No changes made."
        )

    if list(X.columns) == list(range(len(train_columns))):
        X.columns = train_columns
        X.to_pickle(path)
        print(f"Repaired column names: {filename}")
    elif list(X.columns) == train_columns:
        print(f"Already correct: {filename}")
    else:
        raise ValueError(
            f"Unexpected column names in {filename}. "
            "No changes made."
        )

print("Finished.")

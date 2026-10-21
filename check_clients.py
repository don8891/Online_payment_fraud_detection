
import pandas as pd
from pathlib import Path

for i in range(5):
    folder = Path(f"federated/data/client_{i}")

    X = pd.read_pickle(folder / "X.pkl")
    y = pd.read_pickle(folder / "y.pkl")

    fraud_rate = y.mean() * 100

    print(f"\nClient {i}")
    print(f"Rows: {len(X)}")
    print(f"Features: {X.shape[1]}")
    print(f"Labels: {len(y)}")
    print(f"Fraud rate: {fraud_rate:.2f}%")

    assert len(X) == len(y), "Feature/label count mismatch"
    assert X.shape[1] == 421, "Expected 421 features"

print("\nAll five clients passed the basic checks.")

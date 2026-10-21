
import numpy as np
import pandas as pd
import torch

from federated.model import FraudDNN

X = pd.read_pickle(
    "data/processed/X_test_dnn.pkl"
)

checkpoint = "models/fedprox_global_dnn.pth"

print("Input shape:", X.shape)
print("Unique input rows:", np.unique(
    X.iloc[:1000].to_numpy(), axis=0
).shape[0])

model = FraudDNN(input_size=X.shape[1])

state = torch.load(
    checkpoint,
    map_location="cpu",
    weights_only=True
)

model.load_state_dict(state)
model.eval()

sample = X.iloc[:1000].to_numpy(dtype=np.float32)

with torch.no_grad():
    logits = model(torch.tensor(sample)).reshape(-1)
    probabilities = torch.sigmoid(logits).numpy()

print("Probability minimum:", probabilities.min())
print("Probability maximum:", probabilities.max())
print("Probability mean:", probabilities.mean())
print("Probability standard deviation:", probabilities.std())
print(
    "Unique probabilities:",
    np.unique(np.round(probabilities, 6)).size
)

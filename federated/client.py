
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

import flwr as fl

from federated.model import FraudDNN


# --------------------------------------------------
# Load one bank's local data
# --------------------------------------------------

def load_client_data(client_id):
    folder = f"federated/data/client_{client_id}"

    X = pd.read_pickle(f"{folder}/X.pkl")
    y = pd.read_pickle(f"{folder}/y.pkl")

    # --------------------------------------------------
    # client X.pkl files were saved by 04_dnn_baseline.ipynb AFTER
    # StandardScaler.fit_transform() was applied.  No further
    # preprocessing is needed here; applying the scaler a second time
    # would double-scale the inputs and produce out-of-distribution
    # values (~30 σ) that break model training.
    # --------------------------------------------------
    X_scaled = X.to_numpy(dtype="float32")

    X_tensor = torch.tensor(
        X_scaled,
        dtype=torch.float32
    )

    y_tensor = torch.tensor(
        y.values,
        dtype=torch.float32
    ).view(-1, 1)

    return X_tensor, y_tensor


# --------------------------------------------------
# Flower Client
# --------------------------------------------------

class FraudClient(fl.client.NumPyClient):

    def __init__(self, client_id):
        self.client_id = client_id

        self.X, self.y = load_client_data(client_id)

        self.model = FraudDNN(
            input_size=self.X.shape[1]
        )

        self.dataloader = DataLoader(
            TensorDataset(self.X, self.y),
            batch_size=512,
            shuffle=True
        )

        # Calculate class weight
        fraud_count = self.y.sum().item()
        legitimate_count = len(self.y) - fraud_count

        if fraud_count <= 0:
            raise ValueError(
                f"Client {client_id} has no fraud samples."
            )

        self.pos_weight = torch.tensor(
            [legitimate_count / fraud_count],
            dtype=torch.float32
        )

        print(f"Client {client_id} initialized")
        print(f"Samples: {len(self.X)}")
        print(f"Features: {self.X.shape[1]}")
        print(f"Fraud: {int(fraud_count)}")
        print(
            f"Fraud rate: {self.y.mean().item() * 100:.2f}%"
        )

    # --------------------------------------------------
    # Receive global model parameters
    # --------------------------------------------------

    def set_parameters(self, parameters):
        state_dict = self.model.state_dict()

        if len(parameters) != len(state_dict):
            raise ValueError(
                "Received parameter count does not match model."
            )

        for key, value in zip(state_dict.keys(), parameters):
            state_dict[key] = torch.as_tensor(
                value,
                dtype=state_dict[key].dtype
            )

        self.model.load_state_dict(state_dict)

    # --------------------------------------------------
    # Return local model parameters
    # --------------------------------------------------

    def get_parameters(self, config):
        return [
            value.detach().cpu().numpy()
            for value in self.model.state_dict().values()
        ]

    # --------------------------------------------------
    # Local training: FedAvg or FedProx
    # --------------------------------------------------

    def fit(self, parameters, config):

        # Load the current global model
        self.set_parameters(parameters)

        # Keep a fixed reference to the received global model
        global_model = FraudDNN(
            input_size=self.X.shape[1]
        )

        global_model.load_state_dict(self.model.state_dict())
        global_model.eval()

        for param in global_model.parameters():
            param.requires_grad_(False)

        # FedAvg defaults to mu=0; FedProx receives mu=0.01
        proximal_mu = float(config.get("proximal_mu", 0.0))

        if proximal_mu < 0:
            raise ValueError("proximal_mu cannot be negative.")

        epochs = int(config.get("local_epochs", 1))

        if epochs < 1:
            raise ValueError("local_epochs must be at least 1.")

        algorithm = "FedProx" if proximal_mu > 0.0 else "FedAvg"

        print(
            f"\nClient {self.client_id} "
            f"starting {algorithm} local training"
        )
        print(f"Proximal mu: {proximal_mu}")

        self.model.train()

        criterion = nn.BCEWithLogitsLoss(
            pos_weight=self.pos_weight
        )

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=0.001
        )

        # Local training loop
        for epoch in range(epochs):
            total_loss = 0.0

            for X_batch, y_batch in self.dataloader:
                optimizer.zero_grad()

                outputs = self.model(X_batch)

                classification_loss = criterion(
                    outputs,
                    y_batch
                )

                # Apply proximal penalty only for FedProx
                if proximal_mu > 0.0:
                    proximal_loss = torch.zeros(())

                    for local_param, global_param in zip(
                        self.model.parameters(),
                        global_model.parameters()
                    ):
                        proximal_loss = proximal_loss + torch.sum(
                            (local_param - global_param) ** 2
                        )

                    loss = (
                        classification_loss
                        + (proximal_mu / 2.0) * proximal_loss
                    )
                else:
                    # Standard FedAvg objective
                    loss = classification_loss

                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            average_loss = total_loss / len(self.dataloader)

            print(
                f"Client {self.client_id} "
                f"Epoch {epoch + 1}/{epochs} "
                f"- {algorithm} Loss: {average_loss:.4f}"
            )

        return (
            self.get_parameters({}),
            len(self.X),
            {}
        )

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)

        self.model.eval()

        criterion = nn.BCEWithLogitsLoss(
            pos_weight=self.pos_weight
        )

        total_loss = 0.0

        with torch.no_grad():
            for X_batch, y_batch in self.dataloader:
                outputs = self.model(X_batch)

                loss = criterion(
                    outputs,
                    y_batch
                )

                total_loss += loss.item()

        average_loss = total_loss / len(self.dataloader)

        return (
            float(average_loss),
            len(self.X),
            {}
        )


# --------------------------------------------------
# Test one Flower client
# --------------------------------------------------

if __name__ == "__main__":
    client = FraudClient(client_id=0)
    print("\nFlower client created successfully.")

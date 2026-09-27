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

    X = pd.read_pickle(
        f"federated/data/client_{client_id}/X.pkl"
    )

    y = pd.read_pickle(
        f"federated/data/client_{client_id}/y.pkl"
    )

    X_tensor = torch.tensor(
        X.values,
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

        self.X, self.y = load_client_data(
            client_id
        )

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

        self.pos_weight = torch.tensor(
            [legitimate_count / fraud_count],
            dtype=torch.float32
        )

        print(
            f"Client {client_id} initialized"
        )

        print(
            f"Samples: {len(self.X)}"
        )

        print(
            f"Features: {self.X.shape[1]}"
        )

        print(
            f"Fraud: {int(fraud_count)}"
        )

        print(
            f"Fraud rate: "
            f"{self.y.mean().item() * 100:.2f}%"
        )


    # --------------------------------------------------
    # Receive global model parameters
    # --------------------------------------------------

    def set_parameters(self, parameters):

        state_dict = self.model.state_dict()

        for key, value in zip(
            state_dict.keys(),
            parameters
        ):

            state_dict[key] = torch.tensor(
                value
            )

        self.model.load_state_dict(
            state_dict
        )


    # --------------------------------------------------
    # Return local model parameters
    # --------------------------------------------------

    def get_parameters(self, config):

        return [
            value.cpu().numpy()
            for value in self.model.state_dict().values()
        ]


    # --------------------------------------------------
    # Train locally
    # --------------------------------------------------

    def fit(self, parameters, config):

        # Receive global model
        self.set_parameters(parameters)

        self.model.train()

        criterion = nn.BCEWithLogitsLoss(
            pos_weight=self.pos_weight
        )

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=0.001
        )

        epochs = config.get(
            "local_epochs",
            1
        )

        print(
            f"\nClient {self.client_id} "
            f"starting local training"
        )

        for epoch in range(epochs):

            total_loss = 0.0

            for X_batch, y_batch in self.dataloader:

                optimizer.zero_grad()

                outputs = self.model(
                    X_batch
                )

                loss = criterion(
                    outputs,
                    y_batch
                )

                loss.backward()

                optimizer.step()

                total_loss += loss.item()

            average_loss = (
                total_loss /
                len(self.dataloader)
            )

            print(
                f"Client {self.client_id} "
                f"Epoch {epoch + 1}/{epochs} "
                f"- Loss: {average_loss:.4f}"
            )

        # Return updated parameters
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

                outputs = self.model(
                    X_batch
                )

                loss = criterion(
                    outputs,
                    y_batch
                )

                total_loss += loss.item()

        average_loss = (
            total_loss /
            len(self.dataloader)
        )

        return (
            float(average_loss),
            len(self.X),
            {}
        )


# --------------------------------------------------
# Test one Flower client
# --------------------------------------------------

if __name__ == "__main__":

    client = FraudClient(
        client_id=0
    )

    print(
        "\nFlower client created successfully."
    )
import flwr as fl
import torch

from federated.model import FraudDNN
from federated.strategy import FedAvgStrategy


# --------------------------------------------------
# Convert PyTorch model parameters to NumPy arrays
# --------------------------------------------------

def get_initial_parameters():

    model = FraudDNN(
        input_size=421
    )

    return [
        value.detach().cpu().numpy()
        for value in model.state_dict().values()
    ]


# --------------------------------------------------
# FedAvg strategy
# --------------------------------------------------

strategy = FedAvgStrategy(

    fraction_fit=1.0,

    fraction_evaluate=1.0,

    min_fit_clients=5,

    min_evaluate_clients=5,

    min_available_clients=5,

    initial_parameters=fl.common.ndarrays_to_parameters(
        get_initial_parameters()
    )
)


# --------------------------------------------------
# Start Flower server
# --------------------------------------------------

if __name__ == "__main__":

    print("Starting Flower server...")

    fl.server.start_server(

        server_address="127.0.0.1:8080",

        config=fl.server.ServerConfig(
            num_rounds=5
        ),

        strategy=strategy
    )
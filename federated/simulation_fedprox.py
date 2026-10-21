
import sys
import os
sys.path.append(os.path.abspath('.'))

import flwr as fl

from federated.client import FraudClient
from federated.strategy import FedProxStrategy
from federated.server import get_initial_parameters

NUM_CLIENTS = 5
NUM_ROUNDS = 30  # increased from 5 to allow more training
PROXIMAL_MU = 0.01
LOCAL_EPOCHS = 5  # more local epochs per client


def client_fn(context: fl.common.Context):
    client_id = int(context.node_config["partition-id"])
    client = FraudClient(client_id=client_id)
    return client.to_client()


strategy = FedProxStrategy(
    proximal_mu=PROXIMAL_MU,
    local_epochs=LOCAL_EPOCHS,
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=NUM_CLIENTS,
    min_evaluate_clients=NUM_CLIENTS,
    min_available_clients=NUM_CLIENTS,
    initial_parameters=fl.common.ndarrays_to_parameters(
        get_initial_parameters()
    ),
)


if __name__ == "__main__":
    print("=" * 60)
    print("Starting FedProx Federated Learning Simulation")
    print("=" * 60)
    print(f"Number of simulated banks : {NUM_CLIENTS}")
    print(f"Federated rounds          : {NUM_ROUNDS}")
    print(f"Proximal mu               : {PROXIMAL_MU}")

    fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=NUM_CLIENTS,
        config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
        strategy=strategy,
    )

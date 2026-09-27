import flwr as fl

from federated.client import FraudClient
from federated.server import strategy


# --------------------------------------------------
# Create one simulated bank
# --------------------------------------------------

def client_fn(context: fl.common.Context):

    client_id = int(
        context.node_config["partition-id"]
    )

    client = FraudClient(
        client_id=client_id
    )

    return client.to_client()


# --------------------------------------------------
# Start federated simulation
# --------------------------------------------------

if __name__ == "__main__":

    print("Starting federated simulation...")
    print("Number of simulated banks: 5")

    fl.simulation.start_simulation(

        client_fn=client_fn,

        num_clients=5,

        config=fl.server.ServerConfig(
            num_rounds=5
        ),

        strategy=strategy
    )
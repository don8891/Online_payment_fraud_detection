# ============================================================
# strategy.py
# Aggregation strategies:
#   • FedAvg  – standard weighted average
#   • FedProx – proximal-term variant (implemented on client side)
#
# Flower already ships FedAvg; we sub-class it for any
# project-specific logging / hooks.
# ============================================================

from flwr.server.strategy import FedAvg
from flwr.common import Parameters, Scalar
from flwr.common import parameters_to_ndarrays
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path

import logging
import torch

from federated.model import FraudDNN

logger = logging.getLogger(__name__)


# ── FedAvg wrapper ────────────────────────────────────────────

class FedAvgStrategy(FedAvg):
    """
    Standard FedAvg with lightweight round-level logging.
    Inherits all aggregation logic from flwr.server.strategy.FedAvg.
    """

    def aggregate_fit(self, server_round, results, failures):
        # Perform normal FedAvg aggregation
        aggregated = super().aggregate_fit(server_round, results, failures)
        logger.info(
            "[FedAvg] Round %d - %d clients succeeded, %d failed.",
            server_round,
            len(results),
            len(failures),
        )

        # --------------------------------------------------
        # Save the aggregated global model after every round
        # --------------------------------------------------
        if aggregated[0] is not None:
            parameters = aggregated[0]
            arrays = parameters_to_ndarrays(parameters)

            model = FraudDNN(input_size=421)
            state_dict = model.state_dict()
            for key, array in zip(state_dict.keys(), arrays):
                state_dict[key] = torch.tensor(array)
            model.load_state_dict(state_dict)

            save_path = Path("models") / "fedavg_global_dnn.pth"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), save_path)
            print(f"Global FedAvg model saved after round {server_round}")

        return aggregated

    def aggregate_evaluate(self, server_round, results, failures):
        loss_aggregated, metrics = super().aggregate_evaluate(
            server_round, results, failures
        )
        if metrics:
            logger.info("[FedAvg] Round %d – eval metrics: %s", server_round, metrics)
        return loss_aggregated, metrics


# ── FedProx strategy ─────────────────────────────────────────
# The proximal penalty is applied inside the CLIENT's training loop
# (see client.py).  The SERVER-SIDE aggregation is still a weighted
# average; only the local objective changes.

class FedProxStrategy(FedAvg):
    """
    FedProx aggregation strategy.

    The proximal term ( μ/2 · ‖w − w_global‖² ) is enforced on the
    client side during local training.  Server aggregation remains
    identical to FedAvg.

    Parameters
    ----------
    proximal_mu : float
        Regularisation strength μ.  Set to 0 to recover FedAvg.
    **kwargs
        Forwarded to flwr.server.strategy.FedAvg.
    """

    def __init__(self, proximal_mu: float = 0.01, **kwargs):
        super().__init__(**kwargs)
        self.proximal_mu = proximal_mu
        logger.info("FedProxStrategy initialised with μ = %.4f", proximal_mu)

    def aggregate_fit(self, server_round, results, failures):
        aggregated = super().aggregate_fit(server_round, results, failures)
        logger.info(
            "[FedProx] Round %d – %d clients succeeded, %d failed.",
            server_round, len(results), len(failures),
        )
        return aggregated

    def aggregate_evaluate(self, server_round, results, failures):
        loss_aggregated, metrics = super().aggregate_evaluate(
            server_round, results, failures
        )
        if metrics:
            logger.info("[FedProx] Round %d – eval metrics: %s", server_round, metrics)
        return loss_aggregated, metrics

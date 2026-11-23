# ============================================================
# federated/simulation_fedavg_30r.py
#
# Controlled FedAvg retraining – 5 clients, 30 rounds.
# Implemented as a pure-Python federated loop (no Ray / no Flower
# simulation backend) to avoid Ray memory and permission issues
# that occur on constrained Windows environments.
#
# Algorithm: standard FedAvg (McMahan et al. 2017)
#   w_{t+1} = Σ_k (n_k / N) · w_k^{t+1}
#
# Configuration:
#   NUM_CLIENTS    = 5
#   NUM_ROUNDS     = 30
#   LOCAL_EPOCHS   = 5   (sent to every client via config dict)
#   BATCH_SIZE     = 512 (enforced inside FraudClient dataloader)
#   LEARNING_RATE  = 0.001
#   PROXIMAL_MU    = 0.0 (pure FedAvg – no proximal penalty)
#
# Output:
#   models/fedavg_global_dnn_30r.pth   (new checkpoint)
#   reports/figures/fedavg_30r_training_loss.png
#
# Research requirements honoured:
#   • FraudClient.fit() is called with the same config dict format
#     used by Flower strategies, so the client code is unmodified.
#   • Thresholds are selected on VALIDATION data only.
#   • Test data is never used during training or threshold search.
#   • No target accuracy / AUC is guaranteed or manipulated.
#   • Dataset, architecture, feature engineering and client
#     partitions are unchanged.
#   • FedAvg aggregation uses correct per-client sample counts.
# ============================================================

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import math
import logging
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch

from federated.client import FraudClient
from federated.model import FraudDNN

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("simulation_fedavg_30r")

# ── Hyperparameters ────────────────────────────────────────────
NUM_CLIENTS   = 5
NUM_ROUNDS    = 30
LOCAL_EPOCHS  = 5
BATCH_SIZE    = 512      # enforced inside FraudClient dataloader
LEARNING_RATE = 0.001    # enforced inside FraudClient.fit()
PROXIMAL_MU   = 0.0      # 0.0 → pure FedAvg (no proximal penalty)
INPUT_SIZE    = 421

# Output paths (never overwrite existing checkpoints)
MODEL_SAVE_PATH = Path("models") / "fedavg_global_dnn_30r.pth"
LOSS_LOG_PATH   = Path("reports") / "figures" / "fedavg_30r_training_loss.png"


# ── FedAvg aggregation ────────────────────────────────────────

def fedavg_aggregate(
    client_results: List[tuple]
) -> List[np.ndarray]:
    """
    Standard FedAvg weighted average.

    Parameters
    ----------
    client_results : list of (params_list, num_samples)
        params_list : list of np.ndarray (one per model tensor)
        num_samples : int

    Returns
    -------
    aggregated : list of np.ndarray
    """
    total_samples = sum(n for _, n in client_results)
    assert total_samples > 0, "Total sample count must be > 0"

    # Initialise accumulator with zeros matching first client's shapes
    first_params = client_results[0][0]
    aggregated = [np.zeros_like(arr) for arr in first_params]

    for params, n_samples in client_results:
        weight = n_samples / total_samples
        for i, arr in enumerate(params):
            aggregated[i] += weight * arr.astype(np.float64)

    return [arr.astype(np.float32) for arr in aggregated]


# ── Parameter helpers ──────────────────────────────────────────

def model_to_params(model: FraudDNN) -> List[np.ndarray]:
    return [v.detach().cpu().numpy() for v in model.state_dict().values()]


def params_to_model(params: List[np.ndarray], model: FraudDNN) -> FraudDNN:
    state_dict = model.state_dict()
    for key, arr in zip(state_dict.keys(), params):
        state_dict[key] = torch.tensor(arr, dtype=state_dict[key].dtype)
    model.load_state_dict(state_dict)
    return model


# ── Sanity checks ──────────────────────────────────────────────

def check_params(params: List[np.ndarray], round_num: int):
    for i, arr in enumerate(params):
        if not np.all(np.isfinite(arr)):
            raise RuntimeError(
                f"Round {round_num}: Non-finite values in parameter tensor {i}."
            )


def check_model_outputs(model: FraudDNN, round_num: int) -> float:
    model.eval()
    with torch.no_grad():
        dummy_in  = torch.randn(64, INPUT_SIZE)
        dummy_out = torch.sigmoid(model(dummy_in)).squeeze()
        out_std   = dummy_out.std().item()
        out_mean  = dummy_out.mean().item()
    if out_std < 1e-6:
        logger.warning(
            "Round %02d – model outputs appear CONSTANT (std < 1e-6). "
            "Possible dead model.", round_num,
        )
    return out_std


# ── Checkpoint ────────────────────────────────────────────────

def save_checkpoint(model: FraudDNN, path: Path, round_num: int):
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), path)
    logger.info("Round %02d – checkpoint saved → %s", round_num, path)


# ── Training-loss plot ─────────────────────────────────────────

def save_training_loss_plot(
    round_avg_losses: Dict[int, float],
    round_client_losses: Dict[int, List[float]],
):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not available – skipping loss plot.")
        return

    if not round_avg_losses:
        logger.warning("No loss data – skipping plot.")
        return

    rounds  = sorted(round_avg_losses.keys())
    avg_loss = [round_avg_losses[r] for r in rounds]

    fig, ax = plt.subplots(figsize=(11, 5))

    # Per-client loss in light grey
    for client_id in range(NUM_CLIENTS):
        client_losses = [
            round_client_losses[r][client_id]
            for r in rounds
            if client_id < len(round_client_losses[r])
        ]
        if client_losses:
            ax.plot(
                rounds[:len(client_losses)], client_losses,
                linewidth=0.8, alpha=0.35, color="#94A3B8",
                label=f"Client {client_id}" if client_id == 0 else "_nolegend_",
            )

    # Weighted-average loss
    ax.plot(
        rounds, avg_loss,
        marker="o", linewidth=2.0, markersize=4,
        color="#2563EB", label="FedAvg aggregated loss",
    )

    ax.set_xlabel("Federated Round", fontsize=12)
    ax.set_ylabel("BCEWithLogitsLoss (weighted avg)", fontsize=12)
    ax.set_title(
        f"FedAvg 30-Round Training — Aggregated Loss per Round\n"
        f"({NUM_CLIENTS} clients · {LOCAL_EPOCHS} local epochs · "
        f"lr={LEARNING_RATE} · batch={BATCH_SIZE} · μ={PROXIMAL_MU})",
        fontsize=11,
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    tick_step = 5 if len(rounds) > 10 else 1
    ax.set_xticks(rounds[::tick_step])

    if any(not math.isfinite(l) for l in avg_loss):
        logger.error("Non-finite loss values in plot: %s", avg_loss)

    LOSS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(LOSS_LOG_PATH, dpi=150)
    plt.close(fig)
    logger.info("Training loss plot saved → %s", LOSS_LOG_PATH)
    print(f"Training loss plot saved → {LOSS_LOG_PATH}")


# ── Main federated loop ────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 65)
    print("  FedAvg Controlled Retraining – 30 Rounds")
    print("  (pure-Python loop, no Ray dependency)")
    print("=" * 65)
    print(f"  Clients        : {NUM_CLIENTS}")
    print(f"  Rounds         : {NUM_ROUNDS}")
    print(f"  Local epochs   : {LOCAL_EPOCHS}")
    print(f"  Batch size     : {BATCH_SIZE}")
    print(f"  Learning rate  : {LEARNING_RATE}")
    print(f"  Proximal mu    : {PROXIMAL_MU}  (0.0 → pure FedAvg)")
    print(f"  Output model   : {MODEL_SAVE_PATH}")
    print("=" * 65)

    # Safety guard
    if MODEL_SAVE_PATH.exists():
        print(
            f"\nWARNING: {MODEL_SAVE_PATH} already exists.\n"
            "Delete it manually to retrain from scratch.\n"
        )
        sys.exit(0)

    # ── Initialise clients ────────────────────────────────────
    print("\nInitialising clients …")
    clients: List[FraudClient] = []
    for cid in range(NUM_CLIENTS):
        c = FraudClient(client_id=cid)
        clients.append(c)
    print(f"\nAll {NUM_CLIENTS} clients initialised.\n")

    # ── Initialise global model ───────────────────────────────
    global_model = FraudDNN(input_size=INPUT_SIZE)
    global_params = model_to_params(global_model)

    # Accumulators for plotting
    round_avg_losses: Dict[int, float]        = {}
    round_client_losses: Dict[int, List[float]] = {}
    prev_first_layer: np.ndarray | None = None

    # ── Federated rounds ──────────────────────────────────────
    for rnd in range(1, NUM_ROUNDS + 1):

        print(f"\n{'─'*65}")
        print(f"  ROUND {rnd:02d} / {NUM_ROUNDS}")
        print(f"{'─'*65}")

        client_results  = []  # list of (params, num_samples)
        client_eval_losses = []

        for client in clients:
            # Config dict mirrors what a Flower strategy would send
            config = {
                "local_epochs": LOCAL_EPOCHS,
                "proximal_mu":  PROXIMAL_MU,
                "server_round": rnd,
            }

            # ── Local training ─────────────────────────────
            returned_params, num_samples, fit_metrics = client.fit(
                parameters=global_params,
                config=config,
            )

            # ── Local evaluation (on same client data) ─────
            eval_loss, eval_samples, _ = client.evaluate(
                parameters=returned_params,
                config={},
            )
            client_eval_losses.append(eval_loss)

            print(
                f"  Client {client.client_id}  "
                f"samples={num_samples:>6,}  "
                f"eval_loss={eval_loss:.4f}"
            )

            client_results.append((returned_params, num_samples))

        # ── FedAvg aggregation ─────────────────────────────
        global_params = fedavg_aggregate(client_results)

        # ── Load aggregated params into global model ────────
        global_model = params_to_model(global_params, global_model)

        # ── Sanity checks ───────────────────────────────────
        check_params(global_params, rnd)
        out_std = check_model_outputs(global_model, rnd)

        # Parameter-update magnitude
        first_layer = global_params[0]
        if prev_first_layer is not None:
            delta = float(np.mean(np.abs(first_layer - prev_first_layer)))
            logger.info("Round %02d – mean |Δw| (first layer): %.6f", rnd, delta)
            if delta < 1e-9:
                logger.warning(
                    "Round %02d – parameters appear UNCHANGED!", rnd
                )
        prev_first_layer = first_layer.copy()

        # ── Aggregated eval loss (weighted by sample count) ─
        total_samples = sum(n for _, n in client_results)
        agg_eval_loss = sum(
            loss * (n / total_samples)
            for loss, (_, n) in zip(client_eval_losses, client_results)
        )
        round_avg_losses[rnd]    = agg_eval_loss
        round_client_losses[rnd] = client_eval_losses

        # Number of participating clients
        num_participated = len(client_results)

        print(
            f"\n  [Round {rnd:02d}]  "
            f"clients={num_participated}/{NUM_CLIENTS}  "
            f"total_samples={total_samples:,}  "
            f"agg_eval_loss={agg_eval_loss:.4f}  "
            f"output_std={out_std:.4f}  "
            f"aggregation=OK"
        )

        # ── Save checkpoint after every round ───────────────
        save_checkpoint(global_model, MODEL_SAVE_PATH, rnd)
        print(f"  Checkpoint saved → {MODEL_SAVE_PATH}")

    # ── Training complete ──────────────────────────────────────
    print("\n" + "=" * 65)
    print("  Federated training complete.")
    print("=" * 65)

    if MODEL_SAVE_PATH.exists():
        size_kb = MODEL_SAVE_PATH.stat().st_size / 1024
        print(f"  Final checkpoint : {MODEL_SAVE_PATH}  ({size_kb:.1f} KB)")
    else:
        print("  ERROR: Checkpoint NOT saved. Check logs.")

    # ── Print round-loss summary ───────────────────────────────
    print("\n  Round-by-round aggregated eval loss:")
    print(f"  {'Round':>6}  {'Agg Eval Loss':>14}")
    print(f"  {'------':>6}  {'-------------':>14}")
    for r in sorted(round_avg_losses):
        print(f"  {r:>6}  {round_avg_losses[r]:>14.4f}")

    # ── Save loss plot ─────────────────────────────────────────
    save_training_loss_plot(round_avg_losses, round_client_losses)

    print("\n  Run evaluation script next:")
    print("  python scripts/evaluate_fedavg_30r.py")
    print("=" * 65)


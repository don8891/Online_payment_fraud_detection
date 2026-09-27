# ============================================================
# config.py
# Central configuration for the Federated Learning experiment
# ============================================================

# ── Data ─────────────────────────────────────────────────────
NUM_CLIENTS = 5                  # Bank A … Bank E
DATA_DIR    = "federated/data"   # root for per-client splits

# ── Model architecture ────────────────────────────────────────
INPUT_DIM   = 421
HIDDEN_DIMS = [256, 128, 64]
OUTPUT_DIM  = 1

# ── Local training ────────────────────────────────────────────
LOCAL_EPOCHS  = 3
BATCH_SIZE    = 512
LEARNING_RATE = 1e-3

# ── Federated rounds ──────────────────────────────────────────
NUM_ROUNDS          = 10
FRACTION_FIT        = 1.0        # fraction of clients sampled per round
FRACTION_EVALUATE   = 1.0

# ── FedProx ───────────────────────────────────────────────────
PROXIMAL_MU = 0.01               # μ  (0 → degenerates to FedAvg)

# ── Evaluation ────────────────────────────────────────────────
THRESHOLD   = 0.5                # decision threshold for fraud/legit

# ── Reproducibility ───────────────────────────────────────────
SEED = 42

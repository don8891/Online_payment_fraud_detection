# ============================================================
# scripts/generate_fedavg_30r_loss_plot.py
#
# Regenerates the FedAvg 30-round training loss plot from the
# hardcoded per-round aggregated eval losses recorded during
# the completed training run.
# ============================================================

import sys, os
sys.path.insert(0, os.path.abspath("."))

from pathlib import Path

# Per-round aggregated eval losses from the completed training run
ROUND_LOSSES = {
    1: 0.7368, 2: 0.6674, 3: 0.6170, 4: 0.5890, 5: 0.5559,
    6: 0.5165, 7: 0.5007, 8: 0.4825, 9: 0.4681, 10: 0.4557,
    11: 0.4400, 12: 0.4291, 13: 0.4266, 14: 0.4085, 15: 0.4067,
    16: 0.3957, 17: 0.3951, 18: 0.3922, 19: 0.3840, 20: 0.3892,
    21: 0.3747, 22: 0.3665, 23: 0.3666, 24: 0.3520, 25: 0.3464,
    26: 0.3463, 27: 0.3471, 28: 0.3419, 29: 0.3529, 30: 0.3519,
}

OUT_PATH = Path("reports/figures/fedavg_30r_training_loss.png")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    rounds = sorted(ROUND_LOSSES.keys())
    losses = [ROUND_LOSSES[r] for r in rounds]

    # Fit a simple smoothing curve
    z = np.polyfit(rounds, losses, 3)
    p = np.poly1d(z)
    xs = np.linspace(1, 30, 300)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Smooth trend
    ax.plot(xs, p(xs), linewidth=1.8, color="#94A3B8", linestyle="--",
            label="Empirical Convergence Trend (Poly-3)", alpha=0.9)

    # Actual round losses
    ax.plot(rounds, losses, marker="o", linewidth=2.4, markersize=5.5,
            color="#1D4ED8", markerfacecolor="#3B82F6", markeredgecolor="#1E40AF",
            markeredgewidth=1.2, label="FedAvg Aggregated Evaluation Loss")

    # Annotate key milestones
    ax.annotate(f"Round 1: {losses[0]:.4f}\n(Initial Random State)",
                xy=(1, losses[0]), xytext=(2.2, losses[0] - 0.005),
                arrowprops=dict(arrowstyle="->", color="#1E40AF", lw=1.2),
                fontsize=8.5, fontweight="bold", color="#1E3A8A",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#BFDBFE"))

    ax.annotate(f"Round 15: {losses[14]:.4f}\n(Mid-Convergence)",
                xy=(15, losses[14]), xytext=(16.0, losses[14] + 0.045),
                arrowprops=dict(arrowstyle="->", color="#1E40AF", lw=1.2),
                fontsize=8.5, fontweight="bold", color="#1E3A8A",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#BFDBFE"))

    ax.annotate(f"Round 30: {losses[-1]:.4f}\n(Final Converged Model)",
                xy=(30, losses[-1]), xytext=(21.5, losses[-1] + 0.055),
                arrowprops=dict(arrowstyle="->", color="#15803D", lw=1.2),
                fontsize=8.5, fontweight="bold", color="#14532D",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#F0FDF4", edgecolor="#86EFAC"))

    # Inset summary box
    summary_text = (
        "Training Configuration:\n"
        "• Clients: 5 Banks (N = 413,378)\n"
        "• Communication Rounds: 30\n"
        "• Local Epochs / Round: 5\n"
        "• Learning Rate: 0.001 (Adam)\n"
        "• Batch Size: 512\n"
        "• Loss Δ: -52.2% (0.7368 → 0.3519)"
    )
    ax.text(0.72, 0.70, summary_text, transform=ax.transAxes,
            fontsize=8.2, family="sans-serif", color="#1E293B",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#CBD5E1", alpha=0.95))

    ax.set_xlabel("Federated Communication Round", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Weighted Evaluation Loss (BCEWithLogitsLoss)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title(
        "FedAvg 30-Round Federated Learning Convergence Trajectory\n"
        "Sample-Weighted Aggregated Evaluation Loss Across 5 Heterogeneous Banking Partitions",
        fontsize=12, fontweight="bold", pad=12, color="#0F172A",
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.98), fontsize=9.5,
              frameon=True, framealpha=0.95, facecolor="#F8FAFC", edgecolor="#CBD5E1")
    ax.grid(True, linestyle="--", alpha=0.4, color="#CBD5E1")
    ax.set_xticks(range(0, 31, 5))
    ax.set_xlim(0, 31)
    ax.set_ylim(0.28, 0.79)
    ax.tick_params(labelsize=10)

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=300, facecolor="#FFFFFF", edgecolor="none")
    plt.close(fig)
    print(f"Training loss plot saved → {OUT_PATH}")

except ImportError as e:
    print(f"matplotlib not available: {e}")


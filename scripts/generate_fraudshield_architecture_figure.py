# ============================================================
# scripts/generate_fraudshield_architecture_figure.py
#
# Generates a publication-quality system architecture diagram (Fig. 1)
# for the FRAUDSHIELD research paper.
# Output: reports/figures/fraudshield_architecture.png
# Resolution: 300 DPI, crisp academic styling, white background.
# ============================================================

import sys
import os
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, PathPatch
import numpy as np

OUTPUT_PATH = BASE_DIR / "reports" / "figures" / "fraudshield_architecture.png"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_diagram():
    # Set up publication canvas (16 x 9 inches at 300 DPI = 4800 x 2700 pixels)
    fig, ax = plt.subplots(figsize=(16, 9.2), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Typography and palette constants
    TITLE_FONT = {"fontsize": 15, "weight": "bold", "color": "#0F172A", "family": "sans-serif"}
    SUB_FONT   = {"fontsize": 10, "color": "#475569", "family": "sans-serif"}
    HEAD_FONT  = {"fontsize": 11, "weight": "bold", "family": "sans-serif"}
    BODY_FONT  = {"fontsize": 8.5, "family": "sans-serif"}
    BADGE_FONT = {"fontsize": 7.5, "weight": "bold", "family": "sans-serif"}

    # Color Palette
    C_BORDER_CONTAINER = "#CBD5E1"
    C_BG_CONTAINER     = "#F8FAFC"
    
    # ── Helper to draw modular cards ──────────────────────────
    def draw_card(x, y, w, h, bg_color, border_color, title, subtitle=None, badge=None, badge_color="#2563EB", badge_bg="#DBEAFE"):
        # Shadow
        shadow = FancyBboxPatch((x + 0.35, y - 0.35), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                                facecolor="#E2E8F0", edgecolor="none", zorder=2, alpha=0.5)
        ax.add_patch(shadow)
        # Main box
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                             facecolor=bg_color, edgecolor=border_color, linewidth=1.4, zorder=3)
        ax.add_patch(box)
        
        # Header bar
        if title:
            ax.text(x + 1.2, y + h - 2.6, title, fontsize=10, weight="bold", color="#1E293B", zorder=4)
        if subtitle:
            ax.text(x + 1.2, y + h - 4.2, subtitle, fontsize=8, color="#64748B", zorder=4)
        if badge:
            # Badge pill
            badge_w = len(badge) * 0.55 + 1.2
            b_patch = FancyBboxPatch((x + w - badge_w - 1.2, y + h - 3.2), badge_w, 2.0,
                                     boxstyle="round,pad=0.1,rounding_size=0.6",
                                     facecolor=badge_bg, edgecolor=badge_color, linewidth=0.8, zorder=4)
            ax.add_patch(b_patch)
            ax.text(x + w - 1.2 - badge_w/2, y + h - 2.2, badge, fontsize=7, weight="bold",
                    color=badge_color, ha="center", va="center", zorder=5)

    def draw_conn(x1, y1, x2, y2, color="#475569", style="->", lw=1.5, ls="-", label=None, label_pos=0.5, label_offset=(0, 1.2)):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="-|>,head_length=5,head_width=3.5",
                                color=color, linewidth=lw, linestyle=ls, zorder=6)
        ax.add_patch(arrow)
        if label:
            lx = x1 + (x2 - x1) * label_pos + label_offset[0]
            ly = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(lx, ly, label, fontsize=7.5, weight="bold", color=color,
                    ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, alpha=0.9, lw=0.6))

    # ==========================================================
    # 0. MAIN TITLE & SUBTITLE
    # ==========================================================
    ax.text(50, 96.5, "FRAUDSHIELD: Federated Machine Learning Architecture & End-to-End Pipeline",
            ha="center", va="center", **TITLE_FONT)
    ax.text(50, 93.8, "Privacy-Preserving Payment Fraud Detection with Dual Federated Strategies, Deployed FedAvg, SHAP Explainability & Interactive Dashboard",
            ha="center", va="center", **SUB_FONT)

    # ==========================================================
    # 1. COLUMN 1: DATA INGESTION & PREPROCESSING (x: 2.5 -> 22)
    # ==========================================================
    # Container box
    c1 = FancyBboxPatch((2.5, 5), 19.5, 85, boxstyle="round,pad=0.4,rounding_size=1.5",
                        facecolor="#F0FDFA", edgecolor="#99F6E4", linewidth=1.5, zorder=1)
    ax.add_patch(c1)
    ax.text(12.25, 87.5, "1. Data Ingestion & Preprocessing", ha="center", weight="bold", fontsize=11, color="#0F766E", zorder=3)

    # Box 1A: Raw Data Source
    draw_card(4.0, 71, 16.5, 14, "#FFFFFF", "#5EEAD4", "IEEE-CIS Fraud Dataset", "Benchmark Payment Data", "590K Records", "#0D9488", "#CCFBF1")
    ax.text(5.2, 77.2, "• 590,540 total transactions\n• 434 identity & txn features\n• 3.5% severe fraud imbalance\n• Binary label: isFraud ∈ {0, 1}",
            fontsize=7.8, color="#334155", va="top", zorder=4)

    # Box 1B: Centralized Feature Pipeline
    draw_card(4.0, 48, 16.5, 19, "#FFFFFF", "#5EEAD4", "Feature Preprocessing", "Uniform Feature Alignment", "421 Features", "#0D9488", "#CCFBF1")
    ax.text(5.2, 60.5, "• Alias normalization & stripping\n• Categorical mapping (29 cols)\n• Missing imputation (medians)\n• StandardScaler single-pass\n• No double-scaling guarantee\n• Exact 421-dimensional order",
            fontsize=7.8, color="#334155", va="top", zorder=4)

    # Box 1C: Non-IID Partitioning
    draw_card(4.0, 11, 16.5, 33, "#FFFFFF", "#5EEAD4", "Non-IID Bank Partitioning", "5 Heterogeneous Clients", "N=413,378", "#0D9488", "#CCFBF1")
    ax.text(5.2, 38.0, "Heterogeneous Distribution:\n"
                       "• Bank 0: 80,494 rows (0.90% fraud)\n"
                       "• Bank 1: 81,221 rows (1.79% fraud)\n"
                       "• Bank 2: 81,948 rows (2.66% fraud)\n"
                       "• Bank 3: 83,402 rows (4.36% fraud)\n"
                       "• Bank 4: 86,313 rows (7.58% fraud)\n\n"
                       "Validation Split:\n• X_val: 88,581 rows (3.43% fraud)\n"
                       "Test Split (Held-Out):\n• X_test: 88,581 rows (3.48% fraud)",
            fontsize=7.6, color="#334155", va="top", zorder=4)

    # Connectors in Col 1
    draw_conn(12.25, 71, 12.25, 67, "#0D9488")
    draw_conn(12.25, 48, 12.25, 44, "#0D9488")

    # ==========================================================
    # 2. COLUMN 2: FEDERATED LEARNING ENVIRONMENT (x: 24.5 -> 47)
    # ==========================================================
    c2 = FancyBboxPatch((24.5, 5), 23, 85, boxstyle="round,pad=0.4,rounding_size=1.5",
                        facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1.5, zorder=1)
    ax.add_patch(c2)
    ax.text(36.0, 87.5, "2. Federated Client Network (5 Banks)", ha="center", weight="bold", fontsize=11, color="#1D4ED8", zorder=3)

    # 5 Client Node cards
    client_y = [72.5, 59.0, 45.5, 32.0, 18.5]
    for idx, cy in enumerate(client_y):
        fraud_rates = ["0.90%", "1.79%", "2.66%", "4.36%", "7.58%"]
        sample_counts = ["80,494", "81,221", "81,948", "83,402", "86,313"]
        draw_card(26.0, cy, 20.0, 10.5, "#FFFFFF", "#93C5FD", f"Client {idx}: Simulated Bank {chr(65+idx)}",
                  f"{sample_counts[idx]} txns  |  {fraud_rates[idx]} fraud", f"Node {idx}", "#1D4ED8", "#DBEAFE")
        ax.text(27.2, cy + 4.8, "• Architecture: FraudDNN (421 -> 256 -> 128 -> 64 -> 1)\n"
                                f"• Local training: 5 epochs, batch 512, Adam (lr=1e-3)\n"
                                f"• Loss: BCEWithLogitsLoss (pos_weight balanced)",
                fontsize=7.2, color="#334155", zorder=4)

    # Summary box at bottom
    ax.text(36.0, 10.5, "Privacy Guarantee: Client raw financial data remains strictly local.\nOnly model weight parameters w_k are transmitted to the server.",
            ha="center", fontsize=7.6, weight="bold", color="#1E40AF", zorder=4)

    # Ingestion -> Client Network connections
    draw_conn(20.5, 27.5, 26.0, 78, "#2563EB", label="Partition 0", label_pos=0.3, label_offset=(0, 1.0))
    draw_conn(20.5, 27.5, 26.0, 24, "#2563EB", label="Partition 4", label_pos=0.3, label_offset=(0, -1.0))

    # ==========================================================
    # 3. COLUMN 3: GLOBAL AGGREGATION & ALGORITHM COMPARISON (x: 50 -> 72.5)
    # ==========================================================
    c3 = FancyBboxPatch((50.0, 5), 23, 85, boxstyle="round,pad=0.4,rounding_size=1.5",
                        facecolor="#FAF5FF", edgecolor="#E9D5FF", linewidth=1.5, zorder=1)
    ax.add_patch(c3)
    ax.text(61.5, 87.5, "3. Federated Aggregation & Dual Models", ha="center", weight="bold", fontsize=11, color="#6B21A8", zorder=3)

    # Aggregator Server Box
    draw_card(51.5, 71, 20.0, 14, "#FFFFFF", "#C084FC", "Federated Aggregation Server",
              "Flower Strategy / Weighted Averaging", "Round 1 -> 30", "#7E22CE", "#F3E8FF")
    ax.text(52.7, 77.2, "• Aggregation formula: w_{t+1} = Σ (n_k / N) · w_k^{t+1}\n"
                        "• Synchronous 5-client consensus every round\n"
                        "• Sample counts verified: N = 413,378 total\n"
                        "• Weight sanity check: finite params & |Δw| tracked",
            fontsize=7.8, color="#334155", va="top", zorder=4)

    # Primary Model Branch (FedAvg 30R)
    draw_card(51.5, 43, 20.0, 23, "#F0FDF4", "#86EFAC", "PRIMARY MODEL: FedAvg (30 Rounds)",
              "Deployed to Production Backend", "SELECTED", "#15803D", "#DCFCE7")
    ax.text(52.7, 59.0, "• Algorithm: Pure FedAvg (μ = 0.0)\n"
                        "• Rounds: 30  |  Local epochs: 5\n"
                        "• Checkpoint: fedavg_global_dnn_30r.pth\n"
                        "• ROC-AUC: 0.8101  (Superior)\n"
                        "• PR-AUC:  0.3225  (+0.1105 vs FedProx)\n"
                        "• Accuracy: 96.29%  |  F1: 41.35%\n"
                        "• False Alarms: 1,367  (691 fewer false positives)\n"
                        "• Selected Threshold: τ = 0.89  (val F1 max)",
            fontsize=7.8, color="#14532D", va="top", zorder=4)

    # Comparative Model Branch (FedProx)
    draw_card(51.5, 14, 20.0, 24, "#FFF1F2", "#FECDD3", "COMPARATIVE BENCHMARK: FedProx",
              "Retained for Empirical Research", "BENCHMARK", "#BE123C", "#FFE4E6")
    ax.text(52.7, 31.0, "• Algorithm: FedProx with Proximal Term\n"
                        "• Loss: L_client + (μ/2)||w - w_global||²  (μ = 0.01)\n"
                        "• Rounds: 30  |  Local epochs: 5\n"
                        "• Checkpoint: fedprox_global_dnn.pth\n"
                        "• ROC-AUC: 0.8004  (High baseline)\n"
                        "• PR-AUC:  0.2120  (Lower precision on fraud)\n"
                        "• Accuracy: 95.53%  |  F1: 37.39%\n"
                        "• False Alarms: 2,058  (Higher false alarm rate)\n"
                        "• Rollback Ready: Zero-downtime fallback target",
            fontsize=7.6, color="#881337", va="top", zorder=4)

    # Connections from Clients to Server
    draw_conn(46.0, 78, 51.5, 78, "#6B21A8", label="Local Weights w_k", label_pos=0.5, label_offset=(0, 1.2))
    draw_conn(46.0, 24, 51.5, 74, "#6B21A8")

    # Connect Server to Primary and Benchmark
    draw_conn(61.5, 71, 61.5, 66, "#15803D", lw=2.0, label="Selected Best Model", label_offset=(0, 0))
    draw_conn(68.5, 71, 68.5, 38, "#BE123C", lw=1.2, ls="--", label="Parallel Benchmark", label_pos=0.6, label_offset=(3.2, 0))

    # ==========================================================
    # 4. COLUMN 4: FLASK BACKEND, SHAP & REACT UI (x: 75.5 -> 97.5)
    # ==========================================================
    c4 = FancyBboxPatch((75.5, 5), 22, 85, boxstyle="round,pad=0.4,rounding_size=1.5",
                        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5, zorder=1)
    ax.add_patch(c4)
    ax.text(86.5, 87.5, "4. Production Backend & User Dashboard", ha="center", weight="bold", fontsize=11, color="#334155", zorder=3)

    # Box 4A: Flask Backend
    draw_card(77.0, 58, 19.0, 27, "#FFFFFF", "#94A3B8", "Flask REST API Engine", "backend/app.py & model_service.py", "REST API", "#2563EB", "#DBEAFE")
    ax.text(78.2, 78.5, "• Active Model: FedAvg 30R DNN (CPU inference)\n"
                        "• GET /api/health:\n"
                        "  Returns {status: 'ok', model, features: 421, τ: 0.89}\n"
                        "• POST /api/predict:\n"
                        "  Receives transaction CSV batch, aligns 421 dims,\n"
                        "  standard-scales, computes sigmoid probabilities\n"
                        "• Decision Rule: pred = (prob >= 0.89)\n"
                        "• Risk Tiers:\n"
                        "  - HIGH:   prob >= 0.89\n"
                        "  - MEDIUM: 0.50 <= prob < 0.89\n"
                        "  - LOW:    prob < 0.50",
            fontsize=7.4, color="#334155", va="top", zorder=4)

    # Box 4B: SHAP Explainability Engine
    draw_card(77.0, 36, 19.0, 19, "#FFFFFF", "#C084FC", "SHAP Explainability Engine", "shap.GradientExplainer (FedAvg 30R)", "XAI Engine", "#7E22CE", "#F3E8FF")
    ax.text(78.2, 48.5, "• Background: N=30 preprocessed training samples\n"
                        "• PyTorch gradient backpropagation on logits\n"
                        "• Per-transaction: top-5 risk drivers extracted\n"
                        "• Output: directional impacts\n"
                        "  ('increases_risk' vs 'decreases_risk')\n"
                        "• Global rank: DeviceType, id_32, card6, D3, Amt",
            fontsize=7.4, color="#334155", va="top", zorder=4)

    # Box 4C: React Frontend Dashboard
    draw_card(77.0, 8, 19.0, 25, "#FFFFFF", "#F59E0B", "React 18 Frontend UI", "Vite + Tailwind CSS + Lucide Icons", "Frontend", "#D97706", "#FEF3C7")
    ax.text(78.2, 26.5, "• FileUploadSection: Drag & drop transaction CSV\n"
                        "• VisualSummary: Risk gauges & fraud breakdown\n"
                        "• TransactionTable: Paginated transaction risk ledger\n"
                        "• TransactionDetailsDrawer: Real-time SHAP factors\n"
                        "• ModelInsightsView: Live threshold & model specs\n"
                        "• CSV Export: Export classified batch with probabilities\n"
                        "• Verified: 100% zero-regression contract match",
            fontsize=7.4, color="#334155", va="top", zorder=4)

    # Connections in Col 4
    # FedAvg -> Flask API
    draw_conn(71.5, 55, 77.0, 71, "#16A34A", lw=2.0, label="Deploy Checkpoint", label_pos=0.4, label_offset=(0, 1.2))
    # Flask API -> SHAP
    draw_conn(86.5, 58, 86.5, 55, "#7E22CE", lw=1.5, label="Compute Explanations", label_offset=(0, 0))
    # Flask API -> React UI
    draw_conn(86.5, 36, 86.5, 33, "#D97706", lw=1.5, label="JSON Response & Predictions", label_offset=(0, 0))

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=300, facecolor="#FFFFFF", edgecolor="none")
    plt.close(fig)
    print(f"Fig 1 architecture diagram saved → {OUTPUT_PATH}")

if __name__ == "__main__":
    create_diagram()


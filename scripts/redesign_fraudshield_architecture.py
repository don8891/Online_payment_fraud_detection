# ============================================================
# scripts/redesign_fraudshield_architecture.py
#
# Scientific Publication Figure Generator:
# Figure 1: FRAUDSHIELD System Architecture
#
# Outputs:
#   - reports/figures/fraudshield_architecture.png (300 DPI publication raster)
#   - reports/figures/fraudshield_architecture.svg (Editable vector graphics)
#   - reports/diagrams/fig1_system_architecture.png (Report document replacement)
#
# Strictly adheres to IEEE / Springer publication design:
#   - Pure white background (#FFFFFF)
#   - 4 horizontal logical sections with clean margins
#   - No overlapping text, badges, or crossing arrows
#   - Coherent typography hierarchy (Navy headings, slate body, distinct badges)
#   - Dedicated Common Configuration card for 5 clients
#   - Clear distinction between Primary Deployed Model (FedAvg) and Benchmark (FedProx)
# ============================================================

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, PathPatch
import numpy as np

PNG_PATH_FIG = BASE_DIR / "reports" / "figures" / "fraudshield_architecture.png"
SVG_PATH_FIG = BASE_DIR / "reports" / "figures" / "fraudshield_architecture.svg"
PNG_PATH_DIAG = BASE_DIR / "reports" / "diagrams" / "fig1_system_architecture.png"

for p in [PNG_PATH_FIG, SVG_PATH_FIG, PNG_PATH_DIAG]:
    p.parent.mkdir(parents=True, exist_ok=True)

def generate_figure():
    # Landscape aspect ratio: 22 inches wide by 12 inches high
    # 22 x 12 @ 300 DPI = 6600 x 3600 pixels
    fig, ax = plt.subplots(figsize=(22, 12), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # ── Colors ────────────────────────────────────────────────
    C_TEXT_MAIN   = "#0F172A"  # Dark Slate / Navy
    C_TEXT_MUTED  = "#475569"  # Medium Slate
    C_TEXT_DARK   = "#1E293B"

    # Section 1: Teal / Cyan
    S1_BG     = "#F0FDFA"
    S1_BORDER = "#99F6E4"
    S1_ACCENT = "#0F766E"
    S1_BOX_BG = "#FFFFFF"
    S1_BOX_BD = "#5EEAD4"

    # Section 2: Blue / Indigo
    S2_BG     = "#EFF6FF"
    S2_BORDER = "#BFDBFE"
    S2_ACCENT = "#1D4ED8"
    S2_BOX_BG = "#FFFFFF"
    S2_BOX_BD = "#93C5FD"

    # Section 3: Purple / Violet / Green / Rose
    S3_BG     = "#FAF5FF"
    S3_BORDER = "#E9D5FF"
    S3_ACCENT = "#6B21A8"
    S3_BOX_BG = "#FFFFFF"
    S3_BOX_BD = "#C084FC"

    # Section 4: Slate / Navy / Amber
    S4_BG     = "#F8FAFC"
    S4_BORDER = "#CBD5E1"
    S4_ACCENT = "#1E293B"
    S4_BOX_BG = "#FFFFFF"
    S4_BOX_BD = "#94A3B8"

    # ── Component Drawing Primitives ──────────────────────────
    def draw_section_container(x, y, w, h, title, sec_num, bg_color, border_color, title_color):
        # Section background card
        bg = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                            facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=1)
        ax.add_patch(bg)
        # Header banner pill
        header_text = f"SECTION {sec_num}: {title.upper()}"
        ax.text(x + w / 2, y + h - 2.8, header_text, ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=title_color, zorder=3)
        # Subtle separator line
        ax.plot([x + 1.5, x + w - 1.5], [y + h - 4.6, y + h - 4.6],
                color=border_color, linewidth=1.0, zorder=2)

    def draw_box(x, y, w, h, bg_color, border_color, zorder=3):
        # Shadow
        shadow = FancyBboxPatch((x + 0.25, y - 0.25), w, h, boxstyle="round,pad=0.1,rounding_size=0.8",
                                facecolor="#E2E8F0", edgecolor="none", zorder=zorder-1, alpha=0.6)
        ax.add_patch(shadow)
        # Box
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.8",
                              facecolor=bg_color, edgecolor=border_color, linewidth=1.2, zorder=zorder)
        ax.add_patch(rect)

    def draw_badge(x, y, text, fg_color, bg_color, fontsize=7.5):
        w = len(text) * 0.45 + 1.2
        h = 1.8
        bx = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.5",
                            facecolor=bg_color, edgecolor=fg_color, linewidth=0.8, zorder=6)
        ax.add_patch(bx)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=fg_color, zorder=7)
        return w

    def draw_arrow(x1, y1, x2, y2, color="#475569", lw=1.5, ls="-", zorder=8):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="-|>,head_length=5.0,head_width=3.5",
                                color=color, linewidth=lw, linestyle=ls, zorder=zorder)
        ax.add_patch(arrow)

    def draw_elbow_arrow(x1, y1, x_mid, y2, x2, color="#475569", lw=1.5, ls="-", zorder=8):
        # Line from (x1, y1) to (x_mid, y1) then to (x_mid, y2) then arrow to (x2, y2)
        ax.plot([x1, x_mid, x_mid], [y1, y1, y2], color=color, linewidth=lw, linestyle=ls, zorder=zorder)
        arrow = FancyArrowPatch((x_mid, y2), (x2, y2),
                                arrowstyle="-|>,head_length=5.0,head_width=3.5",
                                color=color, linewidth=lw, linestyle=ls, zorder=zorder)
        ax.add_patch(arrow)

    # ==========================================================
    # HEADER AREA
    # ==========================================================
    ax.text(50, 97.5, "FRAUDSHIELD: System Architecture & End-to-End Federated Learning Pipeline",
            ha="center", va="center", fontsize=16, fontweight="bold", color="#0F172A", zorder=10)
    ax.text(50, 95.0, "Privacy-Preserving Online Payment Fraud Detection with Dual Federated Strategies, Deployed FedAvg Model, SHAP Explainability & Interactive Dashboard",
            ha="center", va="center", fontsize=10, color="#475569", zorder=10)

    # 4 Columns Dimensions (width = 22.8 each, gaps = 1.6)
    # Col 1: x = 2.0 to 24.5 (w = 22.5)
    # Col 2: x = 26.5 to 49.0 (w = 22.5)
    # Col 3: x = 51.0 to 73.5 (w = 22.5)
    # Col 4: x = 75.5 to 98.0 (w = 22.5)
    Y_SEC = 2.0
    H_SEC = 91.0

    # ==========================================================
    # SECTION 1: DATA INGESTION AND PREPROCESSING
    # ==========================================================
    draw_section_container(2.0, Y_SEC, 22.5, H_SEC, "Data Ingestion & Preprocessing", "1", S1_BG, S1_BORDER, S1_ACCENT)

    # Box 1A: Raw Dataset
    y_1a = 66.5
    h_1a = 21.0
    draw_box(3.5, y_1a, 19.5, h_1a, S1_BOX_BG, S1_BOX_BD)
    ax.text(4.5, y_1a + h_1a - 2.4, "IEEE-CIS Fraud Detection Dataset", fontsize=9.5, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
    draw_badge(15.2, y_1a + h_1a - 2.8, "590K Records", "#0F766E", "#CCFBF1")

    bullet_1a = [
        ("• Total Records:", "590,540 transaction instances"),
        ("• Raw Features:", "434 attributes (transaction + identity)"),
        ("• Target Column:", "isFraud ∈ {0 = Legit, 1 = Fraud}"),
        ("• Imbalance Ratio:", "~3.5% fraud prevalence (highly skewed)"),
        ("• Split Strategy:", "Train (413k) / Val (88k) / Test (88k)"),
    ]
    for i, (b_title, b_desc) in enumerate(bullet_1a):
        yy = y_1a + h_1a - 5.2 - (i * 2.8)
        ax.text(4.7, yy, b_title, fontsize=8, fontweight="bold", color="#1E293B", zorder=5)
        ax.text(9.8, yy, b_desc, fontsize=8, color="#334155", zorder=5)

    # Box 1B: Preprocessing Pipeline
    y_1b = 39.0
    h_1b = 23.5
    draw_box(3.5, y_1b, 19.5, h_1b, S1_BOX_BG, S1_BOX_BD)
    ax.text(4.5, y_1b + h_1b - 2.4, "Feature Engineering & Normalization", fontsize=9.5, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
    draw_badge(14.8, y_1b + h_1b - 2.8, "421 Features", "#0F766E", "#CCFBF1")

    bullet_1b = [
        ("• Alias Mapping:", "Normalized 8 key payment attributes"),
        ("• Categorical Encoding:", "29 mapped categories (ProductCD, etc.)"),
        ("• Missing Imputation:", "Persisted training medians (421 cols)"),
        ("• Standardization:", "StandardScaler normalization (mean=0, σ=1)"),
        ("• Scaling Integrity:", "Strict single-pass (no double scaling)"),
        ("• Feature Vector:", "421 clean numerical input dimensions"),
    ]
    for i, (b_title, b_desc) in enumerate(bullet_1b):
        yy = y_1b + h_1b - 5.2 - (i * 2.8)
        ax.text(4.7, yy, b_title, fontsize=8, fontweight="bold", color="#1E293B", zorder=5)
        ax.text(10.5, yy, b_desc, fontsize=8, color="#334155", zorder=5)

    # Box 1C: Non-IID Bank Partitions
    y_1c = 5.0
    h_1c = 30.0
    draw_box(3.5, y_1c, 19.5, h_1c, S1_BOX_BG, S1_BOX_BD)
    ax.text(4.5, y_1c + h_1c - 2.4, "Non-IID Client Data Partitioning", fontsize=9.5, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
    draw_badge(15.2, y_1c + h_1c - 2.8, "5 Partitions", "#0F766E", "#CCFBF1")

    ax.text(4.7, y_1c + h_1c - 5.0, "Heterogeneous Distribution Across 5 Banks:", fontsize=8, fontweight="bold", color="#0F766E", zorder=5)
    partitions = [
        ("Bank 0:", "80,494 transactions", "726 fraud (0.90%)"),
        ("Bank 1:", "81,221 transactions", "1,453 fraud (1.79%)"),
        ("Bank 2:", "81,948 transactions", "2,180 fraud (2.66%)"),
        ("Bank 3:", "83,402 transactions", "3,634 fraud (4.36%)"),
        ("Bank 4:", "86,313 transactions", "6,545 fraud (7.58%)"),
    ]
    for i, (p_name, p_size, p_fraud) in enumerate(partitions):
        yy = y_1c + h_1c - 7.6 - (i * 2.6)
        ax.text(5.0, yy, p_name, fontsize=8, fontweight="bold", color="#1E293B", zorder=5)
        ax.text(7.6, yy, p_size, fontsize=8, color="#475569", zorder=5)
        ax.text(14.0, yy, f"[{p_fraud}]", fontsize=8, fontweight="bold", color="#0F766E", zorder=5)

    ax.plot([4.5, 22.0], [y_1c + 8.2, y_1c + 8.2], color="#CCFBF1", linewidth=0.8, zorder=5)
    ax.text(4.7, y_1c + 6.4, "Evaluation Partitions (Held-Out):", fontsize=7.8, fontweight="bold", color="#334155", zorder=5)
    ax.text(4.7, y_1c + 4.2, "• Validation: 88,581 samples (3.43% fraud) — Threshold Tuning\n• Test Set:    88,581 samples (3.48% fraud) — Final Evaluation",
            fontsize=7.5, color="#475569", zorder=5)

    # Connectors in Section 1
    draw_arrow(13.25, y_1a, 13.25, y_1b + h_1b, color=S1_ACCENT, lw=1.6)
    draw_arrow(13.25, y_1b, 13.25, y_1c + h_1c, color=S1_ACCENT, lw=1.6)

    # ==========================================================
    # SECTION 2: FEDERATED CLIENT NETWORK
    # ==========================================================
    draw_section_container(26.5, Y_SEC, 22.5, H_SEC, "Federated Client Network", "2", S2_BG, S2_BORDER, S2_ACCENT)

    # Top: 5 Client Node Boxes
    client_y = [76.5, 67.5, 58.5, 49.5, 40.5]
    c_names = ["Client 0: Simulated Bank 0", "Client 1: Simulated Bank 1",
               "Client 2: Simulated Bank 2", "Client 3: Simulated Bank 3",
               "Client 4: Simulated Bank 4"]
    c_stats = ["80,494 txns  |  0.90% fraud", "81,221 txns  |  1.79% fraud",
               "81,948 txns  |  2.66% fraud", "83,402 txns  |  4.36% fraud",
               "86,313 txns  |  7.58% fraud"]

    for i in range(5):
        cy = client_y[i]
        draw_box(28.0, cy, 19.5, 7.5, S2_BOX_BG, S2_BOX_BD)
        ax.text(29.0, cy + 4.8, c_names[i], fontsize=8.8, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
        ax.text(29.0, cy + 2.0, c_stats[i], fontsize=7.8, color="#2563EB", zorder=5)
        draw_badge(42.5, cy + 3.8, f"Node {i}", "#1D4ED8", "#DBEAFE", fontsize=7.0)

    # Middle: Common Client Architecture & Configuration Card
    y_2conf = 11.5
    h_2conf = 26.5
    draw_box(28.0, y_2conf, 19.5, h_2conf, "#FFFFFF", "#3B82F6")
    ax.text(29.0, y_2conf + h_2conf - 2.4, "Common Local Client Configuration", fontsize=9.2, fontweight="bold", color="#1E3A8A", zorder=5)
    draw_badge(41.5, y_2conf + h_2conf - 2.8, "Uniform Spec", "#1D4ED8", "#DBEAFE")

    bullet_2conf = [
        ("• Local Model:", "FraudDNN (4-Layer PyTorch Network)"),
        ("• Architecture:", "Linear(421→256) → ReLU → Drop(0.3)"),
        ("", "→ Linear(256→128) → ReLU → Drop(0.3)"),
        ("", "→ Linear(128→64) → ReLU → Drop(0.2) → Linear(64→1)"),
        ("• Optimization:", "Adam Optimizer (Learning Rate = 0.001)"),
        ("• Batch Configuration:", "Batch Size = 512 | Local Epochs = 5"),
        ("• Loss Objective:", "BCEWithLogitsLoss with pos_weight"),
        ("• Weighting Formula:", "pos_weight = (N_legit / N_fraud) per client"),
    ]
    for i, (b_t, b_d) in enumerate(bullet_2conf):
        yy = y_2conf + h_2conf - 4.8 - (i * 2.4)
        if b_t:
            ax.text(29.2, yy, b_t, fontsize=7.6, fontweight="bold", color="#1E293B", zorder=5)
            ax.text(34.8, yy, b_d, fontsize=7.6, color="#334155", zorder=5)
        else:
            ax.text(34.8, yy, b_d, fontsize=7.2, color="#475569", zorder=5)

    # Bottom: Privacy Guarantee Note Banner
    y_2priv = 4.5
    h_2priv = 5.8
    pbox = FancyBboxPatch((28.0, y_2priv), 19.5, h_2priv, boxstyle="round,pad=0.1,rounding_size=0.6",
                          facecolor="#DBEAFE", edgecolor="#93C5FD", linewidth=1.2, zorder=3)
    ax.add_patch(pbox)
    ax.text(37.75, y_2priv + h_2priv - 1.8, "DATA PRIVACY GUARANTEE", ha="center", fontsize=8, fontweight="bold", color="#1E40AF", zorder=5)
    ax.text(37.75, y_2priv + 1.2, "Raw transaction data remains strictly local to each bank.\nOnly model parameter tensors w_k are shared for aggregation.",
            ha="center", va="bottom", fontsize=7.2, color="#1E3A8A", zorder=5)

    # Connector from Section 1 to Section 2 (Data to clients)
    draw_arrow(23.0, 20.0, 28.0, 20.0, color=S1_ACCENT, lw=1.6)
    # Connector from Client nodes down to configuration card
    draw_arrow(37.75, 40.5, 37.75, 38.0, color=S2_ACCENT, lw=1.4)

    # ==========================================================
    # SECTION 3: FEDERATED AGGREGATION AND DUAL MODELS
    # ==========================================================
    draw_section_container(51.0, Y_SEC, 22.5, H_SEC, "Federated Aggregation & Dual Models", "3", S3_BG, S3_BORDER, S3_ACCENT)

    # Box 3A: Central Aggregator Server
    y_3srv = 68.0
    h_3srv = 19.5
    draw_box(52.5, y_3srv, 19.5, h_3srv, S3_BOX_BG, S3_BOX_BD)
    ax.text(53.5, y_3srv + h_3srv - 2.4, "Central Aggregation Server", fontsize=9.5, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
    draw_badge(64.2, y_3srv + h_3srv - 2.8, "Flower Framework", "#6B21A8", "#F3E8FF")

    ax.text(53.7, y_3srv + h_3srv - 5.2, "Sample-Weighted Parameter Averaging Formula:", fontsize=7.8, fontweight="bold", color="#6B21A8", zorder=5)
    # Math formula pill
    f_box = FancyBboxPatch((54.5, y_3srv + h_3srv - 9.8), 15.5, 4.0, boxstyle="round,pad=0.1,rounding_size=0.6",
                           facecolor="#FDF4FF", edgecolor="#D8B4FE", linewidth=1.0, zorder=5)
    ax.add_patch(f_box)
    ax.text(62.25, y_3srv + h_3srv - 7.8, r"$w_{t+1} = \sum_{k=1}^{K} \left(\frac{n_k}{N}\right) w_k^{t+1}$",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#581C87", zorder=6)

    bullet_3srv = [
        ("• Participating Clients:", "5 of 5 simulated banks active every round"),
        ("• Communication Rounds:", "30 global federated aggregation rounds"),
        ("• Total Sample Weights:", "N = 413,378 training records aggregated"),
    ]
    for i, (b_t, b_d) in enumerate(bullet_3srv):
        yy = y_3srv + h_3srv - 12.0 - (i * 2.2)
        ax.text(53.7, yy, b_t, fontsize=7.6, fontweight="bold", color="#1E293B", zorder=5)
        ax.text(61.8, yy, b_d, fontsize=7.6, color="#475569", zorder=5)

    # Box 3B: Primary Model (FedAvg 30R) - GREEN HIGHLIGHT
    y_3avg = 37.0
    h_3avg = 27.5
    draw_box(52.5, y_3avg, 19.5, h_3avg, "#F0FDF4", "#22C55E", zorder=4)
    ax.text(53.5, y_3avg + h_3avg - 2.4, "PRIMARY: FedAvg (30 Rounds)", fontsize=9.5, fontweight="bold", color="#14532D", zorder=5)
    draw_badge(64.2, y_3avg + h_3avg - 2.8, "DEPLOYED MODEL", "#15803D", "#DCFCE7")

    fedavg_specs = [
        ("• Algorithm:", "Standard FedAvg (Proximal μ = 0.0)"),
        ("• Checkpoint File:", "models/fedavg_global_dnn_30r.pth"),
        ("• ROC-AUC (Test):", "0.8101 (Superior Global Discrimination)"),
        ("• PR-AUC (Test):", "0.3225 (+52.1% Gain vs. FedProx)"),
        ("• Overall Accuracy:", "96.29% on 88,581 held-out test records"),
        ("• Fraud Precision:", "45.90% (Substantially Lower False Alarms)"),
        ("• Fraud Recall / F1:", "Recall = 37.63%  |  F1-Score = 41.35%"),
        ("• False Alarm Count:", "1,367 False Positives (691 fewer than FedProx)"),
        ("• Decision Cutoff:", "Optimal Threshold τ = 0.89 (Val F1-Tuned)"),
    ]
    for i, (s_t, s_d) in enumerate(fedavg_specs):
        yy = y_3avg + h_3avg - 5.0 - (i * 2.4)
        ax.text(53.7, yy, s_t, fontsize=7.6, fontweight="bold", color="#14532D", zorder=5)
        ax.text(60.2, yy, s_d, fontsize=7.6, color="#166534", zorder=5)

    # Box 3C: Comparative Model (FedProx 30R) - ROSE/SUBTLE HIGHLIGHT
    y_3prox = 5.0
    h_3prox = 28.5
    draw_box(52.5, y_3prox, 19.5, h_3prox, "#FFF1F2", "#F43F5E", zorder=4)
    ax.text(53.5, y_3prox + h_3prox - 2.4, "COMPARATIVE: FedProx (30 Rounds)", fontsize=9.5, fontweight="bold", color="#881337", zorder=5)
    draw_badge(64.2, y_3prox + h_3prox - 2.8, "BENCHMARK", "#BE123C", "#FFE4E6")

    fedprox_specs = [
        ("• Algorithm:", "FedProx with Proximal Term (μ = 0.01)"),
        ("• Local Penalty:", "+ (μ/2) ||w - w_t||² client drift restraint"),
        ("• Checkpoint File:", "models/fedprox_global_dnn.pth"),
        ("• ROC-AUC (Test):", "0.8004 (High Baseline Separability)"),
        ("• PR-AUC (Test):", "0.2120 (Reduced Precision on Rare Fraud)"),
        ("• Overall Accuracy:", "95.53% on 88,581 held-out test records"),
        ("• Fraud Precision:", "36.48% (Higher False Alarm Rate)"),
        ("• Fraud Recall / F1:", "Recall = 38.34%  |  F1-Score = 37.39%"),
        ("• False Alarm Count:", "2,058 False Positives (+691 vs. FedAvg)"),
        ("• System Role:", "Retained for Benchmark & Instant Rollback"),
    ]
    for i, (s_t, s_d) in enumerate(fedprox_specs):
        yy = y_3prox + h_3prox - 5.0 - (i * 2.3)
        ax.text(53.7, yy, s_t, fontsize=7.5, fontweight="bold", color="#881337", zorder=5)
        ax.text(60.2, yy, s_d, fontsize=7.5, color="#9F1239", zorder=5)

    # Connectors from Clients to Aggregator
    draw_arrow(47.5, 60.0, 52.5, 78.0, color=S2_ACCENT, lw=1.6)
    ax.text(49.8, 70.0, "Weight Updates w_k", fontsize=7.2, fontweight="bold", color=S2_ACCENT, rotation=40, zorder=6)

    # Connector from Aggregator to Primary & Comparative models
    draw_arrow(62.25, y_3srv, 62.25, y_3avg + h_3avg, color="#16A34A", lw=2.0)
    ax.text(62.25, (y_3srv + y_3avg + h_3avg) / 2, "Selected Best Strategy", ha="center", va="center",
            fontsize=7.2, fontweight="bold", color="#15803D",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#DCFCE7", edgecolor="#86EFAC", lw=0.6), zorder=6)

    draw_arrow(70.0, y_3srv, 70.0, y_3prox + h_3prox, color="#BE123C", lw=1.4, ls="--")
    ax.text(70.0, (y_3srv + y_3prox + h_3prox) / 2, "Parallel Benchmark", ha="center", va="center",
            fontsize=7.2, fontweight="bold", color="#9F1239",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFE4E6", edgecolor="#FECDD3", lw=0.6), zorder=6)

    # ==========================================================
    # SECTION 4: PRODUCTION BACKEND AND USER DASHBOARD
    # ==========================================================
    draw_section_container(75.5, Y_SEC, 22.5, H_SEC, "Production Backend & Dashboard", "4", S4_BG, S4_BORDER, S4_ACCENT)

    # Box 4A: Flask REST API Backend
    y_4api = 60.0
    h_4api = 27.5
    draw_box(77.0, y_4api, 19.5, h_4api, S4_BOX_BG, S4_BOX_BD)
    ax.text(78.0, y_4api + h_4api - 2.4, "Flask REST API Backend Engine", fontsize=9.5, fontweight="bold", color=C_TEXT_MAIN, zorder=5)
    draw_badge(88.8, y_4api + h_4api - 2.8, "Flask Service", "#2563EB", "#DBEAFE")

    api_specs = [
        ("• Active Model:", "FedAvg 30R DNN (CPU PyTorch Inference)"),
        ("• Input Alignment:", "Exact 421-dimensional feature schema"),
        ("• Preprocessing:", "Persisted StandardScaler, medians & mappings"),
        ("• Output Probability:", "Sigmoid transformation σ(z) ∈ [0.0, 1.0]"),
        ("• Fraud Threshold:", "Decision cutoff τ = 0.89 (val-optimized)"),
        ("• Decision Rule:", "Prob >= 0.89: Fraud  |  Prob < 0.89: Legit"),
        ("• Risk Levels:", "HIGH (≥0.89) | MEDIUM (0.50–0.89) | LOW (<0.50)"),
        ("• Key Endpoints:", "GET /api/health  &  POST /api/predict"),
    ]
    for i, (a_t, a_d) in enumerate(api_specs):
        yy = y_4api + h_4api - 5.0 - (i * 2.6)
        ax.text(78.2, yy, a_t, fontsize=7.6, fontweight="bold", color="#1E293B", zorder=5)
        ax.text(84.5, yy, a_d, fontsize=7.6, color="#334155", zorder=5)

    # Box 4B: SHAP Explainability Engine
    y_4shap = 33.5
    h_4shap = 22.5
    draw_box(77.0, y_4shap, 19.5, h_4shap, S4_BOX_BG, "#C084FC")
    ax.text(78.0, y_4shap + h_4shap - 2.4, "SHAP Explainability Engine", fontsize=9.5, fontweight="bold", color="#581C87", zorder=5)
    draw_badge(89.2, y_4shap + h_4shap - 2.8, "XAI Module", "#7E22CE", "#F3E8FF")

    shap_specs = [
        ("• Explainer Type:", "shap.GradientExplainer (FedAvg 30R)"),
        ("• Reference Data:", "N = 30 representative background instances"),
        ("• Attribution Level:", "Real-time individual transaction attributions"),
        ("• Top Predictors:", "DeviceType, id_32, card6, id_34, D3, TxnAmt"),
        ("• Risk Drivers:", "Features increasing vs. decreasing fraud risk"),
        ("• Visual Output:", "Global importance chart & transaction factors"),
    ]
    for i, (s_t, s_d) in enumerate(shap_specs):
        yy = y_4shap + h_4shap - 5.0 - (i * 2.6)
        ax.text(78.2, yy, s_t, fontsize=7.6, fontweight="bold", color="#581C87", zorder=5)
        ax.text(84.2, yy, s_d, fontsize=7.6, color="#334155", zorder=5)

    # Box 4C: React Frontend Dashboard
    y_4ui = 5.0
    h_4ui = 24.5
    draw_box(77.0, y_4ui, 19.5, h_4ui, S4_BOX_BG, "#F59E0B")
    ax.text(78.0, y_4ui + h_4ui - 2.4, "React 18 Frontend Dashboard", fontsize=9.5, fontweight="bold", color="#92400E", zorder=5)
    draw_badge(89.5, y_4ui + h_4ui - 2.8, "Client UI", "#D97706", "#FEF3C7")

    ui_specs = [
        ("• Framework & Libs:", "Vite + Tailwind CSS + Lucide React Icons"),
        ("• FileUploadSection:", "CSV batch drag & drop with validation"),
        ("• AnalysisSummary:", "Fraud alert counts, fraud rate, risk gauge"),
        ("• TransactionTable:", "Paginated risk ledger with sorting & filter"),
        ("• Details Drawer:", "Transaction metadata & SHAP factor inspection"),
        ("• Results Export:", "Export categorized CSV ledger with risk scores"),
    ]
    for i, (u_t, u_d) in enumerate(ui_specs):
        yy = y_4ui + h_4ui - 5.0 - (i * 2.6)
        ax.text(78.2, yy, u_t, fontsize=7.6, fontweight="bold", color="#92400E", zorder=5)
        ax.text(84.6, yy, u_d, fontsize=7.6, color="#334155", zorder=5)

    # Inter-section Connectors
    # FedAvg to Flask API
    draw_elbow_arrow(72.0, y_3avg + h_3avg - 5.0, 74.5, y_4api + h_4api - 5.0, 77.0, color="#16A34A", lw=2.0)
    ax.text(74.5, (y_3avg + h_3avg + y_4api + h_4api) / 2 - 2.5, "Deploy Checkpoint", ha="center", va="center",
            fontsize=7.2, fontweight="bold", color="#15803D", rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#DCFCE7", edgecolor="#86EFAC", lw=0.6), zorder=6)

    # Flask API to SHAP
    draw_arrow(86.75, y_4api, 86.75, y_4shap + h_4shap, color="#7E22CE", lw=1.6)
    ax.text(86.75, (y_4api + y_4shap + h_4shap) / 2, "Feature Vectors", ha="center", va="center",
            fontsize=7.0, fontweight="bold", color="#7E22CE",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#F3E8FF", edgecolor="#D8B4FE", lw=0.6), zorder=6)

    # SHAP to React UI
    draw_arrow(86.75, y_4shap, 86.75, y_4ui + h_4ui, color="#D97706", lw=1.6)
    ax.text(86.75, (y_4shap + y_4ui + h_4ui) / 2, "Predictions & Explanations (JSON)", ha="center", va="center",
            fontsize=7.0, fontweight="bold", color="#B45309",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#FDE68A", lw=0.6), zorder=6)

    # ==========================================================
    # SAVE FIGURE IN BOTH RASTER (PNG) AND VECTOR (SVG)
    # ==========================================================
    fig.tight_layout(rect=[0.01, 0.01, 0.99, 0.99])

    # 1. High-resolution PNG
    fig.savefig(PNG_PATH_FIG, dpi=300, facecolor="#FFFFFF", edgecolor="none")
    print(f"Saved publication PNG → {PNG_PATH_FIG}")

    # 2. Editable vector SVG
    fig.savefig(SVG_PATH_FIG, format="svg", facecolor="#FFFFFF", edgecolor="none")
    print(f"Saved editable vector SVG → {SVG_PATH_FIG}")

    # 3. Report diagram replacement
    fig.savefig(PNG_PATH_DIAG, dpi=300, facecolor="#FFFFFF", edgecolor="none")
    print(f"Saved document replacement PNG → {PNG_PATH_DIAG}")

    plt.close(fig)

if __name__ == "__main__":
    generate_figure()


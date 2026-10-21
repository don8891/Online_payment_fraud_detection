"""
scripts/generate_report_pdf.py
==============================
Generates the full academic PDF report:
  reports/Online_Payment_Fraud_Detection_System_Design_Methodology_Results.pdf

Run from project root:
  .venv\Scripts\python.exe scripts/generate_report_pdf.py
"""

import sys, os, io, textwrap
sys.path.insert(0, os.path.abspath("."))

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as mpatch
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ─── paths ────────────────────────────────────────────────────
BASE   = Path(__file__).resolve().parents[1]
FIGS   = BASE / "reports" / "figures"
DIAGS  = BASE / "reports" / "diagrams"
DIAGS.mkdir(parents=True, exist_ok=True)
OUT_PDF = BASE / "reports" / "Online_Payment_Fraud_Detection_System_Design_Methodology_Results.pdf"

# ─── reportlab imports ────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.colors import HexColor, black, white, grey

# ═══════════════════════════════════════════════════════════════
# COLOUR PALETTE
# ═══════════════════════════════════════════════════════════════
BLUE    = HexColor("#1e3a5f")
LBLUE   = HexColor("#2563eb")
ACCENT  = HexColor("#0ea5e9")
TEAL    = HexColor("#0d9488")
GREEN   = HexColor("#16a34a")
AMBER   = HexColor("#d97706")
RED     = HexColor("#dc2626")
LGREY   = HexColor("#f1f5f9")
MGREY   = HexColor("#cbd5e1")
DGREY   = HexColor("#475569")
STRIPE  = HexColor("#eff6ff")

# ═══════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════
def build_styles():
    base = getSampleStyleSheet()
    s = {}
    s['Title'] = ParagraphStyle('DocTitle',
        fontSize=22, leading=28, textColor=BLUE,
        fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=6)
    s['Subtitle'] = ParagraphStyle('Subtitle',
        fontSize=13, leading=18, textColor=DGREY,
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=4)
    s['H1'] = ParagraphStyle('H1',
        fontSize=16, leading=22, textColor=BLUE,
        fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8,
        borderPad=4)
    s['H2'] = ParagraphStyle('H2',
        fontSize=13, leading=18, textColor=LBLUE,
        fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    s['H3'] = ParagraphStyle('H3',
        fontSize=11, leading=16, textColor=DGREY,
        fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)
    s['Body'] = ParagraphStyle('Body',
        fontSize=10, leading=15, textColor=HexColor("#1e293b"),
        fontName='Helvetica', alignment=TA_JUSTIFY,
        spaceAfter=6, firstLineIndent=0)
    s['Bullet'] = ParagraphStyle('Bullet',
        fontSize=10, leading=14, textColor=HexColor("#1e293b"),
        fontName='Helvetica', leftIndent=16, spaceAfter=3,
        bulletIndent=6)
    s['Code'] = ParagraphStyle('Code',
        fontSize=8.5, leading=13, textColor=HexColor("#0f172a"),
        fontName='Courier', leftIndent=12, rightIndent=12,
        backColor=LGREY, borderPad=6, spaceAfter=8)
    s['Caption'] = ParagraphStyle('Caption',
        fontSize=9, leading=13, textColor=DGREY,
        fontName='Helvetica-Oblique', alignment=TA_CENTER,
        spaceAfter=10, spaceBefore=4)
    s['TableHeader'] = ParagraphStyle('TH',
        fontSize=9, leading=12, textColor=white,
        fontName='Helvetica-Bold', alignment=TA_CENTER)
    s['TableCell'] = ParagraphStyle('TC',
        fontSize=9, leading=12, textColor=HexColor("#1e293b"),
        fontName='Helvetica', alignment=TA_CENTER)
    s['TableCellL'] = ParagraphStyle('TCL',
        fontSize=9, leading=12, textColor=HexColor("#1e293b"),
        fontName='Helvetica', alignment=TA_LEFT)
    s['Equation'] = ParagraphStyle('Eq',
        fontSize=11, leading=16, textColor=HexColor("#0f172a"),
        fontName='Courier-Bold', alignment=TA_CENTER,
        spaceAfter=8, spaceBefore=8, backColor=LGREY, borderPad=6)
    s['SectionNote'] = ParagraphStyle('Note',
        fontSize=9, leading=13, textColor=DGREY,
        fontName='Helvetica-Oblique', leftIndent=8, spaceAfter=6)
    return s

ST = build_styles()

# ═══════════════════════════════════════════════════════════════
# HEADER / FOOTER
# ═══════════════════════════════════════════════════════════════
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header bar
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - 28, w, 28, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(white)
    canvas.drawString(1.5*cm, h - 19, "Online Payment Fraud Detection Using Federated Learning")
    canvas.drawRightString(w - 1.5*cm, h - 19,
        "B.Tech CSE Final Year Project")
    # Footer
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(MGREY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(1.5*cm, 7, "System Design · Methodology · Results")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.restoreState()

def on_first_page(canvas, doc):
    # No header/footer on cover page
    pass

# ═══════════════════════════════════════════════════════════════
# DIAGRAM HELPERS  (matplotlib → PNG → reportlab Image)
# ═══════════════════════════════════════════════════════════════
def save_fig(fig, name):
    path = DIAGS / name
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return str(path)

def rl_img(path, width=15*cm):
    from PIL import Image as PILImage
    from reportlab.lib.utils import ImageReader
    img = Image(path)
    # Scale proportionally
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width
    img.drawHeight = width * aspect
    return img

# ─── Figure 1: Overall System Architecture ───────────────────
def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def box(x, y, w, h, color, label, sublabel="", textcolor='white', fontsize=9):
        rect = FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.1", linewidth=1.2,
            edgecolor='#334155', facecolor=color, zorder=3)
        ax.add_patch(rect)
        cy = y + h/2 + (0.12 if sublabel else 0)
        ax.text(x + w/2, cy, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=textcolor, zorder=4)
        if sublabel:
            ax.text(x + w/2, y + h/2 - 0.18, sublabel, ha='center', va='center',
                    fontsize=7, color=textcolor, alpha=0.85, zorder=4)

    def arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle='->', color='#334155', lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.12, label, ha='center', fontsize=7,
                    color='#475569', style='italic')

    # Layer labels
    ax.text(0.2, 6.95, "PRESENTATION LAYER", fontsize=7, color='#64748b',
            fontweight='bold', va='top')
    ax.text(0.2, 5.45, "APPLICATION LAYER", fontsize=7, color='#64748b',
            fontweight='bold', va='top')
    ax.text(0.2, 3.45, "ML INFERENCE LAYER", fontsize=7, color='#64748b',
            fontweight='bold', va='top')
    ax.text(0.2, 1.45, "FEDERATED TRAINING LAYER", fontsize=7, color='#64748b',
            fontweight='bold', va='top')

    # Horizontal dividers
    for y in [6.5, 5.0, 3.0, 1.0]:
        ax.axhline(y, color='#e2e8f0', lw=1, zorder=1)

    # Row 1: User + React Frontend
    box(1.5, 6.6, 2.2, 0.7, '#0ea5e9', "User / Analyst", "Web Browser")
    box(5.0, 6.6, 3.0, 0.7, '#2563eb', "React Dashboard", "FraudGuard AI (Vite + Tailwind)")
    box(9.5, 6.6, 2.2, 0.7, '#0d9488', "CSV Upload", "IEEE-CIS format")
    arrow(3.7, 6.95, 5.0, 6.95, "HTTP/REST")
    arrow(8.0, 6.95, 9.5, 6.95)

    # Row 2: Flask API
    box(4.0, 5.1, 5.0, 0.75, '#1e3a5f', "Flask REST API  (backend/app.py)",
        "GET /api/health  |  GET /api/sample-csv  |  POST /api/predict")
    arrow(6.5, 6.6, 6.5, 5.85)
    arrow(6.5, 5.1, 6.5, 4.75, "JSON response")

    # Row 3: Preprocessing + Model + SHAP
    box(0.8, 3.05, 2.8, 0.85, '#7c3aed', "Preprocessing Pipeline",
        "Median imputation · Cat encoding\nStandardScaler · Feature alignment")
    box(4.1, 3.05, 3.8, 0.85, '#1e3a5f', "FedProx DNN Model",
        "421→256→128→64→1  |  σ(logit) ≥ 0.85")
    box(8.4, 3.05, 3.8, 0.85, '#0d9488', "SHAP GradientExplainer",
        "Top-5 feature attribution per transaction")
    arrow(3.6, 3.47, 4.1, 3.47)
    arrow(7.9, 3.47, 8.4, 3.47)
    arrow(4.5, 5.1, 2.2, 3.9, "raw CSV")
    arrow(5.9, 3.05, 5.9, 2.7)

    # Artefact store
    box(3.5, 2.25, 6.0, 0.65, '#f59e0b', "Model & Preprocessing Artefacts  (models/)",
        "fedprox_global_dnn.pth  |  fedprox_scaler.pkl  |  fedprox_train_medians.pkl  |  fedprox_category_mappings.pkl",
        textcolor='#1e293b')
    arrow(6.5, 2.25, 6.5, 2.0, "load on startup")

    # Row 4: FL training
    clients = [
        (0.5, "Bank A\n(Client 0)\n0.90% fraud"),
        (3.0, "Bank B\n(Client 1)\n1.79% fraud"),
        (5.5, "Bank C\n(Client 2)\n2.66% fraud"),
        (8.0, "Bank D\n(Client 3)\n4.36% fraud"),
        (10.5, "Bank E\n(Client 4)\n7.58% fraud"),
    ]
    for cx, lbl in clients:
        box(cx, 0.05, 2.0, 0.85, '#0ea5e9', lbl, textcolor='white', fontsize=7.5)
        ax.annotate("", xy=(6.5, 1.6), xytext=(cx+1.0, 0.9),
            arrowprops=dict(arrowstyle='->', color='#64748b', lw=0.9))

    box(5.25, 1.55, 2.5, 0.65, '#dc2626', "FedProx Aggregator",
        "Flower framework  |  μ=0.01  |  30 rounds", fontsize=8)

    ax.text(6.5, 0.0, "Simulated non-IID banks — partitions of IEEE-CIS dataset",
            ha='center', fontsize=7.5, color='#64748b', style='italic')

    plt.tight_layout(pad=0.2)
    return save_fig(fig, "fig1_system_architecture.png")

# ─── Figure 2: Federated Learning Architecture ───────────────
def draw_federated_architecture():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def box(x, y, w, h, color, lines, textcolor='white', fontsize=9):
        rect = FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.08", linewidth=1.2,
            edgecolor='#334155', facecolor=color, zorder=3)
        ax.add_patch(rect)
        n = len(lines)
        for i, ln in enumerate(lines):
            yy = y + h - (i+1)*h/(n+1)
            fw = 'bold' if i == 0 else 'normal'
            fs = fontsize if i == 0 else fontsize-1
            ax.text(x+w/2, yy, ln, ha='center', va='center',
                    fontsize=fs, fontweight=fw, color=textcolor, zorder=4)

    def arr(x1,y1,x2,y2,col='#334155',lw=1.4,label=''):
        ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
            arrowprops=dict(arrowstyle='->', color=col, lw=lw))
        if label:
            mx,my=(x1+x2)/2,(y1+y2)/2
            ax.text(mx+0.08, my, label, fontsize=7, color='#475569', style='italic')

    # Central server
    box(4.5, 5.3, 4.0, 1.4, '#1e3a5f',
        ["Central Coordinator (Flower Server)",
         "FedProx / FedAvg Aggregation",
         "Weighted parameter averaging",
         "30 communication rounds"])

    # Clients
    client_info = [
        (0.3, 3.0, "Bank A (Client 0)", "80,494 samples\n0.90% fraud"),
        (2.8, 3.0, "Bank B (Client 1)", "81,221 samples\n1.79% fraud"),
        (5.3, 3.0, "Bank C (Client 2)", "81,948 samples\n2.66% fraud"),
        (7.8, 3.0, "Bank D (Client 3)", "83,402 samples\n4.36% fraud"),
        (10.3, 3.0, "Bank E (Client 4)", "86,313 samples\n7.58% fraud"),
    ]
    for cx, cy, name, sub in client_info:
        box(cx, cy, 2.3, 1.7, '#2563eb',
            [name, sub, "Local DNN training", "FedProx proximal loss"])
        # Upload arrow
        arr(cx+1.15, cy+1.7, 6.5, 5.3, col='#16a34a', label='Δw (updates)')
        # Download arrow
        arr(6.5, 5.3, cx+1.15, cy+1.7, col='#dc2626', label='w_global')

    # FedProx loss box
    box(4.0, 1.2, 5.0, 1.3, '#7c3aed',
        ["FedProx Local Objective  (per client k)",
         "L_k(w) = F_k(w)  +  (μ/2) · ‖w − w_t‖²",
         "μ = 0.01   ·   local_epochs = 5   ·   batch = 512   ·   Adam lr = 0.001"])

    # FedAvg comparison note
    box(0.2, 1.2, 3.3, 1.3, '#d97706',
        ["FedAvg Baseline",
         "No proximal term (μ = 0)",
         "5 rounds  ·  Same DNN architecture",
         "Standard weighted average"])

    # Labels
    ax.text(6.5, 6.85, "IEEE-CIS Dataset (Simulated Multi-Bank, Non-IID Partitions)",
            ha='center', fontsize=9, fontweight='bold', color='#1e3a5f')
    ax.text(6.5, 0.85, "Legend:  → send global model   → return local updates",
            ha='center', fontsize=7.5, color='#64748b', style='italic')

    arr(6.5, 1.2, 6.5, 5.3, col='#7c3aed', lw=0.8, label='proximal regularisation')

    plt.tight_layout(pad=0.3)
    return save_fig(fig, "fig2_federated_architecture.png")

# ─── Figure 3: DNN Architecture ──────────────────────────────
def draw_dnn_architecture():
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 5)
    ax.axis('off'); fig.patch.set_facecolor('white')

    layers = [
        (0.5,  2.0, 1.8, 1.0, '#0ea5e9',  "Input Layer",    "421 features\n(IEEE-CIS)"),
        (2.8,  1.7, 2.0, 1.6, '#2563eb',  "Hidden Layer 1", "256 neurons\nReLU · Dropout(0.3)"),
        (5.3,  1.7, 2.0, 1.6, '#1e3a5f',  "Hidden Layer 2", "128 neurons\nReLU · Dropout(0.3)"),
        (7.8,  1.7, 2.0, 1.6, '#7c3aed',  "Hidden Layer 3", "64 neurons\nReLU · Dropout(0.2)"),
        (10.3, 2.0, 1.8, 1.0, '#dc2626',  "Output Layer",   "1 neuron\nBCE logit"),
    ]
    def box(x,y,w,h,col,t,sub):
        r = FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.1",
            linewidth=1.3, edgecolor='#334155', facecolor=col, zorder=3)
        ax.add_patch(r)
        ax.text(x+w/2, y+h*0.65, t, ha='center', va='center',
                fontsize=9, fontweight='bold', color='white', zorder=4)
        ax.text(x+w/2, y+h*0.28, sub, ha='center', va='center',
                fontsize=7.5, color='white', zorder=4)

    for args in layers:
        box(*args)

    # Arrows between layers
    xs = [2.3, 4.8, 7.3, 9.8]
    for x in xs:
        ax.annotate("", xy=(x+0.05, 2.5), xytext=(x-0.05+0.5, 2.5),
            arrowprops=dict(arrowstyle='->', color='#334155', lw=1.5))

    # Sigmoid + threshold note
    ax.text(12.25, 4.2, "σ(logit)", ha='center', fontsize=9, fontweight='bold', color='#dc2626')
    ax.text(12.25, 3.85, "Sigmoid", ha='center', fontsize=8, color='#64748b')
    ax.annotate("", xy=(12.1, 3.7), xytext=(11.4, 2.6),
        arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.2))

    ax.text(12.25, 3.3, "≥ 0.85", ha='center', fontsize=9,
            fontweight='bold', color='#dc2626')
    ax.text(12.25, 3.0, "→ FRAUD", ha='center', fontsize=8.5,
            fontweight='bold', color='#dc2626')
    ax.text(12.25, 2.65, "< 0.85", ha='center', fontsize=9,
            fontweight='bold', color='#16a34a')
    ax.text(12.25, 2.35, "→ LEGIT", ha='center', fontsize=8.5,
            fontweight='bold', color='#16a34a')

    # Loss function note
    ax.text(6.5, 0.5,
        "Loss: BCEWithLogitsLoss with pos_weight = (legitimate count / fraud count) per client  |  "
        "Optimizer: Adam  |  lr = 0.001",
        ha='center', fontsize=8, color='#475569', style='italic')

    ax.text(6.5, 4.7, "FraudDNN Architecture (federated/model.py)",
            ha='center', fontsize=11, fontweight='bold', color='#1e3a5f')

    plt.tight_layout(pad=0.3)
    return save_fig(fig, "fig3_dnn_architecture.png")

# ─── Figure 4: End-to-End Flowchart ──────────────────────────
def draw_e2e_flow():
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6.5)
    ax.axis('off'); fig.patch.set_facecolor('white')

    steps = [
        (0.3,  5.5, 1.8, 0.75, '#0ea5e9', "IEEE-CIS\nDataset"),
        (2.6,  5.5, 1.8, 0.75, '#7c3aed', "Data\nPreprocessing"),
        (4.9,  5.5, 1.8, 0.75, '#2563eb', "Client\nPartitioning\n(5 banks, non-IID)"),
        (7.2,  5.5, 1.8, 0.75, '#1e3a5f', "Local DNN\nTraining\n(FedProx / FedAvg)"),
        (9.5,  5.5, 1.8, 0.75, '#dc2626', "Federated\nAggregation\n(Flower Server)"),
        (11.8, 5.5, 1.8, 0.75, '#0d9488', "Global Model\nEvaluation\n(Test set)"),
    ]
    for x,y,w,h,col,lbl in steps:
        r = FancyBboxPatch((x,y),w,h, boxstyle="round,pad=0.08",
            edgecolor='#334155', facecolor=col, linewidth=1.2, zorder=3)
        ax.add_patch(r)
        ax.text(x+w/2, y+h/2, lbl, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white', zorder=4)

    # Horizontal arrows
    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        x2 = steps[i+1][0]
        y  = steps[i][1] + steps[i][3]/2
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle='->', color='#334155', lw=1.4))

    # Second row: inference pipeline
    steps2 = [
        (0.3,  3.0, 2.0, 0.75, '#0d9488', "Model\nCheckpoint saved\n(models/)"),
        (2.9,  3.0, 2.0, 0.75, '#7c3aed', "Backend loads\nmodel + artefacts\n(startup)"),
        (5.5,  3.0, 2.0, 0.75, '#2563eb', "User uploads\nCSV via\nReact Dashboard"),
        (8.1,  3.0, 2.0, 0.75, '#1e3a5f', "Flask /api/predict\npreprocesses &\nruns DNN inference"),
        (10.7, 3.0, 2.0, 0.75, '#dc2626', "Fraud risk output\n(prob ≥ 0.85\n→ FLAGGED)"),
    ]
    for x,y,w,h,col,lbl in steps2:
        r = FancyBboxPatch((x,y),w,h, boxstyle="round,pad=0.08",
            edgecolor='#334155', facecolor=col, linewidth=1.2, zorder=3)
        ax.add_patch(r)
        ax.text(x+w/2, y+h/2, lbl, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white', zorder=4)

    for i in range(len(steps2)-1):
        x1 = steps2[i][0] + steps2[i][2]
        x2 = steps2[i+1][0]
        y  = steps2[i][1] + steps2[i][3]/2
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle='->', color='#334155', lw=1.4))

    # Vertical connector (training → inference)
    ax.annotate("", xy=(1.3, 3.75), xytext=(11.9, 5.5),
        arrowprops=dict(arrowstyle='->', color='#475569', lw=1.2, linestyle='dashed'))
    ax.text(6.5, 4.45, "─── TRAINING PIPELINE ───", ha='center', fontsize=9,
            fontweight='bold', color='#1e3a5f')
    ax.text(6.5, 2.6, "─── INFERENCE PIPELINE ───", ha='center', fontsize=9,
            fontweight='bold', color='#1e3a5f')

    # SHAP branch
    ax.annotate("", xy=(11.7, 2.35), xytext=(11.7, 3.0),
        arrowprops=dict(arrowstyle='->', color='#d97706', lw=1.2))
    r = FancyBboxPatch((10.7, 1.55), 2.0, 0.75,
        boxstyle="round,pad=0.08", edgecolor='#d97706', facecolor='#fef3c7', linewidth=1.2, zorder=3)
    ax.add_patch(r)
    ax.text(11.7, 1.92, "SHAP explanation\n(Top-5 features)", ha='center', va='center',
            fontsize=7.5, fontweight='bold', color='#92400e', zorder=4)

    ax.text(6.5, 0.4, "Non-IID client distribution ensures FedProx training reflects realistic multi-bank data heterogeneity",
            ha='center', fontsize=8, color='#64748b', style='italic')

    plt.tight_layout(pad=0.3)
    return save_fig(fig, "fig4_e2e_flow.png")

# ─── Figure 5: User Prediction Workflow ──────────────────────
def draw_user_workflow():
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 5)
    ax.axis('off'); fig.patch.set_facecolor('white')

    steps = [
        (0.3,  2.0, 1.9, 0.9,  '#0ea5e9', "User\nUploads CSV", "React Dashboard"),
        (2.6,  2.0, 1.9, 0.9,  '#2563eb', "POST /api/predict", "Flask backend"),
        (4.9,  2.0, 1.9, 0.9,  '#7c3aed', "Preprocessing\nPipeline", "Impute→Encode→Scale"),
        (7.2,  2.0, 1.9, 0.9,  '#1e3a5f', "FedProx DNN\nInference", "421→256→128→64→1"),
        (9.5,  2.0, 1.9, 0.9,  '#d97706', "σ(logit)\nThreshold ≥ 0.85", "FRAUD / LEGIT"),
        (11.3, 2.0, 1.9, 0.9,  '#0d9488', "Results + SHAP\nReturned", "JSON → React UI"),
    ]
    for x,y,w,h,col,lbl,sub in steps:
        r = FancyBboxPatch((x,y),w,h, boxstyle="round,pad=0.08",
            edgecolor='#334155', facecolor=col, linewidth=1.2, zorder=3)
        ax.add_patch(r)
        ax.text(x+w/2, y+h*0.62, lbl, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', zorder=4)
        ax.text(x+w/2, y+h*0.22, sub, ha='center', va='center',
                fontsize=7, color='white', alpha=0.9, zorder=4)

    for i in range(len(steps)-1):
        x1 = steps[i][0] + steps[i][2]
        x2 = steps[i+1][0]
        y  = steps[i][1] + steps[i][3]/2
        ax.annotate("", xy=(x2+0.02, y), xytext=(x1-0.02, y),
            arrowprops=dict(arrowstyle='->', color='#334155', lw=1.5))

    # Artefact load arrows
    arts = [
        (4.95, "fedprox_train_medians.pkl\nfedprox_category_mappings.pkl"),
        (6.2,  "fedprox_scaler.pkl"),
        (7.25, "fedprox_global_dnn.pth"),
    ]
    for ax_x, lbl in arts:
        ax.annotate("", xy=(ax_x+0.95, 2.0), xytext=(ax_x+0.95, 0.95),
            arrowprops=dict(arrowstyle='->', color='#94a3b8', lw=1.0))
        ax.text(ax_x+0.95, 0.78, lbl, ha='center', fontsize=6.5, color='#64748b')

    r2 = FancyBboxPatch((3.8, 0.25), 6.0, 0.5,
        boxstyle="round,pad=0.05", edgecolor='#f59e0b', facecolor='#fef3c7', linewidth=1.0)
    ax.add_patch(r2)
    ax.text(6.8, 0.5, "models/  — preprocessing artefacts + FedProx DNN checkpoint loaded once at backend startup",
            ha='center', va='center', fontsize=7, color='#92400e')

    ax.text(6.5, 4.6, "User Fraud Prediction Workflow — Dashboard to FedProx DNN Inference",
            ha='center', fontsize=11, fontweight='bold', color='#1e3a5f')

    plt.tight_layout(pad=0.3)
    return save_fig(fig, "fig5_user_workflow.png")

# ═══════════════════════════════════════════════════════════════
# GENERATE ALL DIAGRAMS
# ═══════════════════════════════════════════════════════════════
print("Generating architecture diagrams ...")
FIG1 = draw_system_architecture()
print("  Fig 1 done")
FIG2 = draw_federated_architecture()
print("  Fig 2 done")
FIG3 = draw_dnn_architecture()
print("  Fig 3 done")
FIG4 = draw_e2e_flow()
print("  Fig 4 done")
FIG5 = draw_user_workflow()
print("  Fig 5 done")

# Research figures (already exist)
FIG6  = str(FIGS / "fedprox_confusion_matrix.png")
FIG7  = str(FIGS / "fedavg_confusion_matrix.png")
FIG8  = str(FIGS / "roc_curve_federated.png")
FIG9  = str(FIGS / "precision_recall_federated.png")
FIG10 = str(FIGS / "model_performance_comparison.png")
FIG11 = str(FIGS / "fedprox_shap_feature_importance.png")

# ═══════════════════════════════════════════════════════════════
# CONTENT BUILDERS
# ═══════════════════════════════════════════════════════════════
def h1(text):
    return Paragraph(text, ST['H1'])
def h2(text):
    return Paragraph(text, ST['H2'])
def h3(text):
    return Paragraph(text, ST['H3'])
def p(text):
    return Paragraph(text, ST['Body'])
def bull(text):
    return Paragraph(f"• {text}", ST['Bullet'])
def caption(text):
    return Paragraph(text, ST['Caption'])
def code(text):
    return Paragraph(text.replace('\n','<br/>').replace(' ','&nbsp;'), ST['Code'])
def eq(text):
    return Paragraph(text, ST['Equation'])
def sp(h=6):
    return Spacer(1, h)
def hr():
    return HRFlowable(width="100%", thickness=0.5, color=MGREY, spaceAfter=4)
def pb():
    return PageBreak()

def make_table(headers, rows, col_widths=None, stripe=True):
    data = [[Paragraph(h, ST['TableHeader']) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), ST['TableCellL'] if j==0 else ST['TableCell'])
                     for j, c in enumerate(row)])
    style = [
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, STRIPE] if stripe else [white]),
        ('GRID',       (0,0), (-1,-1), 0.4, MGREY),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',(0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0),(-1,-1), 6),
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t

def fig_img(path, width=14*cm, caption_text=""):
    items = [sp(4), rl_img(path, width=width), sp(2)]
    if caption_text:
        items.append(Paragraph(caption_text, ST['Caption']))
    items.append(sp(8))
    return items

# ═══════════════════════════════════════════════════════════════
# BUILD DOCUMENT STORY
# ═══════════════════════════════════════════════════════════════
story = []

# ─── COVER PAGE ───────────────────────────────────────────────
story.append(sp(60))
story.append(Paragraph("B.TECH COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle('CoverSub',
    fontSize=11, alignment=TA_CENTER, textColor=DGREY, fontName='Helvetica',
    spaceAfter=4)))
story.append(Paragraph("FINAL YEAR PROJECT REPORT", ParagraphStyle('CoverSub2',
    fontSize=10, alignment=TA_CENTER, textColor=DGREY, fontName='Helvetica',
    spaceAfter=30)))
story.append(HRFlowable(width="70%", thickness=2, color=BLUE, spaceAfter=20))
story.append(Paragraph("Online Payment Fraud Detection Using", ST['Title']))
story.append(Paragraph("Non-IID-Aware Federated Learning with FedProx", ST['Title']))
story.append(HRFlowable(width="70%", thickness=2, color=BLUE, spaceAfter=20))
story.append(sp(20))
story.append(Paragraph(
    "System Design and Architecture · Methodology and Implementation ·<br/>"
    "Results and Discussion · Appendices",
    ST['Subtitle']))
story.append(sp(40))

cover_table_data = [
    ["Repository", "github.com/don8891/Online_payment_fraud_detection"],
    ["Dataset",    "IEEE-CIS Fraud Detection (Kaggle)"],
    ["Principal Model", "FedProx Deep Neural Network (DNN)"],
    ["Baseline Model",  "FedAvg Deep Neural Network (DNN)"],
    ["Framework",  "Flower (flwr) — Federated Learning"],
    ["Backend",    "Python · Flask REST API"],
    ["Frontend",   "React · Vite · Tailwind CSS"],
    ["Explainability", "SHAP GradientExplainer"],
    ["Test ROC-AUC (FedProx)", "0.8004"],
    ["Test PR-AUC (FedProx)",  "0.2120"],
    ["Classification Threshold", "0.85 (validation F1-optimised)"],
]
ct = Table([[Paragraph(k, ParagraphStyle('CK', fontSize=9, fontName='Helvetica-Bold',
                textColor=BLUE)), Paragraph(v, ParagraphStyle('CV', fontSize=9,
                fontName='Helvetica', textColor=HexColor("#1e293b")))]
            for k, v in cover_table_data],
           colWidths=[6*cm, 10*cm])
ct.setStyle(TableStyle([
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, STRIPE]),
    ('GRID', (0,0), (-1,-1), 0.4, MGREY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(ct)
story.append(pb())

# ─── SECTION 1: SYSTEM DESIGN AND ARCHITECTURE ───────────────
story.append(h1("1. SYSTEM DESIGN AND ARCHITECTURE"))
story.append(hr())

story.append(h2("1.1 System Overview"))
story.append(p(
    "This project presents an end-to-end system for online payment fraud detection using "
    "privacy-preserving Federated Learning. The system integrates a simulated multi-bank "
    "federated training pipeline, a Deep Neural Network (DNN) fraud classifier, a RESTful "
    "Flask backend, and an interactive React dashboard. The FedProx algorithm serves as the "
    "principal federated optimiser, with FedAvg as the comparison baseline. Both algorithms "
    "are orchestrated using the Flower (flwr) framework."
))
story.append(p(
    "The system is designed for the IEEE-CIS Fraud Detection benchmark dataset. Five simulated "
    "bank clients hold disjoint, non-identically distributed (non-IID) data partitions. A "
    "central Flower server performs parameter aggregation across communication rounds. The "
    "resulting global model is served through the Flask backend for batch transaction scoring "
    "via CSV upload. SHAP feature attributions accompany each prediction to provide "
    "interpretable risk explanations."
))

story.append(h2("1.2 Problem Definition"))
story.append(p(
    "Online payment fraud is a severe financial threat characterised by extreme class imbalance: "
    "fraudulent transactions represent approximately 3.5% of all records in the IEEE-CIS dataset, "
    "while legitimate transactions dominate the remaining 96.5%. Standard centralised training "
    "approaches require all raw transaction data to be aggregated at a single location, raising "
    "significant data-privacy concerns for multi-institutional deployments."
))
story.append(p(
    "Federated Learning addresses these concerns by training the model locally at each "
    "participating institution (simulated bank) and sharing only model parameter updates—not "
    "raw transaction data—with a central aggregator. However, non-IID data distributions across "
    "banks cause standard FedAvg convergence to degrade. FedProx introduces a proximal "
    "regularisation term that constrains local model updates to remain close to the current "
    "global model, improving stability under data heterogeneity."
))

story.append(h2("1.3 Functional Requirements"))
for req in [
    "Accept a batch CSV file of IEEE-CIS-compatible transaction records via a web interface.",
    "Preprocess transactions (missing-value imputation, categorical encoding, StandardScaler normalisation).",
    "Run the FedProx DNN model to produce fraud probability scores for each transaction.",
    "Apply a threshold of 0.85 (selected by validation-set F1 maximisation) to classify transactions as fraudulent or legitimate.",
    "Return per-transaction predictions, risk levels (HIGH / MEDIUM / LOW), and SHAP feature attributions.",
    "Expose a REST API with endpoints for health checking, sample CSV download, and batch prediction.",
    "Display results in a React dashboard with searchable transaction tables and fraud-alert summaries.",
    "Support simulated federated training using the Flower framework across five non-IID bank clients.",
    "Evaluate and compare FedProx and FedAvg using ROC-AUC, PR-AUC, precision, recall, F1-score, and confusion matrices.",
]:
    story.append(bull(req))
story.append(sp(4))

story.append(h2("1.4 Non-Functional Requirements"))
for req in [
    "Privacy: Raw transaction data remains at each simulated bank; only model gradients/parameters are shared.",
    "Reproducibility: Random seed fixed to 42; preprocessing artefacts (scaler, medians, mappings) are persisted.",
    "Scalability: The architecture supports extension to additional bank clients without redesigning the aggregation logic.",
    "Accuracy: The FedProx DNN achieves ROC-AUC of 0.8004 on the held-out IEEE-CIS test set.",
    "Interpretability: SHAP GradientExplainer provides feature-level explanations for each prediction.",
    "Performance: Backend serves predictions for batch CSV files; no real-time stream processing is implemented.",
    "Portability: The system runs on a single Windows machine; no distributed infrastructure is required.",
]:
    story.append(bull(req))
story.append(sp(4))

story.append(h2("1.5 Overall System Architecture"))
story.append(p(
    "Figure 1 illustrates the full system architecture across four layers: Presentation (React dashboard), "
    "Application (Flask REST API), ML Inference (preprocessing pipeline + FedProx DNN + SHAP), and "
    "Federated Training (Flower-orchestrated multi-bank simulation). Model artefacts are persisted to "
    "the models/ directory and loaded once at backend startup."
))
story += fig_img(FIG1, width=15.5*cm,
    caption_text="Figure 1: Overall System Architecture — four-layer design from user interface to federated training pipeline.")

story.append(h2("1.6 Dataset and Data-Processing Architecture"))
story.append(p(
    "The IEEE-CIS Fraud Detection dataset is loaded from data/raw/ and processed through a sequence of "
    "operations executed in notebook 02_data_preprocessing.ipynb and notebook 04_dnn_baseline.ipynb. "
    "Processed partitions are stored in data/processed/ as serialised Pandas DataFrames (.pkl). "
    "Preprocessing artefacts — the StandardScaler, training medians, and category mappings — are "
    "serialised to models/ using joblib. These artefacts are loaded by the Flask backend's "
    "FraudModelService at startup to guarantee that inference-time preprocessing is identical to "
    "training-time preprocessing, preventing data-leakage and distribution shift."
))

story.append(h2("1.7 Federated Learning Architecture"))
story.append(p(
    "Figure 2 presents the federated learning architecture. Five simulated bank clients (Bank A–E) "
    "each hold a non-IID partition of the IEEE-CIS training set. In each communication round, the "
    "central Flower server broadcasts the current global model parameters to all clients. Each client "
    "then performs local training for five epochs using the FedProx objective and returns the updated "
    "parameter tensors. The server aggregates the updates using weighted parameter averaging, "
    "proportional to the number of local training samples, and broadcasts the new global model. "
    "This cycle repeats for 30 rounds."
))
story += fig_img(FIG2, width=15.5*cm,
    caption_text="Figure 2: Federated Learning Architecture — five simulated non-IID bank clients, FedProx proximal objective, and Flower aggregation server.")

story.append(h2("1.8 DNN Model Architecture"))
story.append(p(
    "Figure 3 shows the FraudDNN neural network (federated/model.py). The network comprises a "
    "421-dimensional input layer, three hidden layers (256, 128, and 64 neurons) each using ReLU "
    "activation and Dropout regularisation, followed by a single output neuron. The logit output "
    "is passed through the sigmoid function during inference to obtain a fraud probability in [0, 1]. "
    "A classification threshold of 0.85 is applied: probabilities at or above this value are "
    "classified as fraudulent."
))
story += fig_img(FIG3, width=14*cm,
    caption_text="Figure 3: FraudDNN Architecture — 421 → 256 → 128 → 64 → 1 with ReLU activations, Dropout regularisation, and sigmoid output.")

story.append(h2("1.9 Backend Architecture"))
story.append(p(
    "The Flask application (backend/app.py) exposes three REST endpoints. The FraudModelService "
    "(backend/services/model_service.py) handles model loading, preprocessing, DNN inference, "
    "SHAP attribution, and result serialisation. The service is instantiated once at module load "
    "time and reused across requests. Flask-CORS is enabled to allow cross-origin requests from "
    "the React frontend running on a different port."
))
for ep in [
    "<b>GET /api/health</b> — Returns backend status, model name, feature count, and decision threshold.",
    "<b>GET /api/sample-csv</b> — Serves a sample IEEE-CIS-format CSV file for quick testing.",
    "<b>POST /api/predict</b> — Accepts a multipart CSV upload; runs preprocessing and DNN inference; returns per-transaction predictions, risk levels, and SHAP attributions as JSON.",
]:
    story.append(bull(ep))
story.append(sp(4))

story.append(h2("1.10 Frontend Architecture"))
story.append(p(
    "The frontend is a React single-page application built with Vite and styled using Tailwind CSS v4. "
    "It provides three navigation tabs: Overview (file upload, KPI summary, preview table), "
    "Transaction Analysis (full searchable and filterable ledger), and Fraud Alerts (high-risk "
    "transactions sorted by probability). The application polls the /api/health endpoint every "
    "15 seconds and displays backend connectivity status and model metadata in the sidebar."
))

story.append(h2("1.11 Model Inference and Fraud Prediction Workflow"))
story.append(p(
    "Figure 4 shows the end-to-end pipeline from dataset ingestion through federated training "
    "to live inference. Figure 5 shows the user-facing prediction workflow."
))
story += fig_img(FIG4, width=15.5*cm,
    caption_text="Figure 4: End-to-End Fraud Detection Flowchart — from raw IEEE-CIS data through federated training to backend inference and risk output.")
story += fig_img(FIG5, width=15*cm,
    caption_text="Figure 5: User Prediction Workflow — CSV upload through Flask preprocessing, DNN inference, threshold classification, and SHAP attribution.")

story.append(h2("1.12 Data Privacy Considerations"))
story.append(p(
    "The federated architecture ensures that raw transaction records never leave the simulated "
    "bank environment. Only floating-point model parameter arrays are transmitted between clients "
    "and the aggregation server. This design is aligned with the principle of data minimisation "
    "and is motivated by real-world banking regulations such as GDPR. In a production deployment, "
    "communication channels would require TLS encryption and authenticated client identities. "
    "Differential privacy and secure aggregation are not implemented in this prototype but are "
    "identified as natural extensions."
))

story.append(h2("1.13 Design Limitations"))
for lim in [
    "Banks are simulated using static partitions of a single publicly available dataset; real multi-bank deployment is not implemented.",
    "Communication uses Flower's in-process simulation rather than a networked multi-machine deployment.",
    "No differential privacy, gradient clipping, or secure multi-party computation is applied.",
    "The backend processes CSV uploads synchronously; very large files may cause latency.",
    "The system does not implement authentication, session management, or a persistent database.",
    "FedAvg was trained for only 5 rounds in the comparison simulation, compared to 30 rounds for FedProx, which may account for part of the performance gap.",
]:
    story.append(bull(lim))
story.append(pb())

# ─── SECTION 2: METHODOLOGY ────────────────────────────────────
story.append(h1("2. METHODOLOGY AND IMPLEMENTATION"))
story.append(hr())

story.append(h2("2.1 Dataset — IEEE-CIS Fraud Detection"))
story.append(p(
    "The IEEE-CIS Fraud Detection dataset, published through a Kaggle competition, contains "
    "real anonymised online payment transactions. It comprises a transaction table and an "
    "identity table merged on TransactionID. Features include transaction amount, device "
    "information, card metadata, email domains, and a set of engineered V-features (V1–V339) "
    "derived from the original Vesta proprietary system. The binary target label isFraud "
    "indicates whether a transaction was later confirmed as fraudulent."
))
story.append(p(
    "After preprocessing and train/validation/test splitting, the following partition sizes "
    "were verified from the serialised data files (data/processed/):"
))
story.append(make_table(
    ["Split", "Samples", "Features", "Fraud Count", "Fraud Rate"],
    [
        ["Training set",   "413,378",  "421", "14,538", "3.52%"],
        ["Validation set", "88,581",   "421", "3,042",  "3.43%"],
        ["Test set",       "88,581",   "421", "3,083",  "3.48%"],
        ["Total",          "590,540",  "421", "20,663", "3.50%"],
    ],
    col_widths=[4*cm, 3.5*cm, 3*cm, 3.5*cm, 3*cm]
))
story.append(caption("Table 1: Dataset Summary — verified from data/processed/ pickle files."))
story.append(sp(6))

story.append(p(
    "The severe class imbalance (approximately 96.5% legitimate) is addressed during training "
    "through class-weighted loss: the BCEWithLogitsLoss pos_weight for each client equals the "
    "ratio of legitimate samples to fraud samples in that client's local dataset."
))

story.append(h2("2.2 Data Preprocessing"))
story.append(p(
    "Preprocessing is implemented across notebooks 02_data_preprocessing.ipynb and "
    "04_dnn_baseline.ipynb and applied consistently at inference time by FraudModelService. "
    "The pipeline comprises the following verified steps:"
))
for step in [
    "<b>Column normalisation:</b> Column names are stripped, lower-cased, and mapped through an alias dictionary to resolve common naming variants (e.g., 'amount' → 'TransactionAmt').",
    "<b>Categorical encoding:</b> Twenty-nine categorical columns (including ProductCD, card4, card6, P_emaildomain, R_emaildomain, and DeviceType) are mapped to integer codes using dictionaries fitted on the training set. Unknown categories encountered at inference time are mapped to −1. Artefact: models/fedprox_category_mappings.pkl.",
    "<b>Missing value imputation:</b> Numerical missing values are filled using per-feature medians computed from the training set. Any remaining NaN values are replaced with zero. Artefact: models/fedprox_train_medians.pkl.",
    "<b>Feature alignment:</b> The model expects exactly 421 features in a fixed order. Missing columns are added as NaN before imputation; extra columns are ignored.",
    "<b>Standardisation:</b> A scikit-learn StandardScaler is fitted on the training set (413,378 samples × 421 features) and applied to training, validation, test, and inference data. Artefact: models/fedprox_scaler.pkl (StandardScaler, n_features_in_ = 421).",
    "<b>Client data:</b> Each of the five client partitions (federated/data/client_0/ … client_4/) contains X.pkl files with pre-scaled features. The client training loop in federated/client.py converts these directly to float32 tensors without re-applying the scaler, avoiding double-scaling.",
    "<b>Train / validation / test split:</b> The dataset is partitioned chronologically to avoid temporal leakage. The validation set is used exclusively for threshold selection; the test set is used for final evaluation.",
]:
    story.append(bull(step))
story.append(sp(4))

story.append(h2("2.3 Non-IID Client Simulation"))
story.append(p(
    "The federated training uses five simulated bank clients (Bank A through Bank E) created by "
    "partitioning the training set into non-identically distributed subsets. The fraud rate "
    "increases monotonically from Client 0 (0.90%) to Client 4 (7.58%), producing a "
    "heterogeneous distribution that reflects realistic multi-bank scenarios where fraud "
    "exposure varies by institution size, geographic region, and customer segment."
))
story.append(make_table(
    ["Client", "Simulated Bank", "Local Samples", "Fraud Count", "Local Fraud Rate"],
    [
        ["Client 0", "Bank A", "80,494",  "726",   "0.90%"],
        ["Client 1", "Bank B", "81,221",  "1,453", "1.79%"],
        ["Client 2", "Bank C", "81,948",  "2,180", "2.66%"],
        ["Client 3", "Bank D", "83,402",  "3,634", "4.36%"],
        ["Client 4", "Bank E", "86,313",  "6,545", "7.58%"],
        ["Total",    "—",      "413,378", "14,538","3.52%"],
    ],
    col_widths=[2.5*cm, 3*cm, 3.5*cm, 3*cm, 3.5*cm]
))
story.append(caption("Table 2: Non-IID Client Data Distribution — verified from federated/data/client_*/X.pkl and y.pkl."))
story.append(sp(6))
story.append(p(
    "In an IID (independently and identically distributed) scenario, each client's data would "
    "have approximately the same fraud rate as the global dataset. The deliberate non-IID "
    "partitioning here means that FedAvg's assumption of homogeneous gradient directions "
    "across clients is violated, which degrades its convergence — a known weakness that "
    "FedProx's proximal penalty is designed to mitigate."
))

story.append(h2("2.4 DNN Architecture"))
story.append(p(
    "The FraudDNN class (federated/model.py) implements a fully connected feedforward network "
    "with the following verified configuration:"
))
story.append(make_table(
    ["Component", "Specification"],
    [
        ["Input dimension",    "421 (IEEE-CIS preprocessed features)"],
        ["Hidden Layer 1",     "Linear(421, 256) → ReLU → Dropout(p=0.3)"],
        ["Hidden Layer 2",     "Linear(256, 128) → ReLU → Dropout(p=0.3)"],
        ["Hidden Layer 3",     "Linear(128, 64)  → ReLU → Dropout(p=0.2)"],
        ["Output Layer",       "Linear(64, 1)  (raw logit)"],
        ["Activation (output)","sigmoid applied at inference time"],
        ["Loss function",       "BCEWithLogitsLoss with pos_weight per client"],
        ["Optimizer",          "Adam (lr = 0.001)"],
        ["Batch size",         "512"],
        ["Local epochs",       "5 per communication round"],
        ["Total parameters",   "~148k (estimated)"],
    ],
    col_widths=[6.5*cm, 10.5*cm]
))
story.append(caption("Table 3: FraudDNN Architecture and Training Configuration (verified from source code)."))
story.append(sp(6))

story.append(h2("2.5 FedProx Training Algorithm"))
story.append(p(
    "FedProx (Li et al., 2020) modifies the standard federated learning objective by adding a "
    "proximal regularisation term to each client's local loss function. The local objective for "
    "client k at communication round t is:"
))
story.append(eq("L_k(w)  =  F_k(w)  +  (μ / 2) · ‖w − w_t‖²"))
story.append(p(
    "where F_k(w) is the standard empirical loss (BCEWithLogitsLoss) on client k's local data, "
    "w is the current local model parameters, w_t is the global model parameters at round t "
    "(received from the server), and μ (mu) is the proximal regularisation strength. "
    "In this project, μ = 0.01 (verified in federated/simulation_fedprox.py and "
    "federated/strategy.py)."
))
story.append(p(
    "The proximal term penalises local updates that deviate excessively from the global model. "
    "This constrains the optimisation on non-IID clients, preventing divergence and improving "
    "the stability of the aggregated global model."
))
story.append(p(
    "The proximal penalty is computed in the client's fit() method (federated/client.py, "
    "lines 182–196) by summing the squared L2 norm of the difference between each local "
    "parameter tensor and the corresponding global model parameter tensor. The server-side "
    "aggregation in FedProxStrategy.aggregate_fit() performs a standard weighted parameter "
    "average, identical to FedAvg."
))
story.append(make_table(
    ["Hyperparameter", "Value", "Source"],
    [
        ["Proximal μ",              "0.01",   "simulation_fedprox.py / strategy.py"],
        ["Communication rounds",    "30",     "simulation_fedprox.py"],
        ["Clients per round",       "5 (all)","strategy.py — fraction_fit=1.0"],
        ["Local epochs per round",  "5",      "simulation_fedprox.py"],
        ["Batch size",              "512",    "client.py"],
        ["Learning rate",           "0.001",  "client.py"],
        ["Optimiser",               "Adam",   "client.py"],
        ["Aggregation",             "Weighted parameter average", "flwr FedAvg base"],
        ["Random seed",             "42",     "config.py"],
    ],
    col_widths=[5*cm, 4*cm, 8*cm]
))
story.append(caption("Table 4: FedProx Experimental Configuration — verified from source files."))
story.append(sp(6))

story.append(h2("2.6 FedAvg Baseline"))
story.append(p(
    "FedAvg (McMahan et al., 2017) is implemented as FedAvgStrategy in federated/strategy.py "
    "by subclassing Flower's built-in FedAvg strategy. The FedAvg simulation "
    "(federated/simulation.py) uses the same FraudDNN architecture and the same five-client "
    "partition but sets proximal_mu = 0.0 (no proximal penalty) and was run for 5 communication "
    "rounds. The aggregation is a weighted parameter average proportional to local sample counts. "
    "The shorter training schedule and absence of proximal regularisation contribute to the "
    "substantially lower test-set performance observed."
))

story.append(h2("2.7 Model Evaluation and Threshold Selection"))
story.append(p(
    "Threshold selection uses the validation set exclusively (88,581 samples), scanning "
    "candidate thresholds from 0.05 to 0.95 in steps of 0.05 and selecting the threshold "
    "that maximises the fraud-class F1-score. This procedure is implemented in "
    "federated/evaluate_fedprox.py and scripts/regenerate_all_figures.py. The selected "
    "threshold is then applied to the held-out test set for final metric computation. "
    "This protocol prevents threshold selection from contaminating the test-set evaluation."
))
story.append(p(
    "The following metrics are reported on the test set (88,581 transactions, 3,083 fraud):"
))
for metric, note in [
    ("ROC-AUC", "Area under the receiver operating characteristic curve. Threshold-independent. Measures the model's ability to rank fraudulent transactions above legitimate ones."),
    ("PR-AUC (Average Precision)", "Area under the precision-recall curve. More informative than ROC-AUC under severe class imbalance, as it focuses on the minority (fraud) class."),
    ("Precision", "Of all transactions flagged as fraud, the fraction that are genuinely fraudulent. High precision reduces false alarms for analysts."),
    ("Recall", "Of all genuinely fraudulent transactions, the fraction correctly flagged. High recall reduces missed fraud."),
    ("F1-score", "Harmonic mean of precision and recall. Provides a single balanced measure for the fraud class."),
    ("Accuracy", "Overall classification accuracy. Can be misleading under severe class imbalance (a model flagging nothing as fraud achieves ~96.5% accuracy)."),
    ("Confusion matrix", "Reports TP, FP, FN, and TN counts, providing the complete picture of classification outcomes."),
]:
    story.append(bull(f"<b>{metric}:</b> {note}"))
story.append(sp(4))

story.append(h2("2.8 Explainability Using SHAP"))
story.append(p(
    "SHAP (SHapley Additive exPlanations) decomposes each model prediction into additive "
    "feature contributions. For neural networks, the SHAP GradientExplainer back-propagates "
    "expected gradients from a background dataset to attribute the model output to each input feature."
))
story.append(p(
    "Implementation (scripts/regenerate_all_figures.py and backend/services/model_service.py):"
))
for item in [
    "<b>Explainer type:</b> shap.GradientExplainer applied to the FedProx DNN.",
    "<b>Background dataset (offline analysis):</b> 100 randomly selected test-set samples (random seed 42).",
    "<b>Explanation sample (offline analysis):</b> 50 randomly selected test-set samples.",
    "<b>Background dataset (backend inference):</b> 30 randomly selected training-set samples.",
    "<b>Feature importance aggregation:</b> mean absolute SHAP value across all explanation samples.",
    "<b>Output:</b> Per-feature attribution scores for offline importance ranking; top-5 feature attributions returned per transaction in the API response.",
]:
    story.append(bull(item))
story.append(p(
    "SHAP importance indicates which features most strongly influence the model's logit output "
    "in this dataset. It does not imply causal relationships between features and fraud."
))

story.append(h2("2.9 Frontend and Backend Implementation"))
story.append(p(
    "The Flask application (backend/app.py) is the entry point. FraudModelService loads the "
    "FedProx DNN checkpoint, the StandardScaler, the training medians, and the category "
    "mappings from the models/ directory once at startup. Incoming POST requests to /api/predict "
    "pass the uploaded CSV to FraudModelService.predict_dataframe(), which preprocesses each "
    "row, runs batch DNN inference, applies the 0.85 threshold, assigns risk levels, optionally "
    "computes SHAP attributions, and returns a structured JSON response."
))
story.append(p(
    "The React frontend (frontend/src/App.jsx) manages application state (selected file, "
    "analysis results, model metadata, navigation, backend health) and dispatches them to "
    "child components: FileUploadSection, AnalysisSummary, VisualSummary, TransactionTable, "
    "FraudAlertsView, and TransactionDetailsDrawer. All API calls are made using the browser "
    "Fetch API to http://localhost:5000."
))

story.append(h2("2.10 Reproducibility and Execution"))
story.append(p("To reproduce the training and evaluation pipeline on Windows:"))
story.append(code(
    "# 1. Clone the repository\n"
    "git clone https://github.com/don8891/Online_payment_fraud_detection.git\n"
    "cd Online_payment_fraud_detection\n\n"
    "# 2. Create and activate virtual environment\n"
    "python -m venv .venv\n"
    ".venv\\Scripts\\activate\n\n"
    "# 3. Install dependencies (backend)\n"
    ".venv\\Scripts\\pip install -r backend/requirements.txt\n\n"
    "# 4. (Prerequisite) Ensure preprocessed data and model artefacts exist in:\n"
    "#    data/processed/  and  models/\n\n"
    "# 5. Run FedProx federated simulation (30 rounds)\n"
    ".venv\\Scripts\\python -m federated.simulation_fedprox\n\n"
    "# 6. Evaluate FedProx global model on test set\n"
    ".venv\\Scripts\\python -m federated.evaluate_fedprox\n\n"
    "# 7. Regenerate all research figures\n"
    ".venv\\Scripts\\python scripts/regenerate_all_figures.py\n\n"
    "# 8. Start Flask backend\n"
    ".venv\\Scripts\\python -m backend.app\n\n"
    "# 9. Start React frontend (separate terminal)\n"
    "cd frontend && npm install && npm run dev"
))
story.append(pb())

# ─── SECTION 3: RESULTS AND DISCUSSION ────────────────────────
story.append(h1("3. RESULTS AND DISCUSSION"))
story.append(hr())

story.append(h2("3.1 Experimental Configuration Summary"))
story.append(make_table(
    ["Parameter", "FedProx", "FedAvg"],
    [
        ["DNN Architecture",    "421→256→128→64→1",  "421→256→128→64→1"],
        ["Optimizer",           "Adam (lr=0.001)",    "Adam (lr=0.001)"],
        ["Loss Function",       "BCEWithLogitsLoss + pos_weight", "BCEWithLogitsLoss + pos_weight"],
        ["Communication Rounds","30",                 "5"],
        ["Local Epochs / Round","5",                  "1 (default)"],
        ["Batch Size",          "512",                "512"],
        ["Proximal μ",          "0.01",               "0.00 (no penalty)"],
        ["Clients",             "5 (all per round)",  "5 (all per round)"],
        ["Threshold",           "0.85 (val F1 max)",  "0.05 (val F1 max)"],
        ["Framework",           "Flower (flwr)",       "Flower (flwr)"],
    ],
    col_widths=[6*cm, 5*cm, 6*cm]
))
story.append(caption("Table 5: Experimental Configuration — verified from source code."))
story.append(sp(8))

story.append(h2("3.2 FedProx vs. FedAvg Performance Comparison"))
story.append(p(
    "Table 6 presents the complete test-set evaluation results. All metrics are computed on "
    "the held-out IEEE-CIS test set (88,581 transactions, 3,083 fraudulent, 85,498 legitimate). "
    "Thresholds were selected on the validation set by maximising the fraud-class F1-score."
))
story.append(make_table(
    ["Metric", "FedProx DNN", "FedAvg DNN", "Difference"],
    [
        ["ROC-AUC",              "0.8004", "0.4980", "+0.3024 (FedProx better)"],
        ["PR-AUC",               "0.2120", "0.0347", "+0.1773 (FedProx better)"],
        ["Fraud-class F1-score", "0.3751", "0.0673", "+0.3078 (FedProx better)"],
        ["Fraud-class Precision","0.3445", "0.0348", "+0.3097 (FedProx better)"],
        ["Fraud-class Recall",   "0.4116", "1.0000", "−0.5884 (FedAvg higher recall)"],
        ["Overall Accuracy",     "95.23%", "~9.64%*", "FedProx substantially better"],
        ["Decision Threshold",   "0.85",   "0.05",   "—"],
    ],
    col_widths=[5*cm, 3.5*cm, 3.5*cm, 5*cm]
))
story.append(Paragraph(
    "* FedAvg flags nearly all transactions as fraud at threshold 0.05, yielding a very low accuracy. "
    "Accuracy is reported as ~9.64% because ≈85,480 legitimate transactions are falsely flagged.",
    ST['SectionNote']))
story.append(caption("Table 6: FedProx vs. FedAvg Performance on IEEE-CIS Test Set."))
story.append(sp(8))

story.append(h2("3.3 Confusion Matrix Analysis"))
story.append(p(
    "Confusion matrix counts are derived from the classification report values. "
    "For FedProx: actual fraud = 3,083, actual legitimate = 85,498."
))
story.append(make_table(
    ["Model", "True Positive (TP)", "False Negative (FN)", "False Positive (FP)", "True Negative (TN)"],
    [
        ["FedProx DNN", "≈1,269", "≈1,814", "≈2,414", "≈83,084"],
        ["FedAvg DNN",  "3,083",  "0",       "≈85,480", "≈18"],
    ],
    col_widths=[4*cm, 3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm]
))
story.append(Paragraph(
    "TP/FN/FP/TN derived from: TP = Recall × actual_fraud; FP = TP / Precision − TP; "
    "FN = actual_fraud − TP; TN = actual_legit − FP. "
    "FedAvg recall=1.0 means zero fraud missed, but 85,480 legitimate transactions are incorrectly flagged.",
    ST['SectionNote']))
story.append(caption("Table 7: Confusion Matrix Counts for Both Models."))
story.append(sp(8))

story.append(h2("3.4 Confusion Matrix Figures"))
story.append(p(
    "Figures 6 and 7 show the confusion matrices for FedProx DNN and FedAvg DNN respectively, "
    "generated from actual model predictions on the test set."
))

# Side by side confusion matrices
cm_table = Table(
    [[rl_img(FIG6, width=7.2*cm), rl_img(FIG7, width=7.2*cm)]],
    colWidths=[8*cm, 8*cm]
)
cm_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(cm_table)
story.append(caption(
    "Figure 6 (left): FedProx DNN Confusion Matrix (threshold ≥ 0.85) — "
    "1,269 TP, 1,814 FN, 2,414 FP, 83,084 TN.\n"
    "Figure 7 (right): FedAvg DNN Confusion Matrix (threshold ≥ 0.05) — "
    "all fraud detected but ~85,480 legitimate transactions falsely flagged."))
story.append(sp(10))

story.append(h2("3.5 ROC Curve Analysis"))
story += fig_img(FIG8, width=13*cm,
    caption_text="Figure 8: ROC Curve — FedProx DNN (AUC=0.8004) substantially outperforms FedAvg DNN (AUC=0.4980), which is near the random-baseline diagonal.")
story.append(p(
    "The FedProx model achieves an ROC-AUC of 0.8004, indicating a strong ability to rank "
    "fraudulent transactions above legitimate ones across all possible thresholds. The FedAvg "
    "model's ROC-AUC of 0.4980 is below the random-classifier baseline (0.50), indicating "
    "that the FedAvg global model has not converged to a useful classifier under 5 communication "
    "rounds with non-IID data and no proximal regularisation. This result underscores the "
    "importance of FedProx for non-IID federated settings."
))

story.append(h2("3.6 Precision-Recall Curve Analysis"))
story += fig_img(FIG9, width=13*cm,
    caption_text="Figure 9: Precision-Recall Curve — FedProx DNN (AP=0.2120) is substantially above the random baseline (AP≈0.0348). FedAvg DNN collapses near the baseline.")
story.append(p(
    "The PR-AUC (average precision) for FedProx is 0.2120, more than six times the random "
    "baseline of 0.0348 (the dataset fraud rate). This is a meaningful result for highly "
    "imbalanced fraud detection, where PR-AUC is a more informative measure than ROC-AUC. "
    "However, the absolute value of 0.2120 also indicates that identifying high-confidence "
    "fraud across the full recall range remains challenging. The FedAvg curve degenerates near "
    "the random baseline, confirming the failure to converge."
))

story.append(h2("3.7 Model Performance Comparison"))
story += fig_img(FIG10, width=14*cm,
    caption_text="Figure 10: Performance Comparison Bar Chart — FedProx DNN outperforms FedAvg DNN on all threshold-independent and threshold-dependent metrics except recall.")
story.append(p(
    "FedProx outperforms FedAvg on every metric except fraud-class recall. The FedAvg model's "
    "recall of 1.0 (it flags every transaction as fraud at threshold 0.05) comes at the cost "
    "of precision of 0.0348 — meaning only 3.48% of its flagged transactions are genuinely "
    "fraudulent, effectively rendering its alerts meaningless in practice."
))

story.append(h2("3.8 Threshold Comparison"))
story.append(make_table(
    ["Model", "Threshold", "Selection Criterion", "Val F1", "Test Precision", "Test Recall", "Test F1"],
    [
        ["FedProx DNN", "0.85", "Maximise val fraud-class F1", "0.4615", "0.3445", "0.4116", "0.3751"],
        ["FedAvg DNN",  "0.05", "Maximise val fraud-class F1", "0.0664", "0.0348", "1.0000", "0.0673"],
    ],
    col_widths=[3.5*cm, 2.5*cm, 5*cm, 2.5*cm, 3*cm, 2.5*cm, 2.5*cm]
))
story.append(caption("Table 8: Threshold Comparison — both thresholds selected by validation F1 maximisation."))
story.append(sp(8))
story.append(p(
    "The optimal threshold of 0.85 for FedProx reflects the model's calibration: meaningful "
    "fraud signals only emerge at high probability values. This is consistent with the severe "
    "class imbalance and suggests the model is conservative in its fraud assignments. "
    "The very low FedAvg threshold of 0.05 indicates the model assigns only marginally elevated "
    "probabilities to fraudulent transactions, confirming poor discriminative ability."
))

story.append(h2("3.9 SHAP Feature Importance"))
story += fig_img(FIG11, width=14*cm,
    caption_text="Figure 11: Top 20 FedProx DNN SHAP Features — mean absolute SHAP value (logit) computed with GradientExplainer on 50 test-set transactions against 100 background samples.")
story.append(make_table(
    ["Rank", "Feature", "Mean |SHAP| Value", "Feature Category"],
    [
        ["1",  "V95",          "0.7123", "Engineered Vesta feature"],
        ["2",  "DeviceType",   "0.5578", "Device/identity information"],
        ["3",  "V11",          "0.5509", "Engineered Vesta feature"],
        ["4",  "V285",         "0.4901", "Engineered Vesta feature"],
        ["5",  "V97",          "0.4798", "Engineered Vesta feature"],
        ["6",  "TransactionAmt","0.4756","Transaction attribute"],
        ["7",  "card5",        "0.4538", "Card metadata"],
        ["8",  "V100",         "0.4231", "Engineered Vesta feature"],
        ["9",  "id_38",        "0.4183", "Identity feature"],
        ["10", "V101",         "0.3811", "Engineered Vesta feature"],
    ],
    col_widths=[2*cm, 4*cm, 4*cm, 7*cm]
))
story.append(caption("Table 9: Top 10 SHAP Feature Importances — from reports/figures/fedprox_shap_feature_importance.csv."))
story.append(sp(8))
story.append(p(
    "The engineered Vesta V-features (V95, V11, V285, V97, V100, V101) dominate the top-10 "
    "importance list, consistent with their role as transaction behaviour fingerprints in the "
    "IEEE-CIS dataset. DeviceType (rank 2) and id_38 (rank 9) indicate that device and identity "
    "attributes carry significant discriminative signal. TransactionAmt (rank 6) confirms that "
    "transaction value contributes meaningfully to fraud probability, as is expected in online "
    "payment fraud. SHAP importance measures input-output sensitivity; it does not imply "
    "that a high V95 value directly causes fraud."
))

story.append(h2("3.10 Discussion of Results"))
story.append(p(
    "<b>FedProx vs. FedAvg:</b> The results clearly demonstrate FedProx's superiority over "
    "FedAvg under non-IID federated conditions. FedProx achieves ROC-AUC = 0.8004 versus "
    "FedAvg's 0.4980 — a difference of 0.3024 — and PR-AUC = 0.2120 versus 0.0347. The "
    "proximal regularisation term effectively prevents client models from diverging too far "
    "from the global model during local training on heterogeneous data."
))
story.append(p(
    "<b>Fraud Recall Limitation:</b> FedProx's recall of 41.16% means it misses approximately "
    "58.84% of fraudulent transactions at the threshold of 0.85. In a real fraud detection "
    "system, this high false-negative rate would allow a substantial proportion of fraudulent "
    "transactions to pass undetected. The conservative threshold reflects the model's current "
    "calibration but suggests that further training, stronger class-imbalance techniques "
    "(e.g., oversampling within each client), or a lower deployment threshold (with acceptable "
    "precision trade-off) should be explored."
))
story.append(p(
    "<b>FedAvg's Perfect Recall:</b> FedAvg achieves recall = 1.0 because its optimal "
    "threshold of 0.05 effectively classifies all transactions as fraud. This trivially catches "
    "all fraud but produces precision = 0.0348, meaning 96.52% of flagged transactions are "
    "false alarms. Such a system would be unusable in practice due to alert fatigue."
))
story.append(p(
    "<b>Class Imbalance:</b> The 3.48% fraud rate creates a challenging learning environment. "
    "The class-weighted BCEWithLogitsLoss helps prevent the model from defaulting to predicting "
    "all-legitimate, but additional techniques such as oversampling (SMOTE), undersampling, or "
    "focal loss may improve the recall-precision balance in future iterations."
))
story.append(p(
    "<b>Accuracy Caveat:</b> FedProx's overall accuracy of 95.23% is primarily driven by "
    "correct classification of the majority (legitimate) class. A naïve baseline that never "
    "flags fraud would achieve approximately 96.5% accuracy. Overall accuracy is therefore a "
    "poor performance indicator for this imbalanced dataset; ROC-AUC and PR-AUC are more "
    "meaningful."
))

story.append(h2("3.11 Limitations"))
for lim in [
    "Client simulation uses static non-IID partitions of a single historical dataset, not a live multi-institutional deployment.",
    "FedAvg was trained for only 5 rounds versus 30 for FedProx; additional FedAvg rounds may improve its performance.",
    "The FedProx recall of 41.16% indicates that over half of all fraudulent transactions are missed at the 0.85 threshold.",
    "No differential privacy mechanism is applied; gradient inversion attacks remain theoretically possible.",
    "The model was evaluated on IEEE-CIS data from a specific time window; generalisation to other datasets or time periods is not verified.",
    "Computational requirements preclude large-scale hyperparameter search; learning rate, batch size, and proximal μ were not exhaustively tuned.",
    "SHAP values are computed on a small subset (50 samples) and may not be fully representative of the global feature importance distribution.",
]:
    story.append(bull(lim))
story.append(pb())

# ─── APPENDIX A: CORE ─────────────────────────────────────────
story.append(h1("APPENDIX A: CORE IMPLEMENTATION"))
story.append(hr())

story.append(h2("A.1 Project Directory Structure"))
story.append(code(
    "Online_payment_fraud_detection/\n"
    "├── backend/\n"
    "│   ├── app.py                     # Flask application entry point\n"
    "│   ├── config.py                  # Flask configuration\n"
    "│   ├── routes/                    # API route definitions\n"
    "│   ├── services/\n"
    "│   │   └── model_service.py       # FraudModelService — preprocessing + inference\n"
    "│   └── requirements.txt\n"
    "├── federated/\n"
    "│   ├── model.py                   # FraudDNN class definition\n"
    "│   ├── client.py                  # FraudClient — local FedProx/FedAvg training\n"
    "│   ├── strategy.py                # FedProxStrategy, FedAvgStrategy (Flower)\n"
    "│   ├── simulation_fedprox.py      # FedProx simulation entry point (30 rounds)\n"
    "│   ├── simulation.py              # FedAvg simulation entry point (5 rounds)\n"
    "│   ├── server.py                  # Server utilities\n"
    "│   ├── config.py                  # Federated learning hyperparameters\n"
    "│   ├── evaluate_fedprox.py        # FedProx evaluation on test set\n"
    "│   ├── evaluate_fedavg.py         # FedAvg evaluation on test set\n"
    "│   └── data/\n"
    "│       ├── client_0/ … client_4/  # Per-bank X.pkl, y.pkl (pre-scaled)\n"
    "├── frontend/src/\n"
    "│   ├── App.jsx                    # Root component, state management, API calls\n"
    "│   ├── components/\n"
    "│   │   ├── Sidebar.jsx            # Navigation sidebar\n"
    "│   │   ├── Header.jsx             # Top header with status\n"
    "│   │   ├── FileUploadSection.jsx  # CSV upload and analysis trigger\n"
    "│   │   ├── AnalysisSummary.jsx    # 4 KPI metric cards\n"
    "│   │   ├── VisualSummary.jsx      # Charts (fraud distribution, risk breakdown)\n"
    "│   │   ├── TransactionTable.jsx   # Searchable, filterable ledger\n"
    "│   │   ├── FraudAlertsView.jsx    # High-risk transaction alerts list\n"
    "│   │   └── TransactionDetailsDrawer.jsx  # Per-transaction SHAP drawer\n"
    "├── models/\n"
    "│   ├── fedprox_global_dnn.pth     # FedProx trained DNN weights (600 KB)\n"
    "│   ├── fedavg_global_dnn.pth      # FedAvg trained DNN weights (600 KB)\n"
    "│   ├── fedprox_scaler.pkl         # StandardScaler (421 features)\n"
    "│   ├── fedprox_train_medians.pkl  # Per-feature training medians\n"
    "│   ├── fedprox_category_mappings.pkl  # 29 categorical column encoders\n"
    "│   └── feature_info.pkl           # Feature name list and metadata\n"
    "├── data/\n"
    "│   ├── processed/                 # X_train_dnn.pkl, X_val_dnn.pkl, X_test_dnn.pkl, y_*.pkl\n"
    "│   └── sample_transactions.csv    # Sample IEEE-CIS-format CSV for dashboard testing\n"
    "├── notebooks/\n"
    "│   ├── 02_data_preprocessing.ipynb\n"
    "│   ├── 03_model_training.ipynb\n"
    "│   └── 04_dnn_baseline.ipynb\n"
    "├── scripts/\n"
    "│   ├── regenerate_all_figures.py  # Regenerates all 7 research figures\n"
    "│   └── explain_fedprox.py         # Standalone SHAP analysis script\n"
    "└── reports/figures/               # Generated PNG research figures"
))

story.append(h2("A.2 FraudDNN Model Definition"))
story.append(p("File: federated/model.py — verified 30-line implementation:"))
story.append(code(
    "class FraudDNN(nn.Module):\n"
    "    def __init__(self, input_size=421):\n"
    "        super(FraudDNN, self).__init__()\n"
    "        self.network = nn.Sequential(\n"
    "            nn.Linear(input_size, 256),\n"
    "            nn.ReLU(),\n"
    "            nn.Dropout(0.3),\n"
    "            nn.Linear(256, 128),\n"
    "            nn.ReLU(),\n"
    "            nn.Dropout(0.3),\n"
    "            nn.Linear(128, 64),\n"
    "            nn.ReLU(),\n"
    "            nn.Dropout(0.2),\n"
    "            nn.Linear(64, 1)\n"
    "        )\n"
    "    def forward(self, x):\n"
    "        return self.network(x)"
))

story.append(h2("A.3 FedProx Local Training Loop (Key Excerpt)"))
story.append(p("File: federated/client.py — proximal loss computation (lines 182–196):"))
story.append(code(
    "# Apply proximal penalty only for FedProx (mu > 0)\n"
    "if proximal_mu > 0.0:\n"
    "    proximal_loss = torch.zeros(())\n"
    "    for local_param, global_param in zip(\n"
    "        self.model.parameters(),\n"
    "        global_model.parameters()\n"
    "    ):\n"
    "        proximal_loss += torch.sum(\n"
    "            (local_param - global_param) ** 2\n"
    "        )\n"
    "    loss = classification_loss + (proximal_mu / 2.0) * proximal_loss\n"
    "else:\n"
    "    loss = classification_loss  # Standard FedAvg"
))

story.append(h2("A.4 FedProx Strategy Configuration"))
story.append(p("File: federated/simulation_fedprox.py — hyperparameter configuration:"))
story.append(code(
    "NUM_CLIENTS  = 5\n"
    "NUM_ROUNDS   = 30\n"
    "PROXIMAL_MU  = 0.01\n"
    "LOCAL_EPOCHS = 5\n\n"
    "strategy = FedProxStrategy(\n"
    "    proximal_mu=PROXIMAL_MU,\n"
    "    local_epochs=LOCAL_EPOCHS,\n"
    "    fraction_fit=1.0,\n"
    "    fraction_evaluate=1.0,\n"
    "    min_fit_clients=NUM_CLIENTS,\n"
    "    min_available_clients=NUM_CLIENTS,\n"
    ")"
))

story.append(h2("A.5 Flask API Predict Endpoint"))
story.append(p("File: backend/app.py — POST /api/predict:"))
story.append(code(
    "@app.route('/api/predict', methods=['POST'])\n"
    "def predict():\n"
    "    file = request.files['file']\n"
    "    df = pd.read_csv(file)\n"
    "    results = fraud_model.predict_dataframe(df)\n"
    "    return jsonify(results), 200"
))

story.append(h2("A.6 Preprocessing Pipeline (Key Excerpt)"))
story.append(p("File: backend/services/model_service.py — preprocess_dataframe():"))
story.append(code(
    "# 1. Category encoding (29 columns)\n"
    "for col, mapping in self.category_mappings.items():\n"
    "    X[col] = X[col].map(lambda v: mapping.get(v, -1) if pd.notna(v) else -1)\n\n"
    "# 2. Median imputation\n"
    "X = X.fillna(self.medians).fillna(0)\n\n"
    "# 3. StandardScaler\n"
    "scaled = self.scaler.transform(X[self.feature_names])\n"
    "return np.asarray(scaled, dtype=np.float32)"
))

story.append(h2("A.7 Key Commands Summary"))
story.append(make_table(
    ["Task", "Command"],
    [
        ["Run FedProx training",      ".venv\\Scripts\\python -m federated.simulation_fedprox"],
        ["Run FedAvg training",       ".venv\\Scripts\\python -m federated.simulation"],
        ["Evaluate FedProx",          ".venv\\Scripts\\python -m federated.evaluate_fedprox"],
        ["Evaluate FedAvg",           ".venv\\Scripts\\python -m federated.evaluate_fedavg"],
        ["Regenerate all figures",    ".venv\\Scripts\\python scripts/regenerate_all_figures.py"],
        ["Start Flask backend",       ".venv\\Scripts\\python -m backend.app"],
        ["Start React frontend",      "cd frontend && npm run dev"],
        ["Install backend deps",      ".venv\\Scripts\\pip install -r backend/requirements.txt"],
    ],
    col_widths=[6*cm, 11*cm]
))
story.append(pb())

# ─── APPENDIX B: SCREENSHOTS ─────────────────────────────────
story.append(h1("APPENDIX B: SCREENSHOTS"))
story.append(hr())
story.append(p(
    "This appendix is reserved for dashboard screenshots and demo recordings. "
    "The following placeholders describe the expected screenshot locations. "
    "Screenshots should be captured from the live running application at http://localhost:5173 "
    "with the Flask backend active at http://localhost:5000."
))
story.append(sp(8))

screenshots = [
    ("B.1", "Dashboard Overview — Home Tab",
     "Shows the FraudGuard AI sidebar, file upload section, KPI summary cards (total transactions, "
     "fraud count, legitimate count, fraud rate), and the backend connection indicator."),
    ("B.2", "CSV Upload and Analysis in Progress",
     "Capture the upload modal after selecting a CSV file, showing the estimated row count, "
     "file name, and the 'Analyse Batch' button in its active state with the loading animation."),
    ("B.3", "Post-Analysis Overview — Charts and Preview Table",
     "After analysis completes: VisualSummary charts (risk distribution, fraud probability histogram), "
     "and the 6-row evaluated batch preview table with fraud probability, risk level, and inspect buttons."),
    ("B.4", "Transaction Analysis Ledger",
     "Full TransactionTable with search, filter by risk level, sort by fraud probability, and "
     "pagination. Show at least one HIGH-risk transaction highlighted in red."),
    ("B.5", "Fraud Alerts Tab",
     "FraudAlertsView showing the alert header (count of flagged transactions), analyst advisory "
     "disclaimer, and the list of fraud-flagged transaction cards sorted by probability."),
    ("B.6", "Transaction Details Drawer",
     "TransactionDetailsDrawer opened for a single transaction: fraud probability bar, risk badge, "
     "raw feature values, and SHAP top-5 feature attributions with direction indicators."),
]
for code_id, title, desc in screenshots:
    story.append(h3(f"{code_id}: {title}"))
    story.append(p(desc))
    # Placeholder box
    placeholder = Table(
        [[Paragraph(f"[ Screenshot Placeholder: {title} ]",
            ParagraphStyle('PH', fontSize=10, alignment=TA_CENTER,
                textColor=DGREY, fontName='Helvetica-Oblique'))]],
        colWidths=[15*cm], rowHeights=[5*cm]
    )
    placeholder.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, MGREY),
        ('BACKGROUND', (0,0), (-1,-1), LGREY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(placeholder)
    story.append(sp(10))

story.append(pb())

# ─── APPENDIX C: TECH STACK ───────────────────────────────────
story.append(h1("APPENDIX C: CORE TECHNOLOGY STACK"))
story.append(hr())

story.append(make_table(
    ["Technology / Component", "Purpose in the Project", "Actual Usage"],
    [
        ["Python 3.x",           "Primary language",
         "All backend, ML, federated learning, and scripting code"],
        ["PyTorch",              "Deep learning framework",
         "FraudDNN definition, training, and inference; BCEWithLogitsLoss; Adam optimiser"],
        ["Flower (flwr)",        "Federated learning orchestration",
         "FedAvgStrategy, FedProxStrategy, client simulation, parameter aggregation"],
        ["Flask",                "REST API backend",
         "3 endpoints: /api/health, /api/sample-csv, /api/predict"],
        ["Flask-CORS",           "Cross-origin requests",
         "Allows React (port 5173) to call Flask (port 5000)"],
        ["scikit-learn",         "Preprocessing + metrics",
         "StandardScaler, confusion_matrix, roc_auc_score, f1_score, classification_report"],
        ["Pandas",               "Data handling",
         "DataFrame operations, CSV I/O, pickle serialisation"],
        ["NumPy",                "Numerical computation",
         "Array operations, threshold scanning, metric computation"],
        ["SHAP",                 "Explainability",
         "GradientExplainer for per-transaction feature attributions and global importance"],
        ["Matplotlib",           "Visualisation",
         "ROC curves, PR curves, confusion matrices, SHAP bar chart, comparison bar chart"],
        ["Joblib",               "Artefact serialisation",
         "Save/load StandardScaler, medians, category mappings"],
        ["React (Vite)",         "Frontend SPA framework",
         "Dashboard UI with 3 tabs: Overview, Transaction Analysis, Fraud Alerts"],
        ["Tailwind CSS v4",      "Frontend styling",
         "All dashboard component styling, responsive layout"],
        ["IEEE-CIS Dataset",     "Training/evaluation data",
         "590,540 transactions (413k train, 88k val, 88k test); 421 features; 3.5% fraud"],
        ["FedProx algorithm",    "Principal FL optimiser",
         "Proximal regularisation (μ=0.01) applied in client training loop"],
        ["FedAvg algorithm",     "Comparison FL baseline",
         "Standard parameter averaging; no proximal term"],
        ["Git / GitHub",         "Version control",
         "Repository: github.com/don8891/Online_payment_fraud_detection"],
        ["Jupyter Notebooks",    "Preprocessing and EDA",
         "04_dnn_baseline.ipynb generates client partitions and preprocessing artefacts"],
    ],
    col_widths=[4.5*cm, 5.5*cm, 7*cm]
))
story.append(caption("Table 10: Core Technology Stack — all entries verified from source files, requirements, and package imports."))

# ═══════════════════════════════════════════════════════════════
# BUILD PDF
# ═══════════════════════════════════════════════════════════════
print(f"\nBuilding PDF -> {OUT_PDF}")

doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=A4,
    leftMargin=2.0*cm, rightMargin=2.0*cm,
    topMargin=2.5*cm,  bottomMargin=2.0*cm,
    title="Online Payment Fraud Detection — System Design, Methodology & Results",
    author="B.Tech CSE Final Year Project",
)

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
print(f"\n✓ PDF generated successfully: {OUT_PDF}")
print(f"  File size: {OUT_PDF.stat().st_size:,} bytes ({OUT_PDF.stat().st_size/1024/1024:.2f} MB)")

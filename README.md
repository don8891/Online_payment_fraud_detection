# Online Payment Fraud Detection System Using Machine Learning

A scalable, end-to-end framework designed for high-precision online payment fraud detection, integrating Centralized Machine Learning, Federated Learning, and SHAP Explainability into a modern web platform.

---

## 📌 Project Overview & Description

Online payment fraud poses a critical financial risk to e-commerce merchants, financial institutions, and payment processors worldwide. Traditional rule-based fraud detection systems often struggle with rapidly evolving transaction patterns and high false-positive rates.

This project establishes an advanced Machine Learning framework designed to process high-dimensional transaction data, accurately classify fraudulent behavior, maintain data privacy through Federated Learning principles, explain decision outputs using SHAP (SHapley Additive exPlanations), and expose interactive interfaces via a RESTful API backend and modern React dashboard.

---

## 🎯 Project Objectives

- **High Precision Fraud Detection:** Build robust classification models capable of handling severe class imbalance in payment transaction data.
- **Privacy-Preserving Architecture:** Implement Federated Learning prototypes to demonstrate privacy-centric multi-institution model training without centralizing sensitive customer records.
- **Model Explainability (XAI):** Leverage SHAP feature importance analysis to provide interpretable explanations for risk predictions.
- **Modular Enterprise Backend:** Develop a RESTful Flask API serving transaction scoring endpoints.
- **Interactive UI Dashboard:** Construct an intuitive React dashboard for real-time risk visualization and transaction inspection.

---

## 🚀 Current Development Phase

> **CURRENT STATUS: PHASE 1 — PROJECT FOUNDATION**
>
> The project structure, configuration baseline, backend health API foundation, and initial frontend shell have been initialized. Machine Learning models, dataset preprocessing pipelines, Federated Learning protocols, SHAP explainability engines, and complex UI dashboards **have not yet been implemented** and will be built sequentially in upcoming phases.

---

## 🛠️ Technology Stack

| Layer | Planned Technologies |
| :--- | :--- |
| **Backend** | Python, Flask, Flask-CORS, REST API |
| **Frontend** | React, Vite, Axios, React Router, Recharts / Chart.js |
| **Machine Learning** | PyTorch / TensorFlow, scikit-learn, XGBoost / LightGBM, Imbalanced-learn (SMOTE) |
| **Federated Learning** | Flower framework / Custom FL Simulator |
| **Explainability (XAI)** | SHAP (SHapley Additive exPlanations) |
| **Data Processing** | Pandas, NumPy, Joblib |

---

## 🏗️ Planned Architecture

```text
  [ User / Client ]
          │
          ▼
  [ React + Vite Frontend ]
          │ (HTTP / REST JSON)
          ▼
  [ Flask Backend REST API ]
          │
    ┌─────┴──────────────────┬────────────────────┐
    ▼                        ▼                    ▼
[ Centralized ML ]   [ Federated Learning ]   [ SHAP Engine ]
(XGBoost / Random    (Flower / Multi-node     (Feature Risk
    Forest)               Clients)            Explanations)
    └─────┬──────────────────┴────────────────────┘
          ▼
  [ IEEE-CIS Payment Dataset / Preprocessed Pipeline ]
```

---

## 📂 Project Structure

```text
Online_payment_fraud_detection/
├── backend/
│   ├── routes/          # REST API routes and endpoints
│   ├── services/        # Business logic and ML inference wrappers
│   ├── models/          # Backend ORM / Data structures
│   ├── schemas/         # Request validation and serialization schemas
│   ├── utils/           # Helper functions and logger utilities
│   ├── app.py           # Flask entry point (Health API initialized)
│   ├── config.py        # Environment and app configuration
│   └── requirements.txt # Initial backend dependencies
│
├── frontend/            # Basic React + Vite application shell
│
├── ml/
│   ├── data/            # Dataset loading & ingestion utilities
│   ├── preprocessing/   # Cleaning, scaling, & encoding modules
│   ├── features/        # Feature engineering & selection logic
│   ├── centralized/     # Standard ML models (XGBoost, Random Forest, etc.)
│   ├── federated/       # Federated Learning client/server scripts
│   ├── explainability/  # SHAP interpretability calculations
│   ├── evaluation/      # Metrics calculation (ROC-AUC, Precision-Recall)
│   └── inference/       # Pipeline packaging for live inference
│
├── data/
│   ├── raw/             # Original raw IEEE-CIS dataset (Git-ignored)
│   ├── interim/         # Intermediate transformed data files (Git-ignored)
│   ├── processed/       # Cleaned feature sets ready for training (Git-ignored)
│   └── artifacts/       # Scalers, encoders, and serialized metadata (Git-ignored)
│
├── models/              # Serialized ML model binaries (.pkl, .pt) (Git-ignored)
├── notebooks/           # Exploratory Data Analysis & experimental notebooks
├── reports/             # Generated metric charts, confusion matrices, & logs
├── tests/               # Unit tests for backend APIs and ML utilities
├── scripts/             # Utility scripts for setup and data management
├── docs/                # Project documentation and architectural diagrams
├── .gitignore           # Git ignore definitions
├── README.md            # Main project README documentation
└── LICENSE              # MIT License
```

---

## 📊 Dataset Information & Privacy Policy

The system will eventually utilize the benchmark **IEEE-CIS Fraud Detection Dataset** (comprising transaction and identity features).

> [!IMPORTANT]
> **Dataset Version Control Rule:**
> Raw dataset files (`data/raw/`), interim data (`data/interim/`), processed datasets (`data/processed/`), heavy model artifacts (`models/`), and generated binary artifacts (`data/artifacts/`) **must NEVER be committed to Git or GitHub**.
> All data and model directories are explicitly excluded in `.gitignore`.

---

## 🗓️ Development Roadmap

- [x] **Phase 1: Project Foundation** — Folder structure, backend baseline, frontend shell, Git rules, & documentation.
- [ ] **Phase 2: Data Preprocessing & EDA** — IEEE-CIS ingestion, missing value imputation, feature engineering, and class imbalance handling (SMOTE).
- [ ] **Phase 3: Centralized ML Models** — Baseline training, hyperparameter optimization, and evaluation (XGBoost, Random Forest, Neural Networks).
- [ ] **Phase 4: Federated Learning & Explainability** — Privacy-preserving FL client-server simulation and SHAP explanation generation.
- [ ] **Phase 5: Backend & REST APIs** — Flask endpoints for live transaction scoring, explanation retrieval, and model management.
- [ ] **Phase 6: Frontend Dashboard & Integration** — Interactive React dashboard with transaction analysis, charts, and live inference visualization.

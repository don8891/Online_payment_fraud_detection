# FedAvg 30R vs FedProx – Model Comparison Report

> Generated on run of `scripts/evaluate_fedavg_30r.py`

## Evaluation Protocol

- **Validation set**: used only to select the decision threshold (max-F1 sweep 0.05 → 0.95).
- **Test set**: used only for final metric reporting.
- **ROC-AUC** and **PR-AUC** are computed from continuous probability scores, not thresholded predictions.
- Both models share identical preprocessing, feature order, and data splits.
- No target accuracy / AUC was guaranteed or manipulated.

## Metric Comparison

| Metric | FedAvg (30 rounds) | FedProx (30 rounds) |
|--------|-------------|-------------|
| ROC-AUC | 0.8101 | 0.8004 |
| PR-AUC | 0.3225 | 0.2120 |
| Accuracy | 0.9629 | 0.9553 |
| Fraud Precision | 0.4590 | 0.3648 |
| Fraud Recall | 0.3763 | 0.3834 |
| Fraud F1-score | 0.4135 | 0.3739 |
| Val Threshold | 0.89 | 0.89 |

## Confusion Matrices

### FedAvg (30 rounds)  (threshold = 0.89)

| | Pred Legit | Pred Fraud |
|---|---|---|
| **True Legit** | 84,131 | 1,367 |
| **True Fraud** | 1,923 | 1,160 |

### FedProx (30 rounds)  (threshold = 0.89)

| | Pred Legit | Pred Fraud |
|---|---|---|
| **True Legit** | 83,440 | 2,058 |
| **True Fraud** | 1,901 | 1,182 |

## Notes on Figures

- `reports/figures/roc_curve_30r_comparison.png` – overlaid ROC curves.
- `reports/figures/pr_curve_30r_comparison.png` – overlaid PR curves.
- `reports/figures/confusion_matrix_fedavg_30r.png` – FedAvg confusion matrix.
- `reports/figures/confusion_matrix_fedprox_30r.png` – FedProx confusion matrix.
- `reports/figures/fedavg_30r_training_loss.png` – per-round aggregated eval loss.

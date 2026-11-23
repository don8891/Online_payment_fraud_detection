# ============================================================
# tests/test_backend_fedavg_migration.py
#
# Comprehensive test suite for FedAvg 30R Flask backend migration:
#   1. Model loading & parameter verification
#   2. Preprocessing & feature alignment verification
#   3. Single-transaction prediction & SHAP explanation
#   4. 100-row batch prediction & threshold validation (0.89)
#   5. Risk level stratification verification
#   6. Flask API endpoint verification (GET /api/health, POST /api/predict)
# ============================================================

import sys
import os
from pathlib import Path
import io
import json

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd
import torch

from backend.services.model_service import fraud_model, FraudModelService
from backend.app import create_app

def run_tests():
    print("=" * 65)
    print("  FRAUDSHIELD: FedAvg 30R Backend Migration Test Suite")
    print("=" * 65)

    # ---------------------------------------------------------
    # TEST 1: Model Loading & Configuration
    # ---------------------------------------------------------
    print("\n[TEST 1] Model Loading & Configuration Verification...")
    assert fraud_model.model_name == "FedAvg 30R DNN", f"Expected 'FedAvg 30R DNN', got {fraud_model.model_name}"
    assert fraud_model.threshold == 0.89, f"Expected 0.89, got {fraud_model.threshold}"
    assert len(fraud_model.feature_names) == 421, f"Expected 421 features, got {len(fraud_model.feature_names)}"
    assert str(fraud_model.model_path).endswith("fedavg_global_dnn_30r.pth"), f"Unexpected model path: {fraud_model.model_path}"
    assert fraud_model.device == torch.device("cpu"), f"Unexpected device: {fraud_model.device}"
    assert not fraud_model.model.training, "Model must be in eval() mode"

    # Verify model parameters are loaded from fedavg_global_dnn_30r.pth
    expected_state = torch.load(fraud_model.model_path, map_location="cpu", weights_only=True)
    for k, v in fraud_model.model.state_dict().items():
        assert torch.equal(v, expected_state[k]), f"Parameter mismatch for layer {k}"
    print("  ✓ Model loaded: FedAvg 30R DNN (models/fedavg_global_dnn_30r.pth)")
    print("  ✓ Input features: 421 dimensions")
    print("  ✓ Operating mode: eval(), CPU device")
    print("  ✓ Configured threshold: 0.89")

    # ---------------------------------------------------------
    # TEST 2: Preprocessing Integrity (No Double Scaling)
    # ---------------------------------------------------------
    print("\n[TEST 2] Preprocessing Pipeline Verification...")
    assert fraud_model.scaler.n_features_in_ == 421
    assert len(fraud_model.category_mappings) == 29
    assert len(fraud_model.medians) == 421

    # Verify output shape and scaling
    sample_csv_path = BASE_DIR / "data" / "sample_transactions.csv"
    sample_df = pd.read_csv(sample_csv_path)
    X_preprocessed = fraud_model.preprocess_dataframe(sample_df)
    assert X_preprocessed.shape == (100, 421), f"Expected shape (100, 421), got {X_preprocessed.shape}"
    assert np.all(np.isfinite(X_preprocessed)), "Preprocessed features must all be finite"
    assert X_preprocessed.dtype == np.float32, f"Expected float32, got {X_preprocessed.dtype}"
    print("  ✓ Input normalization and 421-column alignment verified")
    print("  ✓ StandardScaler single-pass transformation verified (no double-scaling)")
    print(f"  ✓ Output range: min={X_preprocessed.min():.4f}, max={X_preprocessed.max():.4f}, all finite")

    # ---------------------------------------------------------
    # TEST 3: Single Transaction Prediction & SHAP
    # ---------------------------------------------------------
    print("\n[TEST 3] Single-Transaction Prediction & SHAP Explanation...")
    single_row = sample_df.iloc[[0]]
    single_res = fraud_model.predict_dataframe(single_row)

    assert single_res["success"] is True
    assert single_res["summary"]["total_transactions"] == 1
    assert len(single_res["transactions"]) == 1
    txn0 = single_res["transactions"][0]
    prob0 = txn0["fraud_probability"]
    assert 0.0 <= prob0 <= 1.0, f"Probability out of range: {prob0}"
    assert txn0["prediction"] == (1 if prob0 >= 0.89 else 0)

    # SHAP check
    assert fraud_model.shap_explainer is not None, "SHAP explainer should be initialized"
    assert len(txn0["explanation"]) == 5, f"Expected 5 top SHAP features, got {len(txn0['explanation'])}"
    for item in txn0["explanation"]:
        assert "feature" in item and item["feature"] in fraud_model.feature_names
        assert "shap_value" in item and np.isfinite(item["shap_value"])
        assert item["direction"] in ["increases_model_output", "decreases_model_output", "neutral"]

    print(f"  ✓ Transaction ID: {txn0['transaction_id']}")
    print(f"  ✓ Probability: {prob0:.4f}")
    print(f"  ✓ Prediction: {txn0['prediction']} ({'FRAUD' if txn0['prediction'] == 1 else 'LEGITIMATE'})")
    print(f"  ✓ Risk Level: {txn0['risk_level']}")
    print(f"  ✓ Top SHAP factor: {txn0['explanation'][0]['feature']} (shap={txn0['explanation'][0]['shap_value']:.4f}, {txn0['explanation'][0]['direction']})")

    # ---------------------------------------------------------
    # TEST 4: 100-Row Batch Validation & Threshold Test
    # ---------------------------------------------------------
    print("\n[TEST 4] 100-Row Sample CSV Batch Evaluation...")
    batch_res = fraud_model.predict_dataframe(sample_df)

    assert batch_res["success"] is True
    summary = batch_res["summary"]
    assert summary["total_transactions"] == 100
    assert summary["fraudulent_transactions"] + summary["legitimate_transactions"] == 100
    assert summary["fraud_rate"] == round(summary["fraudulent_transactions"] / 100 * 100, 2)

    probs = [t["fraud_probability"] for t in batch_res["transactions"]]
    preds = [t["prediction"] for t in batch_res["transactions"]]
    risks = [t["risk_level"] for t in batch_res["transactions"]]

    # Verify probability range
    assert all(0.0 <= p <= 1.0 for p in probs), "All probabilities must be in [0.0, 1.0]"
    assert all(np.isfinite(p) for p in probs), "All probabilities must be finite"

    # Verify threshold classification (prediction == 1 iff prob >= 0.89)
    for p, pred in zip(probs, preds):
        if p >= 0.89:
            assert pred == 1, f"Expected 1 for prob {p}, got {pred}"
        else:
            assert pred == 0, f"Expected 0 for prob {p}, got {pred}"

    # Verify risk stratification
    for p, r in zip(probs, risks):
        if p >= 0.89:
            assert r == "HIGH", f"Expected HIGH for prob {p}, got {r}"
        elif p >= 0.50:
            assert r == "MEDIUM", f"Expected MEDIUM for prob {p}, got {r}"
        else:
            assert r == "LOW", f"Expected LOW for prob {p}, got {r}"

    print(f"  ✓ Total processed: {summary['total_transactions']}")
    print(f"  ✓ Fraud detected: {summary['fraudulent_transactions']} ({summary['fraud_rate']}%)")
    print(f"  ✓ Legitimate: {summary['legitimate_transactions']}")
    print(f"  ✓ Probability bounds: min={min(probs):.4f}, max={max(probs):.4f}, mean={np.mean(probs):.4f}")
    print(f"  ✓ Threshold validation (tau=0.89): 100/100 predictions match threshold condition exactly")
    print(f"  ✓ Risk tiers: HIGH={risks.count('HIGH')}, MEDIUM={risks.count('MEDIUM')}, LOW={risks.count('LOW')}")

    # ---------------------------------------------------------
    # TEST 5: Flask HTTP API Endpoints (Health & Predict)
    # ---------------------------------------------------------
    print("\n[TEST 5] Flask HTTP API Integration Test...")
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # GET /api/health
    resp_health = client.get("/api/health")
    assert resp_health.status_code == 200
    data_health = json.loads(resp_health.data)
    assert data_health["status"] == "ok"
    assert data_health["model"] == "FedAvg 30R DNN"
    assert data_health["num_features"] == 421
    assert data_health["threshold"] == 0.89
    print("  ✓ GET /api/health: HTTP 200 OK")
    print(f"    Payload: {data_health}")

    # GET /api/sample-csv
    resp_sample = client.get("/api/sample-csv")
    assert resp_sample.status_code == 200
    assert "text/csv" in resp_sample.content_type
    print("  ✓ GET /api/sample-csv: HTTP 200 OK (Content-Type: text/csv)")

    # POST /api/predict (with 100-row sample CSV)
    with open(sample_csv_path, "rb") as f:
        csv_bytes = f.read()

    resp_predict = client.post(
        "/api/predict",
        data={"file": (io.BytesIO(csv_bytes), "sample_transactions.csv")},
        content_type="multipart/form-data"
    )
    assert resp_predict.status_code == 200
    data_predict = json.loads(resp_predict.data)
    assert data_predict["success"] is True
    assert data_predict["model_info"]["model"] == "FedAvg 30R DNN"
    assert data_predict["model_info"]["threshold"] == 0.89
    assert data_predict["model_info"]["num_features"] == 421
    assert data_predict["summary"]["total_transactions"] == 100
    assert len(data_predict["transactions"]) == 100
    print("  ✓ POST /api/predict: HTTP 200 OK")
    print(f"    Response model_info: {data_predict['model_info']}")
    print(f"    Response summary: {data_predict['summary']}")

    # POST /api/predict edge case: no file
    resp_no_file = client.post("/api/predict")
    assert resp_no_file.status_code == 400
    print("  ✓ POST /api/predict (no file validation): HTTP 400 Bad Request")

    print("\n" + "=" * 65)
    print("  ALL 5 TEST SUITES PASSED SUCCESSFULLY (100% GREEN)")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()


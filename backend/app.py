import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
from backend.config import Config
from backend.services.model_service import fraud_model

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable Cross-Origin Resource Sharing for Frontend communication
    CORS(app)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint to verify backend operational status and model metadata.
        """
        return jsonify({
            "status": "ok",
            "model": "LightGBM",
            "num_features": len(fraud_model.feature_names),
            "threshold": fraud_model.threshold
        }), 200

    @app.route('/api/sample-csv', methods=['GET'])
    def get_sample_csv():
        """
        Serve sample transaction CSV file for quick testing.
        """
        sample_path = Path(__file__).resolve().parents[1] / "data" / "sample_transactions.csv"
        if not sample_path.exists():
            sample_path = Path(__file__).resolve().parents[0] / "static" / "sample_transactions.csv"

        if sample_path.exists():
            return send_file(
                sample_path,
                mimetype="text/csv",
                as_attachment=True,
                download_name="sample_transactions.csv"
            )
        return jsonify({"success": False, "error": "Sample file not found."}), 404

    @app.route('/api/predict', methods=['POST'])
    def predict():
        """
        Endpoint for uploaded transaction CSV predictions using LightGBM model.
        """
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded. Please select a CSV transaction file."
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "Empty filename provided. Please upload a valid CSV file."
            }), 400

        if not file.filename.lower().endswith('.csv'):
            return jsonify({
                "success": False,
                "error": "Invalid file type. Please upload a .csv file."
            }), 400

        try:
            df = pd.read_csv(file)
            if df.empty:
                return jsonify({
                    "success": False,
                    "error": "The uploaded CSV file contains no transaction rows."
                }), 400

            results = fraud_model.predict_dataframe(df)
            return jsonify(results), 200

        except ValueError as ve:
            return jsonify({
                "success": False,
                "error": str(ve)
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to analyze transaction file: {str(e)}"
            }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


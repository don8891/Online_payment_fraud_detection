from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable Cross-Origin Resource Sharing for Frontend communication
    CORS(app)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Simple health check endpoint to verify backend operational status.
        """
        return jsonify({
            "status": "ok"
        }), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

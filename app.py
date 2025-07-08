# Minimal app.py for debugging 502 error
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Enable CORS for all routes
    CORS(app, origins="*")

    # A very simple health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Minimal Flask app is running'
        })

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# TRIGGER A NEW DEPLOYMENT
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.learner import Learner, LearningSession
from src.models.content import Content, LearningPath, Exercise
from src.routes.user import user_bp
from src.routes.learner import learner_bp
from src.routes.content import content_bp
from src.routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'dist'), static_url_path='')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # --- KEY CHANGE: Make trailing slashes optional ---
    app.url_map.strict_slashes = False
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(learner_bp, url_prefix='/api')
    app.register_blueprint(content_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    
    # Database configuration (still commented out for now)
    # ... (database config code remains here) ...

    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "Frontend not built. Please run 'npm run build' in the frontend directory.", 404

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


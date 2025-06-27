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
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'dist'))
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(learner_bp, url_prefix='/api')
    app.register_blueprint(content_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    
    # Database configuration
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Production: Use PostgreSQL
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development: Use SQLite (use existing database)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
        # Create all database tables
    with app.app_context():
        try:
            # !!! DANGER: This will drop all existing tables and data !!!
            # Use with extreme caution in production environments.
            # For initial setup/testing, this ensures a clean schema.
            print("Attempting to drop all database tables...", file=sys.stderr)
            db.drop_all()
            print("All database tables dropped (if they existed).", file=sys.stderr)

            print("Attempting to create all database tables...", file=sys.stderr)
            db.create_all()
            print("All database tables created.", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: Database initialization failed: {e}", file=sys.stderr)
            # Re-raise the exception to make the deployment fail if table creation is critical
            # For now, we'll just log and continue, but this is a strong indicator of a problem
            # raise e # Uncomment this if you want deployment to fail on DB error

    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'message': 'AI Learning Platform API is running',
            'version': '1.0.0',
            'environment': 'production' if os.getenv('DATABASE_URL') else 'development'
        }
    
    @app.route('/api/niches', methods=['GET'])
    def get_available_niches():
        """Get available learning niches"""
        return {
            'niches': [
                {
                    'id': 'tech_career',
                    'name': 'Tech Career Acceleration',
                    'description': 'Coding, AI, Data Science, Cloud Computing',
                    'categories': ['Programming', 'Data Science', 'Cloud Platforms', 'AI/ML', 'DevOps']
                },
                {
                    'id': 'creator_business',
                    'name': 'Business & Entrepreneurship for Creators',
                    'description': 'Building and monetizing creative businesses',
                    'categories': ['Content Marketing', 'Personal Branding', 'Monetization', 'Social Media', 'Email Marketing']
                }
            ]
        }
    
    @app.route('/api/learning-styles', methods=['GET'])
    def get_learning_styles():
        """Get available learning styles"""
        return {
            'learning_styles': [
                {
                    'id': 'visual',
                    'name': 'Visual',
                    'description': 'Learn best through images, diagrams, and visual representations'
                },
                {
                    'id': 'auditory',
                    'name': 'Auditory',
                    'description': 'Learn best through listening and verbal instruction'
                },
                {
                    'id': 'kinesthetic',
                    'name': 'Kinesthetic',
                    'description': 'Learn best through hands-on activities and movement'
                },
                {
                    'id': 'reading_writing',
                    'name': 'Reading/Writing',
                    'description': 'Learn best through reading and writing activities'
                }
            ]
        }
    
    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        # Skip static file serving for API routes
        if path.startswith('api/'):
            return "API endpoint not found", 404
            
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
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')


import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.learner import Learner, LearningSession
from src.models.content import Content, LearningPath, Exercise
from src.routes.user import user_bp
from src.routes.learner import learner_bp
from src.routes.content import content_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(learner_bp, url_prefix='/api')
app.register_blueprint(content_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create all database tables
with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'AI Learning Platform API is running',
        'version': '1.0.0'
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
            },
            {
                'id': 'certification_prep',
                'name': 'Professional Certifications & Licensure Prep',
                'description': 'Preparation for professional certifications',
                'categories': ['Finance (CFA, CPA)', 'Healthcare (NCLEX)', 'Legal (Bar Exam)', 'IT Certifications']
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
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


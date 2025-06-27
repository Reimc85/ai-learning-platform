from flask import Blueprint, request, jsonify
from src.models.learner import Learner, LearningSession, db
from src.models.user import User
from src.services.ai_service import AIContentGenerator
import json
from datetime import datetime

learner_bp = Blueprint('learner', __name__)
ai_generator = AIContentGenerator()

@learner_bp.route('/learners', methods=['POST'])
def create_learner_profile():
    """Create a new learner profile"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['user_id', 'target_niche']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if learner profile already exists for this user
        existing_learner = Learner.query.filter_by(user_id=data['user_id']).first()
        if existing_learner:
            return jsonify({'error': 'Learner profile already exists for this user'}), 400
        
        # Create new learner profile
        learner = Learner(
            user_id=data['user_id'],
            learning_goals=json.dumps(data.get('learning_goals', [])),
            preferred_learning_style=data.get('preferred_learning_style', 'visual'),
            time_availability=data.get('time_availability', 300),  # Default 5 hours per week
            experience_level=data.get('experience_level', 'beginner'),
            target_niche=data['target_niche'],
            knowledge_state=json.dumps({}),
            engagement_metrics=json.dumps({}),
            learning_preferences=json.dumps({})
        )
        
        db.session.add(learner)
        db.session.commit()
        
        return jsonify(learner.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners', methods=['GET'])
def get_all_learners():
    """Get all learner profiles"""
    learners = Learner.query.all()
    return jsonify([learner.to_dict() for learner in learners])

@learner_bp.route('/learners/<int:learner_id>', methods=['GET'])
def get_learner_profile(learner_id):
    """Get learner profile by ID"""
    learner = Learner.query.get_or_404(learner_id)
    return jsonify(learner.to_dict())

@learner_bp.route('/learners/<int:learner_id>', methods=['PUT'])
def update_learner_profile(learner_id):
    """Update learner profile"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        data = request.json
        
        # Update fields if provided
        if 'learning_goals' in data:
            learner.learning_goals = json.dumps(data['learning_goals'])
        if 'preferred_learning_style' in data:
            learner.preferred_learning_style = data['preferred_learning_style']
        if 'time_availability' in data:
            learner.time_availability = data['time_availability']
        if 'experience_level' in data:
            learner.experience_level = data['experience_level']
        if 'target_niche' in data:
            learner.target_niche = data['target_niche']
        
        learner.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(learner.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/knowledge-state', methods=['POST'])
def update_knowledge_state(learner_id):
    """Update knowledge state for specific concepts"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        data = request.json
        
        if 'concept' not in data or 'mastery_level' not in data:
            return jsonify({'error': 'Missing concept or mastery_level'}), 400
        
        learner.update_knowledge_state(data['concept'], data['mastery_level'])
        db.session.commit()
        
        return jsonify({
            'message': 'Knowledge state updated',
            'concept': data['concept'],
            'mastery_level': data['mastery_level']
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/knowledge-gaps', methods=['GET'])
def get_knowledge_gaps(learner_id):
    """Get concepts where learner needs improvement"""
    learner = Learner.query.get_or_404(learner_id)
    threshold = request.args.get('threshold', 0.7, type=float)
    
    knowledge_gaps = learner.get_knowledge_gaps(threshold)
    
    return jsonify({
        'learner_id': learner_id,
        'knowledge_gaps': knowledge_gaps,
        'threshold': threshold
    })

@learner_bp.route('/learners/<int:learner_id>/sessions', methods=['POST'])
def start_learning_session(learner_id):
    """Start a new learning session"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        
        session = LearningSession(
            learner_id=learner_id,
            session_start=datetime.utcnow(),
            content_accessed=json.dumps([]),
            exercises_completed=json.dumps([]),
            performance_scores=json.dumps({})
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify(session.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/sessions/<int:session_id>', methods=['PUT'])
def update_learning_session(learner_id, session_id):
    """Update learning session with interaction data"""
    try:
        session = LearningSession.query.filter_by(
            id=session_id, 
            learner_id=learner_id
        ).first_or_404()
        
        data = request.json
        
        # Update session data
        if 'content_accessed' in data:
            session.content_accessed = json.dumps(data['content_accessed'])
        if 'exercises_completed' in data:
            session.exercises_completed = json.dumps(data['exercises_completed'])
        if 'performance_scores' in data:
            session.performance_scores = json.dumps(data['performance_scores'])
        if 'clicks' in data:
            session.clicks = data['clicks']
        if 'time_on_content' in data:
            session.time_on_content = data['time_on_content']
        if 'completion_rate' in data:
            session.completion_rate = data['completion_rate']
        
        db.session.commit()
        
        return jsonify(session.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/sessions/<int:session_id>/end', methods=['POST'])
def end_learning_session(learner_id, session_id):
    """End a learning session"""
    try:
        session = LearningSession.query.filter_by(
            id=session_id, 
            learner_id=learner_id
        ).first_or_404()
        
        session.session_end = datetime.utcnow()
        
        # Calculate duration
        if session.session_start:
            duration = session.session_end - session.session_start
            session.duration_minutes = int(duration.total_seconds() / 60)
        
        db.session.commit()
        
        # Update learner engagement metrics
        learner = Learner.query.get(learner_id)
        learner.update_engagement_metrics('last_session_duration', session.duration_minutes)
        learner.update_engagement_metrics('last_session_completion', session.completion_rate)
        db.session.commit()
        
        return jsonify(session.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/sessions', methods=['GET'])
def get_learning_sessions(learner_id):
    """Get all learning sessions for a learner"""
    learner = Learner.query.get_or_404(learner_id)
    sessions = LearningSession.query.filter_by(learner_id=learner_id).order_by(
        LearningSession.session_start.desc()
    ).all()
    
    return jsonify([session.to_dict() for session in sessions])

@learner_bp.route('/learners/<int:learner_id>/generate-content', methods=['POST'])
def generate_personalized_content(learner_id):
    """Generate personalized content for a learner"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        data = request.json
        
        if 'concept' not in data:
            return jsonify({'error': 'Missing concept'}), 400
        
        concept = data['concept']
        content_type = data.get('content_type', 'lesson')
        difficulty_level = data.get('difficulty_level', learner.experience_level)
        
        learner_profile = learner.to_dict()
        
        # Prepare personalization parameters
        personalization_params = {
            'learning_style': learner.preferred_learning_style,
            'experience_level': learner.experience_level,
            'niche': learner.target_niche
        }
        
        if content_type == 'lesson':
            generated_content = ai_generator.generate_personalized_content(
                concept=concept,
                content_type='lesson',
                personalization_params=personalization_params
            )
        elif content_type == 'exercise':
            exercise_type = data.get('exercise_type', 'multiple_choice')
            generated_content = ai_generator.generate_personalized_content(
                concept=concept,
                content_type='exercise',
                personalization_params=personalization_params,
                exercise_type=exercise_type
            )
        else:
            return jsonify({'error': 'Invalid content_type'}), 400
        
        return jsonify({
            'concept': concept,
            'content_type': content_type,
            'learner_id': learner_id,
            'generated_content': generated_content,
            'personalization_params': {
                'learning_style': learner.preferred_learning_style,
                'experience_level': learner.experience_level,
                'niche': learner.target_niche,
                'difficulty_level': difficulty_level
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learner_bp.route('/learners/<int:learner_id>/feedback', methods=['POST'])
def generate_personalized_feedback(learner_id):
    """Generate personalized feedback for a learner's response"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        data = request.json
        
        required_fields = ['learner_answer', 'correct_answer', 'concept']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        learner_profile = learner.to_dict()
        
        feedback = ai_generator.generate_personalized_feedback(
            learner_answer=data['learner_answer'],
            correct_answer=data['correct_answer'],
            concept=data['concept'],
            learner_profile=learner_profile
        )
        
        return jsonify({
            'learner_id': learner_id,
            'concept': data['concept'],
            'feedback': feedback,
            'personalized_for': {
                'learning_style': learner.preferred_learning_style,
                'experience_level': learner.experience_level
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


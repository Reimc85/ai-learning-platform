from flask import Blueprint, jsonify, request
from src.models.learner import Learner
from src.services.analytics_service import LearningAnalyticsService
from src.services.ai_service import AIContentGenerator
import json

analytics_bp = Blueprint('analytics', __name__)
analytics_service = LearningAnalyticsService()
ai_generator = AIContentGenerator()

@analytics_bp.route('/learners/<int:learner_id>/analytics/velocity', methods=['GET'])
def get_learning_velocity(learner_id):
    """Get learning velocity metrics for a learner"""
    try:
        days = request.args.get('days', 30, type=int)
        velocity = analytics_service.calculate_learning_velocity(learner_id, days)
        return jsonify(velocity)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/patterns', methods=['GET'])
def get_learning_patterns(learner_id):
    """Get learning patterns analysis for a learner"""
    try:
        patterns = analytics_service.analyze_learning_patterns(learner_id)
        return jsonify(patterns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/progress-report', methods=['GET'])
def get_progress_report(learner_id):
    """Get comprehensive progress report for a learner"""
    try:
        report = analytics_service.generate_progress_report(learner_id)
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/knowledge-gaps', methods=['POST'])
def analyze_knowledge_gaps(learner_id):
    """Analyze knowledge gaps based on learner responses"""
    try:
        data = request.json
        learner_responses = data.get('responses', [])
        
        learner = Learner.query.get_or_404(learner_id)
        learner_profile = learner.to_dict()
        
        gaps = ai_generator.analyze_knowledge_gaps(learner_responses, learner_profile)
        
        return jsonify({
            'learner_id': learner_id,
            'knowledge_gaps': gaps,
            'analysis_date': analytics_service.generate_progress_report(learner_id).get('generated_at')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/learning-path', methods=['POST'])
def get_learning_path_recommendations(learner_id):
    """Get personalized learning path recommendations"""
    try:
        data = request.json or {}
        
        learner = Learner.query.get_or_404(learner_id)
        learner_profile = learner.to_dict()
        
        # Get knowledge gaps
        learner_responses = data.get('responses', [])
        knowledge_gaps = ai_generator.analyze_knowledge_gaps(learner_responses, learner_profile)
        
        # Get current performance
        current_performance = analytics_service.generate_progress_report(learner_id).get('overall_progress', {})
        
        # Generate recommendations
        recommendations = ai_generator.recommend_learning_path(
            learner_profile, 
            knowledge_gaps, 
            current_performance
        )
        
        return jsonify({
            'learner_id': learner_id,
            'recommendations': recommendations,
            'based_on': {
                'knowledge_gaps': len(knowledge_gaps),
                'current_mastery': current_performance.get('mastery_score', 0),
                'learning_style': learner.preferred_learning_style,
                'experience_level': learner.experience_level
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/retention/<concept>', methods=['GET'])
def get_knowledge_retention(learner_id, concept):
    """Get knowledge retention analysis for a specific concept"""
    try:
        retention = analytics_service.calculate_knowledge_retention(learner_id, concept)
        return jsonify(retention)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/prediction/<concept>', methods=['GET'])
def predict_learning_outcome(learner_id, concept):
    """Predict learning outcomes for a target concept"""
    try:
        prediction = analytics_service.predict_learning_outcome(learner_id, concept)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/difficulty-adjustment', methods=['POST'])
def adjust_content_difficulty(learner_id):
    """Adjust content difficulty based on performance"""
    try:
        data = request.json
        current_difficulty = data.get('current_difficulty', 'beginner')
        performance_score = data.get('performance_score', 0.5)
        
        new_difficulty = ai_generator.adjust_difficulty(current_difficulty, performance_score)
        
        # Update learner's experience level if significantly different
        learner = Learner.query.get_or_404(learner_id)
        if new_difficulty != current_difficulty:
            # Update engagement metrics to track difficulty adjustments
            engagement_metrics = json.loads(learner.engagement_metrics or '{}')
            engagement_metrics['last_difficulty_adjustment'] = {
                'from': current_difficulty,
                'to': new_difficulty,
                'performance_score': performance_score,
                'timestamp': analytics_service.generate_progress_report(learner_id).get('generated_at')
            }
            learner.engagement_metrics = json.dumps(engagement_metrics)
            
            from src.models.learner import db
            db.session.commit()
        
        return jsonify({
            'learner_id': learner_id,
            'previous_difficulty': current_difficulty,
            'recommended_difficulty': new_difficulty,
            'performance_score': performance_score,
            'adjustment_made': new_difficulty != current_difficulty
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/learners/<int:learner_id>/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard(learner_id):
    """Get comprehensive analytics dashboard data"""
    try:
        # Gather all analytics data
        velocity = analytics_service.calculate_learning_velocity(learner_id)
        patterns = analytics_service.analyze_learning_patterns(learner_id)
        progress_report = analytics_service.generate_progress_report(learner_id)
        
        # Get recent performance for knowledge gaps analysis
        learner = Learner.query.get_or_404(learner_id)
        
        # Mock recent responses for demonstration
        mock_responses = [
            {'concept': 'Python Functions', 'is_correct': True, 'difficulty_level': 'beginner'},
            {'concept': 'Data Structures', 'is_correct': False, 'difficulty_level': 'intermediate'},
            {'concept': 'Algorithm Optimization', 'is_correct': False, 'difficulty_level': 'intermediate'}
        ]
        
        knowledge_gaps = ai_generator.analyze_knowledge_gaps(mock_responses, learner.to_dict())
        
        dashboard_data = {
            'learner_id': learner_id,
            'summary': {
                'overall_mastery': progress_report.get('overall_progress', {}).get('mastery_score', 0),
                'learning_velocity': velocity.get('velocity_score', 0),
                'consistency_score': patterns.get('learning_consistency', 0),
                'sessions_this_week': velocity.get('sessions_per_week', 0),
                'total_concepts': progress_report.get('overall_progress', {}).get('total_concepts', 0)
            },
            'velocity_metrics': velocity,
            'learning_patterns': patterns,
            'progress_breakdown': progress_report.get('overall_progress', {}),
            'knowledge_gaps': knowledge_gaps[:3],  # Top 3 gaps
            'recommendations': progress_report.get('recommendations', [])[:3],  # Top 3 recommendations
            'goals_progress': progress_report.get('goals_progress', []),
            'generated_at': progress_report.get('generated_at')
        }
        
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


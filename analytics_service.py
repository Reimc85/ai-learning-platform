import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from src.models.learner import Learner, LearningSession
from src.models.content import Content, Exercise
from sqlalchemy import func, and_

class LearningAnalyticsService:
    """
    Advanced learning analytics service for tracking progress, 
    analyzing performance patterns, and generating insights
    """
    
    def __init__(self):
        pass
    
    def calculate_learning_velocity(self, learner_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Calculate how quickly a learner is progressing through content
        """
        from src.models.learner import db
        
        # Get recent learning sessions
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        sessions = LearningSession.query.filter(
            and_(
                LearningSession.learner_id == learner_id,
                LearningSession.session_start >= cutoff_date
            )
        ).all()
        
        if not sessions:
            return {
                'velocity_score': 0.0,
                'sessions_per_week': 0.0,
                'avg_session_duration': 0.0,
                'content_completion_rate': 0.0,
                'trend': 'no_data'
            }
        
        # Calculate metrics
        total_sessions = len(sessions)
        total_duration = sum(s.duration_minutes or 0 for s in sessions)
        total_content_accessed = sum(len(json.loads(s.content_accessed or '[]')) for s in sessions)
        total_exercises_completed = sum(len(json.loads(s.exercises_completed or '[]')) for s in sessions)
        
        # Calculate velocity metrics
        sessions_per_week = (total_sessions / days) * 7
        avg_session_duration = total_duration / total_sessions if total_sessions > 0 else 0
        avg_completion_rate = sum(s.completion_rate or 0 for s in sessions) / total_sessions if total_sessions > 0 else 0
        
        # Calculate velocity score (composite metric)
        velocity_score = (
            (sessions_per_week * 0.3) +
            (avg_session_duration / 60 * 0.2) +  # Normalize to hours
            (avg_completion_rate * 0.3) +
            (total_exercises_completed / max(total_sessions, 1) * 0.2)
        )
        
        # Determine trend
        if len(sessions) >= 4:
            recent_sessions = sessions[-2:]
            older_sessions = sessions[:2]
            recent_avg = sum(s.completion_rate or 0 for s in recent_sessions) / len(recent_sessions)
            older_avg = sum(s.completion_rate or 0 for s in older_sessions) / len(older_sessions)
            
            if recent_avg > older_avg * 1.1:
                trend = 'improving'
            elif recent_avg < older_avg * 0.9:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'velocity_score': round(velocity_score, 2),
            'sessions_per_week': round(sessions_per_week, 1),
            'avg_session_duration': round(avg_session_duration, 1),
            'content_completion_rate': round(avg_completion_rate, 2),
            'total_content_accessed': total_content_accessed,
            'total_exercises_completed': total_exercises_completed,
            'trend': trend
        }
    
    def analyze_learning_patterns(self, learner_id: int) -> Dict[str, Any]:
        """
        Analyze learner's behavioral patterns and preferences
        """
        from src.models.learner import db
        
        learner = Learner.query.get(learner_id)
        if not learner:
            return {'error': 'Learner not found'}
        
        sessions = LearningSession.query.filter_by(learner_id=learner_id).all()
        
        if not sessions:
            return {
                'preferred_session_length': 'unknown',
                'peak_performance_time': 'unknown',
                'learning_consistency': 0.0,
                'content_preferences': {},
                'difficulty_progression': 'unknown'
            }
        
        # Analyze session lengths
        session_durations = [s.duration_minutes for s in sessions if s.duration_minutes]
        if session_durations:
            avg_duration = sum(session_durations) / len(session_durations)
            if avg_duration < 20:
                preferred_length = 'short'
            elif avg_duration < 45:
                preferred_length = 'medium'
            else:
                preferred_length = 'long'
        else:
            preferred_length = 'unknown'
        
        # Analyze performance by time of day (mock implementation)
        # In a real system, you'd analyze actual session start times
        peak_time = 'morning'  # Placeholder
        
        # Calculate learning consistency
        if len(sessions) >= 7:
            # Calculate variance in session frequency
            session_dates = [s.session_start.date() for s in sessions if s.session_start]
            date_counts = defaultdict(int)
            for date in session_dates:
                date_counts[date] += 1
            
            if len(date_counts) > 1:
                frequencies = list(date_counts.values())
                mean_freq = sum(frequencies) / len(frequencies)
                variance = sum((f - mean_freq) ** 2 for f in frequencies) / len(frequencies)
                consistency = max(0, 1 - (variance / (mean_freq + 1)))
            else:
                consistency = 1.0 if len(sessions) > 0 else 0.0
        else:
            consistency = 0.5  # Insufficient data
        
        # Analyze content preferences
        content_types = defaultdict(int)
        for session in sessions:
            content_accessed = json.loads(session.content_accessed or '[]')
            for content in content_accessed:
                content_type = content.get('type', 'unknown')
                content_types[content_type] += 1
        
        return {
            'preferred_session_length': preferred_length,
            'peak_performance_time': peak_time,
            'learning_consistency': round(consistency, 2),
            'content_preferences': dict(content_types),
            'difficulty_progression': 'steady',  # Placeholder
            'total_sessions': len(sessions)
        }
    
    def generate_progress_report(self, learner_id: int) -> Dict[str, Any]:
        """
        Generate comprehensive progress report for a learner
        """
        learner = Learner.query.get(learner_id)
        if not learner:
            return {'error': 'Learner not found'}
        
        # Get learning velocity
        velocity = self.calculate_learning_velocity(learner_id)
        
        # Get learning patterns
        patterns = self.analyze_learning_patterns(learner_id)
        
        # Get knowledge state
        knowledge_state = json.loads(learner.knowledge_state or '{}')
        
        # Calculate overall progress
        if knowledge_state:
            mastery_scores = list(knowledge_state.values())
            overall_mastery = sum(mastery_scores) / len(mastery_scores)
            concepts_mastered = sum(1 for score in mastery_scores if score >= 0.8)
            concepts_in_progress = sum(1 for score in mastery_scores if 0.3 <= score < 0.8)
            concepts_struggling = sum(1 for score in mastery_scores if score < 0.3)
        else:
            overall_mastery = 0.0
            concepts_mastered = 0
            concepts_in_progress = 0
            concepts_struggling = 0
        
        # Generate learning goals progress
        learning_goals = json.loads(learner.learning_goals or '[]')
        goals_progress = []
        for goal in learning_goals:
            # Mock progress calculation - in real system, would track specific goal metrics
            progress = min(overall_mastery + 0.1, 1.0)  # Slight boost for goal tracking
            goals_progress.append({
                'goal': goal,
                'progress': round(progress, 2),
                'status': 'completed' if progress >= 0.9 else 'in_progress' if progress >= 0.3 else 'not_started'
            })
        
        return {
            'learner_id': learner_id,
            'overall_progress': {
                'mastery_score': round(overall_mastery, 2),
                'concepts_mastered': concepts_mastered,
                'concepts_in_progress': concepts_in_progress,
                'concepts_struggling': concepts_struggling,
                'total_concepts': len(knowledge_state)
            },
            'learning_velocity': velocity,
            'learning_patterns': patterns,
            'goals_progress': goals_progress,
            'recommendations': self._generate_recommendations(learner, velocity, patterns, overall_mastery),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_recommendations(self, learner: Learner, velocity: Dict, patterns: Dict, mastery: float) -> List[Dict[str, Any]]:
        """
        Generate personalized recommendations based on analytics
        """
        recommendations = []
        
        # Velocity-based recommendations
        if velocity['velocity_score'] < 1.0:
            recommendations.append({
                'type': 'engagement',
                'priority': 'high',
                'title': 'Increase Learning Frequency',
                'description': 'Try to have more frequent, shorter learning sessions to build momentum.',
                'action': 'Schedule 15-20 minute daily learning sessions'
            })
        
        if velocity['avg_session_duration'] < 15:
            recommendations.append({
                'type': 'session_length',
                'priority': 'medium',
                'title': 'Extend Session Duration',
                'description': 'Longer sessions can help you dive deeper into concepts.',
                'action': 'Aim for 25-30 minute sessions for better retention'
            })
        
        # Pattern-based recommendations
        if patterns['learning_consistency'] < 0.5:
            recommendations.append({
                'type': 'consistency',
                'priority': 'high',
                'title': 'Improve Learning Consistency',
                'description': 'Regular learning schedules lead to better retention and progress.',
                'action': 'Set a specific time each day for learning'
            })
        
        # Mastery-based recommendations
        if mastery < 0.4:
            recommendations.append({
                'type': 'foundation',
                'priority': 'high',
                'title': 'Strengthen Fundamentals',
                'description': 'Focus on mastering basic concepts before moving to advanced topics.',
                'action': 'Review and practice fundamental concepts in your niche'
            })
        elif mastery > 0.8:
            recommendations.append({
                'type': 'advancement',
                'priority': 'medium',
                'title': 'Ready for Advanced Content',
                'description': 'Your strong foundation allows you to tackle more challenging material.',
                'action': 'Explore advanced topics and real-world projects'
            })
        
        # Learning style recommendations
        if learner.preferred_learning_style == 'visual' and patterns.get('content_preferences', {}).get('text', 0) > patterns.get('content_preferences', {}).get('visual', 0):
            recommendations.append({
                'type': 'learning_style',
                'priority': 'medium',
                'title': 'Leverage Visual Learning',
                'description': 'As a visual learner, you might benefit from more diagram and image-based content.',
                'action': 'Seek out visual explanations, diagrams, and interactive content'
            })
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def calculate_knowledge_retention(self, learner_id: int, concept: str) -> Dict[str, Any]:
        """
        Calculate knowledge retention for a specific concept over time
        """
        # Mock implementation - in a real system, this would track performance over time
        learner = Learner.query.get(learner_id)
        if not learner:
            return {'error': 'Learner not found'}
        
        knowledge_state = json.loads(learner.knowledge_state or '{}')
        current_mastery = knowledge_state.get(concept, 0.0)
        
        # Simulate retention curve (Ebbinghaus forgetting curve)
        days_since_last_review = 7  # Mock value
        retention_factor = math.exp(-days_since_last_review / 30)  # 30-day half-life
        estimated_retention = current_mastery * retention_factor
        
        return {
            'concept': concept,
            'current_mastery': current_mastery,
            'estimated_retention': round(estimated_retention, 2),
            'days_since_review': days_since_last_review,
            'needs_review': estimated_retention < 0.6,
            'recommended_review_date': (datetime.utcnow() + timedelta(days=max(1, int(30 * math.log(0.6 / current_mastery))))).isoformat() if current_mastery > 0 else None
        }
    
    def predict_learning_outcome(self, learner_id: int, target_concept: str) -> Dict[str, Any]:
        """
        Predict learning outcomes for a target concept based on current progress
        """
        learner = Learner.query.get(learner_id)
        if not learner:
            return {'error': 'Learner not found'}
        
        # Get current analytics
        velocity = self.calculate_learning_velocity(learner_id)
        patterns = self.analyze_learning_patterns(learner_id)
        
        # Mock prediction algorithm
        base_time = 120  # Base minutes to learn a concept
        
        # Adjust based on experience level
        experience_multiplier = {
            'beginner': 1.5,
            'intermediate': 1.0,
            'advanced': 0.7
        }.get(learner.experience_level, 1.0)
        
        # Adjust based on learning velocity
        velocity_multiplier = max(0.5, 2.0 - velocity['velocity_score'])
        
        # Adjust based on consistency
        consistency_multiplier = max(0.8, 2.0 - patterns['learning_consistency'])
        
        estimated_time = base_time * experience_multiplier * velocity_multiplier * consistency_multiplier
        
        # Calculate success probability
        success_factors = [
            velocity['velocity_score'] / 2.0,
            patterns['learning_consistency'],
            1.0 if learner.experience_level != 'beginner' else 0.8
        ]
        success_probability = min(0.95, sum(success_factors) / len(success_factors))
        
        return {
            'target_concept': target_concept,
            'estimated_learning_time_minutes': round(estimated_time),
            'estimated_sessions_needed': math.ceil(estimated_time / (patterns.get('preferred_session_length', 30))),
            'success_probability': round(success_probability, 2),
            'confidence_level': 'high' if len(LearningSession.query.filter_by(learner_id=learner_id).all()) >= 10 else 'medium',
            'key_factors': {
                'experience_level': learner.experience_level,
                'learning_velocity': velocity['velocity_score'],
                'consistency': patterns['learning_consistency']
            }
        }


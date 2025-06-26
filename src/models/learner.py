from datetime import datetime
import json
from src.models.user import db

class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic profile information
    learning_goals = db.Column(db.Text)  # JSON string of goals
    preferred_learning_style = db.Column(db.String(50))  # visual, auditory, kinesthetic, reading_writing
    time_availability = db.Column(db.Integer)  # minutes per week
    experience_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    target_niche = db.Column(db.String(50))  # tech_career, creator_business, certification_prep
    
    # Dynamic profile data
    knowledge_state = db.Column(db.Text)  # JSON string of concept mastery levels
    engagement_metrics = db.Column(db.Text)  # JSON string of engagement data
    learning_preferences = db.Column(db.Text)  # JSON string of inferred preferences
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Learner {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_goals': json.loads(self.learning_goals) if self.learning_goals else [],
            'preferred_learning_style': self.preferred_learning_style,
            'time_availability': self.time_availability,
            'experience_level': self.experience_level,
            'target_niche': self.target_niche,
            'knowledge_state': json.loads(self.knowledge_state) if self.knowledge_state else {},
            'engagement_metrics': json.loads(self.engagement_metrics) if self.engagement_metrics else {},
            'learning_preferences': json.loads(self.learning_preferences) if self.learning_preferences else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_knowledge_state(self, concept, mastery_level):
        """Update mastery level for a specific concept"""
        knowledge = json.loads(self.knowledge_state) if self.knowledge_state else {}
        knowledge[concept] = mastery_level
        self.knowledge_state = json.dumps(knowledge)
        self.updated_at = datetime.utcnow()
    
    def get_knowledge_gaps(self, threshold=0.7):
        """Get concepts where mastery is below threshold"""
        knowledge = json.loads(self.knowledge_state) if self.knowledge_state else {}
        return [concept for concept, mastery in knowledge.items() if mastery < threshold]
    
    def update_engagement_metrics(self, metric_name, value):
        """Update engagement metrics"""
        metrics = json.loads(self.engagement_metrics) if self.engagement_metrics else {}
        metrics[metric_name] = value
        self.engagement_metrics = json.dumps(metrics)
        self.updated_at = datetime.utcnow()


class LearningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'), nullable=False)
    
    # Session data
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    session_end = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    
    # Content interaction
    content_accessed = db.Column(db.Text)  # JSON array of content IDs
    exercises_completed = db.Column(db.Text)  # JSON array of exercise data
    performance_scores = db.Column(db.Text)  # JSON object of scores
    
    # Engagement data
    clicks = db.Column(db.Integer, default=0)
    time_on_content = db.Column(db.Integer, default=0)  # seconds
    completion_rate = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<LearningSession {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'session_start': self.session_start.isoformat() if self.session_start else None,
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'duration_minutes': self.duration_minutes,
            'content_accessed': json.loads(self.content_accessed) if self.content_accessed else [],
            'exercises_completed': json.loads(self.exercises_completed) if self.exercises_completed else [],
            'performance_scores': json.loads(self.performance_scores) if self.performance_scores else {},
            'clicks': self.clicks,
            'time_on_content': self.time_on_content,
            'completion_rate': self.completion_rate
        }


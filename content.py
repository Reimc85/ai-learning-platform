from datetime import datetime
import json
from src.models.user import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Content metadata
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # lesson, exercise, assessment, example
    niche = db.Column(db.String(50), nullable=False)  # tech_career, creator_business, certification_prep
    difficulty_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    
    # Content data
    content_body = db.Column(db.Text)  # Main content (text, HTML, etc.)
    content_metadata = db.Column(db.Text)  # JSON string for additional metadata
    
    # Learning objectives and prerequisites
    learning_objectives = db.Column(db.Text)  # JSON array of objectives
    prerequisites = db.Column(db.Text)  # JSON array of prerequisite concepts
    concepts_covered = db.Column(db.Text)  # JSON array of concepts this content covers
    
    # AI generation info
    is_ai_generated = db.Column(db.Boolean, default=False)
    generation_prompt = db.Column(db.Text)  # Prompt used to generate this content
    personalization_params = db.Column(db.Text)  # JSON of params used for personalization
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Content {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content_type': self.content_type,
            'niche': self.niche,
            'difficulty_level': self.difficulty_level,
            'content_body': self.content_body,
            'metadata': json.loads(self.content_metadata) if self.content_metadata else {},
            'learning_objectives': json.loads(self.learning_objectives) if self.learning_objectives else [],
            'prerequisites': json.loads(self.prerequisites) if self.prerequisites else [],
            'concepts_covered': json.loads(self.concepts_covered) if self.concepts_covered else [],
            'is_ai_generated': self.is_ai_generated,
            'generation_prompt': self.generation_prompt,
            'personalization_params': json.loads(self.personalization_params) if self.personalization_params else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'), nullable=False)
    
    # Path metadata
    path_name = db.Column(db.String(200))
    target_goal = db.Column(db.String(200))
    estimated_duration_hours = db.Column(db.Integer)
    
    # Path structure
    content_sequence = db.Column(db.Text)  # JSON array of content IDs in order
    current_position = db.Column(db.Integer, default=0)
    completion_status = db.Column(db.String(20), default='in_progress')  # not_started, in_progress, completed
    
    # Adaptive data
    adaptation_history = db.Column(db.Text)  # JSON log of path modifications
    performance_data = db.Column(db.Text)  # JSON of performance on each content item
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningPath {self.path_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'path_name': self.path_name,
            'target_goal': self.target_goal,
            'estimated_duration_hours': self.estimated_duration_hours,
            'content_sequence': json.loads(self.content_sequence) if self.content_sequence else [],
            'current_position': self.current_position,
            'completion_status': self.completion_status,
            'adaptation_history': json.loads(self.adaptation_history) if self.adaptation_history else [],
            'performance_data': json.loads(self.performance_data) if self.performance_data else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_next_content(self):
        """Get the next content item in the learning path"""
        sequence = json.loads(self.content_sequence) if self.content_sequence else []
        if self.current_position < len(sequence):
            return sequence[self.current_position]
        return None
    
    def advance_position(self):
        """Move to the next content item"""
        sequence = json.loads(self.content_sequence) if self.content_sequence else []
        if self.current_position < len(sequence) - 1:
            self.current_position += 1
            self.updated_at = datetime.utcnow()
            return True
        else:
            self.completion_status = 'completed'
            self.updated_at = datetime.utcnow()
            return False
    
    def add_content_to_path(self, content_id, position=None):
        """Add content to the learning path at specified position"""
        sequence = json.loads(self.content_sequence) if self.content_sequence else []
        if position is None:
            sequence.append(content_id)
        else:
            sequence.insert(position, content_id)
        self.content_sequence = json.dumps(sequence)
        self.updated_at = datetime.utcnow()


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    
    # Exercise data
    question = db.Column(db.Text, nullable=False)
    exercise_type = db.Column(db.String(50))  # multiple_choice, coding, essay, simulation
    correct_answer = db.Column(db.Text)
    explanation = db.Column(db.Text)
    
    # Multiple choice specific
    options = db.Column(db.Text)  # JSON array of options
    
    # Coding specific
    starter_code = db.Column(db.Text)
    test_cases = db.Column(db.Text)  # JSON array of test cases
    
    # Difficulty and metadata
    difficulty_score = db.Column(db.Float)
    estimated_time_minutes = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Exercise {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'content_id': self.content_id,
            'question': self.question,
            'exercise_type': self.exercise_type,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'options': json.loads(self.options) if self.options else [],
            'starter_code': self.starter_code,
            'test_cases': json.loads(self.test_cases) if self.test_cases else [],
            'difficulty_score': self.difficulty_score,
            'estimated_time_minutes': self.estimated_time_minutes
        }


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from datetime import datetime

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)  # For uploaded files
    
    # Evaluation scores
    structure_score = db.Column(db.Float, nullable=True)
    content_score = db.Column(db.Float, nullable=True)
    sociological_depth_score = db.Column(db.Float, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    
    # Feedback
    feedback = db.Column(db.Text, nullable=True)
    keywords_used = db.Column(db.Text, nullable=True)  # JSON string of keywords
    thinkers_mentioned = db.Column(db.Text, nullable=True)  # JSON string of thinkers
    theories_referenced = db.Column(db.Text, nullable=True)  # JSON string of theories
    
    # Metadata
    topic = db.Column(db.String(100), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    evaluated_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Answer {self.id}: User {self.user_id} - Question {self.question_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'answer_text': self.answer_text,
            'file_path': self.file_path,
            'structure_score': self.structure_score,
            'content_score': self.content_score,
            'sociological_depth_score': self.sociological_depth_score,
            'overall_score': self.overall_score,
            'feedback': self.feedback,
            'keywords_used': self.keywords_used,
            'thinkers_mentioned': self.thinkers_mentioned,
            'theories_referenced': self.theories_referenced,
            'topic': self.topic,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None
        } 
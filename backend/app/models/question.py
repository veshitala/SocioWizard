import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from datetime import datetime

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Syllabus mapping
    syllabus_topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=True)
    syllabus_subtopic_id = db.Column(db.Integer, db.ForeignKey('syllabus_subtopic.id'), nullable=True)
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.theme} ({self.year})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'year': self.year,
            'theme': self.theme,
            'topic': self.topic,
            'marks': self.marks,
            'syllabus_topic_id': self.syllabus_topic_id,
            'syllabus_subtopic_id': self.syllabus_subtopic_id
        } 
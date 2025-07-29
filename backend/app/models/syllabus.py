import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from datetime import datetime

class SyllabusTopic(db.Model):
    """Main topics in UPSC CSE Sociology syllabus"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)  # e.g., "PAPER1", "PAPER2"
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)  # Relative importance
    order_index = db.Column(db.Integer, default=0)
    paper = db.Column(db.String(10), nullable=False)  # PAPER1 or PAPER2
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    subtopics = db.relationship('SyllabusSubtopic', backref='topic', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SyllabusTopic {self.code}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'weightage': self.weightage,
            'order_index': self.order_index,
            'subtopics_count': len(self.subtopics)
        }

class SyllabusSubtopic(db.Model):
    """Subtopics within main topics"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False)  # e.g., "PAPER1_1.1"
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)
    order_index = db.Column(db.Integer, default=0)
    topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - will be handled in Question model
    
    def __repr__(self):
        return f'<SyllabusSubtopic {self.code}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'weightage': self.weightage,
            'order_index': self.order_index,
            'topic_id': self.topic_id,
            'topic_name': self.topic.name if self.topic else None
        } 
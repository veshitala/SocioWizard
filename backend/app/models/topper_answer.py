import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from datetime import datetime

class TopperAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    # Topper details
    topper_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    marks_obtained = db.Column(db.Float, nullable=True)
    
    # Answer content
    answer_text = db.Column(db.Text, nullable=False)
    keywords_used = db.Column(db.Text, nullable=True)  # JSON string
    thinkers_mentioned = db.Column(db.Text, nullable=True)  # JSON string
    theories_referenced = db.Column(db.Text, nullable=True)  # JSON string
    
    # Analysis features
    word_count = db.Column(db.Integer, nullable=True)
    structure_score = db.Column(db.Float, nullable=True)
    content_depth = db.Column(db.Float, nullable=True)
    sociological_relevance = db.Column(db.Float, nullable=True)
    
    # Embeddings for similarity
    answer_embedding = db.Column(db.Text, nullable=True)  # JSON string of vector
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TopperAnswer {self.id}: {self.topper_name} - Question {self.question_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'topper_name': self.topper_name,
            'year': self.year,
            'rank': self.rank,
            'marks_obtained': self.marks_obtained,
            'answer_text': self.answer_text,
            'keywords_used': self.keywords_used,
            'thinkers_mentioned': self.thinkers_mentioned,
            'theories_referenced': self.theories_referenced,
            'word_count': self.word_count,
            'structure_score': self.structure_score,
            'content_depth': self.content_depth,
            'sociological_relevance': self.sociological_relevance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AnswerSimilarity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    topper_answer_id = db.Column(db.Integer, db.ForeignKey('topper_answer.id'), nullable=False)
    
    # Similarity scores
    overall_similarity = db.Column(db.Float, nullable=False)
    content_similarity = db.Column(db.Float, nullable=True)
    structure_similarity = db.Column(db.Float, nullable=True)
    keyword_similarity = db.Column(db.Float, nullable=True)
    theory_similarity = db.Column(db.Float, nullable=True)
    
    # Feedback
    feedback_text = db.Column(db.Text, nullable=True)
    improvement_suggestions = db.Column(db.Text, nullable=True)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnswerSimilarity {self.id}: Answer {self.user_answer_id} vs Topper {self.topper_answer_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_answer_id': self.user_answer_id,
            'topper_answer_id': self.topper_answer_id,
            'overall_similarity': self.overall_similarity,
            'content_similarity': self.content_similarity,
            'structure_similarity': self.structure_similarity,
            'keyword_similarity': self.keyword_similarity,
            'theory_similarity': self.theory_similarity,
            'feedback_text': self.feedback_text,
            'improvement_suggestions': self.improvement_suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 
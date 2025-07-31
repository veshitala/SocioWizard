from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sociowizard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

# Define models inline to avoid import issues
class SyllabusTopic(db.Model):
    """Main topics in UPSC CSE Sociology syllabus"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SyllabusSubtopic(db.Model):
    """Subtopics within main topics"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)
    order_index = db.Column(db.Integer, default=0)
    topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Syllabus mapping
    syllabus_topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=True)
    syllabus_subtopic_id = db.Column(db.Integer, db.ForeignKey('syllabus_subtopic.id'), nullable=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    structure_score = db.Column(db.Float, nullable=True)
    content_score = db.Column(db.Float, nullable=True)
    sociological_depth_score = db.Column(db.Float, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    keywords_used = db.Column(db.Text, nullable=True)
    thinkers_mentioned = db.Column(db.Text, nullable=True)
    theories_referenced = db.Column(db.Text, nullable=True)
    topic = db.Column(db.String(100), nullable=True)
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    evaluated_at = db.Column(db.DateTime, nullable=True)

class TopperAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    topper_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    marks_obtained = db.Column(db.Float, nullable=True)
    answer_text = db.Column(db.Text, nullable=False)
    keywords_used = db.Column(db.Text, nullable=True)
    thinkers_mentioned = db.Column(db.Text, nullable=True)
    theories_referenced = db.Column(db.Text, nullable=True)
    word_count = db.Column(db.Integer, nullable=True)
    structure_score = db.Column(db.Float, nullable=True)
    content_depth = db.Column(db.Float, nullable=True)
    sociological_relevance = db.Column(db.Float, nullable=True)
    answer_embedding = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class AnswerSimilarity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    topper_answer_id = db.Column(db.Integer, db.ForeignKey('topper_answer.id'), nullable=False)
    overall_similarity = db.Column(db.Float, nullable=False)
    content_similarity = db.Column(db.Float, nullable=True)
    structure_similarity = db.Column(db.Float, nullable=True)
    keyword_similarity = db.Column(db.Float, nullable=True)
    theory_similarity = db.Column(db.Float, nullable=True)
    feedback_text = db.Column(db.Text, nullable=True)
    improvement_suggestions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()
    
    # Create demo user
    if not User.query.filter_by(username='demo_user').first():
        password_hash = bcrypt.generate_password_hash('demo123').decode('utf-8')
        demo_user = User(username='demo_user', email='demo@sociowizard.com', password_hash=password_hash)
        db.session.add(demo_user)
        db.session.commit()
        print("Demo user created!")
    
    # Add sample questions
    sample_questions = [
        {
            'question_text': 'Discuss the concept of social stratification and its various forms in Indian society.',
            'year': 2023,
            'theme': 'Social Stratification',
            'topic': 'Caste',
            'marks': 10
        },
        {
            'question_text': 'Examine the role of education in social mobility with reference to Indian society.',
            'year': 2022,
            'theme': 'Social Mobility',
            'topic': 'Education',
            'marks': 10
        }
    ]
    
    for q_data in sample_questions:
        if not Question.query.filter_by(question_text=q_data['question_text']).first():
            question = Question(**q_data)
            db.session.add(question)
    
    db.session.commit()
    print("Sample questions added!")
    
    # Seed UPSC CSE Sociology syllabus
    # Seed syllabus data
    try:
        from app.services.syllabus_service import seed_upsc_sociology_syllabus
        seed_upsc_sociology_syllabus()
    except Exception as e:
        print(f"Warning: Could not seed syllabus data: {e}")
        print("You can run reorganize_syllabus_hierarchy.py separately to seed syllabus data.")
    
    print("Database initialized successfully!")

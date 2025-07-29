from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sociowizard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models inline
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    syllabus_topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=True)
    syllabus_subtopic_id = db.Column(db.Integer, db.ForeignKey('syllabus_subtopic.id'), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

def check_database():
    with app.app_context():
        print("=== Database Check ===")
        
        # Check questions
        questions = Question.query.all()
        print(f"Total questions in database: {len(questions)}")
        
        if questions:
            print("\nSample questions:")
            for i, q in enumerate(questions[:3]):
                print(f"{i+1}. {q.question_text[:100]}...")
                print(f"   Theme: {q.theme}, Topic: {q.topic}, Year: {q.year}")
        
        # Check users
        users = User.query.all()
        print(f"\nTotal users in database: {len(users)}")
        
        if users:
            print("Users:")
            for user in users:
                print(f"- {user.username} ({user.email})")
        
        # Check if we can query questions
        try:
            random_q = Question.query.first()
            if random_q:
                print(f"\nFirst question: {random_q.question_text[:50]}...")
            else:
                print("\nNo questions found in database!")
        except Exception as e:
            print(f"\nError querying questions: {e}")

if __name__ == '__main__':
    check_database() 
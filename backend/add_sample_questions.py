from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sociowizard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Question model inline
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Syllabus mapping (without foreign key constraints for standalone script)
    syllabus_topic_id = db.Column(db.Integer, nullable=True)
    syllabus_subtopic_id = db.Column(db.Integer, nullable=True)

def add_sample_questions():
    with app.app_context():
        # Check if questions already exist
        existing_count = Question.query.count()
        if existing_count > 10:
            print(f"Already have {existing_count} questions, skipping...")
            return
        
        sample_questions = [
            {
                'question_text': 'Discuss Karl Marx\'s theory of historical materialism and its relevance in understanding social change.',
                'year': 2023,
                'theme': 'Sociological Thinkers',
                'topic': 'Karl Marx',
                'marks': 10
            },
            {
                'question_text': 'Examine Emile Durkheim\'s concept of social facts and its significance in sociological analysis.',
                'year': 2022,
                'theme': 'Sociological Thinkers',
                'topic': 'Emile Durkheim',
                'marks': 10
            },
            {
                'question_text': 'Analyze Max Weber\'s theory of social action and its application in understanding modern society.',
                'year': 2023,
                'theme': 'Sociological Thinkers',
                'topic': 'Max Weber',
                'marks': 10
            },
            {
                'question_text': 'Discuss the concept of social stratification and its various forms in Indian society.',
                'year': 2022,
                'theme': 'Social Stratification',
                'topic': 'Caste',
                'marks': 10
            },
            {
                'question_text': 'Examine the role of education in social mobility with reference to Indian society.',
                'year': 2023,
                'theme': 'Social Mobility',
                'topic': 'Education',
                'marks': 10
            },
            {
                'question_text': 'Analyze the impact of globalization on Indian society and culture.',
                'year': 2022,
                'theme': 'Social Change',
                'topic': 'Globalization',
                'marks': 10
            },
            {
                'question_text': 'Discuss the changing nature of family structure in contemporary India.',
                'year': 2023,
                'theme': 'Family and Marriage',
                'topic': 'Family Structure',
                'marks': 10
            },
            {
                'question_text': 'Examine the role of women\'s movement in bringing about social change in India.',
                'year': 2022,
                'theme': 'Social Movements',
                'topic': 'Women\'s Movement',
                'marks': 10
            },
            {
                'question_text': 'Analyze the relationship between religion and social change in modern India.',
                'year': 2023,
                'theme': 'Religion and Society',
                'topic': 'Religious Change',
                'marks': 10
            },
            {
                'question_text': 'Discuss the challenges faced by tribal communities in the process of development.',
                'year': 2022,
                'theme': 'Tribal Communities',
                'topic': 'Development Issues',
                'marks': 10
            },
            {
                'question_text': 'Examine the role of caste in contemporary Indian politics.',
                'year': 2023,
                'theme': 'Politics and Society',
                'topic': 'Caste Politics',
                'marks': 10
            },
            {
                'question_text': 'Analyze the impact of urbanization on social structure and relationships.',
                'year': 2022,
                'theme': 'Urban Sociology',
                'topic': 'Urbanization',
                'marks': 10
            },
            {
                'question_text': 'Discuss the concept of social capital and its importance in community development.',
                'year': 2023,
                'theme': 'Social Capital',
                'topic': 'Community Development',
                'marks': 10
            },
            {
                'question_text': 'Examine the role of media in shaping public opinion and social change.',
                'year': 2022,
                'theme': 'Media and Society',
                'topic': 'Media Influence',
                'marks': 10
            },
            {
                'question_text': 'Analyze the challenges of environmental sustainability in the context of social development.',
                'year': 2023,
                'theme': 'Environmental Sociology',
                'topic': 'Sustainability',
                'marks': 10
            }
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            db.session.add(question)
        
        db.session.commit()
        print(f"Added {len(sample_questions)} sample questions successfully!")

if __name__ == '__main__':
    add_sample_questions() 
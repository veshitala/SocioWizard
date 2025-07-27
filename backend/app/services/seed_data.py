import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from app.models.question import Question
from app.models.user import User
from app.models.answer import Answer
from datetime import datetime, timedelta
import random

def seed_sample_data():
    """Seed the database with sample data"""
    
    # Check if data already exists
    if Question.query.first():
        return  # Data already seeded
    
    # Sample PYQs
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
        },
        {
            'question_text': 'Analyze the impact of globalization on Indian family structure and kinship patterns.',
            'year': 2023,
            'theme': 'Social Change',
            'topic': 'Family',
            'marks': 10
        },
        {
            'question_text': 'Discuss the concept of secularization and its relevance in contemporary Indian society.',
            'year': 2022,
            'theme': 'Religion',
            'topic': 'Secularization',
            'marks': 10
        },
        {
            'question_text': 'Examine the relationship between urbanization and social change in India.',
            'year': 2021,
            'theme': 'Urban Sociology',
            'topic': 'Urbanization',
            'marks': 10
        },
        {
            'question_text': 'Discuss the role of mass media in shaping public opinion and social movements.',
            'year': 2023,
            'theme': 'Mass Media',
            'topic': 'Communication',
            'marks': 10
        },
        {
            'question_text': 'Analyze the concept of social capital and its significance in community development.',
            'year': 2022,
            'theme': 'Social Capital',
            'topic': 'Community',
            'marks': 10
        },
        {
            'question_text': 'Examine the challenges of tribal integration in mainstream Indian society.',
            'year': 2021,
            'theme': 'Tribal Sociology',
            'topic': 'Tribal',
            'marks': 10
        },
        {
            'question_text': 'Discuss the impact of technology on social relationships and communication patterns.',
            'year': 2023,
            'theme': 'Technology',
            'topic': 'Digital Society',
            'marks': 10
        },
        {
            'question_text': 'Analyze the role of civil society in promoting social justice and human rights.',
            'year': 2022,
            'theme': 'Civil Society',
            'topic': 'Social Justice',
            'marks': 10
        },
        {
            'question_text': 'Examine the concept of social exclusion and its manifestations in Indian society.',
            'year': 2021,
            'theme': 'Social Exclusion',
            'topic': 'Marginalization',
            'marks': 10
        },
        {
            'question_text': 'Discuss the changing patterns of marriage and family in contemporary India.',
            'year': 2023,
            'theme': 'Marriage and Family',
            'topic': 'Kinship',
            'marks': 10
        },
        {
            'question_text': 'Analyze the role of women in economic development and social transformation.',
            'year': 2022,
            'theme': 'Gender Studies',
            'topic': 'Women Empowerment',
            'marks': 10
        },
        {
            'question_text': 'Examine the impact of migration on social structure and cultural identity.',
            'year': 2021,
            'theme': 'Migration',
            'topic': 'Social Change',
            'marks': 10
        },
        {
            'question_text': 'Discuss the concept of social movements and their role in bringing about social change.',
            'year': 2023,
            'theme': 'Social Movements',
            'topic': 'Collective Action',
            'marks': 10
        }
    ]
    
    # Add questions to database
    for q_data in sample_questions:
        question = Question(**q_data)
        db.session.add(question)
    
    # Create a sample user
    sample_user = User(
        username='demo_user',
        email='demo@sociowizard.com',
        password_hash='hashed_password_placeholder'
    )
    db.session.add(sample_user)
    
    db.session.commit()
    
    # Create some sample answers for the demo user
    sample_answers = [
        {
            'question_id': 1,
            'answer_text': 'Social stratification refers to the hierarchical arrangement of individuals in society based on various criteria such as wealth, power, and prestige. In Indian society, stratification manifests through the caste system, class system, and gender hierarchy. The caste system, based on birth and occupation, has historically been the most prominent form of stratification. However, with modernization and education, class-based stratification is becoming increasingly important. The intersection of caste, class, and gender creates complex patterns of inequality that continue to shape social relations in contemporary India.',
            'structure_score': 8.5,
            'content_score': 7.8,
            'sociological_depth_score': 8.2,
            'overall_score': 8.2,
            'feedback': 'Excellent structure with clear introduction and comprehensive coverage. Good use of sociological concepts like intersectionality.',
            'keywords_used': '["stratification", "caste", "class", "hierarchy", "modernization"]',
            'thinkers_mentioned': '["Weber", "Marx"]',
            'theories_referenced': '["conflict theory"]',
            'topic': 'Caste',
            'submitted_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'question_id': 2,
            'answer_text': 'Education plays a crucial role in social mobility by providing individuals with knowledge, skills, and credentials necessary for upward mobility. In India, education has been a key factor in breaking traditional barriers of caste and class. However, access to quality education remains unequal, with rural areas and marginalized communities facing significant challenges. The reservation system in educational institutions has helped promote social justice, but more comprehensive reforms are needed to ensure equal opportunities for all.',
            'structure_score': 7.5,
            'content_score': 8.0,
            'sociological_depth_score': 7.8,
            'overall_score': 7.8,
            'feedback': 'Good content with relevant examples. Could improve structure with better transitions between paragraphs.',
            'keywords_used': '["education", "mobility", "caste", "class", "reservation"]',
            'thinkers_mentioned': '["Durkheim"]',
            'theories_referenced': '["structural functionalism"]',
            'topic': 'Education',
            'submitted_at': datetime.utcnow() - timedelta(days=3)
        }
    ]
    
    for a_data in sample_answers:
        answer = Answer(
            user_id=sample_user.id,
            **a_data
        )
        db.session.add(answer)
    
    db.session.commit()
    
    print("Sample data seeded successfully!") 
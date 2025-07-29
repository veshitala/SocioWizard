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

def seed_syllabus():
    with app.app_context():
        # Check if syllabus already exists
        if SyllabusTopic.query.first():
            print("Syllabus already exists, skipping seeding...")
            return
        
        # Paper 1 - Fundamentals of Sociology
        paper1 = SyllabusTopic(
            name="Paper 1 - Fundamentals of Sociology",
            code="PAPER1",
            description="Sociological Thinkers, Research Methods, and Basic Concepts",
            weightage=1.0,
            order_index=1
        )
        db.session.add(paper1)
        db.session.flush()
        
        # Add some key subtopics for Paper 1
        paper1_subtopics = [
            SyllabusSubtopic(name="Karl Marx", code="PAPER1_4.1", 
                            description="Historical materialism, mode of production, alienation, class struggle", 
                            weightage=1.0, order_index=1, topic_id=paper1.id),
            SyllabusSubtopic(name="Emile Durkheim", code="PAPER1_4.2", 
                            description="Division of labour, social fact, suicide, religion and society", 
                            weightage=1.0, order_index=2, topic_id=paper1.id),
            SyllabusSubtopic(name="Max Weber", code="PAPER1_4.3", 
                            description="Social action, ideal types, authority, bureaucracy, protestant ethic", 
                            weightage=1.0, order_index=3, topic_id=paper1.id),
            SyllabusSubtopic(name="Social Stratification", code="PAPER1_5.1", 
                            description="Equality, inequality, hierarchy, exclusion, poverty and deprivation", 
                            weightage=0.9, order_index=4, topic_id=paper1.id),
            SyllabusSubtopic(name="Social Mobility", code="PAPER1_5.2", 
                            description="Open and closed systems, types of mobility, sources and causes", 
                            weightage=0.8, order_index=5, topic_id=paper1.id),
        ]
        
        for subtopic in paper1_subtopics:
            db.session.add(subtopic)
        
        # Paper 2 - Indian Society: Structure and Change
        paper2 = SyllabusTopic(
            name="Paper 2 - Indian Society: Structure and Change",
            code="PAPER2",
            description="Indian Society, Social Structure, and Contemporary Issues",
            weightage=1.0,
            order_index=2
        )
        db.session.add(paper2)
        db.session.flush()
        
        # Add some key subtopics for Paper 2
        paper2_subtopics = [
            SyllabusSubtopic(name="Caste System", code="PAPER2_2.1", 
                            description="Caste system: Perspectives on the study of caste systems", 
                            weightage=1.0, order_index=1, topic_id=paper2.id),
            SyllabusSubtopic(name="Tribal Communities", code="PAPER2_2.2", 
                            description="Tribal communities in India", 
                            weightage=0.8, order_index=2, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Classes", code="PAPER2_2.3", 
                            description="Social classes in India", 
                            weightage=0.8, order_index=3, topic_id=paper2.id),
            SyllabusSubtopic(name="Women's Movement", code="PAPER2_5.1", 
                            description="Women's movement in India", 
                            weightage=0.8, order_index=4, topic_id=paper2.id),
            SyllabusSubtopic(name="Globalization", code="PAPER2_3.1", 
                            description="Globalization and social change", 
                            weightage=0.8, order_index=5, topic_id=paper2.id),
        ]
        
        for subtopic in paper2_subtopics:
            db.session.add(subtopic)
        
        db.session.commit()
        print("UPSC CSE Sociology syllabus seeded successfully!")
        print(f"Created {SyllabusTopic.query.count()} topics and {SyllabusSubtopic.query.count()} subtopics")

if __name__ == '__main__':
    seed_syllabus() 
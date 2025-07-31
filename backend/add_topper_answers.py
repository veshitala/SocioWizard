#!/usr/bin/env python3
"""
Script to add sample topper answers for testing similarity analysis
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import create_app from app.py
import app as flask_app_module
from extensions import db
from app.models.topper_answer import TopperAnswer
from app.models.question import Question
from app.services.similarity_service import SimilarityAnalysisService
import json

def add_sample_topper_answers():
    """Add sample topper answers to the database"""
    # Import create_app function from app.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    flask_app = app_module.create_app()
    
    with flask_app.app_context():
        # Initialize similarity service
        similarity_service = SimilarityAnalysisService()
        
        # Sample topper answers for different questions
        topper_answers_data = [
            {
                'question_id': 1,
                'topper_name': 'Priya Sharma',
                'year': 2023,
                'rank': 15,
                'marks_obtained': 145,
                'answer_text': '''The emergence of sociology as a discipline was deeply rooted in the social changes that swept through Europe during the 18th and 19th centuries. The Industrial Revolution, urbanization, and the French Revolution created unprecedented social upheaval that demanded systematic study.

Auguste Comte, often called the father of sociology, coined the term "sociology" and emphasized the need for a scientific approach to understanding society. He believed that society could be studied using the same methods as natural sciences, leading to the development of positivism.

The scope of sociology encompasses the study of social institutions, social relationships, social change, and social problems. Unlike other social sciences, sociology takes a holistic view of society, examining how various institutions interact and influence each other. While economics focuses on production and distribution, political science on governance, and psychology on individual behavior, sociology examines the social context that shapes all these phenomena.

Sociology differs from common sense in its systematic approach, empirical methodology, and theoretical framework. Common sense relies on personal experience and anecdotal evidence, while sociology uses rigorous research methods, statistical analysis, and peer-reviewed studies to understand social phenomena. For example, while common sense might suggest that poverty is due to individual laziness, sociological research reveals the complex interplay of structural factors like education, discrimination, and economic policies.'''
            },
            {
                'question_id': 2,
                'topper_name': 'Rahul Verma',
                'year': 2022,
                'rank': 8,
                'marks_obtained': 152,
                'answer_text': '''Sociology as a science follows the scientific method, emphasizing empirical observation, hypothesis testing, and systematic analysis. The major theoretical strands include functionalism, conflict theory, and symbolic interactionism, each offering different perspectives on social phenomena.

Positivism, developed by Auguste Comte, advocates for applying natural science methods to social research. However, this approach has been critiqued for its assumption that social reality can be objectively measured and for ignoring the subjective meanings that individuals attach to their actions.

The fact-value distinction is crucial in sociological research. Facts are objective, observable phenomena, while values are subjective beliefs about what should be. Max Weber emphasized the importance of value neutrality in research, though complete objectivity may be impossible to achieve.

Non-positivist methodologies, including interpretivism and critical theory, emphasize understanding social meaning and challenging power structures. These approaches recognize that social reality is constructed through human interaction and cannot be reduced to measurable variables alone.'''
            },
            {
                'question_id': 3,
                'topper_name': 'Anjali Patel',
                'year': 2021,
                'rank': 12,
                'marks_obtained': 148,
                'answer_text': '''Research methods in sociology can be broadly classified into qualitative and quantitative approaches. Qualitative methods focus on understanding meaning and context through methods like ethnography, interviews, and case studies. Quantitative methods emphasize measurement and statistical analysis through surveys and experiments.

Data collection techniques include participant observation, structured interviews, questionnaires, and secondary data analysis. Each method has its strengths and limitations, and the choice depends on the research question and available resources.

Key concepts in research include variables (characteristics that vary), sampling (selecting a representative subset), hypothesis (testable predictions), reliability (consistency of measurement), and validity (accuracy of measurement). These concepts ensure that research findings are credible and generalizable.

The choice between qualitative and quantitative methods depends on the research question, theoretical framework, and practical considerations. Mixed methods research combines both approaches to provide a more comprehensive understanding of social phenomena.'''
            },
            {
                'question_id': 4,
                'topper_name': 'Vikram Singh',
                'year': 2023,
                'rank': 5,
                'marks_obtained': 158,
                'answer_text': '''Karl Marx's historical materialism posits that material conditions determine social structure and historical development. His analysis of capitalism reveals how the mode of production creates class divisions between bourgeoisie and proletariat, leading to alienation and class struggle.

Emile Durkheim's concept of social facts emphasizes that social phenomena exist independently of individuals and exert external constraint. His study of suicide demonstrated how social integration and regulation affect individual behavior, while his analysis of religion showed its role in maintaining social solidarity.

Max Weber's concept of social action focuses on the subjective meanings that individuals attach to their behavior. His ideal types are analytical constructs that help understand complex social phenomena. His analysis of bureaucracy and authority, along with his study of the Protestant ethic, revealed the relationship between religion and economic development.

Robert K. Merton's distinction between manifest and latent functions shows how social institutions have both intended and unintended consequences. His work on deviance and reference groups expanded our understanding of social behavior and group influence.'''
            },
            {
                'question_id': 5,
                'topper_name': 'Meera Reddy',
                'year': 2022,
                'rank': 10,
                'marks_obtained': 150,
                'answer_text': '''Social stratification refers to the hierarchical arrangement of individuals and groups in society based on various criteria. The structural functionalist theory, advocated by Davis and Moore, argues that stratification is necessary for society to function effectively, as it ensures that the most talented individuals fill the most important positions.

Marxist theory views stratification as a result of class conflict, where the bourgeoisie exploits the proletariat through control of the means of production. This creates a fundamental division between those who own capital and those who must sell their labor.

Weberian theory introduces a three-dimensional view of stratification: class (economic position), status (social prestige), and party (political power). This approach recognizes that individuals can have high standing in one dimension while being low in others.

Social mobility, the movement between social positions, can be open (based on achievement) or closed (based on ascription). Types of mobility include horizontal (same level), vertical (up or down), and intergenerational (between generations). Factors affecting mobility include education, economic opportunities, and social policies.'''
            }
        ]
        
        # Check if topper answers already exist
        existing_count = TopperAnswer.query.count()
        if existing_count > 0:
            print(f"Found {existing_count} existing topper answers. Skipping addition.")
            return
        
        print("Adding sample topper answers...")
        
        for answer_data in topper_answers_data:
            try:
                # Check if question exists
                question = Question.query.get(answer_data['question_id'])
                if not question:
                    print(f"Question {answer_data['question_id']} not found, skipping...")
                    continue
                
                # Add topper answer using the service
                result = similarity_service.add_topper_answer(
                    question_id=answer_data['question_id'],
                    topper_name=answer_data['topper_name'],
                    year=answer_data['year'],
                    answer_text=answer_data['answer_text'],
                    rank=answer_data['rank'],
                    marks=answer_data['marks_obtained']
                )
                
                if 'success' in result:
                    print(f"✓ Added topper answer for {answer_data['topper_name']} (Question {answer_data['question_id']})")
                else:
                    print(f"✗ Failed to add topper answer: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"✗ Error adding topper answer: {e}")
        
        print(f"\nTotal topper answers in database: {TopperAnswer.query.count()}")

if __name__ == '__main__':
    add_sample_topper_answers() 
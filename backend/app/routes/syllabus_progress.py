from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.answer import Answer
from app.models.syllabus import SyllabusTopic, SyllabusSubtopic
from app.models.question import Question
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import json

syllabus_progress_bp = Blueprint('syllabus_progress', __name__)

@syllabus_progress_bp.route('/syllabus-overview', methods=['GET'])
@jwt_required()
def get_syllabus_overview():
    """Get overall syllabus progress overview with proper hierarchy"""
    user_id = get_jwt_identity()
    
    try:
        # Get all topics grouped by paper
        paper1_topics = SyllabusTopic.query.filter_by(paper='PAPER1').order_by(SyllabusTopic.order_index).all()
        paper2_topics = SyllabusTopic.query.filter_by(paper='PAPER2').order_by(SyllabusTopic.order_index).all()
        
        syllabus_overview = []
        total_questions_answered = 0
        total_possible_questions = 0
        
        # Process Paper 1 topics
        paper1_data = []
        for topic in paper1_topics:
            # Get questions answered for this topic
            answered_questions = db.session.query(func.count(Answer.id)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_topic_id == topic.id
                )
            ).scalar()
            
            # Get average score for this topic
            avg_score = db.session.query(func.avg(Answer.overall_score)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_topic_id == topic.id
                )
            ).scalar()
            
            # Calculate progress percentage (assuming 10 questions per subtopic as target)
            total_subtopics = len(topic.subtopics)
            target_questions = total_subtopics * 10  # 10 questions per subtopic
            progress_percentage = min((answered_questions / target_questions * 100) if target_questions > 0 else 0, 100)
            
            topic_data = {
                'id': topic.id,
                'name': topic.name,
                'code': topic.code,
                'description': topic.description,
                'weightage': topic.weightage,
                'paper': topic.paper,
                'subtopics_count': total_subtopics,
                'questions_answered': answered_questions,
                'target_questions': target_questions,
                'progress_percentage': round(progress_percentage, 1),
                'average_score': round(avg_score, 2) if avg_score else 0,
                'strength_level': get_strength_level(avg_score) if avg_score else 'not_started'
            }
            
            paper1_data.append(topic_data)
            total_questions_answered += answered_questions
            total_possible_questions += target_questions
        
        # Process Paper 2 topics
        paper2_data = []
        for topic in paper2_topics:
            # Get questions answered for this topic
            answered_questions = db.session.query(func.count(Answer.id)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_topic_id == topic.id
                )
            ).scalar()
            
            # Get average score for this topic
            avg_score = db.session.query(func.avg(Answer.overall_score)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_topic_id == topic.id
                )
            ).scalar()
            
            # Calculate progress percentage (assuming 10 questions per subtopic as target)
            total_subtopics = len(topic.subtopics)
            target_questions = total_subtopics * 10  # 10 questions per subtopic
            progress_percentage = min((answered_questions / target_questions * 100) if target_questions > 0 else 0, 100)
            
            topic_data = {
                'id': topic.id,
                'name': topic.name,
                'code': topic.code,
                'description': topic.description,
                'weightage': topic.weightage,
                'paper': topic.paper,
                'subtopics_count': total_subtopics,
                'questions_answered': answered_questions,
                'target_questions': target_questions,
                'progress_percentage': round(progress_percentage, 1),
                'average_score': round(avg_score, 2) if avg_score else 0,
                'strength_level': get_strength_level(avg_score) if avg_score else 'not_started'
            }
            
            paper2_data.append(topic_data)
            total_questions_answered += answered_questions
            total_possible_questions += target_questions
        
        # Overall progress
        overall_progress = min((total_questions_answered / total_possible_questions * 100) if total_possible_questions > 0 else 0, 100)
        
        return jsonify({
            'syllabus_overview': {
                'paper1': {
                    'name': 'Paper 1 - Fundamentals of Sociology',
                    'topics': paper1_data
                },
                'paper2': {
                    'name': 'Paper 2 - Indian Society: Structure and Change',
                    'topics': paper2_data
                }
            },
            'overall_progress': round(overall_progress, 1),
            'total_questions_answered': total_questions_answered,
            'total_possible_questions': total_possible_questions
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve syllabus overview'}), 500

@syllabus_progress_bp.route('/topic/<int:topic_id>/subtopics', methods=['GET'])
@jwt_required()
def get_topic_subtopics_progress(topic_id):
    """Get detailed progress for a specific topic and its subtopics"""
    user_id = get_jwt_identity()
    
    try:
        topic = SyllabusTopic.query.get_or_404(topic_id)
        subtopics = SyllabusSubtopic.query.filter_by(topic_id=topic_id).order_by(SyllabusSubtopic.order_index).all()
        
        subtopics_progress = []
        
        for subtopic in subtopics:
            # Get questions answered for this subtopic
            answered_questions = db.session.query(func.count(Answer.id)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_subtopic_id == subtopic.id
                )
            ).scalar()
            
            # Get average score for this subtopic
            avg_score = db.session.query(func.avg(Answer.overall_score)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_subtopic_id == subtopic.id
                )
            ).scalar()
            
            # Get recent answers for this subtopic
            recent_answers = db.session.query(Answer).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_subtopic_id == subtopic.id
                )
            ).order_by(Answer.submitted_at.desc()).limit(3).all()
            
            # Calculate progress percentage
            target_questions = 10  # Target 10 questions per subtopic
            progress_percentage = min((answered_questions / target_questions * 100) if target_questions > 0 else 0, 100)
            
            subtopic_data = {
                'id': subtopic.id,
                'name': subtopic.name,
                'code': subtopic.code,
                'description': subtopic.description,
                'weightage': subtopic.weightage,
                'questions_answered': answered_questions,
                'target_questions': target_questions,
                'progress_percentage': round(progress_percentage, 1),
                'average_score': round(avg_score, 2) if avg_score else 0,
                'strength_level': get_strength_level(avg_score) if avg_score else 'not_started',
                'recent_answers': [
                    {
                        'id': answer.id,
                        'score': answer.overall_score,
                        'submitted_at': answer.submitted_at.isoformat(),
                        'question_text': answer.question.question_text[:100] + '...' if len(answer.question.question_text) > 100 else answer.question.question_text
                    } for answer in recent_answers
                ]
            }
            
            subtopics_progress.append(subtopic_data)
        
        return jsonify({
            'topic': topic.to_dict(),
            'subtopics_progress': subtopics_progress
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve topic progress'}), 500

@syllabus_progress_bp.route('/strength-analysis', methods=['GET'])
@jwt_required()
def get_strength_analysis():
    """Get strength analysis across all topics"""
    user_id = get_jwt_identity()
    
    try:
        # Get all topics with their strength levels
        topics = SyllabusTopic.query.order_by(SyllabusTopic.order_index).all()
        
        strength_analysis = {
            'strong_topics': [],
            'moderate_topics': [],
            'weak_topics': [],
            'not_started_topics': []
        }
        
        for topic in topics:
            # Get average score for this topic
            avg_score = db.session.query(func.avg(Answer.overall_score)).join(
                Question, Answer.question_id == Question.id
            ).filter(
                and_(
                    Answer.user_id == user_id,
                    Question.syllabus_topic_id == topic.id
                )
            ).scalar()
            
            topic_data = {
                'id': topic.id,
                'name': topic.name,
                'code': topic.code,
                'average_score': round(avg_score, 2) if avg_score else 0
            }
            
            if not avg_score:
                strength_analysis['not_started_topics'].append(topic_data)
            elif avg_score >= 8.0:
                strength_analysis['strong_topics'].append(topic_data)
            elif avg_score >= 6.0:
                strength_analysis['moderate_topics'].append(topic_data)
            else:
                strength_analysis['weak_topics'].append(topic_data)
        
        return jsonify(strength_analysis), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve strength analysis'}), 500

@syllabus_progress_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get personalized recommendations based on syllabus progress"""
    user_id = get_jwt_identity()
    
    try:
        recommendations = []
        
        # Get weak topics (score < 6.0)
        weak_topics = db.session.query(
            SyllabusTopic.name,
            func.avg(Answer.overall_score).label('avg_score')
        ).join(
            Question, SyllabusTopic.id == Question.syllabus_topic_id
        ).join(
            Answer, Question.id == Answer.question_id
        ).filter(
            Answer.user_id == user_id
        ).group_by(
            SyllabusTopic.id, SyllabusTopic.name
        ).having(
            func.avg(Answer.overall_score) < 6.0
        ).order_by(
            func.avg(Answer.overall_score)
        ).limit(3).all()
        
        for topic in weak_topics:
            recommendations.append({
                'type': 'focus_area',
                'title': f'Focus on {topic.name}',
                'description': f'Your average score in {topic.name} is {topic.avg_score:.1f}. Consider practicing more questions in this area.',
                'priority': 'high'
            })
        
        # Get topics with few questions answered
        low_practice_topics = db.session.query(
            SyllabusTopic.name,
            func.count(Answer.id).label('questions_count')
        ).join(
            Question, SyllabusTopic.id == Question.syllabus_topic_id
        ).join(
            Answer, Question.id == Answer.question_id
        ).filter(
            Answer.user_id == user_id
        ).group_by(
            SyllabusTopic.id, SyllabusTopic.name
        ).having(
            func.count(Answer.id) < 5
        ).order_by(
            func.count(Answer.id)
        ).limit(3).all()
        
        for topic in low_practice_topics:
            recommendations.append({
                'type': 'practice_more',
                'title': f'Practice More in {topic.name}',
                'description': f'You have only answered {topic.questions_count} questions in {topic.name}. Try to practice more questions.',
                'priority': 'medium'
            })
        
        # Get strong topics for confidence building
        strong_topics = db.session.query(
            SyllabusTopic.name,
            func.avg(Answer.overall_score).label('avg_score')
        ).join(
            Question, SyllabusTopic.id == Question.syllabus_topic_id
        ).join(
            Answer, Question.id == Answer.question_id
        ).filter(
            Answer.user_id == user_id
        ).group_by(
            SyllabusTopic.id, SyllabusTopic.name
        ).having(
            func.avg(Answer.overall_score) >= 8.0
        ).order_by(
            func.avg(Answer.overall_score).desc()
        ).limit(2).all()
        
        for topic in strong_topics:
            recommendations.append({
                'type': 'strength',
                'title': f'Strong Performance in {topic.name}',
                'description': f'Excellent work! Your average score in {topic.name} is {topic.avg_score:.1f}. Keep up the good work!',
                'priority': 'low'
            })
        
        return jsonify({
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve recommendations'}), 500

def get_strength_level(score):
    """Convert score to strength level"""
    if not score:
        return 'not_started'
    elif score >= 8.0:
        return 'strong'
    elif score >= 6.0:
        return 'moderate'
    else:
        return 'weak' 
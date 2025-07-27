from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.answer import Answer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta
import json

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_progress_summary():
    """Get overall progress summary"""
    user_id = get_jwt_identity()
    
    try:
        # Total answers submitted
        total_answers = Answer.query.filter_by(user_id=user_id).count()
        
        # Average scores
        avg_scores = db.session.query(
            func.avg(Answer.structure_score).label('avg_structure'),
            func.avg(Answer.content_score).label('avg_content'),
            func.avg(Answer.sociological_depth_score).label('avg_depth'),
            func.avg(Answer.overall_score).label('avg_overall')
        ).filter_by(user_id=user_id).first()
        
        # Topics practiced
        topics = db.session.query(Answer.topic).filter_by(user_id=user_id).distinct().count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_answers = Answer.query.filter(
            Answer.user_id == user_id,
            Answer.submitted_at >= week_ago
        ).count()
        
        # Best performing topic
        topic_performance = db.session.query(
            Answer.topic,
            func.avg(Answer.overall_score).label('avg_score')
        ).filter_by(user_id=user_id).group_by(Answer.topic).order_by(
            func.avg(Answer.overall_score).desc()
        ).first()
        
        return jsonify({
            'summary': {
                'total_answers': total_answers,
                'topics_practiced': topics,
                'recent_answers': recent_answers,
                'average_scores': {
                    'structure': round(avg_scores.avg_structure, 2) if avg_scores.avg_structure else 0,
                    'content': round(avg_scores.avg_content, 2) if avg_scores.avg_content else 0,
                    'sociological_depth': round(avg_scores.avg_depth, 2) if avg_scores.avg_depth else 0,
                    'overall': round(avg_scores.avg_overall, 2) if avg_scores.avg_overall else 0
                },
                'best_topic': {
                    'name': topic_performance.topic if topic_performance else None,
                    'score': round(topic_performance.avg_score, 2) if topic_performance else 0
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve progress summary'}), 500

@progress_bp.route('/timeline', methods=['GET'])
@jwt_required()
def get_progress_timeline():
    """Get progress timeline data"""
    user_id = get_jwt_identity()
    
    try:
        # Get query parameters
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get answers grouped by date
        timeline_data = db.session.query(
            func.date(Answer.submitted_at).label('date'),
            func.count(Answer.id).label('answers_count'),
            func.avg(Answer.overall_score).label('avg_score')
        ).filter(
            Answer.user_id == user_id,
            Answer.submitted_at >= start_date
        ).group_by(func.date(Answer.submitted_at)).order_by(
            func.date(Answer.submitted_at)
        ).all()
        
        timeline = []
        for data in timeline_data:
            timeline.append({
                'date': data.date.isoformat(),
                'answers_count': data.answers_count,
                'average_score': round(data.avg_score, 2) if data.avg_score else 0
            })
        
        return jsonify({
            'timeline': timeline
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve timeline data'}), 500

@progress_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_topic_progress():
    """Get progress by topic"""
    user_id = get_jwt_identity()
    
    try:
        topic_progress = db.session.query(
            Answer.topic,
            func.count(Answer.id).label('answers_count'),
            func.avg(Answer.overall_score).label('avg_score'),
            func.avg(Answer.structure_score).label('avg_structure'),
            func.avg(Answer.content_score).label('avg_content'),
            func.avg(Answer.sociological_depth_score).label('avg_depth')
        ).filter_by(user_id=user_id).group_by(Answer.topic).all()
        
        topics = []
        for data in topic_progress:
            topics.append({
                'topic': data.topic,
                'answers_count': data.answers_count,
                'average_scores': {
                    'overall': round(data.avg_score, 2) if data.avg_score else 0,
                    'structure': round(data.avg_structure, 2) if data.avg_structure else 0,
                    'content': round(data.avg_content, 2) if data.avg_content else 0,
                    'sociological_depth': round(data.avg_depth, 2) if data.avg_depth else 0
                }
            })
        
        return jsonify({
            'topics': topics
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve topic progress'}), 500

@progress_bp.route('/streak', methods=['GET'])
@jwt_required()
def get_streak():
    """Get current practice streak"""
    user_id = get_jwt_identity()
    
    try:
        # Get all answer dates
        answer_dates = db.session.query(
            func.date(Answer.submitted_at).label('date')
        ).filter_by(user_id=user_id).distinct().order_by(
            func.date(Answer.submitted_at).desc()
        ).all()
        
        if not answer_dates:
            return jsonify({'streak': 0}), 200
        
        # Calculate streak
        streak = 0
        current_date = datetime.utcnow().date()
        
        for i, data in enumerate(answer_dates):
            answer_date = data.date
            expected_date = current_date - timedelta(days=i)
            
            if answer_date == expected_date:
                streak += 1
            else:
                break
        
        return jsonify({
            'streak': streak
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to calculate streak'}), 500 
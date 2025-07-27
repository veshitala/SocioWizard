from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.answer import Answer
from app.models.question import Question
from app.services.evaluation_service import evaluate_answer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from datetime import datetime
import json

answers_bp = Blueprint('answers', __name__)

@answers_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_answer():
    """Submit an answer for evaluation"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['question_id', 'answer_text']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    question_id = data['question_id']
    answer_text = data['answer_text']
    file_path = data.get('file_path')
    topic = data.get('topic')
    
    # Verify question exists
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    try:
        # Create new answer
        new_answer = Answer(
            user_id=user_id,
            question_id=question_id,
            answer_text=answer_text,
            file_path=file_path,
            topic=topic or question.topic
        )
        
        db.session.add(new_answer)
        db.session.commit()
        
        # Evaluate the answer (placeholder for now)
        evaluation_result = evaluate_answer(answer_text, question)
        
        # Update answer with evaluation results
        new_answer.structure_score = evaluation_result['structure_score']
        new_answer.content_score = evaluation_result['content_score']
        new_answer.sociological_depth_score = evaluation_result['sociological_depth_score']
        new_answer.overall_score = evaluation_result['overall_score']
        new_answer.feedback = evaluation_result['feedback']
        new_answer.keywords_used = json.dumps(evaluation_result['keywords_used'])
        new_answer.thinkers_mentioned = json.dumps(evaluation_result['thinkers_mentioned'])
        new_answer.theories_referenced = json.dumps(evaluation_result['theories_referenced'])
        new_answer.evaluated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Answer submitted and evaluated successfully',
            'answer': new_answer.to_dict(),
            'evaluation': evaluation_result
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit answer'}), 500

@answers_bp.route('/history', methods=['GET'])
@jwt_required()
def get_answer_history():
    """Get user's answer history"""
    user_id = get_jwt_identity()
    
    try:
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        topic = request.args.get('topic')
        
        query = Answer.query.filter_by(user_id=user_id)
        
        if topic:
            query = query.filter(Answer.topic == topic)
        
        answers = query.order_by(Answer.submitted_at.desc()).offset(offset).limit(limit).all()
        
        # Include question details
        answer_data = []
        for answer in answers:
            answer_dict = answer.to_dict()
            answer_dict['question'] = answer.question.to_dict()
            answer_data.append(answer_dict)
        
        return jsonify({
            'answers': answer_data,
            'count': len(answer_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve answer history'}), 500

@answers_bp.route('/<int:answer_id>', methods=['GET'])
@jwt_required()
def get_answer(answer_id):
    """Get specific answer details"""
    user_id = get_jwt_identity()
    
    try:
        answer = Answer.query.filter_by(id=answer_id, user_id=user_id).first()
        
        if not answer:
            return jsonify({'error': 'Answer not found'}), 404
        
        answer_dict = answer.to_dict()
        answer_dict['question'] = answer.question.to_dict()
        
        return jsonify({
            'answer': answer_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve answer'}), 500

@answers_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_user_topics():
    """Get topics the user has practiced"""
    user_id = get_jwt_identity()
    
    try:
        topics = db.session.query(Answer.topic).filter_by(user_id=user_id).distinct().all()
        topic_list = [topic[0] for topic in topics if topic[0]]
        
        return jsonify({
            'topics': topic_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve topics'}), 500 
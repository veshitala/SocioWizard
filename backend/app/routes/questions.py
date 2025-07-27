from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.question import Question
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
import random

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/random', methods=['GET'])
@jwt_required()
def get_random_question():
    """Get a random PYQ for practice"""
    try:
        # Get query parameters for filtering
        theme = request.args.get('theme')
        topic = request.args.get('topic')
        year = request.args.get('year')
        
        # Build query
        query = Question.query
        
        if theme:
            query = query.filter(Question.theme == theme)
        if topic:
            query = query.filter(Question.topic == topic)
        if year:
            query = query.filter(Question.year == int(year))
        
        # Get all questions matching criteria
        questions = query.all()
        
        if not questions:
            return jsonify({'error': 'No questions found with the specified criteria'}), 404
        
        # Select random question
        random_question = random.choice(questions)
        
        return jsonify({
            'question': random_question.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve question'}), 500

@questions_bp.route('/themes', methods=['GET'])
@jwt_required()
def get_themes():
    """Get all available themes"""
    try:
        themes = db.session.query(Question.theme).distinct().all()
        theme_list = [theme[0] for theme in themes]
        
        return jsonify({
            'themes': theme_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve themes'}), 500

@questions_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_topics():
    """Get all available topics"""
    try:
        topics = db.session.query(Question.topic).distinct().all()
        topic_list = [topic[0] for topic in topics]
        
        return jsonify({
            'topics': topic_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve topics'}), 500

@questions_bp.route('/years', methods=['GET'])
@jwt_required()
def get_years():
    """Get all available years"""
    try:
        years = db.session.query(Question.year).distinct().order_by(Question.year.desc()).all()
        year_list = [year[0] for year in years]
        
        return jsonify({
            'years': year_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve years'}), 500

@questions_bp.route('/search', methods=['GET'])
@jwt_required()
def search_questions():
    """Search questions with filters"""
    try:
        theme = request.args.get('theme')
        topic = request.args.get('topic')
        year = request.args.get('year')
        limit = request.args.get('limit', 10, type=int)
        
        query = Question.query
        
        if theme:
            query = query.filter(Question.theme == theme)
        if topic:
            query = query.filter(Question.topic == topic)
        if year:
            query = query.filter(Question.year == int(year))
        
        questions = query.limit(limit).all()
        
        return jsonify({
            'questions': [q.to_dict() for q in questions],
            'count': len(questions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to search questions'}), 500 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.similarity_service import SimilarityAnalysisService
from app.models.topper_answer import TopperAnswer, AnswerSimilarity
from app.models.answer import Answer
from extensions import db
import json

topper_analysis_bp = Blueprint('topper_analysis', __name__, url_prefix='/api/topper-analysis')
similarity_service = SimilarityAnalysisService()

@topper_analysis_bp.route('/analyze/<int:answer_id>', methods=['GET'])
@jwt_required()
def analyze_answer(answer_id):
    """Analyze a user answer against topper answers"""
    try:
        user_id = get_jwt_identity()
        
        # Verify the answer belongs to the user
        user_answer = Answer.query.filter_by(id=answer_id, user_id=user_id).first()
        if not user_answer:
            return jsonify({'error': 'Answer not found or access denied'}), 404
        
        # Check if analysis already exists
        existing_analysis = AnswerSimilarity.query.filter_by(user_answer_id=answer_id).first()
        if existing_analysis:
            # Return existing analysis
            topper_answer = TopperAnswer.query.get(existing_analysis.topper_answer_id)
            return jsonify({
                'similarity_analysis': {
                    'overall_similarity': existing_analysis.overall_similarity,
                    'content_similarity': existing_analysis.content_similarity,
                    'keyword_similarity': existing_analysis.keyword_similarity,
                    'structure_similarity': existing_analysis.structure_similarity,
                    'theory_similarity': existing_analysis.theory_similarity
                },
                'topper_answer': topper_answer.to_dict() if topper_answer else None,
                'feedback': {
                    'text': existing_analysis.feedback_text,
                    'suggestions': json.loads(existing_analysis.improvement_suggestions) if existing_analysis.improvement_suggestions else []
                }
            }), 200
        
        # Perform new analysis
        analysis_result = similarity_service.analyze_user_answer(answer_id)
        
        if 'error' in analysis_result:
            return jsonify(analysis_result), 400
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        print(f"Error in analyze_answer: {e}")
        return jsonify({'error': 'Failed to analyze answer'}), 500

@topper_analysis_bp.route('/add-topper-answer', methods=['POST'])
@jwt_required()
def add_topper_answer():
    """Add a new topper answer (admin function)"""
    try:
        data = request.get_json()
        
        required_fields = ['question_id', 'topper_name', 'year', 'answer_text']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = similarity_service.add_topper_answer(
            question_id=data['question_id'],
            topper_name=data['topper_name'],
            year=data['year'],
            answer_text=data['answer_text'],
            rank=data.get('rank'),
            marks=data.get('marks_obtained')
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        print(f"Error in add_topper_answer: {e}")
        return jsonify({'error': 'Failed to add topper answer'}), 500

@topper_analysis_bp.route('/topper-answers/<int:question_id>', methods=['GET'])
@jwt_required()
def get_topper_answers(question_id):
    """Get all topper answers for a specific question"""
    try:
        topper_answers = TopperAnswer.query.filter_by(question_id=question_id).order_by(TopperAnswer.year.desc()).all()
        
        return jsonify({
            'topper_answers': [answer.to_dict() for answer in topper_answers]
        }), 200
        
    except Exception as e:
        print(f"Error in get_topper_answers: {e}")
        return jsonify({'error': 'Failed to retrieve topper answers'}), 500

@topper_analysis_bp.route('/user-analysis-history', methods=['GET'])
@jwt_required()
def get_user_analysis_history():
    """Get analysis history for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's answers with similarity analysis
        analyses = db.session.query(AnswerSimilarity, TopperAnswer, Answer).join(
            TopperAnswer, AnswerSimilarity.topper_answer_id == TopperAnswer.id
        ).join(
            Answer, AnswerSimilarity.user_answer_id == Answer.id
        ).filter(
            Answer.user_id == user_id
        ).order_by(AnswerSimilarity.created_at.desc()).limit(10).all()
        
        history = []
        for analysis, topper_answer, user_answer in analyses:
            history.append({
                'analysis_id': analysis.id,
                'user_answer_id': analysis.user_answer_id,
                'user_answer_preview': user_answer.answer_text[:100] + '...' if len(user_answer.answer_text) > 100 else user_answer.answer_text,
                'topper_answer': topper_answer.to_dict(),
                'similarity_scores': {
                    'overall_similarity': analysis.overall_similarity,
                    'content_similarity': analysis.content_similarity,
                    'keyword_similarity': analysis.keyword_similarity,
                    'structure_similarity': analysis.structure_similarity,
                    'theory_similarity': analysis.theory_similarity
                },
                'feedback': {
                    'text': analysis.feedback_text,
                    'suggestions': json.loads(analysis.improvement_suggestions) if analysis.improvement_suggestions else []
                },
                'analyzed_at': analysis.created_at.isoformat()
            })
        
        return jsonify({
            'analysis_history': history
        }), 200
        
    except Exception as e:
        print(f"Error in get_user_analysis_history: {e}")
        return jsonify({'error': 'Failed to retrieve analysis history'}), 500

@topper_analysis_bp.route('/similarity-stats', methods=['GET'])
@jwt_required()
def get_similarity_stats():
    """Get similarity statistics for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get all analyses for the user
        analyses = db.session.query(AnswerSimilarity).join(
            Answer, AnswerSimilarity.user_answer_id == Answer.id
        ).filter(
            Answer.user_id == user_id
        ).all()
        
        if not analyses:
            return jsonify({
                'total_analyses': 0,
                'average_similarity': 0,
                'improvement_trend': [],
                'strength_areas': [],
                'weakness_areas': []
            }), 200
        
        # Calculate statistics
        total_analyses = len(analyses)
        avg_overall = sum(a.overall_similarity for a in analyses) / total_analyses
        avg_content = sum(a.content_similarity for a in analyses) / total_analyses
        avg_keyword = sum(a.keyword_similarity for a in analyses) / total_analyses
        avg_structure = sum(a.structure_similarity for a in analyses) / total_analyses
        avg_theory = sum(a.theory_similarity for a in analyses) / total_analyses
        
        # Identify strength and weakness areas
        strength_areas = []
        weakness_areas = []
        
        if avg_content > 0.6:
            strength_areas.append('Content Coverage')
        else:
            weakness_areas.append('Content Coverage')
        
        if avg_keyword > 0.5:
            strength_areas.append('Sociological Terminology')
        else:
            weakness_areas.append('Sociological Terminology')
        
        if avg_structure > 0.6:
            strength_areas.append('Answer Structure')
        else:
            weakness_areas.append('Answer Structure')
        
        if avg_theory > 0.4:
            strength_areas.append('Theory Application')
        else:
            weakness_areas.append('Theory Application')
        
        return jsonify({
            'total_analyses': total_analyses,
            'average_similarity': round(avg_overall, 3),
            'detailed_averages': {
                'content_similarity': round(avg_content, 3),
                'keyword_similarity': round(avg_keyword, 3),
                'structure_similarity': round(avg_structure, 3),
                'theory_similarity': round(avg_theory, 3)
            },
            'strength_areas': strength_areas,
            'weakness_areas': weakness_areas
        }), 200
        
    except Exception as e:
        print(f"Error in get_similarity_stats: {e}")
        return jsonify({'error': 'Failed to retrieve similarity statistics'}), 500 
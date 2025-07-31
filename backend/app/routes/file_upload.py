from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from app.models.answer import Answer
from app.models.question import Question
from app.services.evaluation_service import evaluate_uploaded_file, get_ai_suggestions

file_upload_bp = Blueprint('file_upload', __name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_upload_bp.route('/upload-answer', methods=['POST'])
@jwt_required()
def upload_answer():
    """Upload and evaluate answer from file"""
    user_id = get_jwt_identity()
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        question_id = request.form.get('question_id')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not question_id:
            return jsonify({'error': 'Question ID is required'}), 400
        
        # Verify question exists
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Read file content for evaluation
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Evaluate the uploaded answer
            evaluation_result = evaluate_uploaded_file(file_content, file_extension, question)
            
            if 'error' in evaluation_result:
                # Clean up file if evaluation failed
                os.remove(file_path)
                return jsonify({'error': evaluation_result['error']}), 400
            
            # Create new answer record
            new_answer = Answer(
                user_id=user_id,
                question_id=question_id,
                answer_text=f"[Uploaded file: {file.filename}]",  # Placeholder text
                file_path=file_path,
                topic=question.topic,
                structure_score=evaluation_result.get('structure_score'),
                content_score=evaluation_result.get('content_score'),
                sociological_depth_score=evaluation_result.get('sociological_depth_score'),
                overall_score=evaluation_result.get('overall_score'),
                feedback=evaluation_result.get('feedback'),
                keywords_used=str(evaluation_result.get('keywords_used', [])),
                thinkers_mentioned=str(evaluation_result.get('thinkers_mentioned', [])),
                theories_referenced=str(evaluation_result.get('theories_referenced', [])),
                evaluated_at=datetime.utcnow()
            )
            
            db.session.add(new_answer)
            db.session.commit()
            
            return jsonify({
                'message': 'Answer uploaded and evaluated successfully',
                'answer': new_answer.to_dict(),
                'evaluation': evaluation_result,
                'file_info': {
                    'original_name': file.filename,
                    'saved_path': file_path,
                    'file_size': len(file_content)
                }
            }), 200
        
        else:
            return jsonify({'error': 'Invalid file type. Only PDF, DOCX, and DOC files are allowed'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Failed to upload and evaluate answer: {str(e)}'}), 500

@file_upload_bp.route('/get-suggestions', methods=['POST'])
@jwt_required()
def get_suggestions():
    """Get AI suggestions for improving an answer"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['answer_text', 'question_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        question = Question.query.get(data['question_id'])
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        suggestions = get_ai_suggestions(data['answer_text'], question)
        
        return jsonify({
            'suggestions': suggestions
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get suggestions: {str(e)}'}), 500

@file_upload_bp.route('/download/<int:answer_id>', methods=['GET'])
@jwt_required()
def download_answer_file(answer_id):
    """Download the uploaded answer file"""
    user_id = get_jwt_identity()
    
    try:
        answer = Answer.query.filter_by(id=answer_id, user_id=user_id).first()
        if not answer:
            return jsonify({'error': 'Answer not found'}), 404
        
        if not answer.file_path or not os.path.exists(answer.file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Return file path for frontend to handle download
        return jsonify({
            'file_path': answer.file_path,
            'file_name': os.path.basename(answer.file_path)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get file info: {str(e)}'}), 500 
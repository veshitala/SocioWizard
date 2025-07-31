import os
import json
import re
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatGPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4"  # or "gpt-3.5-turbo" for cost optimization
    
    def evaluate_answer(self, answer_text: str, question_text: str) -> Dict:
        """
        Evaluate an answer using ChatGPT API
        """
        try:
            prompt = f"""
            You are an expert UPSC Sociology examiner. Evaluate the following answer based on UPSC standards.

            Question: {question_text}
            
            Answer: {answer_text}
            
            Please provide a comprehensive evaluation in the following JSON format:
            {{
                "structure_score": <score out of 10>,
                "content_score": <score out of 10>,
                "sociological_depth_score": <score out of 10>,
                "overall_score": <average of all scores>,
                "feedback": "<detailed feedback with specific suggestions>",
                "keywords_used": ["keyword1", "keyword2", ...],
                "thinkers_mentioned": ["thinker1", "thinker2", ...],
                "theories_referenced": ["theory1", "theory2", ...],
                "strengths": ["strength1", "strength2", ...],
                "areas_for_improvement": ["area1", "area2", ...]
            }}
            
            Evaluation criteria:
            1. Structure (10 points): Introduction, body organization, conclusion, flow
            2. Content (10 points): Completeness, accuracy, examples, relevance
            3. Sociological depth (10 points): Theoretical understanding, concepts, analytical approach
            
            Be specific and constructive in your feedback. Focus on UPSC Sociology standards.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert UPSC Sociology examiner with deep knowledge of sociological theories, thinkers, and concepts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                evaluation = json.loads(json_match.group())
                return evaluation
            else:
                # Fallback to basic evaluation if JSON parsing fails
                return self._fallback_evaluation(answer_text, question_text)
                
        except Exception as e:
            print(f"Error in ChatGPT evaluation: {e}")
            return self._fallback_evaluation(answer_text, question_text)
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text content from PDF bytes
        """
        try:
            import PyPDF2
            import io
            
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_content: bytes) -> str:
        """
        Extract text content from DOCX bytes
        """
        try:
            import io
            from docx import Document
            
            doc_file = io.BytesIO(docx_content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return ""
    
    def evaluate_uploaded_answer(self, file_content: bytes, file_type: str, question_text: str) -> Dict:
        """
        Evaluate answer from uploaded file
        """
        try:
            # Extract text based on file type
            if file_type.lower() == 'pdf':
                answer_text = self.extract_text_from_pdf(file_content)
            elif file_type.lower() in ['docx', 'doc']:
                answer_text = self.extract_text_from_docx(file_content)
            else:
                return {"error": "Unsupported file type"}
            
            if not answer_text.strip():
                return {"error": "Could not extract text from file"}
            
            # Evaluate the extracted text
            return self.evaluate_answer(answer_text, question_text)
            
        except Exception as e:
            print(f"Error evaluating uploaded answer: {e}")
            return {"error": "Failed to evaluate uploaded answer"}
    
    def _fallback_evaluation(self, answer_text: str, question_text: str) -> Dict:
        """
        Fallback evaluation when ChatGPT API fails
        """
        word_count = len(answer_text.split())
        paragraphs = len([p for p in answer_text.split('\n\n') if p.strip()])
        
        # Basic scoring
        structure_score = min(10, max(1, 6 + (paragraphs * 0.5)))
        content_score = min(10, max(1, 5 + (word_count / 100)))
        sociological_depth_score = 6.0
        
        overall_score = round((structure_score + content_score + sociological_depth_score) / 3, 2)
        
        return {
            "structure_score": round(structure_score, 2),
            "content_score": round(content_score, 2),
            "sociological_depth_score": round(sociological_depth_score, 2),
            "overall_score": overall_score,
            "feedback": "Evaluation completed with basic scoring. Please check your answer structure and content.",
            "keywords_used": [],
            "thinkers_mentioned": [],
            "theories_referenced": [],
            "strengths": [],
            "areas_for_improvement": []
        }
    
    def get_ai_suggestions(self, answer_text: str, question_text: str) -> Dict:
        """
        Get AI-powered suggestions for improving the answer
        """
        try:
            prompt = f"""
            As a UPSC Sociology mentor, provide specific suggestions to improve this answer:

            Question: {question_text}
            Answer: {answer_text}
            
            Provide suggestions in this JSON format:
            {{
                "structure_suggestions": ["suggestion1", "suggestion2"],
                "content_suggestions": ["suggestion1", "suggestion2"],
                "theoretical_suggestions": ["suggestion1", "suggestion2"],
                "examples_to_add": ["example1", "example2"],
                "thinkers_to_mention": ["thinker1", "thinker2"],
                "concepts_to_include": ["concept1", "concept2"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful UPSC Sociology mentor providing constructive feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "Could not generate suggestions"}
                
        except Exception as e:
            print(f"Error getting AI suggestions: {e}")
            return {"error": "Failed to generate suggestions"} 
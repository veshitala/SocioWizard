import json
import re
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db
from app.models.topper_answer import TopperAnswer, AnswerSimilarity
from app.models.answer import Answer

class SimilarityAnalysisService:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Sociology-specific keywords and concepts
        self.sociology_keywords = {
            'theories': ['functionalism', 'conflict theory', 'symbolic interactionism', 'feminism', 'postmodernism'],
            'thinkers': ['karl marx', 'emile durkheim', 'max weber', 'robert merton', 'talcott parsons'],
            'concepts': ['socialization', 'social stratification', 'social mobility', 'social change', 'social institutions'],
            'methods': ['qualitative', 'quantitative', 'ethnography', 'survey', 'interview', 'observation']
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\;\:\!\?]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract sociology-specific keywords from text"""
        text_lower = text.lower()
        keywords = []
        
        for category, terms in self.sociology_keywords.items():
            for term in terms:
                if term in text_lower:
                    keywords.append(term)
        
        return keywords
    
    def extract_thinkers(self, text: str) -> List[str]:
        """Extract mentioned sociological thinkers"""
        thinkers = self.sociology_keywords['thinkers']
        mentioned = []
        
        for thinker in thinkers:
            if thinker in text.lower():
                mentioned.append(thinker)
        
        return mentioned
    
    def extract_theories(self, text: str) -> List[str]:
        """Extract mentioned sociological theories"""
        theories = self.sociology_keywords['theories']
        mentioned = []
        
        for theory in theories:
            if theory in text.lower():
                mentioned.append(theory)
        
        return mentioned
    
    def calculate_content_similarity(self, text1: str, text2: str) -> float:
        """Calculate content similarity using TF-IDF and cosine similarity"""
        if not text1 or not text2:
            return 0.0
        
        try:
            # Preprocess texts
            processed_text1 = self.preprocess_text(text1)
            processed_text2 = self.preprocess_text(text2)
            
            if not processed_text1 or not processed_text2:
                return 0.0
            
            # Create TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([processed_text1, processed_text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error calculating content similarity: {e}")
            return 0.0
    
    def calculate_keyword_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """Calculate similarity based on shared keywords"""
        if not keywords1 or not keywords2:
            return 0.0
        
        set1 = set(keywords1)
        set2 = set(keywords2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def calculate_structure_similarity(self, text1: str, text2: str) -> float:
        """Calculate structural similarity based on paragraph count, sentence length, etc."""
        if not text1 or not text2:
            return 0.0
        
        # Count paragraphs
        paragraphs1 = len([p for p in text1.split('\n\n') if p.strip()])
        paragraphs2 = len([p for p in text2.split('\n\n') if p.strip()])
        
        # Count sentences
        sentences1 = len(re.split(r'[.!?]+', text1))
        sentences2 = len(re.split(r'[.!?]+', text2))
        
        # Calculate word count
        words1 = len(text1.split())
        words2 = len(text2.split())
        
        # Normalize differences
        para_diff = 1 - abs(paragraphs1 - paragraphs2) / max(paragraphs1 + paragraphs2, 1)
        sent_diff = 1 - abs(sentences1 - sentences2) / max(sentences1 + sentences2, 1)
        word_diff = 1 - abs(words1 - words2) / max(words1 + words2, 1)
        
        # Weighted average
        structure_similarity = (para_diff * 0.3 + sent_diff * 0.4 + word_diff * 0.3)
        
        return max(0.0, min(1.0, structure_similarity))
    
    def calculate_theory_similarity(self, theories1: List[str], theories2: List[str]) -> float:
        """Calculate similarity based on mentioned theories"""
        return self.calculate_keyword_similarity(theories1, theories2)
    
    def calculate_overall_similarity(self, content_sim: float, keyword_sim: float, 
                                   structure_sim: float, theory_sim: float) -> float:
        """Calculate weighted overall similarity score"""
        weights = {
            'content': 0.4,
            'keyword': 0.25,
            'structure': 0.2,
            'theory': 0.15
        }
        
        overall = (content_sim * weights['content'] + 
                  keyword_sim * weights['keyword'] + 
                  structure_sim * weights['structure'] + 
                  theory_sim * weights['theory'])
        
        return round(overall, 3)
    
    def generate_feedback(self, user_answer: str, topper_answer: str, 
                         similarity_scores: Dict[str, float]) -> Tuple[str, List[str]]:
        """Generate personalized feedback based on similarity analysis"""
        feedback_parts = []
        suggestions = []
        
        # Content feedback
        if similarity_scores['content_similarity'] < 0.5:
            feedback_parts.append("Your answer could benefit from more comprehensive coverage of the topic.")
            suggestions.append("Include more sociological concepts and examples")
            suggestions.append("Expand on key arguments with supporting evidence")
        
        # Keyword feedback
        if similarity_scores['keyword_similarity'] < 0.4:
            feedback_parts.append("Consider incorporating more sociology-specific terminology.")
            suggestions.append("Use relevant sociological keywords and concepts")
            suggestions.append("Reference appropriate sociological thinkers")
        
        # Structure feedback
        if similarity_scores['structure_similarity'] < 0.6:
            feedback_parts.append("Your answer structure could be improved for better clarity.")
            suggestions.append("Organize your answer with clear paragraphs")
            suggestions.append("Use topic sentences to guide your arguments")
        
        # Theory feedback
        if similarity_scores['theory_similarity'] < 0.3:
            feedback_parts.append("Incorporate relevant sociological theories to strengthen your analysis.")
            suggestions.append("Apply appropriate theoretical frameworks")
            suggestions.append("Connect your arguments to sociological theories")
        
        # Positive feedback
        if similarity_scores['overall_similarity'] > 0.7:
            feedback_parts.append("Excellent work! Your answer demonstrates strong sociological understanding.")
        elif similarity_scores['overall_similarity'] > 0.5:
            feedback_parts.append("Good effort! With some improvements, your answer could be even stronger.")
        
        feedback_text = " ".join(feedback_parts) if feedback_parts else "Keep practicing to improve your sociological analysis."
        
        return feedback_text, suggestions
    
    def analyze_user_answer(self, user_answer_id: int) -> Dict:
        """Analyze a user answer against topper answers"""
        try:
            # Get user answer
            user_answer = Answer.query.get(user_answer_id)
            if not user_answer:
                return {'error': 'User answer not found'}
            
            # Get topper answers for the same question
            topper_answers = TopperAnswer.query.filter_by(question_id=user_answer.question_id).all()
            
            if not topper_answers:
                return {'error': 'No topper answers available for comparison'}
            
            best_match = None
            best_similarity = 0.0
            
            for topper_answer in topper_answers:
                # Calculate similarity scores
                content_sim = self.calculate_content_similarity(
                    user_answer.answer_text, topper_answer.answer_text
                )
                
                user_keywords = self.extract_keywords(user_answer.answer_text)
                topper_keywords = json.loads(topper_answer.keywords_used) if topper_answer.keywords_used else []
                keyword_sim = self.calculate_keyword_similarity(user_keywords, topper_keywords)
                
                structure_sim = self.calculate_structure_similarity(
                    user_answer.answer_text, topper_answer.answer_text
                )
                
                user_theories = self.extract_theories(user_answer.answer_text)
                topper_theories = json.loads(topper_answer.theories_referenced) if topper_answer.theories_referenced else []
                theory_sim = self.calculate_theory_similarity(user_theories, topper_theories)
                
                overall_sim = self.calculate_overall_similarity(
                    content_sim, keyword_sim, structure_sim, theory_sim
                )
                
                # Update best match
                if overall_sim > best_similarity:
                    best_similarity = overall_sim
                    best_match = {
                        'topper_answer': topper_answer,
                        'similarity_scores': {
                            'overall_similarity': overall_sim,
                            'content_similarity': content_sim,
                            'keyword_similarity': keyword_sim,
                            'structure_similarity': structure_sim,
                            'theory_similarity': theory_sim
                        }
                    }
            
            # Generate feedback
            feedback_text, suggestions = self.generate_feedback(
                user_answer.answer_text,
                best_match['topper_answer'].answer_text,
                best_match['similarity_scores']
            )
            
            # Save similarity analysis
            similarity_record = AnswerSimilarity(
                user_answer_id=user_answer_id,
                topper_answer_id=best_match['topper_answer'].id,
                overall_similarity=best_match['similarity_scores']['overall_similarity'],
                content_similarity=best_match['similarity_scores']['content_similarity'],
                structure_similarity=best_match['similarity_scores']['structure_similarity'],
                keyword_similarity=best_match['similarity_scores']['keyword_similarity'],
                theory_similarity=best_match['similarity_scores']['theory_similarity'],
                feedback_text=feedback_text,
                improvement_suggestions=json.dumps(suggestions)
            )
            
            db.session.add(similarity_record)
            db.session.commit()
            
            return {
                'similarity_analysis': {
                    'overall_similarity': best_match['similarity_scores']['overall_similarity'],
                    'content_similarity': best_match['similarity_scores']['content_similarity'],
                    'keyword_similarity': best_match['similarity_scores']['keyword_similarity'],
                    'structure_similarity': best_match['similarity_scores']['structure_similarity'],
                    'theory_similarity': best_match['similarity_scores']['theory_similarity']
                },
                'topper_answer': best_match['topper_answer'].to_dict(),
                'feedback': {
                    'text': feedback_text,
                    'suggestions': suggestions
                },
                'user_keywords': user_keywords,
                'user_theories': user_theories
            }
            
        except Exception as e:
            print(f"Error in analyze_user_answer: {e}")
            return {'error': 'Failed to analyze answer'}
    
    def add_topper_answer(self, question_id: int, topper_name: str, year: int,
                         answer_text: str, rank: int = None, marks: float = None) -> Dict:
        """Add a new topper answer to the database"""
        try:
            # Extract features
            keywords = self.extract_keywords(answer_text)
            thinkers = self.extract_thinkers(answer_text)
            theories = self.extract_theories(answer_text)
            word_count = len(answer_text.split())
            
            # Create topper answer
            topper_answer = TopperAnswer(
                question_id=question_id,
                topper_name=topper_name,
                year=year,
                rank=rank,
                marks_obtained=marks,
                answer_text=answer_text,
                keywords_used=json.dumps(keywords),
                thinkers_mentioned=json.dumps(thinkers),
                theories_referenced=json.dumps(theories),
                word_count=word_count
            )
            
            db.session.add(topper_answer)
            db.session.commit()
            
            return {
                'success': True,
                'topper_answer_id': topper_answer.id,
                'message': 'Topper answer added successfully'
            }
            
        except Exception as e:
            print(f"Error adding topper answer: {e}")
            return {'error': 'Failed to add topper answer'} 
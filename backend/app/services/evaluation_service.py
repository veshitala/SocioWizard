import random
import re
from typing import Dict, List

def evaluate_answer(answer_text: str, question) -> Dict:
    """
    Evaluate an answer using AI/LLM (placeholder implementation)
    This can be replaced with actual OpenAI API or other LLM integration
    """
    
    # Placeholder evaluation logic
    # In production, this would call an actual LLM API
    
    # Analyze answer length and structure
    word_count = len(answer_text.split())
    paragraphs = len([p for p in answer_text.split('\n\n') if p.strip()])
    
    # Simulate structure score based on answer organization
    structure_score = min(10, max(1, random.uniform(6, 9) + (paragraphs * 0.5)))
    
    # Simulate content score based on length and keywords
    content_score = min(10, max(1, random.uniform(5, 8) + (word_count / 100)))
    
    # Simulate sociological depth score
    sociological_depth_score = min(10, max(1, random.uniform(4, 8)))
    
    # Calculate overall score
    overall_score = round((structure_score + content_score + sociological_depth_score) / 3, 2)
    
    # Extract keywords (placeholder)
    keywords_used = extract_keywords(answer_text)
    
    # Extract thinkers mentioned (placeholder)
    thinkers_mentioned = extract_thinkers(answer_text)
    
    # Extract theories referenced (placeholder)
    theories_referenced = extract_theories(answer_text)
    
    # Generate feedback (placeholder)
    feedback = generate_feedback(structure_score, content_score, sociological_depth_score, answer_text)
    
    return {
        'structure_score': round(structure_score, 2),
        'content_score': round(content_score, 2),
        'sociological_depth_score': round(sociological_depth_score, 2),
        'overall_score': overall_score,
        'feedback': feedback,
        'keywords_used': keywords_used,
        'thinkers_mentioned': thinkers_mentioned,
        'theories_referenced': theories_referenced
    }

def extract_keywords(text: str) -> List[str]:
    """Extract sociological keywords from text (placeholder)"""
    # Common sociology keywords
    sociology_keywords = [
        'socialization', 'culture', 'society', 'institution', 'norms', 'values',
        'social structure', 'social change', 'modernization', 'globalization',
        'stratification', 'inequality', 'power', 'authority', 'social control',
        'deviance', 'socialization', 'role', 'status', 'group', 'community',
        'urbanization', 'industrialization', 'democracy', 'bureaucracy',
        'social movement', 'collective behavior', 'social problem'
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for keyword in sociology_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords[:10]  # Limit to 10 keywords

def extract_thinkers(text: str) -> List[str]:
    """Extract sociological thinkers mentioned (placeholder)"""
    # Common sociological thinkers
    thinkers = [
        'Durkheim', 'Weber', 'Marx', 'Parsons', 'Merton', 'Goffman',
        'Bourdieu', 'Foucault', 'Giddens', 'Habermas', 'Bauman',
        'Beck', 'Castells', 'Giddens', 'Luhmann', 'Simmel'
    ]
    
    found_thinkers = []
    text_lower = text.lower()
    
    for thinker in thinkers:
        if thinker.lower() in text_lower:
            found_thinkers.append(thinker)
    
    return found_thinkers[:5]  # Limit to 5 thinkers

def extract_theories(text: str) -> List[str]:
    """Extract sociological theories referenced (placeholder)"""
    # Common sociological theories
    theories = [
        'structural functionalism', 'conflict theory', 'symbolic interactionism',
        'social constructionism', 'feminist theory', 'postmodernism',
        'rational choice theory', 'social exchange theory', 'labeling theory',
        'strain theory', 'differential association', 'social learning theory'
    ]
    
    found_theories = []
    text_lower = text.lower()
    
    for theory in theories:
        if theory in text_lower:
            found_theories.append(theory)
    
    return found_theories[:5]  # Limit to 5 theories

def generate_feedback(structure_score: float, content_score: float, 
                     depth_score: float, answer_text: str) -> str:
    """Generate detailed feedback based on scores (placeholder)"""
    
    feedback_parts = []
    
    # Structure feedback
    if structure_score >= 8:
        feedback_parts.append("Excellent structure with clear introduction, body, and conclusion.")
    elif structure_score >= 6:
        feedback_parts.append("Good structure, but could improve organization and flow.")
    else:
        feedback_parts.append("Structure needs improvement. Consider adding clear sections and transitions.")
    
    # Content feedback
    if content_score >= 8:
        feedback_parts.append("Rich content with comprehensive coverage of the topic.")
    elif content_score >= 6:
        feedback_parts.append("Adequate content, but could include more examples and details.")
    else:
        feedback_parts.append("Content is insufficient. Add more relevant points and examples.")
    
    # Sociological depth feedback
    if depth_score >= 8:
        feedback_parts.append("Strong sociological perspective with appropriate theoretical frameworks.")
    elif depth_score >= 6:
        feedback_parts.append("Good sociological approach, but could integrate more theoretical concepts.")
    else:
        feedback_parts.append("Needs more sociological depth. Incorporate relevant theories and concepts.")
    
    # Word count feedback
    word_count = len(answer_text.split())
    if word_count < 200:
        feedback_parts.append("Answer is too brief. Aim for at least 200-300 words for comprehensive coverage.")
    elif word_count > 800:
        feedback_parts.append("Answer is quite lengthy. Consider being more concise while maintaining quality.")
    
    return " ".join(feedback_parts)

# Future: Integration with actual LLM API
def evaluate_with_llm(answer_text: str, question_text: str) -> Dict:
    """
    Placeholder for actual LLM integration
    This would call OpenAI API or similar service
    """
    # Example OpenAI API call (commented out for now)
    # import openai
    # 
    # prompt = f"""
    # Evaluate this UPSC Sociology answer:
    # 
    # Question: {question_text}
    # Answer: {answer_text}
    # 
    # Provide scores out of 10 for:
    # 1. Structure (organization, flow, clarity)
    # 2. Content (completeness, accuracy, examples)
    # 3. Sociological depth (theoretical understanding, concepts)
    # 
    # Also provide:
    # - Overall score
    # - Detailed feedback
    # - Keywords used
    # - Thinkers mentioned
    # - Theories referenced
    # """
    # 
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # 
    # Parse response and return structured data
    # return parse_llm_response(response.choices[0].message.content)
    
    # For now, return placeholder evaluation
    return evaluate_answer(answer_text, None) 
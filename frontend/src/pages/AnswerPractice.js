import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/apiService';
import { 
  RefreshCw, 
  Send, 
  Filter,
  FileText,
  Calendar,
  Tag
} from 'lucide-react';

const AnswerPractice = () => {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answerText, setAnswerText] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [filters, setFilters] = useState({
    theme: '',
    topic: '',
    year: ''
  });
  const [availableFilters, setAvailableFilters] = useState({
    themes: [],
    topics: [],
    years: []
  });
  const [showFilters, setShowFilters] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    fetchFilters();
    fetchRandomQuestion();
  }, []);

  const fetchFilters = async () => {
    try {
      const [themes, topics, years] = await Promise.all([
        apiService.getThemes(),
        apiService.getTopics(),
        apiService.getYears()
      ]);
      
      setAvailableFilters({
        themes: themes.themes,
        topics: topics.topics,
        years: years.years
      });
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const fetchRandomQuestion = async () => {
    setLoading(true);
    try {
      const response = await apiService.getRandomQuestion(filters);
      console.log('Fetched question:', response.question);
      setCurrentQuestion(response.question);
      setAnswerText('');
    } catch (error) {
      console.error('Error fetching random question:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!answerText.trim()) {
      alert('Please write an answer before submitting.');
      return;
    }

    setSubmitting(true);
    try {
      const response = await apiService.submitAnswer({
        question_id: currentQuestion.id,
        answer_text: answerText,
        topic: currentQuestion.topic
      });
      
      // Navigate to evaluation page with the submitted answer
      navigate('/evaluate', { 
        state: { 
          answer: response.answer,
          evaluation: response.evaluation,
          question: currentQuestion
        }
      });
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const applyFilters = () => {
    fetchRandomQuestion();
    setShowFilters(false);
  };

  const clearFilters = () => {
    setFilters({
      theme: '',
      topic: '',
      year: ''
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Answer Practice</h1>
          <p className="text-gray-600">Practice with random PYQs and get AI-powered feedback</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn-secondary flex items-center"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </button>
          <button
            onClick={fetchRandomQuestion}
            disabled={loading}
            className="btn-primary flex items-center"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Loading...' : 'New Question'}
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Filter Questions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Theme</label>
              <select
                value={filters.theme}
                onChange={(e) => handleFilterChange('theme', e.target.value)}
                className="input-field"
              >
                <option value="">All Themes</option>
                {availableFilters.themes.map(theme => (
                  <option key={theme} value={theme}>{theme}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Topic</label>
              <select
                value={filters.topic}
                onChange={(e) => handleFilterChange('topic', e.target.value)}
                className="input-field"
              >
                <option value="">All Topics</option>
                {availableFilters.topics.map(topic => (
                  <option key={topic} value={topic}>{topic}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Year</label>
              <select
                value={filters.year}
                onChange={(e) => handleFilterChange('year', e.target.value)}
                className="input-field"
              >
                <option value="">All Years</option>
                {availableFilters.years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex space-x-3 mt-4">
            <button onClick={applyFilters} className="btn-primary">
              Apply Filters
            </button>
            <button onClick={clearFilters} className="btn-secondary">
              Clear All
            </button>
          </div>
        </div>
      )}

      {/* Question Display */}
      {currentQuestion && (
        <div className="card">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                {currentQuestion.question_text}
              </h2>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-1" />
                  {currentQuestion.year}
                </div>
                <div className="flex items-center">
                  <Tag className="h-4 w-4 mr-1" />
                  {currentQuestion.topic}
                </div>
                <div className="flex items-center">
                  <FileText className="h-4 w-4 mr-1" />
                  {currentQuestion.theme}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Answer Editor */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Your Answer</h3>
          <div className="text-sm text-gray-500">
            {answerText.length} characters
          </div>
        </div>
        
        <textarea
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          placeholder="Write your answer here... Start with an introduction, develop your arguments with examples and theories, and conclude with a summary of your main points."
          className="w-full h-96 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-gray-900"
          disabled={!currentQuestion}
          style={{ minHeight: '400px' }}
        />
        
        <div className="mt-4 flex justify-between items-center">
          <div className="text-sm text-gray-500">
            <p>💡 Tip: Structure your answer with introduction, body, and conclusion</p>
            <p>📚 Include relevant sociological theories and thinkers</p>
            <p>📝 Aim for 200-300 words for comprehensive coverage</p>
          </div>
          <button
            onClick={handleSubmit}
            disabled={!currentQuestion || !answerText.trim() || submitting}
            className="btn-primary flex items-center"
          >
            <Send className="h-4 w-4 mr-2" />
            {submitting ? 'Submitting...' : 'Submit for Evaluation'}
          </button>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="card">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mr-3"></div>
            <span className="text-gray-600">Loading question...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnswerPractice; 
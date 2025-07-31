import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/apiService';
import { 
  RefreshCw, 
  Send, 
  Filter,
  FileText,
  Calendar,
  Tag,
  Upload,
  Download,
  Lightbulb
} from 'lucide-react';

const AnswerPractice = () => {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answerText, setAnswerText] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState(null);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
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
      setSelectedFile(null);
      setSuggestions(null);
      setShowSuggestions(false);
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
      
      // Show success message with topper analysis info
      if (response.topper_analysis) {
        alert('Answer submitted successfully! Topper analysis is available. Check the Topper Analysis page for detailed comparison.');
      } else {
        alert('Answer submitted successfully!');
      }
      
      // Navigate to evaluation page with the submitted answer
      navigate('/evaluate', { 
        state: { 
          answer: response.answer,
          evaluation: response.evaluation,
          question: currentQuestion,
          topperAnalysis: response.topper_analysis
        }
      });
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }

    setUploading(true);
    try {
      const response = await apiService.uploadAnswerFile(selectedFile, currentQuestion.id);
      
      alert('Answer uploaded and evaluated successfully!');
      
      // Navigate to evaluation page with the uploaded answer
      navigate('/evaluate', { 
        state: { 
          answer: response.answer,
          evaluation: response.evaluation,
          question: currentQuestion,
          fileInfo: response.file_info
        }
      });
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload file. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
      if (allowedTypes.includes(file.type)) {
        setSelectedFile(file);
      } else {
        alert('Please select a PDF, DOCX, or DOC file.');
        event.target.value = '';
      }
    }
  };

  const getAISuggestions = async () => {
    if (!answerText.trim()) {
      alert('Please write an answer before getting suggestions.');
      return;
    }

    setLoadingSuggestions(true);
    try {
      const response = await apiService.getAISuggestions(answerText, currentQuestion.id);
      setSuggestions(response.suggestions);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Error getting suggestions:', error);
      alert('Failed to get AI suggestions. Please try again.');
    } finally {
      setLoadingSuggestions(false);
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

      {/* File Upload Section */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Answer File (Optional)</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <input
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
            />
            <button
              onClick={handleFileUpload}
              disabled={!selectedFile || uploading}
              className="btn-primary flex items-center"
            >
              <Upload className="h-4 w-4 mr-2" />
              {uploading ? 'Uploading...' : 'Upload & Evaluate'}
            </button>
          </div>
          {selectedFile && (
            <div className="text-sm text-gray-600">
              Selected file: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
            </div>
          )}
          <div className="text-sm text-gray-500">
            <p>📄 Supported formats: PDF, DOCX, DOC</p>
            <p>💡 Upload your handwritten or typed answer for AI evaluation</p>
          </div>
        </div>
      </div>

      {/* Answer Editor */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Your Answer</h3>
          <div className="flex items-center space-x-2">
            <div className="text-sm text-gray-500">
              {answerText.length} characters
            </div>
            <button
              onClick={getAISuggestions}
              disabled={!answerText.trim() || loadingSuggestions}
              className="btn-secondary flex items-center text-sm"
            >
              <Lightbulb className="h-4 w-4 mr-1" />
              {loadingSuggestions ? 'Getting Suggestions...' : 'AI Suggestions'}
            </button>
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

      {/* AI Suggestions */}
      {showSuggestions && suggestions && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Suggestions for Improvement</h3>
          <div className="space-y-4">
            {suggestions.structure_suggestions && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Structure Suggestions:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.structure_suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
            {suggestions.content_suggestions && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Content Suggestions:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.content_suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
            {suggestions.theoretical_suggestions && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Theoretical Suggestions:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.theoretical_suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
            {suggestions.examples_to_add && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Examples to Add:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.examples_to_add.map((example, index) => (
                    <li key={index}>{example}</li>
                  ))}
                </ul>
              </div>
            )}
            {suggestions.thinkers_to_mention && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Thinkers to Mention:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.thinkers_to_mention.map((thinker, index) => (
                    <li key={index}>{thinker}</li>
                  ))}
                </ul>
              </div>
            )}
            {suggestions.concepts_to_include && (
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Concepts to Include:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {suggestions.concepts_to_include.map((concept, index) => (
                    <li key={index}>{concept}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

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
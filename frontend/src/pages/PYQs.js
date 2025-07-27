import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../services/apiService';
import { 
  Search, 
  Filter, 
  FileText, 
  Calendar, 
  Tag,
  BookOpen,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

const PYQs = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
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
  const [expandedQuestions, setExpandedQuestions] = useState(new Set());

  useEffect(() => {
    fetchFilters();
    fetchQuestions();
  }, []);

  useEffect(() => {
    fetchQuestions();
  }, [filters]);

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

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const response = await apiService.searchQuestions({
        ...filters,
        limit: 50
      });
      setQuestions(response.questions);
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters({
      theme: '',
      topic: '',
      year: ''
    });
    setSearchTerm('');
  };

  const toggleQuestionExpansion = (questionId) => {
    const newExpanded = new Set(expandedQuestions);
    if (newExpanded.has(questionId)) {
      newExpanded.delete(questionId);
    } else {
      newExpanded.add(questionId);
    }
    setExpandedQuestions(newExpanded);
  };

  const filteredQuestions = questions.filter(question =>
    question.question_text.toLowerCase().includes(searchTerm.toLowerCase()) ||
    question.topic.toLowerCase().includes(searchTerm.toLowerCase()) ||
    question.theme.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Previous Year Questions</h1>
        <p className="text-gray-600">Browse and search through the UPSC Sociology PYQ database</p>
      </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search questions, topics, or themes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn-secondary flex items-center ml-4"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
            {showFilters ? <ChevronUp className="h-4 w-4 ml-2" /> : <ChevronDown className="h-4 w-4 ml-2" />}
          </button>
        </div>

        {showFilters && (
          <div className="border-t pt-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
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
            <div className="flex justify-between items-center">
              <div className="text-sm text-gray-500">
                {filteredQuestions.length} questions found
              </div>
              <button onClick={clearFilters} className="btn-secondary">
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : filteredQuestions.length > 0 ? (
          filteredQuestions.map((question) => (
            <div key={question.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-4 mb-2">
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="h-4 w-4 mr-1" />
                      {question.year}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Tag className="h-4 w-4 mr-1" />
                      {question.topic}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <FileText className="h-4 w-4 mr-1" />
                      {question.theme}
                    </div>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {question.question_text}
                  </h3>
                  
                  {expandedQuestions.has(question.id) && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium text-gray-900">Question Details</h4>
                        <div className="text-sm text-gray-500">
                          {question.marks} marks
                        </div>
                      </div>
                      <p className="text-gray-700 mb-4">{question.question_text}</p>
                      <div className="flex space-x-2">
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                          {question.theme}
                        </span>
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                          {question.topic}
                        </span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                          {question.year}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <button
                    onClick={() => toggleQuestionExpansion(question.id)}
                    className="p-2 text-gray-400 hover:text-gray-600"
                  >
                    {expandedQuestions.has(question.id) ? (
                      <ChevronUp className="h-5 w-5" />
                    ) : (
                      <ChevronDown className="h-5 w-5" />
                    )}
                  </button>
                  <Link
                    to="/practice"
                    state={{ selectedQuestion: question }}
                    className="btn-primary flex items-center"
                  >
                    <BookOpen className="h-4 w-4 mr-2" />
                    Practice
                  </Link>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center py-12">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No questions found</h3>
            <p className="text-gray-500">
              Try adjusting your search terms or filters to find more questions.
            </p>
          </div>
        )}
      </div>

      {/* Statistics */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Database Statistics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{questions.length}</div>
            <div className="text-sm text-gray-500">Total Questions</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{availableFilters.topics.length}</div>
            <div className="text-sm text-gray-500">Topics Covered</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{availableFilters.themes.length}</div>
            <div className="text-sm text-gray-500">Themes</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PYQs; 
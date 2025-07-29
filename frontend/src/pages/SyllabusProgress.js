import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  TrendingUp, 
  Target, 
  Award,
  BookOpen,
  CheckCircle,
  AlertCircle,
  Clock,
  Star,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

const SyllabusProgress = () => {
  const [syllabusOverview, setSyllabusOverview] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [strengthAnalysis, setStrengthAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedTopics, setExpandedTopics] = useState(new Set());

  useEffect(() => {
    fetchSyllabusData();
  }, []);

  const fetchSyllabusData = async () => {
    try {
      const [overview, strength, recs] = await Promise.all([
        apiService.getSyllabusOverview(),
        apiService.getStrengthAnalysis(),
        apiService.getRecommendations()
      ]);
      
      setSyllabusOverview(overview);
      setStrengthAnalysis(strength);
      setRecommendations(recs.recommendations);
    } catch (error) {
      console.error('Error fetching syllabus data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTopicDetails = async (topicId) => {
    try {
      const topicData = await apiService.getTopicSubtopicsProgress(topicId);
      setSelectedTopic(topicData);
    } catch (error) {
      console.error('Error fetching topic details:', error);
    }
  };

  const toggleTopicExpansion = (topicId) => {
    const newExpanded = new Set(expandedTopics);
    if (newExpanded.has(topicId)) {
      newExpanded.delete(topicId);
    } else {
      newExpanded.add(topicId);
      fetchTopicDetails(topicId);
    }
    setExpandedTopics(newExpanded);
  };

  const getStrengthColor = (level) => {
    switch (level) {
      case 'strong': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'weak': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStrengthIcon = (level) => {
    switch (level) {
      case 'strong': return <Star className="h-4 w-4" />;
      case 'moderate': return <AlertCircle className="h-4 w-4" />;
      case 'weak': return <Clock className="h-4 w-4" />;
      default: return <BookOpen className="h-4 w-4" />;
    }
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-yellow-500';
    if (percentage >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Syllabus Progress</h1>
        <p className="text-gray-600">Track your progress across UPSC CSE Sociology syllabus</p>
      </div>

      {/* Overall Progress */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Overall Syllabus Progress</h3>
          <div className="text-right">
            <p className="text-2xl font-bold text-primary-600">
              {syllabusOverview?.overall_progress || 0}%
            </p>
            <p className="text-sm text-gray-600">
              {syllabusOverview?.total_questions_answered || 0} / {syllabusOverview?.total_possible_questions || 0} questions
            </p>
          </div>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className={`${getProgressColor(syllabusOverview?.overall_progress || 0)} h-3 rounded-full transition-all duration-300`}
            style={{ width: `${syllabusOverview?.overall_progress || 0}%` }}
          ></div>
        </div>
      </div>

      {/* Strength Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Strong Topics</p>
              <p className="text-2xl font-bold text-gray-900">
                {strengthAnalysis?.strong_topics?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <AlertCircle className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Moderate Topics</p>
              <p className="text-2xl font-bold text-gray-900">
                {strengthAnalysis?.moderate_topics?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <Clock className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Weak Topics</p>
              <p className="text-2xl font-bold text-gray-900">
                {strengthAnalysis?.weak_topics?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-gray-100 rounded-lg">
              <BookOpen className="h-6 w-6 text-gray-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Not Started</p>
              <p className="text-2xl font-bold text-gray-900">
                {strengthAnalysis?.not_started_topics?.length || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Syllabus Topics */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Syllabus Topics Progress</h3>
        <div className="space-y-6">
          
          {/* Paper 1 */}
          {syllabusOverview?.syllabus_overview?.paper1 && (
            <div className="border rounded-lg p-4 bg-blue-50">
              <h4 className="text-lg font-semibold text-blue-900 mb-4">{syllabusOverview.syllabus_overview.paper1.name}</h4>
              <div className="space-y-4">
                {syllabusOverview.syllabus_overview.paper1.topics?.map((topic) => (
                  <div key={topic.id} className="border rounded-lg p-4 bg-white">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <button
                          onClick={() => toggleTopicExpansion(topic.id)}
                          className="p-1 hover:bg-gray-100 rounded"
                        >
                          {expandedTopics.has(topic.id) ? (
                            <ChevronDown className="h-4 w-4" />
                          ) : (
                            <ChevronRight className="h-4 w-4" />
                          )}
                        </button>
                        <div>
                          <h5 className="font-semibold text-gray-900">{topic.name}</h5>
                          <p className="text-sm text-gray-600">{topic.description}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(topic.strength_level)}`}>
                            {getStrengthIcon(topic.strength_level)}
                            <span className="ml-1">{topic.strength_level.replace('_', ' ')}</span>
                          </span>
                          <span className="text-sm font-medium text-gray-900">
                            {topic.progress_percentage}%
                          </span>
                        </div>
                        <p className="text-xs text-gray-500">
                          {topic.questions_answered}/{topic.target_questions} questions
                        </p>
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                      <div 
                        className={`${getProgressColor(topic.progress_percentage)} h-2 rounded-full transition-all duration-300`}
                        style={{ width: `${topic.progress_percentage}%` }}
                      ></div>
                    </div>

                    {/* Topic Details */}
                    {expandedTopics.has(topic.id) && selectedTopic?.topic?.id === topic.id && (
                      <div className="mt-4 pl-8 border-l-2 border-gray-200">
                        <h6 className="font-medium text-gray-900 mb-3">Subtopics Progress</h6>
                        <div className="space-y-3">
                          {selectedTopic.subtopics_progress?.map((subtopic) => (
                            <div key={subtopic.id} className="bg-gray-50 rounded p-3">
                              <div className="flex items-center justify-between mb-2">
                                <div>
                                  <h7 className="font-medium text-sm text-gray-900">{subtopic.name}</h7>
                                  <p className="text-xs text-gray-600">{subtopic.description}</p>
                                </div>
                                <div className="text-right">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(subtopic.strength_level)}`}>
                                    {subtopic.average_score > 0 ? `${subtopic.average_score}/10` : 'Not started'}
                                  </span>
                                </div>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-1.5">
                                <div 
                                  className={`${getProgressColor(subtopic.progress_percentage)} h-1.5 rounded-full transition-all duration-300`}
                                  style={{ width: `${subtopic.progress_percentage}%` }}
                                ></div>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                {subtopic.questions_answered}/{subtopic.target_questions} questions
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Paper 2 */}
          {syllabusOverview?.syllabus_overview?.paper2 && (
            <div className="border rounded-lg p-4 bg-green-50">
              <h4 className="text-lg font-semibold text-green-900 mb-4">{syllabusOverview.syllabus_overview.paper2.name}</h4>
              <div className="space-y-4">
                {syllabusOverview.syllabus_overview.paper2.topics?.map((topic) => (
                  <div key={topic.id} className="border rounded-lg p-4 bg-white">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <button
                          onClick={() => toggleTopicExpansion(topic.id)}
                          className="p-1 hover:bg-gray-100 rounded"
                        >
                          {expandedTopics.has(topic.id) ? (
                            <ChevronDown className="h-4 w-4" />
                          ) : (
                            <ChevronRight className="h-4 w-4" />
                          )}
                        </button>
                        <div>
                          <h5 className="font-semibold text-gray-900">{topic.name}</h5>
                          <p className="text-sm text-gray-600">{topic.description}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(topic.strength_level)}`}>
                            {getStrengthIcon(topic.strength_level)}
                            <span className="ml-1">{topic.strength_level.replace('_', ' ')}</span>
                          </span>
                          <span className="text-sm font-medium text-gray-900">
                            {topic.progress_percentage}%
                          </span>
                        </div>
                        <p className="text-xs text-gray-500">
                          {topic.questions_answered}/{topic.target_questions} questions
                        </p>
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                      <div 
                        className={`${getProgressColor(topic.progress_percentage)} h-2 rounded-full transition-all duration-300`}
                        style={{ width: `${topic.progress_percentage}%` }}
                      ></div>
                    </div>

                    {/* Topic Details */}
                    {expandedTopics.has(topic.id) && selectedTopic?.topic?.id === topic.id && (
                      <div className="mt-4 pl-8 border-l-2 border-gray-200">
                        <h6 className="font-medium text-gray-900 mb-3">Subtopics Progress</h6>
                        <div className="space-y-3">
                          {selectedTopic.subtopics_progress?.map((subtopic) => (
                            <div key={subtopic.id} className="bg-gray-50 rounded p-3">
                              <div className="flex items-center justify-between mb-2">
                                <div>
                                  <h7 className="font-medium text-sm text-gray-900">{subtopic.name}</h7>
                                  <p className="text-xs text-gray-600">{subtopic.description}</p>
                                </div>
                                <div className="text-right">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(subtopic.strength_level)}`}>
                                    {subtopic.average_score > 0 ? `${subtopic.average_score}/10` : 'Not started'}
                                  </span>
                                </div>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-1.5">
                                <div 
                                  className={`${getProgressColor(subtopic.progress_percentage)} h-1.5 rounded-full transition-all duration-300`}
                                  style={{ width: `${subtopic.progress_percentage}%` }}
                                ></div>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                {subtopic.questions_answered}/{subtopic.target_questions} questions
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Fallback for old API structure */}
          {!syllabusOverview?.syllabus_overview?.paper1 && syllabusOverview?.syllabus_overview && Array.isArray(syllabusOverview.syllabus_overview) && (
            <div className="border rounded-lg p-4 bg-yellow-50">
              <h4 className="text-lg font-semibold text-yellow-900 mb-4">Legacy Syllabus Structure</h4>
              <div className="space-y-4">
                {syllabusOverview.syllabus_overview.map((topic) => (
                  <div key={topic.id} className="border rounded-lg p-4 bg-white">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <button
                          onClick={() => toggleTopicExpansion(topic.id)}
                          className="p-1 hover:bg-gray-100 rounded"
                        >
                          {expandedTopics.has(topic.id) ? (
                            <ChevronDown className="h-4 w-4" />
                          ) : (
                            <ChevronRight className="h-4 w-4" />
                          )}
                        </button>
                        <div>
                          <h5 className="font-semibold text-gray-900">{topic.name}</h5>
                          <p className="text-sm text-gray-600">{topic.description}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(topic.strength_level)}`}>
                            {getStrengthIcon(topic.strength_level)}
                            <span className="ml-1">{topic.strength_level.replace('_', ' ')}</span>
                          </span>
                          <span className="text-sm font-medium text-gray-900">
                            {topic.progress_percentage}%
                          </span>
                        </div>
                        <p className="text-xs text-gray-500">
                          {topic.questions_answered}/{topic.target_questions} questions
                        </p>
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                      <div 
                        className={`${getProgressColor(topic.progress_percentage)} h-2 rounded-full transition-all duration-300`}
                        style={{ width: `${topic.progress_percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Personalized Recommendations</h3>
        <div className="space-y-4">
          {recommendations.map((rec, index) => (
            <div key={index} className={`p-4 rounded-lg ${
              rec.priority === 'high' ? 'bg-red-50 border border-red-200' :
              rec.priority === 'medium' ? 'bg-yellow-50 border border-yellow-200' :
              'bg-green-50 border border-green-200'
            }`}>
              <div className="flex items-start">
                <div className={`p-2 rounded-lg ${
                  rec.priority === 'high' ? 'bg-red-100' :
                  rec.priority === 'medium' ? 'bg-yellow-100' :
                  'bg-green-100'
                }`}>
                  {rec.type === 'focus_area' && <Target className="h-4 w-4 text-red-600" />}
                  {rec.type === 'practice_more' && <TrendingUp className="h-4 w-4 text-yellow-600" />}
                  {rec.type === 'strength' && <Award className="h-4 w-4 text-green-600" />}
                </div>
                <div className="ml-3">
                  <h4 className="font-medium text-gray-900">{rec.title}</h4>
                  <p className="text-sm text-gray-700 mt-1">{rec.description}</p>
                </div>
              </div>
            </div>
          ))}
          {recommendations.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Start practicing questions to get personalized recommendations!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SyllabusProgress; 
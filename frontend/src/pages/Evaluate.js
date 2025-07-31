import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  CheckCircle, 
  AlertCircle, 
  TrendingUp,
  BookOpen,
  Users,
  Lightbulb,
  ArrowLeft,
  Star,
  Trophy,
  Target,
  BarChart3,
  FileText,
  Download
} from 'lucide-react';

const Evaluate = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [evaluationData, setEvaluationData] = useState(null);

  useEffect(() => {
    if (location.state?.evaluation && location.state?.answer) {
      setEvaluationData({
        evaluation: location.state.evaluation,
        answer: location.state.answer,
        question: location.state.question,
        topperAnalysis: location.state.topperAnalysis,
        fileInfo: location.state.fileInfo
      });
    } else {
      // If no evaluation data, redirect to practice
      navigate('/practice');
    }
  }, [location.state, navigate]);

  if (!evaluationData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const { evaluation, answer, question, topperAnalysis, fileInfo } = evaluationData;

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreIcon = (score) => {
    if (score >= 8) return <CheckCircle className="h-5 w-5 text-green-600" />;
    if (score >= 6) return <AlertCircle className="h-5 w-5 text-yellow-600" />;
    return <AlertCircle className="h-5 w-5 text-red-600" />;
  };

  const renderScoreCard = (title, score, description) => (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {getScoreIcon(score)}
      </div>
      <div className="text-center">
        <div className={`text-3xl font-bold ${getScoreColor(score)}`}>
          {score.toFixed(1)}
        </div>
        <div className="text-sm text-gray-500">out of 10</div>
      </div>
      <p className="text-sm text-gray-600 mt-3">{description}</p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/practice')}
            className="btn-secondary flex items-center"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Practice
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Answer Evaluation</h1>
            <p className="text-gray-600">AI-powered feedback on your answer</p>
          </div>
        </div>
      </div>

      {/* File Information */}
      {fileInfo && (
        <div className="card">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-5 w-5 text-primary-600" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Uploaded File</h3>
                <p className="text-sm text-gray-600">
                  {fileInfo.original_name} ({(fileInfo.file_size / 1024).toFixed(1)} KB)
                </p>
              </div>
            </div>
            <button
              onClick={() => window.open(`/api/file-upload/download/${answer.id}`, '_blank')}
              className="btn-secondary flex items-center text-sm"
            >
              <Download className="h-4 w-4 mr-2" />
              Download
            </button>
          </div>
        </div>
      )}

      {/* Question */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Question</h3>
        <p className="text-gray-700">{question.question_text}</p>
        <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
          <span>Year: {question.year}</span>
          <span>Topic: {question.topic}</span>
          <span>Theme: {question.theme}</span>
        </div>
      </div>

      {/* Overall Score */}
      <div className="card">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <Trophy className="h-8 w-8 text-yellow-500 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Overall Score</h2>
          </div>
          <div className={`text-5xl font-bold ${getScoreColor(evaluation.overall_score)}`}>
            {evaluation.overall_score.toFixed(1)}
          </div>
          <div className="text-lg text-gray-500">out of 10</div>
          <div className="mt-4">
            {evaluation.overall_score >= 8 && (
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <Star className="h-4 w-4 mr-1" />
                Excellent Performance
              </div>
            )}
            {evaluation.overall_score >= 6 && evaluation.overall_score < 8 && (
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                <Target className="h-4 w-4 mr-1" />
                Good Performance
              </div>
            )}
            {evaluation.overall_score < 6 && (
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                <AlertCircle className="h-4 w-4 mr-1" />
                Needs Improvement
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Detailed Scores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {renderScoreCard(
          'Structure',
          evaluation.structure_score,
          'Organization, flow, and clarity of your answer'
        )}
        {renderScoreCard(
          'Content',
          evaluation.content_score,
          'Completeness, accuracy, and relevance of content'
        )}
        {renderScoreCard(
          'Sociological Depth',
          evaluation.sociological_depth_score,
          'Theoretical understanding and analytical approach'
        )}
      </div>

      {/* Feedback */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Lightbulb className="h-5 w-5 text-yellow-500 mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Detailed Feedback</h3>
        </div>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">{evaluation.feedback}</p>
        </div>
      </div>

      {/* Strengths and Areas for Improvement */}
      {(evaluation.strengths || evaluation.areas_for_improvement) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {evaluation.strengths && evaluation.strengths.length > 0 && (
            <div className="card">
              <div className="flex items-center mb-4">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">Strengths</h3>
              </div>
              <ul className="space-y-2">
                {evaluation.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {evaluation.areas_for_improvement && evaluation.areas_for_improvement.length > 0 && (
            <div className="card">
              <div className="flex items-center mb-4">
                <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">Areas for Improvement</h3>
              </div>
              <ul className="space-y-2">
                {evaluation.areas_for_improvement.map((area, index) => (
                  <li key={index} className="flex items-start">
                    <AlertCircle className="h-4 w-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{area}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Keywords, Thinkers, and Theories */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {evaluation.keywords_used && evaluation.keywords_used.length > 0 && (
          <div className="card">
            <div className="flex items-center mb-4">
              <BookOpen className="h-5 w-5 text-blue-500 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Keywords Used</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {evaluation.keywords_used.map((keyword, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        {evaluation.thinkers_mentioned && evaluation.thinkers_mentioned.length > 0 && (
          <div className="card">
            <div className="flex items-center mb-4">
              <Users className="h-5 w-5 text-purple-500 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Thinkers Mentioned</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {evaluation.thinkers_mentioned.map((thinker, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-purple-100 text-purple-800 text-sm rounded-full"
                >
                  {thinker}
                </span>
              ))}
            </div>
          </div>
        )}

        {evaluation.theories_referenced && evaluation.theories_referenced.length > 0 && (
          <div className="card">
            <div className="flex items-center mb-4">
              <BarChart3 className="h-5 w-5 text-indigo-500 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Theories Referenced</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {evaluation.theories_referenced.map((theory, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-indigo-100 text-indigo-800 text-sm rounded-full"
                >
                  {theory}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Topper Analysis Link */}
      {topperAnalysis && (
        <div className="card">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <TrendingUp className="h-5 w-5 text-green-500 mr-2" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Topper Analysis Available</h3>
                <p className="text-sm text-gray-600">Compare your answer with topper answers</p>
              </div>
            </div>
            <button
              onClick={() => navigate('/topper-analysis')}
              className="btn-primary"
            >
              View Analysis
            </button>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => navigate('/practice')}
          className="btn-primary"
        >
          Practice Another Question
        </button>
        <button
          onClick={() => navigate('/progress')}
          className="btn-secondary"
        >
          View Progress
        </button>
      </div>
    </div>
  );
};

export default Evaluate; 
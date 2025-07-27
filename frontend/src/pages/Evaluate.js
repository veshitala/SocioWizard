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
  Star
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
        question: location.state.question
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

  const { evaluation, answer, question } = evaluationData;

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
      <div className="card bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
        <div className="text-center">
          <div className="flex items-center justify-center mb-2">
            <Star className="h-6 w-6 text-yellow-500 mr-2" />
            <h2 className="text-2xl font-bold text-gray-900">Overall Score</h2>
          </div>
          <div className={`text-5xl font-bold ${getScoreColor(evaluation.overall_score)}`}>
            {evaluation.overall_score.toFixed(1)}
          </div>
          <div className="text-lg text-gray-600">out of 10</div>
          <p className="text-sm text-gray-500 mt-2">
            Submitted on {new Date(answer.submitted_at).toLocaleDateString()}
          </p>
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
          'Completeness, accuracy, and relevance of information'
        )}
        {renderScoreCard(
          'Sociological Depth',
          evaluation.sociological_depth_score,
          'Use of theories, concepts, and sociological perspective'
        )}
      </div>

      {/* Detailed Feedback */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Lightbulb className="h-5 w-5 text-yellow-500 mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Detailed Feedback</h3>
        </div>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">{evaluation.feedback}</p>
        </div>
      </div>

      {/* Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Keywords Used */}
        <div className="card">
          <div className="flex items-center mb-4">
            <BookOpen className="h-5 w-5 text-blue-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Keywords Used</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {evaluation.keywords_used && evaluation.keywords_used.length > 0 ? (
              evaluation.keywords_used.map((keyword, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                >
                  {keyword}
                </span>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No specific keywords identified</p>
            )}
          </div>
        </div>

        {/* Thinkers Mentioned */}
        <div className="card">
          <div className="flex items-center mb-4">
            <Users className="h-5 w-5 text-green-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Thinkers Mentioned</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {evaluation.thinkers_mentioned && evaluation.thinkers_mentioned.length > 0 ? (
              evaluation.thinkers_mentioned.map((thinker, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full"
                >
                  {thinker}
                </span>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No specific thinkers mentioned</p>
            )}
          </div>
        </div>

        {/* Theories Referenced */}
        <div className="card">
          <div className="flex items-center mb-4">
            <TrendingUp className="h-5 w-5 text-purple-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Theories Referenced</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {evaluation.theories_referenced && evaluation.theories_referenced.length > 0 ? (
              evaluation.theories_referenced.map((theory, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full"
                >
                  {theory}
                </span>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No specific theories referenced</p>
            )}
          </div>
        </div>
      </div>

      {/* Your Answer */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Answer</h3>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-gray-700 whitespace-pre-wrap">{answer.answer_text}</p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => navigate('/practice')}
          className="btn-primary flex items-center"
        >
          <BookOpen className="h-4 w-4 mr-2" />
          Practice Another Question
        </button>
        <button
          onClick={() => navigate('/progress')}
          className="btn-secondary flex items-center"
        >
          <TrendingUp className="h-4 w-4 mr-2" />
          View Progress
        </button>
      </div>
    </div>
  );
};

export default Evaluate; 
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../services/apiService';
import { 
  BookOpen, 
  TrendingUp, 
  Target, 
  Calendar,
  ArrowRight,
  Lightbulb,
  Activity
} from 'lucide-react';

const Dashboard = () => {
  const [progressSummary, setProgressSummary] = useState(null);
  const [recentAnswers, setRecentAnswers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [summary, answers] = await Promise.all([
          apiService.getProgressSummary(),
          apiService.getAnswerHistory({ limit: 5 })
        ]);
        
        setProgressSummary(summary.summary);
        setRecentAnswers(answers.answers);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const dailyTip = "Remember to structure your answers with a clear introduction, body, and conclusion. Use relevant sociological theories and thinkers to demonstrate depth of understanding.";

  const quickActions = [
    {
      title: 'Practice Answer',
      description: 'Get a random PYQ to practice',
      icon: BookOpen,
      href: '/practice',
      color: 'bg-blue-500'
    },
    {
      title: 'View Progress',
      description: 'Check your performance trends',
      icon: TrendingUp,
      href: '/progress',
      color: 'bg-green-500'
    },
    {
      title: 'Browse PYQs',
      description: 'Explore question database',
      icon: Target,
      href: '/pyqs',
      color: 'bg-purple-500'
    }
  ];

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
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome back! Here's your UPSC Sociology progress overview.</p>
      </div>

      {/* Progress Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BookOpen className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Answers</p>
              <p className="text-2xl font-bold text-gray-900">
                {progressSummary?.total_answers || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Average Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {progressSummary?.average_scores?.overall?.toFixed(1) || '0.0'}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Target className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Topics Covered</p>
              <p className="text-2xl font-bold text-gray-900">
                {progressSummary?.topics_practiced || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Calendar className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Recent Activity</p>
              <p className="text-2xl font-bold text-gray-900">
                {progressSummary?.recent_answers || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-1">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              {quickActions.map((action) => (
                <Link
                  key={action.title}
                  to={action.href}
                  className="flex items-center p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
                >
                  <div className={`p-2 rounded-lg ${action.color}`}>
                    <action.icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="ml-3 flex-1">
                    <p className="text-sm font-medium text-gray-900">{action.title}</p>
                    <p className="text-xs text-gray-500">{action.description}</p>
                  </div>
                  <ArrowRight className="h-4 w-4 text-gray-400" />
                </Link>
              ))}
            </div>
          </div>
        </div>

        {/* Daily Tip */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="flex items-center mb-4">
              <Lightbulb className="h-5 w-5 text-yellow-500 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Daily Tip</h3>
            </div>
            <p className="text-gray-700 text-sm leading-relaxed">{dailyTip}</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Activity className="h-5 w-5 text-gray-500 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
              </div>
              <Link to="/progress" className="text-sm text-primary-600 hover:text-primary-500">
                View all
              </Link>
            </div>
            <div className="space-y-3">
              {recentAnswers.length > 0 ? (
                recentAnswers.map((answer) => (
                  <div key={answer.id} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1 min-w-0">
                        <p 
                          className="text-sm font-medium text-gray-900 leading-tight overflow-hidden cursor-help" 
                          style={{
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical'
                          }}
                          title={answer.question?.question_text || 'Question not available'}
                        >
                          {answer.question?.question_text || 'Question not available'}
                        </p>
                      </div>
                      <div className="text-xs text-gray-400 ml-2 flex-shrink-0">
                        {new Date(answer.submitted_at).toLocaleDateString()}
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <p className="text-xs text-gray-500">
                        Score: {answer.overall_score?.toFixed(1) || 'N/A'}
                      </p>
                      <p className="text-xs text-gray-400">
                        {answer.topic || 'General'}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500 text-center py-4">
                  No recent activity. Start practicing to see your progress here!
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Best Performing Topic */}
      {progressSummary?.best_topic?.name && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Best Topic</h3>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Best Performing Topic</p>
              <p className="text-xl font-bold text-gray-900">{progressSummary.best_topic.name}</p>
              <p className="text-sm text-gray-500">
                Average Score: {progressSummary.best_topic.score.toFixed(1)}/10
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-green-600">
                {((progressSummary.best_topic.score / 10) * 100).toFixed(0)}%
              </div>
              <p className="text-sm text-gray-500">Performance</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 
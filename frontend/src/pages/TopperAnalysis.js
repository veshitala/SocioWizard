import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/apiService';

const TopperAnalysis = () => {
    const { user } = useAuth();
    const [analysisHistory, setAnalysisHistory] = useState([]);
    const [similarityStats, setSimilarityStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedAnalysis, setSelectedAnalysis] = useState(null);
    const [showAnalysis, setShowAnalysis] = useState(false);

    useEffect(() => {
        loadAnalysisData();
    }, []);

    const loadAnalysisData = async () => {
        try {
            setLoading(true);
            const [historyResponse, statsResponse] = await Promise.all([
                apiService.get('/topper-analysis/user-analysis-history'),
                apiService.get('/topper-analysis/similarity-stats')
            ]);

            if (historyResponse.data) {
                setAnalysisHistory(historyResponse.data.analysis_history || []);
            }

            if (statsResponse.data) {
                setSimilarityStats(statsResponse.data);
            }
        } catch (error) {
            console.error('Error loading analysis data:', error);
        } finally {
            setLoading(false);
        }
    };

    const analyzeAnswer = async (answerId) => {
        try {
            setLoading(true);
            const response = await apiService.get(`/topper-analysis/analyze/${answerId}`);
            
            if (response.data) {
                setSelectedAnalysis(response.data);
                setShowAnalysis(true);
            }
        } catch (error) {
            console.error('Error analyzing answer:', error);
        } finally {
            setLoading(false);
        }
    };

    const getSimilarityColor = (score) => {
        if (score >= 0.7) return 'text-green-600';
        if (score >= 0.5) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getSimilarityLabel = (score) => {
        if (score >= 0.7) return 'Excellent';
        if (score >= 0.5) return 'Good';
        if (score >= 0.3) return 'Fair';
        return 'Needs Improvement';
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }



    return (
        <div className="p-6 max-w-7xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Topper Answer Analysis</h1>
                <p className="text-gray-600">
                    Compare your answers with topper responses and get personalized feedback
                </p>
            </div>

            {/* Similarity Statistics */}
            {similarityStats && (
                <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h2 className="text-xl font-semibold mb-4">Your Performance Overview</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div className="text-center">
                            <div className="text-3xl font-bold text-blue-600">
                                {similarityStats.total_analyses}
                            </div>
                            <div className="text-sm text-gray-600">Total Analyses</div>
                        </div>
                        <div className="text-center">
                            <div className={`text-3xl font-bold ${getSimilarityColor(similarityStats.average_similarity)}`}>
                                {(similarityStats.average_similarity * 100).toFixed(1)}%
                            </div>
                            <div className="text-sm text-gray-600">Average Similarity</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-semibold text-green-600">
                                {similarityStats.strength_areas?.length || 0}
                            </div>
                            <div className="text-sm text-gray-600">Strength Areas</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-semibold text-red-600">
                                {similarityStats.weakness_areas?.length || 0}
                            </div>
                            <div className="text-sm text-gray-600">Areas to Improve</div>
                        </div>
                    </div>

                    {/* Detailed Averages */}
                    {similarityStats.detailed_averages && (
                        <div className="mt-6">
                            <h3 className="text-lg font-semibold mb-3">Detailed Performance</h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {Object.entries(similarityStats.detailed_averages).map(([key, value]) => (
                                    <div key={key} className="bg-gray-50 rounded-lg p-3">
                                        <div className="text-sm text-gray-600 capitalize">
                                            {key.replace('_', ' ')}
                                        </div>
                                        <div className={`text-lg font-semibold ${getSimilarityColor(value)}`}>
                                            {(value * 100).toFixed(1)}%
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Strength and Weakness Areas */}
                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                        {similarityStats.strength_areas && similarityStats.strength_areas.length > 0 && (
                            <div>
                                <h3 className="text-lg font-semibold text-green-600 mb-2">Your Strengths</h3>
                                <div className="space-y-1">
                                    {similarityStats.strength_areas.map((area, index) => (
                                        <div key={index} className="flex items-center text-green-700">
                                            <span className="mr-2">✓</span>
                                            {area}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {similarityStats.weakness_areas && similarityStats.weakness_areas.length > 0 && (
                            <div>
                                <h3 className="text-lg font-semibold text-red-600 mb-2">Areas to Improve</h3>
                                <div className="space-y-1">
                                    {similarityStats.weakness_areas.map((area, index) => (
                                        <div key={index} className="flex items-center text-red-700">
                                            <span className="mr-2">⚠</span>
                                            {area}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Analysis History */}
            <div className="bg-white rounded-lg shadow-md">
                <div className="p-6 border-b">
                    <h2 className="text-xl font-semibold">Analysis History</h2>
                </div>
                
                {analysisHistory.length === 0 ? (
                    <div className="p-6 text-center text-gray-500">
                        <p>No analysis history found. Submit answers to get started!</p>
                    </div>
                ) : (
                    <div className="divide-y">
                        {analysisHistory.map((analysis) => (
                            <div key={analysis.analysis_id} className="p-6 hover:bg-gray-50">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex-1">
                                        <h3 className="font-semibold text-lg mb-2">
                                            Question Analysis
                                        </h3>
                                        <p className="text-gray-600 text-sm mb-2">
                                            {analysis.user_answer_preview}
                                        </p>
                                        <div className="flex items-center text-sm text-gray-500">
                                            <span>Topper: {analysis.topper_answer.topper_name}</span>
                                            <span className="mx-2">•</span>
                                            <span>Rank: {analysis.topper_answer.rank}</span>
                                            <span className="mx-2">•</span>
                                            <span>Year: {analysis.topper_answer.year}</span>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className={`text-2xl font-bold ${getSimilarityColor(analysis.similarity_scores.overall_similarity)}`}>
                                            {(analysis.similarity_scores.overall_similarity * 100).toFixed(1)}%
                                        </div>
                                        <div className="text-sm text-gray-600">
                                            {getSimilarityLabel(analysis.similarity_scores.overall_similarity)}
                                        </div>
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                                    {Object.entries(analysis.similarity_scores).map(([key, value]) => (
                                        <div key={key} className="text-center">
                                            <div className={`text-lg font-semibold ${getSimilarityColor(value)}`}>
                                                {(value * 100).toFixed(1)}%
                                            </div>
                                            <div className="text-xs text-gray-600 capitalize">
                                                {key.replace('_', ' ')}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="flex justify-between items-center">
                                    <div className="flex-1">
                                        <p className="text-sm text-gray-700 mb-2">
                                            {analysis.feedback.text}
                                        </p>
                                        {analysis.feedback.suggestions && analysis.feedback.suggestions.length > 0 && (
                                            <div className="text-xs text-gray-600">
                                                <strong>Suggestions:</strong> {analysis.feedback.suggestions.join(', ')}
                                            </div>
                                        )}
                                    </div>
                                    <button
                                        onClick={() => {
                                            setSelectedAnalysis(analysis);
                                            setShowAnalysis(true);
                                        }}
                                        className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                                    >
                                        View Details
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Detailed Analysis Modal */}
            {showAnalysis && selectedAnalysis && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="p-6 border-b">
                            <div className="flex justify-between items-center">
                                <h2 className="text-xl font-semibold">Detailed Analysis</h2>
                                <button
                                    onClick={() => setShowAnalysis(false)}
                                    className="text-gray-500 hover:text-gray-700"
                                >
                                    ✕
                                </button>
                            </div>
                        </div>

                        <div className="p-6">
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {/* User Answer */}
                                <div>
                                    <h3 className="font-semibold mb-3">Your Answer</h3>
                                    <div className="bg-gray-50 rounded-lg p-4 text-sm">
                                        {selectedAnalysis.user_answer_preview || 'Answer text not available'}
                                    </div>
                                </div>

                                {/* Topper Answer */}
                                <div>
                                    <h3 className="font-semibold mb-3">Topper Answer</h3>
                                    <div className="bg-green-50 rounded-lg p-4 text-sm">
                                        {selectedAnalysis.topper_answer?.answer_text || 'Topper answer not available'}
                                    </div>
                                </div>
                            </div>

                            {/* Similarity Scores */}
                            <div className="mt-6">
                                <h3 className="font-semibold mb-3">Similarity Analysis</h3>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    {Object.entries(selectedAnalysis.similarity_scores).map(([key, value]) => (
                                        <div key={key} className="bg-gray-50 rounded-lg p-4 text-center">
                                            <div className={`text-2xl font-bold ${getSimilarityColor(value)}`}>
                                                {(value * 100).toFixed(1)}%
                                            </div>
                                            <div className="text-sm text-gray-600 capitalize">
                                                {key.replace('_', ' ')}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Feedback */}
                            <div className="mt-6">
                                <h3 className="font-semibold mb-3">Feedback & Suggestions</h3>
                                <div className="bg-blue-50 rounded-lg p-4">
                                    <p className="text-gray-800 mb-3">{selectedAnalysis.feedback.text}</p>
                                    {selectedAnalysis.feedback.suggestions && selectedAnalysis.feedback.suggestions.length > 0 && (
                                        <div>
                                            <h4 className="font-semibold text-sm mb-2">Improvement Suggestions:</h4>
                                            <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                                {selectedAnalysis.feedback.suggestions.map((suggestion, index) => (
                                                    <li key={index}>{suggestion}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TopperAnalysis; 
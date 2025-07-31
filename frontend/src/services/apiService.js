import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Questions
  async getRandomQuestion(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/questions/random?${params}`);
    return response.data;
  },

  async getThemes() {
    const response = await api.get('/questions/themes');
    return response.data;
  },

  async getTopics() {
    const response = await api.get('/questions/topics');
    return response.data;
  },

  async getYears() {
    const response = await api.get('/questions/years');
    return response.data;
  },

  async searchQuestions(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/questions/search?${params}`);
    return response.data;
  },

  // Answers
  async submitAnswer(answerData) {
    const response = await api.post('/answers/submit', answerData);
    return response.data;
  },

  async getAnswerHistory(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/answers/history?${params}`);
    return response.data;
  },

  async getAnswer(answerId) {
    const response = await api.get(`/answers/${answerId}`);
    return response.data;
  },

  async getUserTopics() {
    const response = await api.get('/answers/topics');
    return response.data;
  },

  // File Upload
  async uploadAnswerFile(file, questionId) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question_id', questionId);
    
    const response = await api.post('/file-upload/upload-answer', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getAISuggestions(answerText, questionId) {
    const response = await api.post('/file-upload/get-suggestions', {
      answer_text: answerText,
      question_id: questionId
    });
    return response.data;
  },

  async downloadAnswerFile(answerId) {
    const response = await api.get(`/file-upload/download/${answerId}`);
    return response.data;
  },

  // Progress
  async getProgressSummary() {
    const response = await api.get('/progress/summary');
    return response.data;
  },

  async getProgressTimeline(days = 30) {
    const response = await api.get(`/progress/timeline?days=${days}`);
    return response.data;
  },

  async getTopicProgress() {
    const response = await api.get('/progress/topics');
    return response.data;
  },

  async getStreak() {
    const response = await api.get('/progress/streak');
    return response.data;
  },

  // Syllabus Progress
  async getSyllabusOverview() {
    const response = await api.get('/syllabus-progress/syllabus-overview');
    return response.data;
  },

  async getTopicSubtopicsProgress(topicId) {
    const response = await api.get(`/syllabus-progress/topic/${topicId}/subtopics`);
    return response.data;
  },

  async getStrengthAnalysis() {
    const response = await api.get('/syllabus-progress/strength-analysis');
    return response.data;
  },

  async getRecommendations() {
    const response = await api.get('/syllabus-progress/recommendations');
    return response.data;
  },

  // Topper Analysis
  async analyzeAnswer(answerId) {
    const response = await api.get(`/topper-analysis/analyze/${answerId}`);
    return response.data;
  },

  async getTopperAnswers(questionId) {
    const response = await api.get(`/topper-analysis/topper-answers/${questionId}`);
    return response.data;
  },

  async getUserAnalysisHistory() {
    const response = await api.get('/topper-analysis/user-analysis-history');
    return response.data;
  },

  async getSimilarityStats() {
    const response = await api.get('/topper-analysis/similarity-stats');
    return response.data;
  },

  async addTopperAnswer(data) {
    const response = await api.post('/topper-analysis/add-topper-answer', data);
    return response.data;
  },
}; 
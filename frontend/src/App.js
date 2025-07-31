import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AnswerPractice from './pages/AnswerPractice';
import Evaluate from './pages/Evaluate';
import Progress from './pages/Progress';
import SyllabusProgress from './pages/SyllabusProgress';
import TopperAnalysis from './pages/TopperAnalysis';
import PYQs from './pages/PYQs';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/practice" element={<AnswerPractice />} />
        <Route path="/evaluate" element={<Evaluate />} />
        <Route path="/progress" element={<Progress />} />
                    <Route path="/syllabus-progress" element={<SyllabusProgress />} />
            <Route path="/topper-analysis" element={<TopperAnalysis />} />
            <Route path="/pyqs" element={<PYQs />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

export default App; 
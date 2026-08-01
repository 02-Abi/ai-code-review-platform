import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import Navbar from './components/common/Navbar';
import AnimatedHero from './components/AnimatedHero';
import AnimatedLogin from './components/auth/AnimatedLogin';
import AnimatedRegister from './components/auth/AnimatedRegister';
import StudentDashboard3D from './pages/StudentDashboard3D';
import AdminDashboard from './pages/AdminDashboard';
import CodeSubmission from './components/student/CodeSubmission';
import ReviewHistory from './components/student/ReviewHistory';
import SubmissionDetail from './pages/SubmissionDetail';
import Profile from './pages/Profile';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#64ffda' },
    secondary: { main: '#00b4d8' },
    background: { default: '#0a0a0a' },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Navbar />
          <ToastContainer position="top-right" autoClose={3000} theme="dark" />
          <Routes>
            <Route path="/" element={<AnimatedHero />} />
            <Route path="/login" element={<AnimatedLogin />} />
            <Route path="/register" element={<AnimatedRegister />} />
            <Route path="/dashboard" element={
              <ProtectedRoute requiredRole="student">
                <StudentDashboard3D />
              </ProtectedRoute>
            } />
            <Route path="/submit-code" element={
              <ProtectedRoute requiredRole="student">
                <CodeSubmission />
              </ProtectedRoute>
            } />
            <Route path="/history" element={
              <ProtectedRoute requiredRole="student">
                <ReviewHistory />
              </ProtectedRoute>
            } />
            <Route path="/submission/:id" element={
              <ProtectedRoute requiredRole="student">
                <SubmissionDetail />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute requiredRole="student">
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/admin" element={
              <ProtectedRoute requiredRole="admin">
                <AdminDashboard />
              </ProtectedRoute>
            } />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
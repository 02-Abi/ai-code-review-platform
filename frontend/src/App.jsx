// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import { useNavigate } from 'react-router-dom';

// Import MUI components
import {
    Box,
    Container,
    Typography,
    Button,
    Grid,
    Card,
    CardContent,
    Paper,
    Chip,
} from '@mui/material';

// Import icons
import CodeIcon from '@mui/icons-material/Code';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

// Import motion
import { motion } from 'framer-motion';

// Auth Pages
import AnimatedLogin from './components/auth/AnimatedLogin';
import Register from './components/auth/Register';

// Student Pages
import StudentDashboard3D from './pages/StudentDashboard3D';
import CodeSubmission from './components/student/CodeSubmission';
import SubmissionDetail from './pages/SubmissionDetail';
import ReviewHistory from './components/student/ReviewHistory';
import Profile from './pages/Profile';

// Admin Pages
import AdminDashboard from './pages/AdminDashboard';

// ✅ Landing Page Component - WITHOUT useAuth
const LandingPage = () => {
    const navigate = useNavigate();

    const features = [
        {
            icon: <AutoAwesomeIcon sx={{ fontSize: 40, color: '#64ffda' }} />,
            title: 'AI-Powered Reviews',
            description: 'Get intelligent code reviews using advanced AI models that understand context and best practices.'
        },
        {
            icon: <SecurityIcon sx={{ fontSize: 40, color: '#ff6b6b' }} />,
            title: 'Security Analysis',
            description: 'Detect vulnerabilities, hardcoded credentials, SQL injection risks, and other security issues.'
        },
        {
            icon: <SpeedIcon sx={{ fontSize: 40, color: '#ffd93d' }} />,
            title: 'Instant Feedback',
            description: 'Get detailed feedback on your code quality, performance, and maintainability in seconds.'
        },
        {
            icon: <CheckCircleIcon sx={{ fontSize: 40, color: '#4ecdc4' }} />,
            title: 'Comprehensive Reports',
            description: 'Receive detailed reports with bugs, issues, suggestions, and test cases for your code.'
        }
    ];

    const languages = [
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'C',
        'Rust', 'Go', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala',
        'Perl', 'Lua', 'R', 'Dart', 'Elixir', 'Haskell', 'Julia',
        'Shell', 'SQL', 'HTML', 'CSS', 'JSON'
    ];

    const handleGetStarted = () => {
        navigate('/login');
    };

    return (
        <Box sx={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%)',
        }}>
            <Container maxWidth="lg" sx={{ pt: 8, pb: 6 }}>
                <motion.div
                    initial={{ y: -50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8 }}
                >
                    <Box sx={{ textAlign: 'center', mb: 6 }}>
                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <Box
                                sx={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    width: 100,
                                    height: 100,
                                    borderRadius: '50%',
                                    background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                                    mb: 3,
                                }}
                            >
                                <CodeIcon sx={{ fontSize: 50, color: '#000' }} />
                            </Box>
                        </motion.div>

                        <Typography
                            variant="h1"
                            sx={{
                                color: '#fff',
                                fontWeight: 'bold',
                                fontSize: { xs: '2.5rem', md: '4rem' },
                                mb: 2,
                            }}
                        >
                            AI Code Review
                            <Box
                                component="span"
                                sx={{
                                    background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent',
                                }}
                            >
                                {' '}Platform
                            </Box>
                        </Typography>

                        <Typography
                            variant="h5"
                            sx={{
                                color: 'rgba(255,255,255,0.7)',
                                maxWidth: '600px',
                                mx: 'auto',
                                mb: 4,
                            }}
                        >
                            Get AI-powered code reviews with detailed analysis, bug detection, and improvement suggestions for 26+ programming languages.
                        </Typography>

                        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                                <Button
                                    variant="contained"
                                    size="large"
                                    onClick={handleGetStarted}
                                    sx={{
                                        background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                                        color: '#000',
                                        fontWeight: 'bold',
                                        px: 4,
                                        py: 1.5,
                                        '&:hover': {
                                            background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                                        },
                                    }}
                                >
                                    Get Started
                                </Button>
                            </motion.div>
                            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                                <Button
                                    variant="outlined"
                                    size="large"
                                    onClick={() => navigate('/register')}
                                    sx={{
                                        borderColor: '#64ffda',
                                        color: '#64ffda',
                                        px: 4,
                                        py: 1.5,
                                        '&:hover': {
                                            borderColor: '#00b4d8',
                                            color: '#00b4d8',
                                            backgroundColor: 'rgba(100,255,218,0.1)',
                                        },
                                    }}
                                >
                                    Sign Up
                                </Button>
                            </motion.div>
                        </Box>
                    </Box>

                    {/* Stats */}
                    <Grid container spacing={3} sx={{ mb: 6 }}>
                        {[
                            { value: '26+', label: 'Languages Supported' },
                            { value: 'AI', label: 'Powered Reviews' },
                            { value: 'Instant', label: 'Real-time Feedback' },
                            { value: 'Free', label: 'Start Today' },
                        ].map((stat, index) => (
                            <Grid item xs={6} sm={3} key={index}>
                                <Paper sx={{ p: 3, textAlign: 'center', background: 'rgba(255,255,255,0.05)' }}>
                                    <Typography variant="h3" sx={{ color: '#64ffda', fontWeight: 'bold' }}>
                                        {stat.value}
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                                        {stat.label}
                                    </Typography>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>

                    {/* Features */}
                    <Typography variant="h3" sx={{ color: '#fff', textAlign: 'center', mb: 4, fontWeight: 'bold' }}>
                        Features
                    </Typography>
                    <Grid container spacing={3}>
                        {features.map((feature, index) => (
                            <Grid item xs={12} sm={6} md={3} key={index}>
                                <motion.div
                                    initial={{ y: 50, opacity: 0 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{ duration: 0.5, delay: index * 0.1 }}
                                    whileHover={{ y: -10, scale: 1.02 }}
                                >
                                    <Card sx={{
                                        height: '100%',
                                        background: 'rgba(255,255,255,0.03)',
                                        backdropFilter: 'blur(10px)',
                                        borderRadius: 3,
                                        border: '1px solid rgba(255,255,255,0.05)',
                                        '&:hover': {
                                            borderColor: 'rgba(100,255,218,0.2)',
                                            boxShadow: '0 10px 40px rgba(100,255,218,0.1)',
                                        },
                                    }}>
                                        <CardContent sx={{ textAlign: 'center', p: 3 }}>
                                            <Box sx={{ mb: 2 }}>
                                                {feature.icon}
                                            </Box>
                                            <Typography variant="h6" sx={{ color: '#fff', mb: 1, fontWeight: 'bold' }}>
                                                {feature.title}
                                            </Typography>
                                            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)' }}>
                                                {feature.description}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </motion.div>
                            </Grid>
                        ))}
                    </Grid>

                    {/* Supported Languages */}
                    <Typography variant="h3" sx={{ color: '#fff', textAlign: 'center', mt: 6, mb: 3, fontWeight: 'bold' }}>
                        Supported Languages
                    </Typography>
                    <Paper sx={{
                        p: 3,
                        background: 'rgba(255,255,255,0.03)',
                        borderRadius: 3,
                        border: '1px solid rgba(255,255,255,0.05)',
                    }}>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
                            {languages.map((lang, index) => (
                                <Chip
                                    key={index}
                                    label={lang}
                                    sx={{
                                        color: '#fff',
                                        borderColor: 'rgba(100,255,218,0.3)',
                                        '&:hover': {
                                            borderColor: '#64ffda',
                                            backgroundColor: 'rgba(100,255,218,0.1)',
                                        },
                                    }}
                                    variant="outlined"
                                />
                            ))}
                        </Box>
                    </Paper>

                    {/* Footer */}
                    <Box sx={{ mt: 6, textAlign: 'center' }}>
                        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.3)' }}>
                            © 2024 AI Code Review Platform. All rights reserved.
                        </Typography>
                    </Box>
                </motion.div>
            </Container>
        </Box>
    );
};

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#64ffda',
        },
        secondary: {
            main: '#00b4d8',
        },
        background: {
            default: '#0a0a0f',
            paper: 'rgba(255,255,255,0.05)',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
});

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <AuthProvider>
                    <Routes>
                        {/* ✅ PUBLIC ROUTES - No authentication required */}
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/login" element={<AnimatedLogin />} />
                        <Route path="/register" element={<Register />} />

                        {/* ✅ PROTECTED ROUTES - Require authentication */}
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <StudentDashboard3D />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/admin"
                            element={
                                <ProtectedRoute>
                                    <AdminDashboard />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/submit"
                            element={
                                <ProtectedRoute>
                                    <CodeSubmission />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/submit-code"
                            element={
                                <ProtectedRoute>
                                    <CodeSubmission />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/review/:id"
                            element={
                                <ProtectedRoute>
                                    <SubmissionDetail />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/history"
                            element={
                                <ProtectedRoute>
                                    <ReviewHistory />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/profile"
                            element={
                                <ProtectedRoute>
                                    <Profile />
                                </ProtectedRoute>
                            }
                        />

                        {/* Fallback */}
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>

                    <ToastContainer
                        position="top-right"
                        autoClose={3000}
                        hideProgressBar={false}
                        newestOnTop
                        closeOnClick
                        rtl={false}
                        pauseOnFocusLoss
                        draggable
                        pauseOnHover
                        theme="dark"
                    />
                </AuthProvider>
            </Router>
        </ThemeProvider>
    );
}

export default App;
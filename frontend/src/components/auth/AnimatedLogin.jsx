import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  Link as MuiLink,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import ParticleBackground from '../3d/ParticleBackground';
import { toast } from 'react-toastify';

const AnimatedLogin = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(formData.username, formData.password);
      console.log('Login result:', result);
      
      if (result.success) {
        toast.success('✅ Login successful! Welcome back!');
        setTimeout(() => {
          navigate(result.user.user_type === 'admin' ? '/admin' : '/dashboard');
        }, 500);
      } else {
        setError(result.error || 'Login failed. Please check your credentials.');
        toast.error(result.error || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An unexpected error occurred. Please try again.');
      toast.error('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <ParticleBackground />
      
      <Container component="main" maxWidth="xs" sx={{ position: 'relative', zIndex: 1 }}>
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, type: 'spring' }}
        >
          <Paper
            elevation={24}
            sx={{
              p: 4,
              background: 'rgba(255, 255, 255, 0.05)',
              backdropFilter: 'blur(20px)',
              borderRadius: 4,
              border: '1px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Typography
                component="h1"
                variant="h4"
                align="center"
                sx={{
                  background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 'bold',
                  mb: 1,
                }}
              >
                Welcome Back
              </Typography>
            </motion.div>
            
            <Typography
              variant="body2"
              align="center"
              sx={{ color: 'rgba(255,255,255,0.7)', mb: 3 }}
            >
              Sign in to access your AI Code Review dashboard
            </Typography>

            {error && (
              <motion.div
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
              >
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              </motion.div>
            )}

            <form onSubmit={handleSubmit}>
              <motion.div
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
              >
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  autoComplete="username"
                  autoFocus
                  value={formData.username}
                  onChange={handleChange}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      color: '#fff',
                      '& fieldset': {
                        borderColor: 'rgba(255,255,255,0.2)',
                      },
                      '&:hover fieldset': {
                        borderColor: '#64ffda',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: '#64ffda',
                      },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255,255,255,0.7)',
                      '&.Mui-focused': {
                        color: '#64ffda',
                      },
                    },
                  }}
                />
              </motion.div>
              
              <motion.div
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  autoComplete="current-password"
                  value={formData.password}
                  onChange={handleChange}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          sx={{ color: 'rgba(255,255,255,0.7)' }}
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      color: '#fff',
                      '& fieldset': {
                        borderColor: 'rgba(255,255,255,0.2)',
                      },
                      '&:hover fieldset': {
                        borderColor: '#64ffda',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: '#64ffda',
                      },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255,255,255,0.7)',
                      '&.Mui-focused': {
                        color: '#64ffda',
                      },
                    },
                  }}
                />
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  disabled={loading}
                  sx={{
                    mt: 3,
                    mb: 2,
                    background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                    color: '#000',
                    fontWeight: 'bold',
                    py: 1.5,
                    '&:hover': {
                      background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                    },
                    '&:disabled': {
                      background: 'rgba(100, 255, 218, 0.3)',
                      color: 'rgba(0,0,0,0.5)',
                    },
                  }}
                >
                  {loading ? 'Signing in...' : 'Sign In'}
                </Button>
              </motion.div>

              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <MuiLink
                  component={Link}
                  to="/forgot-password"
                  variant="body2"
                  sx={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none' }}
                >
                  Forgot password?
                </MuiLink>
              </Box>
              <Box sx={{ textAlign: 'center', mt: 1 }}>
                <MuiLink
                  component={Link}
                  to="/register"
                  variant="body2"
                  sx={{ color: '#64ffda', textDecoration: 'none' }}
                >
                  Don't have an account? Sign Up
                </MuiLink>
              </Box>
            </form>
          </Paper>
        </motion.div>
      </Container>
    </Box>
  );
};

export default AnimatedLogin;
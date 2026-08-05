// src/components/auth/Register.jsx
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
  Grid,
  MenuItem,
  LinearProgress,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import ParticleBackground from '../3d/ParticleBackground';
import { toast } from 'react-toastify';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    user_type: 'student',
    college_name: '',
    year_of_study: '',
    branch: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
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

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      toast.error('Passwords do not match');
      setLoading(false);
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      toast.error('Password must be at least 8 characters');
      setLoading(false);
      return;
    }

    try {
      // ✅ Send only the fields the backend expects
      const registerData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirmPassword,  // ✅ Must match backend field name
        first_name: formData.first_name || '',
        last_name: formData.last_name || '',
        user_type: formData.user_type || 'student',
        college_name: formData.college_name || '',
        year_of_study: formData.year_of_study || '',
        branch: formData.branch || '',
      };
      
      console.log('📝 Sending registration data:', registerData);
      
      const result = await register(registerData);
      console.log('📝 Registration result:', result);
      
      if (result.success) {
        toast.success('✅ Registration successful! Welcome!');
        setTimeout(() => {
          navigate('/dashboard');
        }, 1000);
      } else {
        // ✅ Show detailed error
        let errorMsg = result.error || 'Registration failed. Please try again.';
        
        // Check if there are field-specific errors
        if (result.errors) {
          const errorKeys = Object.keys(result.errors);
          if (errorKeys.length > 0) {
            const firstKey = errorKeys[0];
            const firstError = result.errors[firstKey];
            errorMsg = Array.isArray(firstError) ? firstError[0] : firstError;
          }
        }
        
        setError(errorMsg);
        toast.error(errorMsg);
      }
    } catch (err) {
      console.error('❌ Registration error:', err);
      console.error('❌ Error response:', err.response?.data);
      
      let errorMsg = 'Registration failed. Please try again.';
      
      // ✅ Better error handling from backend
      if (err.response?.data?.errors) {
        const errors = err.response.data.errors;
        if (typeof errors === 'string') {
          errorMsg = errors;
        } else if (Array.isArray(errors)) {
          errorMsg = errors[0];
        } else {
          const firstKey = Object.keys(errors)[0];
          if (firstKey && errors[firstKey]) {
            errorMsg = Array.isArray(errors[firstKey]) ? errors[firstKey][0] : errors[firstKey];
          }
        }
      } else if (err.response?.data?.message) {
        errorMsg = err.response.data.message;
      } else if (err.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      }
      
      setError(errorMsg);
      toast.error(errorMsg);
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
        py: 4,
      }}
    >
      <ParticleBackground />
      
      <Container component="main" maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
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
                Create Account
              </Typography>
            </motion.div>
            
            <Typography
              variant="body2"
              align="center"
              sx={{ color: 'rgba(255,255,255,0.7)', mb: 3 }}
            >
              Join the AI Code Review Platform
            </Typography>

            {loading && <LinearProgress sx={{ mb: 2 }} />}

            {error && (
              <motion.div
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
              >
                <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
                  {error}
                </Alert>
              </motion.div>
            )}

            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                {/* Username */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* Email */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* First Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="First Name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* Last Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Last Name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* Password */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
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
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* Confirm Password */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Confirm Password"
                    name="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            sx={{ color: 'rgba(255,255,255,0.7)' }}
                          >
                            {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* User Type */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    select
                    label="User Type"
                    name="user_type"
                    value={formData.user_type}
                    onChange={handleChange}
                    SelectProps={{
                      MenuProps: {
                        PaperProps: {
                          sx: {
                            backgroundColor: '#1a1a2e',
                            color: '#fff',
                            '& .MuiMenuItem-root': {
                              color: '#fff',
                              '&:hover': {
                                backgroundColor: 'rgba(100,255,218,0.1)',
                              },
                              '&.Mui-selected': {
                                backgroundColor: 'rgba(100,255,218,0.2)',
                                color: '#64ffda',
                              },
                            },
                          },
                        },
                      },
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                      '& .MuiSelect-select': { color: '#fff' },
                    }}
                  >
                    <MenuItem value="student" sx={{ color: '#fff' }}>Student</MenuItem>
                    <MenuItem value="admin" sx={{ color: '#fff' }}>Admin</MenuItem>
                  </TextField>
                </Grid>

                {/* College Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="College Name"
                    name="college_name"
                    value={formData.college_name}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>

                {/* Year of Study */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="Year of Study"
                    name="year_of_study"
                    value={formData.year_of_study}
                    onChange={handleChange}
                    SelectProps={{
                      MenuProps: {
                        PaperProps: {
                          sx: {
                            backgroundColor: '#1a1a2e',
                            color: '#fff',
                            '& .MuiMenuItem-root': {
                              color: '#fff',
                              '&:hover': {
                                backgroundColor: 'rgba(100,255,218,0.1)',
                              },
                              '&.Mui-selected': {
                                backgroundColor: 'rgba(100,255,218,0.2)',
                                color: '#64ffda',
                              },
                            },
                          },
                        },
                      },
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                      '& .MuiSelect-select': { color: '#fff' },
                    }}
                  >
                    <MenuItem value="" sx={{ color: '#fff' }}>Select Year</MenuItem>
                    <MenuItem value="1" sx={{ color: '#fff' }}>1st Year</MenuItem>
                    <MenuItem value="2" sx={{ color: '#fff' }}>2nd Year</MenuItem>
                    <MenuItem value="3" sx={{ color: '#fff' }}>3rd Year</MenuItem>
                    <MenuItem value="4" sx={{ color: '#fff' }}>4th Year</MenuItem>
                  </TextField>
                </Grid>

                {/* Branch */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Branch"
                    name="branch"
                    value={formData.branch}
                    onChange={handleChange}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                        '&:hover fieldset': { borderColor: '#64ffda' },
                        '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                      },
                      '& .MuiInputLabel-root': {
                        color: 'rgba(255,255,255,0.7)',
                        '&.Mui-focused': { color: '#64ffda' },
                      },
                    }}
                  />
                </Grid>
              </Grid>

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
                  {loading ? 'Creating Account...' : 'Create Account'}
                </Button>
              </motion.div>

              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <MuiLink
                  component={Link}
                  to="/login"
                  variant="body2"
                  sx={{ color: '#64ffda', textDecoration: 'none' }}
                >
                  Already have an account? Sign In
                </MuiLink>
              </Box>
            </form>
          </Paper>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Register;
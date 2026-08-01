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
  MenuItem,
  InputAdornment,
  IconButton,
  Grid,
  FormControl,
  InputLabel,
  Select,
  FormHelperText,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import ParticleBackground from '../3d/ParticleBackground';
import { toast } from 'react-toastify';

const AnimatedRegister = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    user_type: 'student',
    college_name: '',
    year_of_study: '',
    branch: '',
    company_name: '',
    job_title: '',
    years_of_experience: '',
    skills: '',
  });
  
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateUsername = (value) => {
    if (!value) return 'Username is required';
    if (value.length < 3) return 'Username must be at least 3 characters';
    if (value.length > 20) return 'Username must be less than 20 characters';
    if (!/^[a-zA-Z0-9_]+$/.test(value)) return 'Username can only contain letters, numbers, and underscore';
    return '';
  };

  const validateEmail = (value) => {
    if (!value) return 'Email is required';
    if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value)) return 'Invalid email address';
    return '';
  };

  const validatePassword = (value) => {
    if (!value) return 'Password is required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    if (!/[A-Z]/.test(value)) return 'Password must contain at least one uppercase letter';
    if (!/[a-z]/.test(value)) return 'Password must contain at least one lowercase letter';
    if (!/[0-9]/.test(value)) return 'Password must contain at least one number';
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) return 'Password must contain at least one special character';
    return '';
  };

  const validateConfirmPassword = (value) => {
    if (!value) return 'Please confirm your password';
    if (value !== formData.password) return 'Passwords do not match';
    return '';
  };

  const validateFirstName = (value) => {
    if (!value) return 'First name is required';
    if (value.length < 2) return 'First name must be at least 2 characters';
    if (!/^[a-zA-Z\s]+$/.test(value)) return 'First name can only contain letters';
    return '';
  };

  const validateLastName = (value) => {
    if (!value) return 'Last name is required';
    if (value.length < 2) return 'Last name must be at least 2 characters';
    if (!/^[a-zA-Z\s]+$/.test(value)) return 'Last name can only contain letters';
    return '';
  };

  const validateCollegeName = (value) => {
    if (formData.user_type === 'student' && !value) return 'College name is required for students';
    return '';
  };

  const validateYearOfStudy = (value) => {
    if (formData.user_type === 'student' && !value) return 'Year of study is required';
    if (value && (parseInt(value) < 1 || parseInt(value) > 5)) return 'Year of study must be between 1 and 5';
    return '';
  };

  const validateBranch = (value) => {
    if (formData.user_type === 'student' && !value) return 'Branch is required for students';
    return '';
  };

  const validateCompanyName = (value) => {
    if (formData.user_type === 'professional' && !value) return 'Company name is required';
    return '';
  };

  const validateJobTitle = (value) => {
    if (formData.user_type === 'professional' && !value) return 'Job title is required';
    return '';
  };

  const validateYearsOfExperience = (value) => {
    if (formData.user_type === 'professional' && !value) return 'Years of experience is required';
    if (value && parseInt(value) < 0) return 'Years of experience cannot be negative';
    return '';
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const handleUserTypeChange = (e) => {
    const value = e.target.value;
    setFormData({ 
      ...formData, 
      user_type: value,
      ...(value === 'student' && {
        company_name: '',
        job_title: '',
        years_of_experience: '',
        skills: '',
      }),
      ...(value === 'professional' && {
        college_name: '',
        year_of_study: '',
        branch: '',
      })
    });
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    let error = '';
    
    switch (name) {
      case 'username':
        error = validateUsername(value);
        break;
      case 'email':
        error = validateEmail(value);
        break;
      case 'password':
        error = validatePassword(value);
        break;
      case 'confirm_password':
        error = validateConfirmPassword(value);
        break;
      case 'first_name':
        error = validateFirstName(value);
        break;
      case 'last_name':
        error = validateLastName(value);
        break;
      case 'college_name':
        error = validateCollegeName(value);
        break;
      case 'year_of_study':
        error = validateYearOfStudy(value);
        break;
      case 'branch':
        error = validateBranch(value);
        break;
      case 'company_name':
        error = validateCompanyName(value);
        break;
      case 'job_title':
        error = validateJobTitle(value);
        break;
      case 'years_of_experience':
        error = validateYearsOfExperience(value);
        break;
      default:
        break;
    }
    
    if (error) {
      setErrors({ ...errors, [name]: error });
    } else {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    newErrors.username = validateUsername(formData.username);
    newErrors.email = validateEmail(formData.email);
    newErrors.password = validatePassword(formData.password);
    newErrors.confirm_password = validateConfirmPassword(formData.confirm_password);
    newErrors.first_name = validateFirstName(formData.first_name);
    newErrors.last_name = validateLastName(formData.last_name);
    
    if (formData.user_type === 'student') {
      newErrors.college_name = validateCollegeName(formData.college_name);
      newErrors.year_of_study = validateYearOfStudy(formData.year_of_study);
      newErrors.branch = validateBranch(formData.branch);
    } else {
      newErrors.company_name = validateCompanyName(formData.company_name);
      newErrors.job_title = validateJobTitle(formData.job_title);
      newErrors.years_of_experience = validateYearsOfExperience(formData.years_of_experience);
    }
    
    setErrors(newErrors);
    return Object.values(newErrors).every(error => error === '');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      const registrationData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirm_password,
        first_name: formData.first_name,
        last_name: formData.last_name,
        user_type: formData.user_type,
        ...(formData.user_type === 'student' && {
          college_name: formData.college_name,
          year_of_study: parseInt(formData.year_of_study),
          branch: formData.branch,
        }),
        ...(formData.user_type === 'professional' && {
          company_name: formData.company_name,
          job_title: formData.job_title,
          years_of_experience: parseInt(formData.years_of_experience),
          skills: formData.skills,
        }),
      };
      
      console.log('Sending registration data:', registrationData);
      
      const result = await register(registrationData);
      console.log('Registration result:', result);
      
      if (result.success) {
        toast.success('✅ Registration successful! Please login to continue.');
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        setError(result.error || 'Registration failed. Please try again.');
      }
    } catch (err) {
      console.error('Registration error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
      position: 'relative',
      overflow: 'hidden',
      py: 4,
    }}>
      <ParticleBackground />
      <Container component="main" maxWidth="sm" sx={{ position: 'relative', zIndex: 1 }}>
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, type: 'spring' }}
        >
          <Paper sx={{
            p: 4,
            background: 'rgba(255,255,255,0.05)',
            backdropFilter: 'blur(20px)',
            borderRadius: 4,
            border: '1px solid rgba(255,255,255,0.1)',
            maxHeight: '90vh',
            overflowY: 'auto',
          }}>
            <Typography component="h1" variant="h4" align="center" sx={{
              background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: 'bold',
              mb: 1,
            }}>
              Create Account
            </Typography>
            <Typography variant="body2" align="center" sx={{ color: 'rgba(255,255,255,0.7)', mb: 3 }}>
              Join the AI Code Review Platform
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <form onSubmit={handleSubmit} noValidate>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    label="Username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.username}
                    helperText={errors.username}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.username ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    label="Email Address"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.email}
                    helperText={errors.email}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.email ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="First Name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.first_name}
                    helperText={errors.first_name}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.first_name ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Last Name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.last_name}
                    helperText={errors.last_name}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.last_name ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.password}
                    helperText={errors.password || 'Min 8 chars, uppercase, lowercase, number, special'}
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton onClick={() => setShowPassword(!showPassword)} sx={{ color: 'rgba(255,255,255,0.7)' }}>
                            {showPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.password ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    label="Confirm Password"
                    name="confirm_password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formData.confirm_password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={!!errors.confirm_password}
                    helperText={errors.confirm_password}
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton onClick={() => setShowConfirmPassword(!showConfirmPassword)} sx={{ color: 'rgba(255,255,255,0.7)' }}>
                            {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        color: '#fff',
                        '& fieldset': { borderColor: errors.confirm_password ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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

                <Grid item xs={12}>
                  <FormControl fullWidth error={!!errors.user_type}>
                    <InputLabel sx={{ color: 'rgba(255,255,255,0.7)' }}>User Type</InputLabel>
                    <Select
                      name="user_type"
                      value={formData.user_type}
                      onChange={handleUserTypeChange}
                      label="User Type"
                      sx={{
                        color: '#fff',
                        '& .MuiOutlinedInput-notchedOutline': {
                          borderColor: 'rgba(255,255,255,0.2)',
                        },
                        '&:hover .MuiOutlinedInput-notchedOutline': {
                          borderColor: '#64ffda',
                        },
                        '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                          borderColor: '#64ffda',
                        },
                        '& .MuiSvgIcon-root': {
                          color: '#fff',
                        },
                      }}
                    >
                      <MenuItem value="student">Student</MenuItem>
                      <MenuItem value="professional">Working Professional</MenuItem>
                    </Select>
                    {errors.user_type && <FormHelperText>{errors.user_type}</FormHelperText>}
                  </FormControl>
                </Grid>

                {formData.user_type === 'student' && (
                  <>
                    <Grid item xs={12}>
                      <TextField
                        required
                        fullWidth
                        label="College Name"
                        name="college_name"
                        value={formData.college_name}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.college_name}
                        helperText={errors.college_name}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.college_name ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label="Year of Study"
                        name="year_of_study"
                        type="number"
                        value={formData.year_of_study}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.year_of_study}
                        helperText={errors.year_of_study || '1-5'}
                        inputProps={{ min: 1, max: 5 }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.year_of_study ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label="Branch"
                        name="branch"
                        value={formData.branch}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.branch}
                        helperText={errors.branch}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.branch ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                  </>
                )}

                {formData.user_type === 'professional' && (
                  <>
                    <Grid item xs={12}>
                      <TextField
                        required
                        fullWidth
                        label="Company Name"
                        name="company_name"
                        value={formData.company_name}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.company_name}
                        helperText={errors.company_name}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.company_name ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label="Job Title"
                        name="job_title"
                        value={formData.job_title}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.job_title}
                        helperText={errors.job_title}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.job_title ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                    <Grid item xs={12} sm={6}>
                      <TextField
                        required
                        fullWidth
                        label="Years of Experience"
                        name="years_of_experience"
                        type="number"
                        value={formData.years_of_experience}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={!!errors.years_of_experience}
                        helperText={errors.years_of_experience || '0+ years'}
                        inputProps={{ min: 0 }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            color: '#fff',
                            '& fieldset': { borderColor: errors.years_of_experience ? '#ff6b6b' : 'rgba(255,255,255,0.2)' },
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
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Skills (comma separated)"
                        name="skills"
                        value={formData.skills}
                        onChange={handleChange}
                        placeholder="React, Python, Django, AI/ML"
                        helperText="List your technical skills separated by commas"
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
                  </>
                )}
              </Grid>

              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
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
                      background: 'rgba(100,255,218,0.3)',
                      color: 'rgba(0,0,0,0.5)',
                    },
                  }}
                >
                  {loading ? 'Creating Account...' : 'Create Account'}
                </Button>
              </motion.div>

              <Box sx={{ textAlign: 'center' }}>
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

export default AnimatedRegister;
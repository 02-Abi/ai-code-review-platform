import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Avatar,
  TextField,
  Button,
  Grid,
  Chip,
  Divider,
  LinearProgress,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import { motion } from 'framer-motion';
import { authAPI } from '../api';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [editMode, setEditMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone_number: user?.phone_number || '',
    college_name: user?.college_name || '',
    branch: user?.branch || '',
    year_of_study: user?.year_of_study || '',
    bio: user?.bio || '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const response = await authAPI.updateProfile(formData);
      updateUser(response.data.user);
      toast.success('✅ Profile updated successfully!');
      setEditMode(false);
    } catch (error) {
      console.error('Update failed:', error);
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ 
          p: 4, 
          background: 'rgba(255,255,255,0.05)', 
          backdropFilter: 'blur(10px)', 
          borderRadius: 4, 
          border: '1px solid rgba(255,255,255,0.1)' 
        }}>
          {loading && <LinearProgress sx={{ mb: 2 }} />}
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 4 }}>
            <Avatar
              sx={{
                width: 80,
                height: 80,
                background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                fontSize: 32,
              }}
            >
              {user?.first_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
            </Avatar>
            <Box>
              <Typography variant="h4" sx={{ color: '#fff' }}>
                {user?.first_name || 'User'} {user?.last_name || ''}
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                @{user?.username}
              </Typography>
              <Chip
                label={user?.user_type === 'student' ? 'Student' : 'Professional'}
                color="primary"
                size="small"
                sx={{ mt: 1 }}
              />
            </Box>
          </Box>

          <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', mb: 3 }} />

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="First Name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Last Name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Phone Number"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="College Name"
                name="college_name"
                value={formData.college_name}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Year of Study"
                name="year_of_study"
                type="number"
                value={formData.year_of_study}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Branch"
                name="branch"
                value={formData.branch}
                onChange={handleChange}
                disabled={!editMode}
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
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                disabled={!editMode}
                placeholder="Tell us about yourself..."
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

          <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
            {editMode ? (
              <>
                <Button
                  variant="contained"
                  onClick={handleSave}
                  disabled={loading}
                  sx={{
                    background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                    color: '#000',
                    fontWeight: 'bold',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                    },
                  }}
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setEditMode(false)}
                  sx={{
                    borderColor: 'rgba(255,255,255,0.2)',
                    color: '#fff',
                    '&:hover': {
                      borderColor: '#ff6b6b',
                      color: '#ff6b6b',
                    },
                  }}
                >
                  Cancel
                </Button>
              </>
            ) : (
              <Button
                variant="contained"
                onClick={() => setEditMode(true)}
                sx={{
                  background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                  color: '#000',
                  fontWeight: 'bold',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                  },
                }}
              >
                Edit Profile
              </Button>
            )}
          </Box>
        </Paper>
      </motion.div>
    </Container>
  );
};

export default Profile;
import React, { useEffect, useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  LinearProgress,
  Box,
  Button,
  IconButton,
  TextField,
  InputAdornment,
} from '@mui/material';
import { codeReviewAPI } from '../../api';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';
import HistoryIcon from '@mui/icons-material/History';
import CodeIcon from '@mui/icons-material/Code';
import { toast } from 'react-toastify';
import '../../styles/3d-effects.css';

const ReviewHistory = () => {
  const navigate = useNavigate();
  const [submissions, setSubmissions] = useState([]);
  const [filteredSubmissions, setFilteredSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchSubmissions();
  }, []);

  useEffect(() => {
    if (searchTerm) {
      const filtered = submissions.filter(sub => 
        sub.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sub.language_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sub.username?.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredSubmissions(filtered);
    } else {
      setFilteredSubmissions(submissions);
    }
  }, [searchTerm, submissions]);

  const fetchSubmissions = async () => {
    setLoading(true);
    try {
      const response = await codeReviewAPI.getSubmissions();
      console.log('Submissions response:', response.data);
      
      let submissionsData = [];
      if (Array.isArray(response.data)) {
        submissionsData = response.data;
      } else if (response.data && Array.isArray(response.data.results)) {
        submissionsData = response.data.results;
      } else if (response.data && typeof response.data === 'object') {
        submissionsData = response.data.data || [];
      }
      
      console.log('Submissions data:', submissionsData);
      setSubmissions(submissionsData);
      setFilteredSubmissions(submissionsData);
    } catch (error) {
      console.error('Failed to fetch submissions:', error);
      toast.error('Failed to load review history');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSubmission = async (id, title) => {
    if (!id) return;
    if (window.confirm(`Are you sure you want to delete "${title}"? This action cannot be undone.`)) {
      try {
        console.log('Deleting submission:', id);
        await codeReviewAPI.deleteSubmission(id);
        toast.success('✅ Submission deleted successfully!');
        
        setSubmissions(prev => prev.filter(sub => sub.id !== id));
        setFilteredSubmissions(prev => prev.filter(sub => sub.id !== id));
        
      } catch (error) {
        console.error('Delete failed:', error);
        if (error.response?.status === 404) {
          toast.error('Submission already deleted');
          setSubmissions(prev => prev.filter(sub => sub.id !== id));
          setFilteredSubmissions(prev => prev.filter(sub => sub.id !== id));
        } else if (error.response?.status === 401) {
          toast.error('Please login again');
          navigate('/login');
        } else {
          toast.error('Failed to delete submission');
        }
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'pending': return 'warning';
      case 'processing': return 'info';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return 'N/A';
    }
  };

  if (loading) {
    return (
      <Container>
        <div className="flex justify-center items-center h-64">
          <div className="spinner-3d"></div>
        </div>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        {/* 3D Glass Card */}
        <Paper className="card-3d" sx={{ 
          p: 3, 
          background: 'rgba(255,255,255,0.05)', 
          backdropFilter: 'blur(10px)', 
          borderRadius: 4, 
          border: '1px solid rgba(255,255,255,0.1)' 
        }}>
          {/* 3D Header */}
          <motion.div
            initial={{ scale: 0.95 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300 }}
            className="glass-3d"
            style={{ padding: '16px', borderRadius: '16px', marginBottom: '24px' }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <HistoryIcon sx={{ fontSize: 32, color: '#64ffda' }} />
                <Typography variant="h4" className="text-gradient-3d">
                  Review History
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                <Chip
                  icon={<CodeIcon />}
                  label={`${filteredSubmissions.length} Submissions`}
                  className="badge-3d"
                  sx={{ 
                    background: 'rgba(100,255,218,0.1)',
                    color: '#64ffda',
                    borderColor: '#64ffda',
                  }}
                  variant="outlined"
                />
              </Box>
            </Box>
          </motion.div>

          {/* Search and Actions - 3D */}
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
              <motion.div whileHover={{ scale: 1.02 }} transition={{ type: 'spring', stiffness: 300 }}>
                <TextField
                  placeholder="🔍 Search submissions..."
                  size="small"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input-3d"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon sx={{ color: 'rgba(255,255,255,0.5)' }} />
                      </InputAdornment>
                    ),
                    sx: {
                      color: '#fff',
                      '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                      '&:hover fieldset': { borderColor: '#64ffda' },
                      '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                    },
                  }}
                  InputLabelProps={{
                    sx: { color: 'rgba(255,255,255,0.7)' },
                  }}
                />
              </motion.div>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    variant="contained"
                    startIcon={<RefreshIcon />}
                    onClick={fetchSubmissions}
                    className="btn-3d"
                    sx={{
                      background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                      color: '#000',
                      fontWeight: 'bold',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                      },
                    }}
                  >
                    Refresh
                  </Button>
                </motion.div>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    variant="contained"
                    onClick={() => navigate('/submit-code')}
                    className="btn-3d"
                    sx={{
                      background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                      color: '#000',
                      fontWeight: 'bold',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                      },
                    }}
                  >
                    New Submission
                  </Button>
                </motion.div>
              </Box>
            </Box>
          </motion.div>

          {/* 3D Table */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <TableContainer className="table-3d">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Title</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Language</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Status</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Quality Score</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Bugs Found</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Submitted</TableCell>
                    <TableCell sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {!filteredSubmissions || filteredSubmissions.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} align="center" sx={{ color: 'rgba(255,255,255,0.5)', py: 4 }}>
                        {searchTerm ? '🔍 No submissions match your search' : '📝 No submissions found. Start by submitting your code for review.'}
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredSubmissions.map((submission, index) => (
                      <motion.tr
                        key={submission.id || index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        whileHover={{ 
                          backgroundColor: 'rgba(99, 102, 241, 0.05)',
                          scale: 1.01
                        }}
                        style={{ 
                          transition: 'all 0.3s ease',
                          cursor: 'pointer',
                        }}
                        onClick={() => navigate(`/submission/${submission.id}`)}
                      >
                        <TableCell sx={{ color: '#fff', fontWeight: '500' }}>
                          {submission.title || 'Untitled'}
                        </TableCell>
                        <TableCell>
                          <span className="badge-3d" style={{ 
                            background: 'rgba(255,255,255,0.05)',
                            color: '#64ffda',
                            borderColor: '#64ffda',
                          }}>
                            {submission.language_name || 'N/A'}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={submission.status || 'pending'}
                            color={getStatusColor(submission.status || 'pending')}
                            size="small"
                            className="badge-3d"
                          />
                        </TableCell>
                        <TableCell>
                          {submission.quality_score ? (
                            <span className="badge-3d" style={{ 
                              background: submission.quality_score >= 70 
                                ? 'linear-gradient(135deg, #2e7d32, #66bb6a)'
                                : submission.quality_score >= 50 
                                ? 'linear-gradient(135deg, #ed6c02, #ffa726)'
                                : 'linear-gradient(135deg, #d32f2f, #ef5350)',
                              color: '#fff',
                            }}>
                              {submission.quality_score}%
                            </span>
                          ) : 'N/A'}
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>
                          {submission.bug_count || 0}
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.85rem' }}>
                          {formatDate(submission.created_at)}
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <motion.div whileHover={{ scale: 1.2 }} whileTap={{ scale: 0.9 }}>
                              <IconButton
                                size="small"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  navigate(`/submission/${submission.id}`);
                                }}
                                className="btn-3d"
                                sx={{ 
                                  color: '#64ffda',
                                  '&:hover': {
                                    backgroundColor: 'rgba(100,255,218,0.1)',
                                  }
                                }}
                              >
                                <VisibilityIcon />
                              </IconButton>
                            </motion.div>
                            <motion.div whileHover={{ scale: 1.2 }} whileTap={{ scale: 0.9 }}>
                              <IconButton
                                size="small"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleDeleteSubmission(submission.id, submission.title);
                                }}
                                className="btn-3d"
                                sx={{ 
                                  color: '#ff6b6b',
                                  '&:hover': {
                                    backgroundColor: 'rgba(255,107,107,0.1)',
                                  }
                                }}
                              >
                                <DeleteIcon />
                              </IconButton>
                            </motion.div>
                          </Box>
                        </TableCell>
                      </motion.tr>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </motion.div>
        </Paper>
      </motion.div>
    </Container>
  );
};

export default ReviewHistory;
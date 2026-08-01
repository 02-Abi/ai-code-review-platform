import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  LinearProgress,
  Avatar,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { codeReviewAPI } from '../api';
import { Link, useNavigate } from 'react-router-dom';
import CodeIcon from '@mui/icons-material/Code';
import HistoryIcon from '@mui/icons-material/History';
import BugReportIcon from '@mui/icons-material/BugReport';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';
import RefreshIcon from '@mui/icons-material/Refresh';
import DescriptionIcon from '@mui/icons-material/Description';
import DeleteIcon from '@mui/icons-material/Delete';
import { motion } from 'framer-motion';
import { toast } from 'react-toastify';

const StudentDashboard3D = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    total_submissions: 0,
    completed_reviews: 0,
    total_bugs_found: 0,
    average_quality_score: 0,
    pending_reviews: 0,
  });
  const [recentSubmissions, setRecentSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [openBugsDialog, setOpenBugsDialog] = useState(false);
  const [openCompletedDialog, setOpenCompletedDialog] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      console.log('Fetching dashboard data...');
      
      const statsResponse = await codeReviewAPI.getStats();
      console.log('Stats response:', statsResponse.data);
      
      if (statsResponse.data && statsResponse.data.data) {
        setStats(statsResponse.data.data);
      }
      
      const submissionsResponse = await codeReviewAPI.getSubmissions();
      console.log('Submissions response:', submissionsResponse.data);
      
      let submissionsData = [];
      if (Array.isArray(submissionsResponse.data)) {
        submissionsData = submissionsResponse.data;
      } else if (submissionsResponse.data && Array.isArray(submissionsResponse.data.results)) {
        submissionsData = submissionsResponse.data.results;
      } else if (submissionsResponse.data && typeof submissionsResponse.data === 'object') {
        submissionsData = submissionsResponse.data.data || [];
      }
      
      console.log('Submissions data:', submissionsData);
      setRecentSubmissions(submissionsData.slice(0, 10));
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
    toast.success('Dashboard refreshed!');
  };

  const handleViewSubmission = (id) => {
    if (!id) return;
    navigate(`/submission/${id}`);
  };

  const handleDeleteSubmission = async (id, title) => {
    if (!id) return;
    if (window.confirm(`Are you sure you want to delete "${title}"? This action cannot be undone.`)) {
      try {
        console.log('Deleting submission:', id);
        await codeReviewAPI.deleteSubmission(id);
        toast.success('✅ Submission deleted successfully!');
        
        // Remove from recent submissions list immediately
        setRecentSubmissions(prev => prev.filter(sub => sub.id !== id));
        
        // Refresh stats
        const statsResponse = await codeReviewAPI.getStats();
        if (statsResponse.data && statsResponse.data.data) {
          setStats(statsResponse.data.data);
        }
        
        // Refresh the dashboard data
        await fetchDashboardData();
        
      } catch (error) {
        console.error('Delete failed:', error);
        if (error.response?.status === 404) {
          toast.error('Submission already deleted');
          setRecentSubmissions(prev => prev.filter(sub => sub.id !== id));
          fetchDashboardData();
        } else if (error.response?.status === 401) {
          toast.error('Please login again');
          navigate('/login');
        } else {
          toast.error('Failed to delete submission');
        }
      }
    }
  };

  const handleCardClick = (type) => {
    switch(type) {
      case 'submissions':
        navigate('/history');
        break;
      case 'completed':
        setOpenCompletedDialog(true);
        break;
      case 'bugs':
        setOpenBugsDialog(true);
        break;
      case 'score':
        toast.info('Your average quality score across all submissions');
        break;
      default:
        break;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'pending':
        return 'warning';
      case 'processing':
        return 'info';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getAllBugs = () => {
    const allBugs = [];
    recentSubmissions.forEach(sub => {
      if (sub.analysis_result && sub.analysis_result.bugs) {
        sub.analysis_result.bugs.forEach(bug => {
          allBugs.push({
            ...bug,
            submission_title: sub.title || 'Untitled',
            submission_id: sub.id,
          });
        });
      }
    });
    return allBugs;
  };

  const getCompletedSubmissions = () => {
    return recentSubmissions.filter(sub => sub.status === 'completed');
  };

  const statCards = [
    {
      title: 'Total Submissions',
      value: stats.total_submissions || 0,
      icon: <CodeIcon sx={{ fontSize: 40, color: '#4ecdc4' }} />,
      gradient: 'linear-gradient(135deg, #4ecdc4, #44a08d)',
      description: 'Click to view all submissions',
      action: () => handleCardClick('submissions'),
    },
    {
      title: 'Completed Reviews',
      value: stats.completed_reviews || 0,
      icon: <CheckCircleIcon sx={{ fontSize: 40, color: '#ffd93d' }} />,
      gradient: 'linear-gradient(135deg, #ffd93d, #f6b93b)',
      description: 'Click to view completed reviews',
      action: () => handleCardClick('completed'),
    },
    {
      title: 'Bugs Found',
      value: stats.total_bugs_found || 0,
      icon: <BugReportIcon sx={{ fontSize: 40, color: '#ff6b6b' }} />,
      gradient: 'linear-gradient(135deg, #ff6b6b, #ee5a24)',
      description: 'Click to view all bugs',
      action: () => handleCardClick('bugs'),
    },
    {
      title: 'Quality Score',
      value: `${stats.average_quality_score || 0}%`,
      icon: <TrendingUpIcon sx={{ fontSize: 40, color: '#6c5ce7' }} />,
      gradient: 'linear-gradient(135deg, #6c5ce7, #4834d4)',
      description: 'Average quality score',
      action: () => handleCardClick('score'),
    },
  ];

  if (loading) {
    return (
      <Box sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        flexDirection: 'column',
        gap: 2,
      }}>
        <CircularProgress sx={{ color: '#64ffda' }} />
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
          Loading your dashboard...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
      py: 4,
    }}>
      <Container maxWidth="lg">
        {/* Welcome Section */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <Paper sx={{
            p: 3,
            background: 'rgba(255,255,255,0.05)',
            backdropFilter: 'blur(20px)',
            borderRadius: 4,
            border: '1px solid rgba(255,255,255,0.1)',
            mb: 4,
          }}>
            <Grid container alignItems="center" spacing={3}>
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar
                    sx={{
                      width: 64,
                      height: 64,
                      background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                      fontSize: 28,
                      fontWeight: 'bold',
                    }}
                  >
                    {user?.first_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
                  </Avatar>
                  <Box>
                    <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
                      Welcome back, {user?.first_name || user?.username || 'User'}!
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                      {user?.user_type === 'student' ? 'Student' : 'Professional'} • 
                      {user?.college_name || user?.company_name || 'AI Code Review'}
                    </Typography>
                    {stats.pending_reviews > 0 && (
                      <Chip
                        icon={<PendingIcon />}
                        label={`${stats.pending_reviews} pending reviews`}
                        color="warning"
                        size="small"
                        sx={{ mt: 1 }}
                      />
                    )}
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: { xs: 'flex-start', md: 'flex-end' }, flexWrap: 'wrap' }}>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Button
                      component={Link}
                      to="/submit-code"
                      variant="contained"
                      startIcon={<CodeIcon />}
                      sx={{
                        background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                        color: '#000',
                        fontWeight: 'bold',
                        '&:hover': {
                          background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                        },
                      }}
                    >
                      Submit Code
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Button
                      component={Link}
                      to="/history"
                      variant="outlined"
                      startIcon={<HistoryIcon />}
                      sx={{
                        borderColor: '#64ffda',
                        color: '#64ffda',
                        '&:hover': {
                          borderColor: '#00b4d8',
                          color: '#00b4d8',
                          backgroundColor: 'rgba(100,255,218,0.1)',
                        },
                      }}
                    >
                      History
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Tooltip title="Refresh Dashboard">
                      <IconButton
                        onClick={handleRefresh}
                        disabled={refreshing}
                        sx={{ color: '#64ffda' }}
                      >
                        <RefreshIcon className={refreshing ? 'spin' : ''} />
                      </IconButton>
                    </Tooltip>
                  </motion.div>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </motion.div>

        {/* Stats Cards */}
        <Grid container spacing={3}>
          {statCards.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                whileHover={{ y: -10, scale: 1.02 }}
              >
                <Card 
                  sx={{
                    background: 'rgba(255,255,255,0.05)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: 3,
                    border: '1px solid rgba(255,255,255,0.05)',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                    '&:hover': {
                      boxShadow: `0 10px 40px rgba(100,255,218,0.15)`,
                      border: '1px solid rgba(100,255,218,0.2)',
                    },
                  }}
                  onClick={stat.action}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <Box>
                        <Typography color="rgba(255,255,255,0.6)" gutterBottom>
                          {stat.title}
                        </Typography>
                        <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
                          {stat.value}
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)' }}>
                          {stat.description}
                        </Typography>
                      </Box>
                      <Box sx={{
                        background: stat.gradient,
                        borderRadius: '50%',
                        p: 1.5,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}>
                        {stat.icon}
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        {/* Bugs Dialog */}
        <Dialog
          open={openBugsDialog}
          onClose={() => setOpenBugsDialog(false)}
          maxWidth="md"
          fullWidth
          PaperProps={{
            sx: {
              background: 'rgba(20,20,40,0.95)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 3,
            }
          }}
        >
          <DialogTitle sx={{ color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <BugReportIcon sx={{ color: '#ff6b6b' }} />
              <Typography variant="h6">All Bugs Found</Typography>
              <Chip label={`${getAllBugs().length} bugs`} color="error" size="small" />
            </Box>
          </DialogTitle>
          <DialogContent sx={{ mt: 2 }}>
            {getAllBugs().length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <BugReportIcon sx={{ fontSize: 60, color: 'rgba(255,255,255,0.1)' }} />
                <Typography sx={{ color: 'rgba(255,255,255,0.5)', mt: 2 }}>
                  No bugs found in your submissions! 🎉
                </Typography>
              </Box>
            ) : (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Bug</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Severity</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Submission</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Suggestion</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {getAllBugs().map((bug, index) => (
                      <TableRow key={index}>
                        <TableCell sx={{ color: '#fff' }}>{bug.description}</TableCell>
                        <TableCell>
                          <Chip
                            label={bug.severity || 'low'}
                            color={bug.severity === 'critical' ? 'error' : bug.severity === 'high' ? 'warning' : 'info'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>
                          {bug.submission_title || 'N/A'}
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.5)' }}>
                          {bug.suggestion || 'No suggestion'}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </DialogContent>
          <DialogActions sx={{ borderTop: '1px solid rgba(255,255,255,0.1)', p: 2 }}>
            <Button onClick={() => setOpenBugsDialog(false)} sx={{ color: '#64ffda' }}>
              Close
            </Button>
          </DialogActions>
        </Dialog>

        {/* Completed Reviews Dialog */}
        <Dialog
          open={openCompletedDialog}
          onClose={() => setOpenCompletedDialog(false)}
          maxWidth="md"
          fullWidth
          PaperProps={{
            sx: {
              background: 'rgba(20,20,40,0.95)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 3,
            }
          }}
        >
          <DialogTitle sx={{ color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CheckCircleIcon sx={{ color: '#ffd93d' }} />
              <Typography variant="h6">Completed Reviews</Typography>
              <Chip label={`${getCompletedSubmissions().length} reviews`} color="success" size="small" />
            </Box>
          </DialogTitle>
          <DialogContent sx={{ mt: 2 }}>
            {getCompletedSubmissions().length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CheckCircleIcon sx={{ fontSize: 60, color: 'rgba(255,255,255,0.1)' }} />
                <Typography sx={{ color: 'rgba(255,255,255,0.5)', mt: 2 }}>
                  No completed reviews yet. Submit code and get AI review!
                </Typography>
                <Button
                  component={Link}
                  to="/submit-code"
                  variant="contained"
                  sx={{ mt: 2 }}
                >
                  Submit Code for Review
                </Button>
              </Box>
            ) : (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Title</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Language</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Score</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Bugs</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Reviewed</TableCell>
                      <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>Action</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {getCompletedSubmissions().map((sub, index) => (
                      <TableRow key={sub.id || index}>
                        <TableCell sx={{ color: '#fff' }}>{sub.title || 'Untitled'}</TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>{sub.language_name || 'N/A'}</TableCell>
                        <TableCell>
                          <Chip
                            label={`${sub.quality_score || 0}%`}
                            color={sub.quality_score >= 70 ? 'success' : sub.quality_score >= 50 ? 'warning' : 'error'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.7)' }}>{sub.bug_count || 0}</TableCell>
                        <TableCell sx={{ color: 'rgba(255,255,255,0.5)' }}>
                          {sub.reviewed_at ? new Date(sub.reviewed_at).toLocaleDateString() : 'N/A'}
                        </TableCell>
                        <TableCell>
                          <IconButton
                            size="small"
                            onClick={() => handleViewSubmission(sub.id)}
                            sx={{ color: '#64ffda' }}
                          >
                            <DescriptionIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteSubmission(sub.id, sub.title)}
                            sx={{ color: '#ff6b6b' }}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </DialogContent>
          <DialogActions sx={{ borderTop: '1px solid rgba(255,255,255,0.1)', p: 2 }}>
            <Button onClick={() => setOpenCompletedDialog(false)} sx={{ color: '#64ffda' }}>
              Close
            </Button>
          </DialogActions>
        </Dialog>

        {/* Recent Submissions */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <Paper sx={{
            mt: 4,
            p: 3,
            background: 'rgba(255,255,255,0.03)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            border: '1px solid rgba(255,255,255,0.05)',
          }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ color: '#fff' }}>
                Recent Submissions
              </Typography>
              <Button
                component={Link}
                to="/history"
                size="small"
                sx={{ color: '#64ffda' }}
              >
                View All
              </Button>
            </Box>
            
            {recentSubmissions.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CodeIcon sx={{ fontSize: 60, color: 'rgba(255,255,255,0.1)' }} />
                <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.5)', mt: 2 }}>
                  No submissions yet
                </Typography>
                <Button
                  component={Link}
                  to="/submit-code"
                  variant="contained"
                  sx={{ mt: 2 }}
                >
                  Submit Your First Code
                </Button>
              </Box>
            ) : (
              <List>
                {recentSubmissions.map((submission, index) => (
                  <React.Fragment key={submission.id || index}>
                    <ListItem
                      secondaryAction={
                        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                          <Chip
                            label={submission.status || 'pending'}
                            color={getStatusColor(submission.status || 'pending')}
                            size="small"
                          />
                          <Tooltip title="View Details">
                            <IconButton
                              edge="end"
                              onClick={() => handleViewSubmission(submission.id)}
                              sx={{ color: '#64ffda' }}
                            >
                              <DescriptionIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Delete Submission">
                            <IconButton
                              edge="end"
                              onClick={() => handleDeleteSubmission(submission.id, submission.title)}
                              sx={{ color: '#ff6b6b' }}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      }
                      sx={{
                        borderRadius: 2,
                        cursor: 'pointer',
                        '&:hover': {
                          background: 'rgba(255,255,255,0.05)',
                        },
                      }}
                      onClick={() => handleViewSubmission(submission.id)}
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'rgba(100,255,218,0.1)', color: '#64ffda' }}>
                          <CodeIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Typography sx={{ color: '#fff' }}>
                            {submission.title || 'Untitled'}
                          </Typography>
                        }
                        secondary={
                          <Box component="span" sx={{ display: 'flex', gap: 2, mt: 0.5, flexWrap: 'wrap' }}>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                              {submission.language_name || 'N/A'}
                            </Typography>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                              {submission.quality_score ? `${submission.quality_score}%` : 'Pending'}
                            </Typography>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)' }}>
                              {submission.created_at ? new Date(submission.created_at).toLocaleDateString() : 'N/A'}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < recentSubmissions.length - 1 && <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)' }} />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.7 }}
        >
          <Paper sx={{
            mt: 4,
            p: 3,
            background: 'rgba(255,255,255,0.03)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            border: '1px solid rgba(255,255,255,0.05)',
          }}>
            <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                  <Button
                    component={Link}
                    to="/submit-code"
                    fullWidth
                    variant="outlined"
                    sx={{
                      borderColor: '#4ecdc4',
                      color: '#4ecdc4',
                      py: 2,
                      '&:hover': {
                        borderColor: '#44a08d',
                        color: '#44a08d',
                        backgroundColor: 'rgba(78,205,196,0.1)',
                      },
                    }}
                  >
                    <CodeIcon sx={{ mr: 1 }} />
                    New Submission
                  </Button>
                </motion.div>
              </Grid>
              <Grid item xs={12} sm={4}>
                <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                  <Button
                    component={Link}
                    to="/history"
                    fullWidth
                    variant="outlined"
                    sx={{
                      borderColor: '#ffd93d',
                      color: '#ffd93d',
                      py: 2,
                      '&:hover': {
                        borderColor: '#f6b93b',
                        color: '#f6b93b',
                        backgroundColor: 'rgba(255,217,61,0.1)',
                      },
                    }}
                  >
                    <HistoryIcon sx={{ mr: 1 }} />
                    Review History
                  </Button>
                </motion.div>
              </Grid>
              <Grid item xs={12} sm={4}>
                <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                  <Button
                    fullWidth
                    variant="outlined"
                    sx={{
                      borderColor: '#6c5ce7',
                      color: '#6c5ce7',
                      py: 2,
                      '&:hover': {
                        borderColor: '#4834d4',
                        color: '#4834d4',
                        backgroundColor: 'rgba(108,92,231,0.1)',
                      },
                    }}
                    onClick={() => {
                      toast.info('Generating report...');
                    }}
                  >
                    <TrendingUpIcon sx={{ mr: 1 }} />
                    Generate Report
                  </Button>
                </motion.div>
              </Grid>
            </Grid>
          </Paper>
        </motion.div>
      </Container>

      <style>
        {`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          .spin {
            animation: spin 1s linear infinite;
          }
        `}
      </style>
    </Box>
  );
};

export default StudentDashboard3D;
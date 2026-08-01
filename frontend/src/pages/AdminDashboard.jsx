import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { codeReviewAPI, dashboardAPI } from '../api';
import PeopleIcon from '@mui/icons-material/People';
import CodeIcon from '@mui/icons-material/Code';
import BugReportIcon from '@mui/icons-material/BugReport';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total_users: 0,
    total_students: 0,
    total_reviews: 0,
    total_bugs: 0,
    average_quality_score: 0,
    pending_reviews: 0,
  });
  const [recentSubmissions, setRecentSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const statsResponse = await codeReviewAPI.getStats();
      setStats(statsResponse.data.data);

      const submissionsResponse = await codeReviewAPI.getSubmissions();
      setRecentSubmissions(submissionsResponse.data.slice(0, 5));
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Total Users',
      value: stats.total_users || 0,
      icon: <PeopleIcon fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Total Submissions',
      value: stats.total_reviews || 0,
      icon: <CodeIcon fontSize="large" />,
      color: '#2e7d32',
    },
    {
      title: 'Total Bugs Found',
      value: stats.total_bugs || 0,
      icon: <BugReportIcon fontSize="large" />,
      color: '#d32f2f',
    },
    {
      title: 'Avg Quality Score',
      value: `${stats.average_quality_score || 0}%`,
      icon: <TrendingUpIcon fontSize="large" />,
      color: '#ed6c02',
    },
  ];

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

  if (loading) {
    return (
      <Container>
        <LinearProgress sx={{ mt: 4 }} />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" gutterBottom>
        Welcome back, {user?.first_name || user?.username}!
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      {stat.title}
                    </Typography>
                    <Typography variant="h4">
                      {stat.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: stat.color }}>
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Submissions
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>User</TableCell>
                    <TableCell>Language</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Quality Score</TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recentSubmissions.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        No submissions yet
                      </TableCell>
                    </TableRow>
                  ) : (
                    recentSubmissions.map((submission) => (
                      <TableRow key={submission.id}>
                        <TableCell>{submission.title}</TableCell>
                        <TableCell>{submission.username}</TableCell>
                        <TableCell>{submission.language_name}</TableCell>
                        <TableCell>
                          <Chip
                            label={submission.status}
                            color={getStatusColor(submission.status)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{submission.quality_score || 'N/A'}</TableCell>
                        <TableCell>
                          {new Date(submission.created_at).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          <Button
                            component={Link}
                            to={`/submission/${submission.id}`}
                            size="small"
                            variant="outlined"
                          >
                            View
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AdminDashboard;
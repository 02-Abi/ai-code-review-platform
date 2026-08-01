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
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { codeReviewAPI } from '../api';
import { Link } from 'react-router-dom';
import CodeIcon from '@mui/icons-material/Code';
import HistoryIcon from '@mui/icons-material/History';
import BugReportIcon from '@mui/icons-material/BugReport';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

const StudentDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total_submissions: 0,
    completed_reviews: 0,
    total_bugs_found: 0,
    average_quality_score: 0,
    pending_reviews: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await codeReviewAPI.getStats();
      setStats(response.data.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Total Submissions',
      value: stats.total_submissions,
      icon: <CodeIcon fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Completed Reviews',
      value: stats.completed_reviews,
      icon: <TrendingUpIcon fontSize="large" />,
      color: '#2e7d32',
    },
    {
      title: 'Bugs Found',
      value: stats.total_bugs_found,
      icon: <BugReportIcon fontSize="large" />,
      color: '#d32f2f',
    },
    {
      title: 'Quality Score',
      value: `${stats.average_quality_score}%`,
      icon: <TrendingUpIcon fontSize="large" />,
      color: '#ed6c02',
    },
  ];

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
        Welcome back, {user?.first_name || user?.username}!
      </Typography>
      <Typography variant="body1" color="textSecondary" gutterBottom>
        Track your code review progress and improve your coding skills.
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

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                component={Link}
                to="/submit-code"
                variant="contained"
                startIcon={<CodeIcon />}
              >
                Submit Code
              </Button>
              <Button
                component={Link}
                to="/history"
                variant="outlined"
                startIcon={<HistoryIcon />}
              >
                View History
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Typography color="textSecondary">
              {stats.pending_reviews > 0
                ? `You have ${stats.pending_reviews} pending review(s)`
                : 'No pending reviews'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default StudentDashboard;
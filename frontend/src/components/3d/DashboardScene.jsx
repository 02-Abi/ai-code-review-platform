import React from 'react';
import { motion } from 'framer-motion';
import { Box, Grid, Paper, Typography } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import BugReportIcon from '@mui/icons-material/BugReport';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const DashboardScene = ({ stats }) => {
  const items = [
    { icon: <CodeIcon sx={{ fontSize: 40, color: '#4ecdc4' }} />, label: 'Reviews', value: stats.total_submissions || 0, color: '#4ecdc4' },
    { icon: <BugReportIcon sx={{ fontSize: 40, color: '#ff6b6b' }} />, label: 'Bugs Found', value: stats.total_bugs_found || 0, color: '#ff6b6b' },
    { icon: <TrendingUpIcon sx={{ fontSize: 40, color: '#ffd93d' }} />, label: 'Score', value: `${stats.average_quality_score || 0}%`, color: '#ffd93d' },
    { icon: <CheckCircleIcon sx={{ fontSize: 40, color: '#6c5ce7' }} />, label: 'Completed', value: stats.completed_reviews || 0, color: '#6c5ce7' },
  ];

  return (
    <Box sx={{ p: 3, position: 'relative' }}>
      <Grid container spacing={3}>
        {items.map((item, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
            >
              <Paper sx={{
                p: 3,
                textAlign: 'center',
                background: 'rgba(255,255,255,0.05)',
                backdropFilter: 'blur(10px)',
                borderRadius: 3,
                border: `1px solid ${item.color}33`,
                transition: 'all 0.3s ease',
              }}>
                <Box sx={{ color: item.color, mb: 1 }}>{item.icon}</Box>
                <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
                  {item.value}
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)' }}>
                  {item.label}
                </Typography>
              </Paper>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default DashboardScene;
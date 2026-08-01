import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const LoadingSpinner = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
      }}
    >
      <CircularProgress sx={{ color: '#64ffda', mb: 2 }} size={60} />
      <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.7)' }}>
        Loading...
      </Typography>
    </Box>
  );
};

export default LoadingSpinner;
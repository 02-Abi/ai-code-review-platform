import React from 'react';
import { motion } from 'framer-motion';
import { Button, Box, Typography, Container, Grid } from '@mui/material';
import { Link } from 'react-router-dom';
import ParticleBackground from './3d/ParticleBackground';
import TypingEffect from './TypingEffect';
import CodeIcon from '@mui/icons-material/Code';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import BugReportIcon from '@mui/icons-material/BugReport';

const AnimatedHero = () => {
  const features = [
    { icon: <CodeIcon sx={{ fontSize: 50, color: '#64ffda' }} />, title: 'AI Code Review', desc: 'Get instant AI-powered code analysis' },
    { icon: <BugReportIcon sx={{ fontSize: 50, color: '#ff6b6b' }} />, title: 'Bug Detection', desc: 'Automatically detect and fix bugs' },
    { icon: <SecurityIcon sx={{ fontSize: 50, color: '#4ecdc4' }} />, title: 'Security Analysis', desc: 'Identify security vulnerabilities' },
    { icon: <SpeedIcon sx={{ fontSize: 50, color: '#ffd93d' }} />, title: 'Quality Score', desc: 'Get detailed quality metrics' },
  ];

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)', 
      position: 'relative', 
      overflow: 'hidden' 
    }}>
      <ParticleBackground />
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ x: -100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 1, type: 'spring' }}
            >
              <Typography 
                variant="h1" 
                sx={{ 
                  fontSize: { xs: '2.5rem', md: '4rem' }, 
                  fontWeight: 'bold', 
                  background: 'linear-gradient(45deg, #64ffda, #00b4d8)', 
                  backgroundClip: 'text', 
                  WebkitBackgroundClip: 'text', 
                  WebkitTextFillColor: 'transparent', 
                  mb: 2 
                }}
              >
                AI Code Review
              </Typography>
              
              <Typography 
                variant="h5" 
                sx={{ 
                  color: '#fff', 
                  mb: 2, 
                  fontWeight: '300',
                  minHeight: '60px'
                }}
              >
                <TypingEffect 
                  strings={[
                    'Review your code instantly',
                    'Detect bugs with AI',
                    'Get quality scores',
                    'Improve your coding'
                  ]} 
                  typeSpeed={50} 
                  backSpeed={30} 
                  loop={true} 
                />
              </Typography>
              
              <Typography 
                variant="body1" 
                sx={{ 
                  color: 'rgba(255,255,255,0.7)', 
                  mb: 4, 
                  fontSize: '1.2rem' 
                }}
              >
                Upload your code and get instant AI-powered feedback, bug detection, 
                quality scores, and test case generation.
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button 
                    component={Link} 
                    to="/register" 
                    variant="contained" 
                    size="large" 
                    sx={{ 
                      background: 'linear-gradient(45deg, #64ffda, #00b4d8)', 
                      color: '#000', 
                      fontWeight: 'bold', 
                      px: 4, 
                      py: 1.5,
                      '&:hover': { 
                        background: 'linear-gradient(45deg, #00b4d8, #64ffda)' 
                      } 
                    }}
                  >
                    Get Started
                  </Button>
                </motion.div>
                
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button 
                    component={Link} 
                    to="/login" 
                    variant="outlined" 
                    size="large" 
                    sx={{ 
                      borderColor: '#64ffda', 
                      color: '#64ffda', 
                      px: 4, 
                      py: 1.5,
                      '&:hover': { 
                        borderColor: '#00b4d8', 
                        color: '#00b4d8', 
                        backgroundColor: 'rgba(100,255,218,0.1)' 
                      } 
                    }}
                  >
                    Sign In
                  </Button>
                </motion.div>
              </Box>
            </motion.div>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 1, delay: 0.3 }}
            >
              <Box sx={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr 1fr', 
                gap: 3, 
                p: 3, 
                background: 'rgba(255,255,255,0.05)', 
                backdropFilter: 'blur(20px)', 
                borderRadius: 4, 
                border: '1px solid rgba(255,255,255,0.1)' 
              }}>
                {features.map((feature, index) => (
                  <motion.div 
                    key={index} 
                    initial={{ y: 50, opacity: 0 }} 
                    animate={{ y: 0, opacity: 1 }} 
                    transition={{ delay: 0.5 + index * 0.1 }} 
                    whileHover={{ scale: 1.05, y: -5 }} 
                    style={{ 
                      background: 'rgba(255,255,255,0.03)', 
                      borderRadius: '12px', 
                      padding: '20px', 
                      textAlign: 'center', 
                      border: '1px solid rgba(255,255,255,0.05)' 
                    }}
                  >
                    <Box sx={{ mb: 1 }}>{feature.icon}</Box>
                    <Typography variant="h6" sx={{ color: '#fff', fontSize: '1rem' }}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.8rem' }}>
                      {feature.desc}
                    </Typography>
                  </motion.div>
                ))}
              </Box>
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default AnimatedHero;
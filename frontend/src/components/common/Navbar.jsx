import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Menu,
  MenuItem,
  IconButton,
} from '@mui/material';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import CodeIcon from '@mui/icons-material/Code';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleClose();
  };

  const handleProfile = () => {
    navigate('/profile');
    handleClose();
  };

  return (
    <AppBar position="static" sx={{ background: 'rgba(10,10,10,0.8)', backdropFilter: 'blur(10px)' }}>
      <Toolbar>
        <CodeIcon sx={{ mr: 2, color: '#64ffda' }} />
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 1, 
            cursor: 'pointer',
            background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 'bold',
          }}
          onClick={() => navigate('/')}
        >
          AI Code Review
        </Typography>
        
        {user ? (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ mr: 2, color: 'rgba(255,255,255,0.7)' }}>
              {user.first_name || user.username}
            </Typography>
            <IconButton onClick={handleMenu} color="inherit">
              <Avatar sx={{ bgcolor: 'linear-gradient(45deg, #64ffda, #00b4d8)' }}>
                {user.first_name ? user.first_name[0] : user.username[0]}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
              PaperProps={{
                sx: {
                  background: 'rgba(20,20,40,0.95)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.1)',
                }
              }}
            >
              <MenuItem onClick={() => navigate('/dashboard')}>
                <CodeIcon sx={{ mr: 1, fontSize: 20 }} />
                Dashboard
              </MenuItem>
              <MenuItem onClick={() => navigate('/submit-code')}>
                <CodeIcon sx={{ mr: 1, fontSize: 20 }} />
                Submit Code
              </MenuItem>
              <MenuItem onClick={() => navigate('/history')}>
                <CodeIcon sx={{ mr: 1, fontSize: 20 }} />
                History
              </MenuItem>
              <MenuItem onClick={handleProfile}>
                <AccountCircleIcon sx={{ mr: 1, fontSize: 20 }} />
                Profile
              </MenuItem>
              <MenuItem onClick={handleLogout} sx={{ color: '#ff6b6b' }}>
                Logout
              </MenuItem>
            </Menu>
          </Box>
        ) : (
          <Box>
            <Button color="inherit" onClick={() => navigate('/login')}>
              Login
            </Button>
            <Button 
              color="inherit" 
              onClick={() => navigate('/register')}
              sx={{
                background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                color: '#000',
                '&:hover': {
                  background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                },
                ml: 1,
              }}
            >
              Register
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { jwtDecode } from 'jwt-decode';

const ProtectedRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, user, loading, loadUser } = useAuth();
  const location = useLocation();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    // Check if token exists and is valid
    const token = localStorage.getItem('accessToken');
    console.log('ProtectedRoute: Checking token...', token ? 'Exists' : 'Not found');
    
    if (token) {
      try {
        const decoded = jwtDecode(token);
        if (decoded.exp * 1000 > Date.now()) {
          console.log('ProtectedRoute: Token is valid');
          if (!isAuthenticated) {
            loadUser();
          }
        } else {
          console.log('ProtectedRoute: Token expired');
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
        }
      } catch (error) {
        console.error('ProtectedRoute: Invalid token', error);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
      }
    }
    setChecking(false);
  }, [isAuthenticated, loadUser]);

  console.log('ProtectedRoute Check:', { 
    isAuthenticated, 
    user, 
    loading, 
    checking,
    path: location.pathname,
    token: localStorage.getItem('accessToken') ? 'Exists' : 'Not found'
  });

  if (loading || checking) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        color: '#fff'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            width: '50px', 
            height: '50px', 
            border: '3px solid rgba(255,255,255,0.1)',
            borderTop: '3px solid #64ffda',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }} />
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  // Check if token exists in localStorage as backup
  const tokenExists = !!localStorage.getItem('accessToken');
  
  if (!isAuthenticated && !tokenExists) {
    console.log('❌ Not authenticated, redirecting to login');
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If token exists but user not loaded, try loading
  if (tokenExists && !isAuthenticated) {
    console.log('🔄 Token exists but user not loaded, attempting to load...');
    loadUser();
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        color: '#fff'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            width: '50px', 
            height: '50px', 
            border: '3px solid rgba(255,255,255,0.1)',
            borderTop: '3px solid #64ffda',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }} />
          <p>Loading user...</p>
        </div>
      </div>
    );
  }

  if (requiredRole && user?.user_type !== requiredRole) {
    console.log('❌ User role mismatch, redirecting to home');
    return <Navigate to="/" replace />;
  }

  console.log('✅ Authenticated, rendering protected content');
  return children;
};

export default ProtectedRoute;
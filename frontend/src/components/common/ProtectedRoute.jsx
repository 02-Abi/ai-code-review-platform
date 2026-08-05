// src/components/common/ProtectedRoute.jsx
import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { jwtDecode } from 'jwt-decode';
import { LinearProgress, Box } from '@mui/material';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, token, loading, user } = useAuth();
    const location = useLocation();
    const [isValid, setIsValid] = useState(true);
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        const validateToken = () => {
            if (token) {
                try {
                    const decoded = jwtDecode(token);
                    const currentTime = Date.now() / 1000;
                    if (decoded.exp < currentTime) {
                        console.log('❌ Token expired');
                        // Clear expired token
                        localStorage.removeItem('accessToken');
                        localStorage.removeItem('refreshToken');
                        setIsValid(false);
                    } else {
                        console.log('✅ Token valid');
                        setIsValid(true);
                    }
                } catch (error) {
                    console.error('❌ Token decode error:', error);
                    setIsValid(false);
                }
            } else {
                console.log('❌ No token');
                setIsValid(false);
            }
            setChecking(false);
        };

        validateToken();
    }, [token]);

    console.log('ProtectedRoute Check:', {
        isAuthenticated,
        hasToken: !!token,
        isValid,
        loading,
        checking,
        path: location.pathname
    });

    if (loading || checking) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <LinearProgress sx={{ width: '50%' }} />
            </Box>
        );
    }

    if (!isAuthenticated || !isValid) {
        console.log('❌ Not authenticated, redirecting to login');
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    console.log('✅ Authenticated, rendering protected content');
    return children;
};

export default ProtectedRoute;
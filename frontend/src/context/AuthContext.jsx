// src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('accessToken'));

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const storedToken = localStorage.getItem('accessToken');
    console.log('🔍 Checking auth...', storedToken ? 'Token exists' : 'No token');
    
    if (!storedToken) {
      setLoading(false);
      setIsAuthenticated(false);
      setToken(null);
      return;
    }

    try {
      const decoded = jwtDecode(storedToken);
      console.log('🔍 Decoded token:', decoded);
      
      if (decoded.exp * 1000 <= Date.now()) {
        console.log('❌ Token expired');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
        setLoading(false);
        return;
      }

      console.log('✅ Token is valid');
      setToken(storedToken);
      await loadUser(storedToken);
    } catch (error) {
      console.error('❌ Error checking auth:', error);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      setToken(null);
      setUser(null);
      setIsAuthenticated(false);
      setLoading(false);
    }
  };

  const loadUser = async (tokenValue) => {
    try {
      console.log('👤 Loading user profile...');
      const response = await authAPI.getProfile();
      console.log('👤 Profile loaded:', response.data);
      
      const userData = response.data.user;
      setUser(userData);
      setIsAuthenticated(true);
      setToken(tokenValue || localStorage.getItem('accessToken'));
      setLoading(false);
      
      console.log('✅ User loaded, isAuthenticated set to true');
    } catch (error) {
      console.error('❌ Failed to load user:', error);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      setUser(null);
      setIsAuthenticated(false);
      setToken(null);
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      console.log('🔐 Attempting login...');
      const response = await authAPI.login({ username, password });
      console.log('🔐 Login response:', response.data);
      
      const { access, refresh } = response.data.tokens;
      const userData = response.data.user;
      
      console.log('👤 User data:', userData);
      console.log('👤 User type:', userData.user_type);
      
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Update state
      setToken(access);
      setUser(userData);
      setIsAuthenticated(true);
      
      console.log('✅ State updated - isAuthenticated:', true);
      console.log('✅ Token set:', access ? 'yes' : 'no');
      
      return { success: true, user: userData };
    } catch (error) {
      console.error('❌ Login error:', error);
      console.error('❌ Error response:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      console.log('📝 Registering...');
      const response = await authAPI.register(userData);
      console.log('📝 Registration response:', response.data);
      
      const { access, refresh } = response.data.tokens;
      const user = response.data.user;
      
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setToken(access);
      setUser(user);
      setIsAuthenticated(true);
      
      return { success: true, user };
    } catch (error) {
      console.error('❌ Registration error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Registration failed' 
      };
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        await authAPI.logout(refreshToken);
      }
    } catch (error) {
      console.error('❌ Logout error:', error);
    } finally {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      setToken(null);
      setUser(null);
      setIsAuthenticated(false);
      console.log('✅ Logged out');
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    token,
    login,
    register,
    logout,
    loadUser,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
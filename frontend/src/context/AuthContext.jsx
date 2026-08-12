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
      // ✅ FIX: Get user from token or API
      const response = await authAPI.getProfile();
      console.log('👤 Profile loaded:', response.data);
      
      const userData = response.data.user || response.data;
      setUser(userData);
      setIsAuthenticated(true);
      setToken(tokenValue || localStorage.getItem('accessToken'));
      setLoading(false);
      
      console.log('✅ User loaded, isAuthenticated set to true');
    } catch (error) {
      console.error('❌ Failed to load user:', error);
      // If profile fails, try to get user from token
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          setIsAuthenticated(true);
          setLoading(false);
          return;
        } catch (e) {
          console.error('❌ Failed to parse stored user:', e);
        }
      }
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
      // ✅ FIX: Use correct JWT endpoint
      const response = await authAPI.login({ username, password });
      console.log('🔐 Login response:', response.data);
      
      // ✅ FIX: Handle JWT response format
      const access = response.data.access;
      const refresh = response.data.refresh;
      
      console.log('✅ Access token received:', access ? 'yes' : 'no');
      
      // Create user data from token or API
      const userData = { username };
      
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('user', JSON.stringify(userData));
      
      setToken(access);
      setUser(userData);
      setIsAuthenticated(true);
      
      console.log('✅ State updated - isAuthenticated:', true);
      
      return { success: true, user: userData };
    } catch (error) {
      console.error('❌ Login error:', error);
      console.error('❌ Error response:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      console.log('📝 Registering...');
      // ✅ FIX: Use register endpoint
      const response = await authAPI.register(userData);
      console.log('📝 Registration response:', response.data);
      
      // Login after registration
      const loginResponse = await login(userData.username, userData.password);
      if (loginResponse.success) {
        return { success: true, user: loginResponse.user };
      }
      
      return { success: false, error: 'Registration failed' };
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
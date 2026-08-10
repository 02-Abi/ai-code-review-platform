// src/api/index.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://ai-code-review-platform-3xhi.onrender.com/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    console.log(`📤 ${config.method?.toUpperCase() || 'GET'} ${config.url}`);
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔑 Token added to request');
    } else {
      console.log('❌ No token found for request:', config.url);
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    console.log(`📥 ${response.config.method?.toUpperCase() || 'GET'} ${response.config.url} - Status: ${response.status}`);
    return response;
  },
  async (error) => {
    console.error('API Error:', error.response?.data || error.message);
    
    // If 401 Unauthorized, try to refresh token
    if (error.response?.status === 401) {
      console.warn('⚠️ 401 Unauthorized - Attempting token refresh...');
      const originalRequest = error.config;
      
      if (!originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          const refreshToken = localStorage.getItem('refreshToken');
          console.log('🔄 Refresh Token:', refreshToken ? 'Exists' : 'Not found');
          
          if (refreshToken) {
            // ✅ FIX: Use correct refresh endpoint
            const response = await axios.post(`${API_URL}/token/refresh/`, {
              refresh: refreshToken,
            });
            
            const { access } = response.data;
            console.log('✅ Token refreshed successfully');
            
            localStorage.setItem('accessToken', access);
            
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return api(originalRequest);
          } else {
            console.warn('❌ No refresh token available');
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
          }
        } catch (refreshError) {
          console.error('❌ Token refresh failed:', refreshError);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// ============================================================
// AUTH API - EXPORTED ✅ FIXED
// ============================================================
export const authAPI = {
  // ✅ FIX: Use JWT endpoints
  login: (data) => api.post('/token/', data),  // Changed from /accounts/login/
  register: (data) => api.post('/accounts/register/', data),
  logout: (refreshToken) => api.post('/token/blacklist/', { refresh: refreshToken }),
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (data) => api.put('/accounts/profile/update/', data),
  changePassword: (data) => api.post('/accounts/password/change/', data),
  requestPasswordReset: (email) => api.post('/accounts/password/reset/request/', { email }),
  verifyOTP: (data) => api.post('/accounts/password/reset/verify/', data),
  confirmPasswordReset: (data) => api.post('/accounts/password/reset/confirm/', data),
  getStats: () => api.get('/accounts/statistics/'),
};

// ============================================================
// CODE REVIEW API - EXPORTED
// ============================================================
export const codeReviewAPI = {
  getLanguages: () => api.get('/code-review/languages/'),
  getLanguagesSupport: () => api.get('/code-review/languages-support/'),
  getSubmissions: () => {
    console.log('📋 API: Getting submissions...');
    return api.get('/code-review/submissions/');
  },
  getSubmission: (id) => api.get(`/code-review/submissions/${id}/`),
  createSubmission: (data) => api.post('/code-review/submissions/', data),
  updateSubmission: (id, data) => api.put(`/code-review/submissions/${id}/`, data),
  deleteSubmission: (id) => api.delete(`/code-review/submissions/${id}/`),
  updateStatus: (id, status) => api.patch(`/code-review/submissions/${id}/status/`, { status }),
  getReviewHistory: () => api.get('/code-review/reviews/'),
  getReviewDetail: (id) => api.get(`/code-review/reviews/${id}/`),
  getComments: (reviewId) => api.get(`/code-review/reviews/${reviewId}/comments/`),
  addComment: (reviewId, data) => api.post(`/code-review/reviews/${reviewId}/comments/`, data),
  getSnippets: () => api.get('/code-review/snippets/'),
  createSnippet: (data) => api.post('/code-review/snippets/', data),
  getStats: () => {
    console.log('📊 API: Getting stats...');
    return api.get('/code-review/stats/');
  },
  initiateReview: (submissionId) => {
    console.log('🤖 API: Initiating review for submission:', submissionId);
    if (!submissionId) {
      console.error('No submission ID provided!');
      return Promise.reject(new Error('No submission ID provided'));
    }
    return api.post('/code-review/initiate/', { 
      submission_id: submissionId 
    });
  },
  detectLanguage: (code) => {
    console.log('🔍 API: Detecting language...');
    return api.post('/code-review/detect-language/', { code });
  },
  getLLMStatus: () => api.get('/code-review/llm-status/'),
};

// ============================================================
// DASHBOARD API - EXPORTED
// ============================================================
export const dashboardAPI = {
  getAdminStats: () => api.get('/dashboard/admin/'),
  getStudentStats: () => api.get('/dashboard/student/'),
};

// ============================================================
// DEFAULT EXPORT
// ============================================================
export default api;
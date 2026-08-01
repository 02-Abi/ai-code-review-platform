export const getAuthHeaders = () => {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    console.warn('No token found');
    return {};
  }
  return {
    'Authorization': `Bearer ${token}`
  };
};

export const isAuthenticated = () => {
  const token = localStorage.getItem('accessToken');
  if (!token) return false;
  
  try {
    const decoded = JSON.parse(atob(token.split('.')[1]));
    return decoded.exp * 1000 > Date.now();
  } catch {
    return false;
  }
};
import axios from 'axios';
import router from '@/router';

// Function to obtain the authentication token
export const getAuthToken = () => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    console.error('No se encontró el token de autenticación.');
    // Consider redirecting to login or displaying an error message here
    return null; // Or throw an error if redirection/error handling is done elsewhere
  }
  return token;
};

// Create an axios instance with the base URL from .env
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

// Interceptor for requests: Add authentication token
api.interceptors.request.use(
  config => {
    const token = getAuthToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Interceptor for responses: Handle errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Clear local storage and redirect to login
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refreshToken'); // If applicable
      localStorage.removeItem('is_superuser');
      localStorage.removeItem('is_staff');
      router.push('/login');
    } else if (error.response && error.response.status === 500) {
      // Handle server errors (consider showing a user-friendly message)
      console.error('Server error:', error.response.data);
      // ... (optionally show a notification to the user)
    }
    return Promise.reject(error);
  }
);

// Export api for reuse in other parts
export { api };
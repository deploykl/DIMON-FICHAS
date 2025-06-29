import axios from 'axios';
import router from '@/router';
import store from '@/store'; // Asegúrate de importar tu store de Vuex

// Function to obtain the authentication token
export const getAuthToken = () => {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    console.error('No se encontró el token de autenticación.');
    return null;
  }
  return token;
};

// Check network status
export const isOnline = () => navigator.onLine;

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

// Interceptor for responses: Handle errors and offline mode
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('is_superuser');
      localStorage.removeItem('is_staff');
      router.push('/login');
      return Promise.reject(error);
    }
    
    // Handle server errors
    if (error.response && error.response.status === 500) {
      console.error('Server error:', error.response.data);
      return Promise.reject(error);
    }
    
    // Handle offline mode
    if (!isOnline() && originalRequest) {
      console.log('App is offline. Queueing request...');
      
      // Store the request in offline queue
      await store.dispatch('offline/addToQueue', {
        method: originalRequest.method,
        url: originalRequest.url,
        data: originalRequest.data,
        headers: originalRequest.headers
      });
      
      // Return a mock response indicating offline operation
      return Promise.resolve({ 
        data: { 
          offline: true, 
          message: 'Operation queued for sync when online',
          timestamp: new Date().toISOString(),
          id: Date.now()
        } 
      });
    }
    
    return Promise.reject(error);
  }
);

// Function to sync queued requests when back online
export const syncOfflineRequests = async () => {
  if (!isOnline()) return;
  
  const requests = store.getters['offline/queue'];
  if (!requests || requests.length === 0) return;
  
  console.log('Syncing offline requests...');
  
  for (const request of requests) {
    try {
      const response = await api({
        method: request.method,
        url: request.url,
        data: request.data,
        headers: request.headers
      });
      
      console.log('Successfully synced:', request.url);
      await store.dispatch('offline/removeFromQueue', request.id);
    } catch (error) {
      console.error('Failed to sync request:', request.url, error);
      // Optionally retry later or mark as failed
    }
  }
};

// Listen for online/offline events
window.addEventListener('online', syncOfflineRequests);
window.addEventListener('offline', () => {
  store.dispatch('offline/setOfflineMode', true);
});

export { api };
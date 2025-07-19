import axios from 'axios';

// API Base URL - wird automatisch auf den Backend-Server zeigen
const API_BASE_URL = '/api';

// Axios-Instanz erstellen
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request-Interceptor für JWT-Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response-Interceptor für Token-Erneuerung
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          });

          const { access_token } = response.data;
          localStorage.setItem('access_token', access_token);

          // Ursprüngliche Anfrage mit neuem Token wiederholen
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh fehlgeschlagen, Benutzer abmelden
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
  refresh: () => api.post('/auth/refresh'),
};

// Server API
export const serverAPI = {
  getServers: () => api.get('/servers'),
  getServer: (id) => api.get(`/servers/${id}`),
  createServer: (serverData) => api.post('/servers', serverData),
  updateServer: (id, serverData) => api.put(`/servers/${id}`, serverData),
  deleteServer: (id) => api.delete(`/servers/${id}`),
  startServer: (id) => api.post(`/servers/${id}/start`),
  stopServer: (id) => api.post(`/servers/${id}/stop`),
  restartServer: (id) => api.post(`/servers/${id}/restart`),
  getServerLogs: (id, params = {}) => api.get(`/servers/${id}/logs`, { params }),
};

// User API
export const userAPI = {
  getUsers: () => api.get('/users'),
  getUser: (id) => api.get(`/users/${id}`),
  createUser: (userData) => api.post('/users', userData),
  updateUser: (id, userData) => api.put(`/users/${id}`, userData),
  deleteUser: (id) => api.delete(`/users/${id}`),
};

export default api;


import axios from 'axios'

// Determine API base URL
// If VITE_API_BASE_URL is set and doesn't contain 'backend:' (Docker service name),
// use it directly. Otherwise, use relative path which will go through Vite proxy.
// 'backend:' only works inside Docker network, not from browser on host machine.
const viteApiBaseUrl = import.meta.env.VITE_API_BASE_URL
const isDockerEnv = import.meta.env.DOCKER_ENV === 'true'
const containsBackend = viteApiBaseUrl?.includes('backend:')

// Use VITE_API_BASE_URL only if:
// 1. It's set AND
// 2. Either we're in Docker OR it doesn't contain 'backend:' (i.e., it's localhost)
const API_BASE_URL = (viteApiBaseUrl && (isDockerEnv || !containsBackend))
  ? `${viteApiBaseUrl}/api/v1`
  : '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api


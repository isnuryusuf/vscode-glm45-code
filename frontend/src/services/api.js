import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/health')
    return response.data
  },

  // Items API
  async getItems() {
    const response = await api.get('/api/items/')
    return response.data
  },

  async getItem(id) {
    const response = await api.get(`/api/items/${id}`)
    return response.data
  },

  async createItem(item) {
    const response = await api.post('/api/items/', item)
    return response.data
  },

  async updateItem(id, item) {
    const response = await api.put(`/api/items/${id}`, item)
    return response.data
  },

  async deleteItem(id) {
    const response = await api.delete(`/api/items/${id}`)
    return response.data
  },

  // Users API
  async getUsers() {
    const response = await api.get('/api/users/')
    return response.data
  },

  async getUser(id) {
    const response = await api.get(`/api/users/${id}`)
    return response.data
  },

  async createUser(user) {
    const response = await api.post('/api/users/', user)
    return response.data
  }
}
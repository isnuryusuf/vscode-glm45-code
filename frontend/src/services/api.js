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
    console.log('Base URL:', api.defaults.baseURL)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    console.error('Error Status:', error.response?.status)
    console.error('Error Config:', error.config)
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
  },

  // Reports API
  async getUsersReport() {
    const response = await api.get('/api/reports/users', {
      responseType: 'blob'
    })
    return response.data
  },

  async getItemsReport() {
    const response = await api.get('/api/reports/items', {
      responseType: 'blob'
    })
    return response.data
  },

  async getComprehensiveReport() {
    const response = await api.get('/api/reports/comprehensive', {
      responseType: 'blob'
    })
    return response.data
  },

  async getReportsHealth() {
    const response = await api.get('/api/reports/health')
    return response.data
  },

  // Contact API
  async getContacts() {
    const response = await api.get('/api/contact/')
    return response.data
  },

  async getContact(id) {
    const response = await api.get(`/api/contact/${id}`)
    return response.data
  },

  async createContact(contact) {
    const response = await api.post('/api/contact/', contact)
    return response.data
  },

  async updateContact(id, contact) {
    const response = await api.put(`/api/contact/${id}`, contact)
    return response.data
  },

  async deleteContact(id) {
    const response = await api.delete(`/api/contact/${id}`)
    return response.data
  }
}
<template>
  <div class="home">
    <h1>Welcome to FastAPI Vue Boilerplate</h1>
    <div class="status-container">
      <div class="status-card">
        <h3>Backend Status</h3>
        <p v-if="loading">Checking backend connection...</p>
        <p v-else-if="error" class="error">{{ error }}</p>
        <p v-else class="success">Backend is connected and healthy!</p>
      </div>
    </div>
    <div class="features">
      <h2>Features</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>FastAPI Backend</h3>
          <p>Modern, fast web framework for building APIs with Python</p>
        </div>
        <div class="feature-card">
          <h3>Vue.js Frontend</h3>
          <p>Progressive JavaScript framework for building user interfaces</p>
        </div>
        <div class="feature-card">
          <h3>SQLite Database</h3>
          <p>Lightweight, serverless SQL database engine</p>
        </div>
        <div class="feature-card">
          <h3>RESTful API</h3>
          <p>Complete CRUD operations for items and users</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Home',
  data() {
    return {
      loading: true,
      error: null
    }
  },
  async mounted() {
    try {
      await api.healthCheck()
    } catch (err) {
      this.error = 'Failed to connect to backend'
      console.error('Backend connection failed:', err)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
}

.status-container {
  margin: 2rem 0;
}

.status-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  max-width: 400px;
  margin: 0 auto;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.success {
  color: #28a745;
  font-weight: bold;
}

.error {
  color: #dc3545;
  font-weight: bold;
}

.features {
  margin-top: 3rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.feature-card h3 {
  color: #42b983;
  margin-bottom: 0.5rem;
}
</style>
<template>
  <div class="users">
    <h1>Users Management</h1>
    
    <div class="user-form">
      <h2>Add New User</h2>
      <form @submit.prevent="saveUser">
        <div class="form-group">
          <label for="username">Username:</label>
          <input 
            id="username" 
            v-model="newUser.username" 
            type="text" 
            required 
            placeholder="Enter username"
          >
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input 
            id="email" 
            v-model="newUser.email" 
            type="email" 
            required 
            placeholder="Enter email address"
          >
        </div>
        <div class="form-actions">
          <button type="submit">Add User</button>
        </div>
      </form>
    </div>

    <div class="users-list">
      <h2>Users List</h2>
      <div v-if="loading" class="loading">Loading users...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="users.length === 0" class="empty">No users found. Add your first user!</div>
      <div v-else class="user-grid">
        <div v-for="user in users" :key="user.id" class="user-card" :class="{ inactive: !user.is_active }">
          <h3>{{ user.username }}</h3>
          <p class="email">{{ user.email }}</p>
          <div class="user-meta">
            <span class="status" :class="{ active: user.is_active, inactive: !user.is_active }">
              {{ user.is_active ? 'Active' : 'Inactive' }}
            </span>
            <span class="date">Joined: {{ formatDate(user.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: true,
      error: null,
      newUser: {
        username: '',
        email: ''
      }
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      try {
        this.loading = true
        this.users = await api.getUsers()
      } catch (err) {
        this.error = 'Failed to load users'
        console.error('Error loading users:', err)
      } finally {
        this.loading = false
      }
    },
    
    async saveUser() {
      try {
        await api.createUser(this.newUser)
        this.resetForm()
        await this.loadUsers()
      } catch (err) {
        console.error('Error saving user:', err)
        alert('Failed to save user. Please check if the username or email already exists.')
      }
    },
    
    resetForm() {
      this.newUser = {
        username: '',
        email: ''
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.users {
  max-width: 1000px;
  margin: 0 auto;
}

.user-form {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 1rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  background: #42b983;
  color: white;
  transition: background-color 0.2s;
}

button:hover {
  background: #3aa876;
}

.users-list {
  margin-top: 2rem;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.empty {
  color: #6c757d;
}

.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.user-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.user-card.inactive {
  opacity: 0.7;
  background: #f8f9fa;
}

.user-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.user-card .email {
  margin: 0 0 1rem 0;
  color: #6c757d;
  font-style: italic;
}

.user-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.status {
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.status.active {
  color: #28a745;
  background: #d4edda;
}

.status.inactive {
  color: #6c757d;
  background: #e2e3e5;
}
</style>
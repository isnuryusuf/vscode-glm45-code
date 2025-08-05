<template>
  <div class="items">
    <h1>Items Management</h1>
    
    <div class="item-form">
      <h2>{{ editingItem ? 'Edit Item' : 'Add New Item' }}</h2>
      <form @submit.prevent="saveItem">
        <div class="form-group">
          <label for="title">Title:</label>
          <input 
            id="title" 
            v-model="currentItem.title" 
            type="text" 
            required 
            placeholder="Enter item title"
          >
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea 
            id="description" 
            v-model="currentItem.description" 
            placeholder="Enter item description"
          ></textarea>
        </div>
        <div class="form-group">
          <label>
            <input v-model="currentItem.completed" type="checkbox">
            Completed
          </label>
        </div>
        <div class="form-actions">
          <button type="submit">{{ editingItem ? 'Update' : 'Add' }} Item</button>
          <button v-if="editingItem" type="button" @click="cancelEdit">Cancel</button>
        </div>
      </form>
    </div>

    <div class="items-list">
      <h2>Items List</h2>
      <div v-if="loading" class="loading">Loading items...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="items.length === 0" class="empty">No items found. Add your first item!</div>
      <div v-else class="item-grid">
        <div v-for="item in items" :key="item.id" class="item-card" :class="{ completed: item.completed }">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description || 'No description' }}</p>
          <div class="item-meta">
            <span class="status">{{ item.completed ? 'Completed' : 'Pending' }}</span>
            <span class="date">{{ formatDate(item.created_at) }}</span>
          </div>
          <div class="item-actions">
            <button @click="editItem(item)" class="btn-edit">Edit</button>
            <button @click="deleteItem(item.id)" class="btn-delete">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Items',
  data() {
    return {
      items: [],
      loading: true,
      error: null,
      editingItem: null,
      currentItem: {
        title: '',
        description: '',
        completed: false
      }
    }
  },
  async mounted() {
    await this.loadItems()
  },
  methods: {
    async loadItems() {
      try {
        this.loading = true
        this.items = await api.getItems()
      } catch (err) {
        this.error = 'Failed to load items'
        console.error('Error loading items:', err)
      } finally {
        this.loading = false
      }
    },
    
    async saveItem() {
      try {
        if (this.editingItem) {
          await api.updateItem(this.editingItem.id, this.currentItem)
        } else {
          await api.createItem(this.currentItem)
        }
        this.resetForm()
        await this.loadItems()
      } catch (err) {
        console.error('Error saving item:', err)
        alert('Failed to save item')
      }
    },
    
    editItem(item) {
      this.editingItem = item
      this.currentItem = {
        title: item.title,
        description: item.description,
        completed: item.completed
      }
    },
    
    cancelEdit() {
      this.resetForm()
    },
    
    resetForm() {
      this.editingItem = null
      this.currentItem = {
        title: '',
        description: '',
        completed: false
      }
    },
    
    async deleteItem(id) {
      if (confirm('Are you sure you want to delete this item?')) {
        try {
          await api.deleteItem(id)
          await this.loadItems()
        } catch (err) {
          console.error('Error deleting item:', err)
          alert('Failed to delete item')
        }
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.items {
  max-width: 1000px;
  margin: 0 auto;
}

.item-form {
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

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
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

button[type="button"] {
  background: #6c757d;
}

button[type="button"]:hover {
  background: #5a6268;
}

.items-list {
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

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.item-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.item-card.completed {
  opacity: 0.7;
  background: #f8f9fa;
}

.item-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.item-card p {
  margin: 0 0 1rem 0;
  color: #6c757d;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.status {
  font-weight: bold;
  color: #28a745;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit {
  background: #ffc107;
  color: #212529;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
}

.btn-edit:hover {
  background: #e0a800;
}

.btn-delete {
  background: #dc3545;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
}

.btn-delete:hover {
  background: #c82333;
}
</style>
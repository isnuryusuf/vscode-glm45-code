<template>
  <div class="contact">
    <h1>Contact Us</h1>
    
    <div class="contact-form">
      <h2>Send us a message</h2>
      <form @submit.prevent="submitContact">
        <div class="form-group">
          <label for="name">Name:</label>
          <input 
            id="name" 
            v-model="contactForm.name" 
            type="text" 
            required 
            placeholder="Enter your full name"
          >
        </div>
        
        <div class="form-group">
          <label for="email">Email:</label>
          <input 
            id="email" 
            v-model="contactForm.email" 
            type="email" 
            required 
            placeholder="Enter your email address"
          >
        </div>
        
        <div class="form-group">
          <label for="subject">Subject:</label>
          <input 
            id="subject" 
            v-model="contactForm.subject" 
            type="text" 
            required 
            placeholder="Enter the subject"
          >
        </div>
        
        <div class="form-group">
          <label for="message">Message:</label>
          <textarea 
            id="message" 
            v-model="contactForm.message" 
            required 
            placeholder="Enter your message"
            rows="6"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="submitting">
            {{ submitting ? 'Sending...' : 'Send Message' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div class="contact-info">
      <h2>Other ways to reach us</h2>
      <div class="info-grid">
        <div class="info-card">
          <h3>Email</h3>
          <p>support@example.com</p>
        </div>
        <div class="info-card">
          <h3>Phone</h3>
          <p>+1 (555) 123-4567</p>
        </div>
        <div class="info-card">
          <h3>Address</h3>
          <p>123 Main Street<br>City, State 12345</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Contact',
  data() {
    return {
      contactForm: {
        name: '',
        email: '',
        subject: '',
        message: ''
      },
      submitting: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  methods: {
    async submitContact() {
      try {
        this.submitting = true
        this.errorMessage = ''
        this.successMessage = ''
        
        await api.createContact(this.contactForm)
        
        this.successMessage = 'Thank you for your message! We will get back to you soon.'
        this.resetForm()
      } catch (err) {
        console.error('Error submitting contact form:', err)
        this.errorMessage = 'Failed to send message. Please try again later.'
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.contactForm = {
        name: '',
        email: '',
        subject: '',
        message: ''
      }
    }
  }
}
</script>

<style scoped>
.contact {
  max-width: 800px;
  margin: 0 auto;
}

.contact-form {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  margin-top: 1.5rem;
}

button {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  background: #42b983;
  color: white;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background: #3aa876;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #c3e6cb;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #f5c6cb;
}

.contact-info {
  margin-top: 3rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.info-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.info-card h3 {
  margin: 0 0 1rem 0;
  color: #42b983;
}

.info-card p {
  margin: 0;
  color: #6c757d;
  line-height: 1.5;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}
</style>
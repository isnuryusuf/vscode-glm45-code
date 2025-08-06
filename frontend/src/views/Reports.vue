<template>
  <div class="reports">
    <h1>PDF Reports</h1>
    
    <div class="reports-container">
      <div class="report-section">
        <h2>Generate Reports</h2>
        <p>Download comprehensive PDF reports of your application data.</p>
        
        <div class="report-cards">
          <div class="report-card">
            <h3>Users Report</h3>
            <p>Download a complete report of all users in the system including their status and creation dates.</p>
            <div class="report-actions">
              <button @click="downloadUsersReport" :disabled="loading.users" class="btn-primary">
                <span v-if="loading.users">Generating...</span>
                <span v-else>Download Users Report</span>
              </button>
            </div>
          </div>
          
          <div class="report-card">
            <h3>Items Report</h3>
            <p>Download a detailed report of all items with completion status and ownership information.</p>
            <div class="report-actions">
              <button @click="downloadItemsReport" :disabled="loading.items" class="btn-primary">
                <span v-if="loading.items">Generating...</span>
                <span v-else>Download Items Report</span>
              </button>
            </div>
          </div>
          
          <div class="report-card">
            <h3>Comprehensive Report</h3>
            <p>Download a complete system report including both users and items with statistics and summaries.</p>
            <div class="report-actions">
              <button @click="downloadComprehensiveReport" :disabled="loading.comprehensive" class="btn-primary">
                <span v-if="loading.comprehensive">Generating...</span>
                <span v-else>Download Comprehensive Report</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="status-section">
        <h2>Reports Service Status</h2>
        <div class="status-card">
          <div v-if="statusLoading" class="loading">Checking service status...</div>
          <div v-else-if="statusError" class="error">{{ statusError }}</div>
          <div v-else class="status-info">
            <div class="status-item">
              <span class="label">Service Status:</span>
              <span class="value" :class="{ healthy: serviceStatus.status === 'healthy' }">
                {{ serviceStatus.status }}
              </span>
            </div>
            <div class="status-item">
              <span class="label">Service Name:</span>
              <span class="value">{{ serviceStatus.service }}</span>
            </div>
            <div class="status-item">
              <span class="label">Version:</span>
              <span class="value">{{ serviceStatus.version }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Reports',
  data() {
    return {
      loading: {
        users: false,
        items: false,
        comprehensive: false
      },
      statusLoading: true,
      statusError: null,
      serviceStatus: {
        status: 'unknown',
        service: 'PDF Reports',
        version: '1.0.0'
      }
    }
  },
  async mounted() {
    await this.checkServiceStatus()
  },
  methods: {
    async checkServiceStatus() {
      try {
        this.statusLoading = true
        this.serviceStatus = await api.getReportsHealth()
      } catch (err) {
        this.statusError = 'Failed to check reports service status'
        console.error('Error checking reports service status:', err)
      } finally {
        this.statusLoading = false
      }
    },
    
    async downloadUsersReport() {
      try {
        this.loading.users = true
        const pdfBlob = await api.getUsersReport()
        this.downloadFile(pdfBlob, 'users_report.pdf')
      } catch (err) {
        console.error('Error downloading users report:', err)
        alert('Failed to download users report. Please try again.')
      } finally {
        this.loading.users = false
      }
    },
    
    async downloadItemsReport() {
      try {
        this.loading.items = true
        const pdfBlob = await api.getItemsReport()
        this.downloadFile(pdfBlob, 'items_report.pdf')
      } catch (err) {
        console.error('Error downloading items report:', err)
        alert('Failed to download items report. Please try again.')
      } finally {
        this.loading.items = false
      }
    },
    
    async downloadComprehensiveReport() {
      try {
        this.loading.comprehensive = true
        const pdfBlob = await api.getComprehensiveReport()
        this.downloadFile(pdfBlob, 'comprehensive_report.pdf')
      } catch (err) {
        console.error('Error downloading comprehensive report:', err)
        alert('Failed to download comprehensive report. Please try again.')
      } finally {
        this.loading.comprehensive = false
      }
    },
    
    downloadFile(blob, filename) {
      // Create a temporary URL for the blob
      const url = window.URL.createObjectURL(blob)
      
      // Create a temporary link element
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      
      // Append the link to the document body
      document.body.appendChild(link)
      
      // Trigger the download
      link.click()
      
      // Clean up
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }
  }
}
</script>

<style scoped>
.reports {
  max-width: 1200px;
  margin: 0 auto;
}

.reports-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.report-section, .status-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.report-section h2, .status-section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
}

.report-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1rem;
}

.report-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.report-card h3 {
  color: #42b983;
  margin: 0 0 0.5rem 0;
}

.report-card p {
  color: #6c757d;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.report-actions {
  display: flex;
  justify-content: flex-start;
}

.btn-primary {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #3aa876;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.status-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.loading, .error {
  text-align: center;
  padding: 1rem;
  font-size: 1rem;
}

.error {
  color: #dc3545;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.status-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: bold;
  color: #495057;
}

.value {
  color: #6c757d;
}

.value.healthy {
  color: #28a745;
  font-weight: bold;
}

@media (max-width: 768px) {
  .reports-container {
    grid-template-columns: 1fr;
  }
  
  .report-cards {
    gap: 1rem;
  }
}
</style>
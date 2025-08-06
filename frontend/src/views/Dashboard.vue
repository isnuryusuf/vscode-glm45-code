<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="loading" class="loading">Loading dashboard data...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="dashboard-content">
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Users</h3>
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">Registered users</div>
        </div>
        
        <div class="stat-card">
          <h3>Active Users</h3>
          <div class="stat-value">{{ stats.active_users }}</div>
          <div class="stat-label">Currently active</div>
        </div>
        
        <div class="stat-card">
          <h3>Total Contacts</h3>
          <div class="stat-value">{{ stats.total_contacts }}</div>
          <div class="stat-label">Contact messages</div>
        </div>
        
        <div class="stat-card">
          <h3>Unresolved Contacts</h3>
          <div class="stat-value">{{ stats.unresolved_contacts }}</div>
          <div class="stat-label">Pending responses</div>
        </div>
        
        <div class="stat-card">
          <h3>Total Items</h3>
          <div class="stat-value">{{ stats.total_items }}</div>
          <div class="stat-label">Items in system</div>
        </div>
        
        <div class="stat-card">
          <h3>Recent Access</h3>
          <div class="stat-value">{{ stats.recent_access_count }}</div>
          <div class="stat-label">Last 7 days</div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <div class="chart-container">
          <h3>Access by Endpoint</h3>
          <div class="chart">
            <div v-for="(count, endpoint) in stats.access_by_endpoint" :key="endpoint" class="chart-bar">
              <div class="bar-label">{{ endpoint || 'Unknown' }}</div>
              <div class="bar-fill" :style="{ width: `${getBarWidth(count, stats.access_by_endpoint)}%` }">
                {{ count }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="chart-container">
          <h3>Access by Method</h3>
          <div class="chart">
            <div v-for="(count, method) in stats.access_by_method" :key="method" class="chart-bar">
              <div class="bar-label">{{ method || 'Unknown' }}</div>
              <div class="bar-fill" :style="{ width: `${getBarWidth(count, stats.access_by_method)}%` }">
                {{ count }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="chart-container">
          <h3>Access by Status Code</h3>
          <div class="chart">
            <div v-for="(count, status) in stats.access_by_status" :key="status" class="chart-bar">
              <div class="bar-label">{{ status || 'Unknown' }}</div>
              <div class="bar-fill" :style="{ width: `${getBarWidth(count, stats.access_by_status)}%` }">
                {{ count }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Access Logs -->
      <div class="recent-access">
        <h3>Recent Access Logs</h3>
        <div v-if="recentAccess.length === 0" class="empty">No recent access data available</div>
        <div v-else class="access-table">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>User</th>
                <th>IP Address</th>
                <th>Endpoint</th>
                <th>Method</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="access in recentAccess" :key="access.id">
                <td>{{ formatDateTime(access.access_time) }}</td>
                <td>{{ access.username || access.email || `User ${access.user_id}` }}</td>
                <td>{{ access.ip_address || 'N/A' }}</td>
                <td>{{ access.endpoint || 'N/A' }}</td>
                <td>{{ access.method || 'N/A' }}</td>
                <td>
                  <span :class="getStatusClass(access.status_code)">
                    {{ access.status_code || 'N/A' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        total_users: 0,
        active_users: 0,
        total_contacts: 0,
        unresolved_contacts: 0,
        total_items: 0,
        recent_access_count: 0,
        access_by_endpoint: {},
        access_by_method: {},
        access_by_status: {}
      },
      recentAccess: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true
        this.error = null
        
        // Load dashboard stats
        this.stats = await api.getDashboardStats()
        
        // Load recent access logs
        this.recentAccess = await api.getRecentAccess()
      } catch (err) {
        console.error('Error loading dashboard data:', err)
        this.error = 'Failed to load dashboard data. Please try again later.'
      } finally {
        this.loading = false
      }
    },
    
    getBarWidth(value, data) {
      const maxValue = Math.max(...Object.values(data), 1)
      return Math.max((value / maxValue) * 100, 5) // Minimum 5% width
    },
    
    getStatusClass(statusCode) {
      if (!statusCode) return 'status-unknown'
      if (statusCode >= 200 && statusCode < 300) return 'status-success'
      if (statusCode >= 300 && statusCode < 400) return 'status-redirect'
      if (statusCode >= 400 && statusCode < 500) return 'status-client-error'
      if (statusCode >= 500) return 'status-server-error'
      return 'status-unknown'
    },
    
    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.chart-container {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.chart-container h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.chart {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.chart-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.bar-label {
  min-width: 80px;
  font-size: 0.9rem;
  color: #6c757d;
}

.bar-fill {
  background: #42b983;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  text-align: center;
  min-width: 30px;
  transition: background-color 0.2s;
}

.bar-fill:hover {
  background: #3aa876;
}

.recent-access {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.recent-access h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.empty {
  text-align: center;
  color: #6c757d;
  padding: 2rem;
  font-style: italic;
}

.access-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

tr:hover {
  background: #f8f9fa;
}

.status-success {
  background: #d4edda;
  color: #155724;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-redirect {
  background: #fff3cd;
  color: #856404;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-client-error {
  background: #f8d7da;
  color: #721c24;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-server-error {
  background: #f8d7da;
  color: #721c24;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-unknown {
  background: #e2e3e5;
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .access-table {
    font-size: 0.9rem;
  }
  
  th, td {
    padding: 0.5rem;
  }
}
</style>
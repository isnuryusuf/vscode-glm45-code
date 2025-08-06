import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Items from '../views/Items.vue'
import Users from '../views/Users.vue'
import Reports from '../views/Reports.vue'
import Contact from '../views/Contact.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/items',
    name: 'Items',
    component: Items
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
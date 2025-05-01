import { createRouter, createWebHistory } from 'vue-router'
import Landing from './pages/Landing.vue'
import Dashboard from './pages/Dashboard.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import Resources from './pages/Resources.vue'
import Products from './pages/Products.vue'
import Planning from './pages/Planning.vue'
import Deliveries from './pages/Deliveries.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: Landing,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { hideTabs: true },
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { hideTabs: true },
  },
  {
    path: '/resources',
    name: 'resources',
    component: Resources,
  },
  {
    path: '/products',
    name: 'products',
    component: Products,
  },
  {
    path: '/planning',
    name: 'planning',
    component: Planning,
  },
  {
    path: '/deliveries',
    name: 'deliveries',
    component: Deliveries,
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import ('./pages/ForgotPassword.vue'),
  },
  {
    path: '/reset/:uid/:token',
    name: 'reset-password',
    compoent: () => import('./pages/ResetPassword.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

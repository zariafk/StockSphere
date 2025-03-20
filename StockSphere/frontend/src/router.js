import { createRouter, createWebHistory } from 'vue-router'
import Landing from './pages/Landing.vue'
import Dashboard from './pages/Dashboard.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

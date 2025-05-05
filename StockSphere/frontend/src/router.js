import { createRouter, createWebHistory } from 'vue-router'
import Landing from './pages/Landing.vue'
import Dashboard from './pages/Dashboard.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import Resources from './pages/Resources.vue'
import Products from './pages/Products.vue'
import Planning from './pages/Planning.vue'
import Deliveries from './pages/Deliveries.vue'
import ForumList from './pages/ForumList.vue'
import CommunityPosts from './pages/CommunityPosts.vue'
import CreatePost from './pages/CreatePost.vue'
import PostDetail from './pages/PostDetail.vue';


const routes = [
  {
    path: '/',
    name: 'landing',
    component: Landing,
    meta: { hideTabs: true }
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
    meta: {hideTabs: true }
  },
  {
    path: '/reset/:uid/:token',
    name: 'reset-password',
    component: () => import('./pages/ResetPassword.vue'),
  },
  {
    path: '/forum',
    name: 'ForumList',
    component: ForumList,
  },
  {
    path: '/forum/:communityId',
    name: 'CommunityPosts',
    component: CommunityPosts,
    props: true,
  },
  {
    path: '/forum/:communityId/post/create',
    name: 'CreatePost',
    component: CreatePost,
    props: true,
  },
  {
    path: '/forum/:communityId/post/:postId',
    name: 'PostDetail',
    component: PostDetail,
    props: true,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

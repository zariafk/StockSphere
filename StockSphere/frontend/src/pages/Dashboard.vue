<template>
    <div class="dashboard-container">
      <h1>Dashboard</h1>
  
      <!-- Notifications Section -->
      <div v-if="notificationStore.notifications.length">
        <div v-for="notification in notificationStore.notifications" :key="notification.id" class="notification">
          <p>{{ notification.message }}</p>
          <button @click="notificationStore.markAsRead(notification.id)">Mark as Read</button>
        </div>
      </div>
      <div v-else>
        <p>No new notifications.</p>
      </div>
  
      <!-- User Section -->
      <div v-if="authStore.isAuthenticated">
        <h2>Hello {{ authStore.user?.username }}!</h2>
        <button @click="logout">Logout</button>
      </div>
      <p v-else>
        You are not logged in. <router-link to="/login">Login</router-link>
      </p>
    </div>
  </template>
  
  <script setup>
    import { watch, onMounted } from 'vue';  // Import watch here
    import { useAuthStore } from '../store/auth';
    import { useNotificationStore } from '../store/notifications';
    
    const authStore = useAuthStore();
    const notificationStore = useNotificationStore();
    
    // Watch for changes in notifications
    watch(
      () => notificationStore.notifications,
      (newNotifications) => {
        console.log('Notifications updated:', newNotifications);
      }
    );
    
    onMounted(() => {
      console.log('Component mounted. Fetching notifications...');
      fetchNotifications();  // Call the function to fetch notifications when mounted
    });
    const fetchNotifications = async () => {
  try {
    const response = await fetch('/api/dashboard');
    if (!response.ok) {
      throw new Error('Failed to fetch notifications');
    }
    const data = await response.json();
    console.log('Raw API response:', data);  // Log the raw data to inspect its structure

    // Ensure that data is an array and contains the necessary notifications
    if (Array.isArray(data)) {
      notificationStore.notifications = data;  // Set the data to the store
    } else {
      console.error('Fetched data is not an array:', data);
    }
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
};

    </script>
    
  <style scoped>
  .dashboard-container {
    padding: 110px 65px;
    color: #eaeaea;
    text-align: left;
  }
  
  .notification {
    margin-bottom: 10px;
  }
  
  button {
    cursor: pointer;
  }
  </style>
  
<template>
    <div class="dashboard-container">
      <h1>Dashboard</h1>
  
      <!-- Notifications Section -->
      <div v-if="notificationStore.notifications.length">
        <div v-for="notification in notificationStore.notifications" :key="notification.id" class="notification">
          <p class="notification-message">{{ notification.message }}</p>
          <!-- Mark as Read Button -->
          <button @click="markAsRead(notification.id)" class="mark-read-button">Mark as Read</button>
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
    import { watch, onMounted } from 'vue';
    import { useAuthStore } from '../store/auth';
    import { useNotificationStore } from '../store/notifications';
    // In Dashboard.vue
import { getCSRFToken } from '../store/auth'; // Adjust the path based on where your auth.js is located
import { useRouter } from 'vue-router';

    const router = useRouter();
   const authStore = useAuthStore();
    const notificationStore = useNotificationStore();
  
    let notificationsFetched = false; // Flag to check if notifications have been fetched already
  
    // Watch for changes in notifications
    watch(
      () => notificationStore.notifications,
      (newNotifications) => {
        console.log('Notifications updated:', newNotifications);
      }
    );
  
    onMounted(() => {
      console.log('Component mounted. Checking if notifications need fetching...');
      if (!notificationsFetched) {
        fetchNotifications();  // Fetch notifications if not already fetched
      }
    });
  
    const fetchNotifications = async () => {
      try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
          throw new Error('Failed to fetch notifications');
        }
        const data = await response.json();
        console.log('Raw API response:', data);
  
        // Ensure that data is an array and contains the necessary notifications
        if (Array.isArray(data)) {
          notificationStore.notifications = data;  // Set the data to the store
          notificationsFetched = true; // Mark as fetched to avoid fetching again
        } else {
          console.error('Fetched data is not an array:', data);
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    };

    const logout = async () => {
  await authStore.logout(router);
    }
  
    const markAsRead = async (notificationId) => {
  console.log(`Marking notification with ID ${notificationId} as read`);

  // Update the notification in the frontend store (mark it as read)
  const notification = notificationStore.notifications.find(
    (notif) => notif.id === notificationId
  );
  
  if (notification) {
    notification.is_read = true;  // Mark as read in the frontend store
  }

  // Remove the notification from the list (it will disappear from the UI)
  notificationStore.notifications = notificationStore.notifications.filter(
    (notif) => notif.id !== notificationId
  );

  // Send an API request to mark the notification as read in the backend
  try {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    const response = await fetch(`http://localhost:8000/api/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include',
    });

    if (response.ok) {
      console.log('Notification marked as read in the backend');
    } else {
      console.error('Failed to mark notification as read in the backend');
    }
  } catch (error) {
    console.error('Error marking notification as read:', error);
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
      display: flex;  /* Align the notification message and button horizontally */
      align-items: center;  /* Vertically center the items */
    }
  
    .notification-message {
      margin-right: 10px;  /* Add space between the message and button */
    }
  
    .mark-read-button {
      cursor: pointer;
    }
  </style>
  
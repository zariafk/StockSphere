import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],  // Pinia automatically makes this state reactive
  }),
  actions: {
    // Fetch notifications from the API (if needed)
    async fetchNotifications() {
      try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
          throw new Error(`Failed to fetch notifications: ${response.statusText}`);
        }
        const data = await response.json();
        this.notifications = data;  // Update the notifications array directly
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    },
    
    // Mark a notification as read
    markAsRead(id) {
      const notification = this.notifications.find(n => n.id === id);
      if (notification) notification.is_read = true;
    },
  },
});

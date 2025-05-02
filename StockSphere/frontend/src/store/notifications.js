import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],  // Pinia automatically makes this state reactive
    notificationsFetched: false,  // Flag to track if notifications are already fetched
  }),
  actions: {
    // Fetch notifications from the API (if needed)
    async fetchNotifications() {
      if (this.notificationsFetched) return; // Skip fetching if already done
      try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
          throw new Error(`Failed to fetch notifications: ${response.statusText}`);
        }
        const data = await response.json();
        this.notifications = data;  // Update the notifications array directly
        this.notificationsFetched = true;  // Mark as fetched
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    },

    // Mark a notification as read
    markAsRead(id) {
      const notification = this.notifications.find(n => n.id === id);
      if (notification) notification.is_read = true;
    },

    // Reset the fetched flag if needed (for example, if you log out or refresh)
    resetNotifications() {
      this.notificationsFetched = false;
      this.notifications = [];  // Optionally clear notifications as well
    }
  },
});

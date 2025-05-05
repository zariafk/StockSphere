import { defineStore } from 'pinia'

// Define the Pinia store for authentication
export const useAuthStore = defineStore('auth', {
  state: () => {
    // Load stored state from localStorage or set default state
    const storedState = localStorage.getItem('authState')
    return storedState
      ? JSON.parse(storedState) // Parse the stored state if it exists
      : {
          user: null, // No user logged in by default
          isAuthenticated: false, // Default authentication state
        }
  },
  actions: {
    // Set CSRF token in the session
    async setCsrfToken() {
      await fetch('http://localhost:8000/api/set-csrf-token', {
        method: 'GET',
        credentials: 'include', // Send cookies along with the request
      })
    },

    // Attempt to log the user in with username and password
    async login(username, password) {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(), // Include CSRF token
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include', // Send cookies with request
      })
    
      const data = await response.json()
    
      if (data.success) {
        // If login successful, 2FA required
        return { requires2FA: true }
      } else {
        // If login fails, reset user state and save to localStorage
        this.user = null
        this.isAuthenticated = false
        this.saveState()
        return { requires2FA: false, error: data.message }
      }
    },

    // Verify the 2FA code, authenticate user
    async verify2FA(code, router = null) {
      const response = await fetch('http://localhost:8000/api/verify-2fa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(), // Include CSRF token
        },
        body: JSON.stringify({ code }),
        credentials: 'include',
      });
    
      const data = await response.json();
    
      if (data.success) {
        // If 2FA successful, fetch user data and mark as authenticated
        await this.fetchUser(); // Populates user info
        this.isAuthenticated = true;
        this.saveState(); // Save updated state to localStorage
    
        if (router) {
          // Redirect to dashboard
          await router.push({ name: 'dashboard' });
        }
      } else {
        // Throw error if invalid 2FA
        throw new Error(data.message || 'Invalid 2FA code');
      }
    },    
    
    // Logout the user and clear authentication state
    async logout(router = null) {
      try {
        const response = await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken(), // Include CSRF token
          },
          credentials: 'include', // Send cookies with request
        })
        if (response.ok) {
          // Reset user state and redirect to login page
          this.user = null
          this.isAuthenticated = false
          this.saveState()
          if (router) {
            await router.push({
              name: 'login',
            })
          }
        }
      } catch (error) {
        console.error('Logout failed', error)
        throw error
      }
    },

    // Fetch the current user date from the server
    async fetchUser() {
      try {
        const response = await fetch('http://localhost:8000/api/user', {
          credentials: 'include', // Send cookie with request
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Icnlude CSRF token
          },
        })
        if (response.ok) {
          const data = await response.json()
          this.user = data // Store user data
          this.isAuthenticated = true
        } else {
          this.user = null // If user data not found, reset state
          this.isAuthenticated = false
        }
      } catch (error) {
        console.error('Failed to fetch user', error)
        this.user = null
        this.isAuthenticated = false
      }
      this.saveState() // Save updated state to localStorage
    },

    // Save current state to localStorage to persist it across page reloads
    saveState() {
      localStorage.setItem(
        'authState',
        JSON.stringify({
          user: this.user,
          isAuthenticated: this.isAuthenticated,
        }),
      )
    },
  },
})

// Utility function to retrieve the CSRF token from the cookies
export function getCSRFToken() {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  // Throw error if CSRF cookie not found
  if (cookieValue === null) { 
    throw 'Missing CSRF cookie.'
  }
  return cookieValue
}

<template>
    <div class="login-container">
      <div class="form-card">
        <h1>Login</h1>
  
        <!-- Step 1: Username/Password -->
        <form v-if="!requires2FA" @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Username:</label>
            <input v-model="username" type="text" required @input="resetError" />
          </div>
  
          <div class="form-group">
            <label>Password:</label>
            <input v-model="password" type="password" required @input="resetError" />
          </div>
  
          <button class="primary-button" type="submit">Login</button>
        </form>
  
        <!-- Step 2: 2FA Code -->
        <form v-else @submit.prevent="submit2FA">
          <div class="form-group">
            <label>Enter 2FA Code (check your email):</label>
            <input v-model="code" type="text" required maxlength="6" />
          </div>
  
          <button class="primary-button" type="submit">Verify</button>
          <button class="secondary-button" @click="cancel2FA" type="button">Cancel</button>
        </form>
  
        <p v-if="error" class="error-text">{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '../store/auth'
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        code: '',
        error: '',
        requires2FA: false,
      }
    },
    setup() {
      const authStore = useAuthStore()
      return { authStore }
    },
    methods: {
      resetError() {
        this.error = ''
      },
      async handleLogin() {
        try {
          this.error = ''
          const result = await this.authStore.login(this.username, this.password)
          if (result.requires2FA) {
            this.requires2FA = true
          } else {
            this.error = result.error || 'Login failed'
          }
        } catch (err) {
          this.error = 'Login error: ' + err.message
        }
      },
      async submit2FA() {
        try {
          await this.authStore.verify2FA(this.code, this.$router)
        } catch (err) {
          this.error = err.message || 'Invalid code'
        }
      },
      cancel2FA() {
        this.requires2FA = false
        this.password = ''
        this.code = ''
        this.error = ''
      },
    },
  }
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  .form-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  .form-group {
    margin-bottom: 1rem;
  }
  .primary-button {
    background: #007bff;
    color: white;
    padding: 0.5rem 1.2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .secondary-button {
    margin-left: 1rem;
    padding: 0.5rem 1rem;
  }
  .error-text {
    color: red;
    margin-top: 1rem;
  }
  </style>
  
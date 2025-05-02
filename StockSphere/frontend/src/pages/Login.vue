<template>
    <div class="login-wrapper">
      <div class="login-card">
        <!-- Left side -->
        <div class="login-left">
          <h1>Welcome Back</h1>
          <p>Enter your credentials to continue to StockSphere.</p>
        </div>
  
        <!-- Right side -->
        <div class="login-right">
          <h2 v-if="!requires2FA">Login</h2>
          <h2 v-else>Two-Factor Authentication</h2>
  
          <!-- Step 1: Username/Password -->
          <form v-if="!requires2FA" @submit.prevent="handleLogin">
            <label for="username">Username</label>
            <input v-model="username" id="username" type="text" required @input="resetError" />
  
            <label for="password">Password</label>
            <input v-model="password" id="password" type="password" required @input="resetError" />
  
            <button type="submit">Login</button>
            <router-link to="/forgot-password" class="forgot-link">Forgot Password?</router-link>
          </form>
  
          <!-- Step 2: 2FA Code -->
          <form v-else @submit.prevent="submit2FA">
            <label for="code">Enter 2FA Code</label>
            <input v-model="code" id="code" type="text" required maxlength="6" />
  
            <button type="submit">Verify</button>
            <button type="button" class="cancel" @click="cancel2FA">Cancel</button>
          </form>
  
          <p v-if="error" class="error">{{ error }}</p>
        </div>
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
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
  
  .login-wrapper {
    min-height: 100vh;
    background-color: #171a23;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Inter', sans-serif;
    padding: 4rem;
  }
  
  .login-card {
    display: flex;
    background-color: #171a23;
    color: #eaeaea;
    border-radius: 12px;
    overflow: hidden;
    width: 100%;
    max-width: 850px;
    box-shadow: none;
  }
  
  .login-left {
    flex: 1;
    padding: 2rem;
    background-color: #1b1e27;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .login-left h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #ffffff;
  }
  
  .login-left p {
    font-size: 1rem;
    color: #bbbbbb;
  }
  
  .login-right {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .login-right h2 {
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-top: 1rem;
    margin-bottom: 0.3rem;
    font-weight: 500;
  }
  
  input {
    padding: 0.6rem;
    font-size: 1rem;
    border: 1px solid #444;
    background-color: #2c2c2c;
    color: #fff;
    border-radius: 6px;
  }
  
  input:focus {
    outline: none;
    border-color: #b43de6;
  }
  
  button[type="submit"] {
    margin-top: 1.5rem;
    padding: 0.6rem;
    font-size: 1rem;
    border: none;
    border-radius: 6px;
    background-color: #b43de6;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  button[type="submit"]:hover {
    background-color: #a12dd5;
  }
  
  button.cancel {
    margin-top: 1rem;
    background: transparent;
    color: #ccc;
    border: 1px solid #666;
  }
  
  button.cancel:hover {
    border-color: #999;
    color: #fff;
  }
  
  .error {
    color: #ff6b6b;
    margin-top: 1.2rem;
    text-align: center;
  }
  .forgot-link {
  color: #b43de6;
  margin-top: 1rem;
  text-align: center;
  display: block;
  text-decoration: underline;
  cursor: pointer;
}
  </style>
  
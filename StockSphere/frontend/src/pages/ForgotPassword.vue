<template>
  <div class="forgot-password">
    <h2>Forgot Password</h2>
    <!-- For forgot password feature -->
    <form @submit.prevent="submitEmail">
      <input type="email" v-model="email" placeholder="Enter your email" required />
      <button type="submit">Send Reset Link</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>
  
<script>
  export default {
    data() {
      return {
        email: '',
        message: '',
      };
    },
    methods: {
      // Function to get CSRF token from cookies
      getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      },
      
      // Method to submit email for password reset
      async submitEmail() {
        const csrfToken = this.getCSRFToken();  // Get CSRF token from cookies

        try {
          const response = await fetch('http://localhost:8000/password_reset', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,  // Include CSRF token in the request header
            },
            credentials: 'include',  // Ensure cookies are sent with the request
            body: JSON.stringify({ email: this.email }),  // Send the email entered by the user
          });

          // Check if the response is in JSON format
          if (response.ok) {
            const data = await response.json();
            this.message = data.message || 'Check your email for a reset link.';
          } else {
            const errorData = await response.json();
            this.message = errorData.error || 'An error occurred while sending the reset link.';
          }
        } catch (error) {
          // Handle network or unexpected errors
          this.message = 'Something went wrong, please try again later.';
        }
      }
    },
  };
</script>
  
<style scoped>
  .forgot-password {
    max-width: 400px;
    margin: 100px auto;
    margin-left: 400px;
    margin-top: 100px;
    padding: 1.5rem;
    background-color: #292929;
    color: #f0f0f0;
    border-radius: 8px;
  }
  
  .forgot-password h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .forgot-password input {
    width: 100%;
    padding: 0.8rem;
    font-size: 1rem;
    margin-bottom: 1rem;
    border-radius: 6px;
    border: 1px solid #444;
  }
  
  .forgot-password button {
    padding: 0.8rem;
    font-size: 1rem;
    background-color: #b43de6;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    width: 100%;
  }
  
  .forgot-password button:hover {
    background-color: #a12dd5;
  }
  
  .forgot-password p {
    text-align: center;
    color: green;
    margin-top: 1rem;
  }
</style>
  
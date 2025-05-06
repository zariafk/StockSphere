<template>
    <div class="reset-password">
      <h2>Reset Password</h2>
      <!-- Resetting password -->
      <form @submit.prevent="submitPassword">
        <input type="password" v-model="password1" placeholder="New password" required />
        <input type="password" v-model="password2" placeholder="Confirm password" required />
        <button type="submit">Reset Password</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        password1: '',
        password2: '',
        message: '',
      };
    },
    methods: {
      async submitPassword() {
        const uid = this.$route.params.uid;  // Uid is passed in URL
        const token = this.$route.params.token;  // Token is passed in URL
  
        // POST request for new password
        const response = await fetch(`http://localhost:8000/password_reset_confirm/${uid}/${token}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', 
          body: JSON.stringify({
            new_password1: this.password1,
            new_password2: this.password2,
          }),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          this.message = 'Your password has been reset successfully.';
          this.$router.push('/login');  // Redirect to login after successful reset
        } else {
          this.message = data.error || 'Error resetting password. Check passwords or link expiry.';
        }
      },
    },
  };
</script>
  
<template>
    <div class="register-container">
        <div class="form-card">
            <h2>Sign Up</h2> 
            <form @submit.prevent = "register">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="business_name">Business Name:</label>
                        <input v-model="business_name" id="business_name" type="text" required>
                    </div>
                    <div class="form-group">
                        <label for="username">Username:</label>
                        <input v-model="username" id="username" type="text" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input v-model="email" id="email" type="email" required>
                    </div> 
                    <div class="form-group">
                        <label for="role">Role:</label>
                        <input v-model="role" id="role" type="text" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input v-model="password" id="password" type="password" required>
                    </div> 
                    <div class="form-group">
                        <label for="password_confirm">Re-Enter Password</label>
                        <input v-model="password_confirm" id="password_confirm" type="password" required>
                    </div>
                </div>

                <p class="note">
                    Note: you will automatically be assigned full access.
                </p>
            
                <button class="primary-button" type="submit">Sign Up</button> 
            </form> 
            <p v-if = "error" class="error-text">Passwords do not match.</p>
            <p v-if="success" class="success-text">{{success}}</p> 
        </div>
    </div>
</template>

<script>
    import {
        getCSRFToken
    } from '../store/auth'

export default {
    data() {
        return {
            business_name: '',
            username: '',
            email: '',
            role: '',
            password: '',
            password_confirm: '',
            error: '',
            success: ''
        }
    },
    methods: {
        async register() {
            try {
                const response = await fetch('http://localhost:8000/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        business_name: this.business_name,
                        username: this.username,
                        email: this.email,
                        role: this.role,
                        password: this.password,
                        password_confirm: this.password_confirm
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.success = 'Registration successful! Please log in.'
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 1000)
                } else {
                    this.error = data.error || 'Registration failed'
                }
            } catch (err) {
                this.error = 'An error occurred during registration: ' + err
            }
        }
    }
} 
</script>

<style scoped>
    .register-container {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        min-height: 100vh; /* Fill the full browser height */
        padding: 2rem;
    }
    
    .form-card {
        background: #fff;
        border-radius: 8px;
        width: 600px;
        max-width: 90%;
        padding: 2rem;
    }

    .form-card h2 {
        text-align: left;
        margin-top: 0;
        margin-bottom: 1.5rem;
        color: #000; /* Adjust to your brand color */
    }
    
    /* 
      A two-column grid for the input fields:
      each row has two inputs side by side.
    */
    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem; /* space between columns and rows */
        margin-bottom: 1rem;
    }
    
    /* 
      Each field group (label + input).
    */
    .form-group {
        display: flex;
        flex-direction: column;
    }
    
    .form-group label {
        text-align: left;
        color: #000;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .form-group input {
        color: #000;
        background-color: #fff;
        padding: 0.5rem;
        border: 3px solid #d44cfc;
        border-radius: 4px;
    }
    
    /* 
      A small note text.
    */
    .note {
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #000;
    }
    
    /* 
      Main action button: 
      pink background, white text, etc.
    */
    .primary-button {
        background-color: #d44cfc;
        color: #000;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .primary-button:hover {
        background-color: #d44cfc;
    }
    
    /* 
      Error and success text styling.
    */
    .error-text {
        color: red;
        margin-top: 1rem;
    }
</style>

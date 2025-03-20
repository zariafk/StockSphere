<template>
    <div class="register-container">
        <div class="form-card">
            <h1>Sign Up</h1> 
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
        padding: 100px 0px;
        padding: 2rem;
        min-height: calc(100vh - 120px);
        overflow: auto;
        background-color: #171A23; /* Purple & deeper purple */ /* Slightly warm dark */
    }

    
    
    .form-card {
        background: #171A23;
        border-radius: 8px;
        width: 600px;
        max-width: 90%;
        padding: 50px 15px;
        margin-top: 20px;
        color: #EAEAEA;
        text-align: left;
        overflow: auto;
        margin-bottom: 30px;
    }

    .form-card h2 {
        text-align: left;
        margin-top: 0;
        margin-bottom: 1.5rem;
        color: #EAEAEA;
    }
    
    /* 
      A two-column grid for the input fields:
      each row has two inputs side by side.
    */
    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem 5rem; /* space between columns and rows */
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
        color: #EAEAEA;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .form-group input {
        width: 100%;
        padding: 12px 14px;
        border: 2px solid #b54de6; /* Subtle border */
        border-radius: 8px; /* Rounded edges for modern look */
        font-size: 1rem;
        transition: all 0.3s ease-in-out; /* Smooth transitions */
        background-color: #D1D5DB; /* Light background for contrast */
        box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.1); /* Soft inner shadow */
        color: black;
    }

    .form-group input:focus {
        border-color: #9c3fd9; /* Darker shade for interaction */
        background-color: white;
        outline: none;
        box-shadow: 0px 4px 8px rgba(42, 1, 61, 0.3); /* Glow effect */
    }
    
    /* 
      A small note text.
    */
    .note {
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #eaeaea;
    }
    
    /* 
      Main action button: 
      pink background, white text, etc.
    */
    .primary-button {
        display: inline-block;
    padding: 12px 20px;
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #b54de6, #9c3fd9); /* Soft gradient */
    border: none;
    border-radius: 8px; /* Rounded corners */
    cursor: pointer;
    text-align: center;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 4px 10px rgba(181, 77, 230, 0.3); /* Soft outer shadow */
    }
    
    .primary-button:hover {
        background-color: #b54de6;
    }
    
    /* 
      Error and success text styling.
    */
    .error-text {
        color: red;
        margin-top: 1rem;
    }
</style>

<template>
    <div class="login-container">
        <div class="form-card">
            <h2>Login</h2> 
            <form @submit.prevent="login">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="username">Username:</label> 
                        <input v-model="username" id = "username" type = "text" required @input="resetError">
                    </div> 
                    <div class="form-group">
                        <label for="password">Password:</label> 
                        <input v-model="password" id = "password" type = "password" required @input = "resetError" >
                    </div>
                </div>
            
                <button class="primary-button" type="submit">Login</button> 
            </form> 
            <p v-if = "error" class = "error-text" > {{error}}</p> 
        </div>
    </div> 
</template>

<script>
import { useAuthStore } from '../store/auth'

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore
        }
    },
    data() {
        return {
            username: "",
            password: "",
            error: ""
        }
    },
    methods: {
        async login() {
            await this.authStore.login(this.username, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.error = 'Login failed. Please check your credentials.'
            }
        },
        resetError() {
            this.error = ""
        },
    }
} 
</script>

<style scoped>
    .login-container {
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

    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem; /* space between columns and rows */
        margin-bottom: 1rem;
    }

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
        border: 3px solid #b54de6;
        border-radius: 4px;
    }

    .primary-button {
        background-color: #b54de6;
        color: #000;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .primary-button:hover {
        background-color: #b54de6;
    }

    .error-text {
        color: red;
        margin-top: 1rem;
    }
</style>
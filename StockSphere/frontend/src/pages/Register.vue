<template>
    <div>
        <h2>Register</h2> 
        <form @submit.prevent = "register">
            <div>
                <label for="business_name">Business Name:</label>
                <input v-model="business_name" id="business_name" type="text" required>
            </div>
            <div>
                <label for="username">Username:</label>
                <input v-model="username" id="username" type="text" required>
            </div>
            <div>
                <label for="email">Email:</label>
                <input v-model="email" id="email" type="email" required>
            </div> 
            <div>
                <label for="role">Role:</label>
                <input v-model="role" id="role" type="text" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input v-model="password" id="password" type="password" required>
            </div> 
            <div>
                <label for="password_confirm">Re-Enter Password</label>
                <input v-model="password_confirm" id="password_confirm" type="password" required>
            </div>
            <button type="submit">Register</button> 
        </form> 
        <p v-if = "error" >{{error}}</p>
        <p v-if="success">{{success}}</p> 
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

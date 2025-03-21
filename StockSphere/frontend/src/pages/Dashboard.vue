<template>
    <div class="dashboard-container">
        <h1>Dashboard</h1> 
        <div v-if = "authStore.isAuthenticated">
            <h2>Hello {{authStore.user?.username}}!</h2> 
            <button @click = "logout" >Logout</button> 
        </div> 
        <p v-else>
            You are not logged in.<router-link to="/login">Login</router-link>
        </p> 
    </div>
</template>

<script>
    import {
        useAuthStore
    } from '../store/auth.js'
import {
    useRouter
} from 'vue-router'

export default {
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()

        return {
            authStore,
            router
        }
    },
    methods: {
        async logout() {
            try {
                await this.authStore.logout(this.$router)
            } catch (error) {
                console.error(error)
            }
        }
    },
    async mounted() {
        await this.authStore.fetchUser()
    }
} 
</script>

<style scoped>
    .dashboard-container {
        padding: 110px 65px;
        color: #eaeaea;
        text-align: left;
    }
</style>
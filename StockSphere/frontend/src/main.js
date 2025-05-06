import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css' 
import router from './router'
import App from './App.vue'
import { useAuthStore } from './store/auth'
import { useDeliveriesStore } from './store/deliveries'


const app = createApp(App)

app.use(createPinia())
app.use(router)

const authStore = useAuthStore()
authStore.setCsrfToken()

// DEV-ONLY: expose the delivery store for manual tweaks in console
if (import.meta.env.DEV) {
    window.deliveryStore = useDeliveriesStore()
}

app.mount('#app')

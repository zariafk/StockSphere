import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Proxy all requests starting with '/api' to the Django backend
      '/api': 'http://localhost:8000',
    }
  }
})

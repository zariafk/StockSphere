// src/store/products.js
import { defineStore } from 'pinia';

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],        // ← will hold array of product objects
  }),

  actions: {
    async fetchProducts() {
      // replace with real API call or local mock
      this.products = [];
    },
    async addProduct(payload) {
      // push locally or POST to server, then:
      this.products.push({ id: Date.now(), ...payload });
    },
    async updateProduct(id, payload) {
      const idx = this.products.findIndex(p => p.id === id);
      if (idx !== -1) this.products[idx] = { id, ...payload };
    },
    async deleteProduct(id) {
      this.products = this.products.filter(p => p.id !== id);
    },
  },
});

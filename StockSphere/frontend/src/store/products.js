import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getCSRFToken } from './auth'; // CSRF token helper like in the resource store

export const useProductStore = defineStore('products', () => {
  const products = ref([]);  // This will store products

  // Fetch products from the API
  const fetchProducts = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/products", {
        headers: { 
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
      });
      products.value = await response.json();  // Populate the products array with the fetched data
    } catch (error) {
      console.error("Failed to fetch products", error);
    }
  };

  // Add a new product
  const addProduct = async (productData) => {
    try {
      const response = await fetch("http://localhost:8000/api/products/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
        body: JSON.stringify(productData),
      });

      const newProduct = await response.json();
      products.value.push(newProduct);  // Add the newly created product to the store
    } catch (error) {
      console.error("Failed to add product", error);
    }
  };

  // Update a product
  const updateProduct = async (id, updatedData) => {
    try {
      const response = await fetch(`http://localhost:8000/api/products/${id}/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
        body: JSON.stringify(updatedData),
      });

      if (response.ok) {
        const updatedProduct = await response.json();
        const index = products.value.findIndex((p) => p.id === id);
        if (index !== -1) products.value[index] = updatedProduct;  // Update the product in the store
      }
    } catch (error) {
      console.error("Failed to update product", error);
    }
  };

  // Delete a product
  const deleteProduct = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/products/${id}/delete`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
      });

      if (response.ok) {
        products.value = products.value.filter((p) => p.id !== id);  // Remove the product from the store
      }
    } catch (error) {
      console.error("Failed to delete product", error);
    }
  };

  return { products, fetchProducts, addProduct, updateProduct, deleteProduct };
});

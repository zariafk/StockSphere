import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore, getCSRFToken } from "./auth";

export const useResourceStore = defineStore("resource", () => {
    const authStore = useAuthStore();
    const resources = ref([]);

    // Fetch only the authenticated user's products
    const fetchResources = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/resources", {
                headers: { 
                    "X-CSRFToken": getCSRFToken(), 
                },
                credentials: "include",
            });
            resources.value = await response.json();
        } catch (error) {
            console.error("Failed to fetch resources", error);
        }
    };

    // Add a new resource
    const addResource = async (resourceData) => {
        try {
            const response = await fetch("http://localhost:8000/api/resources/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                credentials: "include",
                body: JSON.stringify(resourceData),
            });

            const newResource = await response.json();
            resources.value.push(newResource);  // Update store
        } catch (error) {
            console.error("Failed to add resource", error);
        }
    };

    const updateResource = async (id, updatedData) => {
        try {
          const response = await fetch(`http://localhost:8000/api/resources/${id}/update`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
            body: JSON.stringify(updatedData),
          })
      
          if (response.ok) {
            const updated = await response.json()
            const index = resources.value.findIndex((r) => r.id === id)
            if (index !== -1) resources.value[index] = updated
          }
        } catch (error) {
          console.error("Failed to update resource", error)
        }
      }
      
      // Delete resource
      const deleteResource = async (id) => {
        try {
          const response = await fetch(`http://localhost:8000/api/resources/${id}/delete`, {
            method: "DELETE",
            headers: {
              "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
          })
      
          if (response.ok) {
            resources.value = resources.value.filter((r) => r.id !== id)
          }
        } catch (error) {
          console.error("Failed to delete resource", error)
        }
      }
    return { resources, fetchResources, addResource, updateResource, deleteResource };
});


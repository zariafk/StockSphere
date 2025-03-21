import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export const useResourceStore = defineStore("resource", () => {
    const authStore = useAuthStore();
    const resources = ref([]);

    // Fetch only the authenticated user's products
    const fetchResources = async () => {
        if (!authStore.token) return;

        try {
            const response = await fetch("http://localhost:8000/api/resources/", {
                headers: { Authorization: `Bearer ${authStore.token}` },
            });
            resources.value = await response.json();
        } catch (error) {
            console.error("Failed to fetch resources", error);
        }
    };

    // Add a new resource
    const addResource = async (resourceData) => {
        if (!authStore.token) return;

        try {
            const response = await fetch("http://localhost:8000/api/resources/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${authStore.token}`,
                },
                body: JSON.stringify(resourceData),
            });

            const newResource = await response.json();
            resources.value.push(newResource);  // Update store
        } catch (error) {
            console.error("Failed to add resource", error);
        }
    };

    return { resources, fetchResources, addResource };
});

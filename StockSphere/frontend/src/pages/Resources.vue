<template>
    <div class="resources-container">
        <h1>Resources</h1>
            <ul>
                <li v-for="resource in resourceStore.resources" :key="resource.id">
                    {{ resource.name }} - ${{ resource.price_per_pack }} ({{ resource.units_per_pack }} units per pack)
                </li>
            </ul>

            <button class="open-modal" @click="showModal = true">Add resource</button>

            <div v-if="showModal" class="modal-overlay">
                <div class="modal">
                    <h2>Add resource</h2>

                    <div class="grid-container">
                        <div class="form-group">
                            <label class="column-headings">Name</label>
                            <input v-model="name" placeholder="Resource Name" />
                        </div>
    
                        <div class="form-group">
                            <label class="column-headings">Price per Pack</label>
                            <input v-model="price_per_pack" placeholder="Price per Pack" type="number" />
                        </div>
        
                        <div class="form-group">
                            <label class="column-headings">Units per Pack</label>
                            <input v-model="units_per_pack" placeholder="Units per Pack" type="number" />
                        </div>
        
                        <div class="form-group">
                            <label class="column-headings">Available Units</label>
                            <input v-model="available_units" placeholder="Available Units" type="number" />
                        </div>
        
                        <div class="form-group">
                            <label class="column-headings">Notes</label>
                            <textarea v-model="notes" placeholder="Notes"></textarea>
                        </div>

                        <div class="modal-buttons">
                            <button class="submit-button" @click="addResource">Add Resource</button>
                            <button class="close-button" @click="showModal = false">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
    </div>
</template>
    
<script setup>
    import { onMounted, ref } from "vue";
    import { useResourceStore } from "../store/resources";

    const resourceStore = useResourceStore();
    const showModal = ref(false);
    const name = ref("");
    const price_per_pack = ref("");
    const units_per_pack = ref("");
    const available_units = ref("");
    const arriving_units = ref("");
    const notes = ref("");
        
    onMounted(() => {
        resourceStore.fetchResources();
    });
        
    const addResource = async () => {
    await resourceStore.addResource({
        name: name.value,
        price_per_pack: parseFloat(price_per_pack.value),
        units_per_pack: parseInt(units_per_pack.value),
        available_units: parseInt(available_units.value),
        arriving_units: parseInt(arriving_units.value),
        notes: notes.value
    });
        
        name.value = "";
        price_per_pack.value = "";
        units_per_pack.value = "";
        available_units.value = "";
        arriving_units.value = "";
        notes.value = "";

        showModal.value = false;
    };
</script>

<style scoped>
    .resources-container {
        color: #eaeaea;
        margin-top: 100px;
        margin-left: 70px;
        text-align: left;
    }

    .form {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 16px;
    }

    .form-group {
        display: flex;
        flex-direction: column;
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5); /* Dark transparent overlay */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .modal {
        background: #171a23;
        padding: 20px;
        border-radius: 10px;
        width: 500px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        text-align: left;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-top: 10px;
    }

    .column-headings {
        font-weight: bold;
    }

    .modal-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }

    .submit-button {
        padding: 10px;
        background-color: #28a745;
        color: white;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        flex: 1;
        margin-right: 10px;
    }

    .close-button {
        padding: 10px;
        background-color: #dc3545;
        color: white;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        flex: 1;
    }
</style>
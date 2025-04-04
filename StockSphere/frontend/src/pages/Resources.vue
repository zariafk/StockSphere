<template>
    <div class="resources-container">
        <h1>Resources</h1>
            <table class="resource-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Price Per Pack</th>
                        <th>Units Per Pack</th>
                        <th>Unit Price</th>
                        <th>Available Units</th>
                        <th>Arriving Units</th>
                        <th>Notes</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="resource in resourceStore.resources" :key="resource.id">
                        <td>{{ resource.name }}</td>
                        <td>${{ Number(resource.price_per_pack).toFixed(2) }}</td>
                        <td>{{ resource.units_per_pack }}</td>
                        <td>${{ Number(resource.unit_price).toFixed(2) }}</td>
                        <td>{{ resource.available_units }}</td>
                        <td>{{ resource.arriving_units }}</td>
                        <td>{{ resource.notes }}</td>
                        <td>
                            <PencilLine size="16" class="icon-button edit" @click="startEdit(resource)" title="Edit" />
                            <Trash2 size="16" class="icon-button delete" @click="deleteResource(resource.id)" title="Delete" />
                        </td>
                    </tr>
                </tbody>
            </table>

            <button class="open-modal" @click="openAddResourceModal">Add resource</button>

            <div v-if="showModal" class="modal-overlay">
                <div class="modal">
                    <h2>{{ editMode ? "Edit Resource" : "Add resource" }}</h2>

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
                            <button class="submit-button" @click="saveResource">{{ editMode ? "Save Changes" : "Add Resource" }}</button>
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
    import { PencilLine, Trash2 } from 'lucide-vue-next';

    const resourceStore = useResourceStore();
    const showModal = ref(false);

    const name = ref("");
    const price_per_pack = ref("");
    const units_per_pack = ref("");
    const available_units = ref("");
    const arriving_units = ref("");
    const notes = ref("");

    const editMode = ref(false)
    const editingId = ref(null)
        
    onMounted(() => {
        resourceStore.fetchResources();
    });

    const saveResource = async () => {
        const payload = {
            name: name.value,
            price_per_pack: parseFloat(price_per_pack.value),
            units_per_pack: parseInt(units_per_pack.value),
            available_units: parseInt(available_units.value),
            arriving_units: parseInt(arriving_units.value),
            notes: notes.value,
        }

        if (editMode.value && editingId.value !== null) {
            await resourceStore.updateResource(editingId.value, payload)
        } else {
            await resourceStore.addResource(payload)
        }

        resetForm()
        showModal.value = false
    }

    const startEdit = (resource) => {
        name.value = resource.name
        price_per_pack.value = resource.price_per_pack
        units_per_pack.value = resource.units_per_pack
        available_units.value = resource.available_units
        arriving_units.value = resource.arriving_units
        notes.value = resource.notes
        editingId.value = resource.id
        editMode.value = true
        showModal.value = true
    }

    const resetForm = () => {
        name.value = ""
        price_per_pack.value = ""
        units_per_pack.value = ""
        available_units.value = ""
        arriving_units.value = ""
        notes.value = ""
        editingId.value = null
        editMode.value = false
    }

    const openAddResourceModal = () => {
        resetForm();          // This sets editMode.value = false for sure
        showModal.value = true;
    };

    const deleteResource = async (id) => {
        await resourceStore.deleteResource(id)
    }
        
    /*
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
    };*/
</script>

<style scoped>
    .resources-container {
        color: #eaeaea;
        margin-top: 100px;
        margin-left: 70px;
        text-align: left;
    }

    .resource-table {
        width: 100%;
        margin-top: 20px;
    border-collapse: collapse;
    background-color: #1e1e2e;
    color: #eaeaea;
    border-radius: 8px;
    overflow: hidden;
    font-size: 14px;
    }

    .resource-table th,
    .resource-table td {
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid #333;
    }

    .resource-table th {
        background-color: #2b2e3d;
        font-weight: bold;
    }

    .resource-table tr:hover {
        background-color: #2e3344;
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

    .actions-cell {
        display: flex;
        gap: 20px;
        align-items: center;
    }

    .icon-button {
        cursor: pointer;
        width: 18px;
        height: 18px;
        color: #eaeaea;
        transition: color 0.2s;
    }

    .edit {
        margin-right: 10px;
    }

    .edit:hover {
        color: #3b82f6; /* red on hover for delete */
    }

    .delete:hover {
        color: #ff5555
    }
</style>
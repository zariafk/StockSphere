<template>
    <div class="deliveries-container">
      <h1>Deliveries <button class="add-btn" @click="openAddModal">+</button></h1>
  
      <button class="modal-button" @click="showPastModal = true">Past Deliveries</button>
  
      <table class="deliveries-table">
        <thead>
          <tr>
            <th>#</th>
            <th>From</th>
            <th>Total Cost</th>
            <th>Resources</th>
            <th>Cases</th>
            <th>Units</th>
            <th>Cost</th>
            <th>Notes</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(delivery, index) in deliveriesStore.deliveries" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ delivery.from }}</td>
            <td>{{ fmtGBP(calculateTotal(delivery.resources)) }}</td>
            <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ getResourceName(res.resourceId) }}</div></td>
            <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ res.cases }}</div></td>
            <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ getUnits(res.resourceId, res.cases) }}</div></td>
            <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ fmtGBP(getCost(res.resourceId, res.cases)) }}</div></td>
            <td>{{ delivery.notes }}</td>
            <td>
              <PencilLine class="icon-button edit" @click="startEdit(index)" />
              <Trash2 class="icon-button delete" @click="deleteDelivery(index)" />
              <input type="checkbox" @change="markCompleted(index)" />
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Add/Edit Modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h2>{{ editMode ? 'Edit Delivery' : 'Add New Delivery' }}</h2>
          <div class="grid-container">
            <div class="form-group">
              <label>Where From?</label>
              <input v-model="from" />
            </div>
  
            <div class="form-group">
              <label>Notes</label>
              <input v-model="notes" />
            </div>
  
            <div class="resource-group">
              <label>Resources</label>
              <div v-for="(res, idx) in resourceUsages" :key="idx" class="resource-row">
                <select v-model="res.resourceId">
                  <option disabled value="">-- Select Resource --</option>
                  <option v-for="r in resourceStore.resources" :key="r.id" :value="r.id">{{ r.name }}</option>
                </select>
                <input type="number" v-model.number="res.cases" placeholder="Packs" min="1" />
                <button class="remove-row" @click="removeResourceRow(idx)">✕</button>
              </div>
              <button class="add-row" @click="addResourceRow">Add Resource</button>
            </div>
          </div>
          <div class="modal-buttons">
            <button class="submit-button" @click="saveDelivery">{{ editMode ? "Save" : "Add" }}</button>
            <button class="close-button" @click="closeModal">Cancel</button>
          </div>
        </div>
      </div>
  
      <!-- Past Deliveries Modal -->
      <div v-if="showPastModal" class="modal-overlay">
        <div class="modal">
          <h2>Past Deliveries</h2>
          <table class="deliveries-table">
            <thead>
              <tr>
                <th>#</th>
                <th>From</th>
                <th>Total Cost</th>
                <th>Resources</th>
                <th>Packs</th>
                <th>Units</th>
                <th>Cost</th>
                <th>Notes</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(delivery, index) in deliveriesStore.pastDeliveries" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ delivery.from }}</td>
                <td>{{ fmtGBP(delivery.totalCost) }}</td>
                <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ getResourceName(res.resourceId) }}</div></td>
                <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ res.cases }}</div></td>
                <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ res.totalUnits }}</div></td>
                <td><div v-for="res in delivery.resources" :key="res.resourceId">{{ fmtGBP(res.cost) }}</div></td>
                <td>{{ delivery.notes }}</td>
                <td>
                  <Trash2 class="icon-button delete" @click="deletePast(delivery.id)" />
                </td>
              </tr>
            </tbody>
          </table>
          <div class="modal-buttons">
            <button class="close-button" @click="showPastModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useResourceStore } from '../store/resources'
  import { useDeliveriesStore } from '../store/deliveries'
  import { PencilLine, Trash2 } from 'lucide-vue-next'
  
  const resourceStore = useResourceStore()
  const deliveriesStore = useDeliveriesStore()
  
  onMounted(async () => {
    await resourceStore.fetchResources()
    await deliveriesStore.fetchDeliveries()
  })
  
  const showModal = ref(false)
  const showPastModal = ref(false)
  const editMode = ref(false)
  const editingIndex = ref(null)
  
  const from = ref('')
  const notes = ref('')
  const resourceUsages = ref([{ resourceId: '', cases: 1 }])
  
  const addResourceRow = () => resourceUsages.value.push({ resourceId: '', cases: 1 })
  const removeResourceRow = (i) => resourceUsages.value.splice(i, 1)
  
  const resetForm = () => {
    from.value = ''
    notes.value = ''
    resourceUsages.value = [{ resourceId: '', cases: 1 }]
    editMode.value = false
    editingIndex.value = null
  }
  
  const openAddModal = () => {
    resetForm()
    showModal.value = true
  }
  
  const closeModal = () => {
    showModal.value = false
    resetForm()
  }
  
  const getResourceName = (id) => {
    const res = resourceStore.resources.find(r => r.id === id)
    return res ? res.name : 'Unknown'
  }
  
  const getUnits = (id, cases) => {
    const res = resourceStore.resources.find(r => r.id === id)
    return res ? res.units_per_pack * cases : 0
  }
  
  const getCost = (id, cases) => {
    const res = resourceStore.resources.find(r => r.id === id)
    return res ? res.unit_price * res.units_per_pack * cases : 0
  }
  
  const calculateTotal = (items) => {
    return items.reduce((sum, r) => sum + getCost(r.resourceId, r.cases), 0)
  }
  
  const fmtGBP = (val) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP'
    }).format(val)
  }
  
  const saveDelivery = async () => {
    const payload = {
      from_location: from.value,
      notes: notes.value,
      resources: resourceUsages.value
        .filter(r => r.resourceId && r.cases)
        .map(r => ({
          resource: r.resourceId,
          cases: r.cases
        })),
      completed: false
    }
  
    if (editMode.value && editingIndex.value !== null) {
      deliveriesStore.updateDelivery(editingIndex.value, payload)
    } else {
      await deliveriesStore.addDelivery(payload)
      await deliveriesStore.fetchDeliveries()
    }
  
    closeModal()
  }
  
  const deleteDelivery = async (i) => {
    await deliveriesStore.deleteDelivery(i)
    await deliveriesStore.fetchDeliveries()
  }
  
  const deletePast = async (id) => {
    await deliveriesStore.deletePastDeliveryById(id)
  }
  
  const startEdit = (i) => {
    const d = deliveriesStore.deliveries[i]
    from.value = d.from_location
    notes.value = d.notes
    resourceUsages.value = JSON.parse(JSON.stringify(d.resources))
    editingIndex.value = i
    editMode.value = true
    showModal.value = true
  }
  
  const markCompleted = async (i) => {
    await deliveriesStore.markAsCompleted(i)
    await deliveriesStore.fetchDeliveries()
  }
  </script>    
    
  
  <style scoped>
  /* Use your familiar style structure like Planning.vue */
  .deliveries-container {
    color: #eaeaea;
    margin-top: 100px;
    margin-left: 70px;
    text-align: left;
  }
  .add-btn {
    margin-left: 10px;
    padding: 4px 10px;
    font-weight: bold;
    background: #b43de6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  .deliveries-table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
    background-color: #1e1e2e;
    color: #eaeaea;
    font-size: 14px;
  }
  .deliveries-table th,
  .deliveries-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #333;
  }
  .deliveries-table th {
    background-color: #2b2e3d;
  }
  .modal-button {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 8px 16px;
    background-color: #b43de6;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .modal {
    background: #171a23;
    padding: 20px;
    border-radius: 10px;
    width: 80%;
    text-align: left;
    color: white;
  }
  .grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  .form-group {
    display: flex;
    flex-direction: column;
  }
  .form-group input {
    width: 100%;
    box-sizing: border-box;
  }
  .modal-buttons {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }
  .submit-button, .close-button, .add-row {
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
  }
  .submit-button {
    background-color: #b43de6;
    color: white;
  }
  .close-button {
    background-color: #171a23;
    border: 2px solid #b43de6;
    color: white;
  }
  .resource-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.resource-row select,
.resource-row input {
  height: 38px;
  padding: 6px 10px;
  background-color: #2b2e3d;
  color: white;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 14px;
}

.resource-row select {
  flex: 2;
}

.resource-row input {
  flex: 1;
}

.remove-row {
  height: 38px;
  width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2b2e3d;
  border: none;
  color: #ff4d4d;
  font-size: 18px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.remove-row:hover {
  background: #3b3e4d;
}
  </style>
  
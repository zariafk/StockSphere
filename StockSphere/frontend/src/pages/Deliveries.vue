<template>
    <div class="deliveries-container">
      <h1>Deliveries <button class="add-btn" @click="openAddModal">+</button></h1>
  
      <!-- Past Deliveries Button -->
      <button class="modal-button" @click="showPastModal = true">Past Deliveries</button>
  
      <!-- Deliveries Table -->
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
          <tr v-for="(delivery, index) in deliveries.filter(d => !d.completed)" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ delivery.from }}</td>
            <td>{{ fmtGBP(calculateTotal(delivery.resources)) }}</td>
            <td>
              <div v-for="res in delivery.resources" :key="res.resourceId">{{ getResourceName(res.resourceId) }}</div>
            </td>
            <td>
              <div v-for="res in delivery.resources" :key="res.resourceId">{{ res.cases }}</div>
            </td>
            <td>
              <div v-for="res in delivery.resources" :key="res.resourceId">{{ getUnits(res.resourceId, res.cases) }}</div>
            </td>
            <td>
              <div v-for="res in delivery.resources" :key="res.resourceId">
                {{ fmtGBP(getCost(res.resourceId, res.cases)) }}
              </div>
            </td>
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
                  <option v-for="r in resourceStore.resources" :key="r.id" :value="r.id">
                    {{ r.name }}
                  </option>
                </select>
                <input type="number" v-model.number="res.cases" placeholder="Cases" min="1" />
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
          <ul>
            <li v-for="(d, i) in deliveries.filter(d => d.completed)" :key="i">
              ✅ {{ d.from }} — {{ fmtGBP(calculateTotal(d.resources)) }}
            </li>
          </ul>
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
  import { PencilLine, Trash2 } from 'lucide-vue-next'
  
  const resourceStore = useResourceStore()
  onMounted(() => resourceStore.fetchResources())
  
  const deliveries = ref([])
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
    return new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency: "GBP"
    }).format(val)
  }
  
  const saveDelivery = () => {
    const payload = {
      from: from.value,
      notes: notes.value,
      resources: resourceUsages.value.filter(r => r.resourceId && r.cases),
      completed: false
    }
  
    if (editMode.value) {
      deliveries.value[editingIndex.value] = payload
    } else {
      deliveries.value.push(payload)
    }
  
    closeModal()
  }
  
  const deleteDelivery = (i) => {
    deliveries.value.splice(i, 1)
  }
  
  const startEdit = (i) => {
    const d = deliveries.value[i]
    from.value = d.from
    notes.value = d.notes
    resourceUsages.value = JSON.parse(JSON.stringify(d.resources))
    editingIndex.value = i
    editMode.value = true
    showModal.value = true
  }
  
  const markCompleted = (i) => {
    deliveries.value[i].completed = true
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
    width: 600px;
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
  .remove-row {
    background: none;
    border: none;
    color: #ff5555;
    cursor: pointer;
    font-size: 16px;
  }
  </style>
  
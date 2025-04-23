<template>
    <div class="planning-container">
      <h1>Planning</h1>
      <p class="note">
        Note: Existing stock levels of products are not considered. This calculator estimates resources needed to produce new units.
      </p>
  
      <table class="plan-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Units to Make</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(plan, index) in productPlans" :key="index">
            <td>
              <select v-model="plan.productId">
                <option disabled value="">-- Select Product --</option>
                <option v-for="product in productStore.products" :key="product.id" :value="product.id">
                  {{ product.name }}
                </option>
              </select>
            </td>
            <td>
              <input type="number" min="1" v-model.number="plan.units" placeholder="0" />
            </td>
            <td>
              <button @click="removePlanRow(index)" class="remove-row">✕</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <div class="button-row">
        <button class="add-row" @click="addPlanRow">Add Product</button>
        <button class="calculate-button" @click="runCalculation">Calculate</button>
      </div>
  
      <!-- RESULTS MODAL -->
      <div v-if="showResults" class="modal-overlay">
        <div class="modal">
          <h2>Resource Requirements</h2>
  
          <table class="results-table">
            <thead>
              <tr>
                <th>Resource</th>
                <th>Total Units Needed</th>
                <th>Units per Pack</th>
                <th>Packs Needed</th>
                <th>Total Cost</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in calculatedResources" :key="res.id">
                <td>{{ res.name }}</td>
                <td>{{ res.totalUnits }}</td>
                <td>{{ res.unitsPerPack }}</td>
                <td>{{ res.packsNeeded }}</td>
                <td>{{ fmtGBP(res.totalCost) }}</td>
              </tr>
            </tbody>
          </table>
  
          <div class="total-section">
            <strong>Total Cost:</strong> {{ fmtGBP(totalCost) }}
          </div>
  
          <button class="close-button" @click="showResults = false">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  
  <script setup>
    import { ref, computed, onMounted } from 'vue'
    import { useProductStore } from '../store/products'
    import { useResourceStore } from '../store/resources'
    
    const productStore = useProductStore()
    const resourceStore = useResourceStore()

    const gbp = new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP',
        minimumFractionDigits: 2
    })
    const fmtGBP = (v) => (Number.isFinite(v) ? gbp.format(v) : '—')
    
    onMounted(() => {
      productStore.fetchProducts()
      resourceStore.fetchResources()
    })
    
    // User inputs
    const productPlans = ref([{ productId: '', units: 0 }])
    const showResults = ref(false)
    
    const addPlanRow = () => {
      productPlans.value.push({ productId: '', units: 0 })
    }
    const removePlanRow = (index) => {
      productPlans.value.splice(index, 1)
    }
    const resetPlans = () => {
      productPlans.value = [{ productId: '', units: 0 }]
      showResults.value = false
    }
    
    // Core calculation
    const calculatedResources = computed(() => {
      const resultMap = {}
    
      for (const plan of productPlans.value) {
        const product = productStore.products.find(p => p.id === plan.productId)
        if (!product) continue
    
        for (const usage of product.resource_usages) {
          const totalUnits = usage.units * plan.units
          const resource = resourceStore.resources.find(r => r.id === usage.resourceId)
          if (!resource) continue
    
          if (!resultMap[resource.id]) {
            resultMap[resource.id] = {
              name: resource.name,
              totalUnits: 0,
              unitsPerPack: resource.units_per_pack,
              unitPrice: parseFloat(resource.unit_price),
            }
          }
          resultMap[resource.id].totalUnits += totalUnits
        }
      }
    
      return Object.entries(resultMap).map(([id, res]) => {
        const packsNeeded = Math.ceil(res.totalUnits / res.unitsPerPack)
        const totalCost = packsNeeded * res.unitPrice * res.unitsPerPack
    
        return {
          id,
          name: res.name,
          totalUnits: res.totalUnits,
          unitsPerPack: res.unitsPerPack,
          unitPrice: res.unitPrice,
          packsNeeded,
          totalCost,
        }
      })
    })
    
    const totalCost = computed(() =>
      calculatedResources.value.reduce((sum, r) => sum + r.totalCost, 0)
    )
    
    const runCalculation = () => {
      showResults.value = true
    }
    </script>
    
  
  <style scoped>
.planning-container {
  color: #eaeaea;
  margin-top: 100px;
  margin-left: 70px;
  text-align: left;
}

.note {
  font-size: 14px;
  color: #bbbbbb;
  margin-bottom: 20px;
}

.plan-table, .results-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
  background-color: #1e1e2e;
  color: #eaeaea;
  border-radius: 8px;
  overflow: hidden;
  font-size: 14px;
}

.plan-table th, .plan-table td,
.results-table th, .results-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #333;
}

.plan-table th, .results-table th {
  background-color: #2b2e3d;
  font-weight: bold;
}

.plan-table tr:hover, .results-table tr:hover {
  background-color: #2e3344;
}

input[type="number"], select {
  width: 100%;
  padding: 6px 10px;
  background-color: #26293a;
  border: 1px solid #444;
  color: #eaeaea;
  border-radius: 4px;
  font-family: 'Exo', sans-serif;
}

.button-row {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.add-row, .calculate-button {
  padding: 8px 16px;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.add-row {
    background-color: #171a23;
    border-color: #b43de6;
    border-width: 3px;
}
.calculate-button {
  background-color: #b43de6;
}

.calculate-button:hover {
  background-color: #9031b8;
}

.add-row:hover {
  background-color: #12141c;
}

.remove-row {
  background: none;
  border: none;
  color: #ff5555;
  cursor: pointer;
  font-size: 16px;
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
  z-index: 10;
}

.modal {
  background: #171a23;
  padding: 20px;
  border-radius: 10px;
  width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  text-align: left;
}

.total-section {
  margin-top: 20px;
  font-size: 16px;
}

.close-button {
  margin-top: 20px;
  padding: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

  </style>
  
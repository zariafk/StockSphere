import { defineStore } from 'pinia'
import { useResourceStore } from './resources' // ✅ correct path

export const useDeliveriesStore = defineStore('deliveries', {
  state: () => ({
    deliveries: [],       // Current pending deliveries
    pastDeliveries: []    // Completed deliveries
  }),

  actions: {
    // Add a new delivery
    addDelivery(delivery) {
      // Auto-calculate costs for each resource in delivery
      delivery.resources = delivery.resources.map(res => {
        const totalUnits = res.cases * res.unitsPerPack
        const cost = totalUnits * res.unitPrice
        return {
          ...res,
          totalUnits,
          cost
        }
      })

      // Total delivery cost = sum of individual resource costs
      delivery.totalCost = delivery.resources.reduce((sum, r) => sum + r.cost, 0)

      // Push to the active deliveries list
      this.deliveries.push(delivery)
    },

    markAsCompleted(index) {
        const [completed] = this.deliveries.splice(index, 1)
      
        completed.resources = completed.resources.map(res => {
          // Find full resource info from your store (must be globally available)
          const resourceStore = useResourceStore()
          const resource = resourceStore.resources.find(r => r.id === res.resourceId)
      
          const unitsPerPack = resource?.units_per_pack ?? res.unitsPerPack ?? 1
          const unitPrice = resource?.unit_price ?? res.unitPrice ?? 0
          const totalUnits = res.cases * unitsPerPack
          const cost = totalUnits * unitPrice
      
          return {
            ...res,
            unitsPerPack,
            unitPrice,
            totalUnits,
            cost,
          }
        })
      
        completed.totalCost = completed.resources.reduce((sum, r) => sum + r.cost, 0)
      
        this.pastDeliveries.push(completed)
      },
      
      

    // Delete a delivery
    deleteDelivery(index) {
      this.deliveries.splice(index, 1)
    },

    // Optional: Update an existing delivery
    editDelivery(index, updatedDelivery) {
      this.deliveries[index] = updatedDelivery
    },

    // Reset all deliveries (for testing or clearing)
    resetDeliveries() {
      this.deliveries = []
      this.pastDeliveries = []
    },
    deletePastDelivery(index) {
        this.pastDeliveries.splice(index, 1)
      }      
  }
})

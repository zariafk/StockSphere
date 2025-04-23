import { defineStore } from 'pinia'

export const useDeliveryStore = defineStore('delivery', {
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

    // Mark a delivery as completed
    markAsCompleted(index) {
      const [completed] = this.deliveries.splice(index, 1)
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
    }
  }
})

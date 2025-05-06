import { defineStore } from 'pinia'
import { useResourceStore } from './resources'
import { getCSRFToken } from './auth'

export const useDeliveriesStore = defineStore('deliveries', {
  state: () => ({
    deliveries: [], // Array to hold ongoing deliveries
    pastDeliveries: [] // Array to hold completed deliveries
  }),

  actions: {
    // Fetch deliveries from API
    async fetchDeliveries() {
      try {
        const res = await fetch('http://localhost:8000/api/deliveries', {
          credentials: 'include' // Ensure cookies are included within request
        })
        const data = await res.json()

        const resourceStore = useResourceStore()

        // Filter and map ongoing deliverables
        this.deliveries = data
          .filter(d => !d.completed)
          .map(delivery => ({
            ...delivery,
            resources: delivery.resources.map(res => {
              const resourceInfo = resourceStore.resources.find(r => r.id === res.resource) || {}
              return {
                ...res,
                resourceId: res.resource,
                resourceName: resourceInfo.name || 'Unknown',
                unitsPerPack: resourceInfo.units_per_pack || 1,
                unitPrice: resourceInfo.unit_price || 0
              }
            })
          }))
        
        // Filter and map completed deliveries 
        this.pastDeliveries = data
          .filter(d => d.completed)
          .map(delivery => ({
            ...delivery,
            resources: delivery.resources.map(res => {
              const resourceInfo = resourceStore.resources.find(r => r.id === res.resource) || {}
              const unitsPerPack = resourceInfo.units_per_pack || 1;
              const unitPrice = resourceInfo.unit_price || 0;
              const totalUnits = unitsPerPack * (res.cases || 0);
              const cost = totalUnits * unitPrice;
              return {
                ...res,
                resourceId: res.resource,
                resourceName: resourceInfo.name || 'Unknown',
                unitsPerPack,
                unitPrice,
                totalUnits,
                cost
              }
            }),
            // Calculate the total cost of resources 
            totalCost: delivery.resources.reduce((sum, res) => {
              const resourceInfo = resourceStore.resources.find(r => r.id === res.resource) || {}
              const unitsPerPack = resourceInfo.units_per_pack || 1;
              const unitPrice = resourceInfo.unit_price || 0;
              return sum + (unitsPerPack * (res.cases || 0)) * unitPrice;
            }, 0)
          }))

      } catch (err) {
        console.error('Failed to fetch deliveries', err)
      }
    },

    // Add a new delivery and update resources accordingly
    async addDelivery(delivery) {
      try {
        const res = await fetch('http://localhost:8000/api/deliveries/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Add CSRF token to the request
          },
          credentials: 'include',
          body: JSON.stringify(delivery) // Send the delivery data as JSON
        })
        const newDelivery = await res.json()
        this.deliveries.push(newDelivery) // Ass delivery to deliveries list

        const resourceStore = useResourceStore()
        // Update arriving unitd for resources in the new delivery
        for (const resItem of newDelivery.resources) {
          const resource = resourceStore.resources.find(r => r.id === resItem.resource)
          if (resource) {
            const unitsToArrive = resource.units_per_pack * resItem.cases
            await resourceStore.updateResource(resource.id, {
              arriving_units: resource.arriving_units + unitsToArrive
            })
          }
        }

      } catch (err) {
        console.error('Failed to add delivery', err)
      }
    },      

    // Delete a specific delivery and adjust arriving units for the resources(s)
    async deleteDelivery(index) {
      const delivery = this.deliveries[index]
      if (!delivery) return

      try {
        const res = await fetch(`http://localhost:8000/api/deliveries/${delivery.id}/delete`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCSRFToken()
          },
          credentials: 'include'
        })

        if (res.ok) {
          const resourceStore = useResourceStore()
          for (const resItem of delivery.resources) {
            const resource = resourceStore.resources.find(r => r.id === resItem.resource)
            if (resource) {
              const unitsToRemove = resource.units_per_pack * resItem.cases
              await resourceStore.updateResource(resource.id, {
                arriving_units: resource.arriving_units - unitsToRemove
              })
            }
          }

          this.deliveries.splice(index, 1)
        }

      } catch (err) {
        console.error('Failed to delete delivery', err)
      }
    },

    // Delete a completed delivery by its ID
    async deletePastDeliveryById(id) {
      try {
        const res = await fetch(`http://localhost:8000/api/deliveries/${id}/delete`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCSRFToken()
          },
          credentials: 'include'
        })

        if (res.ok) {
          // Filter out the deleted delivery from the past deliveries
          this.pastDeliveries = this.pastDeliveries.filter(d => d.id !== id)
        }

      } catch (err) {
        console.error('Failed to delete past delivery', err)
      }
    },

    // Mark a delivery as completed amd update the corresponding resource(s)
    async markAsCompleted(index) {
      const delivery = this.deliveries[index]
      if (!delivery) return

      try {
        const res = await fetch(`http://localhost:8000/api/deliveries/${delivery.id}/update`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
          credentials: 'include',
          body: JSON.stringify({ ...delivery, completed: true })
        })
        const updatedDelivery = await res.json()

        const resourceStore = useResourceStore()
        for (const resItem of delivery.resources) {
          const resource = resourceStore.resources.find(r => r.id === resItem.resourceId)
          if (resource) {
            const units = resource.units_per_pack * resItem.cases
            await resourceStore.updateResource(resource.id, {
              available_units: resource.available_units + units,
              arriving_units: resource.arriving_units - units
            })
          }
        }

        // Move the delivery from ongoing to completed deliveries
        this.deliveries.splice(index, 1)

        this.pastDeliveries.push({
          ...updatedDelivery,
          resources: updatedDelivery.resources.map(res => {
            const resourceInfo = resourceStore.resources.find(r => r.id === res.resource) || {}
            const unitsPerPack = resourceInfo.units_per_pack || 1
            const unitPrice = resourceInfo.unit_price || 0
            const totalUnits = unitsPerPack * (res.cases || 0)
            const cost = totalUnits * unitPrice
            return {
              ...res,
              resourceId: res.resource,
              resourceName: resourceInfo.name || 'Unknown',
              unitsPerPack,
              unitPrice,
              totalUnits,
              cost
            }
          }),
          totalCost: updatedDelivery.resources.reduce((sum, res) => {
            const resourceInfo = resourceStore.resources.find(r => r.id === res.resource) || {}
            const unitsPerPack = resourceInfo.units_per_pack || 1
            const unitPrice = resourceInfo.unit_price || 0
            return sum + (unitsPerPack * (res.cases || 0)) * unitPrice
          }, 0)
        })

      } catch (err) {
        console.error('Failed to mark delivery as completed', err)
      }
    }
  }
})
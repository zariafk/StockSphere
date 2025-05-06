import { defineStore } from 'pinia'
import { useResourceStore } from './resources'
import { getCSRFToken } from './auth'

export const useDeliveriesStore = defineStore('deliveries', {
  state: () => ({
    deliveries: [],
    pastDeliveries: []
  }),

  actions: {
    async fetchDeliveries() {
      try {
        const res = await fetch('http://localhost:8000/api/deliveries', {
          credentials: 'include'
        })
        const data = await res.json()

        const resourceStore = useResourceStore()

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

    async addDelivery(delivery) {
      try {
        const res = await fetch('http://localhost:8000/api/deliveries/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
          credentials: 'include',
          body: JSON.stringify(delivery)
        })
        const newDelivery = await res.json()
        this.deliveries.push(newDelivery)

        const resourceStore = useResourceStore()
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

    updateDelivery(index, updatedDelivery) {
      const deliveryToUpdate = this.deliveries[index];
      if (deliveryToUpdate) {
          const resourceStore = useResourceStore();
          
          // Step 1: Handle resource updates (subtract the old arriving units and add the new ones)
          deliveryToUpdate.resources.forEach(originalResource => {
              const updatedResource = updatedDelivery.resources.find(r => r.resource === originalResource.resource);
              if (updatedResource) {
                  const oldUnits = originalResource.cases * originalResource.unitsPerPack;
                  const newUnits = updatedResource.cases * updatedResource.unitsPerPack;
  
                  // Ensure the resource quantities are correctly updated
                  resourceStore.updateResource(originalResource.resource, {
                      arriving_units: resourceStore.resources.find(r => r.id === originalResource.resource).arriving_units - oldUnits + newUnits
                  });
              }
          });
  
          // Step 2: Update the delivery data itself (including the new notes, from_location, etc.)
          this.deliveries[index] = { ...deliveryToUpdate, ...updatedDelivery };
      }
  },  
    
    updateResource(resourceId, updatedData) {
      const resource = useResourceStore().resources.find(r => r.id === resourceId);
      if (resource) {
        // Update the resource locally
        Object.assign(resource, updatedData);
    
        // Make the API call to persist the changes to the backend
        fetch(`http://localhost:8000/api/resources/${resourceId}/update`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: JSON.stringify(updatedData),
        })
          .then(response => response.json())
          .catch(error => console.error('Failed to update resource on the server:', error));
      }
    },       

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
          this.pastDeliveries = this.pastDeliveries.filter(d => d.id !== id)
        }

      } catch (err) {
        console.error('Failed to delete past delivery', err)
      }
    },

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

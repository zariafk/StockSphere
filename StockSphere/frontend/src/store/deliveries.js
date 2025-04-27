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
                return {
                  ...res,
                  resourceId: res.resource,
                  resourceName: resourceInfo.name || 'Unknown',
                  unitsPerPack: resourceInfo.units_per_pack || 1,
                  unitPrice: resourceInfo.unit_price || 0
                }
              })
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

        // Update resource arriving units
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

    async markAsCompleted(index) {
        const delivery = this.deliveries[index];
        if (!delivery) return;
      
        try {
          const cleanedDelivery = {
            from_location: delivery.from_location,
            notes: delivery.notes,
            completed: true,
            resources: delivery.resources.map(res => ({
              resource: res.resourceId,
              cases: res.cases
            }))
          };
      
          const res = await fetch(`http://localhost:8000/api/deliveries/${delivery.id}/update`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken()
            },
            credentials: 'include',
            body: JSON.stringify(cleanedDelivery)
          });
      
          if (!res.ok) {
            throw new Error('Failed to complete delivery');
          }
      
          const updatedDelivery = await res.json();
          const resourceStore = useResourceStore();
      
          // Update resource stocks
          for (const resItem of delivery.resources) {
            const resource = resourceStore.resources.find(r => r.id === resItem.resourceId);
            if (resource) {
              const units = resource.units_per_pack * resItem.cases;
              await resourceStore.updateResource(resource.id, {
                available_units: resource.available_units + units,
                arriving_units: resource.arriving_units - units
              });
            }
          }
      
          // 🧠 Manually calculate extra fields
          const mappedResources = delivery.resources.map(res => {
            const resourceInfo = resourceStore.resources.find(r => r.id === res.resourceId) || {};
            const unitsPerPack = resourceInfo.units_per_pack || 1;
            const unitPrice = resourceInfo.unit_price || 0;
            const totalUnits = unitsPerPack * res.cases;
            const cost = totalUnits * unitPrice;
            return {
              ...res,
              resourceName: resourceInfo.name || 'Unknown',
              unitsPerPack,
              unitPrice,
              totalUnits,
              cost
            };
          });
      
          const deliveryWithTotals = {
            id: updatedDelivery.id,
            from: updatedDelivery.from_location,
            notes: updatedDelivery.notes,
            completed: true,
            created_at: updatedDelivery.created_at,
            resources: mappedResources,
            totalCost: mappedResources.reduce((sum, r) => sum + r.cost, 0)
          };
      
          this.deliveries.splice(index, 1);
          this.pastDeliveries.push(deliveryWithTotals);
      
        } catch (err) {
          console.error('Failed to mark delivery as completed', err);
        }
      }
      
      
  }
})

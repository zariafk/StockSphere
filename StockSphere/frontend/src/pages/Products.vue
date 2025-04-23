<template>
    <div class="products-container">
      <h1>Products</h1>
  
      <!-- products table -->
      <table class="product-table">
        <thead>
          <tr>
            <th>Name</th> <!-- Updated column header order -->
            <th>Resources</th> <!-- Updated column header order -->
            <th>Cost</th>
            <th>Sales Price</th>
            <th>Profit</th>
            <th>Units</th>
            <th>Notes</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in productStore.products" :key="product.id">
            <td>{{ product.name }}</td>
            <td>
              <!-- Display resources used by the product -->
              <ul>
                <li v-for="(usage, index) in product.resource_usages" :key="index">
                  {{ getResourceName(usage.resourceId) }} <!-- Display resource name -->
                </li>
              </ul>
            </td>
            <td>{{ fmtGBP(product.cost) }}</td>
            <td>{{ fmtGBP(product.sales_price) }}</td>
            <td :class="{ positive: product.profit >= 0, negative: product.profit < 0 }">
              {{ fmtGBP(product.profit) }}
            </td>
            <td>{{ product.units_in_stock }}</td>
            <td>{{ product.notes }}</td>
            <td>
              <PencilLine size="16" class="icon-button edit" @click="startEdit(product)" title="Edit" />
              <Trash2 size="16" class="icon-button delete" @click="deleteProduct(product.id)" title="Delete" />
            </td>
          </tr>
        </tbody>
      </table>
  
      <button class="open-modal" @click="openAddProductModal">Add product</button>
  
      <!-- modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h2>{{ editMode ? "Edit Product" : "Add Product" }}</h2>
  
          <div class="grid-container">
            <!-- basic fields -->
            <div class="form-group">
              <label class="column-headings">Name</label>
              <input v-model="name" placeholder="Product Name" />
            </div>
  
            <div class="form-group">
              <label class="column-headings">Sales Price</label>
              <input v-model.number="sales_price" type="number" placeholder="e.g. 19.99" />
            </div>
  
            <div class="form-group">
              <label class="column-headings">Units in Stock</label>
              <input v-model.number="units_in_stock" type="number" placeholder="0" />
            </div>
  
            <div class="form-group">
              <label class="column-headings">Notes</label>
              <textarea v-model="notes" placeholder="Notes"></textarea>
            </div>
          </div>
  
          <!-- Resource usage section -->
          <h3 class="section-title">Resources Used</h3>
          <table class="resource-usage-table">
            <thead>
              <tr>
                <th>Resource</th>
                <th>Units Used</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(usage, index) in resourceUsages" :key="index">
                <td>
                  <select v-model="usage.resourceId">
                    <option disabled value="">-- Select Resource --</option>
                    <option v-for="res in resourceStore.resources" :key="res.id" :value="res.id">
                      {{ res.name }} ({{ fmtGBP(Number(res.unit_price) || 0) }})
                    </option>
                  </select>
                </td>
                <td>
                  <input v-model.number="usage.units" type="number" min="0" />
                </td>
                <td>
                  <button class="remove-row" @click="removeResourceRow(index)">✕</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button class="add-row" @click="addResourceRow">Add Resource</button>
  
          <div class="modal-buttons">
            <button class="submit-button" @click="saveProduct">
              {{ editMode ? "Save Changes" : "Add Product" }}
            </button>
            <button class="close-button" @click="closeModal">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
    import { ref, computed, onMounted } from "vue";
    import { PencilLine, Trash2 } from "lucide-vue-next";
    import { useResourceStore } from "../store/resources";
    import { useProductStore } from "../store/products";
    
    /* ---------- getCSRFToken helper ---------- */
    const getCSRFToken = () => {
      const cookies = document.cookie.split("; ");
      for (const cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") return value;
      }
      return null;
    };
    
    /* ---------- stores ---------- */
    const resourceStore = useResourceStore();
    const productStore = useProductStore();
    
    /* ---------- local state ---------- */
    const showModal = ref(false);
    const editMode = ref(false);
    const editingId = ref(null);
    
    // product fields
    const name = ref("");
    const sales_price = ref(null);
    const units_in_stock = ref(null);
    const notes = ref("");
    
    // resources used by product (array of { resourceId, units })
    const resourceUsages = ref([{ resourceId: "", units: null }]);
    
    /* ---------- formatters ---------- */
    const gbp = new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency: "GBP",
      minimumFractionDigits: 2,
    });
    
    const fmtGBP = (v) => (Number.isFinite(v) ? gbp.format(v) : "—");
    
    /* ---------- computed ---------- */
    const computedCost = computed(() =>
      resourceUsages.value.reduce((sum, usage) => {
        const res = resourceStore.resources.find((r) => r.id === usage.resourceId);
        if (!res || !usage.units) return sum;
        const unitPrice = Number(res.unit_price) || 0;
        return sum + unitPrice * usage.units;
      }, 0)
    );
    
    const computedProfit = computed(() => {
      if (!sales_price.value) return 0;
      return sales_price.value - computedCost.value;
    });
    
    /* ---------- lifecycle ---------- */
    onMounted(() => {
      resourceStore.fetchResources();
      productStore.fetchProducts();
    });
    
    /* ---------- helper functions ---------- */
    const addResourceRow = () => {
      resourceUsages.value.push({ resourceId: "", units: null });
    };
    
    const removeResourceRow = (index) => {
      resourceUsages.value.splice(index, 1);
    };
    
    const resetForm = () => {
      name.value = "";
      sales_price.value = null;
      units_in_stock.value = null;
      notes.value = "";
      resourceUsages.value = [{ resourceId: "", units: null }];
      editingId.value = null;
      editMode.value = false;
    };
    
    const openAddProductModal = () => {
      resetForm();
      showModal.value = true;
    };
    
    const closeModal = () => {
      showModal.value = false;
    };
    
    /* ---------- CRUD ---------- */
    const saveProduct = async () => {
      const payload = {
        name: name.value,
        resource_usages: resourceUsages.value.filter((u) => u.resourceId && u.units),
        cost: computedCost.value,
        sales_price: parseFloat(sales_price.value),
        profit: computedProfit.value,
        units_in_stock: parseInt(units_in_stock.value),
        notes: notes.value,
      };
    
      try {
        let response;
    
        if (editMode.value && editingId.value !== null) {
          response = await fetch(`http://localhost:8000/api/products/${editingId.value}/update`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });
        } else {
          response = await fetch("http://localhost:8000/api/products/add", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });
        }
    
        if (!response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            console.error("Product save failed:", errorData);
            alert("Error: " + JSON.stringify(errorData));
          } else {
            const errorText = await response.text();
            console.error("Non-JSON error:", errorText);
            alert("Server returned an error:\n" + errorText.slice(0, 200));
          }
          return;
        }
    
        await productStore.fetchProducts();
        closeModal();
        resetForm();
      } catch (err) {
        console.error("Unexpected error saving product:", err);
        alert("Unexpected error occurred: " + err.message);
      }
    };
    
    const startEdit = (product) => {
      name.value = product.name;
      sales_price.value = product.sales_price;
      units_in_stock.value = product.units_in_stock;
      notes.value = product.notes;
      resourceUsages.value = product.resource_usages.map((u) => ({ ...u }));
      editingId.value = product.id;
      editMode.value = true;
      showModal.value = true;
    };
    
    const deleteProduct = async (id) => {
      await productStore.deleteProduct(id);
    };
    
    /* ---------- Helper function to get resource name by ID ---------- */
    const getResourceName = (resourceId) => {
      const resource = resourceStore.resources.find((r) => r.id === resourceId);
      return resource ? resource.name : "Unknown Resource";
    };
    </script>
    
    
  
  <style scoped>
  .products-container {
    color: #eaeaea;
    margin-top: 100px;
    margin-left: 70px;
    text-align: left;
  }
  
  .product-table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
    background-color: #1e1e2e;
    color: #eaeaea;
    border-radius: 8px;
    overflow: hidden;
    font-size: 14px;
  }
  
  .product-table th,
  .product-table td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #333;
  }
  
  .product-table th {
    background-color: #2b2e3d;
    font-weight: bold;
  }
  
  .product-table tr:hover {
    background-color: #2e3344;
  }
  
  .icon-button {
    cursor: pointer;
    width: 18px;
    height: 18px;
    color: #eaeaea;
    transition: color 0.2s;
  }
  
  .edit:hover { color: #3b82f6; }
  .delete:hover { color: #ff5555; }
  
  .positive { color: #28a745; }
  .negative { color: #dc3545; }
  
  .open-modal {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #B43DE6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .open-modal:hover {
    background-color: #9031b8;
  }
  
  /* modal */
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
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    text-align: left;
  }
  
  .grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 10px;
  }
  
  /* Each label/input pair */
  .form-group {
    display: flex;
    flex-direction: column; /* Align label above input */
    margin-bottom: 20px; /* Space between fields */
  }
  
  .column-headings {
    font-weight: bold;
    margin-bottom: 5px; /* Space between label and input */
  }
  
  .resource-usage-table {
    width: 100%;
    margin-top: 10px;
    border-collapse: collapse;
    background-color: #1e1e2e;
    color: #eaeaea;
    border-radius: 6px;
    overflow: hidden;
    font-size: 13px;
  }
  
  .resource-usage-table th,
  .resource-usage-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #333;
  }
  
  .resource-usage-table th {
    background-color: #2b2e3d;
  }
  
  .add-row {
    margin-top: 10px;
    padding: 6px 12px;
    background-color: #4caf50;
    border: none;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .remove-row {
    background: none;
    border: none;
    color: #ff5555;
    cursor: pointer;
    font-size: 16px;
  }
  
  .modal-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .submit-button {
    padding: 10px;
    background-color: #3b82f6;
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
  
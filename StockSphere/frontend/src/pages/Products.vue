<template>
  <div class="products-container">
    <h1>Products</h1>

    <!-- products table -->
    <table class="product-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Resources</th>
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
            <ul>
              <li v-for="(usage, index) in product.resource_usages" :key="index">
                {{ getResourceName(usage.resourceId) }} ({{ usage.units }} units)
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
            <Info size="16" class="icon-button info" @click="viewProductDetails(product)" title="View Details" />
          </td>
        </tr>
      </tbody>
    </table>

    <button class="open-modal" @click="openAddProductModal">Add product</button>

<!-- Add/Edit Modal -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h2>{{ editMode ? "Edit Product" : "Add Product" }}</h2>

      <div class="grid-container">
        <div class="form-group">
          <label class="column-headings">Name</label>
          <input v-model="name" placeholder="Product Name" />
        </div>

        <div class="form-group">
          <label class="column-headings">Sales Price</label>
          <input v-model.number="sales_price" type="number" placeholder="Sales Price" />
        </div>

        <div class="form-group">
          <label class="column-headings">Units in Stock</label>
          <input v-model.number="units_in_stock" type="number" placeholder="Units Available" />
        </div>

        <div class="form-group">
          <label class="column-headings">Notes</label>
          <textarea v-model="notes" placeholder="Notes"></textarea>
        </div>

        <div class="form-group">
          <label class="column-headings">Resource Usage</label>
          <div v-for="(usage, index) in resourceUsages" :key="index" class="resource-usage-row">
            <select v-model="usage.resourceId">
              <option disabled value="">Select Resource</option>
              <option v-for="resource in resourceStore.resources" :value="resource.id">
                {{ resource.name }}
              </option>
            </select>
            <input v-model.number="usage.units" type="number" placeholder="Units" />
            <button @click="removeResourceRow(index)">Remove</button>
          </div>
          <button class="add-row" @click="addResourceRow">Add Resource</button>
        </div>

        <div class="form-group">
          <label class="column-headings">Sales Forecast</label>
          <div class="forecast-buttons">
            <button class="add-row" @click="openSalesForecastModal()">Add Sales Platform Data</button>
          </div>
        
          <div v-if="salesForecastSummary.length > 0" class="sales-forecast-summary">
            <ul>
              <li v-for="(item, index) in salesForecastSummary" :key="index" class="forecast-summary-item">
                <strong>{{ item.platform }}</strong>: {{ item.totalUnits }} units
                <Edit size="16" class="edit-icon" @click="openSalesForecastModal(index)" title="Edit Platform" />
                <X size="16" class="remove-icon" @click="removePlatform(index)" title="Remove Platform" />

              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="modal-buttons">
        <button class="submit-button" @click="saveProduct">
          {{ editMode ? "Save Changes" : "Add Product" }}
        </button>
        <button class="close-button" @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>


    <!-- Sales Forecast Modal -->
    <div v-if="showSalesForecastModal" class="modal-overlay">
      <div class="modal">
        <h2>Add/Edit Sales Forecast Data</h2>
    
        <input type="text" v-model="tempPlatform.platformName" placeholder="Platform Name" />
    
        <div v-for="(period, i) in tempPlatform.periods" :key="i" class="period-block">
          <input type="date" v-model="period.startDate" />
          <input type="date" v-model="period.endDate" />
          <input type="number" v-model.number="period.unitsSold" placeholder="Units Sold" />
          <button @click="tempPlatform.periods.splice(i, 1)">Remove Period</button>
        </div>
    
        <button class="add-row" @click="tempPlatform.periods.push({ startDate: '', endDate: '', unitsSold: null })">
          Add Time Period
        </button>
    
        <div class="modal-buttons">
          <button class="submit-button" @click="saveSalesForecast">Save</button>
          <button class="close-button" @click="closeSalesForecastModal">Cancel</button>
        </div>
      </div>
    </div>
    


    <!-- Product Details Modal -->
    <div v-if="showProductDetailsModal" class="modal-overlay">
      <div class="modal">
        <h2>Product Details: {{ selectedProduct?.name }}</h2>

        <div class="form-group">
          <p><strong>Sales Price:</strong> {{ fmtGBP(selectedProduct?.sales_price) }}</p>
          <p><strong>Cost:</strong> {{ fmtGBP(selectedProduct?.cost) }}</p>
          <p><strong>Profit:</strong> {{ fmtGBP(selectedProduct?.profit) }}</p>
          <p><strong>Units in Stock:</strong> {{ selectedProduct?.units_in_stock }}</p>
          <p><strong>Notes:</strong> {{ selectedProduct?.notes }}</p>
        </div>

        <div class="form-group">
          <label class="column-headings">Sales Forecast Chart</label>
          <div class="chart-container">
            <canvas id="salesForecastChart"></canvas>
          </div>
        </div>

        <div class="form-group">
          <label class="column-headings">Sales Platform Split</label>
          <div class="chart-container">
            <canvas id="salesPlatformChart"></canvas>
          </div>
        </div>

        <div class="modal-buttons">
          <button class="close-button" @click="closeProductDetails">Close</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
  import { ref, computed, onMounted, nextTick } from 'vue';
  import { PencilLine, Trash2, Info, Edit, X } from "lucide-vue-next";
  import { useResourceStore } from "../store/resources";
  import { useProductStore } from "../store/products";
  import { useNotificationStore } from '../store/notifications';
  import Chart from "chart.js/auto";
  import { useAuthStore } from '../store/auth';  
  
  const resourceStore = useResourceStore();
  const productStore = useProductStore();
  const authStore = useAuthStore();

  
  const showModal = ref(false);
  const salesPlatformsEditIndex = ref(null);
  const tempPlatform = ref({ platformName: "", periods: [] });
  const showSalesForecastModal = ref(false);
  const showProductDetailsModal = ref(false);
  const selectedProduct = ref(null);
  const editMode = ref(false);
  const editingId = ref(null);
  
  const name = ref("");
  const sales_price = ref(null);
  const units_in_stock = ref(null);
  const notes = ref("");
  const resourceUsages = ref([{ resourceId: "", units: null }]);
  const salesPlatforms = ref([]);
  
  const salesForecastChartInstance = ref(null);
  const salesPlatformChartInstance = ref(null);

  const notificationStore = useNotificationStore();
  
  onMounted(async() => {
    console.log('User authenticated:', authStore.isAuthenticated);

    await resourceStore.fetchResources();
    await productStore.fetchProducts();
    console.log(productStore.products);
    if (productStore.products.length > 0) {
    console.log('Calling checkStock...');  // This log should appear
    checkStock();
  } else {
    console.log('No products to check stock for.');
  }
  });
  
  const openAddProductModal = () => {
    resetForm();
    showModal.value = true;
  };
  
  const closeModal = () => {
    showModal.value = false;
  };
  
  const resetForm = () => {
    name.value = "";
    sales_price.value = null;
    units_in_stock.value = null;
    notes.value = "";
    resourceUsages.value = [{ resourceId: "", units: null }];
    salesPlatforms.value = [];
    editingId.value = null;
    editMode.value = false;
  };

  const checkStock = () => {
    console.log('Authenticated User:', authStore.user);

  productStore.products.forEach(async (product) => {
    console.log('Product object:', product);

    if (product.units_in_stock <= 25) {
      // Push the notification locally
      notificationStore.notifications.push({
        message: `Product "${product.name}" has 25 or fewer units left.`,
        type: 'alert',
        is_read: false,
      });
      const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
      console.log('Payload being sent:', {
  userId: authStore.user?.username,
  message: `Product "${product.name}" has 25 or fewer units left.`,
  is_read: false,
});
const userId = authStore.user?.id;
console.log('Authenticated User ID:', userId);
      // Send a request to the backend to save the notification
      try {
        const response = await fetch('http://localhost:8000/api/dashboard', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include',
          body: JSON.stringify({
            userId: authStore.user?.username,
            message: `Product "${product.name}" has 25 or fewer units left.`,
            is_read: false,
          }),
        });

        if (response.ok) {
          console.log('Notification saved to the backend');
        } else {
          console.error('Failed to save notification to backend');
        }
      } catch (error) {
        console.error('Error saving notification:', error);
      }
    }
  });
};


  const salesForecastSummary = computed(() =>
  salesPlatforms.value.map(p => ({
    platform: p.platformName,
    totalUnits: p.periods.reduce((acc, period) => acc + (period.unitsSold || 0), 0)
  }))
);

  
  const addResourceRow = () => {
    resourceUsages.value.push({ resourceId: "", units: null });
  };
  
  const removeResourceRow = (index) => {
    resourceUsages.value.splice(index, 1);
  };

  function formatToInputDate(value) {
  if (!value) return "";
  const d = new Date(value);
  if (isNaN(d.getTime())) return "";
  return d.toISOString().slice(0, 10); // YYYY-MM-DD
}

const openSalesForecastModal = (platformIndex = null) => {
  if (platformIndex === null) {
    // Add new platform
    tempPlatform.value = {
      platformName: "",
      periods: [{ startDate: "", endDate: "", unitsSold: null }]
    };
    salesPlatformsEditIndex.value = null;
  } else {
    const existingPlatform = salesPlatforms.value[platformIndex];
    tempPlatform.value = {
      platformName: existingPlatform.platformName,
      periods: existingPlatform.periods.map(p => ({
        startDate: formatToInputDate(p.startDate),
        endDate: formatToInputDate(p.endDate),
        unitsSold: p.unitsSold || 0
      }))
    };
    salesPlatformsEditIndex.value = platformIndex;
  }

  showSalesForecastModal.value = true;
};

  
  const closeSalesForecastModal = () => {
    showSalesForecastModal.value = false;
  };
  
  const addPeriod = (platformIndex) => {
    salesPlatforms.value[platformIndex].periods.push({ startDate: "", endDate: "", unitsSold: null });
  };
  
  const removePeriod = (platformIndex, periodIndex) => {
    salesPlatforms.value[platformIndex].periods.splice(periodIndex, 1);
  };
  
  const saveSalesForecast = () => {
  const platformData = {
    platformName: tempPlatform.value.platformName,
    periods: tempPlatform.value.periods
  };

  if (salesPlatformsEditIndex.value !== null) {
    salesPlatforms.value[salesPlatformsEditIndex.value] = platformData;
  } else {
    salesPlatforms.value.push(platformData);
  }

  salesPlatformsEditIndex.value = null;
  showSalesForecastModal.value = false;
};



const removePlatform = (index) => {
  salesPlatforms.value.splice(index, 1);
};


  
  const saveProduct = async () => {
    const forecastData = salesPlatforms.value.map(platform => ({
  platform: platform.platformName,
  periods: platform.periods.map(p => ({
    startDate: p.startDate,
    endDate: p.endDate,
    unitsSold: p.unitsSold
    })) || []
}));

  
    const payload = {
      name: name.value,
      resource_usages: resourceUsages.value.filter((u) => u.resourceId && u.units),
      cost: computedCost.value,
      sales_price: parseFloat(sales_price.value),
      profit: computedProfit.value,
      units_in_stock: parseInt(units_in_stock.value),
      sales_forecast: forecastData,
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
    salesPlatforms.value = product.sales_forecast?.map(p => ({
      platformName: p.platform,
      periods: p.periods.map(per => ({
        startDate: per.startDate || "",
        endDate: per.endDate || "",
        unitsSold: per.unitsSold || 0
    }))
  })) || [];
    editingId.value = product.id;
    editMode.value = true;
    showModal.value = true;
  };
  
  const deleteProduct = async (id) => {
    await productStore.deleteProduct(id);
  };
  
  const viewProductDetails = async (product) => {
    selectedProduct.value = product;
    showProductDetailsModal.value = true;
    await nextTick();
    renderCharts();
  };
  
  const closeProductDetails = () => {
    showProductDetailsModal.value = false;
    if (salesForecastChartInstance.value) salesForecastChartInstance.value.destroy();
    if (salesPlatformChartInstance.value) salesPlatformChartInstance.value.destroy();
  };
  
  const renderCharts = () => {
  if (salesForecastChartInstance.value) salesForecastChartInstance.value.destroy();
  if (salesPlatformChartInstance.value) salesPlatformChartInstance.value.destroy();

  const ctx1 = document.getElementById("salesForecastChart")?.getContext("2d");
  const ctx2 = document.getElementById("salesPlatformChart")?.getContext("2d");

  if (!selectedProduct.value) return;

  // Step 1: Extract and sort sales data
  const salesData = [];
  (selectedProduct.value.sales_forecast || []).forEach((platform) => {
    platform.periods.forEach((period) => {
      if (period.unitsSold && period.endDate) {
        salesData.push({
          date: new Date(period.endDate),
          units: period.unitsSold,
        });
      }
    });
  });

  salesData.sort((a, b) => new Date(a.date) - new Date(b.date));

  // Step 2: Filter last 12 months
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
  const filteredSalesData = salesData.filter(d => d.date >= oneYearAgo);

  const realSalesUnits = filteredSalesData.map(d => d.units);
  const realSalesDates = filteredSalesData.map(d => d.date);

  // Step 3: Calculate forecast
  const forecastUnits = [];
  const forecastDates = [];

  const monthlyChanges = [];
  for (let i = 1; i < realSalesUnits.length; i++) {
    monthlyChanges.push(realSalesUnits[i] - realSalesUnits[i - 1]);
  }
  const avgChange = monthlyChanges.reduce((a, b) => a + b, 0) / monthlyChanges.length || 0;

  const lastRealValue = realSalesUnits[realSalesUnits.length - 1] || 0;
  const lastRealDate = realSalesDates[realSalesDates.length - 1] || new Date();

  for (let i = 1; i <= 5; i++) {
    const futureDate = new Date(lastRealDate);
    futureDate.setDate(1)
    futureDate.setMonth(futureDate.getMonth() + i);
    forecastDates.push(futureDate);

    const growth = avgChange * Math.pow(1.1, i - 1); // compound growth
    const previousValue = i === 1 ? lastRealValue : forecastUnits[i - 2];
    forecastUnits.push(Math.round(previousValue + growth));
  }

  // Step 4: Adjust forecast start to avoid duplicated months
  const firstForecastMonth = forecastDates[0]?.getMonth();
  const lastRealMonth = lastRealDate.getMonth();
  const firstForecastYear = forecastDates[0]?.getFullYear();
  const lastRealYear = lastRealDate.getFullYear();

  const trimmedForecastDates = (firstForecastMonth === lastRealMonth && firstForecastYear === lastRealYear)
    ? forecastDates.slice(1)
    : forecastDates;

  const trimmedForecastUnits = (firstForecastMonth === lastRealMonth && firstForecastYear === lastRealYear)
    ? forecastUnits.slice(1)
    : forecastUnits;

    const allDates = [...realSalesDates, ...trimmedForecastDates];

const seenMonths = new Set();
const uniqueDates = [];
allDates.forEach(date => {
  const key = `${date.getFullYear()}-${date.getMonth()}`;
  if (!seenMonths.has(key)) {
    seenMonths.add(key);
    uniqueDates.push(date);
  }
});

const formattedLabels = uniqueDates.map(d =>
  d.toLocaleDateString("en-GB", { month: "short", year: "numeric" })
);



  const paddedForecast = [
    ...Array(realSalesUnits.length - 1).fill(null),
    lastRealValue,
    ...trimmedForecastUnits
  ];

  // Step 5: Draw chart
  if (ctx1) {
    salesForecastChartInstance.value = new Chart(ctx1, {
      type: "line",
      data: {
        labels: formattedLabels,
        datasets: [
          {
            label: "Real Sales",
            data: [...realSalesUnits, ...Array(trimmedForecastUnits.length + 1).fill(null)],
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
            fill: false,
            tension: 0.4,
          },
          {
            label: "Projected Sales",
            data: paddedForecast,
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 2,
            fill: false,
            tension: 0.4,
            borderDash: [5, 5],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }

  // Optional: Pie chart
  if (ctx2) {
    const platformSales = selectedProduct.value.sales_forecast?.map(p => ({
      platform: p.platform,
      totalSales: p.periods.reduce((sum, period) => sum + period.unitsSold, 0),
    })) || [];

    if (platformSales.length > 0) {
      salesPlatformChartInstance.value = new Chart(ctx2, {
        type: "pie",
        data: {
          labels: platformSales.map((p) => p.platform),
          datasets: [{
            data: platformSales.map((p) => p.totalSales),
            backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
          }],
        },
      });
    }
  }
};

  
  const fmtGBP = (v) => (Number.isFinite(v) ? gbp.format(v) : "—");
  const gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", minimumFractionDigits: 2 });
  const getResourceName = (resourceId) => {
    const resource = resourceStore.resources.find((r) => r.id === resourceId);
    return resource ? resource.name : "Unknown Resource";
  };
  
  function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken'))?.split('=')[1];
  }
  
  const computedCost = computed(() => {
    return resourceUsages.value.reduce((acc, usage) => {
      const resource = resourceStore.resources.find((r) => r.id === usage.resourceId);
      return acc + (resource?.unit_price || 0) * (usage.units || 0);
    }, 0);
  });
  
  const computedProfit = computed(() => {
    if (!sales_price.value || !computedCost.value) return 0;
    return sales_price.value - computedCost.value;
  });
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
    
    ul {
      list-style-type: none;
      padding-left: 0;
      margin: 0;
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
    .info:hover { color: #b43de6; }
    
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
    
    /* Modal Styling */
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
    
    .form-group {
      display: flex;
      flex-direction: column;
      margin-bottom: 20px;
    }
    
    .column-headings {
      font-weight: bold;
      margin-bottom: 5px;
    }
    
    .resource-usage-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }
    
    .resource-usage-row select,
    .resource-usage-row input[type="number"] {
      flex: 1;
      padding: 5px;
    }
    
    .resource-usage-row button {
      background-color: transparent;
      color: #ff5555;
      border: none;
      cursor: pointer;
      font-size: 16px;
    }
    
    /* New: Chart containers */
    .chart-container {
      width: 100%;
      height: 350px;
      position: relative;
      margin-top: 10px;
    }
    
    /* Forecast Platform/Periods Styling */
    .platform-block {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }
    
    .platform-block input[type="text"] {
      padding: 6px;
      font-size: 14px;
      background-color: #262836;
      border: 1px solid #444;
      color: #fff;
      border-radius: 4px;
    }
    
    .period-block {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }
    
    .period-block input[type="date"],
    .period-block input[type="number"] {
      flex: 1;
      padding: 5px;
      background-color: #262836;
      border: 1px solid #444;
      color: #fff;
      border-radius: 4px;
    }
    
    .period-block button {
      background-color: transparent;
      color: #ff5555;
      border: none;
      cursor: pointer;
      font-size: 16px;
    }
    
    .period-block::after {
      content: "(inclusive)";
      font-size: 12px;
      color: #aaa;
      margin-left: 5px;
    }
    
    .modal-buttons {
      display: flex;
      justify-content: space-between;
      margin-top: 20px;
    }
    
    .submit-button,
    .add-row {
      padding: 10px;
      background-color: #b43de6;
      color: white;
      border: none;
      cursor: pointer;
      border-radius: 5px;
      flex: 1;
      margin-right: 10px;
    }
    
    .submit-button:hover,
    .add-row:hover {
      background-color: #9031b8;
    }
    
    .close-button {
      padding: 10px;
      background-color: #171A23;
      color: white;
      border: 2px solid #b43de6;
      cursor: pointer;
      border-radius: 5px;
      flex: 1;
    }

    .forecast-summary-item {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-icon,
.remove-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #ccc;
}

.edit-icon:hover { color: #4bc0c0; }
.remove-icon:hover { color: #ff5555; }

    </style>
    
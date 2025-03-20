<template>
    <div class="landing-page">
      <h1>Getting Started</h1>

      <p class="text1">
        Take your business to the next level by signing up to StockSphere today!
      </p>
      <p class="text2">
        From inventory management to sales forecasting and communications, StockSphere is the 
        perfect place for small businesses to grow via simple data input-no advanced data 
        handling experience necessary!
      </p>

      <button class="register-button" @click="goToRegister">Sign Up</button>
      <button class="login-button" @click="goToLogin">Login</button>

      <div class="features-container">
        <div class="feature-item">
            <h3>Inventory Management</h3>
            <img class="feature-icon" src="./icons/inventory_management.png" alt="Inventory Management Icon" />
            <p>Keep track of stock, products and deliveries.</p>
        </div>
        <div class="feature-item">
            <h3>Sales Forecasting</h3>
            <img class="feature-icon" src="./icons/sales_forecasting.png" alt="Sales Forecasting Icon" />
            <p>Input sales data to see predictions about future sales.</p>
        </div>
        <div class="feature-item">
            <h3>Communications</h3>
            <img class="feature-icon" src="./icons/communications.png" alt="Communications Icon" />
            <p>Communicate both internally and externally.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      goToRegister() {
        this.$router.push('/register')
      },
      
      goToLogin() {
        this.$router.push('/login')
      },
    }
  }
  </script>

  <style scoped>
    .landing-page {
        text-align: left;
        color: #eaeaea;
        margin: 100px 70px;

    }

    .register-button {
        background-color: #b54de6;
        color: #eaeaea;
        padding: 0.75rem 1.5rem;
        border: 3px solid #b54de6;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }

    .login-button {
        background-color: #171a23;
        color: #eaeaea;
        padding: 0.75rem 1.5rem;
        border: 3px solid #b54de6;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }

    button + button {
        margin-top: 20px;
        margin-left: 16px;
        margin-bottom: 35px;
    }

    .features-container {
        display: flex;
        justify-content: space-between;
        margin-top: 40px;
        text-align: center;
        gap: 20px;
    }

    .feature-item {
        flex: 1;
    }

    .feature-item h3 {
        font-size: 1.2rem;
        margin-bottom: 8px;
    }

    .feature-item p {
        font-size: 1rem;
        line-height: 1.4;
        color: #dadada;
    }

    /* placeholder icons */
    .feature-icon {
        width: 80px;
        height: 80px;
        margin: 0 auto 15px auto;
    }

    .feature-icon {
  width: 100px !important;
  height: auto !important;
  display: block !important;
  background-color: red !important;
}
</style>
<template>
    <div class="app-bar">
      <h1 class="logo-text">StockSphere</h1>
    </div>
  </template>
  
  <script>
  export default {
    name: "AppBar",
  };
  </script>
  
  <style scoped>
  .app-bar {
    background-color: #b54de6; /* Use your color code here */
    padding: 25px 25px;
    text-align: left;
    width: 100vw;
  }
  
  .logo-text {
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    margin: 0;
  }
  </style>
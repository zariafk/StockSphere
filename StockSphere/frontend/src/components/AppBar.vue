<template>
    <nav class="app-bar">
      <h1 class="logo-text">StockSphere</h1>
      <div v-if="!$route.meta.hideTabs" class="tabs">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/resources">Resources</router-link>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "AppBar",
  };
</script>
  
<style scoped>
    .app-bar {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #b54de6;
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 90vw;
        height: 70px;
        border-radius: 15px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease-in-out;
    }
  
    .logo-text {
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
        margin: 0;
    }

    .tabs a {
        margin: 0 20px;
        text-decoration: none;
        color: white;
        padding: 5px 10px;
        border-bottom: 2px solid transparent;
    }

    .tabs a.router-link-active {
        background-color: rgba(255, 255, 255, 0.2); /* Slight white tint */
        box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5); /* Subtle glow */
    }

    .tabs a:hover {
        background-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0px 0px 12px rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease-in-out;
    }
  </style>
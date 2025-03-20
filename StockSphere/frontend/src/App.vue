<template>
  <div id="app">
    <AppBar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
  import AppBar from './components/AppBar.vue'
  
  export default {
    components: {
      AppBar,
    },
  }
</script>

<style>
  html, body, #app {
    margin: 0;
    padding: 0;
    height: 100%;
    background-color: #171A23;
  }

  #app {
    display: flex;
    flex-direction: column;
  }

  .main-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
  }
  
  * {
  box-sizing: border-box;
  }

  body {
    font-family: 'Exo', sans-serif !important;
    font-size: 16px;
  }

  h1, h2, h3, h4 {
    margin-top: 0;
  }

  h1, h2, h3, h4, p {
    font-family: 'Exo', sans-serif;
  }

  .content-wrapper {
    margin-top: 120px; /* Adjust this value to match App Bar height */
    padding: 20px; /* Optional: Adds spacing inside */
  }

  /* Hide scrollbar for Chrome, Safari, and Edge */
  ::-webkit-scrollbar {
    width: 0px; /* Removes the visible scrollbar */
    height: 0px;
    display: none;
  }

  /* Hide scrollbar for Firefox */
  html {
    scrollbar-width: none;
  }

  /* Hide scrollbar for IE and Edge */
  body {
    -ms-overflow-style: none;
  }
</style>
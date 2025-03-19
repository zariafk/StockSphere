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
    background-color: #fff;
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
    font-family: 'Arial', sans-serif;
    font-size: 16px;
  }

  h1, h2, h3, h4 {
    margin-top: 0;
  }
</style>
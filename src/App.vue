<template>
  <!-- The main container for the application -->
  <div id="app">
    <!-- Dynamically renders components based on the current route -->
    <router-view />
  </div>
</template>

<script>
export default {
  // Component name for internal reference and debugging
  name: "App",
};
</script>

<style>
/* global styles for App.vue here */
#app {
  width: 100%;
}

:root {
  --fc-border-color: black;
  --fc-daygrid-event-dot-width: 5px;
  --fc-toolbar-title-font-size: 0.1rem; 
}

body {
  font-family: "DM Sans", sans-serif;
  /* background-color: #DCC7BE; */
  /* background-color: #F0F2EF; */
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>

<!-- Header component -->

<template>
  <header class="header">
    <h1>{{ title }}</h1>

    <nav class="btn-container">
      <!-- Slot for flight schedule Button -->
      <slot name="flightschedule" class="btn"></slot>

      <!-- Slot for Enquiry Button -->
      <slot name="enquiry" class="btn"></slot>

      <!-- Slot for Login Button -->
      <slot name="login" class="btn"></slot>
    </nav>
  </header>
</template>

<script>
export default {

  //prop 'title' of type String with a default value
  props: {
    title: {
      type: String,
      default: "Drone Video Streaming" // Default title if not provided
    }
  },
}
</script>

<style scoped src="./header-styles.css"></style>
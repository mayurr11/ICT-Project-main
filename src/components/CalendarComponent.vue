<!-- Calendar component  -->

<template>
  <div class="calendar-container">
    <!-- FullCalendar component -->
    <div id="calendar"></div>
  </div>
</template>

<script>

// Importing FullCalendar and dayGridPlugin
import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';

export default {
  mounted() {
    // Call the method to initialize the calendar when the component is mounted 
    this.initCalendar();
  },
  methods: {
    initCalendar() {
      // Initialize FullCalendar library here
      const calendarEl = document.getElementById('calendar');
      const calendar = new Calendar(calendarEl, {

        // Your calendar configuration options
        plugins: [dayGridPlugin], // Add dayGrid plugin
        events: [
          // Your events data
          {
            title: 'Event 1',
            start: '2024-05-01',
            end: '2024-05-03'
          },
          {
            title: 'Event 2',
            start: '2024-05-05'
          }
        ]
      });

      // Render the calendar
      calendar.render();
    }
  }
}
</script>

<style scoped>
/* styles for CalendarComponent.vue */

.calendar-container {
  width: 33%;
  background-color: aliceblue;
  padding: 2.5rem;
  border-radius: 10px;
}

@media screen and (max-width: 820px) {
  .calendar-container {
    padding: 1.2rem;
    width: 90%;
  }
}
</style>
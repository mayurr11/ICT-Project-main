<!-- Home page -->

<template>
  <div>
    <!-- Header Component -->
    <HeaderComponent>
      <template #flightschedule>
        <div class="dropdown" ref="dropdown">
          <button @click="toggleDropdown" class="flight-schedule-btn">Flight Schedule</button>
          <div v-show="isDropdownOpen" class="dropdown-content">
            <button @click="openFlightInfoModal">Subscribe to Upcoming Flights</button>
            <button @click="openCalendarModal">Calendar</button>
          </div>
        </div>

        <!-- Flight Info Modal -->
        <div v-if="isFlightInfoModalOpen" class="modal">
          <div class="modal-content">
            <span class="close" @click="closeFlightInfoModal">&times;</span>
            <h1>Upcoming Flight Information</h1>
            <div v-if="upcomingFlights.length === 0">
              <p class="no-flight-available">No upcoming flights available.</p>
            </div>
            <ul v-else>
              <li v-for="flight in upcomingFlights" :key="flight.id">
                <div><b>{{ flight.location }}</b></div>
                <div>{{ formatDate(flight.date) }}</div>
                <div>{{ formatTime(flight.time) }}</div>
                <button @click="openSubscriptionModal(flight, flight.date)">Subscribe</button>
              </li>
            </ul>
          </div>
        </div>

        <!-- Modal for Calendar -->
        <div v-if="isCalendarModalOpen" class="modal">
          <div class="modal-content calendar-modal">
            <span class="close" @click="closeCalendarModal">&times;</span>
            <h1>Calendar</h1>
            <div class="calendar-container" ref="calendarContainer"></div>
          </div>
        </div>

        <!-- Subscription Form Modal -->
        <div v-if="isSubscriptionModalOpen" class="modal">
          <div class="modal-content">
            <span class="close" @click="closeSubscriptionModal">&times;</span>
            <div class="subscription-container">
              <h1 class="subsciption-title">Subscribe for Flight Notifications</h1>
              <div>
                <p v-if="selectedDate === 'Today'">Flight Date: Today</p>
                <p v-else>Selected Date: {{ selectedDate }}</p>
              </div>
              <form @submit.prevent="submitSubscription" class="subscription-form">
                <input type="email" v-model="email" placeholder="Enter your email" class="input-field" required>
                <label for="notification-time" class="label">Select notification time before flight:</label>
                <select id="notification-time" v-model="notificationTime" class="input-field">
                  <option value="1">1 hour</option>
                  <option value="2">2 hours</option>
                  <option value="3">3 hours</option>
                  <!-- Add more options as needed -->
                </select>
                <button type="submit" class="submit-button">Subscribe</button>
              </form>
            </div>
          </div>
        </div>
        <div v-if="subscriptionSuccess" class="popup">
          <div class="popup-content">
            <span class="close" @click="closeSubscriptionSuccess">&times;</span>
            <h2>Subscription Successful!</h2>
            <p>Thank you for subscribing.</p>
          </div>
        </div>
      </template>

      <template #enquiry>
        <div>
          <button @click="openModal" class="enquiry-button">Enquiry</button>
          <!-- Modal -->
          <!-- Enquiry Form Modal -->
          <!-- Enquiry Form Modal -->
          <div v-if="isModalOpen" class="modal">
            <div class="modal-content">
              <span class="close" @click="closeModal">&times;</span>
              <div class="enquiry-container">
                <h1 class="enquiry-title">Enquiry</h1>
                <form @submit.prevent="handleSubmit" class="enquiry-form">
                  <input type="email" v-model="email" placeholder="Your Email" class="input-field" required>
                  <input type="email" v-model="confirmEmail" placeholder="Confirm Your Email" class="input-field"
                    required>
                  <!-- Error message -->
                  <p v-if="email !== confirmEmail && confirmEmail" class="error-message">Emails do not match</p>
                  <textarea v-model="message" placeholder="Your Message" class="input-field" required></textarea>
                  <button type="submit" :disabled="email !== confirmEmail" class="submit-button">
                    Submit Enquiry
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>

        <!-- Enquiry Success Popup -->
        <div v-if="enquirySuccess" class="popup">
          <div class="popup-content">
            <span class="close" @click="closeEnquirySuccess">&times;</span>
            <h2>Enquiry Sent!</h2>
            <p>Your enquiry has been successfully submitted.</p>
          </div>
        </div>

      </template>


      <!-- Login Button Slot -->
      <template #login>
        <ButtonComponent v-if="!isLoggedIn" destination="/login" class="login-logout-btn">
          Login
        </ButtonComponent>

        <ButtonComponent v-else class="login-logout-btn" @click="logout">
          Logout
        </ButtonComponent>
      </template>


    </HeaderComponent>

    <!-- Main Content -->
    <div class="main-content">
      <VideoComponent />

      <div class="right-section">
        <!-- Information box -->
        <div class="box-content">

          <!-- List of flight information -->
          <ul>
            <li> Flight Speed: </li>
            <li> Take off time: </li>
            <li> Docking time: </li>
            <li> Flight duration: </li>
            <li> Location: </li>
          </ul>
        </div>
      </div>
      <br>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Importing required components
import HeaderComponent from "../components/HeaderComponent.vue";
import VideoComponent from "../components/VideoComponent.vue";
import ButtonComponent from "../components/ButtonComponent.vue";
import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';


export default {
  components: {
    HeaderComponent,
    VideoComponent,
    ButtonComponent,
  },
  data() {
    return {
      name: '',
      message: '',
      error: '',
      notificationTime: 1,
      isModalOpen: false,
      isDropdownOpen: false,
      isFlightInfoModalOpen: false,
      upcomingFlights: [],
      isCalendarModalOpen: false,
      calendar: null,
      events: [
        { title: 'Event 1', start: '2024-05-10' },
        { title: 'Event 2', start: '2024-05-15' },
      ],
      isSubscriptionModalOpen: false,
      email: '',
      confirmEmail: '',
      subscriptionSuccess: false,
      enquirySuccess: false,
      noFlightPopup: false,
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
  },
  methods: {
    formatDate(date) {
      // Assuming date is in the format "YYYY-MM-DD"
      const [year, month, day] = date.split('-');
      return `${day}/${month}/${year.slice(-2)}`; // Format date as "dd/mm/yy"
    },

    formatTime(time) {
      // Assuming time is in the format "HH:MM:SS"
      return time.slice(0, 5); // Extract "HH:MM"
    },
    logout() {
      this.$store.dispatch('logout');
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },

    handleSubmit() {
      if (this.email !== this.confirmEmail) {
        this.error = 'Emails do not match'; // Set error message
        return;
      }
      this.error = ''; // Clear error message if emails match
      this.submitEnquiry();
    },

    submitEnquiry() {
      axios.post('http://localhost:8000/submit_enquiry/', {
        email: this.email,
        message: this.message,
      })
        .then(response => {
          console.log(response.data.message);
          this.enquirySuccess = true;
          this.closeModal();
          this.email = "";
          this.confirmEmail = "";
          this.message = "";
        })
        .catch(error => {
          console.error(error);
        });
    },
    closeEnquirySuccess() {
      this.enquirySuccess = false;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    openFlightInfoModal() {
      this.isFlightInfoModalOpen = true;
    },
    closeFlightInfoModal() {
      this.isFlightInfoModalOpen = false;
    },
    subscribeFlight(flightId) {
      console.log("Subscribed to flight with ID:", flightId);
    },
    openCalendarModal() {
      this.isCalendarModalOpen = true;
      this.$nextTick(this.initCalendar);
    },
    closeCalendarModal() {
      this.isCalendarModalOpen = false;
      if (this.calendar) {
        this.calendar.destroy();
        this.calendar = null;
      }
    },
    initCalendar() {
      const calendarEl = this.$refs.calendarContainer;
      this.calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        selectable: true,
        select: this.handleDateSelect.bind(this, 'select'),
        dateClick: this.handleDateSelect.bind(this, 'dateClick'),
        events: [
          { title: 'Event 1', start: '2024-05-01' },
          { title: 'Event 2', start: '2024-05-05' }
        ]
      });
      this.calendar.render();
    },
    handleDateSelect(eventType, selectInfo) {
      const selectedDate = new Date(selectInfo.date || selectInfo.startStr);
      const formattedDate = selectedDate.toLocaleDateString('en-GB');
      this.openSubscriptionModal(eventType, formattedDate);
    },
    openSubscriptionModal(flight, selectedDate) {
      this.isSubscriptionModalOpen = true;
      if (flight && flight.date) {
        console.log(flight.date);
      }
      if (selectedDate === 'Today') {
        this.selectedDate = 'Today';
      } else {
        this.selectedDate = selectedDate;
      }
      this.flight = flight; // Store the flight object for later use
    },
    closeSubscriptionModal() {
      this.isSubscriptionModalOpen = false;
    },
    submitSubscription() {
      axios.post('http://localhost:8000/subscribe/', {
        email: this.email,
        notification_time: this.notificationTime,
        flight_id: this.flight.id, // Access the flight id here
        flight_date: this.selectedDate,
        flight_time: this.flight.time
      })
        .then(response => {
          console.log(response.data.message);
          this.closeSubscriptionModal();
          this.email = '';
          this.notificationTime = '';
          this.flight.id = '';
          this.selectedDate = '';
          this.flight.time = '';
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchTodayFlights() {
      axios.get('http://localhost:8000/get_today_flights/')
        .then(response => {
          console.log(response.data);
          this.upcomingFlights = response.data.flights.map(flight => ({
            id: flight.flight_id,
            time: flight.time,
            date: flight.date,
            location: flight.location,
            status: flight.status,
          }));
        })
        .catch(error => {
          console.error(error);
        });
    },
    closeSubscriptionSuccess() {
      this.subscriptionSuccess = false;
    },
    closeNoFlightPopup() {
      this.noFlightPopup = false;
    },
  },
  mounted() {
    document.title = "Home";
    this.fetchTodayFlights();
    console.log(this.upcomingFlights)
    console.log('test')
  },

};
</script>

<style scoped src="./home-view-styles.css"></style>
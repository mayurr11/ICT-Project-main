<template>
  <div>
    <!-- Header Component -->
    <HeaderComponent>
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
            <li>Flight Speed: </li>
            <li>Take off time: </li>
            <li>Docking time: </li>
            <li>Flight duration: </li>
            <li>Location: </li>
          </ul>
        </div>
      </div>
      <br>
    </div>

    <!-- Messages Section -->
    <div class="messages-section">
      <h2>Enquiries</h2>
      <!-- Refresh Button -->
      <!-- <button @click="refreshMessages" :disabled="isFetchingMessages" class="refresh-button">
        <span v-if="isFetchingMessages">Refreshing...</span>
        <span v-else>Refresh Messages</span>
      </button> -->

      <div v-if="messages.length === 0" class="no-enquiries">
        <p>No enquiries available.</p>
      </div>
      <ul v-else>
        <li v-for="(message, index) in messages" :key="message.id">
          <div class="message-left">
            <span class="message-number">{{ index + 1 }}.</span>
            <p><strong>{{ message.sender }}</strong>: {{ message.content }}</p>
          </div>
          <div class="message-right">
            <button class="reply" @click="openReplyModal(message.sender, message.id)">Reply</button>
            <button class="dismiss" @click="dismissMessage(message.id)">Dismiss</button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Reply Modal -->
    <!-- Reply Modal -->
    <div v-if="isModalOpen" class="modal">
      <div class="modal-content">
        <span class="close" @click="isModalOpen = false">&times;</span>
        <h2>Reply to Message</h2>
        <form @submit.prevent="submitReply">
          <textarea v-model="replyText" placeholder="Type your reply here..." rows="8" cols="34" class="input-reply"
            :maxlength="maxReplyLength" :disabled="isSending"></textarea>
          <br>
          <p v-if="replyError" class="error-message">{{ replyError }}</p>
          <button type="submit" class="submit-reply" :disabled="isSending">
            <span v-if="isSending">Sending reply...</span>
            <span v-else>Send</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Success Popup -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <h2>Reply sent successfully!</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderComponent from "../components/HeaderComponent.vue";
import VideoComponent from "../components/VideoComponent.vue";
import ButtonComponent from "../components/ButtonComponent.vue";
import { mapGetters } from 'vuex';

export default {
  components: {
    HeaderComponent,
    VideoComponent,
    ButtonComponent,
  },
  data() {
    return {
      messages: [],
      isModalOpen: false,
      showPopup: false,
      currentMessageId: null,
      replyText: '',
      replyError: null,
      responseEmail: '',
      maxReplyLength: '300', // maximum length for the reply text
      isSending: false, // state to track if the message is being sent
      // isFetchingMessages: false, 
    };
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push({ name: 'login' });
    },
    openReplyModal(responseEmail, messageId) {
      this.currentMessageId = messageId;
      this.responseEmail = responseEmail;
      this.isModalOpen = true;
      this.replyText = ''; // Reset reply text when opening the modal
      this.replyError = null; // Clear any previous error messages
    },
    submitReply() {
      // Validate replyText
      if (!this.replyText.trim()) {
        this.replyError = 'Reply cannot be empty.';
        return;
      }

      if (this.replyText.length > 255) {
        this.replyError = `Your reply is too long. Please keep it under 255 characters.`;
        return;
      }

      // If validation passes
      this.replyError = null;
      this.isSending = true;  // Set sending status to true
      axios.post('http://localhost:8000/send_reply_email/', {
        to_email: this.responseEmail,
        reply_message: this.replyText
      })
        .then(response => {
          if (response.data.status === 'success') {
            this.isModalOpen = false;
            this.replyText = ''; // Clear reply text after successful submission
            this.showPopup = true;
            this.fetchMessages();
            setTimeout(() => {
              this.showPopup = false;
            }, 2000);
          } else {
            console.error('Failed to send email:', response.data.message);
          }
        })
        .catch(error => {
          console.error('Error sending email:', error);
        })
        .finally(() => {
          this.isSending = false;  // Reset sending status
        });
    },
    dismissMessage(messageId) {
      axios.post('http://localhost:8000/dismiss_message/', {
        messageId: messageId
      })
        .then(response => {
          if (response.data.status === 'success') {
            this.fetchMessages();
          } else {
            console.error('Failed to dismiss message:', response.data.message);
          }
        })
        .catch(error => {
          console.error('Error during dismissal:', error);
        });
    },
    fetchMessages() {
      axios.get('http://localhost:8000/get_query/')
        .then(response => {
          this.messages = response.data.queries.map(query => ({
            id: query.id,
            sender: query.email,
            content: query.query,
          })).reverse();
        })
        .catch(error => {
          console.error('Error fetching messages:', error);
        });
    },
    refreshMessages() {
      this.fetchMessages();
    }
  },
  mounted() {
    document.title = "Admin Panel";
    if (this.isLoggedIn) {
      this.fetchMessages();
      setInterval(this.fetchMessages, 10000);
    } else {
      this.$router.push({ name: 'login' });
    }
  }
}
</script>

<style scoped src="./admin-view-styles.css"></style>
<style scoped src="./home-view-styles.css"></style>

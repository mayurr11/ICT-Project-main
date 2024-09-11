<template>
  <div>
    <HeaderComponent />

    <div class="root">

      <div class="login-container">
        <div class="left-form">
          <h1 class="login-title">Admin<br /><span class="bold">Login</span></h1>
          <form @submit.prevent="login" class="login-form">
            <input type="text" v-model="username" placeholder="Username" class="input-field" required>
            <input type="password" v-model="password" placeholder="Password" class="input-field" required>
            <button type="submit" class="login-button">Login</button>
          </form>
        </div>
        <div class="img-background">
        </div>
      </div>

    </div>

    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <span class="close" @click="closePopup">&times;</span>
        <p>{{ popupMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
// Importing Header component and register it.
import HeaderComponent from "../components/HeaderComponent.vue";
// import auth from '../store/modules/auth';

export default {
  components: {
    HeaderComponent
  },

  // Initialize data properties
  data() {
    return {
      username: '',
      password: '',
      showPopup: false,
      popupMessage: '',
      loggedIn: true
    };
  },
  methods: {
    login() {
    if (this.username && this.password) {
      const credentials = { username: this.username, password: this.password };
      this.$store.dispatch('login', credentials)
        .then((loggedIn) => {
          if (loggedIn) {
            this.showPopup = true;
            this.popupMessage = 'Login successful! ✅';
            this.username = '';
            this.password = '';
            setTimeout(() => {
              this.$router.push({ name: 'admin' });
            }, 1000);
          } else {
            this.showPopup = true;
            this.popupMessage = 'Invalid username or password! ❌';
            this.username = '';
            this.password = '';
            setTimeout(() => {
              this.showPopup = false;
            }, 1000);
          }
        })
        .catch(error => {
          console.error(error);
        });
    } else {
      console.error('Username and password are required');
    }
  },

    // Method to close popup
    closePopup() {
      this.showPopup = false;
    }
  }
};
</script>

<style scoped src="./login-view-styles.css"></style>

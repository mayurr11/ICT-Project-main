import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

// Importing views from different routes
import HomeView from './views/HomeView.vue';
import LoginView from './views/LoginView.vue';

// Importing the root component of the Vue application
import App from './App.vue';

// Importing store module
import store from './store';
import AdminView from "@/views/AdminView.vue";

// routes for the application
const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  {path: '/admin', name: 'admin', component: AdminView }
];

// create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// create Vue app instance and mount it to the root element in the HTML
createApp(App)
.use(router)
.use(store) // use the store
.mount('#app');

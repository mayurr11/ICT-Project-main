import { createStore } from 'vuex';

export default createStore({
  state: {
    isLoggedIn: !!localStorage.getItem('authToken'),
  },
  mutations: {
    login(state) {
      state.isLoggedIn = true;
    },
    logout(state) {
      state.isLoggedIn = false;
    },
  },
  actions: {
    login({ commit }, credentials) {
      // Simulate authentication logic (replace with actual logic)
      if (credentials.username === 'Admin' && credentials.password === 'Admin@123') {
        localStorage.setItem('authToken', 'fake-token'); // Save token in localStorage
        commit('login');
        return true;
      } else {
        return false;
      }
    },
    logout({ commit }) {
      localStorage.removeItem('authToken'); // Remove token from localStorage
      commit('logout');
    },
  },
  getters: {
    isLoggedIn: (state) => state.isLoggedIn,
  },
});

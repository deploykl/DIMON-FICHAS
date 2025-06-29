// src/utils/network.js
export const isOnline = () => navigator.onLine;

export const setupNetworkListener = (store) => {
  window.addEventListener('online', () => {
    store.dispatch('syncOfflineData');
  });
  window.addEventListener('offline', () => {
    store.dispatch('setOfflineMode', true);
  });
};
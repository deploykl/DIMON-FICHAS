<template>
<header-component-vue v-if="shouldShowComponents"/>
  <sidebar-component-vue v-if="shouldShowComponents"/>
  <router-view />
</template>
<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute } from 'vue-router';

import HeaderComponentVue from './components/HeaderComponent.vue';
import SidebarComponentVue from './components/SidebarComponent.vue';

// Importa los componentes
const route = useRoute();


// Lógica compartida para ambos componentes
const shouldShowComponents = computed(
  () => route.name !== 'HOME' && route.name !== 'login'
);
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

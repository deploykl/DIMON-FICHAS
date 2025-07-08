<template>
  <div class="app-layout">
    <template v-if="shouldShowComponents">
      <header-component-vue />
      <div class="main-container">
        <sidebar-component-vue 
          @toggle-collapse="handleSidebarToggle"
          :is-collapsed="isSidebarCollapsed"
        />
        <main class="content-area" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
          <router-view />
          
        <footer-component-vue />

        </main>
      </div>
    </template>
    
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import HeaderComponentVue from './components/HeaderComponent.vue';
import FooterComponentVue from './components/FooterComponent.vue';
import SidebarComponentVue from './components/SidebarComponent.vue';

const route = useRoute();
const isSidebarCollapsed = ref(false);

const shouldShowComponents = computed(
  () => route.name !== 'HOME' && route.name !== 
  'login' && route.name !== 
  'password-reset' && route.name !== 
  'reset-password' && route.name !== 
  'reuniones' && route.name
);

const handleSidebarToggle = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<style>
:root {
  --header-height: 70px;
  --sidebar-width: 250px;
  --sidebar-collapsed-width: 70px;
  --transition-speed: 0.3s;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Solo aplica estos estilos cuando shouldShowComponents es true */
.main-container {
  display: flex;
  flex: 1;
  margin-top: var(--header-height);
  position: relative;
}

.content-area {
  flex: 1;
  padding: 20px;
  transition: margin-left var(--transition-speed) ease;
  width: 100%;
  min-height: calc(100vh - var(--header-height));
  background-color: #f8f9fa;
}

/* Estilos responsivos solo para layout con sidebar */
@media (min-width: 769px) {
  .content-area {
    margin-left: var(--sidebar-width);
  }
  
  .content-area.sidebar-collapsed {
    margin-left: var(--sidebar-collapsed-width);
  }
}
</style>
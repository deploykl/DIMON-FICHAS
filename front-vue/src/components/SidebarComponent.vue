<template>
  <!-- Botón de toggle para móvil (siempre visible en móvil) -->
  <div v-if="isMobile" class="mobile-toggle-btn" @click="toggleSidebar">
    <i class="fas fa-bars"></i>
  </div>

  <!-- Sidebar con overlay en móvil -->
  <div v-if="isMobile && !isCollapsed" class="sidebar-overlay" @click="toggleSidebar"></div>

  <aside :class="['sidebar', { 'collapsed': isCollapsed, 'mobile-hidden': isMobile && isCollapsed }]">
    <!-- Botón para colapsar/expandir (oculto en móvil) -->
    <div class="toggle-btn" @click="toggleSidebar" v-if="!isMobile">
      <i :class="[isCollapsed ? 'fas fa-angle-double-right' : 'fas fa-angle-double-left']"></i>
    </div>

    <!-- Logo -->
    <div class="sidebar-header"></div>

    <!-- Menú principal -->
    <nav class="sidebar-menu">
      <ul>
        <li v-for="(item, index) in menuItems" :key="index" :class="{ 'active': activeMenu === index }">
          <!-- Ítems de primer nivel -->
          <router-link v-if="!item.submenu" :to="item.path" class="menu-item" @click="() => toggleSubmenu(index)">
            <div class="menu-content">
              <i :class="['fas', item.icon]"></i>
              <span v-if="!isCollapsed || isMobile">{{ item.title }}</span>
            </div>
          </router-link>

          <div v-else class="menu-item" @click="toggleSubmenu(index)">
            <div class="menu-content">
              <i :class="['fas', item.icon]"></i>
              <span v-if="!isCollapsed || isMobile">{{ item.title }}</span>
            </div>
            <i v-if="item.submenu && (!isCollapsed || isMobile)"
              :class="['fas', 'submenu-arrow', isSubmenuOpen(index) ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </div>


          <!-- Submenús -->
          <transition name="slide">
            <ul v-if="item.submenu && isSubmenuOpen(index) && (!isCollapsed || isMobile)" class="submenu">
              <li v-for="(subItem, subIndex) in item.submenu" :key="subIndex"
                :class="{ 'active': activeSubmenu === `${index}-${subIndex}` }">
                <router-link :to="subItem.path" class="submenu-item" @click="handleSubmenuClick(index, subIndex)">
                  <i :class="['fas', subItem.icon]"></i>
                  <span>{{ subItem.title }}</span>
                </router-link>
              </li>
            </ul>
          </transition>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['toggle-collapse'])

// Estado del sidebar
const isCollapsed = ref(false)
const isMobile = ref(false)
const activeMenu = ref(null)
const activeSubmenu = ref(null)
const openSubmenus = ref([])

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
})

// Función para alternar el sidebar
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  emit('toggle-collapse', isCollapsed.value)
}

// Sincronizamos con los cambios de props
watch(() => props.isCollapsed, (newVal) => {
  isCollapsed.value = newVal
})

// Datos de ejemplo del menú
const menuItems = ref([
  {
    title: 'Dashboard',
    icon: 'fa-tachometer-alt',
    path: '/urls',
    submenu: null
  },
  {
    title: 'Emergencia',
    icon: 'fa-user-injured',
    path: '/patients',
    submenu: [
      { title: 'Fichas de Monitoreo', icon: 'fa-chart-bar', path: '/fichas' },
      { title: 'Matriz de compromiso', icon: 'fa-book', path: '/matriz-list' },
    ]
  },
  {
    title: 'Fichas de Monitoreo',
    icon: 'fa-chart-bar',
    path: '/fichas',
    submenu: null
  },
  {
    title: 'Matriz de compromiso',
    icon: 'fa-book',
    path: '/matriz-list',
    submenu: null
  },
  {
    title: 'Alertas',
    icon: 'fa-chart-bar',
    path: '/alertas',
    submenu: null
  },
  {
    title: 'Game',
    icon: 'fa-gamepad',
    path: '/game',
    submenu: null
  },
    {
    title: 'Archivos',
    icon: 'fa-file',
    path: '/archivos',
    submenu: null
  },
  {
    title: 'Boletin',
    icon: 'fa-book',
    path: '/boletin',
    submenu: null
  },
  {
    title: 'Boletin-list',
    icon: 'fa-pen',
    path: '/boletin-list',
    submenu: null
  },
    {
    title: 'Agregar Reunión',
    icon: 'fa-pen',
    path: '/reuniones/admin',
    submenu: null
  },
    {
    title: 'Reuniones',
    icon: 'fa-pen',
    path: '/reuniones',
    submenu: null
  },
])

const toggleSubmenu = (index) => {
  if (menuItems.value[index].submenu) {
    const submenuIndex = openSubmenus.value.indexOf(index)
    if (submenuIndex === -1) {
      openSubmenus.value.push(index)
    } else {
      openSubmenus.value.splice(submenuIndex, 1)
    }
  } else {
    activeMenu.value = index
    activeSubmenu.value = null
    if (isMobile.value) {
      isCollapsed.value = true // Cerrar sidebar después de seleccionar un ítem en móvil
    }
  }
}

const isSubmenuOpen = (index) => {
  return openSubmenus.value.includes(index)
}

const setActiveSubmenu = (menuIndex, submenuIndex) => {
  activeMenu.value = menuIndex
  activeSubmenu.value = `${menuIndex}-${submenuIndex}`
}

const handleSubmenuClick = (menuIndex, submenuIndex) => {
  setActiveSubmenu(menuIndex, submenuIndex)
  if (isMobile.value) {
    isCollapsed.value = true // Cerrar sidebar después de seleccionar un subítem en móvil
  }
}

// Configuración responsive
const checkScreenSize = () => {
  const width = window.innerWidth
  isMobile.value = width < 768
  if (isMobile.value) {
    isCollapsed.value = true // Por defecto colapsado en móvil
  } else {
    isCollapsed.value = false // Expandido en desktop
  }
}

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)

  // Marcar menú activo según la ruta actual
  const currentPath = route.path
  menuItems.value.forEach((item, index) => {
    if (item.path === currentPath) {
      activeMenu.value = index
    } else if (item.submenu) {
      item.submenu.forEach((subItem, subIndex) => {
        if (subItem.path === currentPath) {
          activeMenu.value = index
          activeSubmenu.value = `${index}-${subIndex}`
          if (!openSubmenus.value.includes(index)) {
            openSubmenus.value.push(index)
          }
        }
      })
    }
  })
})
</script>

<style scoped>
/* Variables CSS */
:root {
  --sidebar-width: 250px;
  --sidebar-collapsed-width: 70px;
  --header-height: 60px;
  --transition-speed: 0.3s;
}

/* Estilos base */
.sidebar {
  width: var(--sidebar-width);
  height: calc(100vh - var(--header-height));
  position: fixed;
  top: var(--header-height);
  left: 0;
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  transition: all var(--transition-speed) ease;
  z-index: 1001;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

/* Encabezado del sidebar */
.sidebar-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
}

/* Botón de toggle */
.toggle-btn {
  position: absolute;
  right: 10px;
  top: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 101;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Estilos del menú */
.sidebar-menu {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.sidebar-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  position: relative;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.menu-item i {
  min-width: 20px;
  text-align: center;
}

.menu-item span {
  white-space: nowrap;
}

.submenu-arrow {
  transition: transform 0.3s ease;
}

/* Submenús */
.submenu {
  background: rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.submenu-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 20px 10px 50px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
}

.submenu-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.submenu-item i {
  font-size: 0.8rem;
}

/* Estilos activos */
.active>.menu-item {
  background: rgba(255, 255, 255, 0.15);
  border-left: 3px solid white;
}

.active .submenu-item {
  color: white;
}

/* Transiciones */
.slide-enter-active,
.slide-leave-active {
  transition: max-height 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
}

.slide-enter-to,
.slide-leave-from {
  max-height: 300px;
}

/* Estilo para el botón de toggle en móvil */
.mobile-toggle-btn {
  position: fixed;
  left: 15px;
  top: calc(var(--header-height) + 5px);
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.mobile-toggle-btn:hover {
  transform: scale(1.1);
}

/* Overlay para móviles */
.sidebar-overlay {
  position: fixed;
  top: var(--header-height);
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px);
}

/* Ajustes para móvil */
@media (max-width: 768px) {
  .sidebar {
    width: 250px;
    transform: translateX(-100%);
    z-index: 1001;
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.3);
  }

  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .sidebar.collapsed {
    width: 250px;
  }

  .toggle-btn {
    display: none;
  }

  /* Mostrar texto completo en móvil cuando el sidebar está abierto */
  .sidebar:not(.collapsed) .menu-item span,
  .sidebar:not(.collapsed) .submenu-arrow {
    display: inline !important;
  }
}

/* Estilos para sidebar colapsado (solo desktop) */
@media (min-width: 769px) {

  .sidebar.collapsed .menu-item span,
  .sidebar.collapsed .submenu-arrow,
  .sidebar.collapsed .user-details,
  .sidebar.collapsed .logo-full {
    display: none;
  }

  .sidebar.collapsed .menu-item {
    justify-content: center;
    padding: 12px 0;
  }

  .sidebar.collapsed .menu-content {
    justify-content: center;
  }

  .sidebar.collapsed .sidebar-header {
    padding: 20px 0;
  }

  .sidebar.collapsed .toggle-btn {
    right: 20px;
  }
}
</style>
<template>
  <aside 
    :class="['sidebar', { 'collapsed': isCollapsed }]"
    :style="sidebarStyle"
  >
    <!-- Botón para colapsar/expandir -->
    <div class="toggle-btn" @click="toggleSidebar">
      <i :class="[isCollapsed ? 'fas fa-angle-double-right' : 'fas fa-angle-double-left']"></i>
    </div>

    <!-- Logo >-->
    <div class="sidebar-header">
      
    </div>

    <!-- Menú principal -->
    <nav class="sidebar-menu">
      <ul>
        <li 
          v-for="(item, index) in menuItems" 
          :key="index"
          :class="{ 'active': activeMenu === index }"
        >
          <!-- Ítems de primer nivel -->
          <div 
            class="menu-item" 
            @click="toggleSubmenu(index)"
          >
            <div class="menu-content">
              <i :class="['fas', item.icon]"></i>
              <span v-if="!isCollapsed">{{ item.title }}</span>
            </div>
            <i 
              v-if="item.submenu && !isCollapsed" 
              :class="['fas', 'submenu-arrow', isSubmenuOpen(index) ? 'fa-chevron-up' : 'fa-chevron-down']"
            ></i>
          </div>

          <!-- Submenús -->
          <transition name="slide">
            <ul 
              v-if="item.submenu && isSubmenuOpen(index) && !isCollapsed" 
              class="submenu"
            >
              <li 
                v-for="(subItem, subIndex) in item.submenu" 
                :key="subIndex"
                :class="{ 'active': activeSubmenu === `${index}-${subIndex}` }"
              >
                <router-link 
                  :to="subItem.path" 
                  class="submenu-item"
                  @click="setActiveSubmenu(index, subIndex)"
                >
                  <i :class="['fas', subItem.icon]"></i>
                  <span>{{ subItem.title }}</span>
                </router-link>
              </li>
            </ul>
          </transition>
        </li>
      </ul>
    </nav>

    <!-- Footer del sidebar
    <div class="sidebar-footer" v-if="!isCollapsed">
      <div class="user-info">
        <img :src="userImage" alt="Usuario" class="user-avatar">
        <div class="user-details">
          <span class="user-name">{{ userName }}</span>
          <span class="user-role">{{ userRole }}</span>
        </div>
      </div>
    </div> -->
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Estado del sidebar
const isCollapsed = ref(false)
const activeMenu = ref(null)
const activeSubmenu = ref(null)
const openSubmenus = ref([])

// Datos de ejemplo
const menuItems = ref([
  {
    title: 'Dashboard',
    icon: 'fa-tachometer-alt',
    path: '/dashboard',
    submenu: null
  },
  {
    title: 'Pacientes',
    icon: 'fa-user-injured',
    path: '/patients',
    submenu: [
      { title: 'Registrar', icon: 'fa-user-plus', path: '/patients/register' },
      { title: 'Listado', icon: 'fa-list', path: '/patients/list' },
      { title: 'Historial', icon: 'fa-history', path: '/patients/history' }
    ]
  },
  {
    title: 'Citas',
    icon: 'fa-calendar-check',
    path: '/appointments',
    submenu: [
      { title: 'Agendar', icon: 'fa-plus-circle', path: '/appointments/schedule' },
      { title: 'Calendario', icon: 'fa-calendar-alt', path: '/appointments/calendar' }
    ]
  },
  {
    title: 'Reportes',
    icon: 'fa-chart-bar',
    path: '/reports',
    submenu: null
  },
  {
    title: 'Configuración',
    icon: 'fa-cog',
    path: '/settings',
    submenu: [
      { title: 'Usuarios', icon: 'fa-users', path: '/settings/users' },
      { title: 'Permisos', icon: 'fa-key', path: '/settings/permissions' }
    ]
  }
])

// Datos de usuario
const userName = ref('Dr. Juan Pérez')
const userRole = ref('Administrador')
const userImage = ref('https://via.placeholder.com/40')

// Funciones para manejar el estado
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

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
  }
}

const isSubmenuOpen = (index) => {
  return openSubmenus.value.includes(index)
}

const setActiveSubmenu = (menuIndex, submenuIndex) => {
  activeMenu.value = menuIndex
  activeSubmenu.value = `${menuIndex}-${submenuIndex}`
}

// Estilo computado para el sidebar
const sidebarStyle = computed(() => {
  return {
    width: isCollapsed.value ? '70px' : '250px',
    top: '60px', // Ajustar según la altura de tu header
    height: 'calc(100vh - 60px)' // Restar la altura del header
  }
})

// Configuración responsive
const checkScreenSize = () => {
  const width = window.innerWidth
  if (width < 768) {
    isCollapsed.value = true
  } else {
    isCollapsed.value = false
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
/* Estilos base */
.sidebar {
  position: fixed;
  left: 0;
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  transition: all 0.3s ease;
  z-index: 100;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
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
.active > .menu-item {
  background: rgba(255, 255, 255, 0.15);
  border-left: 3px solid white;
}

.active .submenu-item {
  color: white;
}

/* Footer del sidebar */
.sidebar-footer {
  padding: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.7rem;
  opacity: 0.8;
}

/* Transiciones */
.slide-enter-active, .slide-leave-active {
  transition: max-height 0.3s ease;
}

.slide-enter-from, .slide-leave-to {
  max-height: 0;
}

.slide-enter-to, .slide-leave-from {
  max-height: 300px;
}

/* Estilos para sidebar colapsado */
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

/* Responsive */
@media (max-width: 768px) {
  .sidebar:not(.collapsed) {
    width: 250px;
    z-index: 1000;
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.2);
  }
  
  .sidebar.collapsed {
    width: 70px;
  }
  
  /* Opcional: overlay para móviles */
  .sidebar-overlay {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 99;
    display: none;
  }
  
  .sidebar:not(.collapsed) + .sidebar-overlay {
    display: block;
  }
}
</style>
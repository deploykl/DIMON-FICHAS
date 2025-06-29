<template>
  <main id="main" class="main">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4 header-container">
      <div>
        <h1 class="mb-0 header-title">Lista de enlaces de información</h1>
        <p class="mb-0 header-subtitle">Acceso rápido a recursos digitales</p>
      </div>
      <router-link to="/fichas" class="btn btn-outline-light">
        <i class="fas fa-arrow-left me-2"></i> Volver
      </router-link>
    </div>

    <!-- Search and Filter -->
    <div class="row justify-content-center mb-4 g-3">
      <div class="col-md-8">
        <div class="input-group search-container">
          <span class="input-group-text">
            <i class="fas fa-search"></i>
          </span>
          <input type="text" class="form-control" placeholder="Buscar enlaces..." 
                 v-model="searchQuery" @input="filterEnlaces">
        </div>
      </div>
      <div class="col-md-4">
        <div class="input-group filter-container">
          <span class="input-group-text">
            <i class="fas fa-filter"></i>
          </span>
          <select class="form-select" v-model="filterType" @change="filterEnlaces">
            <option value="">Todos los tipos</option>
            <option v-for="type in uniqueTypes" :key="type" :value="type">{{ type }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5 loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-3">Cargando enlaces...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger text-center error-container">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchEnlaces">
        Reintentar
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredEnlaces.length === 0" class="text-center py-5 empty-container">
      <i class="fas fa-link fa-3x mb-3"></i>
      <h4>No se encontraron enlaces</h4>
      <p class="text-muted">Intenta con otros términos de búsqueda o añade nuevos enlaces</p>
    </div>

    <!-- Enlaces Grid -->
   <div class="row g-4">
      <div v-for="(enlace, index) in filteredEnlaces" :key="enlace.id"
           class="col-xxl-2 col-xl-3 col-lg-4 col-md-6 col-sm-6"
           :class="`animate__animated animate__fadeInUp`" 
           :style="`animation-delay: ${index * 0.1}s`">
        <a :href="enlace.url" target="_blank" class="text-decoration-none h-100 card-link">
          <div class="dashboard-card h-100">
            <div class="card-icon-container">
              <img v-if="enlace.imagen_url" :src="enlace.imagen_url" :alt="enlace.titulo" class="card-icon">
              <i v-else :class="getIconClass(enlace.tipo)"></i>
            </div>
            <h4 class="card-title">{{ enlace.titulo }}</h4>
            <p class="card-description">{{ enlace.descripcion }}</p>
            <span class="badge rounded-pill type-badge">{{ enlace.tipo || 'General' }}</span>
          </div>
        </a>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/components/services/auth_axios';

// Estado
const enlaces = ref([])
const filteredEnlaces = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const filterType = ref('')

// Obtener enlaces de la API
const fetchEnlaces = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await api.get('enlace/urls/')
    
    // Modificar las URLs de las imágenes usando la variable de entorno
    enlaces.value = response.data.map(enlace => ({
      ...enlace,
      imagen_url: enlace.imagen_url 
        ? `${process.env.VUE_APP_IMG_SERVER}${enlace.imagen_url}` 
        : null
    }))
    
    filteredEnlaces.value = [...enlaces.value]
  } catch (err) {
    console.error('Error fetching enlaces:', err)
    error.value = 'Error al cargar los enlaces. Verifica tu conexión.'
  } finally {
    loading.value = false
  }
}

// Filtrar enlaces
const filterEnlaces = () => {
  filteredEnlaces.value = enlaces.value.filter(enlace => {
    const matchesSearch = enlace.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      enlace.descripcion.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = filterType.value === '' || enlace.tipo === filterType.value
    return matchesSearch && matchesType
  })
}

// Tipos únicos para el filtro
const uniqueTypes = computed(() => {
  const types = new Set()
  enlaces.value.forEach(enlace => types.add(enlace.tipo))
  return Array.from(types).sort()
})

// Iconos según el tipo
const getIconClass = (tipo) => {
  if (!tipo) return 'fas fa-link'

  const tipoLower = tipo.toLowerCase()
  const iconMap = {
    'documento': 'fas fa-file-alt',
    'herramienta': 'fas fa-tools',
    'dashboard': 'fas fa-chart-line',
    'sistema': 'fas fa-laptop-code',
    'recurso': 'fas fa-box-open',
    'videoconferencia': 'fas fa-video'
  }

  if (iconMap[tipoLower]) return iconMap[tipoLower]

  for (const [key, value] of Object.entries(iconMap)) {
    if (tipoLower.includes(key)) return value
  }

  return 'fas fa-link'
}

// Inicialización
onMounted(() => {
  fetchEnlaces()
})
</script>

<style scoped>
:root {
  --primary-color: #103c4b;
  --primary-light: #1a5a6e;
  --accent-color: #e63946;
  --dark-color: #1d3557;
  --text-color: #333;
  --text-light: #6c757d;
  --white: #ffffff;
}

.main {
  padding: 20px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Header Styles */
.header-container {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  border-radius: 12px;
  padding: 15px 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 0.2rem;
}

.header-subtitle {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

/* Search and Filter */
.search-container, .filter-container {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.search-container .input-group-text,
.filter-container .input-group-text {
  background-color: var(--white);
  color: var(--primary-color);
  border-right: none;
}

.search-container .form-control,
.filter-container .form-select {
  border-left: none;
  box-shadow: none;
}

/* Cards */
.dashboard-card {
  background: var(--white);
  border-radius: 12px;
  padding: 20px;
  height: 100%;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-top: 4px solid var(--primary-color);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border-top-color: var(--accent-color);
}

.card-icon-container {
  width: 80px;
  height: 80px;
  background: var(--white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid var(--primary-color);
  transition: all 0.3s ease;
}

.card-icon {
  max-width: 60%;
  max-height: 60%;
  object-fit: contain;
  transition: all 0.3s ease;
}

.dashboard-card:hover .card-icon-container {
  background-color: #103c4b;
  border-color: var(--primary-color);
}

.dashboard-card:hover .card-icon {
  filter: brightness(0) invert(1);
}

.card-icon-container i {
  font-size: 1.5rem;
  color: var(--primary-color);
  transition: all 0.3s ease;
}

.dashboard-card:hover .card-icon-container i {
  color: var(--white);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--dark-color);
  margin-bottom: 10px;
  text-align: center;
  min-height: 3em;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-description {
  font-size: 0.9rem;
  color: #103c4b;
  margin-bottom: 15px;
  text-align: center;
  flex-grow: 1;
}

.type-badge {
  background-color: var(--primary-color);
  color: white;
  align-self: center;
  margin-top: auto;
  padding: 5px 10px;
  font-weight: 500;
}

/* States */
.loading-container {
  background: var(--white);
  border-radius: 12px;
  padding: 40px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.error-container {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.empty-container {
  background: var(--white);
  border-radius: 12px;
  padding: 40px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.empty-container i {
  color: var(--primary-color);
}

/* Animations */
.animate__animated.animate__fadeInUp {
  --animate-duration: 0.5s;
}

/* Responsive - 6 columnas en pantallas extra grandes */
@media (min-width: 1400px) {
  .col-xxl-2 {
    flex: 0 0 auto;
    width: 16.66666667%;
  }
}

@media (max-width: 1399.98px) {
  /* 4 columnas en pantallas grandes */
  .col-xl-3 {
    flex: 0 0 auto;
    width: 25%;
  }
}

@media (max-width: 1199.98px) {
  /* 3 columnas en pantallas medianas */
  .col-lg-4 {
    flex: 0 0 auto;
    width: 33.333333%;
  }
}

@media (max-width: 991.98px) {
  /* 2 columnas en tablets */
  .col-md-6 {
    flex: 0 0 auto;
    width: 50%;
  }
}

@media (max-width: 767.98px) {
  /* 1 columna en móviles */
  .col-sm-6 {
    flex: 0 0 auto;
    width: 100%;
  }
  
  .header-title {
    font-size: 1.4rem;
  }
  
  .card-icon-container {
    width: 60px;
    height: 60px;
  }
  
  .card-title {
    font-size: 1rem;
  }
}

@media (max-width: 575.98px) {
  .header-container {
    padding: 15px;
  }
  
  .header-title {
    font-size: 1.2rem;
  }
  
  .card-icon-container {
    width: 50px;
    height: 50px;
  }
  
  .dashboard-card {
    padding: 15px;
  }
}
</style>
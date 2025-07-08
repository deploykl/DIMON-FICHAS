<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Boletines Informativos</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/">Inicio</a></li>
          <li class="breadcrumb-item active">Boletines</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <!-- Filtros y búsqueda -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="input-group">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Buscar boletines..." 
              v-model="searchQuery"
              @input="fetchNewsletters"
            >
            <button class="btn btn-outline-secondary" type="button">
              <i class="bi bi-search"></i>
            </button>
          </div>
        </div>
        <div class="col-md-6">
          <select class="form-select" v-model="filterStatus" @change="fetchNewsletters">
            <option value="all">Todos los estados</option>
            <option value="published">Publicados</option>
            <option value="drafts">Borradores</option>
          </select>
        </div>
      </div>

      <!-- Listado de boletines -->
      <div class="row">
        <div 
          class="col-lg-4 col-md-6 mb-4" 
          v-for="newsletter in newsletters" 
          :key="newsletter.id"
        >
          <div class="card h-100 newsletter-card">
            <!-- Imagen destacada -->
            <div class="newsletter-image-container">
              <img 
                v-if="newsletter.imagen_principal_url" 
                :src="newsletter.imagen_principal_url" 
                class="card-img-top newsletter-image"
                alt="Imagen del boletín"
              >
              <div v-else class="no-image-placeholder">
                <i class="bi bi-newspaper"></i>
              </div>
              <span class="badge" :class="newsletter.is_published ? 'bg-success' : 'bg-secondary'">
                {{ newsletter.is_published ? 'Publicado' : 'Borrador' }}
              </span>
            </div>

            <!-- Contenido del boletín -->
            <div class="card-body">
              <h5 class="card-title">{{ newsletter.titulo }}</h5>
              <p class="card-text text-muted">
                <small>
                  <i class="bi bi-person"></i> {{ newsletter.autor_username }} | 
                  <i class="bi bi-calendar"></i> {{ formatDate(newsletter.created_at) }}
                </small>
              </p>
              <p class="card-text">{{ truncateContent(newsletter.contenido, 150) }}</p>
            </div>

            <!-- Acciones -->
            <div class="card-footer bg-transparent">
              <button 
                @click="viewNewsletterDetail(newsletter)" 
                class="btn btn-outline-primary btn-sm"
              >
                <i class="bi bi-eye"></i> Ver completo
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Paginación -->
      <div class="row">
        <div class="col-12">
          <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="changePage(currentPage - 1)">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li 
                v-for="page in visiblePages" 
                :key="page" 
                class="page-item" 
                :class="{ active: currentPage === page }"
              >
                <button class="page-link" @click="changePage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="changePage(currentPage + 1)">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      <!-- Modal para ver boletín completo -->
      <div class="modal fade" :class="{ show: showDetailModal, 'd-block': showDetailModal }" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ selectedNewsletter?.titulo }}</h5>
              <button type="button" class="btn-close" @click="closeDetailModal"></button>
            </div>
            <div class="modal-body">
              <!-- Carrusel de imágenes -->
              <div id="newsletterImagesCarousel" class="carousel slide mb-4" v-if="selectedNewsletter?.imagenes?.length">
                <div class="carousel-inner rounded">
                  <div 
                    v-for="(image, index) in selectedNewsletter.imagenes" 
                    :key="image.id"
                    class="carousel-item"
                    :class="{ active: index === 0 }"
                  >
                    <img 
                      :src="image.imagen_url" 
                      class="d-block w-100"
                      :alt="'Imagen ' + (index + 1) + ' del boletín'"
                    >
                    <div class="carousel-caption d-none d-md-block" v-if="image.es_portada">
                      <span class="badge bg-primary">Portada</span>
                    </div>
                  </div>
                </div>
                <button 
                  class="carousel-control-prev" 
                  type="button" 
                  data-bs-target="#newsletterImagesCarousel" 
                  data-bs-slide="prev"
                >
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Anterior</span>
                </button>
                <button 
                  class="carousel-control-next" 
                  type="button" 
                  data-bs-target="#newsletterImagesCarousel" 
                  data-bs-slide="next"
                >
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Siguiente</span>
                </button>
              </div>

              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">
                  <i class="bi bi-person"></i> {{ selectedNewsletter?.autor_username }}
                </span>
                <span class="text-muted">
                  <i class="bi bi-calendar"></i> {{ formatDate(selectedNewsletter?.created_at) }}
                </span>
              </div>
              <div class="newsletter-content" v-html="formatContent(selectedNewsletter?.contenido)"></div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeDetailModal">
                <i class="bi bi-x-circle"></i> Cerrar
              </button>
              <button 
                type="button" 
                class="btn btn-primary"
                @click="printNewsletter"
                v-if="selectedNewsletter"
              >
                <i class="bi bi-printer"></i> Imprimir
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade" :class="{ show: showDetailModal }" v-if="showDetailModal"></div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { api } from '@/components/services/auth_axios';

// Datos reactivos
const newsletters = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const isLoading = ref(false);
const error = ref(null);
const searchQuery = ref('');
const filterStatus = ref('published');
const showDetailModal = ref(false);
const selectedNewsletter = ref(null);

// Configuración de paginación
const maxVisiblePages = 5;
const visiblePages = computed(() => {
  const pages = [];
  let startPage = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1);
  
  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  
  return pages;
});

// Funciones de formato
const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('es-ES', options);
};

const truncateContent = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};

const formatContent = (content) => {
  if (!content) return '';
  return content.replace(/\n/g, '<br>');
};

// Funciones de fetch
const fetchNewsletters = async (page = 1) => {
  isLoading.value = true;
  error.value = null;
  
  try {
    let url = `boletin/boletin/?page=${page}`;
    
    // Aplicar filtros
    if (searchQuery.value) {
      url += `&search=${encodeURIComponent(searchQuery.value)}`;
    }
    
    if (filterStatus.value === 'published') {
      url += '&is_published=true';
    } else if (filterStatus.value === 'drafts') {
      url += '&is_published=false';
    }
    
    const response = await api.get(url);
    
    if (response.data.results) {
      newsletters.value = response.data.results;
      totalPages.value = Math.ceil(response.data.count / 12); // 12 items por página
    } else {
      newsletters.value = response.data;
      totalPages.value = 1;
    }
    
    currentPage.value = page;
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al cargar boletines';
    console.error('Error:', err);
  } finally {
    isLoading.value = false;
  }
};

// Funciones de paginación
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page;
    fetchNewsletters(page);
  }
};

// Funciones para el modal de detalle
const viewNewsletterDetail = (newsletter) => {
  selectedNewsletter.value = newsletter;
  showDetailModal.value = true;
};

const closeDetailModal = () => {
  showDetailModal.value = false;
};

const printNewsletter = () => {
  window.print();
};

// Cargar datos iniciales
onMounted(() => {
  fetchNewsletters();
});
</script>

<style scoped>
.newsletter-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 10px;
  overflow: hidden;
}

.newsletter-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.newsletter-image-container {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.newsletter-image {
  height: 100%;
  width: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.newsletter-card:hover .newsletter-image {
  transform: scale(1.05);
}

.no-image-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #6c757d;
  font-size: 3rem;
}

.badge {
  position: absolute;
  top: 10px;
  right: 10px;
}

.newsletter-content {
  line-height: 1.8;
  font-size: 1.1rem;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-backdrop {
  opacity: 0.5;
}

/* Estilos para el carrusel */
.carousel {
  max-height: 400px;
  overflow: hidden;
}

.carousel-item img {
  object-fit: cover;
  max-height: 400px;
  width: 100%;
}

.carousel-caption {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 5px;
  padding: 5px 10px;
}

/* Estilos para el modal en modo impresión */
@media print {
  body * {
    visibility: hidden;
  }
  .modal, .modal * {
    visibility: visible;
  }
  .modal {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: auto;
    margin: 0;
    padding: 0;
  }
  .modal-footer {
    display: none;
  }
  
  .carousel, .carousel-inner, .carousel-item {
    display: block !important;
    position: static !important;
  }
  
  .carousel-item {
    page-break-inside: avoid;
  }
  
  .carousel-item:not(.active) {
    display: none !important;
  }
  
  .carousel-controls {
    display: none !important;
  }
}
</style>
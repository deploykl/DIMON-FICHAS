<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Gestión de Boletines</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item">Comunicación</li>
          <li class="breadcrumb-item active">Boletines</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <!-- Botón para abrir modal de creación -->
              <button @click="openCreateModal" class="btn btn-primary mb-3">
                <i class="bi bi-plus-circle"></i> Nuevo Boletín
              </button>

              <!-- Tabla de boletines -->
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Imagen</th>
                      <th>Título</th>
                      <th>Autor</th>
                      <th>Fecha</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="newsletter in newsletters" :key="newsletter.id">
                      <td>{{ newsletter.id }}</td>
                      <td>
                        <img 
                          v-if="newsletter.imagen_url" 
                          :src="newsletter.imagen_url" 
                          alt="Imagen del boletín" 
                          class="img-thumbnail" 
                          style="max-width: 100px;"
                        >
                      </td>
                      <td>{{ newsletter.titulo }}</td>
                      <td>{{ newsletter.autor_username }}</td>
                      <td>{{ formatDate(newsletter.created_at) }}</td>
                      <td>
                        <span :class="['badge', newsletter.is_published ? 'bg-success' : 'bg-warning']">
                          {{ newsletter.is_published ? 'Publicado' : 'Borrador' }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group">
                          <button @click="openEditModal(newsletter)" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-pencil"></i>
                          </button>
                          <button @click="openDeleteModal(newsletter.id)" class="btn btn-sm btn-outline-danger">
                            <i class="bi bi-trash"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Paginación -->
              <nav v-if="totalPages > 1">
                <ul class="pagination justify-content-center">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="fetchNewsletters(currentPage - 1)">Anterior</button>
                  </li>
                  <li 
                    v-for="page in totalPages" 
                    :key="page" 
                    class="page-item" 
                    :class="{ active: currentPage === page }"
                  >
                    <button class="page-link" @click="fetchNewsletters(page)">{{ page }}</button>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link" @click="fetchNewsletters(currentPage + 1)">Siguiente</button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para Crear/Editar -->
    <div class="modal fade" :class="{ show: showModal, 'd-block': showModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Editar Boletín' : 'Nuevo Boletín' }}</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="titulo" class="form-label">Título</label>
                <input type="text" class="form-control" id="titulo" v-model="formData.titulo" required>
              </div>
              
              <div class="mb-3">
                <label for="contenido" class="form-label">Contenido</label>
                <textarea class="form-control" id="contenido" v-model="formData.contenido" rows="5" required></textarea>
              </div>
              
              <div class="mb-3">
                <label for="imagen" class="form-label">Imagen</label>
                <input type="file" class="form-control" id="imagen" @change="handleImageUpload">
                <small class="text-muted">Tamaño recomendado: 800x400px</small>
                <img v-if="formData.imagen_url && !formData.imagen" :src="formData.imagen_url" class="img-thumbnail mt-2" style="max-width: 200px;">
              </div>
              
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_published" v-model="formData.is_published">
                <label class="form-check-label" for="is_published">Publicar</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm">
              {{ isEditing ? 'Actualizar' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ show: showModal }" v-if="showModal"></div>

    <!-- Modal para Eliminar -->
    <div class="modal fade" :class="{ show: showDeleteModal, 'd-block': showDeleteModal }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar Eliminación</h5>
            <button type="button" class="close" @click="closeDeleteModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas eliminar este boletín? Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="confirmDelete">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ show: showDeleteModal }" v-if="showDeleteModal"></div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '@/components/services/auth_axios';

// Datos reactivos
const newsletters = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const isLoading = ref(false);
const error = ref(null);

// Datos para modales
const showModal = ref(false);
const showDeleteModal = ref(false);
const isEditing = ref(false);
const currentNewsletterId = ref(null);

// Formulario
const formData = ref({
  titulo: '',
  contenido: '',
  imagen: null,
  imagen_url: null,
  is_published: false
});

// Función para formatear fecha
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('es-ES', options);
};

// Función para obtener boletines
const fetchNewsletters = async (page = 1) => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await api.get('boletin/boletin/');
    
    if (response.data.results) {
      newsletters.value = response.data.results;
      totalPages.value = Math.ceil(response.data.count / 10);
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

// Funciones para modal de creación/edición
const openCreateModal = () => {
  resetForm();
  isEditing.value = false;
  showModal.value = true;
};

const openEditModal = (newsletter) => {
  formData.value = {
    titulo: newsletter.titulo,
    contenido: newsletter.contenido,
    imagen: null,
    imagen_url: newsletter.imagen_url,
    is_published: newsletter.is_published
  };
  currentNewsletterId.value = newsletter.id;
  isEditing.value = true;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleImageUpload = (event) => {
  formData.value.imagen = event.target.files[0];
  formData.value.imagen_url = null;
};

const resetForm = () => {
  formData.value = {
    titulo: '',
    contenido: '',
    imagen: null,
    imagen_url: null,
    is_published: false
  };
  currentNewsletterId.value = null;
};

const submitForm = async () => {
  try {
    const data = new FormData();
    data.append('titulo', formData.value.titulo);
    data.append('contenido', formData.value.contenido);
    data.append('is_published', formData.value.is_published);
    if (formData.value.imagen) {
      data.append('imagen', formData.value.imagen);
    }

    if (isEditing.value) {
      await api.put(`boletin/boletin/${currentNewsletterId.value}/`, data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } else {
      await api.post('boletin/boletin/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    }

    closeModal();
    fetchNewsletters(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al guardar el boletín';
    console.error('Error:', err);
  }
};

// Funciones para modal de eliminación
const openDeleteModal = (id) => {
  currentNewsletterId.value = id;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
};

const confirmDelete = async () => {
  try {
    await api.delete(`boletin/boletin/${currentNewsletterId.value}/`);
    closeDeleteModal();
    fetchNewsletters(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al eliminar el boletín';
    console.error('Error:', err);
  }
};

// Cargar datos al montar el componente
onMounted(() => {
  fetchNewsletters();
});
</script>

<style scoped>
.img-thumbnail {
  transition: transform 0.2s;
}
.img-thumbnail:hover {
  transform: scale(1.05);
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-backdrop {
  opacity: 0.5;
}
</style>
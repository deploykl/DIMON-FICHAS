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
                      <th>Portada</th>
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
                          v-if="newsletter.imagen_principal_url" 
                          :src="newsletter.imagen_principal_url" 
                          alt="Portada del boletín" 
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
              
              <!-- Sección para múltiples imágenes -->
              <div class="mb-3">
                <label class="form-label">Imágenes</label>
                <input 
                  type="file" 
                  class="form-control mb-2" 
                  @change="handleImageUpload" 
                  multiple
                  accept="image/jpeg, image/png, image/gif"
                  ref="fileInput"
                >
                <small class="text-muted">Formatos aceptados: JPG, PNG, GIF. La primera imagen será la portada.</small>
                
                <!-- Vista previa de imágenes nuevas -->
                <div class="d-flex flex-wrap gap-2 mt-2">
                  <div v-for="(img, index) in newImages" :key="'new-'+index" class="position-relative">
                    <img :src="img.preview" class="img-thumbnail" style="width: 100px; height: 100px; object-fit: cover;">
                    <div class="position-absolute top-0 start-0 bg-info text-white px-1 small" v-if="index === 0">
                      Portada
                    </div>
                    <button @click="removeNewImage(index)" class="btn btn-danger btn-sm position-absolute top-0 end-0">
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
                
                <!-- Imágenes existentes -->
                <div class="d-flex flex-wrap gap-2 mt-3" v-if="formData.imagenes && formData.imagenes.length">
                  <div v-for="img in formData.imagenes" :key="img.id" class="position-relative">
                    <img :src="img.imagen_url" class="img-thumbnail" style="width: 100px; height: 100px; object-fit: cover;">
                    <div class="position-absolute top-0 start-0 bg-info text-white px-1 small" v-if="img.es_portada">
                      Portada
                    </div>
                    <button @click="removeExistingImage(img.id)" class="btn btn-danger btn-sm position-absolute top-0 end-0">
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="is_published" v-model="formData.is_published">
                <label class="form-check-label" for="is_published">Publicar</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="submitForm" :disabled="isSubmitting">
              <span v-if="isSubmitting">
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Procesando...
              </span>
              <span v-else>
                {{ isEditing ? 'Actualizar' : 'Guardar' }}
              </span>
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
            <button type="button" class="btn btn-danger" @click="confirmDelete" :disabled="isDeleting">
              <span v-if="isDeleting">
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Eliminando...
              </span>
              <span v-else>Eliminar</span>
            </button>
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
const isSubmitting = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const newImages = ref([]);
const fileInput = ref(null);

// Datos para modales
const showModal = ref(false);
const showDeleteModal = ref(false);
const isEditing = ref(false);
const currentNewsletterId = ref(null);

// Formulario
const formData = ref({
  titulo: '',
  contenido: '',
  is_published: false,
  imagenes: []
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
    is_published: newsletter.is_published,
    imagenes: newsletter.imagenes || []
  };
  newImages.value = [];
  currentNewsletterId.value = newsletter.id;
  isEditing.value = true;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleImageUpload = (event) => {
  const files = event.target.files;
  if (!files) return;
  
  newImages.value = []; // Limpiar imágenes anteriores
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const reader = new FileReader();
    
    reader.onload = (e) => {
      newImages.value.push({
        file: file,
        preview: e.target.result
      });
    };
    
    reader.readAsDataURL(file);
  }
  
  // Limpiar el input para permitir seleccionar las mismas imágenes otra vez
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const removeNewImage = (index) => {
  newImages.value.splice(index, 1);
};

const removeExistingImage = async (imageId) => {
  try {
    await api.delete(`boletin/boletin/${currentNewsletterId.value}/delete-image/${imageId}/`);
    formData.value.imagenes = formData.value.imagenes.filter(img => img.id !== imageId);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al eliminar la imagen';
    console.error('Error:', err);
  }
};

const resetForm = () => {
  formData.value = {
    titulo: '',
    contenido: '',
    is_published: false,
    imagenes: []
  };
  newImages.value = [];
  currentNewsletterId.value = null;
};

const submitForm = async () => {
  isSubmitting.value = true;
  error.value = null;
  
  try {
    // Primero guardar/actualizar el newsletter
    const newsletterData = {
      titulo: formData.value.titulo,
      contenido: formData.value.contenido,
      is_published: formData.value.is_published
    };

    let newsletter;
    if (isEditing.value) {
      newsletter = await api.put(`boletin/boletin/${currentNewsletterId.value}/`, newsletterData);
    } else {
      newsletter = await api.post('boletin/boletin/', newsletterData);
      currentNewsletterId.value = newsletter.data.id;
    }

    // Luego subir las imágenes si hay nuevas
    if (newImages.value.length > 0) {
      const formDataImages = new FormData();
      newImages.value.forEach((img, index) => {
        formDataImages.append('imagenes', img.file);
        // Si es la primera imagen, marcarla como portada
        if (index === 0) {
          formDataImages.append('es_portada', 'true');
        }
      });

      await api.post(
        `boletin/boletin/${currentNewsletterId.value}/upload-image/`,
        formDataImages,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
    }

    closeModal();
    await fetchNewsletters(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al guardar el boletín';
    console.error('Error:', err);
  } finally {
    isSubmitting.value = false;
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
  isDeleting.value = true;
  try {
    await api.delete(`boletin/boletin/${currentNewsletterId.value}/`);
    closeDeleteModal();
    await fetchNewsletters(currentPage.value);
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al eliminar el boletín';
    console.error('Error:', err);
  } finally {
    isDeleting.value = false;
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
  object-fit: cover;
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

.position-relative {
  transition: all 0.3s ease;
}

.position-relative:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.badge {
  font-size: 0.9em;
  padding: 0.35em 0.65em;
}

.btn-outline-primary, .btn-outline-danger {
  transition: all 0.2s;
}

.btn-outline-primary:hover {
  background-color: var(--bs-primary);
  color: white;
}

.btn-outline-danger:hover {
  background-color: var(--bs-danger);
  color: white;
}

.spinner-border {
  vertical-align: middle;
}
</style>
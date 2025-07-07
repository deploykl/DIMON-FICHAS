<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Boletines Informativos</h1>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <!-- Botón para crear nuevo boletín -->
              <router-link to="/newsletters/create" class="btn btn-primary mb-3">
                <i class="bi bi-plus-circle"></i> Nuevo Boletín
              </router-link>

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
                          <router-link 
                            :to="`/newsletters/edit/${newsletter.id}`" 
                            class="btn btn-sm btn-outline-primary"
                          >
                            <i class="bi bi-pencil"></i>
                          </router-link>
                          <button 
                            @click="deleteNewsletter(newsletter.id)" 
                            class="btn btn-sm btn-outline-danger"
                          >
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
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '@/components/services/auth_axios';

// Datos reactivos
const newsletters = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);

// Función para formatear fecha
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('es-ES', options);
};

// Función para obtener boletines
const fetchNewsletters = async (page = 1) => {
  try {
    const response = await api.get(`newsletters/?page=${page}`);
    newsletters.value = response.data.results;
    currentPage.value = page;
    totalPages.value = Math.ceil(response.data.count / 10); // Ajusta según tu paginación
  } catch (error) {
    console.error('Error fetching newsletters:', error);
  }
};

// Función para eliminar boletín
const deleteNewsletter = async (id) => {
  if (confirm('¿Estás seguro de eliminar este boletín?')) {
    try {
      await api.delete(`newsletters/${id}/`);
      fetchNewsletters(currentPage.value);
    } catch (error) {
      console.error('Error deleting newsletter:', error);
    }
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
</style>
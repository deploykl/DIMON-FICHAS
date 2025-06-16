<template>
  <main id="main" class="main">
    <div v-if="loading" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Cargando...
    </div>
    
    <template v-else>
      <div v-if="error" class="error-alert">
        <i class="fas fa-exclamation-triangle"></i> {{ error }}
      </div>
      
      <div v-else-if="!proceso" class="no-data">
        No se encontró el proceso con ID 1
      </div>
      
      <div v-else class="process-container">
        <div class="process-details">
          <h1>{{ proceso.nombre }}</h1>
          <div class="detail-item">
            <label>Nombre del Proceso:</label>
            <span>{{ proceso.nombre_proceso }}</span>
          </div>
          <div class="detail-item">
            <label>Dueño del Proceso:</label>
            <span>{{ proceso.dueño_proceso }}</span>
          </div>
          <div class="detail-item">
            <label>Objetivo:</label>
            <span>{{ proceso.objetivo }}</span>
          </div>
        </div>

        <!-- Subprocesos relacionados -->
        <div class="subprocesses-section">
    <h2>Subprocesos Relacionados</h2>
    <div v-if="loadingSubprocesos" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Cargando subprocesos...
    </div>
    <div v-else-if="subprocesosError" class="error-alert">
      <i class="fas fa-exclamation-triangle"></i> {{ subprocesosError }}
    </div>
    <div v-else-if="subprocesosFiltrados.length === 0" class="no-data">
      No hay subprocesos asociados a este proceso
    </div>
    <div v-else class="subprocess-list">
      <div v-for="subproceso in subprocesosFiltrados" :key="subproceso.id" class="subprocess-item">
        <h3>{{ subproceso.nombre }}</h3>
        <div class="detail-item">
          <label>Nivel:</label>
          <span>{{ subproceso.nivel }}</span>
        </div>
        <div class="detail-item">
          <label>Código:</label>
          <span>{{ subproceso.nombre.split(' ')[0] }}</span>
        </div>
      </div>
    </div>
  </div>

        <!-- Verificadores relacionados -->
        <div class="verifiers-section">
          <h2>Verificadores Relacionados</h2>
          <div v-if="loadingVerificadores" class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i> Cargando verificadores...
          </div>
          <div v-else-if="verificadoresError" class="error-alert">
            <i class="fas fa-exclamation-triangle"></i> {{ verificadoresError }}
          </div>
          <div v-else-if="filteredVerificadores.length === 0" class="no-data">
            No hay verificadores asociados a este proceso
          </div>
          <div v-else class="verifier-list">
            <div v-for="verificador in filteredVerificadores" :key="verificador.id" class="verifier-item">
              <h3>{{ verificador.nombre }}</h3>
              <div class="detail-item">
                <label>Tipo:</label>
                <span>{{ verificador.tipo }}</span>
              </div>
              <div class="detail-item">
                <label>Frecuencia:</label>
                <span>{{ verificador.frecuencia }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '@/components/services/auth_axios';

const proceso = ref(null);
const loading = ref(true);
const error = ref(null);

// Subprocesos
const subprocesos = ref([]);
const loadingSubprocesos = ref(false);
const subprocesosError = ref(null);

// Verificadores
const verificadores = ref([]);
const loadingVerificadores = ref(false);
const verificadoresError = ref(null);

// Computed para filtrar subprocesos
const subprocesosFiltrados = computed(() => {
  if (!proceso.value) return [];
  return subprocesos.value.filter(sub => sub.proceso === proceso.value.id);
});

// Filtrar verificadores por proceso_id = 1 (ajusta según tu modelo de datos)
const filteredVerificadores = computed(() => {
  return verificadores.value.filter(ver => ver.proceso_id === 1);
});

const fetchProceso = async () => {
  try {
    const response = await api.get('ficha/proceso/1/');
    proceso.value = response.data;
    
    // Cargar todos los subprocesos y verificadores
    await fetchAllSubprocesos();
    await fetchAllVerificadores();
  } catch (err) {
    error.value = err.response?.data?.detail || 
                 err.message || 
                 'Error al cargar el proceso';
    console.error('API Error:', err);
  } finally {
    loading.value = false;
  }
};

const fetchAllSubprocesos = async () => {
  try {
    loadingSubprocesos.value = true;
    subprocesosError.value = null;
    
    const response = await api.get('ficha/subproceso/');
    subprocesos.value = response.data.results || response.data;
  } catch (err) {
    subprocesosError.value = err.response?.data?.detail || 
                           err.message || 
                           'Error al cargar subprocesos';
    console.error('API Error (subprocesos):', err);
  } finally {
    loadingSubprocesos.value = false;
  }
};

const fetchAllVerificadores = async () => {
  try {
    loadingVerificadores.value = true;
    verificadoresError.value = null;
    
    const response = await api.get('ficha/verificador/');
    verificadores.value = response.data.results || response.data;
  } catch (err) {
    verificadoresError.value = err.response?.data?.detail || 
                             err.message || 
                             'Error al cargar verificadores';
    console.error('API Error (verificadores):', err);
  } finally {
    loadingVerificadores.value = false;
  }
};

onMounted(() => {
  fetchProceso();
});
</script>

<style scoped>
.main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-spinner {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-alert {
  padding: 15px;
  background: #ffebee;
  color: #c62828;
  border-radius: 4px;
  margin-bottom: 20px;
}

.no-data {
  padding: 20px;
  text-align: center;
  color: #666;
}

.process-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.process-details,
.subprocesses-section,
.verifiers-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.detail-item {
  margin-bottom: 15px;
}

.detail-item label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.detail-item span {
  display: block;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 4px;
}

h1, h2, h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

h1 {
  font-size: 1.8rem;
}

h2 {
  font-size: 1.5rem;
}

h3 {
  font-size: 1.2rem;
}

.subprocess-list,
.verifier-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.subprocess-item,
.verifier-item {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid #42b983;
}
</style>
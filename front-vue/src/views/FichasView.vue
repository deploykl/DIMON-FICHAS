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

        <!-- Formulario de IPRESS (solo una vez) -->
        <div class="ipress-form-section">
          <h2>Datos de la IPRESS</h2>
          <div class="ipress-form">
            <div class="form-group">
              <label>Tipo de IPRESS:</label>
              <select v-model="evaluacionData.tipo" class="form-control">
                <option value="EESS">Establecimiento de Salud</option>
                <option value="DIRIS">Dirección de Red Integrada de Salud</option>
                <option value="DIRESA">Dirección Regional de Salud</option>
                <option value="GERESA">Gerencia Regional de Salud</option>
              </select>
            </div>
            <div class="form-group">
              <label>Nombre de la IPRESS:</label>
              <input v-model="evaluacionData.establecimiento" type="text" class="form-control">
            </div>
            <div class="form-group">
              <label>Código de la IPRESS:</label>
              <input v-model="evaluacionData.codigo" type="text" class="form-control">
            </div>
            <div class="form-group">
              <label>Categoría:</label>
              <input v-model="evaluacionData.categoria" type="text" class="form-control">
            </div>
          </div>
        </div>

        <!-- Tabla de Subprocesos con sus Verificadores -->
        <div class="subprocess-verifiers-section">
          <h2>Subprocesos y sus Verificadores</h2>
          
          <div v-if="loadingSubprocesos || loadingVerificadores" class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i> Cargando datos...
          </div>
          
          <div v-else-if="subprocesosError || verificadoresError" class="error-alert">
            <i class="fas fa-exclamation-triangle"></i> 
            {{ subprocesosError || verificadoresError }}
          </div>
          
          <div v-else-if="subprocesosFiltrados.length === 0" class="no-data">
            No hay subprocesos asociados a este proceso
          </div>
          
          <div v-else class="subprocess-verifiers-table">
            <table>
              <thead>
                <tr>
                  <th>Subproceso</th>
                  <th>Verificadores</th>
                  <th>Evaluación</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subproceso in subprocesosFiltrados" :key="subproceso.id">
                  <td class="subprocess-cell">
                    <h3>{{ subproceso.nombre }}</h3>
                    <div class="subprocess-details">
                      <div><strong>Nivel:</strong> {{ subproceso.nivel }}</div>
                      <div><strong>Código:</strong> {{ subproceso.nombre.split(' ')[0] }}</div>
                    </div>
                  </td>
                  <td class="verifiers-cell">
                    <div v-if="getVerificadoresBySubproceso(subproceso.id).length === 0" class="no-verifiers">
                      No hay verificadores para este subproceso
                    </div>
                    <div v-else class="verifiers-list">
                      <div v-for="verificador in getVerificadoresBySubproceso(subproceso.id)" 
                           :key="verificador.id" 
                           class="verifier-item">
                        <div class="verifier-order">Verificador #{{ verificador.orden }}</div>
                        <div class="verifier-desc">{{ verificador.descripcion }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="evaluation-cell">
                    <div v-for="verificador in getVerificadoresBySubproceso(subproceso.id)" 
                         :key="verificador.id" 
                         class="evaluation-item">
                      <select v-model="evaluaciones[verificador.id].estado" class="form-control">
                        <option value="C">Cumple</option>
                        <option value="NC">No Cumple</option>
                        <option value="NA">No Aplica</option>
                      </select>
                      <textarea 
                        v-model="evaluaciones[verificador.id].observaciones" 
                        placeholder="Observaciones"
                        class="form-control"
                      ></textarea>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Botón de guardar -->
        <div class="form-actions">
          <button @click="submitEvaluaciones" class="btn-submit">
            Guardar Evaluación
          </button>
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

// Datos de evaluación
const evaluacionData = ref({
  tipo: 'EESS',
  establecimiento: '',
  codigo: '',
  categoria: ''
});

// Evaluaciones por verificador
const evaluaciones = ref({});

// Computed para filtrar subprocesos
const subprocesosFiltrados = computed(() => {
  if (!proceso.value) return [];
  return subprocesos.value.filter(sub => sub.proceso === proceso.value.id);
});

// Método para obtener verificadores por subproceso
const getVerificadoresBySubproceso = (subprocesoId) => {
  return verificadores.value.filter(ver => ver.subproceso === subprocesoId)
    .sort((a, b) => a.orden - b.orden);
};

// Inicializar evaluaciones para cada verificador
const initializeEvaluaciones = () => {
  // Limpiar evaluaciones existentes
  evaluaciones.value = {};
  
  // Solo inicializar para verificadores del proceso actual
  verificadores.value.forEach(verificador => {
    if (subprocesosFiltrados.value.some(sp => sp.id === verificador.subproceso)) {
      evaluaciones.value[verificador.id] = {
        estado: 'C',
        observaciones: ''
      };
    }
  });
};

const submitEvaluaciones = async () => {
  try {
    // Validar datos de IPRESS
    if (!evaluacionData.value.establecimiento || !evaluacionData.value.codigo || !evaluacionData.value.categoria) {
      alert('Por favor complete todos los datos de la IPRESS');
      return;
    }

    // Preparar datos para enviar
    const evaluacionesToSubmit = Object.keys(evaluaciones.value).map(verificadorId => {
      return {
        verificador: verificadorId,
        estado: evaluaciones.value[verificadorId].estado,
        observaciones: evaluaciones.value[verificadorId].observaciones,
        ...evaluacionData.value
      };
    });

    // Enviar cada evaluación (podrías optimizar esto con un endpoint batch si lo tienes)
    for (const evaluacion of evaluacionesToSubmit) {
      await api.post('ficha/evaluaciones/', evaluacion);
    }

    alert('Evaluaciones guardadas correctamente');
    
  } catch (err) {
    console.error('Error al guardar evaluaciones:', err);
    alert('Error al guardar las evaluaciones');
  }
};

const fetchProceso = async () => {
  try {
    const response = await api.get('ficha/proceso/1/');
    proceso.value = response.data;
    await fetchAllSubprocesos();
    await fetchAllVerificadores();
    initializeEvaluaciones();
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Error al cargar el proceso';
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
    subprocesosError.value = err.response?.data?.detail || err.message || 'Error al cargar subprocesos';
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
    initializeEvaluaciones(); // Esto ahora solo inicializará los relevantes
  } catch (err) {
    verificadoresError.value = err.response?.data?.detail || err.message || 'Error al cargar verificadores';
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

.process-details {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ipress-form-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ipress-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.subprocess-verifiers-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.subprocess-verifiers-table {
  margin-top: 20px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 15px;
  background-color: #f5f5f5;
  border-bottom: 2px solid #ddd;
}

td {
  padding: 15px;
  border-bottom: 1px solid #eee;
  vertical-align: top;
}

.subprocess-cell {
  width: 25%;
}

.verifiers-cell {
  width: 50%;
}

.evaluation-cell {
  width: 25%;
}

.subprocess-details {
  margin-top: 10px;
  font-size: 0.9em;
  color: #666;
}

.verifiers-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.verifier-item {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 4px;
  border-left: 3px solid #42b983;
}

.verifier-order {
  font-weight: bold;
  margin-bottom: 5px;
}

.verifier-desc {
  font-size: 0.9em;
}

.evaluation-item {
  margin-bottom: 15px;
}

.evaluation-item select {
  width: 100%;
  margin-bottom: 8px;
}

.evaluation-item textarea {
  width: 100%;
  min-height: 60px;
}

.no-verifiers {
  color: #999;
  font-style: italic;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-submit {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-submit:hover {
  background-color: #369f73;
}

h1, h2, h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

h1 {
  font-size: 1.8rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

h2 {
  font-size: 1.5rem;
}
</style>
<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Matriz de Compromiso</h1>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>

              <div v-else-if="matriz">
                <div class="mb-3">
                  <h5 class="card-title">Información de la Evaluación</h5>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Dependencia:</label>
                      <p>{{ matriz.evaluacion_data.tipo }} - {{ matriz.evaluacion_data.establecimiento }}</p>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Fecha del Monitoreo:</label>
                      <p>{{ formatDate(matriz.evaluacion_data.fecha_monitoreo) }}</p>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Nombre del Proceso:</label>
                      <p>{{ matriz.evaluacion_data.proceso_nombre }}</p>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Tipo de Proceso:</label>
                      <p>{{ matriz.evaluacion_data.categoria }}</p>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Dueño del Proceso:</label>
                      <p>{{ matriz.evaluacion_data.dueño_proceso }}</p>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-bold">Estado:</label>
                      <p>{{ matriz.evaluacion_data.estado }}</p>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-12">
                      <label class="form-label fw-bold">Subproceso:</label>
                      <p>{{ matriz.evaluacion_data.subproceso_nombre }}</p>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-12">
                      <label class="form-label fw-bold">Verificador:</label>
                      <p>{{ matriz.evaluacion_data.verificador_descripcion }}</p>
                    </div>
                  </div>
                </div>

                <hr>

                <h5 class="card-title">Matriz de Compromiso</h5>
                <form @submit.prevent="guardarMatriz">
                  <div class="row mb-3">
                    <div class="col-md-12">
                      <label class="form-label">Descripción del estado situacional del proceso</label>
                      <textarea v-model="matriz.descripcion_situacional" class="form-control" rows="3"></textarea>
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Semáforo</label>
                      <select v-model="matriz.semaforo" class="form-select">
                        <option value="Rojo">Rojo</option>
                        <option value="Amarillo">Amarillo</option>
                        <option value="Verde">Verde</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Identificación del Riesgo</label>
                      <textarea v-model="matriz.riesgo_identificado" class="form-control" rows="3"></textarea>
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Medidas correctivas/Compromisos</label>
                      <textarea v-model="matriz.medidas_correctivas" class="form-control" rows="3"></textarea>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Hito esperado</label>
                      <textarea v-model="matriz.hito_esperado" class="form-control" rows="3"></textarea>
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-4">
                      <label class="form-label">Responsable directo (A)</label>
                      <input v-model="matriz.responsable_directo" type="text" class="form-control">
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Plazo inicio</label>
                      <input v-model="matriz.plazo_inicio" type="date" class="form-control">
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Plazo fin</label>
                      <input v-model="matriz.plazo_fin" type="date" class="form-control">
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Funcionario del que depende directamente (B)</label>
                      <input v-model="matriz.funcionario_depen_directo" type="text" class="form-control">
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Funcionario del que depende indirectamente (C)</label>
                      <input v-model="matriz.funcionario_depen_indirecto" type="text" class="form-control">
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-12">
                      <label class="form-label">Firmas adicionales (máx. 5)</label>
                      <textarea v-model="matriz.firmas_adicionales" class="form-control" rows="2" placeholder="Ingrese nombres completos separados por comas"></textarea>
                    </div>
                  </div>

                  <!-- Componente para captura de firmas -->
                  <div class="row mb-3">
                    <div class="col-md-12">
                      <label class="form-label">Firmas:</label>
                      <div class="row">
                        <div class="col-md-4">
                          <h6>Responsable directo (A)</h6>
                          <signature-pad @save="setFirmaA" />
                        </div>
                        <div class="col-md-4">
                          <h6>Funcionario (B)</h6>
                          <signature-pad @save="setFirmaB" />
                        </div>
                        <div class="col-md-4">
                          <h6>Funcionario (C)</h6>
                          <signature-pad @save="setFirmaC" />
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="text-center">
                    <button type="submit" class="btn btn-primary">Guardar Matriz</button>
                  </div>
                </form>
              </div>

              <div v-else class="alert alert-danger">
                No se encontró la matriz de compromiso para esta evaluación.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import SignaturePad from '@/components/SignaturePad.vue'

const route = useRoute()
const loading = ref(true)
const matriz = ref(null)
const firmaA = ref(null)
const firmaB = ref(null)
const firmaC = ref(null)

const fetchMatriz = async () => {
  try {
    const evaluacionId = route.params.id
    const response = await axios.get(`/api/ficha/matriz-compromiso/por_evaluacion/?evaluacion_id=${evaluacionId}`)
    matriz.value = response.data
  } catch (error) {
    console.error('Error al cargar la matriz:', error)
  } finally {
    loading.value = false
  }
}

const guardarMatriz = async () => {
  try {
    loading.value = true
    const data = {
      ...matriz.value,
      firma_a: firmaA.value,
      firma_b: firmaB.value,
      firma_c: firmaC.value
    }
    
    if (matriz.value.id) {
      await axios.put(`/api/ficha/matriz-compromiso/${matriz.value.id}/`, data)
    } else {
      await axios.post('/api/ficha/matriz-compromiso/', data)
    }
    
    alert('Matriz guardada correctamente')
  } catch (error) {
    console.error('Error al guardar la matriz:', error)
    alert('Error al guardar la matriz')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const setFirmaA = (firma) => {
  firmaA.value = firma
}

const setFirmaB = (firma) => {
  firmaB.value = firma
}

const setFirmaC = (firma) => {
  firmaC.value = firma
}

onMounted(() => {
  fetchMatriz()
})
</script>

<style scoped>
.signature-container {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.signature-actions {
  margin-top: 10px;
}
</style>
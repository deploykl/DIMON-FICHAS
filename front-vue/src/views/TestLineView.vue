<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Listado de Matrices de Compromiso</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/">Inicio</router-link>
          </li>
          <li class="breadcrumb-item active">Matrices de Compromiso</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <!-- Filtros -->
              <div class="row mb-3">
                <div class="col-md-4">
                  <label class="form-label">Filtrar por establecimiento</label>
                  <input v-model="filtroEstablecimiento" type="text" class="form-control" placeholder="Nombre del establecimiento">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Filtrar por código</label>
                  <input v-model="filtroCodigo" type="text" class="form-control" placeholder="Código">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Filtrar por categoría</label>
                  <select v-model="filtroCategoria" class="form-select">
                    <option value="">Todas</option>
                    <option v-for="categoria in categoriasUnicas" :value="categoria">{{ categoria }}</option>
                  </select>
                </div>
              </div>

              <!-- Listado agrupado por monitor -->
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando matrices de compromiso...</p>
              </div>

              <div v-else>
                <div v-if="matricesAgrupadas.length === 0" class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  No se encontraron matrices de compromiso
                </div>

                <div v-for="grupo in matricesAgrupadas" :key="grupo.monitor" class="mb-5">
                  <h5 class="card-title border-bottom pb-2 mb-3">
                    <i class="fas fa-user-circle me-2"></i>
                    Monitor: <strong>{{ grupo.monitor }}</strong>
                    <span class="badge bg-primary ms-2">{{ grupo.matrices.length }} matriz(ces)</span>
                  </h5>

                  <div class="table-responsive">
                    <table class="table table-hover">
                      <thead>
                        <tr>
                          <th>Establecimiento</th>
                          <th>Código</th>
                          <th>Categoría</th>
                          <th>Semáforo</th>
                          <th>Fecha Creación</th>
                          <th>Verificadores NC</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="matriz in grupo.matrices" :key="matriz.id">
                          <td>{{ getEstablecimiento(matriz) }}</td>
                          <td>{{ getCodigo(matriz) }}</td>
                          <td>
                            <span class="badge" :class="getBadgeClass(getCategoria(matriz))">
                              {{ getCategoria(matriz) || 'N/A' }}
                            </span>
                          </td>
                          <td>
                            <span class="badge" :class="getSemaforoClass(matriz.semaforo)">
                              {{ matriz.semaforo }}
                            </span>
                          </td>
                          <td>{{ formatDate(matriz.fecha_creacion) }}</td>
                          <td>
                            <span class="badge bg-danger">
                              {{ getTotalNC(matriz) }} NC
                            </span>
                          </td>
                          <td>
                            <button @click="verDetalles(matriz)" class="btn btn-sm btn-outline-primary me-2" title="Ver detalles">
                              <i class="fas fa-eye"></i>
                            </button>
                            <router-link :to="`/matriz-compromiso/matriz/${matriz.id}`" class="btn btn-sm btn-outline-success me-2" title="Editar">
                              <i class="fas fa-edit"></i>
                            </router-link>
                            <button @click="exportarPDF(matriz.id)" class="btn btn-sm btn-outline-secondary" title="Exportar PDF">
                              <i class="fas fa-file-pdf"></i>
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para ver detalles -->
    <div v-if="matrizSeleccionada" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalles de Matriz de Compromiso</h5>
            <button type="button" class="btn-close" @click="matrizSeleccionada = null"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <h6><i class="fas fa-info-circle me-2"></i>Información General</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Establecimiento:</strong> {{ getEstablecimiento(matrizSeleccionada) }}</p>
                    <p><strong>Código:</strong> {{ getCodigo(matrizSeleccionada) }}</p>
                    <p><strong>Categoría:</strong> {{ getCategoria(matrizSeleccionada) }}</p>
                    <p><strong>Semáforo:</strong> 
                      <span class="badge" :class="getSemaforoClass(matrizSeleccionada.semaforo)">
                        {{ matrizSeleccionada.semaforo }}
                      </span>
                    </p>
                    <p><strong>Fecha Creación:</strong> {{ formatDate(matrizSeleccionada.fecha_creacion) }}</p>
                  </div>
                </div>

                <h6><i class="fas fa-clipboard-check me-2"></i>Compromisos</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Descripción situacional:</strong></p>
                    <p class="text-muted">{{ matrizSeleccionada.descripcion_situacional }}</p>
                    
                    <p><strong>Riesgo identificado:</strong></p>
                    <p class="text-muted">{{ matrizSeleccionada.riesgo_identificado }}</p>
                    
                    <p><strong>Medidas correctivas:</strong></p>
                    <p class="text-muted">{{ matrizSeleccionada.medidas_correctivas }}</p>
                    
                    <p><strong>Hito esperado:</strong></p>
                    <p class="text-muted">{{ matrizSeleccionada.hito_esperado }}</p>
                  </div>
                </div>
              </div>

              <div class="col-md-6">
                <h6><i class="fas fa-calendar-alt me-2"></i>Plazos</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Inicio:</strong> {{ formatDate(matrizSeleccionada.plazo_inicio) }}</p>
                    <p><strong>Fin:</strong> {{ formatDate(matrizSeleccionada.plazo_fin) }}</p>
                    <p><strong>Duración:</strong> {{ calcularDias(matrizSeleccionada.plazo_inicio, matrizSeleccionada.plazo_fin) }} días</p>
                  </div>
                </div>

                <h6><i class="fas fa-users me-2"></i>Responsables</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Responsable directo (A):</strong> {{ matrizSeleccionada.responsable_directo }}</p>
                    <div v-if="matrizSeleccionada.firma_a" class="text-center mb-3">
                      <img :src="matrizSeleccionada.firma_a" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Responsable Directo</p>
                    </div>

                    <p><strong>Funcionario (B):</strong> {{ matrizSeleccionada.funcionario_depen_directo }}</p>
                    <div v-if="matrizSeleccionada.firma_b" class="text-center mb-3">
                      <img :src="matrizSeleccionada.firma_b" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Funcionario B</p>
                    </div>

                    <p><strong>Funcionario (C):</strong> {{ matrizSeleccionada.funcionario_depen_indirecto }}</p>
                    <div v-if="matrizSeleccionada.firma_c" class="text-center mb-3">
                      <img :src="matrizSeleccionada.firma_c" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Funcionario C</p>
                    </div>

                    <div v-if="matrizSeleccionada.funcionario_d">
                      <p><strong>Funcionario (D):</strong> {{ matrizSeleccionada.funcionario_d }}</p>
                      <div v-if="matrizSeleccionada.firma_d" class="text-center mb-3">
                        <img :src="matrizSeleccionada.firma_d" class="img-fluid border rounded" style="max-height: 80px;">
                        <p class="small text-muted mt-1">Firma Funcionario D</p>
                      </div>
                    </div>

                    <div v-if="matrizSeleccionada.funcionario_e">
                      <p><strong>Funcionario (E):</strong> {{ matrizSeleccionada.funcionario_e }}</p>
                      <div v-if="matrizSeleccionada.firma_e" class="text-center mb-3">
                        <img :src="matrizSeleccionada.firma_e" class="img-fluid border rounded" style="max-height: 80px;">
                        <p class="small text-muted mt-1">Firma Funcionario E</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Verificadores No Conformes -->
            <h6><i class="fas fa-exclamation-triangle text-danger me-2"></i>Verificadores No Conformes ({{ getTotalNC(matrizSeleccionada) }})</h6>
            <div class="card border-0 shadow-sm">
              <div class="card-body">
                <div v-if="getTotalNC(matrizSeleccionada) === 0" class="alert alert-info">
                  No hay verificadores no conformes asociados a esta matriz
                </div>
                <div v-else class="accordion" id="accordionNC">
                  <div v-for="(nc, index) in getEvaluacionesNC(matrizSeleccionada)" :key="index" class="accordion-item mb-2">
                    <h2 class="accordion-header">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                        :data-bs-target="'#collapseNC-' + index" aria-expanded="false">
                        Verificador #{{ index + 1 }}: {{ getVerificadorNombre(nc) }}
                      </button>
                    </h2>
                    <div :id="'collapseNC-' + index" class="accordion-collapse collapse" data-bs-parent="#accordionNC">
                      <div class="accordion-body">
                        <p><strong>Subproceso:</strong> {{ getSubprocesoNombre(nc) }} ({{ getSubprocesoCodigo(nc) }})</p>
                        <p><strong>Observaciones:</strong> {{ nc.observaciones || 'Sin observaciones' }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="matrizSeleccionada = null">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="exportarPDF(matrizSeleccionada.id)">
              <i class="fas fa-file-pdf me-2"></i> Exportar PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/components/services/auth_axios'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'

const $toast = useToast()

// Estados
const loading = ref(true)
const matrices = ref([])
const matrizSeleccionada = ref(null)
const filtroEstablecimiento = ref('')
const filtroCodigo = ref('')
const filtroCategoria = ref('')

// Métodos para acceder a datos anidados de forma segura
const getEstablecimiento = (matriz) => {
  return matriz?.evaluacion_data?.establecimiento || 
         matriz?.evaluacion?.establecimiento || 
         'N/A'
}

const getCodigo = (matriz) => {
  // Primero verifica si hay datos directos en la matriz
  if (matriz?.codigo) return matriz.codigo;
  
  // Luego verifica evaluacion_data (expandido)
  if (matriz?.evaluacion_data?.codigo) return matriz.evaluacion_data.codigo;
  
  // Luego verifica la relación evaluacion (no expandida)
  if (matriz?.evaluacion?.codigo) return matriz.evaluacion.codigo;
  
  // Finalmente verifica en evaluacion si es un objeto (a veces la API devuelve el ID como string)
  if (typeof matriz?.evaluacion === 'object' && matriz.evaluacion?.codigo) {
    return matriz.evaluacion.codigo;
  }
  
  return 'N/A';
}

const getCategoria = (matriz) => {
  return matriz?.evaluacion_data?.categoria || 
         matriz?.evaluacion?.categoria || 
         'N/A'
}

const getMonitorNombre = (matriz) => {
  return matriz?.evaluacion_data?.monitor_nombre || 
         (matriz?.evaluacion?.usuario ? 
          `${matriz.evaluacion.usuario.first_name} ${matriz.evaluacion.usuario.last_name}` : 
          'Sin monitor asignado')
}

const getTotalNC = (matriz) => {
  return matriz?.evaluaciones_nc?.length || 0
}

const getEvaluacionesNC = (matriz) => {
  return matriz?.evaluaciones_nc || []
}

const getVerificadorNombre = (evaluacion) => {
  return evaluacion?.verificador_nombre || 
         evaluacion?.verificador?.descripcion || 
         'Verificador desconocido'
}

const getSubprocesoNombre = (evaluacion) => {
  return evaluacion?.subproceso_nombre || 
         evaluacion?.verificador?.subproceso?.nombre || 
         'Subproceso desconocido'
}

const getSubprocesoCodigo = (evaluacion) => {
  return evaluacion?.subproceso_codigo || 
         (evaluacion?.verificador?.subproceso ? 
          `PS${evaluacion.verificador.subproceso.proceso.id}.${evaluacion.verificador.subproceso.id}` : 
          'Código desconocido')
}

// Obtener matrices al montar el componente
onMounted(async () => {
  try {
    loading.value = true
    console.log("Iniciando carga de matrices...")
    
    const response = await api.get('ficha/matriz-compromiso/', {
      params: {
        expand: 'evaluacion,evaluacion.usuario,evaluaciones_nc.verificador.subproceso.proceso'
      }
    })
    
    console.log("Respuesta recibida:", response)
    
    if (response.data) {
      // Normalizar datos para manejar diferentes formatos de respuesta
      if (Array.isArray(response.data)) {
        matrices.value = response.data
      } else if (response.data.results) {
        matrices.value = response.data.results
      } else {
        matrices.value = [response.data]
      }
      
      //console.log("Matrices cargadas:", matrices.value)
    } else {
      console.error("La respuesta no contiene datos:", response)
      $toast.error("No se recibieron datos del servidor")
    }
  } catch (error) {
    console.error("Error al cargar matrices:", {
      message: error.message,
      response: error.response,
      stack: error.stack
    })
    
    let errorMessage = 'Error al cargar matrices'
    if (error.response) {
      if (error.response.status === 401) {
        errorMessage = 'No autorizado - Por favor inicie sesión'
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail
      }
    }
    
    $toast.error(errorMessage)
  } finally {
    loading.value = false
  }
})

// Agrupar matrices por monitor
const matricesAgrupadas = computed(() => {
  const agrupadas = {}
  
  matricesFiltradas.value.forEach(matriz => {
    const monitor = getMonitorNombre(matriz)
    
    if (!agrupadas[monitor]) {
      agrupadas[monitor] = {
        monitor,
        matrices: []
      }
    }
    
    agrupadas[monitor].matrices.push(matriz)
  })
  
  return Object.values(agrupadas)
})

// Filtrar matrices
const matricesFiltradas = computed(() => {
  return matrices.value.filter(matriz => {
    const establecimiento = getEstablecimiento(matriz).toLowerCase()
    const codigo = getCodigo(matriz).toLowerCase()
    const categoria = getCategoria(matriz)
    
    return (
      establecimiento.includes(filtroEstablecimiento.value.toLowerCase()) &&
      codigo.includes(filtroCodigo.value.toLowerCase()) &&
      (filtroCategoria.value === '' || categoria === filtroCategoria.value)
    )
  })
})

// Obtener categorías únicas para el filtro
const categoriasUnicas = computed(() => {
  const categorias = new Set()
  matrices.value.forEach(matriz => {
    const categoria = getCategoria(matriz)
    if (categoria) {
      categorias.add(categoria)
    }
  })
  return Array.from(categorias).sort()
})

// Métodos utilitarios
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const calcularDias = (inicio, fin) => {
  if (!inicio || !fin) return 0
  const start = new Date(inicio)
  const end = new Date(fin)
  const diff = end.getTime() - start.getTime()
  return Math.ceil(diff / (1000 * 3600 * 24)) + 1
}

const getBadgeClass = (categoria) => {
  if (!categoria) return 'bg-secondary'
  const categoriasColores = {
    'I-1': 'bg-primary',
    'I-2': 'bg-info',
    'I-3': 'bg-success',
    'I-4': 'bg-warning',
    'II-1': 'bg-danger',
    'II-2': 'bg-dark'
  }
  return categoriasColores[categoria] || 'bg-secondary'
}

const getSemaforoClass = (semaforo) => {
  const semaforos = {
    'Rojo': 'bg-danger',
    'Amarillo': 'bg-warning',
    'Verde': 'bg-success'
  }
  return semaforos[semaforo] || 'bg-secondary'
}

const verDetalles = (matriz) => {
  matrizSeleccionada.value = matriz
}

const exportarPDF = async (matrizId) => {
  try {
    const response = await api.get(
      `ficha/matriz-compromiso/${matrizId}/export_pdf/`,
      { responseType: 'blob' }
    )

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `matriz_compromiso_${matrizId}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    $toast.success('PDF generado correctamente')
  } catch (error) {
    console.error('Error al exportar PDF:', error)
    $toast.error('Error al generar el PDF')
  }
}
</script>

<style scoped>
.main {
  background-color: #f8f9fa;
}

.pagetitle {
  padding: 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.card {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.card-title {
  color: #012970;
  font-weight: 600;
}

.breadcrumb {
  background-color: transparent;
  padding: 0.5rem 0;
}

.breadcrumb-item.active {
  color: #899bbd;
}

.table th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.1);
  color: #012970;
}

.badge {
  font-weight: 500;
  padding: 5px 8px;
}

.modal-content {
  border-radius: 10px;
}

.img-fluid {
  max-height: 80px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-body {
    padding: 15px;
  }
  
  .table-responsive {
    overflow-x: auto;
  }
  
  .modal-dialog {
    margin: 0.5rem;
  }
}
</style>
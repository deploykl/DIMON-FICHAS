<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Matriz de Compromiso</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/">Inicio</router-link>
          </li>
          <li class="breadcrumb-item">
            <router-link to="/fichas/seleccion">Fichas</router-link>
          </li>
          <li class="breadcrumb-item active">Matriz de Compromiso</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>

              <div v-else>
                <!-- Mensaje cuando no existe matriz -->
                <div v-if="!matriz.id" class="alert alert-danger">
                  No se encontró la matriz de compromiso para esta evaluación.
                  <button @click="$router.back()" class="btn btn-sm btn-outline-danger ms-3">
                    Volver
                  </button>
                  <button @click="crearNuevaMatriz" class="btn btn-sm btn-primary ms-2">
                    <i class="fas fa-plus me-1"></i> Crear Nueva Matriz
                  </button>
                </div>

                <!-- Contenido cuando existe matriz -->
                <div v-else>
                  <!-- Sección de Verificadores No Conformes -->
                  <div v-if="matriz.evaluaciones_nc && matriz.evaluaciones_nc.length > 0" class="mb-4">
                    <h5 class="card-title">Verificadores No Conformes</h5>
                    <div class="alert alert-warning">
                      Se han identificado <strong>{{ matriz.evaluaciones_nc.length }}</strong> verificadores que no
                      cumplen
                      en <strong>{{new Set(matriz.evaluaciones_nc.map(nc => nc.subproceso_nombre)).size}}</strong>
                      subprocesos.
                    </div>

                    <div class="accordion" id="accordionNC">
                      <template v-for="(grupo, subproceso) in agruparPorSubproceso(matriz.evaluaciones_nc)"
                        :key="subproceso">
                        <div class="accordion-item mb-2 border">
                          <h2 class="accordion-header">
                            <button class="accordion-button collapsed bg-light" type="button" data-bs-toggle="collapse"
                              :data-bs-target="'#collapse' + slugify(subproceso)" aria-expanded="false">
                              <strong class="me-2">Subproceso:</strong> {{ subproceso }}
                            </button>
                          </h2>
                          <div :id="'collapse' + slugify(subproceso)" class="accordion-collapse collapse"
                            data-bs-parent="#accordionNC">
                            <div class="accordion-body p-2">
                              <div v-for="(nc, index) in grupo" :key="nc.id" class="mb-2 p-2 border-bottom">
                                <p class="mb-1"><strong>Verificador #{{ index + 1 }}:</strong> {{ nc.verificador_nombre }}
                                </p>
                                <span class="badge bg-danger">No Cumple</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>
                    </div>
                  </div>

                  <div class="mb-3">
                    <h5 class="card-title">Información de la Evaluación</h5>
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Dependencia:</label>
                        <p>{{ matriz.evaluacion_data?.tipo }} - {{ matriz.evaluacion_data?.establecimiento }}</p>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Fecha del Monitoreo:</label>
                        <p>{{ formatDate(matriz.evaluacion_data?.fecha_monitoreo) }}</p>
                      </div>
                    </div>
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Nombre del Proceso:</label>
                        <p>{{ matriz.evaluacion_data?.proceso_nombre }}</p>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Tipo de Proceso:</label>
                        <p>{{ matriz.evaluacion_data?.categoria }}</p>
                      </div>
                    </div>
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Dueño del Proceso:</label>
                        <p>{{ matriz.evaluacion_data?.dueño_proceso }}</p>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Monitor que generó la ficha:</label>
                        <p>{{ matriz.evaluacion_data?.monitor_nombre }}</p>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Estado:</label>
                        <p>{{ matriz.evaluacion_data?.estado }}</p>
                      </div>
                    </div>
                  </div>

                  <hr>

                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0">Matriz de Compromiso</h5>
                    <div>
                      <button @click="exportarPDF" class="btn btn-success">
                        <i class="fas fa-file-pdf me-2"></i> Exportar a PDF
                      </button>
                    </div>
                  </div>

                  <form @submit.prevent="guardarMatriz">
                    <!-- Resto del formulario... -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">Descripción del estado situacional del proceso</label>
                        <div class="input-group">
                          <textarea v-model="matriz.descripcion_situacional" class="form-control" rows="5"
                            required></textarea>
                          <button @click.prevent="generarDescripcion" class="btn btn-outline-primary" type="button"
                            :disabled="generandoDescripcion">
                            <template v-if="generandoDescripcion">
                              <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                              Generando...
                            </template>
                            <template v-else>
                              <i class="fas fa-robot me-2"></i> Ayuda con IA
                            </template>
                          </button>
                        </div>
                        <small class="text-muted">Presiona el botón para obtener ayuda con la descripción</small>
                      </div>
                    </div>

                    <!-- Resto de los campos del formulario... -->
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Semáforo</label>
                        <select v-model="matriz.semaforo" class="form-select" required>
                          <option value="Rojo">Rojo</option>
                          <option value="Amarillo">Amarillo</option>
                          <option value="Verde">Verde</option>
                        </select>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Identificación del Riesgo</label>
                        <textarea v-model="matriz.riesgo_identificado" class="form-control" rows="3" required></textarea>
                      </div>
                    </div>

                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Medidas correctivas/Compromisos</label>
                        <textarea v-model="matriz.medidas_correctivas" class="form-control" rows="3" required></textarea>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Hito esperado</label>
                        <textarea v-model="matriz.hito_esperado" class="form-control" rows="3" required></textarea>
                      </div>
                    </div>

                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Plazo inicio</label>
                        <input v-model="matriz.plazo_inicio" type="date" class="form-control" required>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Plazo fin</label>
                        <input v-model="matriz.plazo_fin" type="date" class="form-control" required>
                      </div>
                    </div>

                    <div class="row mb-3">
                      <div class="col-md-4">
                        <label class="form-label">Responsable directo (A)</label>
                        <input v-model="matriz.responsable_directo" type="text" class="form-control" required>
                        <small class="text-muted">Monitor que generó la ficha: {{ matriz.evaluacion_data?.monitor_nombre }}</small>
                      </div>
                      <div class="col-md-4">
                        <label class="form-label">Funcionario del que depende directamente (B)</label>
                        <input v-model="matriz.funcionario_depen_directo" type="text" class="form-control" required>
                      </div>
                      <div class="col-md-4">
                        <label class="form-label">Funcionario del que depende indirectamente (C)</label>
                        <input v-model="matriz.funcionario_depen_indirecto" type="text" class="form-control" required>
                      </div>
                    </div>

                    <!-- Firmas adicionales -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">Firmas adicionales (máx. 5)</label>
                        <textarea v-model="matriz.firmas_adicionales" class="form-control" rows="2"
                          placeholder="Ingrese nombres completos separados por comas"></textarea>

                        <button v-if="!showFuncionarioD && !matriz.funcionario_d" @click="showFuncionarioD = true" type="button"
                          class="btn btn-sm btn-outline-primary mt-2">
                          <i class="fas fa-plus me-1"></i> Agregar Funcionario D
                        </button>
                      </div>
                    </div>

                    <!-- Funcionario D -->
                    <div v-if="showFuncionarioD || matriz.funcionario_d" class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Funcionario (D)</label>
                        <input v-model="matriz.funcionario_d" type="text" class="form-control">
                      </div>
                      <div class="col-md-6">
                        <h6>Firma Funcionario (D)</h6>
                        <div v-if="matriz.firma_d" class="mb-3">
                          <img :src="matriz.firma_d" class="img-fluid border rounded" style="max-height: 150px;" />
                          <button @click="mostrarPadFirma('D')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                            <i class="fas fa-edit me-1"></i> Reemplazar
                          </button>
                          <button @click="limpiarFirma('D')" class="btn btn-sm btn-outline-danger mt-2">
                            <i class="fas fa-trash me-1"></i> Eliminar
                          </button>
                        </div>
                        <signature-pad v-else @save="setFirmaD" />
                        
                        <button v-if="!showFuncionarioE && !matriz.funcionario_e" @click="showFuncionarioE = true" type="button"
                          class="btn btn-sm btn-outline-primary mt-2">
                          <i class="fas fa-plus me-1"></i> Agregar Funcionario E
                        </button>
                      </div>
                    </div>

                    <!-- Funcionario E -->
                    <div v-if="showFuncionarioE || matriz.funcionario_e" class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Funcionario (E)</label>
                        <input v-model="matriz.funcionario_e" type="text" class="form-control">
                      </div>
                      <div class="col-md-6">
                        <h6>Firma Funcionario (E)</h6>
                        <div v-if="matriz.firma_e" class="mb-3">
                          <img :src="matriz.firma_e" class="img-fluid border rounded" style="max-height: 150px;" />
                          <button @click="mostrarPadFirma('E')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                            <i class="fas fa-edit me-1"></i> Reemplazar
                          </button>
                          <button @click="limpiarFirma('E')" class="btn btn-sm btn-outline-danger mt-2">
                            <i class="fas fa-trash me-1"></i> Eliminar
                          </button>
                        </div>
                        <signature-pad v-else @save="setFirmaE" />
                      </div>
                    </div>

                    <!-- Firmas principales -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">Firmas:</label>
                        <div class="row">
                          <!-- Firma A -->
                          <div class="col-md-4">
                            <h6>Responsable directo (A)</h6>
                            <div v-if="matriz.firma_a" class="mb-3">
                              <img :src="matriz.firma_a" class="img-fluid border rounded" style="max-height: 150px;" />
                              <button @click="mostrarPadFirma('A')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                                <i class="fas fa-edit me-1"></i> Reemplazar
                              </button>
                              <button @click="limpiarFirma('A')" class="btn btn-sm btn-outline-danger mt-2">
                                <i class="fas fa-trash me-1"></i> Eliminar
                              </button>
                            </div>
                            <signature-pad v-else @save="setFirmaA" />
                          </div>
                          
                          <!-- Firma B -->
                          <div class="col-md-4">
                            <h6>Funcionario (B)</h6>
                            <div v-if="matriz.firma_b" class="mb-3">
                              <img :src="matriz.firma_b" class="img-fluid border rounded" style="max-height: 150px;" />
                              <button @click="mostrarPadFirma('B')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                                <i class="fas fa-edit me-1"></i> Reemplazar
                              </button>
                              <button @click="limpiarFirma('B')" class="btn btn-sm btn-outline-danger mt-2">
                                <i class="fas fa-trash me-1"></i> Eliminar
                              </button>
                            </div>
                            <signature-pad v-else @save="setFirmaB" />
                          </div>
                          
                          <!-- Firma C -->
                          <div class="col-md-4">
                            <h6>Funcionario (C)</h6>
                            <div v-if="matriz.firma_c" class="mb-3">
                              <img :src="matriz.firma_c" class="img-fluid border rounded" style="max-height: 150px;" />
                              <button @click="mostrarPadFirma('C')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                                <i class="fas fa-edit me-1"></i> Reemplazar
                              </button>
                              <button @click="limpiarFirma('C')" class="btn btn-sm btn-outline-danger mt-2">
                                <i class="fas fa-trash me-1"></i> Eliminar
                              </button>
                            </div>
                            <signature-pad v-else @save="setFirmaC" />
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="text-center mt-4">
                      <button type="submit" class="btn btn-primary me-2" :disabled="saving">
                        <template v-if="saving">
                          <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                          Guardando...
                        </template>
                        <template v-else>
                          <i class="fas fa-save me-2"></i> Guardar Matriz
                        </template>
                      </button>
                      <button type="button" @click="cancelar" class="btn btn-secondary">
                        <i class="fas fa-times me-2"></i> Cancelar
                      </button>
                    </div>
                  </form>
                </div>
              </div>

              <!-- Modal para reemplazar firmas -->
              <div v-if="showSignatureModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Reemplazar Firma {{firmaActual}}</h5>
                      <button type="button" class="btn-close" @click="cerrarModalFirma"></button>
                    </div>
                    <div class="modal-body">
                      <signature-pad ref="signaturePad" @save="guardarFirmaReemplazo" />
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModalFirma">Cancelar</button>
                      <button type="button" class="btn btn-primary" @click="guardarFirmaDesdeModal">Guardar Firma</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios'
import SignaturePad from '@/components/SignaturePad.vue'
import { useToast } from 'vue-toast-notification'
import { generateText } from '@/components/services/gemini'
import 'vue-toast-notification/dist/theme-sugar.css'

const route = useRoute()
const router = useRouter()
const $toast = useToast()

const loading = ref(true)
const saving = ref(false)
const generandoDescripcion = ref(false)
const matriz = ref({
  evaluacion: null,
  descripcion_situacional: '',
  semaforo: 'Rojo',
  riesgo_identificado: '',
  medidas_correctivas: '',
  hito_esperado: '',
  plazo_inicio: '',
  plazo_fin: '',
  responsable_directo: '',
  funcionario_depen_directo: '',
  funcionario_depen_indirecto: '',
  firmas_adicionales: '',
  firma_a: null,
  firma_b: null,
  firma_c: null,
  firma_d: null,
  firma_e: null
})

const firmaA = ref(null)
const firmaB = ref(null)
const firmaC = ref(null)
const firmaD = ref(null)
const firmaE = ref(null)
const showFuncionarioD = ref(false)
const showFuncionarioE = ref(false)

// Variables para el modal de firmas
const showSignatureModal = ref(false)
const firmaActual = ref('')
const signaturePad = ref(null)

// Métodos auxiliares
const agruparPorSubproceso = (evaluaciones) => {
  return evaluaciones.reduce((acc, nc) => {
    const subproceso = nc.subproceso_nombre;
    if (!acc[subproceso]) {
      acc[subproceso] = [];
    }
    acc[subproceso].push(nc);
    return acc;
  }, {});
};

const slugify = (text) => {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

// Función para convertir data URL a Blob
const dataURLtoBlob = (dataURL) => {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new Blob([u8arr], { type: mime });
};

// Métodos para manejar firmas
const mostrarPadFirma = async (tipo) => {
  firmaActual.value = tipo;
  showSignatureModal.value = true;

  // Espera a que el modal se renderice
  await nextTick()

  // Limpia el pad de firmas
  if (signaturePad.value && signaturePad.value.clearSignature) {
    signaturePad.value.clearSignature()
  }
};

const cerrarModalFirma = () => {
  showSignatureModal.value = false;
};

const guardarFirmaDesdeModal = () => {
  if (signaturePad.value && signaturePad.value.saveSignature) {
    signaturePad.value.saveSignature();
  }
};

const guardarFirmaReemplazo = (firma) => {
  if (!firma || !firmaActual.value) return;

  const firmaProp = `firma_${firmaActual.value.toLowerCase()}`;
  const firmaRef = `firma${firmaActual.value}`;

  // Actualiza tanto la ref reactiva como la propiedad en matriz.value
  if (firmaRef in { firmaA, firmaB, firmaC, firmaD, firmaE }) {
    eval(`${firmaRef}.value = firma`);
  }
  matriz.value[firmaProp] = firma;

  showSignatureModal.value = false;
};

const setFirmaA = (firma) => {
  firmaA.value = firma;
  matriz.value.firma_a = firma;
}
const setFirmaB = (firma) => {
  firmaB.value = firma;
  matriz.value.firma_b = firma;
}
const setFirmaC = (firma) => {
  firmaC.value = firma;
  matriz.value.firma_c = firma;
}
const setFirmaD = (firma) => {
  firmaD.value = firma;
  matriz.value.firma_d = firma;
}
const setFirmaE = (firma) => {
  firmaE.value = firma;
  matriz.value.firma_e = firma;
}

const limpiarFirma = (tipo) => {
  const firmaProp = `firma_${tipo.toLowerCase()}`;
  const firmaRef = `firma${tipo}`;

  if (firmaRef in { firmaA, firmaB, firmaC, firmaD, firmaE }) {
    eval(`${firmaRef}.value = null`);
  }
  matriz.value[firmaProp] = null;

  // Si es D o E, oculta la sección si no hay datos
  if (tipo === 'D' && !matriz.value.funcionario_d) {
    showFuncionarioD.value = false;
  }
  if (tipo === 'E' && !matriz.value.funcionario_e) {
    showFuncionarioE.value = false;
  }
}

// Métodos principales
const generarDescripcion = async () => {
  try {
    generandoDescripcion.value = true;
    const textoExistente = matriz.value.descripcion_situacional || '';

    const prompt = `Como experto en redacción técnica profesional, toma la siguiente descripción y conviértela en un texto formal, estructurado y técnicamente preciso, adecuado para un documento oficial de gestión de procesos. 
    Mantén la esencia pero mejora la redacción, estructura y terminología técnica. Si el texto está vacío, genera una descripción técnica estándar basada en los verificadores no conformes.
    
    Texto original: "${textoExistente}"
    
    Verificadores no conformes: ${JSON.stringify(matriz.value.evaluaciones_nc?.map(nc => nc.verificador_nombre) || 'No especificados')}
    
    Proceso: ${matriz.value.evaluacion_data?.proceso_nombre || 'No especificado'}
    
    Devuelve SOLO el texto mejorado, sin comentarios adicionales.`;

    const descripcionGenerada = await generateText(prompt);
    matriz.value.descripcion_situacional = descripcionGenerada.trim()
      .replace(/^"+|"+$/g, '')
      .replace(/\\n/g, '\n');

    $toast.success('Descripción técnica generada con éxito');
  } catch (error) {
    console.error('Error al generar descripción técnica:', error);
    let errorMsg = 'Error al generar la descripción técnica';
    if (error.message.includes('model')) errorMsg = 'Error: Modelo no disponible. Intente con "gemini-1.5-pro"';
    else if (error.message.includes('API_KEY')) errorMsg = 'Error de configuración con la API de Gemini';
    $toast.error(errorMsg);
  } finally {
    generandoDescripcion.value = false;
  }
};

const fetchData = async () => {
  try {
    loading.value = true;
    const matrizResponse = await api.get(`ficha/matriz-compromiso/${route.params.id}/`);

    if (matrizResponse.data) {
      // Asignar todos los datos de la matriz
      matriz.value = {
        ...matriz.value, // Mantener los valores por defecto
        ...matrizResponse.data, // Sobrescribir con los datos del servidor
        firma_a: matrizResponse.data.firma_a || null,
        firma_b: matrizResponse.data.firma_b || null,
        firma_c: matrizResponse.data.firma_c || null,
        firma_d: matrizResponse.data.firma_d || null,
        firma_e: matrizResponse.data.firma_e || null
      };

      // Mostrar campos D y E si tienen datos
      if (matriz.value.funcionario_d) showFuncionarioD.value = true;
      if (matriz.value.funcionario_e) showFuncionarioE.value = true;

      // Asignar firmas a las variables reactivas
      firmaA.value = matriz.value.firma_a;
      firmaB.value = matriz.value.firma_b;
      firmaC.value = matriz.value.firma_c;
      firmaD.value = matriz.value.firma_d;
      firmaE.value = matriz.value.firma_e;

      // Obtener datos de evaluación si no están incluidos
      if (!matriz.value.evaluacion_data && matriz.value.evaluacion) {
        const evaluacionResponse = await api.get(`ficha/evaluaciones/${matriz.value.evaluacion}/`);
        matriz.value.evaluacion_data = evaluacionResponse.data;
      }
    } else {
      // Si no hay matriz, crear una nueva asociada a la evaluación
      matriz.value.evaluacion = route.params.id;
    }
  } catch (error) {
    console.error('Error al cargar datos:', error);
    $toast.error('Error al cargar la matriz de compromiso');
    // Crear matriz vacía asociada a la evaluación
    matriz.value.evaluacion = route.params.id;
  } finally {
    loading.value = false;
  }
};

const guardarMatriz = async () => {
  try {
    saving.value = true;

    // Validación de campos requeridos
    if (!matriz.value.descripcion_situacional || !matriz.value.riesgo_identificado ||
      !matriz.value.medidas_correctivas || !matriz.value.hito_esperado ||
      !matriz.value.responsable_directo || !matriz.value.plazo_inicio ||
      !matriz.value.plazo_fin || !matriz.value.funcionario_depen_directo ||
      !matriz.value.funcionario_depen_indirecto) {
      $toast.warning('Por favor complete todos los campos requeridos');
      return;
    }

    // Crear FormData para enviar archivos
    const formData = new FormData();

    // Agregar todos los campos de la matriz
    for (const key in matriz.value) {
      if (key.startsWith('firma_')) continue;
      if (matriz.value[key] !== null && matriz.value[key] !== undefined) {
        formData.append(key, matriz.value[key]);
      }
    }

    // Agregar las firmas como archivos
    const firmas = {
      'firma_a': firmaA.value,
      'firma_b': firmaB.value,
      'firma_c': firmaC.value,
      'firma_d': firmaD.value,
      'firma_e': firmaE.value
    };

    for (const [key, value] of Object.entries(firmas)) {
      if (value) {
        // Si es una URL (firma existente), no la volvemos a enviar
        if (typeof value === 'string' && (value.startsWith('http') || value.startsWith('/'))) {
          formData.append(key, value);
        } else {
          const blob = dataURLtoBlob(value);
          formData.append(key, blob, `${key}.png`);
        }
      } else {
        formData.append(key, '');
      }
    }

    const config = {
      headers: { 'Content-Type': 'multipart/form-data' }
    };

    if (matriz.value.id) {
      await api.put(`ficha/matriz-compromiso/${matriz.value.id}/`, formData, config);
      $toast.success('Matriz actualizada correctamente');
    } else {
      const response = await api.post('ficha/matriz-compromiso/', formData, config);
      matriz.value.id = response.data.id;
      $toast.success('Matriz creada correctamente');
    }

    // Recargar datos para asegurar consistencia
    await fetchData();
  } catch (error) {
    console.error('Error al guardar la matriz:', error);
    $toast.error('Error al guardar la matriz');
  } finally {
    saving.value = false;
  }
};

const exportarPDF = async () => {
  try {
    if (!matriz.value?.id) {
      $toast.warning('Debe guardar la matriz antes de exportar');
      return;
    }

    const response = await api.get(
      `ficha/matriz-compromiso/${matriz.value.id}/export_pdf/`,
      { responseType: 'blob' }
    );

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `matriz_compromiso_${matriz.value.id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error al exportar PDF:', error);
    $toast.error('Error al generar el PDF');
  }
};

const cancelar = () => {
  router.back();
}

onMounted(() => {
  fetchData();
});
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

.card-title {
  color: #012970;
}

.breadcrumb {
  background-color: transparent;
  padding: 0.5rem 0;
}

.breadcrumb-item.active {
  color: #899bbd;
}

.form-label {
  font-weight: 500;
}

.btn-export {
  background-color: #2ecc71;
  border-color: #2ecc71;
}

.btn-export:hover {
  background-color: #27ae60;
  border-color: #27ae60;
}

.input-group-text {
  cursor: pointer;
  transition: all 0.3s;
}

.input-group-text:hover {
  background-color: #e9ecef;
}

.btn-add-signer {
  margin-top: 10px;
  margin-bottom: 15px;
}

.additional-signer-fields {
  border-left: 3px solid #0d6efd;
  padding-left: 15px;
  margin-top: 10px;
  margin-bottom: 20px;
}

/* Estilos para las imágenes de firma */
.firma-img-container {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  text-align: center;
}

.firma-img {
  max-height: 120px;
  display: block;
  margin: 0 auto;
  border: 1px solid #eee;
}

.firma-actions {
  margin-top: 10px;
  display: flex;
  gap: 5px;
  justify-content: center;
}

/* Estilos para el modal de firma */
.modal {
  z-index: 1060;
}

.modal-backdrop {
  opacity: 0.5 !important;
}
</style>
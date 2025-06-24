<template>
    <main id="main" class="container py-4">
        <!-- Breadcrumb -->
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <router-link to="/fichas">Fichas</router-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                    {{ proceso?.nombre || 'Cargando...' }}
                </li>
            </ol>
        </nav>
        <!-- Botón para generar PDF -->
        <div class="d-flex justify-content-end mb-3">
            <button @click="generatePdf" class="btn btn-danger">
                <i class="fas fa-file-pdf me-2"></i> Generar PDF
            </button>
        </div>

        <!-- Componente PDF (oculto visualmente) -->
        <div style="position: absolute; left: -9999px;">
            <pdf-generator ref="pdfGenerator" :proceso="proceso" :subprocesos="subprocesos"
                :verificadores="verificadores" :evaluaciones="evaluaciones" :evaluacion-data="evaluacionData" />
        </div>


        <!-- Contenido de la Ficha -->
        <template v-if="proceso">
            <!-- Información del Proceso -->
            <div class="card mb-4 shadow-sm">
                <div class="card-body">
                    <h1 class="card-title border-bottom pb-2 mb-4">{{ proceso.titulo }}</h1>
                    <h3 class="h4 mb-4">{{ proceso.nombre }}</h3>

                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded">
                                <p class="mb-1"><strong>Nombre del Proceso:</strong></p>
                                <p class="mb-0">{{ proceso.nombre_proceso }}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded">
                                <p class="mb-1"><strong>Dueño del Proceso:</strong></p>
                                <p class="mb-0">{{ proceso.dueño_proceso }}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded">
                                <p class="mb-1"><strong>Objetivo:</strong></p>
                                <p class="mb-0">{{ proceso.objetivo }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Formulario de IPRESS -->
  <!-- Formulario de IPRESS -->
  <div class="card mb-4 shadow-sm">
    <div class="card-body">
      <h2 class="card-title h4 mb-4">Datos de la IPRESS</h2>
      <div class="row g-3">
        <div class="col-md-3">
          <label class="form-label">Tipo de IPRESS:</label>
          <select v-model="evaluacionData.tipo" class="form-select" required>
            <option value="EESS">Establecimiento de Salud</option>
            <option value="DIRIS">Dirección de Red Integrada de Salud</option>
            <option value="DIRESA">Dirección Regional de Salud</option>
            <option value="GERESA">Gerencia Regional de Salud</option>
          </select>
        </div>

        <!-- Búsqueda por Nombre -->
        <div class="col-md-3 position-relative">
          <label class="form-label">Nombre de la IPRESS:</label>
          <input 
            v-model="evaluacionData.establecimiento" 
            type="text" 
            class="form-control" 
            required
            @input="(e) => handleIpressSearch('nombre', e)"
            @focus="showNameSuggestions = true"
            @blur="hideNameSuggestions"
          >
          <div v-if="isSearchingByName" class="position-absolute top-50 end-0 translate-middle-y me-2">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          </div>
          <div v-if="showNameSuggestions && nameResults.length > 0" class="suggestions-dropdown">
            <div 
              v-for="item in nameResults" 
              :key="item.COD_IPRESS" 
              class="suggestion-item"
              @mousedown="selectIpress(item)"
            >
              <div class="fw-bold">{{ item.NOMBRE }}</div>
              <div class="small text-muted">
                <span>Código: {{ item.COD_IPRESS }}</span> |
                <span>Categoría: {{ item.CATEGORIA }}</span>
              </div>
              <div class="small text-muted">
                {{ item.DEPARTAMENTO }} > {{ item.PROVINCIA }} > {{ item.DISTRITO }} - {{ item.DISA }} - {{ item.INSTITUCION }}
              </div>
            </div>
          </div>
          <div v-if="showNameSuggestions && nameResults.length === 0 && !isSearchingByName" 
               class="suggestions-dropdown">
            <div class="p-3 text-muted">No se encontraron resultados</div>
          </div>
        </div>

        <!-- Búsqueda por Código -->
        <div class="col-md-3 position-relative">
          <label class="form-label">Código de la IPRESS:</label>
          <input 
            v-model="evaluacionData.codigo" 
            type="text" 
            class="form-control" 
            required
            @keypress="soloNumeros"
            @input="(e) => handleIpressSearch('codigo', e)"
            @focus="showCodeSuggestions = true"
            @blur="hideCodeSuggestions"
          >
          <div v-if="isSearchingByCode" class="position-absolute top-50 end-0 translate-middle-y me-2">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          </div>
          <div v-if="showCodeSuggestions && codeResults.length > 0" class="suggestions-dropdown">
            <div 
              v-for="item in codeResults" 
              :key="item.COD_IPRESS" 
              class="suggestion-item"
              @mousedown="selectIpress(item)"
            >
              <div class="fw-bold">{{ item.NOMBRE }}</div>
              <div class="small text-muted">
                <span>Código: {{ item.COD_IPRESS }}</span> |
                <span>Categoría: {{ item.CATEGORIA }}</span>
              </div>
              <div class="small text-muted">
                {{ item.DEPARTAMENTO }} > {{ item.PROVINCIA }} > {{ item.DISTRITO }}
              </div>
            </div>
          </div>
          <div v-if="showCodeSuggestions && codeResults.length === 0 && !isSearchingByCode" 
               class="suggestions-dropdown">
            <div class="p-3 text-muted">No se encontraron resultados</div>
          </div>
        </div>

        <!-- Resto de campos (se autocompletarán) -->
        <div class="col-md-3">
          <label class="form-label">Categoría:</label>
          <input v-model="evaluacionData.categoria" type="text" class="form-control" required readonly>
        </div>

        <div class="col-md-3">
          <label class="form-label">Departamento:</label>
          <input v-model="evaluacionData.departamento" type="text" class="form-control" readonly>
        </div>

        <div class="col-md-3">
          <label class="form-label">Provincia:</label>
          <input v-model="evaluacionData.provincia" type="text" class="form-control" readonly>
        </div>

        <div class="col-md-3">
          <label class="form-label">Distrito:</label>
          <input v-model="evaluacionData.distrito" type="text" class="form-control" readonly>
        </div>

        <div class="col-md-3">
          <label class="form-label">DISA:</label>
          <input v-model="evaluacionData.disa" type="text" class="form-control" readonly>
        </div>
        
        <div class="col-md-3">
          <label class="form-label">Institución:</label>
          <input v-model="evaluacionData.institucion" type="text" class="form-control" readonly>
        </div>
      </div>
    </div>
  </div>

            <!-- Tabla de Subprocesos con Verificadores -->
            <div class="card mb-4 shadow-sm">
                <div class="card-body">
                    <h2 class="card-title h4 mb-4">Subprocesos y Verificadores</h2>

                    <div v-if="loadingSubprocesos || loadingVerificadores" class="text-center py-3">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Cargando...</span>
                        </div>
                        <p class="mt-2">Cargando subprocesos y verificadores...</p>
                    </div>

                    <div v-else-if="subprocesosError || verificadoresError" class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        {{ subprocesosError || verificadoresError }}
                    </div>

                    <div v-else-if="subprocesosFiltrados.length === 0" class="alert alert-info">
                        No hay subprocesos asociados a este proceso
                    </div>

                    <div v-else class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th style="width: 25%">Subproceso</th>
                                    <th style="width: 60%">Verificadores</th>
                                    <th style="width: 15%">Evaluación</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="subproceso in subprocesosFiltrados" :key="subproceso.id">
                                    <td>
                                        <h3 class="h6 mb-1">{{ subproceso.nombre }}</h3>
                                        <div class="small text-muted">
                                            <div><strong>Nivel:</strong> {{ subproceso.nivel }}</div>
                                            <div><strong>Código:</strong> {{ subproceso.nombre.split(' ')[0] }}</div>
                                        </div>
                                    </td>
                                    <td colspan="2">
                                        <div v-if="getVerificadoresBySubproceso(subproceso.id).length === 0"
                                            class="text-muted fst-italic">
                                            No hay verificadores para este subproceso
                                        </div>
                                        <div v-for="verificador in getVerificadoresBySubproceso(subproceso.id)"
                                            :key="verificador.id"
                                            class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded">
                                            <div>
                                                <div class="fw-bold">Verificador #{{ verificador.orden }}</div>
                                                <div class="small">{{ verificador.descripcion }}</div>
                                            </div>
                                            <select v-model="getEvaluacion(verificador.id).estado"
                                                class="form-select form-select-sm" style="width: 120px">
                                                <option value="C">Cumple</option>
                                                <option value="NC">No Cumple</option>
                                                <option value="NA">No Aplica</option>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Botón de guardar -->
            <div class="d-flex justify-content-between mb-4">
                <button @click="resetForm" class="btn btn-outline-secondary">
                    <i class="fas fa-sync-alt me-2"></i> Reiniciar
                </button>
                <button @click="submitEvaluaciones" class="btn btn-primary" :disabled="saving">
                    <template v-if="saving">
                        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Guardando...
                    </template>
                    <template v-else>
                        <i class="fas fa-save me-2"></i> Guardar Evaluación
                    </template>
                </button>
            </div>

            <!-- Modal para generación de matriz -->
            <div class="modal fade" id="matrizModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header" :class="{
                            'bg-success': todosCumplen || soloCumplen,
                            'bg-primary': !todosCumplen && !soloCumplen
                        }">
                            <h5 class="modal-title text-white">
                                {{ todosCumplen ? 'Resultado de la Evaluación' :
                                    soloCumplen ? 'Evaluaciones que cumplen' :
                                        'Evaluaciones que no cumplen' }}
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div v-if="todosCumplen" class="alert alert-success">
                                <i class="fas fa-check-circle me-2"></i>
                                ¡Todos los verificadores cumplen con los requisitos!
                            </div>

                            <p v-if="!todosCumplen && totalVerificadoresNoCumplen > 0">
                                Se han identificado <strong>{{ totalVerificadoresNoCumplen }}</strong> verificadores que
                                no cumplen en <strong>{{ subprocesosNoCumplen.length }}</strong> subprocesos.
                            </p>

                            <p v-if="!todosCumplen && totalVerificadoresCumplen > 0">
                                Se han identificado <strong>{{ totalVerificadoresCumplen }}</strong> verificadores que
                                cumplen con observaciones en <strong>{{ subprocesosCumplen.length }}</strong>
                                subprocesos.
                            </p>

                            <!-- Tablas de resultados (mostrar solo si no es el caso de todos cumplen) -->
                            <template v-if="!todosCumplen">
                                <!-- Tabla para verificadores que no cumplen -->
                                <div v-if="totalVerificadoresNoCumplen > 0" class="table-responsive mb-4">
                                    <table class="table table-hover">
                                        <thead>
                                            <tr>
                                                <th>Subproceso</th>
                                                <th>Verificadores que no cumplen</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="subproceso in subprocesosNoCumplen" :key="subproceso.id">
                                                <td>
                                                    <strong>{{ subproceso.nombre }}</strong>
                                                    <div class="small text-muted">
                                                        Nivel: {{ subproceso.nivel }} |
                                                        Código: {{ subproceso.nombre.split(' ')[0] }}
                                                    </div>
                                                </td>
                                                <td>
                                                    <ul class="list-unstyled mb-0">
                                                        <li v-for="verificador in getVerificadoresNoCumplen(subproceso.id)"
                                                            :key="verificador.id" class="mb-1">
                                                            Verificador #{{ verificador.orden }}: {{
                                                                verificador.descripcion }}
                                                        </li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <!-- Tabla para verificadores que cumplen con observaciones -->
                                <div v-if="totalVerificadoresCumplen > 0" class="table-responsive mb-4">
                                    <table class="table table-hover">
                                        <thead>
                                            <tr>
                                                <th>Subproceso</th>
                                                <th>Verificadores que cumplen con observaciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="subproceso in subprocesosCumplen" :key="subproceso.id">
                                                <td>
                                                    <strong>{{ subproceso.nombre }}</strong>
                                                    <div class="small text-muted">
                                                        Nivel: {{ subproceso.nivel }} |
                                                        Código: {{ subproceso.nombre.split(' ')[0] }}
                                                    </div>
                                                </td>
                                                <td>
                                                    <ul class="list-unstyled mb-0">
                                                        <li v-for="verificador in getVerificadoresCumplen(subproceso.id)"
                                                            :key="verificador.id" class="mb-1">
                                                            Verificador #{{ verificador.orden }}: {{
                                                                verificador.descripcion }}
                                                        </li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </template>

                            <div class="alert" :class="{
                                'alert-success': todosCumplen,
                                'alert-info': soloCumplen && !todosCumplen,
                                'alert-warning': !soloCumplen && !todosCumplen
                            }">
                                <i class="fas fa-info-circle me-2"></i>
                                <span v-if="todosCumplen">
                                    Puede generar una matriz de compromiso para documentar el cumplimiento total.
                                </span>
                                <span v-else-if="!soloCumplen">
                                    Puede generar una matriz de compromiso que incluya todos los verificadores que no
                                    cumplen.
                                </span>
                                <span v-else>
                                    Puede generar una matriz de compromiso que incluya todos los verificadores que
                                    cumplen con
                                    observaciones.
                                </span>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                            <button type="button" class="btn btn-success" @click="continuarSinMatriz">
                                Continuar sin generar matriz
                            </button>
                            <button @click="generarMatrizCompleta" class="btn" :class="{
                                'btn-success': todosCumplen || soloCumplen,
                                'btn-primary': !todosCumplen && !soloCumplen
                            }">
                                <i class="fas fa-file-alt me-2"></i>
                                {{ todosCumplen ? 'Generar Matriz de Cumplimiento' :
                                    soloCumplen ? 'Generar Matriz de Seguimiento' :
                                        'Generar Matriz Completa' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </main>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { api } from '@/components/services/auth_axios';
import { useRoute, useRouter } from 'vue-router';
import { Modal } from 'bootstrap';
import { useToast } from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';
import PdfGenerator from '@/components/widgets/PdfGenerator.vue';

const route = useRoute();
const router = useRouter();
const $toast = useToast();

// Datos del proceso seleccionado
const proceso = ref(null);
const error = ref(null);

// Subprocesos y verificadores
const subprocesos = ref([]);
const loadingSubprocesos = ref(false);
const subprocesosError = ref(null);
const verificadores = ref([]);
const loadingVerificadores = ref(false);
const verificadoresError = ref(null);
const pdfGenerator = ref(null);
// Variables reactivas para búsqueda
const nameResults = ref([]);
const codeResults = ref([]);
const showNameSuggestions = ref(false);
const showCodeSuggestions = ref(false);
const isSearchingByName = ref(false);
const isSearchingByCode = ref(false);
const ipressResults = ref([]);
// Variables reactivas adicionales
const showSuggestions = ref(false);
const isSearching = ref(false);
// Datos de evaluación
const evaluacionData = ref({
    tipo: 'EESS',
    establecimiento: '',
    codigo: '',
    categoria: '',
    departamento: '',
    provincia: '',
    distrito: '',
    disa: '',
    institucion: ''
});
const soloNumeros = (event) => {
  const charCode = event.keyCode || event.which;
  const charStr = String.fromCharCode(charCode);
  
  // Permitir solo dígitos (0-9) y teclas de control (backspace, delete, etc.)
  if (!/^\d+$/.test(charStr)) {
    event.preventDefault();
  }
};
const generatePdf = () => {
    if (pdfGenerator.value) {
        pdfGenerator.value.generatePdf();
    }
};
// Evaluaciones por verificador
const evaluaciones = ref({});
const saving = ref(false);
const evaluacionesNoCumplen = ref([]);
let matrizModal = null;


// Método para buscar IPRESS por nombre o código
const searchIpress = async (type, inputValue) => {
    if (!inputValue) return [];
    
    if (type === 'nombre') isSearchingByName.value = true;
    else isSearchingByCode.value = true;

    try {
        const params = new URLSearchParams();
        params.append('limit', '10');
        
        if (type === 'nombre') {
            params.append('q', inputValue);
        } else {
            // Validar que sea un número válido
            const codigo = parseInt(inputValue);
            if (isNaN(codigo)) return [];
            
            // Enviar como filtro exacto
            params.append('COD_IPRESS', codigo.toString());
        }

        const response = await api.get('ficha/renipress/', {
            params,
            paramsSerializer: params => params.toString()
        });

        // Verificar respuesta y mapear resultados
        if (!response.data?.result?.records) return [];
        
        return response.data.result.records.map(item => ({
            ...item,
            COD_IPRESS: item.COD_IPRESS?.toString() || '',
            CATEGORIA: item.CATEGORIA || 'Sin categoría',
            DEPARTAMENTO: item.DEPARTAMENTO || 'Sin departamento',
            PROVINCIA: item.PROVINCIA || 'Sin provincia',
            DISTRITO: item.DISTRITO || 'Sin distrito',
            DISA: item.DISA || 'Sin DISA',
            INSTITUCION: item.INSTITUCION || 'Sin Institución'
        }));

    } catch (error) {
        console.error('Error en búsqueda:', error);
        $toast.error('Error al buscar IPRESS');
        return [];
    } finally {
        if (type === 'nombre') isSearchingByName.value = false;
        else isSearchingByCode.value = false;
    }
};
// Seleccionar IPRESS
const selectIpress = (item) => {
    evaluacionData.value = {
        ...evaluacionData.value,
        establecimiento: item.NOMBRE,
        codigo: item.COD_IPRESS,
        categoria: item.CATEGORIA,
        departamento: item.DEPARTAMENTO || '',
        provincia: item.PROVINCIA || '',
        distrito: item.DISTRITO || '',
        disa: item.DISA || '',
        institucion: item.INSTITUCION || ''
    };
    showNameSuggestions.value = false;
    showCodeSuggestions.value = false;
};
// Método para buscar IPRESS
// Manejar búsqueda con debounce
const handleIpressSearch = debounce(async (type, event) => {
    const inputValue = event.target.value.trim();
    
    if (type === 'codigo' && inputValue.length < 1) {
        codeResults.value = [];
        return;
    }
    if (type === 'nombre' && inputValue.length < 2) {
        nameResults.value = [];
        return;
    }

    const results = await searchIpress(type, inputValue);
    
    if (type === 'nombre') {
        nameResults.value = results;
    } else {
        codeResults.value = results;
    }
}, 300);

// Ocultar sugerencias con retraso
const hideNameSuggestions = () => {
    setTimeout(() => {
        showNameSuggestions.value = false;
    }, 200);
};

const hideCodeSuggestions = () => {
    setTimeout(() => {
        showCodeSuggestions.value = false;
    }, 200);
};

// Función debounce
function debounce(fn, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), delay);
    };
}
// Computed properties
const todosCumplen = computed(() => {
    if (!verificadores.value || verificadores.value.length === 0) return false;
    return Object.values(evaluaciones.value).every(evaluacion => evaluacion.estado === 'C');
});

const totalVerificadoresCumplen = computed(() => {
    if (!verificadores.value) return 0;
    return Object.keys(evaluaciones.value).filter(verificadorId => {
        return evaluaciones.value[verificadorId]?.estado === 'C' &&
            evaluaciones.value[verificadorId]?.observaciones;
    }).length;
});
// Método para obtener la evaluación de forma segura
const getEvaluacion = (verificadorId) => {
    if (!evaluaciones.value[verificadorId]) {
        evaluaciones.value[verificadorId] = {
            estado: 'C',  // Valor por defecto: Cumple
            observaciones: ''
        };
    }
    return evaluaciones.value[verificadorId];
};
const subprocesosCumplen = computed(() => {
    if (!subprocesosFiltrados.value || !verificadores.value) return [];
    return subprocesosFiltrados.value.filter(subproceso => {
        return getVerificadoresBySubproceso(subproceso.id).some(verificador => {
            return evaluaciones.value[verificador.id]?.estado === 'C' &&
                evaluaciones.value[verificador.id]?.observaciones;
        });
    });
});

const soloCumplen = computed(() => {
    return totalVerificadoresNoCumplen.value === 0 && totalVerificadoresCumplen.value > 0;
});

const subprocesosNoCumplen = computed(() => {
    if (!subprocesosFiltrados.value || !verificadores.value) return [];
    return subprocesosFiltrados.value.filter(subproceso => {
        return getVerificadoresBySubproceso(subproceso.id).some(verificador => {
            return evaluaciones.value[verificador.id]?.estado === 'NC';
        });
    });
});

const totalVerificadoresNoCumplen = computed(() => {
    if (!verificadores.value) return 0;
    return Object.keys(evaluaciones.value).filter(verificadorId => {
        return evaluaciones.value[verificadorId]?.estado === 'NC';
    }).length;
});

// Computed para filtrar subprocesos
const subprocesosFiltrados = computed(() => {
    if (!proceso.value) return [];
    return subprocesos.value.filter(sub => sub.proceso === proceso.value.id);
});

// Métodos
const getVerificadoresCumplen = (subprocesoId) => {
    return getVerificadoresBySubproceso(subprocesoId).filter(verificador => {
        return evaluaciones.value[verificador.id]?.estado === 'C' &&
            evaluaciones.value[verificador.id]?.observaciones;
    });
};

const getVerificadoresNoCumplen = (subprocesoId) => {
    return getVerificadoresBySubproceso(subprocesoId).filter(verificador => {
        return evaluaciones.value[verificador.id]?.estado === 'NC';
    });
};

// En el método que genera la matriz
const generarMatrizCompleta = async () => {
    try {
        if (matrizModal) {
            matrizModal.hide();
        }

        // Enviar TODAS las evaluaciones, no solo las NC
        const evaluacionesIds = evaluacionesNoCumplen.value.map(e => e.id);

        // Crear la matriz en el backend
        const response = await api.post('ficha/matriz-compromiso/generar_completa/', {
            evaluaciones_ids: evaluacionesIds
        });

        // Redirigir usando el ID de la matriz
        router.push(`/matriz-compromiso/matriz/${response.data.id}`);

    } catch (error) {
        console.error('Error al generar matriz completa:', error);
        $toast.error(error.response?.data?.error || 'Error al generar la matriz');
    }
};

// Método para obtener verificadores por subproceso
const getVerificadoresBySubproceso = (subprocesoId) => {
    return verificadores.value.filter(ver => ver.subproceso === subprocesoId)
        .sort((a, b) => a.orden - b.orden);
};

// Modificar el método initializeEvaluaciones para que sea más robusto
const initializeEvaluaciones = () => {
    evaluaciones.value = {};
    if (verificadores.value && verificadores.value.length > 0) {
        verificadores.value.forEach(verificador => {
            if (subprocesosFiltrados.value.some(sp => sp.id === verificador.subproceso)) {
                evaluaciones.value[verificador.id] = {
                    estado: 'C',  // Valor por defecto: Cumple
                    observaciones: ''
                };
            }
        });
    }
};


// Resetear formulario
const resetForm = () => {
    evaluacionData.value = {
        tipo: 'EESS',
        establecimiento: '',
        codigo: '',
        categoria: '',
        departamento: '',
        provincia: '',
        distrito: '',
        disa: '',
        institucion: ''
    };
    initializeEvaluaciones();
};

// Guardar evaluaciones
const submitEvaluaciones = async () => {
    try {
        saving.value = true;

        // Validar datos de IPRESS
        if (!evaluacionData.value.establecimiento || !evaluacionData.value.codigo || !evaluacionData.value.categoria) {
            $toast.warning('Por favor complete todos los datos de la IPRESS');
            return;
        }

        const evaluacionesToSubmit = Object.keys(evaluaciones.value).map(verificadorId => {
            return {
                verificador: verificadorId,
                estado: evaluaciones.value[verificadorId].estado,
                observaciones: evaluaciones.value[verificadorId].observaciones || '',
                ...evaluacionData.value,
                proceso: proceso.value.id
            };
        });

        // Enviar todas las evaluaciones
        const responses = await Promise.all(
            evaluacionesToSubmit.map(evaluacion =>
                api.post('ficha/evaluaciones/', evaluacion)
            )
        );

        // Guardar todas las evaluaciones para mostrar en el modal
        evaluacionesNoCumplen.value = responses.map(res => res.data);

        // Siempre mostrar el modal, independientemente del estado
        matrizModal.show();

    } catch (err) {
        console.error('Error al guardar evaluaciones:', err);
        $toast.error('Error al guardar las evaluaciones');
    } finally {
        saving.value = false;
    }
};

// Continuar sin generar matrices
const continuarSinMatriz = () => {
    if (matrizModal) {
        matrizModal.hide();
    }
    $toast.success('Evaluaciones guardadas correctamente');
    router.push('/fichas/seleccion');
};

// Cargar todos los subprocesos
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

// Cargar todos los verificadores
const fetchAllVerificadores = async () => {
    try {
        loadingVerificadores.value = true;
        verificadoresError.value = null;

        const response = await api.get('ficha/verificador/');
        verificadores.value = response.data.results || response.data;
        initializeEvaluaciones();

    } catch (err) {
        verificadoresError.value = err.response?.data?.detail || err.message || 'Error al cargar verificadores';
        console.error('API Error (verificadores):', err);
    } finally {
        loadingVerificadores.value = false;
    }
};

// Cargar proceso por ID
const loadProcesoById = async (procesoId) => {
    try {
        error.value = null;

        // Cargar proceso
        const procesoResponse = await api.get(`ficha/proceso/${procesoId}/`);
        proceso.value = procesoResponse.data;

        // Cargar subprocesos y verificadores
        await Promise.all([fetchAllSubprocesos(), fetchAllVerificadores()]);

    } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Error al cargar el proceso';
        console.error('API Error:', err);
    }
};

// Inicializar modal al montar el componente
onMounted(async () => {
    // Si viene con ID en la ruta, cargar directamente
    if (route.params.id) {
        await loadProcesoById(route.params.id);
    }

    // Inicializar modal después de que todo esté cargado
    nextTick(() => {
        const modalElement = document.getElementById('matrizModal');
        if (modalElement) {
            matrizModal = new Modal(modalElement);
        }
    });
});
</script>

<style scoped>
.breadcrumb {
    background-color: transparent;
    padding: 0;
}

.card {
    border: none;
    border-radius: 0.5rem;
}

.table th {
    font-weight: 600;
    background-color: #f8f9fa;
}

.bg-light {
    background-color: #f8f9fa !important;
}

.form-select-sm {
    max-width: 150px;
}

.modal-header {
    padding: 1rem 1.5rem;
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    padding: 1rem 1.5rem;
}

.suggestions-dropdown {
    position: absolute;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    background: white;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    z-index: 1050;
    margin-top: 2px;
}

.suggestion-item {
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:last-child {
    border-bottom: none;
}

.suggestion-item:hover {
    background-color: #f8f9fa;
}

.suggestion-item .fw-bold {
    font-size: 0.9rem;
}

.suggestion-item .small {
    font-size: 0.8rem;
    line-height: 1.3;
}

.position-relative {
    position: relative;
}
</style>
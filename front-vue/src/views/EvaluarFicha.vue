<template>
    <main id="main" class="container py-4">
        <!-- Breadcrumb y botón de volver -->
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <router-link to="/fichas/seleccion">Fichas</router-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                    {{ proceso?.nombre || 'Cargando...' }}
                </li>
            </ol>
        </nav>

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
            <div class="card mb-4 shadow-sm">
                <div class="card-body">
                    <h2 class="card-title h4 mb-4">Datos de la IPRESS</h2>
                    <div class="row g-3">
                        <div class="col-md-3">
                            <label class="form-label">Tipo de IPRESS:</label>
                            <select v-model="evaluacionData.tipo" class="form-select">
                                <option value="EESS">Establecimiento de Salud</option>
                                <option value="DIRIS">Dirección de Red Integrada de Salud</option>
                                <option value="DIRESA">Dirección Regional de Salud</option>
                                <option value="GERESA">Gerencia Regional de Salud</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Nombre de la IPRESS:</label>
                            <input v-model="evaluacionData.establecimiento" type="text" class="form-control">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Código de la IPRESS:</label>
                            <input v-model="evaluacionData.codigo" type="text" class="form-control">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Categoría:</label>
                            <input v-model="evaluacionData.categoria" type="text" class="form-control">
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
                            <span class="visually-hidden">Cargando datos...</span>
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
                                    <td>
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
                                            <template v-if="evaluaciones[verificador.id]">
                                                <select v-model="evaluaciones[verificador.id].estado"
                                                    class="form-select form-select-sm" style="width: 120px">
                                                    <option value="C">Cumple</option>
                                                    <option value="NC">No Cumple</option>
                                                    <option value="NA">No Aplica</option>
                                                </select>
                                            </template>
                                            <template v-else>
                                                <div class="text-danger small">Cargando...</div>
                                            </template>
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
        </template>
    </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '@/components/services/auth_axios';
import { useRoute } from 'vue-router';

const route = useRoute();

// Datos para selección
const categorias = ref([]);
const selectedCategory = ref(null);
const procesos = ref([]);
const selectedProceso = ref(null);
const loading = ref(true);

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

// Datos de evaluación
const evaluacionData = ref({
    tipo: 'EESS',
    establecimiento: '',
    codigo: '',
    categoria: ''
});

// Evaluaciones por verificador
const evaluaciones = ref({});
const saving = ref(false);

// Computed para filtrar procesos por categoría
const procesosFiltrados = computed(() => {
    if (!selectedCategory.value) return [];
    return procesos.value.filter(p => p.categoria === selectedCategory.value);
});

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
        categoria: ''
    };
    initializeEvaluaciones();
};

// Guardar evaluaciones
const submitEvaluaciones = async () => {
    try {
        saving.value = true;

        // Validar datos de IPRESS
        if (!evaluacionData.value.establecimiento || !evaluacionData.value.codigo || !evaluacionData.value.categoria) {
            alert('Por favor complete todos los datos de la IPRESS');
            return;
        }

        const evaluacionesToSubmit = Object.keys(evaluaciones.value).map(verificadorId => {
            return {
                verificador: verificadorId,
                estado: evaluaciones.value[verificadorId].estado,
                observaciones: evaluaciones.value[verificadorId].observaciones,
                ...evaluacionData.value
            };
        });

        // Enviar todas las evaluaciones
        const promises = evaluacionesToSubmit.map(evaluacion =>
            api.post('ficha/evaluaciones/', evaluacion)
        );

        await Promise.all(promises);
        alert('Evaluaciones guardadas correctamente');

    } catch (err) {
        console.error('Error al guardar evaluaciones:', err);
        alert('Error al guardar las evaluaciones');
    } finally {
        saving.value = false;
    }
};

// Cargar categorías y procesos
const fetchInitialData = async () => {
    try {
        const [catResponse, procResponse] = await Promise.all([
            api.get('ficha/categoria/'),
            api.get('ficha/proceso/')
        ]);

        categorias.value = catResponse.data;
        procesos.value = procResponse.data;

    } catch (err) {
        error.value = 'Error al cargar los datos iniciales';
        console.error('Error:', err);
    }
};

// Cargar procesos por categoría
const fetchProcesosByCategory = async () => {
    try {
        if (!selectedCategory.value) return;

        loading.value = true;
        const response = await api.get('ficha/proceso/', {
            params: { categoria_id: selectedCategory.value }
        });

        procesos.value = response.data;
        selectedProceso.value = null;
        proceso.value = null;

    } catch (err) {
        error.value = 'Error al cargar procesos';
        console.error('Error:', err);
    } finally {
        loading.value = false;
    }
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

// Cargar datos de un proceso específico
const loadProcesoData = async () => {
    if (!selectedProceso.value) return;
    await loadProcesoById(selectedProceso.value);
};

// Cargar proceso por ID
const loadProcesoById = async (procesoId) => {
    try {
        loading.value = true;
        error.value = null;

        // Cargar proceso
        const procesoResponse = await api.get(`ficha/proceso/${procesoId}/`);
        proceso.value = procesoResponse.data;
        selectedCategory.value = proceso.value.categoria;

        // Cargar subprocesos y verificadores
        await Promise.all([fetchAllSubprocesos(), fetchAllVerificadores()]);

    } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Error al cargar el proceso';
        console.error('API Error:', err);
    } finally {
        loading.value = false;
    }
};

// Cargar datos iniciales al montar el componente
onMounted(async () => {
    await fetchInitialData();

    // Si viene con ID en la ruta, cargar directamente
    if (route.params.id) {
        await loadProcesoById(route.params.id);
    }
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
</style>
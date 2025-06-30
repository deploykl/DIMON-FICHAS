<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Listado de Alertas</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Nueva Alerta
      </button>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Alertas Registradas</h5>

              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>Código</th>
                      <th>Tipo</th>
                      <th>Descripción</th>
                      <th>Fecha Creación</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="alerta in alertas" :key="alerta.id">
                      <td>{{ alerta.codigo }}</td>
                      <td>
                        <span :class="`badge bg-${getBadgeColor(alerta.tipo)}`">
                          {{ alerta.tipo }}
                        </span>
                      </td>
                      <td>{{ alerta.descripcion }}</td>
                      <td>{{ formatDateTime(alerta.fecha_creacion) }}</td>
                      <td>
                        <button @click="verSeguimientos(alerta.id)" class="btn btn-sm btn-info me-1">
                          <i class="fas fa-history"></i> Seguimientos
                        </button>
                        <button @click="openEditModal(alerta)" class="btn btn-sm btn-warning me-1">
                          <i class="bi bi-pencil"></i> Editar
                        </button>
                        <button @click="openDeleteModal(alerta)" class="btn btn-sm btn-danger">
                          <i class="bi bi-trash"></i> Eliminar
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
    </section>

    <!-- Modal para Crear Alerta -->
    <div class="modal fade" :class="{ 'show': showCreateModal }" tabindex="-1" style="display: block;"
      v-if="showCreateModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Crear Nueva Alerta</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="crearAlerta">
              <div class="mb-3">
                <label class="form-label">Tipo</label>
                <select v-model="nuevaAlerta.tipo" class="form-select" required>
                  <option value="">Seleccione un tipo</option>
                  <option value="Urgente">Urgente</option>
                  <option value="Importante">Importante</option>
                  <option value="Informativa">Informativa</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea v-model="nuevaAlerta.descripcion" class="form-control" rows="3" required></textarea>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showCreateModal = false">Cancelar</button>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Guardar</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal"></div>

    <!-- Modal para Editar Alerta -->
    <div class="modal fade" :class="{ 'show': showEditModal }" tabindex="-1" style="display: block;"
      v-if="showEditModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar Alerta</h5>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="actualizarAlerta">
              <div class="mb-3">
                <label class="form-label">Código</label>
                <input v-model="alertaEditada.codigo" class="form-control" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Tipo</label>
                <select v-model="alertaEditada.tipo" class="form-select" required>
                  <option value="Urgente">Urgente</option>
                  <option value="Importante">Importante</option>
                  <option value="Informativa">Informativa</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea v-model="alertaEditada.descripcion" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Fecha Creación</label>
                <input v-model="alertaEditada.fecha_creacion" class="form-control" disabled>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showEditModal = false">Cancelar</button>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Guardar Cambios</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showEditModal"></div>

    <!-- Modal para Eliminar Alerta -->
    <div class="modal fade" :class="{ 'show': showDeleteModal }" tabindex="-1" style="display: block;"
      v-if="showDeleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar Eliminación</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas eliminar la alerta <strong>{{ alertaAEliminar.codigo }}</strong>?</p>
            <p class="text-muted">Tipo: {{ alertaAEliminar.tipo }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="eliminarAlerta" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
              <span v-else>Eliminar</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showDeleteModal"></div>

    <!-- Modal de Seguimientos para Alertas -->
    <div v-if="showSeguimientosAlertaModal" class="modal fade show d-block"
      style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="fas fa-history me-2"></i>
              Seguimientos - {{ alertaSeguimientos.alertaData ? alertaSeguimientos.alertaData.codigo : 'N/A' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="cerrarModalesAlerta"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingSeguimientosAlerta" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-2">Cargando información de seguimientos...</p>
            </div>

            <div v-else>
              <!-- Sección de Información de la Alerta -->
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h6 class="mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    Información de la Alerta
                  </h6>
                </div>
                <div class="card-body">
                  <div class="row">
                    <!-- Columna Izquierda - Información General -->
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="fw-bold">Código:</label>
                        <p>{{ alertaSeguimientos.alertaData?.codigo || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Tipo:</label>
                        <p><span :class="`badge bg-${getBadgeColor(alertaSeguimientos.alertaData?.tipo)}`">
                            {{ alertaSeguimientos.alertaData?.tipo || 'N/A' }}
                          </span></p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Usuario que generó:</label>
                        <p>{{ alertaSeguimientos.alertaData?.usuario || 'N/A' }}</p>
                      </div>
                    </div>

                    <!-- Columna Derecha - Descripción -->
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="fw-bold">Descripción:</label>
                        <p class="text-muted">{{ alertaSeguimientos.alertaData?.descripcion || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Fecha de creación:</label>
                        <p>{{ formatDateTime(alertaSeguimientos.alertaData?.fecha_creacion) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sección de Historial de Seguimientos -->
              <div class="card">
                <div class="card-header bg-light d-flex justify-content-between align-items-center">
                  <h6 class="mb-0">
                    <i class="fas fa-list-ol me-2"></i>
                    Historial de Seguimientos (Total: {{ alertaSeguimientos.seguimientos?.length || 0 }})
                  </h6>
                  <button @click="nuevoSeguimientoAlerta(alertaSeguimientos.id)" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus me-1"></i> Nuevo Seguimiento
                  </button>
                </div>

                <div class="card-body">
                  <div v-if="alertaSeguimientos.seguimientos?.length > 0">
                    <div class="table-responsive">
                      <table class="table table-hover table-bordered">
                        <thead class="table-light">
                          <tr>
                            <th width="80">#</th>
                            <th>Fecha creación</th>
                            <th>Plazo Seguimiento</th>
                            <th>Estado</th>
                            <th>Registrado por</th>
                            <th>Descripción</th>
                            <th width="120">Acciones</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(seguimiento, index) in alertaSeguimientos.seguimientos"
                            :key="'seg-alerta-' + index" :class="getEstadoSeguimientoBgClass(seguimiento.estado)">
                            <td class="fw-bold">{{ index + 1 }}</td>
                            <td>{{ formatDateTime(seguimiento.fecha_creacion) }}</td>
                            <td>{{ formatDateTime(seguimiento.fecha_seguimiento) }}</td>
                            <td>
                              <span class="badge" :class="getEstadoSeguimientoClass(seguimiento.estado)">
                                {{ getEstadoSeguimientoDisplay(seguimiento.estado) }}
                              </span>
                            </td>
                            <td>{{ seguimiento.usuario_nombre || 'N/A' }}</td>
                            <!-- Por esto: -->
                            <td>
                              <div>
                                {{ seguimiento.analisis_accion || 'Sin descripción' }}
                              </div>
                            </td>
                            <td>
                              <button @click="editarSeguimientoAlerta(seguimiento.id)"
                                class="btn btn-sm btn-outline-primary me-1" title="Editar">
                                <i class="fas fa-edit"></i>
                              </button>

                            </td>
                          </tr>
                          <!-- Fila de detalles expandible -->
                          <tr v-for="(seguimiento, index) in alertaSeguimientos.seguimientos"
                            :key="'detail-alerta-' + index" class="collapse" :id="'detailsSegAlerta-' + index">
                            <td colspan="6" class="bg-light">
                              <div class="p-3">
                                <div class="row">
                                  <div class="col-md-12 mb-3">
                                    <label class="fw-bold">Análisis/Acción:</label>
                                    <p class="text-muted">{{ seguimiento.analisis_accion || 'Sin descripción' }}</p>
                                  </div>

                                  <div class="col-md-12 mb-3" v-if="seguimiento.observaciones">
                                    <label class="fw-bold">Observaciones:</label>
                                    <p class="text-muted">{{ seguimiento.observaciones }}</p>
                                  </div>
                                </div>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div v-else class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay seguimientos registrados para esta alerta
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalesAlerta">
              <i class="fas fa-times me-1"></i> Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Editar/Crear Seguimiento de Alerta -->
    <div v-if="showEditarSeguimientoAlertaModal" class="modal fade show d-block"
      style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ seguimientoAlertaEditando?.isNew ? 'Nuevo Seguimiento' : 'Editar Seguimiento' }}
            </h5>
            <button type="button" class="btn-close" @click="cerrarModalesAlerta"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarSeguimientoAlerta">
              <!-- Por este componente personalizado -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Fecha</label>
                  <input v-model="fechaPart" type="date" class="form-control" required
                    :min="new Date().toISOString().split('T')[0]">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Hora</label>
                  <input v-model="horaPart" type="time" class="form-control" required>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Estado</label>
                <select v-model="formSeguimientoAlerta.estado" class="form-select" required>
                  <option value="P">Pendiente</option>
                  <option value="EP">En Progreso</option>
                  <option value="C">Completado</option>
                  <option value="A">Aprobado</option>
                  <option value="R">Rechazado</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Análisis/Acción</label>
                <textarea v-model="formSeguimientoAlerta.analisis_accion" class="form-control" rows="5"
                  required></textarea>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-secondary" @click="cerrarModalesAlerta">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { api } from '@/components/services/auth_axios';
import { useToast } from 'vue-toast-notification';

const toast = useToast();
const alertas = ref([]);
const isLoading = ref(false);

// Estados para los modales
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);

// Estados para seguimientos de alertas
const showSeguimientosAlertaModal = ref(false);
const showEditarSeguimientoAlertaModal = ref(false);
const loadingSeguimientosAlerta = ref(false);
const alertaSeguimientos = ref(null);

// Datos para fecha y hora separados
const fechaPart = ref(new Date().toISOString().split('T')[0]);
const horaPart = ref('12:00');

// Propiedades computadas
const fechaHoraCompleta = computed(() => {
  if (!fechaPart.value || !horaPart.value) return null;

  // Formato: YYYY-MM-DDTHH:MM:SS
  return `${fechaPart.value}T${horaPart.value}:00`;
});

// Función para formatear fecha y hora
const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    // Ajustar a zona horaria local
    return date.toLocaleString('es-PE', {
      timeZone: 'America/Lima',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
  } catch (error) {
    return 'Fecha inválida';
  }
};

// Datos para los formularios
const nuevaAlerta = reactive({
  tipo: '',
  descripcion: ''
});

const alertaEditada = reactive({
  id: null,
  codigo: '',
  tipo: '',
  descripcion: '',
  fecha_creacion: ''
});

const alertaAEliminar = reactive({
  id: null,
  codigo: '',
  tipo: ''
});

// Formulario para seguimientos
const formSeguimientoAlerta = reactive({
  estado: 'P',
  analisis_accion: ''
});

const seguimientoAlertaEditando = ref(null);

// Métodos generales
const getBadgeColor = (tipo) => {
  const colors = {
    'Urgente': 'danger',
    'Importante': 'warning',
    'Informativa': 'info'
  };
  return colors[tipo] || 'primary';
};

// Métodos para estados de seguimiento
const getEstadoSeguimientoDisplay = (estado) => {
  const estados = {
    'P': 'Pendiente',
    'EP': 'En Progreso',
    'C': 'Completado',
    'A': 'Aprobado',
    'R': 'Rechazado'
  };
  return estados[estado] || estado;
};

const getEstadoSeguimientoClass = (estado) => {
  const clases = {
    'P': 'bg-secondary',
    'EP': 'bg-warning text-dark',
    'C': 'bg-info',
    'A': 'bg-success',
    'R': 'bg-danger'
  };
  return clases[estado] || 'bg-secondary';
};

const getEstadoSeguimientoBgClass = (estado) => {
  const clases = {
    'P': 'bg-light',
    'EP': 'bg-light',
    'C': 'bg-light',
    'A': 'bg-light',
    'R': 'bg-light'
  };
  return clases[estado] || 'bg-light';
};

// Métodos para CRUD de alertas
const cargarAlertas = async () => {
  isLoading.value = true;
  try {
    const response = await api.get('ficha/alertas/');
    alertas.value = response.data;
  } catch (error) {
    toast.error('Error al cargar alertas', { position: 'top-right' });
  } finally {
    isLoading.value = false;
  }
};

const crearAlerta = async () => {
  isLoading.value = true;
  try {
    const response = await api.post('ficha/alertas/', nuevaAlerta);
    toast.success('Alerta creada correctamente', { position: 'top-right' });
    showCreateModal.value = false;
    nuevaAlerta.tipo = '';
    nuevaAlerta.descripcion = '';
    cargarAlertas();
  } catch (error) {
    toast.error('Error al crear alerta', { position: 'top-right' });
  } finally {
    isLoading.value = false;
  }
};

const openEditModal = (alerta) => {
  alertaEditada.id = alerta.id;
  alertaEditada.codigo = alerta.codigo;
  alertaEditada.tipo = alerta.tipo;
  alertaEditada.descripcion = alerta.descripcion;
  alertaEditada.fecha_creacion = alerta.fecha_creacion;
  showEditModal.value = true;
};

const actualizarAlerta = async () => {
  isLoading.value = true;
  try {
    await api.put(`ficha/alertas/${alertaEditada.id}/`, {
      tipo: alertaEditada.tipo,
      descripcion: alertaEditada.descripcion
    });
    toast.success('Alerta actualizada', { position: 'top-right' });
    showEditModal.value = false;
    cargarAlertas();
  } catch (error) {
    toast.error('Error al actualizar alerta', { position: 'top-right' });
  } finally {
    isLoading.value = false;
  }
};

const openDeleteModal = (alerta) => {
  alertaAEliminar.id = alerta.id;
  alertaAEliminar.codigo = alerta.codigo;
  alertaAEliminar.tipo = alerta.tipo;
  showDeleteModal.value = true;
};

const eliminarAlerta = async () => {
  isLoading.value = true;
  try {
    await api.delete(`ficha/alertas/${alertaAEliminar.id}/`);
    toast.success('Alerta eliminada', { position: 'top-right' });
    showDeleteModal.value = false;
    cargarAlertas();
  } catch (error) {
    toast.error('Error al eliminar alerta', { position: 'top-right' });
  } finally {
    isLoading.value = false;
  }
};

// Métodos para seguimientos de alertas
const verSeguimientos = async (alertaId) => {
  try {
    loadingSeguimientosAlerta.value = true;

    const [alertaResponse, seguimientosResponse] = await Promise.all([
      api.get(`ficha/alertas/${alertaId}/`),
      api.get(`ficha/seguimiento-alertas/`, {
        params: {
          alerta: alertaId,
          fields: 'id,fecha_seguimiento,estado,analisis_accion,fecha_creacion,usuario_creacion',
          'usuario_creacion.fields': 'first_name,last_name'
        }
      })
    ]);

    alertaSeguimientos.value = {
      id: alertaId,
      seguimientos: seguimientosResponse.data,
      alertaData: alertaResponse.data
    };

    showSeguimientosAlertaModal.value = true;
  } catch (error) {
    console.error('Error al cargar seguimientos de alerta:', error);
    toast.error('Error al cargar los datos de los seguimientos');
  } finally {
    loadingSeguimientosAlerta.value = false;
  }
};

const nuevoSeguimientoAlerta = (alertaId) => {
  // Resetear valores
  fechaPart.value = new Date().toISOString().split('T')[0];
  horaPart.value = '12:00';
  formSeguimientoAlerta.estado = 'P';
  formSeguimientoAlerta.analisis_accion = '';

  seguimientoAlertaEditando.value = {
    alertaId,
    isNew: true
  };
  showEditarSeguimientoAlertaModal.value = true;
};

const editarSeguimientoAlerta = async (seguimientoId) => {
  try {
    loadingSeguimientosAlerta.value = true;
    const response = await api.get(`ficha/seguimiento-alertas/${seguimientoId}/`);

    // Parsear la fecha existente
    const fecha = new Date(response.data.fecha_seguimiento);
    fechaPart.value = fecha.toISOString().split('T')[0];
    horaPart.value = `${String(fecha.getHours()).padStart(2, '0')}:${String(fecha.getMinutes()).padStart(2, '0')}`;

    formSeguimientoAlerta.estado = response.data.estado;
    formSeguimientoAlerta.analisis_accion = response.data.analisis_accion;

    seguimientoAlertaEditando.value = {
      seguimientoId,
      isNew: false
    };
    showEditarSeguimientoAlertaModal.value = true;
  } catch (error) {
    console.error('Error al cargar seguimiento:', error);
    toast.error('Error al cargar el seguimiento');
  } finally {
    loadingSeguimientosAlerta.value = false;
  }
};

const guardarSeguimientoAlerta = async () => {
  try {
    loadingSeguimientosAlerta.value = true;

    if (!seguimientoAlertaEditando.value) {
      throw new Error('No hay seguimiento en edición');
    }

    // Asegurar el formato YYYY-MM-DD
    const fechaHora = new Date(`${fechaPart.value}T${horaPart.value}`);
    const fechaHoraISO = fechaHora.toISOString(); // Esto envía en UTC

    const payload = {
      fecha_seguimiento: fechaHoraISO, // Formato ISO con hora UTC
      estado: formSeguimientoAlerta.estado,
      analisis_accion: formSeguimientoAlerta.analisis_accion,
    };

    // Resto del código permanece igual...
    if (seguimientoAlertaEditando.value.isNew) {
      if (!seguimientoAlertaEditando.value.alertaId) {
        throw new Error('ID de alerta no definido para nuevo seguimiento');
      }
      payload.alerta_id = seguimientoAlertaEditando.value.alertaId;
    }

    let response;
    if (seguimientoAlertaEditando.value.isNew) {
      response = await api.post('ficha/seguimiento-alertas/', payload);
      toast.success('Seguimiento creado correctamente');

      if (alertaSeguimientos.value) {
        alertaSeguimientos.value.seguimientos.unshift(response.data);
      }
    } else {
      if (!seguimientoAlertaEditando.value.seguimientoId) {
        throw new Error('ID de seguimiento no definido para edición');
      }

      response = await api.put(
        `ficha/seguimiento-alertas/${seguimientoAlertaEditando.value.seguimientoId}/`,
        payload
      );
      toast.success('Seguimiento actualizado correctamente');

      if (alertaSeguimientos.value) {
        const index = alertaSeguimientos.value.seguimientos.findIndex(
          s => s.id === seguimientoAlertaEditando.value.seguimientoId
        );
        if (index !== -1) {
          alertaSeguimientos.value.seguimientos[index] = response.data;
        }
      }
    }

    showEditarSeguimientoAlertaModal.value = false;
    seguimientoAlertaEditando.value = null;

  } catch (error) {
    console.error('Error al guardar seguimiento:', error);
    let errorMsg = 'Error al guardar el seguimiento';
    if (error.response?.data) {
      errorMsg = Object.entries(error.response.data)
        .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
        .join(' | ');
    } else if (error.message) {
      errorMsg = error.message;
    }

    toast.error(errorMsg, { position: 'top-right', duration: 5000 });
  } finally {
    loadingSeguimientosAlerta.value = false;
  }
};

const cerrarModalesAlerta = () => {
  showSeguimientosAlertaModal.value = false;
  showEditarSeguimientoAlertaModal.value = false;
  alertaSeguimientos.value = null;
  seguimientoAlertaEditando.value = null;
};

// Cargar alertas al montar el componente
onMounted(() => {
  cargarAlertas();
});
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-backdrop {
  opacity: 0.5;
}

.badge {
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 700;
  line-height: 1;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;
}

.bg-primary {
  background-color: #0d6efd !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
  color: #000 !important;
}

.bg-info {
  background-color: #0dcaf0 !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}
</style>
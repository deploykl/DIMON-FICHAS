<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Registro de Participantes</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/">Inicio</a></li>
          <li class="breadcrumb-item active">Participantes</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Lista de Eventos</h5>
              
              <!-- Filtros -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="input-group">
                    <input 
                      v-model="searchTerm"
                      type="text" 
                      class="form-control" 
                      placeholder="Buscar eventos..."
                    >
                    <button class="btn btn-outline-secondary" type="button" @click="clearSearch">
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-check form-switch float-md-end">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      id="showFinished"
                      v-model="showFinished"
                    >
                    <label class="form-check-label" for="showFinished">
                      Mostrar eventos finalizados
                    </label>
                  </div>
                </div>
              </div>

              <!-- Lista de eventos -->
              <div class="accordion" id="eventsAccordion">
                <div 
                  v-for="evento in filteredEvents" 
                  :key="evento.id" 
                  class="accordion-item"
                >
                  <h2 class="accordion-header">
                    <button 
                      class="accordion-button collapsed" 
                      type="button" 
                      data-bs-toggle="collapse"
                      :data-bs-target="'#collapse' + evento.id"
                      :aria-expanded="false"
                      :aria-controls="'collapse' + evento.id"
                    >
                      <div class="d-flex w-100 justify-content-between align-items-center pe-3">
                        <div>
                          <span class="fw-bold me-2">{{ evento.descripcion }}</span>
                          <span class="badge" :class="statusBadgeClass(evento.estado)">
                            {{ getStatusText(evento.estado) }}
                          </span>
                        </div>
                        <small class="text-muted">
                          {{ formatDate(evento.fecha) }} | 
                          {{ formatTime(evento.hora_inicio) }} - {{ formatTime(evento.hora_fin) }}
                        </small>
                      </div>
                    </button>
                  </h2>
                  <div 
                    :id="'collapse' + evento.id" 
                    class="accordion-collapse collapse"
                    :aria-labelledby="'heading' + evento.id"
                    data-bs-parent="#eventsAccordion"
                    @shown.bs.collapse="() => loadEventParticipants(evento.id)"
                  >
                    <div class="accordion-body">
                      <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="mb-0">Participantes registrados: {{ evento.participantes_count || 0 }}</h6>
                        <button 
                          class="btn btn-sm btn-outline-primary"
                          @click="fetchParticipants(evento.id)"
                          :disabled="loadingParticipants === evento.id"
                        >
                          <span v-if="loadingParticipants === evento.id" class="spinner-border spinner-border-sm me-1"></span>
                          <i v-else class="bi bi-arrow-clockwise"></i> 
                          Actualizar
                        </button>
                      </div>

                      <!-- Spinner de carga -->
                      <div v-if="loadingParticipants === evento.id && !participants[evento.id]" class="text-center py-3">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Cargando...</span>
                        </div>
                      </div>

                      <!-- Tabla de participantes -->
                      <div class="table-responsive" v-if="participants[evento.id]?.length > 0">
                        <table class="table table-hover table-sm">
                          <thead>
                            <tr>
                              <th scope="col">#</th>
                              <th scope="col">DNI</th>
                              <th scope="col">Nombre Completo</th>
                              <th scope="col">Cargo</th>
                              <th scope="col">Establecimiento</th>
                              <th scope="col">Código</th>
                              <th scope="col">Acciones</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(participante, index) in participants[evento.id]" :key="participante.id">
                              <th scope="row">{{ index + 1 }}</th>
                              <td>{{ participante.dni }}</td>
                              <td>{{ participante.nombre }} {{ participante.apellido }}</td>
                              <td>{{ participante.cargo }}</td>
                              <td>{{ participante.establecimiento }}</td>
                              <td>{{ participante.codigo }}</td>
                              <td>
                                <button 
                                  class="btn btn-sm btn-outline-danger"
                                  @click="confirmDeleteParticipant(participante)"
                                >
                                  <i class="bi bi-trash"></i>
                                </button>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                      <div v-if="!loadingParticipants && (!participants[evento.id] || participants[evento.id]?.length === 0)" class="alert alert-info mb-0">
                        <i class="bi bi-info-circle me-2"></i>
                        No hay participantes registrados para este evento.
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="filteredEvents.length === 0" class="text-center py-4">
                  <i class="bi bi-calendar-x fs-1 text-muted mb-3"></i>
                  <p class="mb-0">No se encontraron eventos que coincidan con los criterios de búsqueda</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal de confirmación para eliminar participante -->
    <div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar eliminación</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            ¿Estás seguro que deseas eliminar al participante <strong>{{ selectedParticipant?.nombre }} {{ selectedParticipant?.apellido }}</strong> con DNI <strong>{{ selectedParticipant?.dni }}</strong>?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button 
              type="button" 
              class="btn btn-danger"
              @click="deleteParticipant"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
              Eliminar
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
import { Modal } from 'bootstrap'

const toast = useToast()

// Estados y datos
const events = ref([])
const participants = ref({})
const searchTerm = ref('')
const showFinished = ref(false)
const selectedParticipant = ref(null)
const deleting = ref(false)
const loadingParticipants = ref(null)
let confirmDeleteModal = null

// Configuración de estados
const statusColors = {
  PENDIENTE: 'warning',
  EN_PROGRESO: 'primary',
  FINALIZADO: 'success'
}

const statusTexts = {
  PENDIENTE: 'Pendiente',
  EN_PROGRESO: 'En Progreso',
  FINALIZADO: 'Finalizado'
}

// Computed
const filteredEvents = computed(() => {
  let filtered = [...events.value]
  
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(evento => 
      evento.descripcion.toLowerCase().includes(term) ||
      (evento.creado_por && evento.creado_por.toLowerCase().includes(term))
    ) // cierre correcto aquí
  }
  
  if (!showFinished.value) {
    filtered = filtered.filter(evento => evento.estado !== 'FINALIZADO')
  }
  
  filtered.sort((a, b) => {
    const dateA = new Date(`${a.fecha}T${a.hora_inicio}`)
    const dateB = new Date(`${b.fecha}T${b.hora_inicio}`)
    return dateB - dateA
  })
  
  return filtered
})


// Métodos
const statusBadgeClass = (status) => `bg-${statusColors[status]}`

const getStatusText = (status) => statusTexts[status] || status

const formatDate = (dateString) => {
  const [year, month, day] = dateString.split('-')
  const date = new Date(year, month - 1, day)
  return date.toLocaleDateString('es-PE', { 
    weekday: 'short', 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const formatTime = (timeString) => {
  const [hours, minutes] = timeString.split(':')
  return `${hours}:${minutes}`
}

const clearSearch = () => {
  searchTerm.value = ''
}

const fetchEvents = async () => {
  try {
    const response = await api.get('reuniones/evento/')
    events.value = response.data.map(event => ({
      ...event,
      estado: event.estado || 'PENDIENTE',
      participantes_count: event.participantes_count || 0
    }))
  } catch (error) {
    toast.error('Error al cargar los eventos')
    console.error('Error fetching events:', error)
  }
}

const loadEventParticipants = async (eventId) => {
  if (!participants.value[eventId]) {
    await fetchParticipants(eventId)
  }
}

const fetchParticipants = async (eventId) => {
  loadingParticipants.value = eventId
  try {
    const response = await api.get(`reuniones/persona/?eventos=${eventId}`)
    participants.value = {
      ...participants.value,
      [eventId]: response.data
    }
    
    // Actualizar contador en el evento
    const eventIndex = events.value.findIndex(e => e.id === eventId)
    if (eventIndex !== -1) {
      events.value[eventIndex].participantes_count = response.data.length
    }
  } catch (error) {
    toast.error('Error al cargar los participantes')
    console.error('Error fetching participants:', error)
  } finally {
    loadingParticipants.value = null
  }
}

const confirmDeleteParticipant = (participant) => {
  selectedParticipant.value = participant
  confirmDeleteModal.show()
}

const deleteParticipant = async () => {
  if (!selectedParticipant.value) return
  
  deleting.value = true
  try {
    await api.delete(`reuniones/persona/${selectedParticipant.value.id}/`)
    toast.success('Participante eliminado correctamente')
    
    const eventId = selectedParticipant.value.eventos[0]
    if (eventId) {
      await fetchParticipants(eventId)
    }
    
    confirmDeleteModal.hide()
  } catch (error) {
    toast.error('Error al eliminar participante')
    console.error('Error deleting participant:', error)
  } finally {
    deleting.value = false
  }
}

// Ciclo de vida
onMounted(async () => {
  confirmDeleteModal = new Modal(document.getElementById('confirmDeleteModal'))
  await fetchEvents()
})
</script>

<style scoped>
.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.05);
}

.accordion-item {
  margin-bottom: 0.5rem;
  border-radius: 0.375rem !important;
}

.table th, .table td {
  vertical-align: middle;
}

.badge {
  font-size: 0.75em;
  font-weight: 500;
}
</style>
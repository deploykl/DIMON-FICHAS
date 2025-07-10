<template>
  <main id="main" class="main">
    <!-- Header con breadcrumb -->
    <div class="pagetitle">
      <h1>Registro de Participantes</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/">Inicio</a></li>
          <li class="breadcrumb-item active">Participantes</li>
        </ol>
      </nav>
    </div>

    <!-- Botón para abrir modal de creación -->
    <div class="text-end mb-4">
      <button @click="openCreateModal" class="btn btn-primary">
        <i class="bi bi-plus-lg me-2"></i> Nueva Reunión
      </button>
    </div>

    <!-- Sección principal -->
    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card shadow-sm">
            <div class="card-body">

              <!-- Filtros mejorados -->
              <div class="row mb-3">
                <div class="col-md-8">
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input v-model="searchTerm" type="text" class="form-control" placeholder="Buscar reunión...">
                    <button @click="clearSearch" class="btn btn-outline-secondary" type="button">
                      <i class="bi bi-x-lg"></i>
                    </button>
                  </div>
                </div>

                <div class="col-md-4 d-flex align-items-center justify-content-end">
                  <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" v-model="showFinished" id="showFinished">
                    <label class="form-check-label" for="showFinished">Mostrar finalizados</label>
                  </div>
                </div>
              </div>

              <!-- Lista de eventos con acordeón -->
              <div class="accordion" id="eventsAccordion">
                <div v-if="filteredEvents.length === 0" class="text-center py-5">
                  <i class="bi bi-search text-muted" style="font-size: 3rem;"></i>
                  <p class="text-muted mt-3">No se encontraron eventos</p>
                </div>

                <div v-for="evento in filteredEvents" :key="evento.id" class="accordion-item mb-2">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" @click="toggleAccordion(evento.id)"
                      :class="{ 'collapsed': activeAccordion !== evento.id }">
                      <div class="d-flex flex-column w-100">
                        <div class="d-flex justify-content-between align-items-center">
                          <span class="fw-bold">{{ evento.descripcion }}</span>
                          <span class="badge" :class="statusBadgeClass(evento.estado)">
                            {{ getStatusText(evento.estado) }}
                          </span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                          <small class="text-muted">
                            {{ formatDate(evento.fecha) }} |
                            {{ formatTime(evento.hora_inicio) }} - {{ formatTime(evento.hora_fin) }}
                          </small>
                          <small class="text-primary fw-bold">
                            Participantes: {{ evento.participantes_count || 0 }}
                          </small>
                        </div>
                      </div>
                    </button>
                  </h2>

                  <div class="accordion-collapse collapse" :class="{ 'show': activeAccordion === evento.id }">
                    <div class="accordion-body">
                      <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="mb-0">Participantes registrados: {{ evento.participantes_count || 0 }}</h5>
                        <div>
                          <button @click="fetchParticipants(evento.id)" :disabled="loadingParticipants === evento.id"
                            class="btn btn-sm btn-outline-secondary me-2">
                            <span v-if="loadingParticipants === evento.id"
                              class="spinner-border spinner-border-sm me-1"></span>
                            <i v-else class="bi bi-arrow-clockwise me-1"></i>
                            Actualizar
                          </button>
                          <button @click="generateEventPDF(evento)"
                            :disabled="loadingParticipants === evento.id || !participants[evento.id]?.length"
                            class="btn btn-sm btn-danger">
                            <i class="bi bi-file-earmark-pdf me-1"></i>
                            PDF
                          </button>
                        </div>
                      </div>

                      <!-- Spinner de carga -->
                      <div v-if="loadingParticipants === evento.id && !participants[evento.id]"
                        class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                          <span class="visually-hidden">Cargando...</span>
                        </div>
                      </div>

                      <!-- Tabla de participantes -->
                      <div v-if="participants[evento.id]?.length > 0" class="table-responsive">
                        <table class="table table-hover table-sm">
                          <thead class="table-light">
                            <tr>
                              <th>#</th>
                              <th>Fecha Registro</th>
                              <th>DNI</th>
                              <th>Nombre</th>
                              <th>Cargo</th>
                              <th>N° celular</th>
                              <th>Correo</th>
                              <th>Establecimiento</th>
                              <th>Código</th>
                              <th>Firma</th>
                              <th>Acciones</th>
                            </tr>
                          </thead>
                          <tbody>
                            <!-- En la tabla de participantes, modifica la columna de Acciones -->
                            <tr v-for="(participante, index) in participants[evento.id]" :key="participante.id">
                              <td>{{ index + 1 }}</td>
                              <td>{{ formatDateTime(participante.fecha_registro) }}</td>
                              <td>{{ participante.dni }}</td>
                              <td>{{ participante.nombre }} {{ participante.apellido }}</td>
                              <td>{{ participante.cargo }}</td>
                              <td>{{ participante.telefono }}</td>
                              <td>{{ participante.email }}</td>
                              <td>{{ participante.establecimiento }}</td>
                              <td>{{ participante.codigo }}</td>
                              <td> <img v-if="participante.firma_url" :src="participante.firma_url"
                                  @click="viewSignature(participante.firma_url)"
                                  style="max-width: 40px; max-height: 30px; cursor: pointer;" class="img-thumbnail me-1"
                                  alt="Firma">
                                <span v-else class="text-muted">Sin firma</span>
                              </td>
                              <td>
                                <button @click="confirmDeleteParticipant(participante)"
                                  class="btn btn-sm btn-outline-danger me-1" title="Eliminar">
                                  <i class="bi bi-trash"></i>
                                </button>
                                <!-- Mostrar miniatura de la firma si existe -->

                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                      <div
                        v-if="!loadingParticipants && (!participants[evento.id] || participants[evento.id]?.length === 0)"
                        class="text-center py-4 text-muted">
                        <i class="bi bi-people" style="font-size: 2rem;"></i>
                        <p class="mt-2">No hay participantes registrados</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para crear evento -->
    <div class="modal fade" :class="{ 'show d-block': showCreateModal }" tabindex="-1" v-if="showCreateModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Programar Nueva Reunión</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeCreateModal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="crearEvento">
              <!-- Descripción -->
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea v-model="evento.descripcion" class="form-control" rows="3" required></textarea>
              </div>

              <!-- Fecha y Horario -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label">Fecha</label>
                  <input v-model="evento.fecha" type="date" class="form-control" required :min="today">
                </div>

                <div class="col-md-6">
                  <label class="form-label">Horario</label>
                  <div class="d-flex align-items-center">
                    <input v-model="evento.hora_inicio" type="time" class="form-control" step="300" required>
                    <span class="mx-2">—</span>
                    <input v-model="evento.hora_fin" type="time" class="form-control" step="300" required>
                  </div>
                </div>
              </div>

              <!-- Botones -->
              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-secondary" @click="limpiarFormulario">
                  <i class="bi bi-eraser me-1"></i> Limpiar
                </button>
                <button type="submit" class="btn btn-primary" :disabled="creatingEvent">
                  <span v-if="creatingEvent" class="spinner-border spinner-border-sm me-1"></span>
                  <i v-else class="bi bi-save me-1"></i>
                  {{ creatingEvent ? 'Guardando...' : 'Guardar Reunión' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal"></div>

    <!-- Modal de confirmación para eliminar participante -->
    <div class="modal fade" :class="{ 'show d-block': showDeleteModal }" tabindex="-1" v-if="showDeleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-warning text-dark">
            <h5 class="modal-title">Confirmar eliminación</h5>
            <button type="button" class="btn-close" @click="closeDeleteModal"></button>
          </div>

          <div class="modal-body">
            <p>¿Eliminar a <strong>{{ selectedParticipant?.nombre }} {{ selectedParticipant?.apellido }}</strong> (DNI:
              {{ selectedParticipant?.dni }})?</p>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="deleteParticipant" :disabled="deleting">
              <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
              {{ deleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showDeleteModal"></div>

    <!-- Modal para visualizar firma -->
    <div class="modal fade" :class="{ 'show d-block': showSignatureModal }" tabindex="-1" v-if="showSignatureModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Firma del participante</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeSignatureModal"></button>
          </div>

          <div class="modal-body text-center">
            <img :src="selectedSignature" class="img-fluid border rounded" alt="Firma">
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeSignatureModal">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showSignatureModal"></div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { api } from '@/components/services/auth_axios'
import { useToast } from 'vue-toast-notification'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const toast = useToast()

// Estados y datos
const events = ref([])
const participants = ref({})
const searchTerm = ref('')
const showFinished = ref(false)
const selectedParticipant = ref(null)
const selectedSignature = ref(null)
const deleting = ref(false)
const loadingParticipants = ref(null)
const generatingPDF = ref(false)
const creatingEvent = ref(false)
const activeAccordion = ref(null)
let intervaloActualizacion = null

// Modales
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const showSignatureModal = ref(false)

// Funciones auxiliares para fecha y hora
const getCurrentDate = () => {
  const today = new Date()
  return today.toISOString().split('T')[0]
}

const getRoundedTime = () => {
  const now = new Date()
  let hours = now.getHours()
  let minutes = now.getMinutes()

  // Redondear a los próximos 30 minutos
  if (minutes < 30) {
    minutes = 30
  } else {
    minutes = 0
    hours = (hours + 1) % 24
  }

  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
}

const addHours = (timeString, hoursToAdd) => {
  const [hours, minutes] = timeString.split(':').map(Number)
  let newHours = hours + hoursToAdd
  newHours = newHours % 24 // Manejar cambio de día

  return `${newHours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
}

// Datos del evento con valores por defecto
const evento = ref({
  descripcion: '',
  fecha: getCurrentDate(),
  hora_inicio: getRoundedTime(),
  hora_fin: addHours(getRoundedTime(), 2)
})

// Configuración de estados
const statusColors = {
  PENDIENTE: 'bg-warning',
  EN_PROGRESO: 'bg-primary',
  FINALIZADO: 'bg-success'
}

const statusTexts = {
  PENDIENTE: 'Pendiente',
  EN_PROGRESO: 'En Progreso',
  FINALIZADO: 'Finalizado'
}

// Computed
const filteredEvents = computed(() => {
  let filtered = [...events.value]

  // Filtros
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filtered = filtered.filter(evento =>
      evento.descripcion.toLowerCase().includes(term))
  }

  if (!showFinished.value) {
    filtered = filtered.filter(evento => evento.estado !== 'FINALIZADO')
  }

  // Ordenación mejorada
  filtered.sort((a, b) => {
    // Primero por estado (En progreso primero)
    if (a.estado === 'EN_PROGRESO' && b.estado !== 'EN_PROGRESO') return -1
    if (b.estado === 'EN_PROGRESO' && a.estado !== 'EN_PROGRESO') return 1

    // Luego por fecha y hora
    const fechaHoraA = new Date(`${a.fecha}T${a.hora_inicio}`).getTime()
    const fechaHoraB = new Date(`${b.fecha}T${b.hora_inicio}`).getTime()
    const ahora = new Date().getTime()

    const diffA = Math.abs(fechaHoraA - ahora)
    const diffB = Math.abs(fechaHoraB - ahora)

    return diffA - diffB
  })

  return filtered
})

// Métodos
const statusBadgeClass = (status) => statusColors[status] || 'bg-secondary'

const getStatusText = (status) => statusTexts[status] || status

const formatDate = (dateString) => {
  const options = {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC'
  }
  const [year, month, day] = dateString.split('-')
  const date = new Date(Date.UTC(year, month - 1, day))
  return date.toLocaleDateString('es-PE', options)
}

const formatTime = (timeString) => {
  const [hours, minutes] = timeString.split(':')
  return `${hours}:${minutes}`
}

const clearSearch = () => {
  searchTerm.value = ''
}

const toggleAccordion = (eventId) => {
  if (activeAccordion.value === eventId) {
    activeAccordion.value = null
  } else {
    activeAccordion.value = eventId
    loadEventParticipants(eventId)
  }
}

// Iniciar actualización automática de estados
const iniciarActualizacionAutomatica = () => {
  if (intervaloActualizacion) clearInterval(intervaloActualizacion)

  intervaloActualizacion = setInterval(async () => {
    await actualizarEstadosEventos()
  }, 30000) // Actualizar cada 30 segundos
}

// Actualizar estados de eventos
const actualizarEstadosEventos = async () => {
  try {
    // Guardar los conteos actuales antes de actualizar
    const conteosActuales = {};
    events.value.forEach(event => {
      conteosActuales[event.id] = event.participantes_count || 0;
    });

    const response = await api.post('reuniones/evento/actualizar_estados/');

    // Mantener los conteos existentes o usar los nuevos si están disponibles
    events.value = response.data.map(event => ({
      ...event,
      estado: event.estado || 'PENDIENTE',
      participantes_count: event.participantes_count || conteosActuales[event.id] || 0
    }));
  } catch (error) {
    console.error('Error en actualización de estados:', error);
  }
};

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

    // Ordenar por fecha de registro (más antiguo primero)
    const sortedParticipants = response.data.sort((a, b) => {
      return new Date(a.fecha_registro) - new Date(b.fecha_registro)
    })

    participants.value = {
      ...participants.value,
      [eventId]: sortedParticipants
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

const openCreateModal = () => {
  showCreateModal.value = true
}

const closeCreateModal = () => {
  showCreateModal.value = false
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

const closeSignatureModal = () => {
  showSignatureModal.value = false
}

const confirmDeleteParticipant = (participant) => {
  selectedParticipant.value = participant
  showDeleteModal.value = true
}

const viewSignature = (signatureUrl) => {
  selectedSignature.value = signatureUrl
  showSignatureModal.value = true
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

    closeDeleteModal()
  } catch (error) {
    toast.error('Error al eliminar participante')
    console.error('Error deleting participant:', error)
  } finally {
    deleting.value = false
  }
}
const formatDateTime = (datetimeString) => {
  if (!datetimeString) return 'N/A'

  const date = new Date(datetimeString)
  const options = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return date.toLocaleString('es-PE', options)
}
const crearEvento = async () => {
  if (evento.value.hora_fin <= evento.value.hora_inicio) {
    toast.error('La hora de fin debe ser mayor a la hora de inicio')
    return
  }

  creatingEvent.value = true
  try {
    const response = await api.post('reuniones/evento/', evento.value)
    toast.success('Reunión creada correctamente')
    await fetchEvents()
    limpiarFormulario()
    closeCreateModal()
  } catch (error) {
    toast.error('Error al crear reunión: ' + (error.response?.data?.detail || error.message))
    console.error('Error:', error)
  } finally {
    creatingEvent.value = false
  }
}

const limpiarFormulario = () => {
  evento.value = {
    descripcion: '',
    fecha: getCurrentDate(),
    hora_inicio: getRoundedTime(),
    hora_fin: addHours(getRoundedTime(), 2)
  }
}

const generateEventPDF = async (evento) => {
  generatingPDF.value = true
  try {
    toast.info('Generando PDF...', { timeout: 2000 })

    if (!participants.value[evento.id] || participants.value[evento.id].length === 0) {
      toast.error('No hay participantes para generar el PDF')
      return
    }

    const doc = new jsPDF({
      orientation: 'landscape',
      unit: 'mm'
    })

    // Título del documento
    doc.setFontSize(18)
    doc.setTextColor(40)
    doc.text(`Lista de Participantes - ${evento.descripcion}`, 105, 15, { align: 'center' })

    // Información del evento
    doc.setFontSize(12)
    doc.text(`Fecha: ${formatDate(evento.fecha)}`, 15, 25)
    doc.text(`Horario: ${formatTime(evento.hora_inicio)} - ${formatTime(evento.hora_fin)}`, 15, 30)
    doc.text(`Total de participantes: ${participants.value[evento.id].length}`, 15, 35)

    // Configuración de la tabla
    const headers = [
      '#',
      'DNI',
      'Nombre Completo',
      'Cargo',
      'Correo',
      'N° Celular',
      'Establecimiento',
      'Firma'
    ]

    // Preparar los datos
    const data = participants.value[evento.id].map((participante, index) => {
      return [
        index + 1,
        participante.dni,
        `${participante.nombre} ${participante.apellido}`,
        participante.cargo,
        participante.email,
        participante.telefono,
        participante.establecimiento,
        participante.firma_url ? 'Firma registrada' : 'Sin firma'
      ]
    })

    // Crear la tabla principal
    autoTable(doc, {
      startY: 40,
      head: [headers],
      body: data,
      theme: 'grid',
      headStyles: {
        fillColor: [41, 128, 185],
        textColor: 255,
        fontStyle: 'bold'
      },
      alternateRowStyles: {
        fillColor: [245, 245, 245]
      },
      margin: { top: 40 },
      styles: {
        fontSize: 10,
        cellPadding: 3,
        overflow: 'linebreak'
      },
      columnStyles: {
        0: { cellWidth: 10 },
        1: { cellWidth: 25 },
        2: { cellWidth: 45 },
        3: { cellWidth: 40 },
        4: { cellWidth: 40 },
        5: { cellWidth: 25 },
        6: { cellWidth: 30 }
      }
    })

    // Agregar las firmas como imágenes en páginas adicionales
    const participantsWithSignatures = participants.value[evento.id].filter(p => p.firma_url)

    if (participantsWithSignatures.length > 0) {
      doc.addPage('landscape')
      doc.setFontSize(16)
      doc.text('Firmas de los Participantes', 105, 20, { align: 'center' })

      let yPosition = 30
      const imgWidth = 80
      const imgHeight = 30
      const margin = 10
      const itemsPerRow = 3
      const itemsPerPage = 9

      let currentItem = 0

      for (const participante of participantsWithSignatures) {
        const colIndex = currentItem % itemsPerRow
        const xPosition = margin + (colIndex * (imgWidth + margin))

        if (currentItem > 0 && currentItem % itemsPerRow === 0) {
          yPosition += imgHeight + margin
        }

        if (currentItem > 0 && currentItem % itemsPerPage === 0) {
          doc.addPage('landscape')
          doc.setFontSize(16)
          doc.text('Firmas de los Participantes (continuación)', 105, 20, { align: 'center' })
          yPosition = 30
          currentItem = 0
          continue
        }

        try {
          doc.setFontSize(8)
          doc.text(`${participante.nombre} ${participante.apellido} (DNI: ${participante.dni})`,
            xPosition, yPosition - 5)

          const img = new Image()
          img.src = participante.firma_url

          await new Promise((resolve) => {
            img.onload = () => {
              doc.addImage(img, 'JPEG', xPosition, yPosition, imgWidth, imgHeight)
              resolve()
            }
            img.onerror = () => {
              doc.text('Error al cargar firma', xPosition, yPosition + imgHeight / 2)
              resolve()
            }
          })

          currentItem++
        } catch (error) {
          console.error('Error al agregar firma:', error)
          doc.text('Error al cargar firma', xPosition, yPosition + imgHeight / 2)
          currentItem++
        }
      }
    }

    // Pie de página
    const pageCount = doc.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      doc.setFontSize(10)
      doc.setTextColor(150)
      doc.text(
        `Página ${i} de ${pageCount}`,
        280,
        200,
        { align: 'right' }
      )
      doc.text(
        `Generado el ${new Date().toLocaleDateString()}`,
        15,
        200
      )
    }

    doc.save(`Participantes_${evento.descripcion.replace(/[^a-z0-9]/gi, '_')}.pdf`)
    toast.success('PDF generado correctamente')
  } catch (error) {
    toast.error('Error al generar PDF')
    console.error('Error generating PDF:', error)
  } finally {
    generatingPDF.value = false
  }
}

// Fecha mínima (hoy)
const today = new Date().toISOString().split('T')[0]

// Ciclo de vida
onMounted(async () => {
  await fetchEvents()
  iniciarActualizacionAutomatica()
})

onBeforeUnmount(() => {
  if (intervaloActualizacion) clearInterval(intervaloActualizacion)
})
</script>

<style scoped>
/* Estilos personalizados adicionales */
.main {
  padding: 20px;
}

.pagetitle {
  margin-bottom: 20px;
}

.pagetitle h1 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.05);
}

.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(0, 0, 0, 0.125);
}

.table th {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-backdrop {
  opacity: 0.5;
}

/* Estilo para la firma en el modal */
.signature-img {
  max-height: 70vh;
  object-fit: contain;
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .pagetitle h1 {
    font-size: 1.5rem;
  }

  .filter-section {
    flex-direction: column;
    gap: 10px;
  }

  .time-inputs {
    flex-direction: column;
    gap: 10px;
  }

  .time-separator {
    display: none;
  }
}

/* Estilos para las miniaturas de firma */
.img-thumbnail {
  padding: 0.15rem;
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  transition: all 0.2s ease-in-out;
}

.img-thumbnail:hover {
  transform: scale(1.5);
  z-index: 10;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}
</style>
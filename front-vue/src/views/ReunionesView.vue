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
                        <div>
                          <button 
                            class="btn btn-sm btn-outline-primary me-2"
                            @click="fetchParticipants(evento.id)"
                            :disabled="loadingParticipants === evento.id"
                          >
                            <span v-if="loadingParticipants === evento.id" class="spinner-border spinner-border-sm me-1"></span>
                            <i v-else class="bi bi-arrow-clockwise"></i> 
                            Actualizar
                          </button>
                          <button 
                            class="btn btn-sm btn-outline-success"
                            @click="generateEventPDF(evento)"
                            :disabled="loadingParticipants === evento.id || !participants[evento.id]?.length"
                          >
                            <i class="bi bi-file-earmark-pdf"></i> 
                            Descargar PDF
                          </button>
                        </div>
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
                                  class="btn btn-sm btn-outline-danger me-2"
                                  @click="confirmDeleteParticipant(participante)"
                                  title="Eliminar participante"
                                >
                                  <i class="bi bi-trash"></i>
                                </button>
                                <button 
                                  v-if="participante.firma"
                                  class="btn btn-sm btn-outline-primary"
                                  @click="viewSignature(participante.firma)"
                                  title="Ver firma"
                                >
                                  <i class="bi bi-eye"></i>
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

    <!-- Modal para visualizar firma -->
    <div class="modal fade" id="signatureModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Firma del participante</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="selectedSignature" class="img-fluid signature-img" alt="Firma del participante">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
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
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

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
let confirmDeleteModal = null
let signatureModal = null

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
    )
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

const viewSignature = (signatureUrl) => {
  selectedSignature.value = signatureUrl
  signatureModal.show()
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

const generateEventPDF = async (evento) => {
  generatingPDF.value = true
  try {
    toast.info('Generando PDF, por favor espere...', { timeout: 2000 })
    
    // Crear PDF en orientación horizontal para mejor espacio
    const doc = new jsPDF({
      orientation: 'landscape',
      unit: 'mm'
    })
    
    // Configuración inicial
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 10
    const contentWidth = pageWidth - 2 * margin
    
    // Logo (opcional)
    // const logoUrl = '/path/to/logo.png'
    // if (logoUrl) {
    //   const logoData = await loadImage(logoUrl)
    //   doc.addImage(logoData, 'PNG', margin, margin, 30, 15)
    // }
    
    // Título del documento
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text(`Reporte de Participantes - Evento: ${evento.descripcion}`, pageWidth / 2, 20, { align: 'center' })
    
    // Información del evento
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.text(`Fecha: ${formatDate(evento.fecha)}`, margin, 30)
    doc.text(`Horario: ${formatTime(evento.hora_inicio)} - ${formatTime(evento.hora_fin)}`, margin + 50, 30)
    doc.text(`Estado: ${getStatusText(evento.estado)}`, margin + 100, 30)
    doc.text(`Total participantes: ${evento.participantes_count || 0}`, margin + 150, 30)
    
    // Tabla de participantes
    let yPosition = 40
    const participantes = participants.value[evento.id]
    
    // Encabezados de tabla
    doc.setFontSize(10)
    doc.setFont('helvetica', 'bold')
    doc.text('N°', margin, yPosition)
    doc.text('DNI', margin + 15, yPosition)
    doc.text('Nombre Completo', margin + 30, yPosition)
    doc.text('Cargo', margin + 70, yPosition)
    doc.text('Establecimiento', margin + 110, yPosition)
    doc.text('Código', margin + 160, yPosition)
    doc.text('Firma', margin + 190, yPosition)
    
    yPosition += 5
    
    // Línea divisoria
    doc.setDrawColor(200, 200, 200)
    doc.line(margin, yPosition, pageWidth - margin, yPosition)
    yPosition += 5
    
    // Contenido de la tabla
    doc.setFontSize(9)
    doc.setFont('helvetica', 'normal')
    
    for (let i = 0; i < participantes.length; i++) {
      const p = participantes[i]
      
      // Verificar espacio en página
      if (yPosition > pageHeight - 20) {
        doc.addPage('landscape')
        yPosition = 20
      }
      
      // Datos del participante
      doc.text(`${i + 1}`, margin, yPosition)
      doc.text(p.dni, margin + 15, yPosition)
      
      // Nombre
      const nombre = `${p.nombre} ${p.apellido}`
      const nombreLines = doc.splitTextToSize(nombre, 35)
      doc.text(nombreLines, margin + 30, yPosition)
      
      // Cargo
      const cargoLines = doc.splitTextToSize(p.cargo, 35)
      doc.text(cargoLines, margin + 70, yPosition)
      
      // Establecimiento
      const establecimientoLines = doc.splitTextToSize(p.establecimiento, 45)
      doc.text(establecimientoLines, margin + 110, yPosition)
      
      // Código
      doc.text(p.codigo || 'N/A', margin + 160, yPosition)
      
      // Agregar firma si existe
      if (p.firma) {
        try {
          const imgData = await loadImage(p.firma)
          const imgWidth = 30
          const imgHeight = 15
          doc.addImage(imgData, 'PNG', margin + 190, yPosition - 10, imgWidth, imgHeight)
        } catch (error) {
          doc.text('Firma no disponible', margin + 190, yPosition)
          console.error('Error al cargar firma:', error)
        }
      } else {
        doc.text('Sin firma', margin + 190, yPosition)
      }
      
      yPosition += 15
      
      // Línea divisoria entre participantes
      if (i < participantes.length - 1) {
        doc.setDrawColor(240, 240, 240)
        doc.line(margin, yPosition - 2, pageWidth - margin, yPosition - 2)
      }
    }
    
    // Pie de página
    doc.setFontSize(8)
    doc.setTextColor(150, 150, 150)
    doc.text(`Generado el: ${new Date().toLocaleDateString()} a las ${new Date().toLocaleTimeString()}`, pageWidth / 2, pageHeight - 10, { align: 'center' })
    
    // Guardar PDF
    doc.save(`Participantes_${evento.descripcion.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().slice(0,10)}.pdf`)
    
    toast.success('PDF generado correctamente')
  } catch (error) {
    toast.error('Error al generar el PDF')
    console.error('Error generating PDF:', error)
  } finally {
    generatingPDF.value = false
  }
}

const loadImage = (url) => {
  return new Promise((resolve) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.onload = () => resolve(img)
    img.onerror = () => resolve(null)
    img.src = url
  })
}

// Ciclo de vida
onMounted(async () => {
  confirmDeleteModal = new Modal(document.getElementById('confirmDeleteModal'))
  signatureModal = new Modal(document.getElementById('signatureModal'))
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

.signature-img {
  max-width: 100%;
  max-height: 70vh;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background-color: white;
  padding: 10px;
}

.btn-outline-primary {
  transition: all 0.2s;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: white;
}

.btn-outline-success {
  transition: all 0.2s;
}

.btn-outline-success:hover {
  background-color: #198754;
  color: white;
}
</style>
<template>
    <main class="container">
        <div class="card shadow">
            <div class="card-body p-4">
                <!-- Paso 1: Selección de Evento -->
                <div v-if="paso === 1">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="card-title mb-0 fw-bold">Lista de Eventos</h5>
                    </div>

                    <!-- Buscador -->
                    <div class="row g-3 mb-4">
                        <div class="col-md-8 col-lg-6">
                            <div class="input-group">
                                <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
                                <input v-model="terminoBusqueda" type="text" class="form-control"
                                    placeholder="Buscar eventos..." @input="filtrarEventos">
                                <button class="btn btn-outline-secondary" type="button" @click="limpiarBusqueda">
                                    <i class="bi bi-x-lg"></i>
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4 col-lg-6 text-md-end">
                            <div class="form-check form-switch d-inline-flex align-items-center">
                                <input class="form-check-input me-2" type="checkbox" id="mostrarFinalizados"
                                    v-model="mostrarFinalizados">
                                <label class="form-check-label" for="mostrarFinalizados">
                                    Mostrar finalizados
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="list-group overflow-auto" style="max-height: 65vh;">
                        <button v-for="evento in eventosFiltrados" :key="evento.id" @click="seleccionarEvento(evento)"
                            class="list-group-item list-group-item-action border-start border-5 py-3" :class="{
                                'border-warning': evento.estado === 'PENDIENTE',
                                'border-primary': evento.estado === 'EN_PROGRESO',
                                'border-success': evento.estado === 'FINALIZADO',
                                'pe-none': evento.estado !== 'EN_PROGRESO'
                            }"
                            :title="evento.estado !== 'EN_PROGRESO' ? 'Solo se puede registrar en eventos en progreso' : ''">
                            <div v-if="evento.estado !== 'EN_PROGRESO'"
                                class="position-absolute top-50 end-0 translate-middle-y me-3">
                                <i class="bi bi-lock-fill text-muted"></i>
                            </div>
                            <div class="d-flex w-100 justify-content-between align-items-start">
                                <h6 class="mb-1 fw-bold">{{ evento.descripcion }}</h6>
                                <div class="d-flex align-items-center">
                                    <small class="text-muted">{{ formatFecha(evento.fecha) }}</small>
                                    <span class="badge ms-2" :class="`bg-${estadosColores[evento.estado]}`">
                                        {{ evento.estado_display || estadosTexto[evento.estado] }}
                                    </span>
                                </div>
                            </div>
                            <p class="mb-1 text-muted">
                                <i class="bi bi-clock me-1"></i>{{ formatHora(evento.hora_inicio) }} - {{
                                    formatHora(evento.hora_fin) }}
                            </p>
                            <small class="text-muted">
                                <i class="bi bi-person me-1"></i>Creado por: {{ evento.creado_por }}
                            </small>
                        </button>
                        <div v-if="eventosFiltrados.length === 0" class="list-group-item text-center text-muted py-5">
                            <i class="bi bi-calendar-x fs-4 mb-2"></i>
                            <p class="mb-0">No se encontraron eventos que coincidan con la búsqueda</p>
                        </div>
                    </div>
                </div>

                <!-- Paso 2: Registro de Participantes -->
                <div v-if="paso === 2">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="card-title mb-0 fw-bold">
                            <i class="bi bi-person-plus me-2"></i>Registro para: {{ eventoSeleccionado.descripcion }}
                        </h5>
                        <button @click="volverAListado" class="btn btn-outline-secondary btn-sm">
                            <i class="bi bi-arrow-left me-1"></i> Volver
                        </button>
                    </div>

                    <div class="alert mb-4 d-flex align-items-center"
                        :class="`alert-${estadosColores[eventoSeleccionado.estado]}`">
                        <i class="bi bi-info-circle me-2 fs-5"></i>
                        <div>
                            <span class="fw-bold">Estado:</span> {{ eventoSeleccionado.estado_display ||
                                estadosTexto[eventoSeleccionado.estado] }} |
                            <span class="fw-bold">Fecha:</span> {{ formatFecha(eventoSeleccionado.fecha) }} |
                            <span class="fw-bold">Horario:</span> {{ formatHora(eventoSeleccionado.hora_inicio) }} - {{
                                formatHora(eventoSeleccionado.hora_fin) }}
                        </div>
                    </div>

                    <form @submit.prevent="registrarParticipante" class="needs-validation" novalidate
                        :class="{ 'pe-none': eventoSeleccionado.estado !== 'EN_PROGRESO' }">
                        <fieldset :disabled="eventoSeleccionado.estado !== 'EN_PROGRESO'">

                            <!-- Sección de Datos Personales -->
                            <div class="card mb-4 border-0 shadow-sm">
                                <div class="card-header bg-light">
                                    <h6 class="mb-0 fw-bold"><i class="bi bi-person-vcard me-2"></i>Datos Personales
                                    </h6>
                                </div>
                                <div class="card-body">
                                    <div class="row g-3 mb-3">
                                        <div class="col-md-6">
                                            <label class="form-label">DNI <span class="text-danger">*</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.dni" type="text" class="form-control"
                                                    required maxlength="8" @keypress="soloNumeros"
                                                    :class="{ 'is-invalid': dniInvalido }" placeholder="Ingrese DNI">
                                                <span class="input-group-text"><i class="bi bi-credit-card"></i></span>
                                                <div v-if="dniInvalido" class="invalid-feedback">
                                                    El DNI debe tener exactamente 8 dígitos numéricos
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label">Nombre <span class="text-danger">*</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.nombre" type="text" class="form-control"
                                                    required :class="{ 'is-invalid': !participante.nombre }"
                                                    placeholder="Nombres completos">
                                                <span class="input-group-text"><i class="bi bi-person"></i></span>
                                                <div v-if="!participante.nombre" class="invalid-feedback">
                                                    El nombre es obligatorio
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="row g-3 mb-3">
                                        <div class="col-md-6">
                                            <label class="form-label">Apellido <span
                                                    class="text-danger">*</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.apellido" type="text" class="form-control"
                                                    required :class="{ 'is-invalid': !participante.apellido }"
                                                    placeholder="Apellidos completos">
                                                <span class="input-group-text"><i class="bi bi-person"></i></span>
                                                <div v-if="!participante.apellido" class="invalid-feedback">
                                                    El apellido es obligatorio
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label">Cargo <span class="text-danger">*</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.cargo" type="text" class="form-control"
                                                    required :class="{ 'is-invalid': !participante.cargo }"
                                                    placeholder="Cargo o puesto">
                                                <span class="input-group-text"><i class="bi bi-briefcase"></i></span>
                                                <div v-if="!participante.cargo" class="invalid-feedback">
                                                    El cargo es obligatorio
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row g-3">
                                        <div class="col-md-6">
                                            <label class="form-label">Email <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.email" type="email" class="form-control"
                                                    placeholder="correo@dominio.com">
                                                <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                                            </div>
                                        </div>

                                        <div class="col-md-6">
                                            <label class="form-label">Teléfono <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.telefono" type="text" class="form-control"
                                                    maxlength="9" @keypress="soloNumeros"
                                                    :class="{ 'is-invalid': telefonoInvalido }"
                                                    placeholder="Número de contacto">
                                                <span class="input-group-text"><i class="bi bi-phone"></i></span>
                                                <div v-if="telefonoInvalido" class="invalid-feedback">
                                                    El teléfono debe tener máximo 9 dígitos numéricos
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Sección de Datos de IPRESS -->
                            <div class="card mb-4 border-0 shadow-sm">
                                <div class="card-header bg-light">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <h6 class="mb-0 fw-bold"><i class="bi bi-building me-2"></i>Datos del
                                            Establecimiento</h6>
                                        <button @click="toggleEdicionCampos" class="btn btn-sm"
                                            :class="camposEditables ? 'btn-primary' : 'btn-outline-secondary'"
                                            :title="camposEditables ? 'Bloquear campos' : 'Editar manualmente'">
                                            <i class="fas me-1" :class="camposEditables ? 'fa-unlock' : 'fa-lock'"></i>
                                            {{ camposEditables ? 'Edición Activa' : 'Edición Bloqueada' }}
                                        </button>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="row g-3">
                                        <!-- Búsqueda por Nombre -->
                                        <div class="col-md-6 position-relative">
                                            <label class="form-label">Establecimiento <span
                                                    class="text-danger">*</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.establecimiento" type="text"
                                                    class="form-control" placeholder="Buscar por nombre" required
                                                    @input="(e) => handleIpressSearch('nombre', e)"
                                                    @focus="showNameSuggestions = true" @blur="hideNameSuggestions">
                                                <span class="input-group-text"><i class="bi bi-search"></i></span>
                                            </div>
                                            <div v-if="isSearchingByName"
                                                class="position-absolute top-50 end-0 translate-middle-y me-3">
                                                <span class="spinner-border spinner-border-sm text-primary"
                                                    role="status"></span>
                                            </div>
                                            <div v-if="showNameSuggestions && nameResults.length > 0"
                                                class="dropdown-menu show w-100 mt-1 shadow">
                                                <div v-for="item in nameResults" :key="item.COD_IPRESS"
                                                    class="dropdown-item" @mousedown="selectIpress(item)">
                                                    <div class="fw-bold">{{ item.NOMBRE }}</div>
                                                    <div class="small text-muted">
                                                        <span>Código: {{ item.COD_IPRESS }}</span> |
                                                        <span>Categoría: {{ item.CATEGORIA }}</span>
                                                    </div>
                                                    <div class="small text-muted">
                                                        {{ item.DEPARTAMENTO }} > {{ item.PROVINCIA }} > {{
                                                            item.DISTRITO }} - {{
                                                            item.DISA }} - {{ item.INSTITUCION }}
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="showNameSuggestions && nameResults.length === 0 && !isSearchingByName"
                                                class="dropdown-menu show w-100 mt-1">
                                                <div class="dropdown-item text-muted">No se encontraron resultados</div>
                                            </div>
                                        </div>

                                        <!-- Búsqueda por Código -->
                                        <div class="col-md-6 position-relative">
                                            <label class="form-label">Código Renipress <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.codigo" type="text" class="form-control"
                                                    placeholder="Buscar por código" @keypress="soloNumeros"
                                                    @input="(e) => handleIpressSearch('codigo', e)"
                                                    @focus="showCodeSuggestions = true" @blur="hideCodeSuggestions">
                                                <span class="input-group-text"><i class="bi bi-upc-scan"></i></span>
                                            </div>
                                            <div v-if="isSearchingByCode"
                                                class="position-absolute top-50 end-0 translate-middle-y me-3">
                                                <span class="spinner-border spinner-border-sm text-primary"
                                                    role="status"></span>
                                            </div>
                                            <div v-if="showCodeSuggestions && codeResults.length > 0"
                                                class="dropdown-menu show w-100 mt-1 shadow">
                                                <div v-for="item in codeResults" :key="item.COD_IPRESS"
                                                    class="dropdown-item" @mousedown="selectIpress(item)">
                                                    <div class="fw-bold">{{ item.NOMBRE }}</div>
                                                    <div class="small text-muted">
                                                        <span>Código: {{ item.COD_IPRESS }}</span> |
                                                        <span>Categoría: {{ item.CATEGORIA }}</span>
                                                    </div>
                                                    <div class="small text-muted">
                                                        {{ item.DEPARTAMENTO }} > {{ item.PROVINCIA }} > {{
                                                            item.DISTRITO }} - {{
                                                            item.DISA }} - {{ item.INSTITUCION }}
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="showCodeSuggestions && codeResults.length === 0 && !isSearchingByCode"
                                                class="dropdown-menu show w-100 mt-1">
                                                <div class="dropdown-item text-muted">No se encontraron resultados</div>
                                            </div>
                                        </div>

                                        <!-- Resto de campos (se autocompletarán) -->
                                        <div class="col-md-4">
                                            <label class="form-label">Categoría <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.categoria" type="text" class="form-control"
                                                    :readonly="!camposEditables"
                                                    placeholder="Categoría del establecimiento">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>

                                        <div class="col-md-4">
                                            <label class="form-label">Departamento <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.departamento" type="text"
                                                    class="form-control" :readonly="!camposEditables"
                                                    placeholder="Departamento">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>

                                        <div class="col-md-4">
                                            <label class="form-label">Provincia <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.provincia" type="text" class="form-control"
                                                    :readonly="!camposEditables" placeholder="Provincia">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>

                                        <div class="col-md-4">
                                            <label class="form-label">Distrito <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.distrito" type="text" class="form-control"
                                                    :readonly="!camposEditables" placeholder="Distrito">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>

                                        <div class="col-md-4">
                                            <label class="form-label">DISA <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.disa" type="text" class="form-control"
                                                    :readonly="!camposEditables" placeholder="DISA">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>

                                        <div class="col-md-4">
                                            <label class="form-label">Institución <span
                                                    class="text-muted">(Opcional)</span></label>
                                            <div class="input-group">
                                                <input v-model="participante.institucion" type="text"
                                                    class="form-control" :readonly="!camposEditables"
                                                    placeholder="Institución">
                                                <span class="input-group-text">
                                                    <span class="badge"
                                                        :class="camposEditables ? 'bg-primary' : 'bg-secondary'">
                                                        <i class="fas me-1"
                                                            :class="camposEditables ? 'fa-lock-open' : 'fa-lock'"></i>
                                                    </span>
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Sección de Firma Digital -->
                            <div class="card mb-4 border-0 shadow-sm">
                                <div class="card-header bg-light">
                                    <h6 class="mb-0 fw-bold"><i class="bi bi-pen me-2"></i>Firma Digital</h6>
                                </div>
                                <div class="card-body">
                                    <div class="alert alert-info mb-3">
                                        <i class="bi bi-info-circle me-2"></i>
                                        Por favor, firme en el área designada para validar su asistencia.
                                    </div>

                                    <SignaturePad ref="signaturePad" @save="handleSignatureSave" class="mb-3" />

                                    <div v-if="firmaGuardada" class="alert alert-success d-flex align-items-center">
                                        <i class="bi bi-check-circle-fill me-2"></i>
                                        <span>Firma capturada correctamente</span>
                                    </div>

                                    <div class="d-flex justify-content-between">
                                        <!--  <button type="button" class="btn btn-outline-danger" @click="limpiarFirma">
                                            <i class="bi bi-eraser me-1"></i> Limpiar Firma
                                        </button>

                                        <button type="button" class="btn btn-outline-primary" @click="guardarFirma">
                                            <i class="bi bi-save me-1"></i> Guardar Firma
                                        </button> -->
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex justify-content-end gap-2">
                                <button type="button" class="btn btn-outline-secondary" @click="resetearFormulario">
                                    <i class="bi bi-eraser me-1"></i> Limpiar
                                </button>
                                <button type="submit" class="btn btn-primary" :disabled="!firmaGuardada">
                                    <i class="bi bi-save me-1"></i> Guardar Participante
                                </button>
                            </div>
                        </fieldset>
                    </form>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { api } from '@/components/services/auth_axios'
import { useToast } from 'vue-toast-notification'
import { debounce } from 'lodash'
import SignaturePad from '@/components/SignaturePad.vue'

const toast = useToast()

// Variables para la firma
const signaturePad = ref(null)
const firmaBase64 = ref(null)
const firmaGuardada = ref(false)

// Configuración de estados
const estadosColores = {
    PENDIENTE: 'warning',
    EN_PROGRESO: 'primary',
    FINALIZADO: 'success'
}

const estadosTexto = {
    PENDIENTE: 'Pendiente',
    EN_PROGRESO: 'En Progreso',
    FINALIZADO: 'Finalizado'
}

// Estado del componente
const paso = ref(1)
const eventos = ref([])
const eventoSeleccionado = ref(null)
let intervaloActualizacion = null

// Búsqueda y filtros
const terminoBusqueda = ref('')
const mostrarFinalizados = ref(false)

// Búsqueda de IPRESS
const nameResults = ref([])
const codeResults = ref([])
const showNameSuggestions = ref(false)
const showCodeSuggestions = ref(false)
const isSearchingByName = ref(false)
const isSearchingByCode = ref(false)
const camposEditables = ref(false)

// Datos del participante
const participante = ref({
    dni: '',
    nombre: '',
    apellido: '',
    cargo: '',
    email: '',
    telefono: '',
    tipo: 'EESS',
    establecimiento: '',
    codigo: '',
    categoria: '',
    departamento: '',
    provincia: '',
    distrito: '',
    disa: '',
    institucion: '',
    eventos: []
})

// Métodos para manejar la firma
const handleSignatureSave = (signatureData) => {
    firmaBase64.value = signatureData
    firmaGuardada.value = true
    toast.success('Firma guardada correctamente')
}

const limpiarFirma = () => {
    if (signaturePad.value) {
        signaturePad.value.clear()
        firmaBase64.value = null
        firmaGuardada.value = false
    }
}

const guardarFirma = () => {
    if (!signaturePad.value) {
        toast.warning('No se encontró el componente de firma')
        return
    }

    try {
        // Verificar si el canvas está vacío
        if (signaturePad.value.isCanvasEmpty()) {
            toast.warning('Por favor, realice una firma antes de guardar')
            return
        }

        // Disparar el evento save del componente hijo
        signaturePad.value.save()
    } catch (error) {
        console.error('Error al guardar firma:', error)
        toast.error('Error al guardar la firma')
    }
}

// Computed para validaciones
const dniInvalido = computed(() => {
    return participante.value.dni && !/^\d{8}$/.test(participante.value.dni)
})

const telefonoInvalido = computed(() => {
    return participante.value.telefono && !/^\d{0,9}$/.test(participante.value.telefono)
})

// Eventos filtrados y ordenados
const eventosFiltrados = computed(() => {
    let resultados = [...eventos.value]

    // Filtrar por término de búsqueda
    if (terminoBusqueda.value) {
        const termino = terminoBusqueda.value.toLowerCase()
        resultados = resultados.filter(evento =>
            evento.descripcion.toLowerCase().includes(termino) ||
            (evento.creado_por && evento.creado_por.toLowerCase().includes(termino))
        )
    }

    // Filtrar por estado
    if (!mostrarFinalizados.value) {
        resultados = resultados.filter(evento => evento.estado !== 'FINALIZADO')
    }

    // Ordenar por proximidad
    resultados.sort((a, b) => {
        const fechaHoraA = new Date(`${a.fecha}T${a.hora_inicio}`).getTime()
        const fechaHoraB = new Date(`${b.fecha}T${b.hora_inicio}`).getTime()
        const ahora = new Date().getTime()

        const diffA = Math.abs(fechaHoraA - ahora)
        const diffB = Math.abs(fechaHoraB - ahora)

        if (a.estado === 'EN_PROGRESO' && b.estado !== 'EN_PROGRESO') return -1
        if (b.estado === 'EN_PROGRESO' && a.estado !== 'EN_PROGRESO') return 1

        return diffA - diffB
    })

    return resultados
})

// Cargar eventos al montar el componente
onMounted(async () => {
    await cargarEventos()
    iniciarActualizacionAutomatica()
})

// Iniciar actualización automática de estados
const iniciarActualizacionAutomatica = () => {
    if (intervaloActualizacion) clearInterval(intervaloActualizacion)

    intervaloActualizacion = setInterval(async () => {
        await actualizarEstadosEventos()
    }, 30000) // Actualizar cada 30 segundos
}

// Cargar eventos desde la API
const cargarEventos = async () => {
    try {
        const response = await api.get('reuniones/evento/')
        eventos.value = response.data.map(evento => ({
            ...evento,
            estado: evento.estado || 'PENDIENTE'
        }))
        await actualizarEstadosEventos()
    } catch (error) {
        mostrarError('Error al cargar eventos', error)
    }
}

// Actualizar estados de todos los eventos
const actualizarEstadosEventos = async () => {
    try {
        const response = await api.post('reuniones/evento/actualizar_estados/')
        eventos.value = response.data

        if (eventoSeleccionado.value) {
            const eventoActualizado = response.data.find(e => e.id === eventoSeleccionado.value.id)
            if (eventoActualizado) {
                eventoSeleccionado.value = eventoActualizado
            }
        }
    } catch (error) {
        console.error('Error en actualización de estados:', error)
    }
}

// Formatear fecha
const formatFecha = (fecha) => {
    const [year, month, day] = fecha.split('-')
    const fechaObj = new Date(year, month - 1, day)

    return fechaObj.toLocaleDateString('es-PE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
}

// Formatear hora
const formatHora = (hora) => {
    const [hh, mm] = hora.split(':')
    return `${hh}:${mm}`
}

// Seleccionar evento
const seleccionarEvento = (evento) => {
    if (evento.estado !== 'EN_PROGRESO') {
        toast.warning('Solo se pueden registrar participantes en eventos en progreso')
        return
    }
    eventoSeleccionado.value = { ...evento }
    paso.value = 2
}

// Registrar participante
const registrarParticipante = async () => {
    try {
        // Validaciones básicas
        if (eventoSeleccionado.value.estado !== 'EN_PROGRESO') {
            toast.error('Solo se pueden registrar participantes en eventos en progreso')
            return
        }

        if (dniInvalido.value || !participante.value.dni || !participante.value.nombre ||
            !participante.value.apellido || !participante.value.cargo || !participante.value.establecimiento) {
            toast.error('Por favor complete todos los campos obligatorios correctamente')
            return
        }

        if (!firmaGuardada.value) {
            toast.error('Por favor proporcione su firma digital')
            return
        }

        // Verificar DNI duplicado en el evento
        try {
            const response = await api.get(`reuniones/persona/verificar_dni_evento/?dni=${participante.value.dni}&evento_id=${eventoSeleccionado.value.id}`)
            if (response.data.existe) {
                toast.error('Este DNI ya está registrado en este evento')
                return
            }
        } catch (error) {
            console.error('Error verificando DNI:', error)
        }

        // Crear FormData para enviar la firma como archivo
        const formData = new FormData()

        // Agregar campos del participante
        Object.keys(participante.value).forEach(key => {
            if (key !== 'eventos') {
                formData.append(key, participante.value[key])
            }
        })

        // Agregar evento
        formData.append('eventos', eventoSeleccionado.value.id)

        // Convertir y agregar la firma
        if (firmaBase64.value) {
            const blob = dataURLtoBlob(firmaBase64.value)
            formData.append('firma', blob, 'firma.png')
        }

        // Enviar datos
        await api.post('reuniones/persona/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        toast.success('Participante registrado correctamente')
        resetearFormulario()
        volverAListado()
    } catch (error) {
        mostrarError('Error al registrar participante', error)
    }
}

// Convertir DataURL a Blob
const dataURLtoBlob = (dataURL) => {
    const arr = dataURL.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)

    while (n--) {
        u8arr[n] = bstr.charCodeAt(n)
    }

    return new Blob([u8arr], { type: mime })
}

// Volver al listado
const volverAListado = () => {
    paso.value = 1
    resetearFormulario()
}

// Resetear formulario
const resetearFormulario = () => {
    participante.value = {
        dni: '',
        nombre: '',
        apellido: '',
        cargo: '',
        email: '',
        telefono: '',
        tipo: 'EESS',
        establecimiento: '',
        codigo: '',
        categoria: '',
        departamento: '',
        provincia: '',
        distrito: '',
        disa: '',
        institucion: '',
        eventos: []
    }
    firmaBase64.value = null
    firmaGuardada.value = false
    camposEditables.value = false

    if (signaturePad.value) {
        signaturePad.value.clear()
    }
}

// Mostrar error
const mostrarError = (mensaje, error) => {
    toast.error(`${mensaje}: ${error.response?.data?.detail || error.message}`)
    console.error(mensaje, error)
}

// Limpiar intervalo al desmontar
onBeforeUnmount(() => {
    if (intervaloActualizacion) clearInterval(intervaloActualizacion)
})

// Búsqueda de IPRESS
const searchIpress = async (type, inputValue) => {
    if (!inputValue) return []

    if (type === 'nombre') isSearchingByName.value = true
    else isSearchingByCode.value = true

    try {
        const params = new URLSearchParams()
        params.append('limit', '10')

        if (type === 'nombre') {
            params.append('q', inputValue)
        } else {
            const codigo = parseInt(inputValue)
            if (isNaN(codigo)) return []
            params.append('COD_IPRESS', codigo.toString())
        }

        const response = await api.get('ficha/renipress/', {
            params,
            paramsSerializer: params => params.toString()
        })

        if (!response.data?.result?.records) return []

        return response.data.result.records.map(item => ({
            ...item,
            COD_IPRESS: item.COD_IPRESS?.toString() || '',
            CATEGORIA: item.CATEGORIA || 'Sin categoría',
            DEPARTAMENTO: item.DEPARTAMENTO || 'Sin departamento',
            PROVINCIA: item.PROVINCIA || 'Sin provincia',
            DISTRITO: item.DISTRITO || 'Sin distrito',
            DISA: item.DISA || 'Sin DISA',
            INSTITUCION: item.INSTITUCION || 'Sin Institución'
        }))

    } catch (error) {
        console.error('Error en búsqueda:', error)
        toast.error('Error al buscar IPRESS')
        return []
    } finally {
        if (type === 'nombre') isSearchingByName.value = false
        else isSearchingByCode.value = false
    }
}

// Seleccionar IPRESS
const selectIpress = (item) => {
    participante.value = {
        ...participante.value,
        establecimiento: item.NOMBRE,
        codigo: item.COD_IPRESS,
        categoria: item.CATEGORIA,
        departamento: item.DEPARTAMENTO || '',
        provincia: item.PROVINCIA || '',
        distrito: item.DISTRITO || '',
        disa: item.DISA || '',
        institucion: item.INSTITUCION || ''
    }
    camposEditables.value = false
    showNameSuggestions.value = false
    showCodeSuggestions.value = false
}

// Manejar búsqueda con debounce
const handleIpressSearch = debounce(async (type, event) => {
    const inputValue = event.target.value.trim()

    if (type === 'codigo' && inputValue.length < 1) {
        codeResults.value = []
        return
    }
    if (type === 'nombre' && inputValue.length < 2) {
        nameResults.value = []
        return
    }

    const results = await searchIpress(type, inputValue)

    if (type === 'nombre') {
        nameResults.value = results
    } else {
        codeResults.value = results
    }
}, 300)

// Validar solo números en DNI y teléfono
const soloNumeros = (event) => {
    const charCode = event.keyCode || event.which
    const charStr = String.fromCharCode(charCode)

    if (!/^\d+$/.test(charStr)) {
        event.preventDefault()
    }
}

// Ocultar sugerencias con retraso
const hideNameSuggestions = () => {
    setTimeout(() => {
        showNameSuggestions.value = false
    }, 200)
}

const hideCodeSuggestions = () => {
    setTimeout(() => {
        showCodeSuggestions.value = false
    }, 200)
}

// Toggle para edición de campos
const toggleEdicionCampos = () => {
    camposEditables.value = !camposEditables.value

    if (!camposEditables.value) {
        toast.info('Campos bloqueados para edición')
    } else {
        toast.warning('Modo edición manual activado')
    }
}
</script>

<style scoped>
/* Estilos generales */
.card {
    max-width: 1200px;
    margin: 0 auto;
}

.list-group-item {
    transition: all 0.2s ease;
    position: relative;
}

.list-group-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Estilos para dropdowns de búsqueda */
.dropdown-item {
    cursor: pointer;
    white-space: normal;
    padding: 0.5rem 1rem;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.dropdown-menu {
    max-height: 300px;
    overflow-y: auto;
}

/* Estilos para campos editables */
input:not(:read-only) {
    background-color: #fff;
    border-color: #86b7fe;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}

/* Badges y estados */
.badge {
    font-size: 0.75em;
    letter-spacing: 0.5px;
}

.pe-none {
    pointer-events: none;
    opacity: 0.8;
    cursor: not-allowed;
}

/* Bordes de estado */
.border-warning {
    border-left-color: #ffc107 !important;
}

.border-primary {
    border-left-color: #0d6efd !important;
}

.border-success {
    border-left-color: #198754 !important;
}

/* Estilos específicos para el área de firma */
.signature-container {
    border: 1px dashed #dee2e6;
    border-radius: 8px;
    background-color: #f8f9fa;
    margin-bottom: 1rem;
    position: relative;
}

.signature-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
}

/* Animación para mensajes */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

/* Responsividad */
@media (max-width: 768px) {
    .card-body {
        padding: 1rem;
    }

    .row.g-3>[class*="col-"] {
        margin-bottom: 1rem;
    }

    .signature-actions {
        flex-direction: column;
        gap: 0.5rem;
    }

    .signature-actions button {
        width: 100%;
    }
}

/* Estilos para el canvas de firma */
.signature-canvas {
    width: 100%;
    height: 200px;
    background-color: white;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    touch-action: none;
    cursor: crosshair;
}
</style>
<template>
    <main id="main" class="main">
        <div class="card">
            <div class="card-body">
                <!-- Paso 1: Selección de Evento -->
                <div v-if="paso === 1">
                    <h5 class="card-title">Seleccione un Evento</h5>
                    <div class="list-group">
                        <button v-for="evento in eventos" :key="evento.id" @click="seleccionarEvento(evento)"
                            class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">{{ evento.descripcion }}</h6>
                                <small>{{ formatFecha(evento.fecha) }}</small>
                            </div>
                            <p class="mb-1">Horario: {{ formatHoraPeru(evento.hora_inicio) }} - {{
                                formatHoraPeru(evento.hora_fin) }}</p>
                            <small>Creado por: {{ evento.creado_por }}</small>
                        </button>
                    </div>
                </div>

                <!-- Paso 2: Registro de Participantes -->
                <div v-if="paso === 2">
                    <h5 class="card-title">Registrar Participante para: {{ eventoSeleccionado.descripcion }}</h5>

                    <form @submit.prevent="registrarParticipante">
                        <div class="row mb-3">
                            <label class="col-sm-2 col-form-label">DNI</label>
                            <div class="col-sm-10">
                                <input v-model="participante.dni" type="text" class="form-control" required>
                            </div>
                        </div>

                        <div class="row mb-3">
                            <label class="col-sm-2 col-form-label">Nombre</label>
                            <div class="col-sm-10">
                                <input v-model="participante.nombre" type="text" class="form-control" required>
                            </div>
                        </div>

                        <div class="row mb-3">
                            <label class="col-sm-2 col-form-label">Apellido</label>
                            <div class="col-sm-10">
                                <input v-model="participante.apellido" type="text" class="form-control" required>
                            </div>
                        </div>

                        <div class="row mb-3">
                            <label class="col-sm-2 col-form-label">Email</label>
                            <div class="col-sm-10">
                                <input v-model="participante.email" type="email" class="form-control">
                            </div>
                        </div>

                        <div class="row mb-3">
                            <label class="col-sm-2 col-form-label">Teléfono</label>
                            <div class="col-sm-10">
                                <input v-model="participante.telefono" type="text" class="form-control">
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-sm-10 offset-sm-2">
                                <button type="submit" class="btn btn-primary me-2">Guardar</button>
                                <button @click="volverAListado" type="button" class="btn btn-secondary">Volver</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/components/services/auth_axios';
import { useToast } from 'vue-toast-notification';

const toast = useToast()

// Estado del componente
const paso = ref(1) // 1 = selección evento, 2 = registro participante
const eventos = ref([])
const eventoSeleccionado = ref(null)

// Datos del participante
const participante = ref({
    dni: '',
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    eventos: [] // Aquí guardaremos el ID del evento seleccionado
})

// Cargar eventos al montar el componente
onMounted(async () => {
    try {
        const response = await api.get('reuniones/evento/')
        eventos.value = response.data
    } catch (error) {
        toast.error('Error al cargar los eventos: ' + error.message)
        console.error('Error fetching eventos:', error)
    }
})

// Formatear fecha para mostrar
const formatFecha = (fecha) => {
    // Crear fecha en UTC (asumiendo que el backend envía fechas en UTC)
    const fechaUTC = new Date(fecha + 'T00:00:00Z');

    // Ajustar a hora peruana (UTC-5)
    const fechaLima = new Date(fechaUTC.getTime() - (5 * 60 * 60 * 1000));

    return fechaLima.toLocaleDateString('es-PE', {
        timeZone: 'America/Lima',
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
const formatHoraPeru = (horaUTC) => {
    // Extraer horas y minutos de la hora UTC
    const [hh, mm] = horaUTC.split(':');

    // Crear fecha ficticia para el cálculo
    const fecha = new Date(`2000-01-01T${hh}:${mm}:00Z`);

    // Ajustar a hora peruana (UTC-5)
    fecha.setHours(fecha.getHours() - 5);

    // Formatear como HH:MM en 24 horas
    return fecha.toLocaleTimeString('es-PE', {
        timeZone: 'America/Lima',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}
// Seleccionar un evento
const seleccionarEvento = (evento) => {
    eventoSeleccionado.value = evento
    paso.value = 2
}

// Volver al listado de eventos
const volverAListado = () => {
    paso.value = 1
    resetearFormulario()
}

// Registrar participante
const registrarParticipante = async () => {
    try {
        // Asignar el evento seleccionado
        participante.value.eventos = [eventoSeleccionado.value.id]

        const response = await api.post('reuniones/persona/', participante.value)

        toast.success('Participante registrado correctamente')
        resetearFormulario()
    } catch (error) {
        toast.error('Error al registrar participante: ' + (error.response?.data?.detail || error.message))
        console.error('Error:', error)
    }
}

// Resetear formulario
const resetearFormulario = () => {
    participante.value = {
        dni: '',
        nombre: '',
        apellido: '',
        email: '',
        telefono: '',
        eventos: []
    }
}
</script>

<style scoped>
.card {
    max-width: 800px;
    margin: 0 auto;
}

.list-group-item {
    cursor: pointer;
    transition: all 0.3s;
}

.list-group-item:hover {
    background-color: #f8f9fa;
}
</style>
<template>
  <main id="main" class="main">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Registro de Persona</h5>

        <form @submit.prevent="submitForm">
          <!-- Datos básicos -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">DNI</label>
            <div class="col-sm-10">
              <input v-model="persona.dni" type="text" class="form-control" required>
            </div>
          </div>

          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Nombre</label>
            <div class="col-sm-10">
              <input v-model="persona.nombre" type="text" class="form-control" required>
            </div>
          </div>

          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Apellido</label>
            <div class="col-sm-10">
              <input v-model="persona.apellido" type="text" class="form-control" required>
            </div>
          </div>

          <!-- Contacto -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-10">
              <input v-model="persona.email" type="email" class="form-control">
            </div>
          </div>

          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Teléfono</label>
            <div class="col-sm-10">
              <input v-model="persona.telefono" type="text" class="form-control">
            </div>
          </div>

          <!-- Selección de Eventos -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Eventos</label>
            <div class="col-sm-10">
              <select v-model="selectedEventos" multiple class="form-select">
                <option v-for="evento in eventosDisponibles" :key="evento.id" :value="evento.id">
                  {{ evento.descripcion }} - {{ evento.fecha }}
                </option>
              </select>
              <small class="text-muted">Mantén presionado Ctrl para seleccionar múltiples eventos</small>
            </div>
          </div>

          <!-- Botón de envío -->
          <div class="row mb-3">
            <div class="col-sm-10 offset-sm-2">
              <button type="submit" class="btn btn-primary">Registrar</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/components/services/auth_axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification';

const toast = useToast()
const router = useRouter()

// Datos de la persona
const persona = ref({
  dni: '',
  nombre: '',
  apellido: '',
  email: '',
  telefono: '',
  eventos: []
})

// Lista de eventos disponibles
const eventosDisponibles = ref([])
const selectedEventos = ref([])

// Cargar eventos disponibles al montar el componente
onMounted(async () => {
  try {
    const response = await api.get('reuniones/evento/')
    eventosDisponibles.value = response.data
  } catch (error) {
    toast.error('Error al cargar los eventos: ' + error.message)
    console.error('Error fetching eventos:', error)
  }
})

// Enviar formulario
const submitForm = async () => {
  try {
    // Asignar los eventos seleccionados
    persona.value.eventos = selectedEventos.value
    
    const response = await api.post('reuniones/persona/', persona.value)
    
    toast.success('Persona registrada correctamente')
    router.push('/personas')  // Redirigir a la lista de personas
  } catch (error) {
    toast.error('Error al registrar persona: ' + error.response?.data?.detail || error.message)
    console.error('Error submitting form:', error)
  }
}
</script>

<style scoped>
.card {
  max-width: 800px;
  margin: 0 auto;
}
select[multiple] {
  height: auto;
  min-height: 120px;
}
</style>
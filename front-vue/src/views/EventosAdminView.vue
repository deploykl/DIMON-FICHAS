<template>
  <main id="main" class="main">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Crear Nuevo Evento</h5>

        <form @submit.prevent="crearEvento">
          <!-- Descripción -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Descripción</label>
            <div class="col-sm-10">
              <textarea v-model="evento.descripcion" class="form-control" rows="3" required></textarea>
            </div>
          </div>

          <!-- Fecha -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Fecha</label>
            <div class="col-sm-10">
              <input v-model="evento.fecha" type="date" class="form-control" required>
            </div>
          </div>

          <!-- Horario -->
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Horario</label>
            <div class="col-sm-5">
              <label class="form-label">Hora de inicio</label>
              <input v-model="evento.hora_inicio" type="time" class="form-control" step="300" required>
            </div>
            <div class="col-sm-5">
              <label class="form-label">Hora de fin</label>
              <input v-model="evento.hora_fin" type="time" class="form-control" step="300" required>
            </div>
          </div>

          <!-- Botones -->
          <div class="row mb-3">
            <div class="col-sm-10 offset-sm-2">
              <button type="submit" class="btn btn-primary">Guardar Evento</button>
              <button type="button" class="btn btn-secondary ms-2" @click="limpiarFormulario">Limpiar</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/components/services/auth_axios';
import { useToast } from 'vue-toast-notification';
import { useRouter } from 'vue-router'

const toast = useToast()
const router = useRouter()

// Datos del evento
const evento = ref({
  descripcion: '',
  fecha: '',
  hora_inicio: '09:00',
  hora_fin: '17:00'
})

// Crear evento
const crearEvento = async () => {
  try {
    // Validar que la hora de fin sea mayor a la de inicio
    if (evento.value.hora_fin <= evento.value.hora_inicio) {
      toast.error('La hora de fin debe ser mayor a la hora de inicio')
      return
    }

    const response = await api.post('reuniones/evento/', evento.value)
    
    toast.success('Evento creado correctamente')
    router.push('/eventos') // Redirigir al listado de eventos
  } catch (error) {
    toast.error('Error al crear evento: ' + (error.response?.data?.detail || error.message))
    console.error('Error:', error)
  }
}

// Limpiar formulario
const limpiarFormulario = () => {
  evento.value = {
    descripcion: '',
    fecha: '',
    hora_inicio: '09:00',
    hora_fin: '17:00'
  }
}

// Establecer fecha mínima como hoy
const today = new Date().toISOString().split('T')[0]
</script>

<style scoped>
.card {
  max-width: 800px;
  margin: 0 auto;
}

/* Estilo para los inputs de tiempo */
input[type="time"]::-webkit-calendar-picker-indicator {
  filter: invert(0.5);
}
</style>
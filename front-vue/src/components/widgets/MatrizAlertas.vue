<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h3 class="card-title mb-0">Alertas de Matrices de Compromiso</h3>
        <div>
          <button 
            @click="enviarAlertasManualmente" 
            class="btn btn-sm btn-warning me-2"
            :disabled="enviandoManual"
          >
            <span v-if="enviandoManual">
              <i class="fas fa-spinner fa-spin"></i> Enviando...
            </span>
            <span v-else>
              <i class="fas fa-paper-plane"></i> Enviar alertas manualmente
            </span>
          </button>
          <button @click="fetchAlertas" class="btn btn-sm btn-light">
            <i class="fas fa-sync"></i> Actualizar
          </button>
        </div>
      </div>
      
      <div class="card-body">
        <!-- Contenido existente de alertas -->
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
          <p class="mt-2">Cargando alertas...</p>
        </div>
        
        <div v-else>
          <div v-if="alertas.length === 0" class="alert alert-info">
            No hay alertas pendientes en este momento.
          </div>
          
          <div v-else class="alertas-list">
            <div v-for="alerta in alertas" :key="alerta.id" class="alert mb-3" :class="{
              'alert-danger': alerta.urgencia === 'alta',
              'alert-warning': alerta.urgencia === 'media',
              'alert-info': alerta.urgencia === 'baja'
            }">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <h4>
                    <span v-if="alerta.urgencia === 'alta'">🚨</span>
                    <span v-else-if="alerta.urgencia === 'media'">⚠️</span>
                    <span v-else>⏰</span>
                    {{ alerta.establecimiento }} ({{ alerta.codigo }})
                  </h4>
                  <p><strong>Fecha límite:</strong> {{ alerta.plazo_fin }} ({{ alerta.dias_restantes }} días restantes)</p>
                  <p><strong>Última alerta:</strong> {{ alerta.ultima_alerta || 'No enviada' }}</p>
                  <p><strong>Compromisos:</strong> {{ alerta.medidas_correctivas }}</p>
                </div>
                <div class="d-flex flex-column">
                  <button 
                    @click="enviarAlertaIndividual(alerta.id)" 
                    class="btn btn-sm btn-outline-warning mb-2"
                    :disabled="enviandoIndividual === alerta.id"
                  >
                    <span v-if="enviandoIndividual === alerta.id">
                      <i class="fas fa-spinner fa-spin"></i> Enviando
                    </span>
                    <span v-else>
                      <i class="fas fa-paper-plane"></i> Reenviar alerta
                    </span>
                  </button>
                  <button @click="marcarComoLeida(alerta.id)" class="btn btn-sm btn-outline-primary mb-2">
                    <i class="fas fa-check"></i> Marcar como leída
                  </button>
                  <button @click="verMatriz(alerta.id)" class="btn btn-sm btn-primary">
                    <i class="fas fa-eye"></i> Ver detalles
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'MatrizAlertas',
  emits: ['update-count', 'close-modal'],
  setup(props, { emit }) {
    const alertas = ref([])
    const loading = ref(true)
    const enviandoManual = ref(false)
    const enviandoIndividual = ref(null)
    const router = useRouter()

    const fetchAlertas = async () => {
      try {
        loading.value = true
        const response = await axios.get('/matriz-compromiso/alertas/')
        alertas.value = response.data
        emit('update-count', alertas.value.length)
      } catch (error) {
        console.error('Error al cargar alertas:', error)
        // Opcional: Mostrar mensaje de error al usuario
      } finally {
        loading.value = false
      }
    }

    const marcarComoLeida = async (matrizId) => {
      try {
        await axios.post(`/matriz-compromiso/${matrizId}/marcar-leida/`)
        console.log('Alerta marcada como leída')
        fetchAlertas()
      } catch (error) {
        console.error('Error al marcar como leída:', error)
      }
    }

    const enviarAlertasManualmente = async () => {
      try {
        enviandoManual.value = true
        const response = await axios.post('/matriz-compromiso/enviar-alertas/')
        console.log('Alertas enviadas:', response.data)
        fetchAlertas()
      } catch (error) {
        console.error('Error al enviar alertas:', error)
      } finally {
        enviandoManual.value = false
      }
    }

    const enviarAlertaIndividual = async (matrizId) => {
      try {
        enviandoIndividual.value = matrizId
        const response = await axios.post(`/matriz-compromiso/${matrizId}/enviar-alerta/`)
        console.log('Alerta individual enviada:', response.data)
        fetchAlertas()
      } catch (error) {
        console.error('Error al enviar alerta individual:', error)
      } finally {
        enviandoIndividual.value = null
      }
    }

    const verMatriz = (matrizId) => {
      emit('close-modal')
      router.push(`/matrices/${matrizId}`)
    }

    onMounted(() => {
      fetchAlertas()
      // Actualizar cada 5 minutos
      const intervalId = setInterval(fetchAlertas, 300000)
      
      // Limpiar intervalo al desmontar el componente
      return () => clearInterval(intervalId)
    })

    return {
      alertas,
      loading,
      enviandoManual,
      enviandoIndividual,
      fetchAlertas,
      marcarComoLeida,
      enviarAlertasManualmente,
      enviarAlertaIndividual,
      verMatriz
    }
  }
}
</script>

<style scoped>
.alertas-list {
  max-height: 70vh;
  overflow-y: auto;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}
</style>
<template>
  <div>
    <form @submit.prevent="guardarSeguimiento">
      <!-- Campos existentes -->
      <div class="form-group">
        <label>Fecha y Hora de Seguimiento</label>
        <input type="datetime-local" v-model="seguimiento.fecha_seguimiento" required>
      </div>
      
      <div class="form-group">
        <label>Estado</label>
        <textarea v-model="seguimiento.estado" required></textarea>
      </div>
      
      <div class="form-group">
        <label>Análisis/Acción realizada</label>
        <textarea v-model="seguimiento.analisis_accion" required></textarea>
      </div>
      
      <!-- Configuración de envío -->
      <div class="form-group">
        <label>Frecuencia de envío</label>
        <select v-model="seguimiento.frecuencia_envio" @change="handleFrecuenciaChange">
          <option value="diario">Diario</option>
          <option value="2dias">Cada 2 días</option>
          <option value="3dias">Cada 3 días</option>
          <option value="semanal">Semanal</option>
          <option value="mensual">Mensual</option>
          <option value="personalizado">Personalizado</option>
        </select>
      </div>
      
      <div class="form-group" v-if="seguimiento.frecuencia_envio === 'personalizado'">
        <label>Días personalizados</label>
        <input type="number" v-model="seguimiento.dias_personalizados" min="1">
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="seguimiento.enviar_email"> Enviar por correo
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="seguimiento.enviar_telegram"> Enviar por Telegram
        </label>
      </div>
      
      <button type="submit" class="btn btn-primary">Guardar y Programar</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      seguimiento: {
        fecha_seguimiento: '',
        estado: '',
        analisis_accion: '',
        frecuencia_envio: 'diario',
        dias_personalizados: null,
        enviar_email: true,
        enviar_telegram: true,
        alerta_id: this.$route.params.alertaId // Asumiendo que pasas el ID de la alerta
      }
    }
  },
  methods: {
    handleFrecuenciaChange() {
      if (this.seguimiento.frecuencia_envio !== 'personalizado') {
        this.seguimiento.dias_personalizados = null
      }
    },
    async guardarSeguimiento() {
      try {
        const response = await this.$axios.post('/api/seguimiento-alertas/', this.seguimiento)
        this.$notify({
          title: 'Éxito',
          message: 'Seguimiento guardado y programado correctamente',
          type: 'success'
        })
        this.$router.push(`/alertas/${this.seguimiento.alerta_id}`)
      } catch (error) {
        this.$notify.error({
          title: 'Error',
          message: 'Ocurrió un error al guardar el seguimiento'
        })
      }
    }
  }
}
</script>
<template>
  <main id="main" class="main">
     <div class="enlace-viewer">
    <div class="viewer-header">
      <button @click="closeViewer" class="btn btn-outline-light">
        <i class="fas fa-arrow-left me-2"></i> Volver
      </button>
      <h2>Dashboard</h2>
    </div>
    
    <div class="viewer-content">
      <iframe 
        v-if="currentEnlace.url"
        :src="currentEnlace.url"
        frameborder="0"
        allowfullscreen
        class="enlace-iframe"
      ></iframe>
      
      <div v-else class="alert alert-warning">
        No hay URL disponible para este enlace
      </div>
    </div>
  </div>
  </main>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios'

const route = useRoute()
const router = useRouter()
const currentEnlace = ref({})

onMounted(async () => {
  try {
    const response = await api.get(`enlace/urls/${route.params.id}/`)
    currentEnlace.value = response.data
  } catch (error) {
    console.error('Error cargando enlace:', error)
  }
})

const closeViewer = () => {
  router.go(-1) // O puedes redirigir a la lista: router.push('/enlaces')
}
</script>

<style scoped>
.enlace-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #f8f9fa;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.viewer-header {
  background: linear-gradient(135deg, #103c4b 0%, #1a5a6e 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.viewer-header h2 {
  margin: 0;
  flex-grow: 1;
  text-align: center;
}

.enlace-iframe {
  width: 100%;
  height: 100%;
  flex-grow: 1;
  border: none;
}

.viewer-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
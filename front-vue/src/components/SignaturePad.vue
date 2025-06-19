<!-- components/SignaturePad.vue -->
<template>
  <div class="signature-container">
    <canvas ref="canvas" :width="width" :height="height"></canvas>
    <div class="signature-actions">
      <button @click="clear" type="button" class="btn btn-sm btn-outline-secondary me-2">Limpiar</button>
      <button @click="save" type="button" class="btn btn-sm btn-primary">Guardar Firma</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  width: {
    type: Number,
    default: 300
  },
  height: {
    type: Number,
    default: 150
  }
})

const emit = defineEmits(['save'])

const canvas = ref(null)
let ctx = null
let isDrawing = false
let lastX = 0
let lastY = 0
let signatureData = null

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  ctx.strokeStyle = '#000'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  // Event listeners
  canvas.value.addEventListener('mousedown', startDrawing)
  canvas.value.addEventListener('mousemove', draw)
  canvas.value.addEventListener('mouseup', stopDrawing)
  canvas.value.addEventListener('mouseout', stopDrawing)
  
  // Touch support
  canvas.value.addEventListener('touchstart', handleTouchStart)
  canvas.value.addEventListener('touchmove', handleTouchMove)
  canvas.value.addEventListener('touchend', handleTouchEnd)
})

const startDrawing = (e) => {
  isDrawing = true
  const pos = getPosition(e)
  lastX = pos.x
  lastY = pos.y
}

const draw = (e) => {
  if (!isDrawing) return
  const pos = getPosition(e)
  
  ctx.beginPath()
  ctx.moveTo(lastX, lastY)
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
  
  lastX = pos.x
  lastY = pos.y
}

const stopDrawing = () => {
  isDrawing = false
}

const getPosition = (e) => {
  const rect = canvas.value.getBoundingClientRect()
  return {
    x: (e.clientX || e.touches[0].clientX) - rect.left,
    y: (e.clientY || e.touches[0].clientY) - rect.top
  }
}

const clear = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  signatureData = null
}

const save = () => {
  signatureData = canvas.value.toDataURL('image/png')
  emit('save', signatureData)
}

// Touch handlers
const handleTouchStart = (e) => {
  if (e.touches.length === 1) {
    e.preventDefault()
    startDrawing(e)
  }
}

const handleTouchMove = (e) => {
  if (e.touches.length === 1) {
    e.preventDefault()
    draw(e)
  }
}

const handleTouchEnd = (e) => {
  if (e.touches.length === 0) {
    e.preventDefault()
    stopDrawing()
  }
}
</script>

<style scoped>
canvas {
  background-color: #fff;
  border: 1px solid #ddd;
  touch-action: none; /* Important for touch devices */
}
</style>
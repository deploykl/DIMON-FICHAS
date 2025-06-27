<template>
  <div class="signature-pad-container">
    <div class="signature-header">
      <h4 class="signature-title">Firme aquí</h4>
      <div class="signature-guide">Deslice su dedo o use el mouse</div>
    </div>
    
    <div class="signature-canvas-wrapper">
      <canvas 
        ref="canvas" 
        :width="width" 
        :height="height" 
        class="signature-canvas"
        aria-label="Área para firmar"
      ></canvas>
      <div class="signature-watermark">Firma válida</div>
    </div>
    
    <div class="signature-actions">
      <button 
        @click="clear" 
        type="button" 
        class="btn-clear"
        aria-label="Limpiar firma"
      >
        <svg class="icon" viewBox="0 0 24 24">
          <path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
        </svg>
        <span>Limpiar</span>
      </button>
      
      <button 
        @click="save" 
        type="button" 
        class="btn-save"
        aria-label="Guardar firma"
      >
        <svg class="icon" viewBox="0 0 24 24">
          <path fill="currentColor" d="M15,9H5V5H15M12,19A3,3 0 0,1 9,16A3,3 0 0,1 12,13A3,3 0 0,1 15,16A3,3 0 0,1 12,19M17,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3Z" />
        </svg>
        <span>Guardar firma</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 200
  },
  penColor: {
    type: String,
    default: '#1a73e8'
  },
  penWidth: {
    type: Number,
    default: 2.5
  }
})

const emit = defineEmits(['save'])

const canvas = ref(null)
let ctx = null
let isDrawing = false
let lastX = 0
let lastY = 0
let signatureData = null
let resizeObserver = null

// Función para agregar event listeners
const addEventListeners = () => {
  if (!canvas.value) return
  
  canvas.value.addEventListener('mousedown', startDrawing)
  canvas.value.addEventListener('mousemove', draw)
  canvas.value.addEventListener('mouseup', stopDrawing)
  canvas.value.addEventListener('mouseout', stopDrawing)
  
  canvas.value.addEventListener('touchstart', handleTouchStart, { passive: false })
  canvas.value.addEventListener('touchmove', handleTouchMove, { passive: false })
  canvas.value.addEventListener('touchend', handleTouchEnd)
}

// Función para remover event listeners
const removeEventListeners = () => {
  if (!canvas.value) return
  
  canvas.value.removeEventListener('mousedown', startDrawing)
  canvas.value.removeEventListener('mousemove', draw)
  canvas.value.removeEventListener('mouseup', stopDrawing)
  canvas.value.removeEventListener('mouseout', stopDrawing)
  
  canvas.value.removeEventListener('touchstart', handleTouchStart)
  canvas.value.removeEventListener('touchmove', handleTouchMove)
  canvas.value.removeEventListener('touchend', handleTouchEnd)
}

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
  const scaleX = canvas.value.width / rect.width
  const scaleY = canvas.value.height / rect.height
  
  let clientX, clientY
  
  if (e.type.includes('touch')) {
    e.preventDefault()
    clientX = e.touches[0].clientX
    clientY = e.touches[0].clientY
  } else {
    clientX = e.clientX
    clientY = e.clientY
  }
  
  return {
    x: (clientX - rect.left) * scaleX,
    y: (clientY - rect.top) * scaleY
  }
}

const clear = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  signatureData = null
}

const save = () => {
  if (isCanvasEmpty()) {
    alert('Por favor, realice una firma antes de guardar')
    return
  }
  signatureData = canvas.value.toDataURL('image/png')
  emit('save', signatureData)
}

const isCanvasEmpty = () => {
  const blank = document.createElement('canvas')
  blank.width = canvas.value.width
  blank.height = canvas.value.height
  return canvas.value.toDataURL() === blank.toDataURL()
}

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
    stopDrawing()
  }
}

const setupCanvas = () => {
  ctx = canvas.value.getContext('2d')
  ctx.strokeStyle = props.penColor
  ctx.lineWidth = props.penWidth
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  addEventListeners()
}

const setupResizeObserver = () => {
  if (typeof ResizeObserver !== 'undefined') {
    let resizeTimeout
    
    resizeObserver = new ResizeObserver(entries => {
      clearTimeout(resizeTimeout)
      resizeTimeout = setTimeout(() => {
        if (!entries || entries.length === 0) return
        // Puedes agregar lógica de redimensionamiento aquí si es necesario
      }, 100)
    })
    
    if (canvas.value && canvas.value.parentElement) {
      resizeObserver.observe(canvas.value.parentElement)
    }
  }
}

onMounted(() => {
  setupCanvas()
  setupResizeObserver()
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  removeEventListeners()
})
</script>

<style scoped>
.signature-pad-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  background: white;
}

.signature-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  color: white;
}

.signature-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.signature-guide {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-top: 4px;
}

.signature-canvas-wrapper {
  position: relative;
  padding: 20px;
  background: #f8f9fa;
}

.signature-canvas {
  display: block;
  width: 100%;
  height: 200px;
  background: white;
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
  border: 1px dashed #e0e0e0;
  touch-action: none;
  cursor: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%231a73e8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 19a7 7 0 1 0 0-14 7 7 0 0 0 0 14z'></path></svg>") 8 8, crosshair;
}

.signature-watermark {
  position: absolute;
  bottom: 30px;
  right: 30px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.1);
  pointer-events: none;
  user-select: none;
  font-weight: bold;
  letter-spacing: 1px;
}

.signature-actions {
  display: flex;
  padding: 16px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.btn-clear, .btn-save {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  margin: 0 5px;
}

.btn-clear {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #e0e0e0;
}

.btn-clear:hover {
  background: #e9ecef;
  color: #495057;
}

.btn-save {
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  color: white;
  box-shadow: 0 2px 10px rgba(110, 142, 251, 0.3);
}

.btn-save:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(110, 142, 251, 0.4);
}

.icon {
  width: 18px;
  height: 18px;
  margin-right: 8px;
}

@media (max-width: 480px) {
  .signature-pad-container {
    border-radius: 0;
  }
  
  .signature-canvas {
    height: 180px;
  }
  
  .signature-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .btn-clear, .btn-save {
    width: 100%;
    margin: 0;
  }
}

</style>
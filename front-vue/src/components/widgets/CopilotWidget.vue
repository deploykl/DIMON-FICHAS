<!-- CopilotWidget.vue -->
<template>
  <div class="copilot-container">
    <button @click="toggle" class="copilot-button">🤖</button>
    <div v-if="visible" class="copilot-box">
      <p>Hola  👋 ¿En qué puedo ayudarte?</p>
      <!-- Aquí puedes integrar lógica de chat -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(false)
const toggle = () => (visible.value = !visible.value)
</script>

<style scoped>
.copilot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
}
.copilot-button {
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 24px;
  cursor: pointer;
}
.copilot-box {
  margin-top: 10px;
  width: 300px;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
<template>
  <main id="main" class="main">
    <div class="container">
      <h1 class="title">Ruleta de Decisiones</h1>
      
      <div class="input-section">
        <input 
          v-model="newWord" 
          @keyup.enter="addWord"
          placeholder="Ingresa una opción"
          class="input-field"
        >
        <button @click="addWord" class="add-btn">
          <span>+</span>
        </button>
      </div>
      
      <div class="words-list" v-if="words.length > 0">
        <h3 class="subtitle">Opciones registradas:</h3>
        <ul class="words-grid">
          <li v-for="(word, index) in words" :key="index" class="word-item">
            <span>{{ word }}</span>
            <button @click="removeWord(index)" class="remove-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </li>
        </ul>
      </div>
      
      <div class="wheel-section" v-if="words.length > 0">
        <div class="wheel-wrapper">
          <div 
            class="wheel" 
            :style="{ transform: `rotate(${rotation}deg)` }"
            @click="spinWheel"
            :class="{ spinning: isSpinning }"
          >
            <div 
              class="wheel-item" 
              v-for="(word, index) in words" 
              :key="index"
              :style="getWheelItemStyle(index)"
            >
              <span class="wheel-text">{{ word }}</span>
            </div>
            <div class="wheel-center">
              <div class="wheel-center-inner"></div>
            </div>
          </div>
          <div class="pointer">
            <div class="pointer-arrow"></div>
            <div class="pointer-base"></div>
          </div>
        </div>
        
        <button 
          @click="spinWheel" 
          :disabled="isSpinning || words.length < 2"
          class="spin-btn"
        >
          <span v-if="!isSpinning">Girar Ruleta</span>
          <span v-else class="spinner"></span>
        </button>
      </div>
      
      <div class="result" v-if="selectedWord">
        <div class="result-card">
          <div class="result-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="result-content">
            <h2 class="result-title">¡Seleccionado!</h2>
            <p class="result-word">{{ selectedWord }}</p>
          </div>
        </div>
      </div>
      
      <div class="empty-state" v-if="words.length === 0">
        <div class="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3 class="empty-title">Agrega opciones para comenzar</h3>
        <p class="empty-text">Presiona el botón "+" para añadir nuevas opciones</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue';

const newWord = ref('');
const words = ref([]);
const rotation = ref(0);
const isSpinning = ref(false);
const selectedWord = ref('');

const addWord = () => {
  if (newWord.value.trim() && !words.value.includes(newWord.value.trim())) {
    words.value.push(newWord.value.trim());
    newWord.value = '';
  }
};

const removeWord = (index) => {
  words.value.splice(index, 1);
  selectedWord.value = '';
};

const spinWheel = () => {
  if (words.value.length < 2 || isSpinning.value) return;
  
  isSpinning.value = true;
  selectedWord.value = '';
  
  // Número aleatorio de rotaciones completas (5-10) más un ángulo aleatorio
  const spins = 5 + Math.floor(Math.random() * 5);
  const randomAngle = Math.floor(Math.random() * 360);
  const totalRotation = spins * 360 + randomAngle;
  
  rotation.value += totalRotation;
  
  // Calcular la palabra seleccionada después de que termine la animación
  setTimeout(() => {
    const segmentAngle = 360 / words.value.length;
    const normalizedAngle = rotation.value % 360;
    // Ajustar para que el apuntador esté en la parte superior
    const effectiveAngle = (360 - normalizedAngle) % 360;
    const selectedIndex = Math.floor(effectiveAngle / segmentAngle);
    
    selectedWord.value = words.value[selectedIndex];
    isSpinning.value = false;
  }, 5000); // Tiempo que dura la animación (5s)
};

const getWheelItemStyle = (index) => {
  const segmentAngle = 360 / words.value.length;
  const hue = (index * (360 / words.value.length)) % 360;
  
  return {
    transform: `rotate(${index * segmentAngle}deg) skewY(${90 - segmentAngle}deg)`,
    backgroundColor: `hsl(${hue}, 80%, 80%)`,
    width: `${50 / Math.tan((segmentAngle * Math.PI) / 360)}%`,
    filter: `brightness(1.1)`
  };
};
</script>

<style scoped>
.main {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fafc;
  padding: 20px;
  color: #1e293b;
}

.container {
  max-width: 800px;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
  padding: 40px;
  text-align: center;
}

.title {
  color: #0f172a;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.input-section {
  display: flex;
  gap: 12px;
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.input-field {
  flex: 1;
  padding: 12px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  color: #334155;
}

.input-field:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.add-btn {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background-color: #3b82f6;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn span {
  font-size: 1.5rem;
  line-height: 1;
  font-weight: 300;
}

.add-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.words-list {
  margin: 2rem 0;
}

.words-grid {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  max-width: 600px;
  margin: 0 auto;
}

.word-item {
  background-color: white;
  padding: 10px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.word-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.word-item span {
  flex: 1;
  text-align: left;
  font-size: 0.95rem;
  color: #334155;
}

.remove-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #fef2f2;
  color: #ef4444;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.remove-btn:hover {
  background-color: #fee2e2;
}

.wheel-section {
  margin: 3rem 0;
}

.wheel-wrapper {
  position: relative;
  width: 300px;
  height: 300px;
  margin: 0 auto 2rem;
}

.wheel {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  overflow: hidden;
  transition: transform 5s cubic-bezier(0.17, 0.67, 0.21, 0.99);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  border: 8px solid white;
}

.wheel.spinning {
  cursor: not-allowed;
}

.wheel-item {
  position: absolute;
  left: 50%;
  top: 0;
  transform-origin: left bottom;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-weight: 600;
  color: #1e293b;
  padding-left: 30px;
  box-sizing: border-box;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.wheel-text {
  transform: skewY(10deg) rotate(5deg);
  display: inline-block;
  white-space: nowrap;
  font-size: 0.9rem;
}

.wheel-center {
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.wheel-center-inner {
  width: 30px;
  height: 30px;
  background: #3b82f6;
  border-radius: 50%;
}

.pointer {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pointer-arrow {
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-top: 25px solid #3b82f6;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.pointer-base {
  width: 30px;
  height: 10px;
  background: white;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.spin-btn {
  margin-top: 1rem;
  padding: 14px 32px;
  font-size: 1rem;
  font-weight: 600;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
  position: relative;
  overflow: hidden;
}

.spin-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3);
}

.spin-btn:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

.spin-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0));
  opacity: 0;
  transition: opacity 0.3s;
}

.spin-btn:hover::after {
  opacity: 1;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result {
  margin: 2rem auto;
  max-width: 400px;
}

.result-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: left;
  border: 1px solid #e2e8f0;
}

.result-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e0f2fe;
  color: #0ea5e9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-content {
  flex: 1;
}

.result-title {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
  margin-bottom: 4px;
}

.result-word {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.empty-state {
  margin: 3rem 0;
  color: #64748b;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  color: #cbd5e1;
}

.empty-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #475569;
}

.empty-text {
  font-size: 0.95rem;
  margin: 0;
  opacity: 0.8;
}

@media (max-width: 640px) {
  .container {
    padding: 24px;
  }
  
  .title {
    font-size: 1.8rem;
  }
  
  .wheel-wrapper {
    width: 280px;
    height: 280px;
  }
  
  .words-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>
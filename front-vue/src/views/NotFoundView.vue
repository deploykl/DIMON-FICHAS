<template>
  <div class="error-page">
    <!-- Elementos decorativos -->
    <div class="circle move" data-value="-2"></div>
    <div class="circle move" data-value="1.5"></div>
    <div class="circle move" data-value="-1.2"></div>
    <div class="circle move" data-value="0.8"></div>

    <!-- Estrellas de fondo con efecto de parpadeo -->
    <div class="stars">
      <div class="star" v-for="(star, index) in stars" :key="index" 
           :style="star.style"></div>
    </div>

    <!-- Nebulosa decorativa -->
    <div class="nebula"></div>

    <!-- Contenido principal -->
    <div class="container">
      <div class="content">
        <p class="subtitle">Señal perdida en el hiperespacio digital</p>
        <h1 class="title">404</h1>
        <p class="message">La página que buscas ha sido arrastrada a un agujero de gusano</p>
        <a href="/" class="home-link">
          <i class="fas fa-rocket"></i> Regresar a casa
        </a>
      </div>
      <div class="astronaut-container">
        <img :src="astronautImage" alt="Astronauta flotante" class="astronaut">
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

// Importa las imágenes
import astronautImage from '@/assets/img/astronaut.png'

// Generador de estrellas aleatorias
const stars = ref([])
const generateStars = () => {
  const count = 150
  const newStars = []
  for (let i = 0; i < count; i++) {
    newStars.push({
      style: {
        top: `${Math.random() * 100}%`,
        left: `${Math.random() * 100}%`,
        width: `${Math.random() * 3 + 1}px`,
        height: `${Math.random() * 3 + 1}px`,
        opacity: Math.random(),
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${Math.random() * 3 + 2}s`
      }
    })
  }
  stars.value = newStars
}

// Efecto de movimiento con el mouse
const handleMouseMove = (event) => {
  document.querySelectorAll('.move').forEach(element => {
    const data = parseFloat(element.getAttribute('data-value'))
    const x = (window.innerWidth - event.pageX * data) / 120
    const y = (window.innerHeight - event.pageY * data) / 120
    element.style.transform = `translateX(${x}px) translateY(${y}px)`
  })
}

onMounted(() => {
  generateStars()
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})
</script>

<style scoped>
.error-page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  background: radial-gradient(ellipse at bottom, #0d1e31 0%, #0c0d13 100%);
  position: relative;
  color: white;
}

/* Círculos decorativos mejorados */
.circle {
  position: absolute;
  border-radius: 50%;
  z-index: 1;
  filter: blur(60px);
  opacity: 0.7;
  transition: transform 0.3s ease-out;
}

.circle:nth-of-type(1) {
  top: -15%;
  left: 70%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(81, 65, 210, 0.8) 0%, rgba(12, 13, 19, 0) 70%);
}

.circle:nth-of-type(2) {
  top: 60%;
  left: 10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(210, 65, 165, 0.6) 0%, rgba(12, 13, 19, 0) 70%);
}

.circle:nth-of-type(3) {
  top: 10%;
  left: 15%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(65, 210, 182, 0.5) 0%, rgba(12, 13, 19, 0) 70%);
}

.circle:nth-of-type(4) {
  top: 70%;
  left: 75%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(210, 153, 65, 0.4) 0%, rgba(12, 13, 19, 0) 70%);
}

/* Estrellas animadas */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.star {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  animation: twinkle infinite alternate;
}

@keyframes twinkle {
  0% { opacity: 0.2; }
  100% { opacity: 1; }
}

/* Nebulosa decorativa */
.nebula {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="5" stitchTiles="stitch"/><feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.05 0"/></filter><rect width="100%" height="100%" filter="url(%23noise)"/></svg>');
  opacity: 0.15;
  z-index: 1;
}

/* Contenedor principal */
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  z-index: 2;
  position: relative;
  padding: 2rem;
  box-sizing: border-box;
}

.content {
  text-align: center;
  max-width: 800px;
  position: relative;
  z-index: 3;
}

/* Textos */
.subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 2px;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
}

.title {
  font-family: 'Barlow', sans-serif;
  font-size: 15rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1;
  text-shadow: 0 0 20px rgba(167, 119, 227, 0.2);
}

.message {
  font-size: 1.25rem;
  font-weight: 300;
  margin: 1.5rem 0 3rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 600px;
  line-height: 1.6;
}

/* Botón de regreso */
.home-link {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  color: white;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(110, 142, 251, 0.3);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.home-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #a777e3, #6e8efb);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.home-link:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(110, 142, 251, 0.4);
}

.home-link:hover::before {
  opacity: 1;
}

.home-link i {
  transition: transform 0.3s ease;
}

.home-link:hover i {
  transform: translateX(3px);
}

/* Contenedor del astronauta con borde */
.astronaut-container {
  position: absolute;
  right: 10%;
  bottom: 10%;
  z-index: 2;
  padding: 8px;
  background: linear-gradient(135deg, rgba(110, 142, 251, 0.3), rgba(167, 119, 227, 0.3));
  border-radius: 50%;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 0 20px rgba(110, 142, 251, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
  animation: float 8s ease-in-out infinite;
}

.astronaut {
  width: 100%;
  max-width: 400px;
  min-width: 120px;
  display: block;
  border-radius: 50%;
  filter: drop-shadow(0 0 10px rgba(167, 119, 227, 0.5));
  position: relative;
  z-index: 1;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(2deg); }
  50% { transform: translateY(-20px) rotate(-2deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .title {
    font-size: 12rem;
  }
  
  .astronaut-container {
    right: 5%;
    bottom: 5%;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 8rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  .message {
    font-size: 1rem;
  }
  
  .astronaut-container {
    right: 0%;
    transform: translateX(50%);
    bottom: 35%;
    max-width: 180px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 6rem;
  }
  
  .subtitle {
    font-size: 1rem;
    letter-spacing: 1px;
  }
  
  .home-link {
    padding: 0.8rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .circle:nth-of-type(1),
  .circle:nth-of-type(2),
  .circle:nth-of-type(3),
  .circle:nth-of-type(4) {
    filter: blur(40px);
  }
  
  .astronaut-container {
    max-width: 150px;
    padding: 6px;
  }
}
</style>
<template>
  <div class="page-wrapper">
    <header class="header">
      <div class="header-content">
        <img src="@/assets/img/logo1.png" alt="Logo" class="logo">
        <a href="/login" class="login-btn">
          <i class="bi bi-box-arrow-in-right"></i> Ingresar
        </a>
      </div>
    </header>

    <main class="main-content">
      <div class="presentation-container">
        <div class="image-container">
          <img src="@/assets/img/home/portada4.png" alt="Presentación" class="main-image">
        </div>
        <div class="text-content">
          <h1>Plataforma OBS Salud</h1>
          <p class="description">
            La Plataforma OBS Salud es un sistema web para gestionar el cumplimiento de
            procesos estratégicos, misionales y de soporte en una organización de salud.
          </p>
          <p class="features">
            Permite evaluar, registrar y monitorear el estado de cumplimiento mediante fichas de verificación...
          </p>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="quotes-container">
        <div id="quoteCarousel" class="quotes-slider">
          <div class="quote active">
            <div class="quote-content">
              <div class="quote-icon">“</div>
              <p class="quote-text">Si lo puedes imaginar, lo puedes programar</p>
              <div class="quote-author">
                <div class="author-line"></div>
                <span>Alan Kay</span>
              </div>
            </div>
          </div>
          <div class="quote">
            <div class="quote-content">
              <div class="quote-icon">“</div>
              <p class="quote-text">Camina hacia el futuro, abriendo nuevas puertas y probando cosas nuevas...</p>
              <div class="quote-author">
                <div class="author-line"></div>
                <span>Walt Disney</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-info">
        <div class="copyright">
          &copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS
        </div>
        <div class="technologies">
          Tecnologías:
          <span class="tech-tag"><i class="fab fa-python"></i> Python</span>
          <span class="tech-tag"><i class="fab fa-python"></i> Django</span>
          <span class="tech-tag"><i class="fas fa-layer-group"></i> REST API</span>
          <span class="tech-tag"><i class="fab fa-js"></i> Vue.js</span>
          <span class="tech-tag"><i class="fas fa-database"></i> SQL Server</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentYear = ref(new Date().getFullYear());

onMounted(() => {
  const quotes = document.querySelectorAll('.quote');
  let currentIndex = 0;

  setInterval(() => {
    quotes[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % quotes.length;
    quotes[currentIndex].classList.add('active');
  }, 4000);
});
</script>

<style>
/* Reset básico */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
}

/* Estructura principal */
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  background: linear-gradient(to right, #0b4a7a, #083758);
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  height: 50px;
  width: auto;
}

.login-btn {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border: 1px solid white;
  border-radius: 5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Contenido principal */
.main-content {
  flex: 1;
  padding: 4rem 0 0;
  display: flex;
  align-items: flex-start;
}

.presentation-container {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: center;
  gap: 2rem;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 2rem;
}

.image-container,
.text-content {
  align-self: flex-start;
  margin-top: 0;
}

.main-image {
  max-width: 100%;
  max-height: 400px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.text-content {
  flex: 1;
  min-width: 300px;
  max-width: 500px;
}

.text-content h1 {
  color: #0b4a7a;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.description {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #555;
}

.features {
  color: #666;
}

/* Footer */
.footer {
  background-color: #0f172a;
  color: white;
  padding: 1rem 0;
}

/* Contenedor de frases - Versión compacta */
.quotes-container {
  width: 90%;
  max-width: 700px;
  margin: 0 auto 1rem;
  padding: 1rem;
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.quotes-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #3b82f6, #8b5cf6);
}

.quotes-slider {
  position: relative;
  min-height: 80px;
  /* Altura reducida */
}

.quote {
  position: absolute;
  width: 100%;
  opacity: 0;
  transition: all 0.5s ease;
}

.quote.active {
  opacity: 1;
}

.quote-content {
  padding: 0 1rem;
}

.quote-icon {
  font-size: 3rem;
  /* Tamaño reducido */
  color: #3b82f6;
  opacity: 0.2;
  position: absolute;
  top: -1rem;
  /* Posición ajustada */
  left: 0;
  line-height: 1;
  font-family: Georgia, serif;
}

.quote-text {
  font-size: 1.1rem;
  /* Texto más pequeño */
  line-height: 1.5;
  color: #f8fafc;
  margin-bottom: 1rem;
  position: relative;
  font-style: italic;
  padding-left: 1rem;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.author-line {
  flex-grow: 1;
  height: 1px;
  background: linear-gradient(to right, rgba(59, 130, 246, 0.5), transparent);
}

.quote-author span {
  color: #94a3b8;
  font-size: 0.85rem;
  /* Texto más pequeño */
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

/* Información del footer */
.footer-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.copyright {
  color: #94a3b8;
  font-size: 0.9rem;
}

.technologies {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.tech-tag {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* Responsive */
@media (max-width: 768px) {
  .presentation-container {
    flex-direction: column;
    text-align: center;
  }

  .quotes-container {
    padding: 1.2rem;
    min-height: 100px;
  }

  .quote-text {
    font-size: 1rem;
  }

  .quote-icon {
    font-size: 2.5rem;
    top: -0.8rem;
  }

  .footer-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .technologies {
    justify-content: center;
  }
}
</style>
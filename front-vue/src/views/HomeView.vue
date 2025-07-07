<template>
  <div class="page-wrapper">
    <header class="header">
      <div class="header-content">
        <img src="@/assets/img/logo1.png" alt="Logo" class="logo">
      </div>
    </header>

    <main class="main-content py-4">
      <div class="container">
        <div class="row align-items-center justify-content-center"> <!-- Centrado vertical y horizontal -->
          <!-- Columna de la imagen -->
          <div class="col-md-6 mb-4 mb-md-0 d-flex justify-content-center">
            <img src="@/assets/img/home/work.png" alt="Presentación" class="img-fluid rounded mx-auto d-block image-style me-5">
          </div>

          <!-- Columna del texto - centrada vertical y horizontalmente -->
          <div class="col-md-6 text-center">
            <!-- Título principal -->
            <h1 class="mb-3 text-center text-primary fw-bold">Plataforma OBS Salud</h1>
            <!-- Descripción -->
            <p class="mb-3 lead">
              Sistema integral para la gestión del cumplimiento normativo en organizaciones de salud.
            </p>

            <!-- Alertas importantes -->
            <div class="alert alert-info d-flex align-items-center mb-4">
              <i class="bi bi-exclamation-circle-fill me-2 fs-4"></i>
              <div>
                <strong>Novedad:</strong> Lanzamiento de la Versión Demo (v1.0) con módulos esenciales
              </div>
            </div>

            <!-- Módulos destacados -->
            <div class="mb-4">
              <h5 class="mb-3 text-center"><i class="bi bi-grid-fill me-2"></i>Módulos Principales</h5>
              <div class="row justify-content-center g-3"> <!-- Centrado y mejor espaciado -->
                <!-- Módulo de Fichas -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-clipboard-check fs-3 text-success mb-2"></i>
                    <h6 class="fw-bold">Fichas de Verificación</h6>
                    <p class="small text-muted mb-0">Gestión completa de fichas técnicas</p>
                  </div>
                </div>

                <!-- Módulo de Compromisos -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-microsoft-teams fs-3 text-primary mb-2"></i>
                    <h6 class="fw-bold">Compromisos</h6>
                    <p class="small text-muted mb-0">Seguimiento de acuerdos</p>
                  </div>
                </div>

                <!-- Módulo de Alertas -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-exclamation-triangle fs-3 text-warning mb-2"></i>
                    <h6 class="fw-bold">Alertas</h6>
                    <p class="small text-muted mb-0">Notificaciones importantes</p>
                  </div>
                </div>

                <!-- Módulo de Enlaces -->
                <div class="col-8 col-sm-3 col-md-5 col-lg-3">
                  <div class="p-3 border rounded bg-light text-center h-100 module-card">
                    <i class="bi bi-link-45deg fs-3 text-info mb-2"></i>
                    <h6 class="fw-bold">Enlaces Rápidos</h6>
                    <p class="small text-muted mb-0">Acceso directo a recursos</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Botón de acceso -->
            <div class="text-center"> <!-- Centrado en todas las pantallas -->
              <a href="/login" class="btn btn-primary px-4">
                <i class="bi bi-box-arrow-in-right me-2"></i> Ingresar al sistema
              </a>
            </div>
          </div>
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
  }, 5000);
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

/* Contenido principal */
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 3rem 0;
  text-align: center;

}

.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
  text-align: center;

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
  color: #3b82f6;
  opacity: 0.2;
  position: absolute;
  top: -1rem;
  left: 0;
  line-height: 1;
  font-family: Georgia, serif;
}

.quote-text {
  font-size: 1.1rem;
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

/* Estilos para el botón */
.btn-primary {
  background-color: #0b4a7a;
  border-color: #0b4a7a;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #083758;
  border-color: #083758;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
  }

  .min-vh-75 {
    min-height: auto;
    padding: 2rem 0;
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

  .col-md-6 {
    text-align: center !important;
  }

  .d-flex.justify-content-center.justify-content-md-start {
    justify-content: center !important;
  }
}
/* Estilos para la imagen */
.image-style {
  border: none !important;
  box-shadow: none !important;
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25)); /* Efecto hover más notable */
  transition: all 0.3s ease;
  max-width: 90%; /* Asegura que la imagen no sea demasiado grande */
  margin: 0 auto; /* Centrado adicional */
    transform: translateY(-3px); /* Efecto de elevación sutil */

}

.image-style:hover {
  filter: drop-shadow(0 12px 20px rgba(0, 0, 0, 0.25)); /* Efecto hover más notable */
  transform: translateY(-3px); /* Efecto de elevación sutil */
}

/* Elimina cualquier sombra preexistente en el contenedor */
.img-fluid.rounded.shadow {
  box-shadow: none !important;
}
</style>
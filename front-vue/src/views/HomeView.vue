<template>
  <div class="page-wrapper">
    <main class="main-container">
      <header class="header-bar mb-4 shadow-sm">
        <div class="d-flex justify-content-between align-items-center container py-3">
          <img src="@/assets/img/login/logo.png" alt="Logo" class="logo">
          <a class="btn btn-outline-light px-4" href="/login">
            <i class="bi bi-box-arrow-in-right"></i> Ingresar
          </a>
        </div>
      </header>

      <section class="container presentation my-auto py-5">
        <div class="row align-items-center justify-content-center">
          <div class="col-md-8 text-center mb-4 mb-md-0 d-flex justify-content-center align-items-center">
            <img src="@/assets/img/home/portada4.png" alt="Presentación" class="img-fluid img-presentation mx-auto">
          </div>
          <div class="col-md-4">
            <h1 class="display-5 fw-bold text-primary text-center mb-4">Plataforma OBS Salud</h1>
            <p class="lead text-justify">
              La Plataforma OBS Salud es un sistema web desarrollado en Django para gestionar el cumplimiento de
              procesos estratégicos, misionales y de soporte en una organización de salud.
            </p>
            <p class="text-justify">
              Permite evaluar, registrar y monitorear el estado de cumplimiento mediante fichas de verificación, donde
              los usuarios pueden marcar:
              <br><br>
              ✅ Cumple<br>
              ❌ No Cumple<br>
              ➖ No Aplica
              <br><br>
              También almacena fechas, responsables y observaciones para facilitar la auditoría interna y el
              seguimiento.
            </p>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer py-4 bg-dark text-light">
      <div class="container">
        <div class="row">
          <div class="col-md-6 mb-2 mb-md-0">
            <p class="mb-0">
              &copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS
            </p>
          </div>
          <div class="col-md-6 text-md-end">
            <p class="mb-0">Tecnologías:
              <span class="badge bg-light text-dark me-1"><i class="fab fa-python"></i> Python</span>
              <span class="badge bg-secondary me-1"><i class="fab fa-python"></i> Django</span>
              <span class="badge bg-info me-1"><i class="fas fa-layer-group"></i> REST API</span>
              <span class="badge bg-success me-1"><i class="fab fa-js"></i> Vue.js</span>
              <span class="badge bg-warning text-dark"><i class="fas fa-database"></i> SQL Server</span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const currentYear = new Date().getFullYear();
</script>

<style scoped>
/* General */
body {
  background-color: #f4f7fa;
  font-family: 'Segoe UI', sans-serif;
  margin: 0;
  min-height: 100vh;
}

.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-container {
  background: linear-gradient(to bottom right, #ffffff, #eef3f7);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.text-justify {
  text-align: justify;
}

.logo {
  max-width: 240px;
  height: auto;
}

/* Header */
.header-bar {
  background: linear-gradient(90deg, #083758, #0b4a7a);
  color: white;
}

/* Presentación */
.presentation {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.presentation h1 {
  font-family: 'Georgia', serif;
}

.img-presentation {
  max-height: 400px;
  object-fit: contain;
  filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.2));
}

/* Footer */
.footer {
  border-top: 1px solid #444;
  font-size: 0.95rem;
  margin-top: auto;
}

.badge {
  font-size: 0.85rem;
  padding: 0.4em 0.7em;
}
</style>
<template>
  <header id="header" class="bg-light shadow-sm">
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container-fluid">
        <!-- Botón de menú móvil -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Menú de navegación -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Título del sistema centrado -->
          <a class="navbar-brand mx-auto custom-title" href="#">Plataforma Local de Desarrollo - DevCode</a>
          
          <!-- Menú de autenticación alineado a la derecha -->
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a v-if="isAuthenticated" class="nav-link btn btn-primary text-white" href="#">
                <i class="fas fa-user"></i> <span class="ms-2">Bienvenido, {{ userName }} {{ userLastName }}</span>
              </a>
              <a v-else class="nav-link btn btn-secondary text-white" href="/login">
                <i class="fas fa-user"></i> <span class="ms-2">Iniciar sesión</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const isAuthenticated = ref(false) // Cambia esto basado en la lógica de autenticación
const isAdmin = ref(false) // Cambia esto basado en los permisos del usuario
const userName = ref('') // Cambia esto basado en los datos del usuario
const userLastName = ref('') // Cambia esto basado en los datos del usuario
</script>

<style scoped>
/* Estilo adicional para el menú */
.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav-link {
  font-size: 1rem;
}

.navbar-nav .nav-link {
  margin-right: 1rem;
}

.navbar-nav .btn {
  border-radius: 20px;
}

.navbar-toggler {
  border: none;
}
.custom-title {
  font-family: 'Arial', sans-serif; /* Cambia la fuente a algo más profesional */
  font-size: 1.5rem; /* Tamaño más grande para destacar */
  font-weight: bold; /* Negrita para resaltar */
  color: #004085; /* Color azul oscuro para darle seriedad */
  text-transform: uppercase; /* Texto en mayúsculas para formalidad */
}
</style>

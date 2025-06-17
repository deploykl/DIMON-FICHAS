<template>
  <div class="container">
    <h1 class="my-4">Gestión de Fichas</h1>
    
    <div class="card">
      <div class="card-body">
        <h2 class="card-title">Selección de Fichas Técnicas</h2>
        <p class="card-text">Seleccione una opción para comenzar la evaluación:</p>
        
        <div class="d-grid gap-3">
          <router-link 
            to="/fichas/seleccion" 
            class="btn btn-primary btn-lg">
            <i class="fas fa-list-check me-2"></i> Ver todas las fichas disponibles
          </router-link>
          
          <button class="btn btn-outline-secondary btn-lg">
            <i class="fas fa-history me-2"></i> Ver evaluaciones anteriores
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Puedes agregar lógica adicional si es necesario
</script>
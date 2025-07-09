<template>
  <main id="main" class="main">
    <h2>Documentos disponibles</h2>
    <h3>ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR - ENDES – MINSA 2024</h3>
    
     <!-- Categoría de Documentos Generales -->
    <div class="category-section">
      <h3>Documentos Generales</h3>
      <div class="document-list">
        <div v-for="file in files" :key="file.name" class="document-item">
          <button @click="openDocument(file)">
            <i :class="fileIcon(file)"></i> {{ file.name }}
          </button>
        </div>
      </div>
    </div>
    <!-- Categoría de Cuadros Anexos -->
    <div class="category-section">
      <h3>Cuadros Anexos</h3>
      <div class="document-list">
        <div v-for="file in cuadrosAnexos" :key="file.name" class="document-item">
          <button @click="openOfficeDocument(file)">
            <i class="fas fa-file-excel"></i> {{ file.name }}
          </button>
        </div>
      </div>
    </div>
    
   
  </main>
</template>

<script setup>
import { ref } from 'vue';

// Lista de cuadros anexos (archivos Excel)
const cuadrosAnexos = ref([
  { name: 'I.- Articulado Nutricional 2024.xlsx', path: '/docs/I-Articulado_Nutricional_2024.xlsx', type: 'excel' },
  { name: 'II.- Desarrollo Infantil Temprano 2024.xlsx', path: '/docs/II-Desarrollo_Infantil_Temprano_2024.xlsx', type: 'excel' },
  { name: 'III.- Salud Materno Neonatal 2024.xlsx', path: '/docs/III-Salud_Materno_Neonatal_2024.xlsx', type: 'excel' },
  { name: 'IV.- Acceso a la Identidad 2024.xlsx', path: '/docs/IV-Acceso_a_la_Identidad_2024.xlsx', type: 'excel' },
  { name: 'V.- Violencia 2024.xlsx', path: '/docs/V-Violencia_2024.xlsx', type: 'excel' }
]);

// Lista de documentos generales
const files = ref([
  { name: 'Nota.txt', path: '/docs/nota.txt', type: 'text' },
  { name: 'Documento PDF', path: '/docs/r80595.pdf', type: 'pdf' },
  { name: 'I-Resultados ENDES 2024', path: '/docs/1_Sintesis de los resultados PPR ENDES 2024.pdf', type: 'pdf' },
  { name: 'II-Resultados Presupuestales 2024', path: '/docs/2_Indicadores_de_Resultados_de_los_Programas_Presupuestales_ENDES_2024.pdf', type: 'pdf' }
]);

// Función para obtener icono según tipo de archivo
const fileIcon = (file) => {
  switch(file.type) {
    case 'pdf': return 'fas fa-file-pdf';
    case 'text': return 'fas fa-file-alt';
    case 'excel': return 'fas fa-file-excel';
    default: return 'fas fa-file';
  }
};

// Función para abrir documentos Office (Excel)
function openOfficeDocument(file) {
  try {
    // Usamos el protocolo ms-excel para abrir en la aplicación nativa si está disponible
    const fullUrl = window.location.origin + file.path;
    window.location.href = `ms-excel:ofe|u|${fullUrl}`;
    
    // Fallback: abrir en nueva pestaña después de un breve retraso
    setTimeout(() => {
      window.open(fullUrl, '_blank');
    }, 500);
  } catch (error) {
    console.error('Error al abrir documento Office:', error);
    window.open(file.path, '_blank');
  }
}

// Función para abrir otros documentos (PDF, texto)
function openDocument(file) {
  // Abrir todos los documentos en nueva pestaña
  window.open(file.path, '_blank');
}
</script>

<style scoped>
.main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.category-section {
  margin-bottom: 30px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.category-section h3 {
  color: #2c3e50;
  border-bottom: 2px solid #4361ee;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.document-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}

.document-item button {
  width: 100%;
  padding: 12px 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.document-item button:hover {
  background: #f0f0f0;
  border-color: #4361ee;
}

.document-item button i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

/* Estilos específicos para iconos por tipo de archivo */
.fa-file-pdf {
  color: #d32f2f;
}

.fa-file-excel {
  color: #1d6f42;
}

.fa-file-alt {
  color: #6c757d;
}

@media (max-width: 768px) {
  .document-list {
    grid-template-columns: 1fr;
  }
  
  .document-item button {
    padding: 10px 12px;
  }
}
</style>
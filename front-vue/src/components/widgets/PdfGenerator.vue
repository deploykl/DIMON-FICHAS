<template>
  <div class="pdf-container" ref="pdfContent">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb" class="mb-4">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          Fichas
        </li>
        <li class="breadcrumb-item active" aria-current="page">
          {{ proceso?.nombre || 'Cargando...' }}
        </li>
      </ol>
    </nav>

    <!-- Contenido de la Ficha -->
    <template v-if="proceso">
      <!-- Información del Proceso -->
      <div class="card mb-4">
        <div class="card-body">
          <h1 class="card-title border-bottom pb-2 mb-4">{{ proceso.titulo }}</h1>
          <h3 class="h4 mb-4">{{ proceso.nombre }}</h3>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="p-3 bg-light rounded">
                <p class="mb-1"><strong>Nombre del Proceso:</strong></p>
                <p class="mb-0">{{ proceso.nombre_proceso }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 bg-light rounded">
                <p class="mb-1"><strong>Dueño del Proceso:</strong></p>
                <p class="mb-0">{{ proceso.dueño_proceso }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 bg-light rounded">
                <p class="mb-1"><strong>Objetivo:</strong></p>
                <p class="mb-0">{{ proceso.objetivo }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Formulario de IPRESS -->
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title h4 mb-4">Datos de la IPRESS</h2>
          <div class="row g-3">
            <div class="col-md-3">
              <p><strong>Tipo de IPRESS:</strong> {{ evaluacionData.tipo }}</p>
            </div>
            <div class="col-md-3">
              <p><strong>Nombre de la IPRESS:</strong> {{ evaluacionData.establecimiento }}</p>
            </div>
            <div class="col-md-3">
              <p><strong>Código de la IPRESS:</strong> {{ evaluacionData.codigo }}</p>
            </div>
            <div class="col-md-3">
              <p><strong>Categoría:</strong> {{ evaluacionData.categoria }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabla de Subprocesos con Verificadores -->
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title h4 mb-4">Subprocesos y Verificadores</h2>

          <div v-if="subprocesosFiltrados.length > 0">
            <table class="table">
              <thead>
                <tr>
                  <th>Subproceso</th>
                  <th>Verificadores</th>
                  <th>Evaluación</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subproceso in subprocesosFiltrados" :key="subproceso.id">
                  <td>
                    <h3 class="h6 mb-1">{{ subproceso.nombre }}</h3>
                    <div class="small text-muted">
                      <div><strong>Nivel:</strong> {{ subproceso.nivel }}</div>
                      <div><strong>Código:</strong> {{ subproceso.nombre.split(' ')[0] }}</div>
                    </div>
                  </td>
                  <td>
                    <div v-for="verificador in getVerificadoresBySubproceso(subproceso.id)" :key="verificador.id">
                      <div class="fw-bold">Verificador #{{ verificador.orden }}</div>
                      <div class="small">{{ verificador.descripcion }}</div>
                    </div>
                  </td>
                  <td>
                    <div v-for="verificador in getVerificadoresBySubproceso(subproceso.id)" :key="verificador.id">
                      {{ getEstadoEvaluacion(verificador.id) }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'; // Añade computed aquí
import html2pdf from 'html2pdf.js';

const props = defineProps({
  proceso: Object,
  subprocesos: Array,
  verificadores: Array,
  evaluaciones: Object,
  evaluacionData: Object
});

const pdfContent = ref(null);

const getVerificadoresBySubproceso = (subprocesoId) => {
  return props.verificadores?.filter(ver => ver.subproceso === subprocesoId) || [];
};

const getEstadoEvaluacion = (verificadorId) => {
  const evaluacion = props.evaluaciones[verificadorId];
  if (!evaluacion) return 'No evaluado';
  
  return evaluacion.estado === 'C' ? 'Cumple' : 
         evaluacion.estado === 'NC' ? 'No Cumple' : 'No Aplica';
};

const subprocesosFiltrados = computed(() => {
  if (!props.proceso) return [];
  return props.subprocesos?.filter(sub => sub.proceso === props.proceso.id) || [];
});

const generatePdf = () => {
  const element = pdfContent.value;
  const opt = {
    margin: 10,
    filename: `evaluacion_${props.proceso?.nombre || 'reporte'}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };

  html2pdf().from(element).set(opt).save();
};

defineExpose({ generatePdf });
</script>
<style scoped>
.pdf-container {
  padding: 20px;
  background-color: white;
  color: black;
}

.card {
  border: 1px solid #ddd;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.breadcrumb {
  background-color: transparent;
  padding: 0;
  margin-bottom: 20px;
}
</style>
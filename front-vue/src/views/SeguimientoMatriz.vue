<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Listado de Matrices de Compromiso</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/fichas">Fichas</router-link>
          </li>
          <li class="breadcrumb-item active">Matrices de Compromiso</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <!-- Filtros -->
              <div class="row mb-3">
                <div class="col-md-4">
                  <label class="form-label">Filtrar por establecimiento</label>
                  <input v-model="filtroEstablecimiento" type="text" class="form-control"
                    placeholder="Nombre del establecimiento">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Filtrar por código</label>
                  <input v-model="filtroCodigo" type="text" class="form-control" placeholder="Código">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Filtrar por categoría</label>
                  <select v-model="filtroCategoria" class="form-select">
                    <option value="">Todas</option>
                    <option v-for="categoria in categoriasUnicas" :value="categoria">{{ categoria }}</option>
                  </select>
                </div>
              </div>

              <!-- Listado agrupado por monitor -->
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando matrices de compromiso...</p>
              </div>

              <div v-else>
                <div v-if="matricesAgrupadas.length === 0" class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  No se encontraron matrices de compromiso
                </div>

                <div v-for="grupo in matricesAgrupadas" :key="grupo.monitor" class="mb-5">
                  <h5 class="card-title border-bottom pb-2 mb-3">
                    <i class="fas fa-user-circle me-2"></i>
                    Monitor: <strong>{{ grupo.monitor }}</strong>
                    <span class="badge bg-primary ms-2">{{ grupo.matrices.length }} matriz(ces)</span>
                  </h5>

                  <div class="table-responsive">
                    <table class="table table-hover">
                      <thead>
                        <tr>
                          <th>Establecimiento</th>
                          <th>Código</th>
                          <th>Categoría</th>
                          <th>Semáforo</th>
                          <th>Fecha Creación</th>
                          <th>Verificadores NC</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="matriz in grupo.matrices" :key="matriz.id">
                          <td>{{ getEstablecimiento(matriz) }}</td>
                          <td>{{ getCodigo(matriz) }}</td>
                          <td>
                            <span class="badge" :class="getBadgeClass(getCategoria(matriz))">
                              {{ getCategoria(matriz) || 'N/A' }}
                            </span>
                          </td>
                          <td>
                            <span class="badge" :class="getSemaforoClass(matriz.semaforo)">
                              {{ matriz.semaforo }}
                            </span>
                          </td>
                          <td>{{ formatDateTime(matriz.fecha_creacion) }}</td>
                          <td>
                            <div class="d-flex gap-1">
                              <span class="badge bg-danger" title="No Conformes">
                                {{ matriz.contadores_evaluaciones?.total_nc || 0 }} NC
                              </span>
                              <span class="badge bg-warning text-dark" title="No Aplica">
                                {{ matriz.contadores_evaluaciones?.total_na || 0 }} NA
                              </span>
                              <span class="badge bg-success" title="Cumple">
                                {{ matriz.contadores_evaluaciones?.total_c || 0 }} C
                              </span>
                            </div>
                          </td>
                          <td>
                            <button @click="verDetalles(matriz)" class="btn btn-sm btn-outline-primary me-2"
                              title="Ver detalles">
                              <i class="fas fa-eye"></i>
                            </button>
                            <router-link :to="`/matriz-compromiso/matriz/${matriz.id}`"
                              class="btn btn-sm btn-outline-success me-2" title="Editar">
                              <i class="fas fa-edit"></i>
                            </router-link>
                            <button @click="exportarPDF(matriz.id)" class="btn btn-sm btn-outline-secondary me-2"
                              title="Exportar PDF">
                              <i class="fas fa-file-pdf"></i>
                            </button>
                            <button @click="verSeguimientos(matriz.id)" class="btn btn-sm btn-outline-info"
                              title="Seguimientos">
                              <i class="fas fa-history"></i>
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para ver detalles -->
    <div v-if="showDetallesModal" class="modal fade show d-block" tabindex="-1"
      style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-lg">
    <div class="modal-content" ref="modalContent">
          <div class="modal-header">
            <h5 class="modal-title">Detalles de Matriz de Compromiso</h5>
            <button type="button" class="btn-close" @click="cerrarModales"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <!-- Columna izquierda (Información General y Compromisos) -->
              <div class="col-md-6">
                <h6><i class="fas fa-info-circle me-2"></i>Información General</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Establecimiento:</strong> {{ getEstablecimiento(matrizDetalles) }}</p>
                    <p><strong>Código:</strong> {{ getCodigo(matrizDetalles) }}</p>
                    <p><strong>Categoría:</strong> {{ getCategoria(matrizDetalles) }}</p>
                    <p><strong>Semáforo:</strong>
                      <span class="badge" :class="getSemaforoClass(matrizDetalles.semaforo)">
                        {{ matrizDetalles.semaforo }}
                      </span>
                    </p>
                    <p><strong>Fecha Creación:</strong> {{ formatDateTime(matrizDetalles.fecha_creacion) }}</p>
                  </div>
                </div>

                <h6><i class="fas fa-clipboard-check me-2"></i>Compromisos</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Descripción situacional:</strong></p>
                    <p class="text-muted">{{ matrizDetalles.descripcion_situacional }}</p>

                    <p><strong>Riesgo identificado:</strong></p>
                    <p class="text-muted">{{ matrizDetalles.riesgo_identificado }}</p>

                    <p><strong>Medidas correctivas:</strong></p>
                    <p class="text-muted">{{ matrizDetalles.medidas_correctivas }}</p>

                    <p><strong>Hito esperado:</strong></p>
                    <p class="text-muted">{{ matrizDetalles.hito_esperado }}</p>
                  </div>
                </div>
              </div>

              <!-- Columna derecha (Plazos y Responsables) -->
              <div class="col-md-6">
                <h6><i class="fas fa-calendar-alt me-2"></i>Plazos</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <p><strong>Inicio:</strong> {{ formatDateTime(matrizDetalles.plazo_inicio) }}</p>
                    <p><strong>Fin:</strong> {{ formatDateTime(matrizDetalles.plazo_fin) }}</p>
                    <p><strong>Duración:</strong> {{ calcularDias(matrizDetalles.plazo_inicio,
                      matrizDetalles.plazo_fin) }} días</p>
                  </div>
                </div>

                <h6><i class="fas fa-users me-2"></i>Responsables</h6>
                <div class="card border-0 shadow-sm mb-3">
                  <div class="card-body">
                    <!-- Responsable M -->
                    <p><strong>Monitor (M):</strong> {{ matrizDetalles.monitor_nombre }}</p>
                    <div v-if="matrizDetalles.firma_m" class="text-center mb-3">
                      <img :src="matrizDetalles.firma_m" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Monitor</p>
                    </div>

                    <!-- Responsable A -->
                    <p><strong>Responsable directo (A):</strong> {{ matrizDetalles.responsable_directo }}</p>
                    <div v-if="matrizDetalles.firma_a" class="text-center mb-3">
                      <img :src="matrizDetalles.firma_a" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Responsable Directo</p>
                    </div>
                    <!-- Funcionario B -->
                    <p><strong>Funcionario (B):</strong> {{ matrizDetalles.funcionario_depen_directo }}</p>
                    <div v-if="matrizDetalles.firma_b" class="text-center mb-3">
                      <img :src="matrizDetalles.firma_b" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Funcionario B</p>
                    </div>

                    <!-- Funcionario C -->
                    <p><strong>Funcionario (C):</strong> {{ matrizDetalles.funcionario_depen_indirecto }}</p>
                    <div v-if="matrizDetalles.firma_c" class="text-center mb-3">
                      <img :src="matrizDetalles.firma_c" class="img-fluid border rounded" style="max-height: 80px;">
                      <p class="small text-muted mt-1">Firma Funcionario C</p>
                    </div>

                    <!-- Funcionario D (condicional) -->
                    <div v-if="matrizDetalles.funcionario_d">
                      <p><strong>Funcionario (D):</strong> {{ matrizDetalles.funcionario_d }}</p>
                      <div v-if="matrizDetalles.firma_d" class="text-center mb-3">
                        <img :src="matrizDetalles.firma_d" class="img-fluid border rounded" style="max-height: 80px;">
                        <p class="small text-muted mt-1">Firma Funcionario D</p>
                      </div>
                    </div>

                    <!-- Funcionario E (condicional) -->
                    <div v-if="matrizDetalles.funcionario_e">
                      <p><strong>Funcionario (E):</strong> {{ matrizDetalles.funcionario_e }}</p>
                      <div v-if="matrizDetalles.firma_e" class="text-center mb-3">
                        <img :src="matrizDetalles.firma_e" class="img-fluid border rounded" style="max-height: 80px;">
                        <p class="small text-muted mt-1">Firma Funcionario E</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sección de Verificadores -->
            <h6>
              <i class="fas fa-chart-pie me-2"></i>
              Resumen de Verificadores (Total: {{ getTotalNC(matrizDetalles) + getTotalNA(matrizDetalles) +
                getTotalC(matrizDetalles) }})
            </h6>
            <div class="card border-0 shadow-sm mb-3">
              <div class="card-body">
                <div class="d-flex gap-3 mb-3">
                  <span class="badge bg-danger">
                    {{ getTotalNC(matrizDetalles) }} No Conformes
                  </span>
                  <span class="badge bg-warning text-dark">
                    {{ getTotalNA(matrizDetalles) }} No Aplica
                  </span>
                  <span class="badge bg-success">
                    {{ getTotalC(matrizDetalles) }} Cumple
                  </span>
                </div>

                <!-- Acordeón para Verificadores No Conformes -->
                <div v-if="getTotalNC(matrizDetalles) > 0">
                  <h6 class="mt-3"><i class="fas fa-exclamation-triangle text-danger me-2"></i>Verificadores No
                    Conformes</h6>
                  <div class="accordion">
                    <div v-for="(nc, index) in getEvaluacionesNC(matrizDetalles)" :key="'nc-' + index"
                      class="accordion-item mb-2">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                          :data-bs-target="'#collapseNC-' + index">
                          Verificador #{{ index + 1 }}: {{ getVerificadorNombre(nc) }}
                        </button>
                      </h2>
                      <div :id="'collapseNC-' + index" class="accordion-collapse collapse">
                        <div class="accordion-body">
                          <p><strong>Subproceso:</strong> {{ getSubprocesoNombre(nc) }} ({{ getSubprocesoCodigo(nc) }})
                          </p>
                          <p><strong>Estado:</strong>
                            <span class="badge bg-danger">No Conforme</span>
                          </p>
                          <p><strong>Observaciones:</strong> {{ nc.observaciones || 'Sin observaciones' }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="alert alert-info">
                  No hay verificadores no conformes asociados a esta matriz
                </div>

                <!-- Acordeón para Verificadores No Aplica -->
                <div v-if="getTotalNA(matrizDetalles) > 0" class="mt-4">
                  <h6><i class="fas fa-question-circle text-warning me-2"></i>Verificadores No Aplica</h6>
                  <div class="accordion">
                    <div v-for="(na, index) in getEvaluacionesNA(matrizDetalles)" :key="'na-' + index"
                      class="accordion-item mb-2">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                          :data-bs-target="'#collapseNA-' + index">
                          Verificador #{{ index + 1 }}: {{ getVerificadorNombre(na) }}
                        </button>
                      </h2>
                      <div :id="'collapseNA-' + index" class="accordion-collapse collapse">
                        <div class="accordion-body">
                          <p><strong>Subproceso:</strong> {{ getSubprocesoNombre(na) }} ({{ getSubprocesoCodigo(na) }})
                          </p>
                          <p><strong>Estado:</strong>
                            <span class="badge bg-warning text-dark">No Aplica</span>
                          </p>
                          <p><strong>Observaciones:</strong> {{ na.observaciones || 'Sin observaciones' }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="getTotalNC(matrizDetalles) === 0" class="alert alert-info mt-4">
                  No hay verificadores no aplica asociados a esta matriz
                </div>

                <!-- Acordeón para Verificadores Cumple -->
                <div v-if="getTotalC(matrizDetalles) > 0" class="mt-4">
                  <h6><i class="fas fa-check-circle text-success me-2"></i>Verificadores Cumple</h6>
                  <div class="accordion">
                    <div v-for="(c, index) in getEvaluacionesC(matrizDetalles)" :key="'c-' + index"
                      class="accordion-item mb-2">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                          :data-bs-target="'#collapseC-' + index">
                          Verificador #{{ index + 1 }}: {{ getVerificadorNombre(c) }}
                        </button>
                      </h2>
                      <div :id="'collapseC-' + index" class="accordion-collapse collapse">
                        <div class="accordion-body">
                          <p><strong>Subproceso:</strong> {{ getSubprocesoNombre(c) }} ({{ getSubprocesoCodigo(c) }})
                          </p>
                          <p><strong>Estado:</strong>
                            <span class="badge bg-success">Cumple</span>
                          </p>
                          <p><strong>Observaciones:</strong> {{ c.observaciones || 'Sin observaciones' }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="getTotalNC(matrizDetalles) === 0 && getTotalNA(matrizDetalles) === 0" class="alert alert-info mt-4">
                  No hay verificadores cumple asociados a esta matriz
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModales">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="exportarPDFDesdeModal">
              <i class="fas fa-file-pdf me-2"></i> Exportar PDF
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Seguimientos -->
    <div v-if="showSeguimientosModal" class="modal fade show d-block"
      style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="fas fa-history me-2"></i>
              Seguimientos - {{ matrizSeguimientos.matrizData ? getEstablecimiento(matrizSeguimientos.matrizData) :
              'N/A' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="cerrarModales"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingSeguimientos" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-2">Cargando información de seguimientos...</p>
            </div>

            <div v-else>
              <!-- Sección de Información de la Matriz -->
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h6 class="mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    Información de la Matriz de Compromiso
                  </h6>
                </div>
                <div class="card-body">
                  <div class="row">
                    <!-- Columna Izquierda - Información General -->
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="fw-bold">Monitor que generó la matriz:</label>
                        <p>{{ matrizSeguimientos.matrizData?.monitor_nombre || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Fecha de creación:</label>
                        <p>{{ formatDateTime(matrizSeguimientos.matrizData?.fecha_creacion) }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Descripción situacional:</label>
                        <p class="text-muted">{{ matrizSeguimientos.matrizData?.descripcion_situacional || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Riesgo identificado:</label>
                        <p class="text-muted">{{ matrizSeguimientos.matrizData?.riesgo_identificado || 'N/A' }}</p>
                      </div>
                    </div>

                    <!-- Columna Derecha - Compromisos y Plazos -->
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="fw-bold">Medidas correctivas:</label>
                        <p class="text-muted">{{ matrizSeguimientos.matrizData?.medidas_correctivas || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Hito esperado:</label>
                        <p class="text-muted">{{ matrizSeguimientos.matrizData?.hito_esperado || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Responsable directo (A):</label>
                        <p>{{ matrizSeguimientos.matrizData?.responsable_directo || 'N/A' }}</p>
                      </div>

                      <div class="mb-3">
                        <label class="fw-bold">Plazos:</label>
                        <div class="ps-3">
                          <p><strong>Inicio:</strong> {{ formatDateTime(matrizSeguimientos.matrizData?.plazo_inicio) }}</p>
                          <p><strong>Fin:</strong> {{ formatDateTime(matrizSeguimientos.matrizData?.plazo_fin) }}</p>
                          <p><strong>Duración:</strong>
                            {{ calcularDias(matrizSeguimientos.matrizData?.plazo_inicio,
                              matrizSeguimientos.matrizData?.plazo_fin) }} días
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sección de Historial de Seguimientos -->
              <div class="card">
                <div class="card-header bg-light d-flex justify-content-between align-items-center">
                  <h6 class="mb-0">
                    <i class="fas fa-list-ol me-2"></i>
                    Historial de Seguimientos (Total: {{ matrizSeguimientos.seguimientos?.length || 0 }})
                  </h6>
                  <button @click="nuevoSeguimiento(matrizSeguimientos.id)" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus me-1"></i> Nuevo Seguimiento
                  </button>
                </div>

                <div class="card-body">
                  <div v-if="matrizSeguimientos.seguimientos?.length > 0">
                    <div class="table-responsive">
                      <table class="table table-hover table-bordered">
                        <thead class="table-light">
                          <tr>
                            <th width="80">#</th>
                            <th>Fecha Seguimiento</th>
                            <th>Estado</th>
                            <th>Registrado por</th>
                            <th>Fecha Registro</th>
                            <th width="120">Acciones</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(seguimiento, index) in matrizSeguimientos.seguimientos" :key="'seg-' + index"
                            :class="getEstadoSeguimientoBgClass(seguimiento.estado)">
                            <td class="fw-bold">{{ index + 1 }}</td>
                            <td>{{ formatDateTime(seguimiento.fecha_seguimiento) }}</td>
                            <td>
                              <span class="badge" :class="getEstadoSeguimientoClass(seguimiento.estado)">
                                {{ getEstadoSeguimientoDisplay(seguimiento.estado) }}
                              </span>
                            </td>
                            <td>{{ seguimiento.usuario_nombre || 'N/A' }}</td>
                            <td>{{ formatDateTime(seguimiento.fecha_creacion) }}</td>
                            <td>
                              <button @click="editarSeguimiento(seguimiento.id)"
                                class="btn btn-sm btn-outline-primary me-1" title="Editar">
                                <i class="fas fa-edit"></i>
                              </button>
                              <button class="btn btn-sm btn-outline-info" title="Ver detalles" data-bs-toggle="collapse"
                                :data-bs-target="'#detailsSeg-' + index">
                                <i class="fas fa-eye"></i>
                              </button>
                            </td>
                          </tr>
                          <!-- Fila de detalles expandible -->
                          <tr v-for="(seguimiento, index) in matrizSeguimientos.seguimientos" :key="'detail-' + index"
                            class="collapse" :id="'detailsSeg-' + index">
                            <td colspan="6" class="bg-light">
                              <div class="p-3">
                                <div class="row">
                                  <div class="col-md-6 mb-3">
                                    <label class="fw-bold">Análisis/Acción:</label>
                                    <p class="text-muted">{{ seguimiento.analisis_accion || 'Sin descripción' }}</p>
                                  </div>

                                  <div class="col-md-6 mb-3" v-if="seguimiento.observaciones">
                                    <label class="fw-bold">Observaciones:</label>
                                    <p class="text-muted">{{ seguimiento.observaciones }}</p>
                                  </div>

                                  <div class="col-12" v-if="seguimiento.evidencia_url">
                                    <label class="fw-bold">Evidencia:</label>
                                    <div>
                                      <a :href="seguimiento.evidencia_url" target="_blank"
                                        class="btn btn-sm btn-outline-success">
                                        <i class="fas fa-file-download me-1"></i> Descargar evidencia
                                      </a>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div v-else class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay seguimientos registrados para esta matriz
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModales">
              <i class="fas fa-times me-1"></i> Cerrar
            </button>
            <button type="button" class="btn btn-primary" @click="exportarPDF(matrizSeguimientos.id)">
              <i class="fas fa-file-pdf me-1"></i> Exportar PDF
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Editar/Crear Seguimiento -->
    <div v-if="showEditarSeguimientoModal" class="modal fade show d-block"
      style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ seguimientoEditando?.isNew ? 'Nuevo Seguimiento' : 'Editar Seguimiento' }}</h5>
            <button type="button" class="btn-close" @click="cerrarModales"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarSeguimiento">
              <div class="mb-3">
                <label class="form-label">Fecha de Seguimiento</label>
                <input v-model="formSeguimiento.fecha_seguimiento" type="date" class="form-control" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Estado</label>
                <select v-model="formSeguimiento.estado" class="form-select" required>
                  <option value="P">Pendiente</option>
                  <option value="EP">En Progreso</option>
                  <option value="C">Completado</option>
                  <option value="A">Aprobado</option>
                  <option value="R">Rechazado</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Análisis/Acción</label>
                <textarea v-model="formSeguimiento.analisis_accion" class="form-control" rows="5" required></textarea>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-secondary" @click="cerrarModales">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script setup>
import { ref, computed, onMounted, reactive , nextTick } from 'vue'
import { api } from '@/components/services/auth_axios'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'
import html2pdf from 'html2pdf.js';
const $toast = useToast()

// Estados
const loading = ref(true)
const matrices = ref([])
const filtroEstablecimiento = ref('')
const filtroCodigo = ref('')
const filtroCategoria = ref('')

// Estados para los modales
const showDetallesModal = ref(false)
const showSeguimientosModal = ref(false)
const showEditarSeguimientoModal = ref(false)
const loadingSeguimientos = ref(false) // <-- Añade esta línea

// Matrices separadas
const matrizDetalles = ref(null)
const matrizSeguimientos = ref(null)

// Seguimiento
const seguimientoEditando = ref(null)
const formSeguimiento = reactive({
  fecha_seguimiento: new Date().toISOString().split('T')[0],
  estado: 'P',
  analisis_accion: ''
})


const getCodigo = (matriz) => {
  if (matriz?.codigo) return matriz.codigo;
  if (matriz?.evaluacion_data?.codigo) return matriz.evaluacion_data.codigo;
  if (matriz?.evaluacion?.codigo) return matriz.evaluacion.codigo;
  if (typeof matriz?.evaluacion === 'object' && matriz.evaluacion?.codigo) {
    return matriz.evaluacion.codigo;
  }
  return 'N/A';
}
const getEstadoSeguimientoBgClass = (estado) => {
  const clases = {
    'P': 'bg-light', // Pendiente
    'EP': 'bg-light', // En Progreso
    'C': 'bg-light', // Completado
    'A': 'bg-light', // Aprobado
    'R': 'bg-light' // Rechazado
  }
  return clases[estado] || 'bg-light'
}

const getCategoria = (matriz) => {
  return matriz?.evaluacion_data?.categoria ||
    matriz?.evaluacion?.categoria ||
    'N/A'
}

// Métodos para manejar estados de seguimiento
const getEstadoSeguimientoDisplay = (estado) => {
  const estados = {
    'P': 'Pendiente',
    'EP': 'En Progreso',
    'C': 'Completado',
    'A': 'Aprobado',
    'R': 'Rechazado'
  }
  return estados[estado] || estado
}

const getEstadoSeguimientoClass = (estado) => {
  const clases = {
    'P': 'bg-secondary',
    'EP': 'bg-warning text-dark',
    'C': 'bg-info',
    'A': 'bg-success',
    'R': 'bg-danger'
  }
  return clases[estado] || 'bg-secondary'
}

// Métodos para ver detalles
const verDetalles = (matriz) => {
  matrizDetalles.value = matriz
  showDetallesModal.value = true
}

// Métodos para seguimientos
const verSeguimientos = async (matrizId) => {
  try {
    loadingSeguimientos.value = true;
    
    // Inicializar correctamente el objeto antes de la llamada API
    matrizSeguimientos.value = {
      id: matrizId,
      seguimientos: [],
      matrizData: null
    };

    const response = await api.get(`ficha/seguimiento-matriz/`, {
      params: {
        matriz_id: matrizId,
        expand: 'matriz.evaluacion,usuario'
      }
    });

    // Verificar si hay datos antes de asignarlos
    if (response.data && response.data.length > 0) {
      matrizSeguimientos.value = {
        id: matrizId,
        seguimientos: [...response.data],
        matrizData: { ...response.data[0].matriz }
      };
    } else {
      // Si no hay seguimientos, cargar solo los datos de la matriz
      const matrizResponse = await api.get(`ficha/matriz-compromiso/${matrizId}/`, {
        params: { expand: 'evaluacion' }
      });
      
      matrizSeguimientos.value = {
        id: matrizId,
        seguimientos: [],
        matrizData: { ...matrizResponse.data }
      };
    }

    showSeguimientosModal.value = true;
  } catch (error) {
    console.error('Error al cargar seguimientos:', error);
    $toast.error('Error al cargar los datos de los seguimientos');
  } finally {
    loadingSeguimientos.value = false;
  }
};

const getEstablecimiento = (matriz) => {
  if (!matriz) return 'N/A'
  return matriz?.evaluacion_data?.establecimiento ||
    matriz?.evaluacion?.establecimiento ||
    'N/A'
}


const nuevoSeguimiento = (matrizId) => {
  formSeguimiento.fecha_seguimiento = new Date().toISOString().split('T')[0]
  formSeguimiento.estado = 'P'
  formSeguimiento.analisis_accion = ''

  seguimientoEditando.value = {
    matrizId,
    isNew: true
  }
  showEditarSeguimientoModal.value = true
  showSeguimientosModal.value = false
}

const editarSeguimiento = async (seguimientoId) => {
  try {
    loading.value = true
    const response = await api.get(`ficha/seguimiento-matriz/${seguimientoId}/`)
    formSeguimiento.fecha_seguimiento = response.data.fecha_seguimiento
    formSeguimiento.estado = response.data.estado
    formSeguimiento.analisis_accion = response.data.analisis_accion

    seguimientoEditando.value = {
      seguimientoId,
      isNew: false
    }
    showEditarSeguimientoModal.value = true
  } catch (error) {
    console.error('Error al cargar seguimiento:', error)
    $toast.error('Error al cargar el seguimiento')
  } finally {
    loading.value = false
  }
}

const cerrarModales = () => {
  showDetallesModal.value = false
  showSeguimientosModal.value = false
  showEditarSeguimientoModal.value = false
  matrizDetalles.value = null
  matrizSeguimientos.value = null
  seguimientoEditando.value = null
}

const cargarSeguimientos = async (matrizId) => {
  try {
    const response = await api.get(`ficha/seguimiento-matriz/`, {
      params: {
        matriz_id: matrizId,
        expand: 'matriz.evaluacion'
      }
    });

    // Actualizar reactivamente
    if (matrizSeguimientos.value?.id === matrizId) {
      matrizSeguimientos.value = {
        ...matrizSeguimientos.value,
        seguimientos: [...response.data],
        matrizData: response.data.length > 0 ? { ...response.data[0].matriz } : null
      };
    }
  } catch (error) {
    console.error('Error al cargar seguimientos:', error);
  }
};

const guardarSeguimiento = async () => {
  try {
    // Preparar datos comunes
    const datosBase = {
      fecha_seguimiento: formSeguimiento.fecha_seguimiento,
      estado: formSeguimiento.estado,
      analisis_accion: formSeguimiento.analisis_accion,
      matriz_id: seguimientoEditando.value.matrizId // Asegúrate de incluir esto

    };

    let response;

    if (seguimientoEditando.value.isNew) {
      // Para creación: incluir matriz_id
      const datosCompletos = {
        ...datosBase,
        matriz_id: seguimientoEditando.value.matrizId
      };

      response = await api.post('ficha/seguimiento-matriz/', datosCompletos);
      $toast.success('Seguimiento creado correctamente');

      // Actualización optimista para nuevo seguimiento
      if (matrizSeguimientos.value) {
        const nuevoSeguimiento = {
          ...response.data,
          id: response.data.id,
          matriz: {
            id: seguimientoEditando.value.matrizId,
            evaluacion: matrizSeguimientos.value.matrizData?.evaluacion
          }
        };

        matrizSeguimientos.value.seguimientos = [
          nuevoSeguimiento,
          ...matrizSeguimientos.value.seguimientos
        ];
      }
    } else {
      // Para actualización: solo enviar campos modificables
      response = await api.put(
        `ficha/seguimiento-matriz/${seguimientoEditando.value.seguimientoId}/`,
        datosBase
      );
      $toast.success('Seguimiento actualizado correctamente');

      // Actualizar el seguimiento en la lista
      if (matrizSeguimientos.value) {
        const index = matrizSeguimientos.value.seguimientos.findIndex(
          s => s.id === seguimientoEditando.value.seguimientoId
        );

        if (index !== -1) {
          const updatedSeguimientos = [...matrizSeguimientos.value.seguimientos];
          updatedSeguimientos[index] = {
            ...updatedSeguimientos[index],
            ...datosBase,
            fecha_actualizacion: new Date().toISOString()
          };
          matrizSeguimientos.value.seguimientos = updatedSeguimientos;
        }
      }
    }

    // Cerrar el modal de edición
    showEditarSeguimientoModal.value = false;

    // Recargar datos si es necesario
    if (seguimientoEditando.value.isNew) {
      await cargarSeguimientos(seguimientoEditando.value.matrizId);
    }

  } catch (error) {
    console.error('Error al guardar seguimiento:', error);

    // Mostrar mensaje de error detallado
    let errorMessage = 'Error al guardar el seguimiento';

    if (error.response) {
      // Manejar errores de validación del backend
      if (error.response.data) {
        if (typeof error.response.data === 'object') {
          errorMessage += ': ' + Object.values(error.response.data).join(', ');
        } else {
          errorMessage += ': ' + error.response.data;
        }
      }
    } else {
      errorMessage += ': ' + error.message;
    }

    $toast.error(errorMessage);

    // Revertir cambios si hubo actualización optimista
    if (matrizSeguimientos.value && seguimientoEditando.value.isNew) {
      matrizSeguimientos.value.seguimientos =
        matrizSeguimientos.value.seguimientos.filter(
          s => s.id !== seguimientoEditando.value.seguimientoId
        );
    }
  }
};

const getMonitorNombre = (matriz) => {
  return matriz?.evaluacion_data?.monitor_nombre ||
    (matriz?.evaluacion?.usuario ?
      `${matriz.evaluacion.usuario.first_name} ${matriz.evaluacion.usuario.last_name}` :
      'Sin monitor asignado')
}

const getTotalNC = (matriz) => {
  return matriz?.contadores_evaluaciones?.total_nc || 0
}

const getTotalNA = (matriz) => {
  return matriz?.contadores_evaluaciones?.total_na || 0
}

const getTotalC = (matriz) => {
  return matriz?.contadores_evaluaciones?.total_c || 0
}

const getEvaluacionesNC = (matriz) => {
  return matriz?.todas_evaluaciones?.filter(e => e.estado === 'NC') || []
}

const getVerificadorNombre = (evaluacion) => {
  return evaluacion?.verificador_nombre ||
    evaluacion?.verificador?.descripcion ||
    'Verificador desconocido'
}

const getEvaluacionesNA = (matriz) => {
  return matriz?.todas_evaluaciones?.filter(e => e.estado === 'NA') || []
}

const getEvaluacionesC = (matriz) => {
  return matriz?.todas_evaluaciones?.filter(e => e.estado === 'C') || []
}

const getSubprocesoNombre = (evaluacion) => {
  return evaluacion?.subproceso_nombre ||
    evaluacion?.verificador?.subproceso?.nombre ||
    'Subproceso desconocido'
}

const getSubprocesoCodigo = (evaluacion) => {
  return evaluacion?.subproceso_codigo ||
    (evaluacion?.verificador?.subproceso ?
      `PS${evaluacion.verificador.subproceso.proceso.id}.${evaluacion.verificador.subproceso.id}` :
      'Código desconocido')
}
const exportarPDFDesdeModal = async () => {
  try {
    $toast.info('Preparando PDF...', { timeout: false });
    await nextTick();

    const element = document.querySelector('.modal.show.d-block .modal-content');
    if (!element) throw new Error('Modal no encontrado');

    const clonedElement = element.cloneNode(true);
    
    // 1. Preparar imágenes
    const images = clonedElement.querySelectorAll('img');
    await Promise.all(Array.from(images).map(img => {
      if (!img.complete) {
        return new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
        });
      }
      return Promise.resolve();
    }));

    // 2. Ajustar estilos
    clonedElement.style.width = '210mm';
    clonedElement.style.padding = '15mm';
    clonedElement.style.backgroundColor = '#ffffff';
    
    // Eliminar footer
    const footer = clonedElement.querySelector('.modal-footer');
    if (footer) footer.remove();

    // Ajustar textos grises
    clonedElement.querySelectorAll('.text-muted').forEach(el => {
      el.style.color = '#000000';
    });

    // 3. Configuración PDF
    const opt = {
      margin: 10,
      filename: `matriz_${matrizDetalles.value?.id || 'detalle'}_${new Date().toISOString().split('T')[0]}.pdf`,
      image: { type: 'jpeg', quality: 1 },
      html2canvas: {
        scale: 3,
        useCORS: true,
        allowTaint: true,
        logging: true,
        letterRendering: true,
        timeout: 30000
      },
      jsPDF: {
        unit: 'mm',
        format: 'a4',
        orientation: 'portrait'
      },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    $toast.info('Generando PDF...', { timeout: false });
    await html2pdf().set(opt).from(clonedElement).save();
    $toast.success('PDF generado correctamente');

  } catch (error) {
    console.error('Error PDF:', error);
    $toast.error(`Error: ${error.message}`);
  } finally {
    $toast.clear();
  }
};
// Obtener matrices al montar el componente
onMounted(async () => {
  try {
    loading.value = true

    const response = await api.get('ficha/matriz-compromiso/', {
      params: {
        expand: 'evaluacion,evaluacion.usuario,evaluaciones_nc.verificador.subproceso.proceso'
      }
    })

    if (response.data) {
      if (Array.isArray(response.data)) {
        matrices.value = response.data
      } else if (response.data.results) {
        matrices.value = response.data.results
      } else {
        matrices.value = [response.data]
      }
    } else {
      console.error("La respuesta no contiene datos:", response)
      $toast.error("No se recibieron datos del servidor")
    }
  } catch (error) {
    console.error("Error al cargar matrices:", {
      message: error.message,
      response: error.response,
      stack: error.stack
    })

    let errorMessage = 'Error al cargar matrices'
    if (error.response) {
      if (error.response.status === 401) {
        errorMessage = 'No autorizado - Por favor inicie sesión'
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail
      }
    }

    $toast.error(errorMessage)
  } finally {
    loading.value = false
  }
})

// Agrupar matrices por monitor
const matricesAgrupadas = computed(() => {
  const agrupadas = {}

  matricesFiltradas.value.forEach(matriz => {
    const monitor = getMonitorNombre(matriz)

    if (!agrupadas[monitor]) {
      agrupadas[monitor] = {
        monitor,
        matrices: []
      }
    }

    agrupadas[monitor].matrices.push(matriz)
  })

  return Object.values(agrupadas)
})

// Filtrar matrices
const matricesFiltradas = computed(() => {
  return matrices.value.filter(matriz => {
    const establecimiento = getEstablecimiento(matriz).toLowerCase()
    const codigo = getCodigo(matriz).toLowerCase()
    const categoria = getCategoria(matriz)

    return (
      establecimiento.includes(filtroEstablecimiento.value.toLowerCase()) &&
      codigo.includes(filtroCodigo.value.toLowerCase()) &&
      (filtroCategoria.value === '' || categoria === filtroCategoria.value)
    )
  })
})

// Obtener categorías únicas para el filtro
const categoriasUnicas = computed(() => {
  const categorias = new Set()
  matrices.value.forEach(matriz => {
    const categoria = getCategoria(matriz)
    if (categoria) {
      categorias.add(categoria)
    }
  })
  return Array.from(categorias).sort()
})

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  
  // Obtener día, mes, año
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0') // Los meses van de 0-11
  const year = date.getFullYear()
  
  // Obtener horas, minutos, segundos
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  
  return `${day}/${month}/${year}, ${hours}:${minutes}:${seconds}`
}

const calcularDias = (inicio, fin) => {
  if (!inicio || !fin) return 0
  const start = new Date(inicio)
  const end = new Date(fin)
  const diff = end.getTime() - start.getTime()
  return Math.ceil(diff / (1000 * 3600 * 24)) + 1
}

const getBadgeClass = (categoria) => {
  if (!categoria) return 'bg-secondary'
  const categoriasColores = {
    'I-1': 'bg-primary',
    'I-2': 'bg-info',
    'I-3': 'bg-success',
    'I-4': 'bg-warning',
    'II-1': 'bg-danger',
    'II-2': 'bg-dark'
  }
  return categoriasColores[categoria] || 'bg-secondary'
}

const getSemaforoClass = (semaforo) => {
  const semaforos = {
    'Rojo': 'bg-danger',
    'Amarillo': 'bg-warning',
    'Verde': 'bg-success'
  }
  return semaforos[semaforo] || 'bg-secondary'
}

const exportarPDF = async (matrizId) => {
  try {
    const response = await api.get(
      `ficha/matriz-compromiso/${matrizId}/export_pdf/`,
      { responseType: 'blob' }
    )

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `matriz_compromiso_${matrizId}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()

    $toast.success('PDF generado correctamente')
  } catch (error) {
    console.error('Error al exportar PDF:', error)
    $toast.error('Error al generar el PDF')
  }
}
</script>

<style scoped>
.main {
  background-color: #f8f9fa;
}

.pagetitle {
  padding: 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.card {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.card-title {
  color: #012970;
  font-weight: 600;
}

.breadcrumb {
  background-color: transparent;
  padding: 0.5rem 0;
}

.breadcrumb-item.active {
  color: #899bbd;
}

.table th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.1);
  color: #012970;
}

.badge {
  font-weight: 500;
  padding: 5px 8px;
}

.modal-content {
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* Estilos para el modal de seguimientos */
.modal-xl {
  max-width: 1200px;
}

.accordion-button {
  transition: all 0.3s ease;
}

.accordion-button:not(.collapsed) {
  transform: none;
  box-shadow: none;
}

.accordion-item {
  border-radius: 5px;
  overflow: hidden;
}

/* Mejora visual para los estados */
.bg-estado-pendiente {
  background-color: rgba(108, 117, 125, 0.1);
}

.bg-estado-progreso {
  background-color: rgba(255, 193, 7, 0.1);
}

.bg-estado-completado {
  background-color: rgba(13, 202, 240, 0.1);
}

.bg-estado-aprobado {
  background-color: rgba(25, 135, 84, 0.1);
}

.bg-estado-rechazado {
  background-color: rgba(220, 53, 69, 0.1);
}

/* Mejora visual para las cards */
.card {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: none;
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.modal-dialog {
  max-width: 40%;
  margin: 1.75rem auto;
}

@media (max-width: 768px) {
  .modal-dialog {
    margin: 0.5rem auto;
    max-width: 95%;
  }
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.1);
  color: #012970;
}

.img-fluid {
  max-height: 80px;
}

/* Estilos para los modales */
.modal-backdrop {
  z-index: 1050;
}

.modal {
  z-index: 1060;
}

/* Estilos para los estados de seguimiento */
.bg-secondary {
  background-color: #6c757d !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.bg-info {
  background-color: #0dcaf0 !important;
}

.bg-success {
  background-color: #198754 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-body {
    padding: 15px;
  }

  .table-responsive {
    overflow-x: auto;
  }

  .modal-dialog {
    max-width: 95%;
    margin: 0.5rem auto;
  }
}
</style>
<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <h1>Matriz de Compromiso</h1>
      <nav>
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/">Inicio</router-link>
          </li>
          <li class="breadcrumb-item">
            <router-link to="/fichas">Fichas</router-link>
          </li>
          <li class="breadcrumb-item active">Matriz de Compromiso</li>
        </ol>
      </nav>
    </div>

    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando matriz de compromiso...</p>
              </div>

              <div v-else>
                <!-- Mensaje cuando no existe matriz -->
                <div v-if="!matriz.id" class="alert alert-danger">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <i class="fas fa-exclamation-circle me-2"></i>
                      No se encontró la matriz de compromiso para esta evaluación.
                    </div>
                    <div>
                      <button @click="$router.back()" class="btn btn-sm btn-outline-danger me-2">
                        <i class="fas fa-arrow-left me-1"></i> Volver
                      </button>
                      <button @click="crearNuevaMatriz" class="btn btn-sm btn-primary">
                        <i class="fas fa-plus me-1"></i> Crear Nueva Matriz
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Contenido cuando existe matriz -->
                <div v-else>
                  <!-- Resumen de Verificadores -->
                  <div class="row mb-4">
                    <div class="col-md-4">
                      <div class="card border-success">
                        <div class="card-body text-center">
                          <h6 class="card-title text-success">Verificadores Cumplidos</h6>
                          <h3 class="text-success">{{ totalVerificadoresCumplidos }}</h3>
                          <button @click="mostrarVerificadoresCumplidos = !mostrarVerificadoresCumplidos"
                            class="btn btn-sm btn-outline-success">
                            <i :class="mostrarVerificadoresCumplidos ? 'fas fa-eye-slash' : 'fas fa-eye'"
                              class="me-1"></i>
                            {{ mostrarVerificadoresCumplidos ? 'Ocultar' : 'Mostrar' }}
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="card border-warning">
                        <div class="card-body text-center">
                          <h6 class="card-title text-warning">Verificadores No Aplica</h6>
                          <h3 class="text-warning">{{ totalVerificadoresNoAplica }}</h3>
                          <button @click="mostrarVerificadoresNoAplica = !mostrarVerificadoresNoAplica"
                            class="btn btn-sm btn-outline-warning">
                            <i :class="mostrarVerificadoresNoAplica ? 'fas fa-eye-slash' : 'fas fa-eye'"
                              class="me-1"></i>
                            {{ mostrarVerificadoresNoAplica ? 'Ocultar' : 'Mostrar' }}
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="card border-danger">
                        <div class="card-body text-center">
                          <h6 class="card-title text-danger">Verificadores No Cumplidos</h6>
                          <h3 class="text-danger">{{ totalVerificadoresNoCumplidos }}</h3>
                          <button @click="mostrarVerificadoresNoCumplidos = !mostrarVerificadoresNoCumplidos"
                            class="btn btn-sm btn-outline-danger">
                            <i :class="mostrarVerificadoresNoCumplidos ? 'fas fa-eye-slash' : 'fas fa-eye'"
                              class="me-1"></i>
                            {{ mostrarVerificadoresNoCumplidos ? 'Ocultar' : 'Mostrar' }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>


                  <!-- Sección de Verificadores No Aplica -->
                  <div v-if="mostrarVerificadoresNoAplica" class="mb-4">
                    <h5 class="card-title">
                      <i class="fas fa-info-circle text-warning me-2"></i>
                      Verificadores No Aplica
                    </h5>

                    <div v-if="verificadoresNoAplica.length === 0" class="alert alert-info">
                      <i class="fas fa-info-circle me-2"></i>
                      No hay verificadores marcados como "No Aplica"
                    </div>

                    <div v-else class="accordion" id="accordionNoAplica">
                      <template v-for="(grupo, subproceso) in agruparPorSubproceso(verificadoresNoAplica)"
                        :key="'na-'+subproceso">
                        <div class="accordion-item mb-2 border border-warning">
                          <h2 class="accordion-header">
                            <button class="accordion-button collapsed bg-warning bg-opacity-10" type="button"
                              data-bs-toggle="collapse" :data-bs-target="'#collapseNA-' + slugify(subproceso)"
                              aria-expanded="false">
                              <strong class="me-2">Subproceso:</strong> {{ subproceso }}
                              <span class="badge bg-warning ms-2">
                                {{ grupo.length }} verificador(es)
                              </span>
                            </button>
                          </h2>
                          <div :id="'collapseNA-' + slugify(subproceso)" class="accordion-collapse collapse"
                            data-bs-parent="#accordionNoAplica">
                            <div class="accordion-body p-2">
                              <div v-for="(verificador, index) in grupo" :key="'na-' + verificador.id"
                                class="mb-2 p-2 border-bottom border-warning border-opacity-25">
                                <div class="d-flex justify-content-between align-items-start">
                                  <div>
                                    <p class="mb-1"><strong>Verificador #{{ verificador.verificador?.orden || index + 1
                                    }}:</strong>
                                      {{ verificador.verificador_nombre }}</p>
                                    <span class="badge bg-warning">
                                      {{ verificador.estado_display }}
                                    </span>
                                  </div>
                                  <small class="text-muted">Código: {{ verificador.subproceso_codigo }}</small>
                                </div>
                                <p v-if="verificador.observaciones" class="mt-2 small">
                                  <strong>Observaciones:</strong> {{ verificador.observaciones }}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>
                    </div>
                  </div>

                  <!-- Sección de Verificadores No Cumplidos -->
                  <div v-if="mostrarVerificadoresNoCumplidos" class="mb-4">
                    <h5 class="card-title">
                      <i class="fas fa-exclamation-triangle text-danger me-2"></i>
                      Verificadores No Cumplidos
                    </h5>

                    <div v-if="verificadoresNoConformes.length === 0" class="alert alert-info">
                      <i class="fas fa-info-circle me-2"></i>
                      No hay verificadores no cumplidos para mostrar
                    </div>

                    <div v-else class="accordion" id="accordionNoCumplidos">
                      <template v-for="(grupo, subproceso) in agruparPorSubproceso(verificadoresNoConformes)"
                        :key="'nc-'+subproceso">
                        <div class="accordion-item mb-2 border border-danger">
                          <h2 class="accordion-header">
                            <button class="accordion-button collapsed bg-danger bg-opacity-10" type="button"
                              data-bs-toggle="collapse" :data-bs-target="'#collapseNC-' + slugify(subproceso)"
                              aria-expanded="false">
                              <strong class="me-2">Subproceso:</strong> {{ subproceso }}
                              <span class="badge bg-danger ms-2">
                                {{ grupo.length }} verificador(es)
                              </span>
                            </button>
                          </h2>
                          <div :id="'collapseNC-' + slugify(subproceso)" class="accordion-collapse collapse"
                            data-bs-parent="#accordionNoCumplidos">
                            <div class="accordion-body p-2">
                              <div v-for="(verificador, index) in grupo" :key="'nc-' + verificador.id"
                                class="mb-2 p-2 border-bottom border-danger border-opacity-25">
                                <div class="d-flex justify-content-between align-items-start">
                                  <div>
                                    <p class="mb-1"><strong>Verificador #{{ verificador.verificador?.orden || index + 1
                                    }}:</strong>
                                      {{ verificador.verificador_nombre }}</p>
                                    <span class="badge bg-danger">
                                      {{ verificador.estado_display }}
                                    </span>
                                  </div>
                                  <small class="text-muted">Código: {{ verificador.subproceso_codigo }}</small>
                                </div>
                                <p v-if="verificador.observaciones" class="mt-2 small">
                                  <strong>Observaciones:</strong> {{ verificador.observaciones }}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>
                    </div>
                  </div>

                  <!-- Sección de Verificadores Cumplidos -->
                  <div v-if="mostrarVerificadoresCumplidos" class="mb-4">
                    <h5 class="card-title">
                      <i class="fas fa-check-circle text-success me-2"></i>
                      Verificadores Cumplidos
                    </h5>

                    <div v-if="verificadoresCumplidos.length === 0" class="alert alert-info">
                      <i class="fas fa-info-circle me-2"></i>
                      No hay verificadores cumplidos para mostrar
                    </div>

                    <div v-else class="accordion" id="accordionCumplidos">
                      <template v-for="(grupo, subproceso) in agruparPorSubproceso(verificadoresCumplidos)"
                        :key="'c-'+subproceso">
                        <div class="accordion-item mb-2 border border-success">
                          <h2 class="accordion-header">
                            <button class="accordion-button collapsed bg-success bg-opacity-10" type="button"
                              data-bs-toggle="collapse" :data-bs-target="'#collapseC-' + slugify(subproceso)"
                              aria-expanded="false">
                              <strong class="me-2">Subproceso:</strong> {{ subproceso }}
                              <span class="badge bg-success ms-2">
                                {{ grupo.length }} verificador(es)
                              </span>
                            </button>
                          </h2>
                          <div :id="'collapseC-' + slugify(subproceso)" class="accordion-collapse collapse"
                            data-bs-parent="#accordionCumplidos">
                            <div class="accordion-body p-2">
                              <div v-for="(verificador, index) in grupo" :key="'c-' + verificador.id"
                                class="mb-2 p-2 border-bottom border-success border-opacity-25">
                                <div class="d-flex justify-content-between align-items-start">
                                  <div>
                                    <p class="mb-1"><strong>Verificador #{{ verificador.verificador?.orden || index + 1
                                    }}:</strong>
                                      {{ verificador.verificador_nombre }}</p>
                                    <span class="badge bg-success">
                                      {{ verificador.estado_display }}
                                    </span>
                                  </div>
                                  <small class="text-muted">Código: {{ verificador.subproceso_codigo }}</small>
                                </div>
                                <p v-if="verificador.observaciones" class="mt-2 small">
                                  <strong>Observaciones:</strong> {{ verificador.observaciones }}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>
                    </div>
                  </div>

                  <!-- Información de la Evaluación -->
                  <div class="mb-3">
                    <h5 class="card-title">
                      <i class="fas fa-info-circle text-primary me-2"></i>
                      Información de la Evaluación
                    </h5>
                    <div class="card border-0 shadow-sm">
                      <div class="card-body">
                        <div class="row">
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Dependencia:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.tipo }} - {{
                              matriz.evaluacion_data?.establecimiento }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Fecha del Monitoreo:</label>
                            <p class="fw-semibold">{{ formatDate(matriz.evaluacion_data?.fecha_monitoreo) }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Nombre del Proceso:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.proceso_nombre }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Tipo de Proceso:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.categoria }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Dueño del Proceso:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.dueño_proceso }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Monitor que generó la ficha:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.monitor_nombre }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Estado:</label>
                            <p class="fw-semibold">{{ matriz.evaluacion_data?.estado }}</p>
                          </div>
                          <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold text-muted">Total verificadores:</label>
                            <p class="fw-semibold">{{ totalVerificadores }} (C: {{ totalVerificadoresCumplidos }}, NC:
                              {{
                                totalVerificadoresNoCumplidos }}, NA: {{ totalVerificadoresNoAplica }})</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <hr>

                  <!-- Formulario de Matriz de Compromiso -->
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0">
                      <i class="fas fa-file-contract text-primary me-2"></i>
                      Matriz de Compromiso
                    </h5>
                    <div>
                      <button @click="exportarPDF" class="btn btn-success me-2">
                        <i class="fas fa-file-pdf me-2"></i> Exportar a PDF
                      </button>
                      <button @click="mostrarAyuda = !mostrarAyuda" class="btn btn-info">
                        <i class="fas fa-question-circle me-2"></i> Ayuda
                      </button>
                    </div>
                  </div>

                  <div v-if="mostrarAyuda" class="alert alert-info mb-4">
                    <button type="button" class="btn-close float-end" @click="mostrarAyuda = false"></button>
                    <h5><i class="fas fa-info-circle me-2"></i>Instrucciones</h5>
                    <ul class="mb-0">
                      <li>Complete todos los campos obligatorios marcados con <span class="text-danger">*</span></li>
                      <li>Para las firmas, haga clic en el área de firma y dibuje su firma con el mouse o dedo</li>
                      <li>Use el botón "Ayuda con IA" para generar automáticamente descripciones</li>
                      <li>Revise los plazos y responsables antes de guardar</li>
                    </ul>
                  </div>

                  <form @submit.prevent="guardarMatriz">
                    <!-- Descripción situacional -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">
                          Descripción del estado situacional del proceso <span class="text-danger">*</span>
                        </label>
                        <div class="input-group">
                          <textarea v-model="matriz.descripcion_situacional" class="form-control" rows="5" required
                            placeholder="Describa la situación actual del proceso"></textarea>
                          <button @click.prevent="generarDescripcion" class="btn btn-outline-primary" type="button"
                            :disabled="generandoDescripcion" title="Generar descripción con IA">
                            <template v-if="generandoDescripcion">
                              <span class="spinner-border spinner-border-sm me-2" role="status"
                                aria-hidden="true"></span>
                              Generando...
                            </template>
                            <template v-else>
                              <i class="fas fa-robot me-2"></i> Ayuda con IA
                            </template>
                          </button>
                        </div>
                        <small class="text-muted">Presiona el botón para obtener ayuda con la descripción</small>
                      </div>
                    </div>

                    <!-- Semáforo y Riesgo -->
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Semáforo <span class="text-danger">*</span></label>
                        <select v-model="matriz.semaforo" class="form-select" required>
                          <option value="Rojo">Rojo - No cumple</option>
                          <option value="Amarillo">Amarillo - Cumple parcialmente</option>
                          <option value="Verde">Verde - Cumple totalmente</option>
                        </select>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Identificación del Riesgo <span class="text-danger">*</span></label>
                        <textarea v-model="matriz.riesgo_identificado" class="form-control" rows="3" required
                          placeholder="Describa los riesgos identificados"></textarea>
                      </div>
                    </div>

                    <!-- Medidas correctivas y Hito esperado -->
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Medidas correctivas/Compromisos <span
                            class="text-danger">*</span></label>
                        <textarea v-model="matriz.medidas_correctivas" class="form-control" rows="3" required
                          placeholder="Describa las medidas correctivas a implementar"></textarea>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Hito esperado <span class="text-danger">*</span></label>
                        <textarea v-model="matriz.hito_esperado" class="form-control" rows="3" required
                          placeholder="Describa el resultado esperado"></textarea>
                      </div>
                    </div>

                    <!-- Plazos -->
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Plazo inicio <span class="text-danger">*</span></label>
                        <input v-model="matriz.plazo_inicio" type="date" class="form-control" required>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label">Plazo fin <span class="text-danger">*</span></label>
                        <input v-model="matriz.plazo_fin" type="date" class="form-control" required>
                        <small class="text-muted" v-if="diasPlazo > 0">
                          Duración: {{ diasPlazo }} día(s)
                        </small>
                      </div>
                    </div>

                    <!-- Firmas principales -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">Firmas obligatorias <span class="text-danger">*</span></label>
                        <div class="row">
                          <!-- Responsable directo (A) -->
                          <div class="col-md-4">
                            <div class="mb-3">
                              <label class="form-label">Responsable directo (A) <span
                                  class="text-danger">*</span></label>
                              <input v-model="matriz.responsable_directo" type="text" class="form-control mb-2" required
                                placeholder="Nombre del responsable">
                            </div>
                            <div v-if="matriz.firma_a" class="mb-3">
                              <img :src="matriz.firma_a" class="img-fluid border rounded" style="max-height: 150px;" />
                              <div class="d-flex mt-2">
                                <button @click="mostrarPadFirma('A')" class="btn btn-sm btn-outline-primary me-2">
                                  <i class="fas fa-edit me-1"></i> Reemplazar
                                </button>
                                <button @click="limpiarFirma('A')" class="btn btn-sm btn-outline-danger">
                                  <i class="fas fa-trash me-1"></i> Eliminar
                                </button>
                              </div>
                            </div>
                            <signature-pad v-else @save="setFirmaA" />
                          </div>

                          <!-- Funcionario (B) -->
                          <div class="col-md-4">
                            <div class="mb-3">
                              <label class="form-label">Funcionario del que depende directamente (B) <span
                                  class="text-danger">*</span></label>
                              <input v-model="matriz.funcionario_depen_directo" type="text" class="form-control mb-2"
                                required placeholder="Nombre del funcionario">
                            </div>
                            <div v-if="matriz.firma_b" class="mb-3">
                              <img :src="matriz.firma_b" class="img-fluid border rounded" style="max-height: 150px;" />
                              <div class="d-flex mt-2">
                                <button @click="mostrarPadFirma('B')" class="btn btn-sm btn-outline-primary me-2">
                                  <i class="fas fa-edit me-1"></i> Reemplazar
                                </button>
                                <button @click="limpiarFirma('B')" class="btn btn-sm btn-outline-danger">
                                  <i class="fas fa-trash me-1"></i> Eliminar
                                </button>
                              </div>
                            </div>
                            <signature-pad v-else @save="setFirmaB" />
                          </div>

                          <!-- Funcionario (C) -->
                          <div class="col-md-4">
                            <div class="mb-3">
                              <label class="form-label">Funcionario del que depende indirectamente (C) <span
                                  class="text-danger">*</span></label>
                              <input v-model="matriz.funcionario_depen_indirecto" type="text" class="form-control mb-2"
                                required placeholder="Nombre del funcionario">
                            </div>
                            <div v-if="matriz.firma_c" class="mb-3">
                              <img :src="matriz.firma_c" class="img-fluid border rounded" style="max-height: 150px;" />
                              <div class="d-flex mt-2">
                                <button @click="mostrarPadFirma('C')" class="btn btn-sm btn-outline-primary me-2">
                                  <i class="fas fa-edit me-1"></i> Reemplazar
                                </button>
                                <button @click="limpiarFirma('C')" class="btn btn-sm btn-outline-danger">
                                  <i class="fas fa-trash me-1"></i> Eliminar
                                </button>
                              </div>
                            </div>
                            <signature-pad v-else @save="setFirmaC" />
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Firmas adicionales -->
                    <div class="row mb-3">
                      <div class="col-md-12">
                        <label class="form-label">Firmas adicionales (máx. 5)</label>
                        <textarea v-model="matriz.firmas_adicionales" class="form-control" rows="2"
                          placeholder="Ingrese nombres completos separados por comas"></textarea>

                        <button v-if="!showFuncionarioD && !matriz.funcionario_d" @click="showFuncionarioD = true"
                          type="button" class="btn btn-sm btn-outline-primary mt-2">
                          <i class="fas fa-plus me-1"></i> Agregar Funcionario D
                        </button>
                      </div>
                    </div>

                    <!-- Funcionario D -->
                    <div v-if="showFuncionarioD || matriz.funcionario_d" class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Funcionario (D)</label>
                        <input v-model="matriz.funcionario_d" type="text" class="form-control"
                          placeholder="Nombre del funcionario">
                      </div>
                      <div class="col-md-6">
                        <h6>Firma Funcionario (D)</h6>
                        <div v-if="matriz.firma_d" class="mb-3">
                          <img :src="matriz.firma_d" class="img-fluid border rounded" style="max-height: 150px;" />
                          <button @click="mostrarPadFirma('D')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                            <i class="fas fa-edit me-1"></i> Reemplazar
                          </button>
                          <button @click="limpiarFirma('D')" class="btn btn-sm btn-outline-danger mt-2">
                            <i class="fas fa-trash me-1"></i> Eliminar
                          </button>
                        </div>
                        <signature-pad v-else @save="setFirmaD" />

                        <button v-if="!showFuncionarioE && !matriz.funcionario_e" @click="showFuncionarioE = true"
                          type="button" class="btn btn-sm btn-outline-primary mt-2">
                          <i class="fas fa-plus me-1"></i> Agregar Funcionario E
                        </button>
                      </div>
                    </div>

                    <!-- Funcionario E -->
                    <div v-if="showFuncionarioE || matriz.funcionario_e" class="row mb-3">
                      <div class="col-md-6">
                        <label class="form-label">Funcionario (E)</label>
                        <input v-model="matriz.funcionario_e" type="text" class="form-control"
                          placeholder="Nombre del funcionario">
                      </div>
                      <div class="col-md-6">
                        <h6>Firma Funcionario (E)</h6>
                        <div v-if="matriz.firma_e" class="mb-3">
                          <img :src="matriz.firma_e" class="img-fluid border rounded" style="max-height: 150px;" />
                          <button @click="mostrarPadFirma('E')" class="btn btn-sm btn-outline-primary mt-2 me-2">
                            <i class="fas fa-edit me-1"></i> Reemplazar
                          </button>
                          <button @click="limpiarFirma('E')" class="btn btn-sm btn-outline-danger mt-2">
                            <i class="fas fa-trash me-1"></i> Eliminar
                          </button>
                        </div>
                        <signature-pad v-else @save="setFirmaE" />
                      </div>
                    </div>


                    <div class="text-center mt-4">
                      <button type="submit" class="btn btn-primary me-2" :disabled="saving">
                        <template v-if="saving">
                          <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                          Guardando...
                        </template>
                        <template v-else>
                          <i class="fas fa-save me-2"></i> Guardar Matriz
                        </template>
                      </button>
                      <button type="button" @click="cancelar" class="btn btn-secondary me-2">
                        <i class="fas fa-times me-2"></i> Cancelar
                      </button>
                      <button type="button" @click="resetForm" class="btn btn-outline-secondary">
                        <i class="fas fa-sync-alt me-2"></i> Reiniciar
                      </button>
                    </div>
                  </form>
                </div>
              </div>

              <!-- Modal para reemplazar firmas -->
              <div v-if="showSignatureModal" class="modal fade show d-block" tabindex="-1"
                style="background-color: rgba(0,0,0,0.5); z-index: 1060;">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Reemplazar Firma {{ firmaActual }}</h5>
                      <button type="button" class="btn-close" @click="cerrarModalFirma"></button>
                    </div>
                    <div class="modal-body">
                      <signature-pad ref="signaturePad" @save="guardarFirmaReemplazo" />
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModalFirma">Cancelar</button>
                      <button type="button" class="btn btn-primary" @click="guardarFirmaDesdeModal">Guardar
                        Firma</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios'
import SignaturePad from '@/components/SignaturePad.vue'
import { useToast } from 'vue-toast-notification'
import { generateText } from '@/components/services/gemini'
import 'vue-toast-notification/dist/theme-sugar.css'

const route = useRoute()
const router = useRouter()
const $toast = useToast()

// Estados
const loading = ref(true)
const saving = ref(false)
const generandoDescripcion = ref(false)
// En la sección de estados
const mostrarVerificadoresCumplidos = ref(false)
const mostrarVerificadoresNoAplica = ref(false)
const mostrarVerificadoresNoCumplidos = ref(true)

const mostrarAyuda = ref(false)
const showSignatureModal = ref(false)
const firmaActual = ref('')
const signaturePad = ref(null)
const showFuncionarioD = ref(false)
const showFuncionarioE = ref(false)

// Refs para firmas
const firmaA = ref(null)
const firmaB = ref(null)
const firmaC = ref(null)
const firmaD = ref(null)
const firmaE = ref(null)

// Datos de la matriz
const matriz = ref({
  id: null,
  evaluacion: null,
  descripcion_situacional: '',
  semaforo: 'Rojo',
  riesgo_identificado: '',
  medidas_correctivas: '',
  hito_esperado: '',
  plazo_inicio: '',
  plazo_fin: '',
  responsable_directo: '',
  funcionario_depen_directo: '',
  funcionario_depen_indirecto: '',
  firmas_adicionales: '',
  firma_a: null,
  firma_b: null,
  firma_c: null,
  firma_d: null,
  firma_e: null,
  funcionario_d: '',
  funcionario_e: '',
  evaluacion_data: null,
  evaluaciones_nc: []
})

// Reemplaza las computed properties existentes por estas:
const todasEvaluaciones = computed(() => matriz.value.todas_evaluaciones || [])

const totalVerificadores = computed(() => {
  return todasEvaluaciones.value.length
})

const totalVerificadoresCumplidos = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'C').length
})

const totalVerificadoresNoCumplidos = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'NC').length
})

const totalVerificadoresNoAplica = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'NA').length
})

const verificadoresCumplidos = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'C')
})
const verificadoresNoAplica = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'NA')
})
const verificadoresNoConformes = computed(() => {
  return todasEvaluaciones.value.filter(e => e.estado === 'NC')
})
const diasPlazo = computed(() => {
  if (!matriz.value.plazo_inicio || !matriz.value.plazo_fin) return 0

  const start = new Date(matriz.value.plazo_inicio)
  const end = new Date(matriz.value.plazo_fin)
  const diff = end.getTime() - start.getTime()

  return Math.ceil(diff / (1000 * 3600 * 24)) + 1 // +1 para incluir ambos días
})


// Métodos auxiliares
const agruparPorSubproceso = (evaluaciones) => {
  return evaluaciones.reduce((acc, nc) => {
    const subproceso = nc.subproceso_nombre
    if (!acc[subproceso]) {
      acc[subproceso] = []
    }
    acc[subproceso].push(nc)
    return acc
  }, {})
}

const slugify = (text) => {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '')             // Trim - from end of text
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const dataURLtoBlob = (dataURL) => {
  const arr = dataURL.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }

  return new Blob([u8arr], { type: mime })
}

// Métodos para manejar firmas
const mostrarPadFirma = async (tipo) => {
  firmaActual.value = tipo
  showSignatureModal.value = true

  await nextTick()

  if (signaturePad.value && signaturePad.value.clearSignature) {
    signaturePad.value.clearSignature()
  }
}

const cerrarModalFirma = () => {
  showSignatureModal.value = false
}

const guardarFirmaDesdeModal = () => {
  if (signaturePad.value && signaturePad.value.saveSignature) {
    signaturePad.value.saveSignature()
  }
}

const guardarFirmaReemplazo = (firma) => {
  if (!firma || !firmaActual.value) return

  const firmaProp = `firma_${firmaActual.value.toLowerCase()}`
  const firmaRef = `firma${firmaActual.value}`

  if (firmaRef in { firmaA, firmaB, firmaC, firmaD, firmaE }) {
    eval(`${firmaRef}.value = firma`)
  }
  matriz.value[firmaProp] = firma

  showSignatureModal.value = false
}

const setFirmaA = (firma) => {
  firmaA.value = firma
  matriz.value.firma_a = firma
}

const setFirmaB = (firma) => {
  firmaB.value = firma
  matriz.value.firma_b = firma
}

const setFirmaC = (firma) => {
  firmaC.value = firma
  matriz.value.firma_c = firma
}

const setFirmaD = (firma) => {
  firmaD.value = firma
  matriz.value.firma_d = firma
}

const setFirmaE = (firma) => {
  firmaE.value = firma
  matriz.value.firma_e = firma
}

const limpiarFirma = (tipo) => {
  const firmaProp = `firma_${tipo.toLowerCase()}`
  const firmaRef = `firma${tipo}`

  if (firmaRef in { firmaA, firmaB, firmaC, firmaD, firmaE }) {
    eval(`${firmaRef}.value = null`)
  }
  matriz.value[firmaProp] = null

  if (tipo === 'D' && !matriz.value.funcionario_d) {
    showFuncionarioD.value = false
  }
  if (tipo === 'E' && !matriz.value.funcionario_e) {
    showFuncionarioE.value = false
  }
}

// Métodos principales
const generarDescripcion = async () => {
  try {
    generandoDescripcion.value = true;
    const textoExistente = matriz.value.descripcion_situacional || '';

    // Obtener verificadores no conformes (NC)
    const verificadoresNC = matriz.value.evaluaciones_nc
      ?.filter(nc => nc.estado === 'NC')
      .map(nc => nc.verificador_nombre) || ['No especificados'];

    // Obtener nombre del proceso
    const nombreProceso = matriz.value.evaluacion_data?.proceso_nombre || 'No especificado';

    // Construir el prompt de forma más limpia
    const prompt = `
Como experto en redacción técnica profesional, genera una descripción formal del estado situacional 
de un proceso, considerando los siguientes elementos:

1. Verificadores no conformes: ${JSON.stringify(verificadoresNC)}
2. Proceso evaluado: ${nombreProceso}
3. Contexto: ${matriz.value.evaluacion_data?.categoria || 'No especificado'}

El texto debe:
- Ser técnico y profesional
- Estar estructurado en párrafos coherentes
- Mencionar los principales hallazgos
- Ser adecuado para un documento oficial
- Tener entre 100 y 200 palabras

Formato requerido:
- No incluir títulos o encabezados
- Usar lenguaje formal pero claro
- Evitar repeticiones

Texto existente (puedes mejorarlo): "${textoExistente}"

Devuelve SOLO el texto mejorado, sin comentarios adicionales.`;

    const descripcionGenerada = await generateText(prompt);

    // Limpiar y formatear la respuesta
    matriz.value.descripcion_situacional = descripcionGenerada
      .trim()
      .replace(/^"+|"+$/g, '')  // Eliminar comillas al inicio/final
      .replace(/\\n/g, '\n')     // Convertir saltos de línea escapados
      .replace(/\*\*/g, '')      // Eliminar marcadores de negrita si existen
      .replace(/^\s*-\s*/gm, '') // Eliminar viñetas si las usa
      .replace(/\s{2,}/g, ' ');  // Normalizar espacios múltiples

    $toast.success('Descripción generada con éxito', {
      position: 'top-right',
      duration: 3000
    });
  } catch (error) {
    console.error('Error al generar descripción:', error);
    $toast.error(error.response?.data?.message || 'Error al generar la descripción automática', {
      position: 'top-right',
      duration: 5000
    });
  } finally {
    generandoDescripcion.value = false;
  }
}

const resetForm = () => {
  if (confirm('¿Está seguro de reiniciar el formulario? Se perderán los cambios no guardados.')) {
    // Mantener solo los datos esenciales
    matriz.value = {
      ...matriz.value,
      descripcion_situacional: '',
      semaforo: 'Rojo',
      riesgo_identificado: '',
      medidas_correctivas: '',
      hito_esperado: '',
      plazo_inicio: '',
      plazo_fin: '',
      responsable_directo: '',
      funcionario_depen_directo: '',
      funcionario_depen_indirecto: '',
      firmas_adicionales: '',
      firma_a: null,
      firma_b: null,
      firma_c: null,
      firma_d: null,
      firma_e: null,
      funcionario_d: '',
      funcionario_e: ''
    }

    // Resetear firmas reactivas
    firmaA.value = null
    firmaB.value = null
    firmaC.value = null
    firmaD.value = null
    firmaE.value = null

    // Ocultar campos adicionales
    showFuncionarioD.value = false
    showFuncionarioE.value = false

    $toast.info('Formulario reiniciado')
  }
}

const crearNuevaMatriz = async () => {
  try {
    loading.value = true
    const response = await api.post('ficha/matriz-compromiso/', {
      evaluacion: route.params.id
    })

    matriz.value = {
      ...matriz.value,
      ...response.data,
      id: response.data.id
    }

    $toast.success('Matriz creada correctamente')
    await fetchData()
  } catch (error) {
    console.error('Error al crear matriz:', error)
    $toast.error('Error al crear la matriz')
  } finally {
    loading.value = false
  }
}

const fetchData = async () => {
  try {
    loading.value = true
    const matrizResponse = await api.get(`ficha/matriz-compromiso/${route.params.id}/`)

    if (matrizResponse.data) {
      // Asignar todos los datos de la matriz
      matriz.value = {
        ...matriz.value,
        ...matrizResponse.data,
        firma_a: matrizResponse.data.firma_a || null,
        firma_b: matrizResponse.data.firma_b || null,
        firma_c: matrizResponse.data.firma_c || null,
        firma_d: matrizResponse.data.firma_d || null,
        firma_e: matrizResponse.data.firma_e || null
      }

      // Mostrar campos D y E si tienen datos
      if (matriz.value.funcionario_d) showFuncionarioD.value = true
      if (matriz.value.funcionario_e) showFuncionarioE.value = true

      // Asignar firmas a las variables reactivas
      firmaA.value = matriz.value.firma_a
      firmaB.value = matriz.value.firma_b
      firmaC.value = matriz.value.firma_c
      firmaD.value = matriz.value.firma_d
      firmaE.value = matriz.value.firma_e

      // Obtener datos de evaluación si no están incluidos
      if (!matriz.value.evaluacion_data && matriz.value.evaluacion) {
        const evaluacionResponse = await api.get(`ficha/evaluaciones/${matriz.value.evaluacion}/`)
        matriz.value.evaluacion_data = evaluacionResponse.data
      }
    }
  } catch (error) {
    console.error('Error al cargar datos:', error)
    $toast.error('Error al cargar la matriz de compromiso')
  } finally {
    loading.value = false
  }
}

const guardarMatriz = async () => {
  try {
    saving.value = true

    // Validación básica
    if (!matriz.value.descripcion_situacional ||
      !matriz.value.riesgo_identificado ||
      !matriz.value.medidas_correctivas ||
      !matriz.value.hito_esperado ||
      !matriz.value.plazo_inicio ||
      !matriz.value.plazo_fin ||
      !matriz.value.responsable_directo ||
      !matriz.value.funcionario_depen_directo ||
      !matriz.value.funcionario_depen_indirecto) {
      $toast.warning('Por favor complete todos los campos requeridos')
      return
    }

    // Validar fechas
    const inicio = new Date(matriz.value.plazo_inicio)
    const fin = new Date(matriz.value.plazo_fin)

    if (fin < inicio) {
      $toast.warning('La fecha de fin no puede ser anterior a la fecha de inicio')
      return
    }

    // Validar firmas obligatorias
    if (!matriz.value.firma_a || !matriz.value.firma_b || !matriz.value.firma_c) {
      $toast.warning('Debe registrar las firmas obligatorias (A, B y C)')
      return
    }

    // Crear FormData para enviar archivos
    const formData = new FormData()

    // Agregar todos los campos de la matriz
    for (const key in matriz.value) {
      if (key.startsWith('firma_')) continue
      if (matriz.value[key] !== null && matriz.value[key] !== undefined) {
        formData.append(key, matriz.value[key])
      }
    }

    // Agregar las firmas como archivos
    const firmas = {
      'firma_a': firmaA.value,
      'firma_b': firmaB.value,
      'firma_c': firmaC.value,
      'firma_d': firmaD.value,
      'firma_e': firmaE.value
    }

    for (const [key, value] of Object.entries(firmas)) {
      if (value) {
        if (typeof value === 'string' && (value.startsWith('http') || value.startsWith('/'))) {
          formData.append(key, value)
        } else {
          const blob = dataURLtoBlob(value)
          formData.append(key, blob, `${key}.png`)
        }
      } else {
        formData.append(key, '')
      }
    }

    const config = {
      headers: { 'Content-Type': 'multipart/form-data' }
    }

    if (matriz.value.id) {
      await api.put(`ficha/matriz-compromiso/${matriz.value.id}/`, formData, config)
      $toast.success('Matriz actualizada correctamente')
    } else {
      const response = await api.post('ficha/matriz-compromiso/', formData, config)
      matriz.value.id = response.data.id
      $toast.success('Matriz creada correctamente')
    }

    // Recargar datos para asegurar consistencia
    await fetchData()
  } catch (error) {
    console.error('Error al guardar la matriz:', error)
    $toast.error(error.response?.data?.message || 'Error al guardar la matriz')
  } finally {
    saving.value = false
  }
}

const exportarPDF = async () => {
  try {
    if (!matriz.value?.id) {
      $toast.warning('Debe guardar la matriz antes de exportar')
      return
    }

    const response = await api.get(
      `ficha/matriz-compromiso/${matriz.value.id}/export_pdf/`,
      { responseType: 'blob' }
    )

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `matriz_compromiso_${matriz.value.id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error al exportar PDF:', error)
    $toast.error('Error al generar el PDF')
  }
}

const cancelar = () => {
  if (confirm('¿Está seguro de salir sin guardar los cambios?')) {
    router.back()
  }
}

onMounted(() => {
  fetchData()
})
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

.form-label {
  font-weight: 500;
  color: #495057;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(13, 110, 253, 0.1);
  color: #012970;
}

.accordion-item {
  border-radius: 5px !important;
}

.badge {
  font-weight: 500;
  padding: 5px 8px;
}

.signature-container {
  border: 1px dashed #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
}

.signature-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.btn-export {
  background-color: #2ecc71;
  border-color: #2ecc71;
  transition: all 0.3s;
}

.btn-export:hover {
  background-color: #27ae60;
  border-color: #27ae60;
  transform: translateY(-2px);
}

.input-group-text {
  cursor: pointer;
  transition: all 0.3s;
}

.input-group-text:hover {
  background-color: #e9ecef;
}

.firma-img-container {
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #fff;
  text-align: center;
}

.firma-img {
  max-height: 120px;
  display: block;
  margin: 0 auto;
  border: 1px solid #eee;
  border-radius: 3px;
}

.firma-actions {
  margin-top: 10px;
  display: flex;
  gap: 5px;
  justify-content: center;
}

.modal-content {
  border-radius: 10px;
}

/* Estilos para los acordeones de verificadores */
.accordion-button {
  font-weight: 500;
}

.accordion-body {
  background-color: rgba(248, 249, 250, 0.5);
}

/* Estilo para los cards de resumen */
.card-border {
  border-left: 4px solid transparent;
}

.card-border-success {
  border-left-color: #2ecc71;
}

.card-border-warning {
  border-left-color: #f39c12;
}

.card-border-danger {
  border-left-color: #e74c3c;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-body {
    padding: 15px;
  }

  .form-label {
    font-size: 14px;
  }

  .btn {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>
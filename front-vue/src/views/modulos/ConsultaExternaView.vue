<template>
    <main id="main" class="main">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Importar Consultas Externas</h5>

                <!-- Sección desplegable de estructura del Excel -->
                <div class="alert alert-info cursor-pointer" @click="toggleEstructura">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="bi bi-info-circle"></i> Estructura requerida del Excel (columnas en orden exacto)
                        </div>
                        <i :class="mostrarEstructura ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
                    </div>

                    <transition name="slide-fade">
                        <div v-if="mostrarEstructura" class="overflow-auto">
                            <table class="table table-sm mt-2">
                                <thead>
                                    <tr>
                                        <th># Columna</th>
                                        <th>Campo</th>
                                        <th>Requerido</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>0</td>
                                        <td>Tipo de seguro</td>
                                        <td><span class="text-danger">*</span></td>
                                    </tr>
                                    <tr>
                                        <td>1</td>
                                        <td>Fecha Nacimiento</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>2</td>
                                        <td>Sexo (M/F)</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>3</td>
                                        <td>Lugar de procedencia</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>4</td>
                                        <td>Tipo de documento</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>5</td>
                                        <td>N° de documento</td>
                                        <td><span class="text-danger">*</span></td>
                                    </tr>
                                    <tr>
                                        <td>6</td>
                                        <td>N° HCL</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>7</td>
                                        <td>Fecha y Hora de Cita Otorgada</td>
                                        <td><span class="text-danger">*</span></td>
                                    </tr>
                                    <tr>
                                        <td>8</td>
                                        <td>Fecha y Hora de atención efectiva</td>
                                        <td><span class="text-danger">*</span></td>
                                    </tr>
                                    <tr>
                                        <td>9</td>
                                        <td>Diagnóstico Médico</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>10</td>
                                        <td>Dx CIE-10 Principal</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>11</td>
                                        <td>Dx CIE-10 Secundario</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>12</td>
                                        <td>Dx CIE-10 Terciario</td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>13</td>
                                        <td>Especialidad</td>
                                        <td></td>
                                    </tr>
                                </tbody>
                            </table>
                            <small class="text-muted">Las columnas deben estar exactamente en este orden (comenzando
                                desde 0)</small>
                        </div>
                    </transition>
                </div>

                <!-- Formulario de importación -->
                <div class="mb-3">
                    <label for="excelFile" class="form-label">Seleccionar archivo Excel</label>
                    <input type="file" class="form-control" id="excelFile" accept=".xlsx, .xls"
                        @change="handleFileChange" :disabled="loading">
                    <div class="form-text">Formatos soportados: .xlsx, .xls (Máx. 10MB)</div>
                </div>

                <div class="d-flex flex-wrap gap-2 mb-4">
                    <button class="btn btn-primary" :disabled="!file || loading" @click="uploadFile">
                        <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                        {{ loading ? 'Importando...' : 'Importar Datos' }}
                    </button>

                    <button class="btn btn-outline-secondary" @click="resetForm" :disabled="loading">
                        Limpiar
                    </button>
                    <!-- Nuevo botón para exportar a Excel -->
                    <button class="btn btn-success" @click="exportToExcel"
                        :disabled="registros.length === 0 || loading">
                        <i class="bi bi-file-excel"></i> Exportar Excel
                    </button>
                    <!-- Agrega esto en la sección de filtros, cerca del buscador -->
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label class="form-label">Año</label>
                            <select class="form-select" v-model="filtroAnio" @change="cargarRegistros">
                                <option v-for="year in [...new Set(mesesDisponibles.map(item => item.year))]"
                                    :key="year" :value="year">
                                    {{ year }}
                                </option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Mes</label>
                            <select class="form-select" v-model="filtroMes" @change="cargarRegistros">
                                <option v-for="month in mesesDisponibles.filter(item => item.year === filtroAnio)"
                                    :key="`${month.year}-${month.month}`" :value="month.month">
                                    {{ month.month }} - {{ getMonthName(month.month) }}
                                </option>
                            </select>
                        </div>
                        <div class="col-md-4 d-flex align-items-end">
                            <button class="btn btn-outline-secondary" @click="resetFiltros" :disabled="!filtroMes">
                                Limpiar filtros
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Resultados de importación -->
                <div v-if="importResult" class="mt-3 alert"
                    :class="importResult.success ? 'alert-success' : 'alert-danger'">
                    <h5 class="alert-heading">{{ importResult.message }}</h5>
                    <hr>

                    <div v-if="importResult.success && importResult.omitidas > 0" class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle-fill"></i>
                        Se omitieron {{ importResult.omitidas }} registros con fechas anteriores a marzo 2025
                    </div>

                    <template v-if="importResult.success">
                        <div class="row">
                            <div class="col-md-3">
                                <p><strong>Total filas procesadas:</strong> {{ importResult.total_filas }}</p>
                            </div>
                            <div class="col-md-3">
                                <p><strong>Registros creados:</strong> {{ importResult.creados }}</p>
                            </div>
                            <div class="col-md-3">
                                <p><strong>Registros actualizados:</strong> {{ importResult.actualizados }}</p>
                            </div>
                            <div class="col-md-3" v-if="importResult.omitidas > 0">
                                <p><strong>Registros omitidos:</strong> {{ importResult.omitidas }}</p>
                            </div>
                        </div>
                    </template>
                    <div v-if="importResult.detalle_errores && importResult.detalle_errores.length" class="mt-2">
                        <button class="btn btn-sm btn-outline-danger" @click="toggleErrores">
                            {{ mostrarErrores ? 'Ocultar' : 'Mostrar' }} detalles de errores ({{ importResult.errores
                            }})
                        </button>

                        <transition name="slide-fade">
                            <div v-if="mostrarErrores" class="mt-2">
                                <h6>Resumen de errores:</h6>

                                <!-- Agrupar errores por tipo -->
                                <div class="mb-3" v-if="erroresPorTipo.length">
                                    <div v-for="(tipo, index) in erroresPorTipo" :key="index" class="mb-2">
                                        <span class="badge bg-danger me-1">{{ tipo.count }}</span>
                                        {{ tipo.message }}
                                    </div>
                                </div>

                                <h6>Detalles completos:</h6>
                                <ul class="list-unstyled">
                                    <li v-for="(error, index) in importResult.detalle_errores" :key="index"
                                        class="mb-1">
                                        <span class="badge bg-danger me-1">{{ index + 1 }}</span>
                                        {{ error }}
                                    </li>
                                </ul>
                            </div>
                        </transition>
                    </div>
                </div>

                <!-- Listado de registros -->
                <div class="mt-5">
                    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3">
                        <h5 class="card-title mb-2 mb-md-0">Registros Importados ({{ totalRegistros.toLocaleString() }})
                        </h5>

                        <div class="d-flex flex-column flex-md-row gap-2">
                            <div class="input-group" style="max-width: 300px;">
                                <span class="input-group-text"><i class="bi bi-search"></i></span>
                                <input type="text" class="form-control" placeholder="Buscar..." v-model="busqueda"
                                    @input="debounceBuscar">
                                <button class="btn btn-outline-secondary" type="button" @click="resetBusqueda"
                                    :disabled="!busqueda">
                                    <i class="bi bi-x-lg"></i>
                                </button>
                            </div>

                            <select class="form-select" v-model="itemsPorPagina" @change="cargarRegistros"
                                style="max-width: 150px;">
                                <option value="10">10 por página</option>
                                <option value="25">25 por página</option>
                                <option value="50">50 por página</option>
                                <option value="100">100 por página</option>
                                <option value="200">200 por página</option>
                            </select>
                        </div>
                    </div>

                    <div class="table-responsive">
                        <table class="table table-striped table-hover table-sm">
                            <thead class="table-light">
                                <tr>
                                    <th>Tipo Seguro</th>
                                    <th>Fecha Nacimiento</th>
                                    <th>N° Documento</th>
                                    <th>fecha_hora_cita_otorgada</th>
                                    <th>Fecha Atención</th>
                                    <th>Especialidad</th>
                                    <th>Diagnóstico</th>
                                    <th class="text-end">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in registros" :key="item.id">
                                    <td>{{ item.tipo_seguro || 'N/A' }}</td>
                                    <td>{{ formatFecha(item.fecha_nacimiento) }}</td>

                                    <td>{{ item.documento }}</td>
                                    <td>{{ formatDateTime(item.fecha_hora_cita_otorgada) }}</td>
                                    <td>{{ formatDateTime(item.fecha_hora_atencion) }}</td>
                                    <td>{{ item.especialidad || 'N/A' }}</td>
                                    <td>
                                        <span v-if="item.diagnostico_medico" :title="item.diagnostico_medico">
                                            {{ truncateText(item.diagnostico_medico, 30) }}
                                        </span>
                                        <span v-else>N/A</span>
                                    </td>
                                    <td class="text-end">
                                        <button class="btn btn-sm btn-outline-primary" @click="verDetalle(item)">
                                            <i class="bi bi-eye"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-if="registros.length === 0" class="text-center py-4">
                        <div class="alert alert-info">
                            No se encontraron registros. Importe un archivo Excel para comenzar.
                        </div>
                    </div>

                    <!-- Paginación mejorada -->
                    <nav aria-label="Paginación" class="mt-3" v-if="paginacion.total_pages > 1">
                        <ul class="pagination justify-content-center flex-wrap">
                            <li class="page-item" :class="{ disabled: paginacion.current_page === 1 }">
                                <button class="page-link" @click="cambiarPagina(1)"
                                    :disabled="paginacion.current_page === 1">
                                    <i class="bi bi-chevron-double-left"></i>
                                </button>
                            </li>
                            <li class="page-item" :class="{ disabled: paginacion.current_page === 1 }">
                                <button class="page-link" @click="cambiarPagina(paginacion.current_page - 1)"
                                    :disabled="paginacion.current_page === 1">
                                    <i class="bi bi-chevron-left"></i>
                                </button>
                            </li>

                            <!-- Mostrar páginas cercanas a la actual -->
                            <template v-for="page in paginasVisibles" :key="page">
                                <li class="page-item" :class="{ active: paginacion.current_page === page }">
                                    <button class="page-link" @click="cambiarPagina(page)">
                                        {{ page }}
                                    </button>
                                </li>
                            </template>

                            <li class="page-item"
                                :class="{ disabled: paginacion.current_page === paginacion.total_pages }">
                                <button class="page-link" @click="cambiarPagina(paginacion.current_page + 1)"
                                    :disabled="paginacion.current_page === paginacion.total_pages">
                                    <i class="bi bi-chevron-right"></i>
                                </button>
                            </li>
                            <li class="page-item"
                                :class="{ disabled: paginacion.current_page === paginacion.total_pages }">
                                <button class="page-link" @click="cambiarPagina(paginacion.total_pages)"
                                    :disabled="paginacion.current_page === paginacion.total_pages">
                                    <i class="bi bi-chevron-double-right"></i>
                                </button>
                            </li>
                        </ul>

                        <div class="text-center text-muted">
                            Página {{ paginacion.current_page }} de {{ paginacion.total_pages }}
                            (Mostrando {{ registros.length }} de {{ totalRegistros.toLocaleString() }} registros)
                        </div>
                    </nav>
                </div>
            </div>
        </div>

        <!-- Modal de detalle -->
        <div class="modal fade" id="detalleModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalle de Consulta Externa</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="registroSeleccionado" class="row">
                            <div class="col-md-6">
                                <p><strong>Documento:</strong> {{ registroSeleccionado.documento }}</p>
                                <p><strong>Tipo de Seguro:</strong> {{ registroSeleccionado.tipo_seguro || 'N/A' }}</p>
                                <p><strong>Fecha Nacimiento:</strong> {{
                                    formatFecha(registroSeleccionado.fecha_nacimiento) }}
                                </p>
                                <p><strong>Sexo:</strong> {{ registroSeleccionado.sexo || 'N/A' }}</p>
                                <p><strong>Procedencia:</strong> {{ registroSeleccionado.lugar_procedencia || 'N/A' }}
                                </p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Fecha Cita:</strong> {{ formatDateTime(registroSeleccionado.fecha_hora_cita)
                                    }}</p>
                                <p><strong>Fecha Atención:</strong> {{
                                    formatDateTime(registroSeleccionado.fecha_hora_atencion)
                                    }}</p>
                                <p><strong>Especialidad:</strong> {{ registroSeleccionado.especialidad || 'N/A' }}</p>
                                <p><strong>CIE-10 Principal:</strong> {{ registroSeleccionado.dx_cie10_principal ||
                                    'N/A' }}</p>
                            </div>
                            <div class="col-12 mt-3" v-if="registroSeleccionado.diagnostico_medico">
                                <p class="fw-bold">Diagnóstico Médico:</p>
                                <div class="border p-2 bg-light">
                                    {{ registroSeleccionado.diagnostico_medico }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/components/services/auth_axios'
import { debounce } from 'lodash'
import { Modal } from 'bootstrap'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'

// Variables para estructura desplegable
const mostrarEstructura = ref(false)
const mostrarErrores = ref(false)
const toggleEstructura = () => {
    mostrarEstructura.value = !mostrarEstructura.value
}
const toggleErrores = () => {
    mostrarErrores.value = !mostrarErrores.value
}
// Método para obtener el nombre del mes
const getMonthName = (month) => {
  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ]
  return months[month - 1] || ''
}

// Método para resetear los filtros
const resetFiltros = () => {
  filtroMes.value = null
  filtroAnio.value = null
  cargarRegistros()
}
// Variables para importación
const file = ref(null)
const loading = ref(false)
const importResult = ref(null)

// Variables para listado
const registros = ref([])
const registroSeleccionado = ref(null)
const busqueda = ref('')
const itemsPorPagina = ref(25)
const totalRegistros = ref(0)

// Agrega estas variables al inicio de tu script
const mesesDisponibles = ref([])
const filtroMes = ref(null)
const filtroAnio = ref(null)


const paginacion = ref({
    current_page: 1,
    total_pages: 1
})

// Agrega este método para cargar los meses disponibles
const cargarMesesDisponibles = async () => {
    try {
        const response = await api.get('/user/consultas-externas/meses-disponibles/')
        mesesDisponibles.value = response.data

        // Si hay datos, establecer el primer mes como seleccionado por defecto
        if (mesesDisponibles.value.length > 0) {
            filtroAnio.value = mesesDisponibles.value[0].year
            filtroMes.value = mesesDisponibles.value[0].month
        }
    } catch (error) {
        console.error('Error cargando meses disponibles:', error)
    }
}

// Método para exportar a Excel
const exportToExcel = async () => {
    try {
        loading.value = true

        // Obtener todos los registros del usuario
        const response = await api.get('/user/consultas-externas/exportar-todos/', {
            params: {
                search: busqueda.value // Opcional: mantener el filtro de búsqueda
            }
        })

        const data = response.data

        if (data.length === 0) {
            importResult.value = {
                success: false,
                message: 'No hay datos para exportar'
            }
            return
        }

        // Función para formatear fechas
        const formatDateForExcel = (dateStr) => {
            if (!dateStr) return 'N/A'
            const date = new Date(dateStr)
            return isNaN(date.getTime()) ? 'N/A' : date.toLocaleString('es-ES')
        }

        // Preparar los datos para Excel
        const excelData = data.map(item => ({
            'Tipo Seguro': item.tipo_seguro,
            'Fecha Nacimiento': formatDateForExcel(item.fecha_nacimiento),
            'Sexo': item.sexo,
            'Lugar Procedencia': item.lugar_procedencia,
            'Tipo Documento': item.tipo_documento,
            'Documento': item.documento,
            'N° HCL': item.n_hcl,
            'Fecha Cita Otorgada': formatDateForExcel(item.fecha_hora_cita_otorgada),
            'Fecha Atención': formatDateForExcel(item.fecha_hora_atencion),
            'Diagnóstico Médico': item.diagnostico_medico,
            'Dx CIE-10 Principal': item.dx_CIE_10_1,
            'Dx CIE-10 Secundario': item.dx_CIE_10_2,
            'Dx CIE-10 Terciario': item.dx_CIE_10_3,
            'Especialidad': item.especialidad,
            'Creado Por': item.creado_por__username || 'N/A',
            'Fecha Creación': formatDateForExcel(item.fecha_creacion)
        }))

        // Crear hoja de trabajo con opciones para grandes conjuntos de datos
        const worksheet = XLSX.utils.json_to_sheet(excelData, {
            cellDates: true,
            dateNF: 'dd/mm/yyyy hh:mm:ss'
        })

        // Ajustar el ancho de las columnas
        const wscols = [
            { wch: 15 }, { wch: 15 }, { wch: 5 },
            { wch: 20 }, { wch: 15 }, { wch: 15 },
            { wch: 15 }, { wch: 20 }, { wch: 20 },
            { wch: 30 }, { wch: 15 }, { wch: 15 },
            { wch: 15 }, { wch: 20 }, { wch: 15 },
            { wch: 20 }
        ]
        worksheet['!cols'] = wscols

        // Crear libro de trabajo
        const workbook = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(workbook, worksheet, 'ConsultasExternas')

        // Generar archivo Excel en formato binario
        const excelBuffer = XLSX.write(workbook, {
            bookType: 'xlsx',
            type: 'array',
            compression: true
        })

        // Crear y descargar el blob
        const blob = new Blob([excelBuffer], {
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        // Nombre del archivo con fecha y hora
        const dateStr = new Date().toISOString().replace(/[:.]/g, '-')
        saveAs(blob, `consultas_externas_${dateStr}.xlsx`)

    } catch (error) {
        console.error('Error al exportar a Excel:', error)
        importResult.value = {
            success: false,
            message: 'Error al exportar los datos a Excel: ' +
                (error.response?.data?.detail || error.message)
        }

        // Mostrar error detallado en consola para depuración
        if (error.response) {
            console.error('Detalles del error:', error.response.data)
        }
    } finally {
        loading.value = false
    }
}
// Modal
let detalleModal = null
onMounted(() => {
    detalleModal = new Modal(document.getElementById('detalleModal'))
})
// Computed para agrupar errores similares
const erroresPorTipo = computed(() => {
    if (!importResult.value?.detalle_errores) return []

    const errores = importResult.value.detalle_errores
    const resumen = {}

    errores.forEach(error => {
        // Extraer el tipo de error (primera parte del mensaje)
        const tipo = error.split(':')[0] || 'Error desconocido'
        resumen[tipo] = (resumen[tipo] || 0) + 1
    })

    return Object.entries(resumen).map(([message, count]) => ({
        message,
        count
    })).sort((a, b) => b.count - a.count)
})
// Computed para paginación inteligente
const paginasVisibles = computed(() => {
    const current = paginacion.value.current_page
    const total = paginacion.value.total_pages
    const range = 2 // Cuántas páginas mostrar alrededor de la actual
    let start = Math.max(1, current - range)
    let end = Math.min(total, current + range)

    // Ajustar si estamos cerca del inicio o final
    if (current <= range + 1) {
        end = Math.min(2 * range + 1, total)
    }
    if (current >= total - range) {
        start = Math.max(total - 2 * range, 1)
    }

    const pages = []
    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

// Métodos para importación
const handleFileChange = (event) => {
    file.value = event.target.files[0]
    importResult.value = null
}

const resetForm = () => {
    file.value = null
    importResult.value = null
    const fileInput = document.getElementById('excelFile')
    if (fileInput) fileInput.value = ''
}

const uploadFile = async () => {
    if (!file.value) return

    if (file.value.size > 10 * 1024 * 1024) {
        importResult.value = {
            success: false,
            message: 'El archivo es demasiado grande (máximo 10MB permitidos)'
        }
        return
    }

    loading.value = true
    importResult.value = null
    mostrarErrores.value = false

    try {
        const formData = new FormData()
        formData.append('file', file.value)

        // Agrega logs para depuración
        console.log('Enviando archivo:', file.value.name)
        console.log('Tamaño:', file.value.size)

        const response = await api.post('/user/consultas-externas/importar-excel/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        console.log('Respuesta del servidor:', response.data)

        importResult.value = {
            ...response.data,
            success: true
        }

        await cargarRegistros()

    } catch (error) {
        console.error('Error en la importación:', error)
        console.error('Detalles del error:', error.response?.data)

        let errorMessage = 'Error al importar el archivo'
        if (error.response?.data?.error) {
            errorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
            errorMessage = error.response.data.detail
        }

        importResult.value = {
            success: false,
            message: errorMessage,
            detalle_errores: error.response?.data?.detalle_errores || [],
            total_filas: error.response?.data?.total_filas || 0,
            errores: error.response?.data?.errores || 0,
            omitidas: error.response?.data?.omitidas || 0
        }
    } finally {
        loading.value = false
    }
}

// Métodos para listado
const cargarRegistros = async () => {
    try {
        const params = {
            page: paginacion.value.current_page,
            page_size: itemsPorPagina.value,
            search: busqueda.value
        }

        // Agregar filtros de mes y año si están seleccionados
        if (filtroAnio.value) {
            params.year = filtroAnio.value
        }
        if (filtroMes.value) {
            params.month = filtroMes.value
        }

        const response = await api.get('/user/consultas-externas/', { params })
        registros.value = response.data.results
        totalRegistros.value = response.data.count
        paginacion.value = {
            current_page: response.data.current_page,
            total_pages: Math.ceil(response.data.count / itemsPorPagina.value)
        }
    } catch (error) {
        console.error('Error cargando registros:', error)
    }
}

// Debounce para búsqueda
const debounceBuscar = debounce(() => {
    paginacion.value.current_page = 1
    cargarRegistros()
}, 500)

const resetBusqueda = () => {
    busqueda.value = ''
    paginacion.value.current_page = 1
    cargarRegistros()
}

const cambiarPagina = (page) => {
    if (page >= 1 && page <= paginacion.value.total_pages) {
        paginacion.value.current_page = page
        cargarRegistros()
        // Scroll suave hacia arriba
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
}

// Métodos para formato y utilidades
const formatFecha = (fecha) => {
    if (!fecha) return 'N/A'
    return new Date(fecha).toLocaleDateString('es-ES')
}

const formatDateTime = (fecha) => {
    if (!fecha) return 'N/A'
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }
    return new Date(fecha).toLocaleString('es-ES', options)
}

const truncateText = (text, maxLength) => {
    if (!text) return ''
    return text.length > maxLength
        ? text.substring(0, maxLength) + '...'
        : text
}

const verDetalle = (registro) => {
    registroSeleccionado.value = registro
    detalleModal.show()
}

// Cargar datos iniciales
onMounted(async () => {
    await cargarMesesDisponibles()
    cargarRegistros()
})
</script>

<style scoped>
/* Estilos para el acordeón */
.cursor-pointer {
    cursor: pointer;
}

/* Transiciones suaves */
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateY(-10px);
    opacity: 0;
}

/* Estilos existentes */
.spinner-border {
    margin-right: 5px;
}

.table {
    font-size: 0.85rem;
}

.text-danger {
    color: #dc3545;
}

.alert ul {
    margin-bottom: 0;
}

.table-responsive {
    max-height: 500px;
    overflow-y: auto;
}
</style>
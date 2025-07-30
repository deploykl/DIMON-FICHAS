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
                        <div v-if="mostrarEstructura" class="estructura-columnas">
                            <DataTable :value="columnasEstructura" class="p-datatable-sm" :scrollable="true"
                                scrollHeight="flex">
                                <Column field="numero" header="#" headerStyle="width: 5%"></Column>
                                <Column field="nombre" header="Campo"></Column>
                                <Column field="requerido" header="Requerido" headerStyle="width: 10%">
                                    <template #body="{ data }">
                                        <span v-if="data.requerido" class="text-danger">*</span>
                                    </template>
                                </Column>
                                <Column field="recomendacion" header="Recomendaciones"></Column>
                            </DataTable>

                            <div class="recomendaciones mt-2">
                                <h6 class="fw-bold">📌 Recomendaciones importantes:</h6>
                                <ul class="text-muted small">
                                    <li>Las columnas deben estar exactamente en este orden (comenzando desde 0)</li>
                                    <li>Formatos de fecha: DD/MM/YYYY o YYYY-MM-DD</li>
                                    <li>Sexo debe ser 'M' o 'F'</li>
                                    <li>Campos marcados con * son obligatorios</li>
                                </ul>
                            </div>
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

                <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
                    <!-- Botón Importar Datos -->
                    <button class="btn btn-primary d-flex align-items-center" :disabled="!file || loading"
                        @click="uploadFile">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                        <i v-else class="bi bi-upload me-2"></i>
                        {{ loading ? 'Importando...' : 'Importar Datos' }}
                    </button>

                    <!-- Botón Limpiar -->
                    <button class="btn btn-outline-secondary d-flex align-items-center" @click="resetForm"
                        :disabled="loading">
                        <i class="bi bi-trash me-2"></i>
                        Limpiar
                    </button>

                    <!-- Botón Exportar Excel -->
                    <button class="btn btn-success d-flex align-items-center" @click="exportToExcel"
                        :disabled="registros.length === 0 || loading">
                        <i class="bi bi-file-earmark-excel me-2"></i>
                        Exportar Excel
                    </button>
                    <!-- NUEVO BOTÓN: Descargar Plantilla -->
                    <button class="btn btn-info d-flex align-items-center" @click="descargarPlantilla">
                        <i class="bi bi-download me-2"></i>
                        Descargar Plantilla
                    </button>
                    <!-- Filtros -->
                    <div class="d-flex flex-wrap gap-2 align-items-center ms-md-auto">
                        <div class="input-group" style="width: 200px;">
                            <span class="input-group-text bg-white"><i class="bi bi-calendar"></i></span>
                            <select class="form-select" v-model="filtroAnio" @change="cargarRegistros">
                                <option :value="null">Todos los años</option>
                                <option v-for="year in [...new Set(mesesDisponibles.map(item => item.year))]"
                                    :key="year" :value="year">
                                    {{ year }}
                                </option>
                            </select>
                        </div>

                        <div class="input-group" style="width: 150px;">
                            <span class="input-group-text bg-white"><i class="bi bi-filter"></i></span>
                            <select class="form-select" v-model="filtroMes" @change="cargarRegistros"
                                :disabled="!filtroAnio">
                                <option :value="null">Todos</option>
                                <option
                                    v-for="month in mesesDisponibles.filter(item => !filtroAnio || item.year === filtroAnio)"
                                    :key="`${month.year}-${month.month}`" :value="month.month">
                                    {{ getMonthName(month.month) }}
                                </option>
                            </select>
                        </div>

                        <button class="btn btn-outline-danger d-flex align-items-center" @click="resetFiltros"
                            :disabled="!filtroMes && !filtroAnio">
                            <i class="bi bi-x-lg me-1"></i>
                            Filtros
                        </button>
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

                    </div>

                    <DataTable :value="registros" :paginator="true" :rows="itemsPorPagina"
                        :totalRecords="totalRegistros" :loading="loading" :rowsPerPageOptions="[10, 25, 50, 100, 200]"
                        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros"
                        @page="onPageChange" :expandedRows.sync="expandedRows" responsiveLayout="stack" rowHover
                        class="p-datatable-sm">

                        <!-- Columna enumeradora -->
                        <Column header="N°" headerStyle="width: 1rem">
                            <template #body="slotProps">
                                {{ slotProps.index + 1 }}
                            </template>
                        </Column>

                        <Column field="tipo_seguro" header="Tipo Seguro">
                            <template #body="{ data }">
                                {{ data.tipo_seguro || 'N/A' }}
                            </template>
                        </Column>

                        <Column field="fecha_nacimiento" header="Fecha Nacimiento">
                            <template #body="{ data }">
                                {{ formatFecha(data.fecha_nacimiento) }}
                            </template>
                        </Column>
                        <Column field="sexo" header="Sexo">
                            <template #body="{ data }">
                                {{ data.sexo || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="lugar_procedencia" header="Lugar Procedencia">
                            <template #body="{ data }">
                                {{ data.lugar_procedencia || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="n_hcl" header="N° HCL">
                            <template #body="{ data }">
                                {{ data.n_hcl || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="fecha_hora_cita_otorgada" header="Cita Otorgada">
                            <template #body="{ data }">
                                {{ formatDateTime(data.fecha_hora_cita_otorgada) }}
                            </template>
                        </Column>

                        <Column field="fecha_hora_atencion" header="Fecha Atención">
                            <template #body="{ data }">
                                {{ formatDateTime(data.fecha_hora_atencion) }}
                            </template>
                        </Column>

                        <Column field="diagnostico_medico" header="Diagnóstico">
                            <template #body="{ data }">
                                {{ data.diagnostico_medico || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="dx_CIE_10_1" header="dx_CIE_10_1">
                            <template #body="{ data }">
                                {{ data.dx_CIE_10_1 || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="dx_CIE_10_2" header="dx_CIE_10_2">
                            <template #body="{ data }">
                                {{ data.dx_CIE_10_2 || 'N/A' }}
                            </template>
                        </Column>
                        <Column field="dx_CIE_10_3" header="dx_CIE_10_3">
                            <template #body="{ data }">
                                {{ data.dx_CIE_10_3 || 'N/A' }}
                            </template>
                        </Column>

                        <Column field="especialidad" header="Especialidad">
                            <template #body="{ data }">
                                {{ data.especialidad || 'N/A' }}
                            </template>
                        </Column>
                        <template #empty>
                            <div class="text-center py-4">
                                <Message severity="info">
                                    No se encontraron registros. Importe un archivo Excel para comenzar.
                                </Message>
                            </div>
                        </template>
                    </DataTable>

                </div>
            </div>
        </div>

    </main>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { api } from '@/components/services/auth_axios'
import { debounce } from 'lodash'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

const columnasEstructura = ref([
    { numero: 0, nombre: 'Tipo de seguro', requerido: true, recomendacion: 'Ej: SIS, ESSALUD, Privado' },
    { numero: 1, nombre: 'Fecha Nacimiento', requerido: false, recomendacion: 'Formato DD/MM/YYYY' },
    { numero: 2, nombre: 'Sexo (M/F)', requerido: false, recomendacion: 'Solo "M" o "F"' },
    { numero: 3, nombre: 'Lugar de procedencia', requerido: false, recomendacion: 'Ej: Lima, Arequipa' },
    { numero: 4, nombre: 'N° HCL', requerido: false, recomendacion: 'Número de historia clínica' },
    { numero: 5, nombre: 'Fecha y Hora de Cita Otorgada', requerido: true, recomendacion: 'Formato DD/MM/YYYY HH:MM' },
    { numero: 6, nombre: 'Fecha y Hora de atención efectiva', requerido: true, recomendacion: 'Formato DD/MM/YYYY HH:MM' },
    { numero: 7, nombre: 'Diagnóstico Médico', requerido: false, recomendacion: 'Descripción textual' },
    { numero: 8, nombre: 'Dx CIE-10 Principal', requerido: false, recomendacion: 'Código CIE-10' },
    { numero: 9, nombre: 'Dx CIE-10 Secundario', requerido: false, recomendacion: 'Opcional' },
    { numero: 10, nombre: 'Dx CIE-10 Terciario', requerido: false, recomendacion: 'Opcional' },
    { numero: 11, nombre: 'Especialidad', requerido: false, recomendacion: 'Ej: Cardiología, Pediatría' }
]);

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
// Watcher para la búsqueda con debounce
watch(busqueda, (newValue) => {
    if (newValue.trim().length === 0 || newValue.trim().length >= 3) {
        debouncedSearch()
    }
})
// Función de búsqueda debounceada
const debouncedSearch = debounce(() => {
    paginacion.value.current_page = 1
    cargarRegistros()
}, 500)


// Agrega este método para cargar los meses disponibles
const cargarMesesDisponibles = async () => {
    try {
        const response = await api.get('/user/consultas-externas/meses-disponibles/')
        mesesDisponibles.value = response.data

        // Elimina la selección automática del primer mes/año
        filtroAnio.value = null
        filtroAnio.value = null
        filtroMes.value = null
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
            search: busqueda.value.trim()
        }

        // Solo agregar filtros si están seleccionados explícitamente
        if (filtroAnio.value && filtroMes.value) {
            params.year = filtroAnio.value
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

// Método para descargar la plantilla de ejemplo
const descargarPlantilla = () => {
    try {
        // Ruta al archivo en la carpeta public
        const url = '/docs/data_masiva1.xlsx'

        // Crear un enlace temporal
        const link = document.createElement('a')
        link.href = url
        link.download = 'plantilla_consultas_externas.xlsx' // Nombre del archivo al descargar
        link.target = '_blank'

        // Simular click en el enlace
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        // Opcional: Mostrar mensaje de éxito
        importResult.value = {
            success: true,
            message: 'Plantilla descargada correctamente'
        }
    } catch (error) {
        console.error('Error al descargar plantilla:', error)
        importResult.value = {
            success: false,
            message: 'Error al descargar la plantilla'
        }
    }
}
// Cargar datos iniciales
onMounted(async () => {
    await cargarMesesDisponibles()
    cargarRegistros()
})
</script>

<style scoped>
/* Estilos para el acordeón */
.btn-info {
    background-color: #17a2b8;
    border-color: #17a2b8;
    color: white;
}

.btn-info:hover {
    background-color: #138496;
    border-color: #117a8b;
}

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

/* Estilos para botones */
.btn {
    transition: all 0.2s ease;
    font-weight: 500;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn-primary {
    background-color: #4361ee;
    border-color: #4361ee;
}

.btn-primary:hover {
    background-color: #3a56d4;
    border-color: #3a56d4;
}

.btn-success {
    background-color: #2e7d32;
    border-color: #2e7d32;
}

.btn-success:hover {
    background-color: #276a2b;
    border-color: #276a2b;
}

.btn-outline-secondary {
    color: #6c757d;
    border-color: #6c757d;
}

.btn-outline-secondary:hover {
    background-color: #f8f9fa;
    color: #6c757d;
}

.btn-outline-danger {
    color: #dc3545;
    border-color: #dc3545;
}

.btn-outline-danger:hover {
    background-color: #fff0f0;
    color: #dc3545;
}

/* Estilos para íconos en botones */
.bi {
    font-size: 1rem;
}

/* Estilos para selects */
.form-select {
    border-radius: 6px;
    border: 1px solid #ced4da;
    transition: all 0.2s ease;
}

.form-select:focus {
    border-color: #4361ee;
    box-shadow: 0 0 0 0.25rem rgba(67, 97, 238, 0.25);
}

.input-group-text {
    border-radius: 6px 0 0 6px;
    background-color: #f8f9fa;
}

/* Efecto de deshabilitado */
.btn:disabled {
    opacity: 0.65;
    transform: none !important;
    box-shadow: none !important;
}
</style>
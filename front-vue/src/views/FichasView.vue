<template>
    <main class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Seleccionar Ficha de Evaluación</h1>
            <router-link to="/fichas" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-left me-2"></i> Volver
            </router-link>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-2">Cargando fichas disponibles...</p>
        </div>

        <div v-else class="row">
            <div v-for="category in categorias" :key="category.id" class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-header" :class="getCategoryColor(category)">
                        <h2 class="h5 mb-0 text-white">{{ category.name }}</h2>
                        <small class="text-white-50">{{ category.tipo }}</small>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <router-link v-for="proceso in getProcesosByCategory(category.id)" :key="proceso.id"
                                :to="{ name: 'evaluar-ficha', params: { id: proceso.id } }"
                                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                <div>
                                    <h3 class="h6 mb-1">{{ proceso.nombre }}</h3>
                                    <small class="text-muted">{{ proceso.nombre_proceso }}</small>
                                </div>
                                <i class="fas fa-chevron-right text-muted"></i>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <FloatingChat />

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '@/components/services/auth_axios';
import FloatingChat from '@/components/widgets/GeminiChatbot.vue';
const categorias = ref([]);
const procesos = ref([]);
const loading = ref(true);
const error = ref(null);

// Obtener color según categoría
const getCategoryColor = (category) => {
    const colors = [
        'bg-primary', 'bg-success', 'bg-info',
        'bg-warning', 'bg-danger', 'bg-secondary'
    ];
    const index = category.id % colors.length;
    return colors[index];
};

// Filtrar procesos por categoría
const getProcesosByCategory = (categoryId) => {
    return procesos.value.filter(p => p.categoria === categoryId);
};

// Cargar datos al montar el componente
onMounted(async () => {
    try {
        const [catResponse, procResponse] = await Promise.all([
            api.get('ficha/categoria/'),
            api.get('ficha/proceso/')
        ]);

        categorias.value = catResponse.data;
        procesos.value = procResponse.data;

        // Ordenar categorías
        categorias.value.sort((a, b) => a.name.localeCompare(b.name));
    } catch (err) {
        error.value = 'Error al cargar las fichas disponibles';
        console.error('Error:', err);
    } finally {
        loading.value = false;
    }
});
</script>

<style scoped>
.card {
    transition: all 0.3s ease;
    border: none;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
    border-bottom: none;
}

.list-group-item {
    border-left: none;
    border-right: none;
    padding: 1rem 1.25rem;
    transition: all 0.2s ease;
}

.list-group-item:hover {
    background-color: #f8f9fa;
}

.list-group-item h3 {
    transition: all 0.2s ease;
}

.list-group-item:hover h3 {
    color: #0d6efd;
}
</style>
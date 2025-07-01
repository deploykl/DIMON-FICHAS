<template>
    <div class="password-reset-container">
        <div class="login-wrapper">
            <div class="login-card">
                <div class="header">
                    <img src="@/assets/img/logo1.png" alt="Logo" class="logo">
                    <h2>Recuperar Contraseña</h2>
                </div>

                <form @submit.prevent="submitRequest">
                    <div class="form-group">
                        <label for="email">Correo Electrónico</label>
                        <input type="email" id="email" v-model="email" required
                            placeholder="Ingresa tu correo registrado" class="form-input">
                    </div>

                    <button type="submit" :disabled="loading" class="submit-btn">
                        <span v-if="loading">
                            <i class="bi bi-arrow-repeat rotate"></i> Enviando...
                        </span>
                        <span v-else>
                            <i class="bi bi-send-fill"></i> Enviar enlace
                        </span>
                    </button>

                    <p v-if="message" class="message" :class="{ 'error-message': isError }">
                        <i :class="messageIcon"></i> {{ message }}
                    </p>

                    <!-- Solo para desarrollo: muestra el enlace en pantalla -->
                    <div v-if="isDevelopment && resetLink" class="dev-info">
                        <h4><i class="bi bi-code-slash"></i> Modo Desarrollo</h4>
                        <p>En producción, esto se enviaría por correo a <strong>{{ email }}</strong></p>
                        <div class="link-container">
                            <a :href="resetLink" target="_blank" class="reset-link">
                                <i class="bi bi-link-45deg"></i> {{ resetLink }}
                            </a>
                            <button @click="copyLink" class="copy-btn" :title="copyTooltip">
                                <i class="bi" :class="copyIcon"></i>
                            </button>
                        </div>
                    </div>
                </form>

                <div class="footer-links">
                    <router-link to="/login" class="back-link">
                        <i class="bi bi-arrow-left"></i> Volver al inicio de sesión
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios'

const email = ref('')
const loading = ref(false)
const message = ref('')
const resetLink = ref('')
const copyTooltip = ref('Copiar enlace')
const copyIcon = ref('bi-clipboard')
const isDevelopment = ref(false)
const router = useRouter()

onMounted(() => {
    // Verificar si estamos en desarrollo
    isDevelopment.value = process.env.NODE_ENV === 'development'
})

const isError = computed(() => {
    return message.value.toLowerCase().includes('error') ||
        message.value.toLowerCase().includes('invalido') ||
        message.value.toLowerCase().includes('incorrecto')
})

const messageIcon = computed(() => {
    return isError.value ? 'bi-exclamation-circle-fill' : 'bi-check-circle-fill'
})

const copyLink = () => {
    navigator.clipboard.writeText(resetLink.value)
    copyTooltip.value = '¡Copiado!'
    copyIcon.value = 'bi-check2'
    setTimeout(() => {
        copyTooltip.value = 'Copiar enlace'
        copyIcon.value = 'bi-clipboard'
    }, 2000)
}

const submitRequest = async () => {
    if (!email.value) {
        message.value = 'Por favor ingresa tu correo electrónico'
        return
    }

    loading.value = true
    message.value = ''

    try {
        const response = await api.post('user/password/reset/', {
            email: email.value
        })

        message.value = response.data.detail

        // Solo en desarrollo, muestra el enlace simulado
        if (isDevelopment.value) {
            resetLink.value = `http://localhost:8080/reset-password?token=simulated-token-${Math.random().toString(36).substring(2, 15)}`
        }

        setTimeout(() => {
            if (!isError.value) {
                router.push('/login')
            }
        }, 3000)
    } catch (error) {
        message.value = error.response?.data?.detail || 'Ocurrió un error al procesar tu solicitud'
        console.error('Error:', error)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
/* Nuevos estilos agregados para el contenedor */
.password-reset-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-wrapper {
    width: 100%;
    max-width: 450px;
    padding: 0 20px;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 40px;
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Estilos existentes del formulario (mantener los que ya tienes) */
.header {
    background: #ffffff;
    text-align: center;
    margin-bottom: 2rem;
}

.logo {
    height: 50px;
    margin-bottom: 1rem;
}

h2 {
    color: #0b4a7a;
    margin-bottom: 1.5rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-input:focus {
    border-color: #0b4a7a;
    outline: none;
    box-shadow: 0 0 0 3px rgba(11, 74, 122, 0.1);
}

.submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #0b4a7a;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.submit-btn:hover {
    background-color: #083758;
}

.submit-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.rotate {
    animation: rotate 1s linear infinite;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.message {
    margin-top: 1.5rem;
    padding: 12px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.message i {
    font-size: 1.2rem;
}

.message:not(.error-message) {
    background-color: #e8f5e9;
    color: #2e7d32;
}

.error-message {
    background-color: #ffebee;
    color: #c62828;
}

.dev-info {
    margin-top: 2rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 6px;
    border-left: 4px solid #0b4a7a;
}

.dev-info h4 {
    color: #0b4a7a;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.link-container {
    display: flex;
    align-items: center;
    margin-top: 1rem;
    background: white;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.reset-link {
    flex-grow: 1;
    color: #0b4a7a;
    word-break: break-all;
    display: flex;
    align-items: center;
    gap: 5px;
}

.copy-btn {
    background: none;
    border: none;
    color: #0b4a7a;
    cursor: pointer;
    padding: 5px;
    margin-left: 10px;
    font-size: 1.2rem;
}

.copy-btn:hover {
    color: #083758;
}

.footer-links {
    margin-top: 2rem;
    text-align: center;
}

.back-link {
    color: #0b4a7a;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: color 0.3s;
}

.back-link:hover {
    color: #083758;
    text-decoration: underline;
}

@media (max-width: 480px) {
    .login-card {
        padding: 1.5rem;
    }
}
</style>
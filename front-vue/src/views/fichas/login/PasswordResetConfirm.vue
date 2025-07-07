<template>
    <div class="password-reset-container">
        <div class="login-wrapper">
            <div class="login-card">
                <div class="header">
                    <img src="@/assets/img/logo1.png" alt="Logo" class="logo">
                    <h2>Restablecer Contraseña</h2>
                </div>

                <form @submit.prevent="submitReset">
                    <div v-if="tokenInvalid" class="error-message">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>El enlace de recuperación no es válido o ha expirado</p>
                        <router-link to="/password-reset" class="back-link">
                            <i class="fas fa-redo"></i> Solicitar nuevo enlace
                        </router-link>
                    </div>

                    <div v-else>
                        <div class="form-group">
                            <label for="password">Nueva Contraseña</label>
                            <div class="input-group">
                                <div class="input-icon">
                                    <i class="fas fa-lock"></i>
                                </div>
                                <input 
                                    id="password" 
                                    v-model="password" 
                                    required
                                    placeholder="Mínimo 8 caracteres" 
                                    class="input-field"
                                    :type="showPassword ? 'text' : 'password'"
                                >
                                <div class="password-toggle" @click="showPassword = !showPassword">
                                    <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="password2">Confirmar Contraseña</label>
                            <div class="input-group">
                                <div class="input-icon">
                                    <i class="fas fa-lock"></i>
                                </div>
                                <input 
                                    id="password2" 
                                    v-model="password2" 
                                    required
                                    placeholder="Repite tu nueva contraseña" 
                                    class="input-field"
                                    :type="showConfirmPassword ? 'text' : 'password'"
                                >
                                <div class="password-toggle" @click="showConfirmPassword = !showConfirmPassword">
                                    <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                                </div>
                            </div>
                        </div>

                        <button type="submit" :disabled="loading" class="submit-btn">
                            <span v-if="loading">
                                <i class="fas fa-circle-notch fa-spin"></i> Procesando...
                            </span>
                            <span v-else>
                                <i class="fas fa-key"></i> Restablecer contraseña
                            </span>
                        </button>

                        <p v-if="message" class="message" :class="{ 'error-message': isError }">
                            <i :class="isError ? 'fas fa-exclamation-circle' : 'fas fa-check-circle'"></i> {{ message }}
                        </p>
                    </div>
                </form>

                <div class="footer-links">
                    <router-link to="/login" class="back-link">
                        <i class="fas fa-arrow-left"></i> Volver al inicio de sesión
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api } from '@/components/services/auth_axios'

const route = useRoute()
const router = useRouter()
const token = ref(route.query.token || '')
const password = ref('')
const password2 = ref('')
const loading = ref(false)
const message = ref('')
const tokenInvalid = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const isError = computed(() => {
    return message.value.toLowerCase().includes('error') ||
        message.value.toLowerCase().includes('invalido') ||
        message.value.toLowerCase().includes('incorrecto')
})

onMounted(() => {
    if (!token.value) {
        tokenInvalid.value = true
    }
})

const submitReset = async () => {
    if (password.value !== password2.value) {
        message.value = 'Las contraseñas no coinciden'
        return
    }

    if (password.value.length < 8) {
        message.value = 'La contraseña debe tener al menos 8 caracteres'
        return
    }

    loading.value = true
    message.value = ''

    try {
        const response = await api.post('user/password/reset/confirm/', {
            token: token.value,
            password: password.value,
            password2: password2.value
        })

        message.value = response.data.detail

        setTimeout(() => {
            router.push('/login')
        }, 2000)
    } catch (error) {
        if (error.response?.status === 400) {
            tokenInvalid.value = true
        }
        message.value = error.response?.data?.detail || 'Ocurrió un error al restablecer la contraseña'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
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

.header {
    text-align: center;
    margin-bottom: 2rem;
    background: #fff;
}

.logo {
    height: 50px;
    margin-bottom: 1rem;
}

h2 {
    color: #0b4a7a;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.input-group {
    position: relative;
    margin-bottom: 1.5rem;
}

.input-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #143168;
    font-size: 1rem;
}

.input-field {
    width: 100%;
    padding: 12px 15px 12px 45px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s;
    background-color: rgba(255, 255, 255, 0.9);
}

.input-field:focus {
    border-color: #0b4a7a;
    outline: none;
    box-shadow: 0 0 0 3px rgba(11, 74, 122, 0.2);
}

.password-toggle {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #757575;
    cursor: pointer;
    font-size: 1.2rem;
    transition: color 0.3s;
}

.password-toggle:hover {
    color: #0b4a7a;
}

.submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #0b4a7a;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: 1rem;
}

.submit-btn:hover {
    background-color: #083758;
}

.submit-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.fa-spin {
    animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.message {
    margin-top: 1.5rem;
    padding: 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
}

.message i {
    font-size: 1rem;
}

.message:not(.error-message) {
    background-color: #e8f5e9;
    color: #2e7d32;
}

.error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    text-align: center;
}

.error-message i {
    font-size: 1.5rem;
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
    font-size: 0.9rem;
}

.back-link:hover {
    color: #083758;
    text-decoration: underline;
}

@media (max-width: 480px) {
    .login-card {
        padding: 1.5rem;
    }
    
    h2 {
        font-size: 1.3rem;
    }
    
    .input-field {
        padding: 10px 12px 10px 40px;
    }
}
</style>
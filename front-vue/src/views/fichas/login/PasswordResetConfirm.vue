<template>
  <div class="password-reset-confirm-container">
    <div class="header">
      <img src="@/assets/img/logo1.png" alt="Logo" class="logo">
      <h2>Restablecer Contraseña</h2>
    </div>
    
    <form @submit.prevent="submitReset" class="reset-form">
      <div v-if="tokenInvalid" class="token-error">
        <i class="bi bi-exclamation-triangle"></i>
        <p>El enlace de recuperación no es válido o ha expirado</p>
        <router-link to="/password-reset" class="request-new-link">
          Solicitar nuevo enlace
        </router-link>
      </div>
      
      <div v-else>
        <div class="form-group">
          <label for="password">Nueva Contraseña</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            placeholder="Mínimo 8 caracteres"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
          <label for="password2">Confirmar Contraseña</label>
          <input 
            type="password" 
            id="password2" 
            v-model="password2" 
            required
            placeholder="Repite tu nueva contraseña"
            class="form-input"
          >
        </div>
        
        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="loading">
            <i class="bi bi-arrow-repeat rotate"></i> Procesando...
          </span>
          <span v-else>
            <i class="bi bi-shield-lock"></i> Restablecer contraseña
          </span>
        </button>
        
        <p v-if="message" class="message" :class="{ 'error': isError }">
          <i :class="messageIcon"></i> {{ message }}
        </p>
      </div>
    </form>
    
    <div class="footer-links">
      <router-link to="/login" class="back-link">
        <i class="bi bi-arrow-left"></i> Volver al inicio de sesión
      </router-link>
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

const isError = computed(() => {
  return message.value.toLowerCase().includes('error') || 
         message.value.toLowerCase().includes('invalido') ||
         message.value.toLowerCase().includes('incorrecto')
})

const messageIcon = computed(() => {
  return isError.value ? 'bi-exclamation-circle-fill' : 'bi-check-circle-fill'
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
.password-reset-confirm-container {
  max-width: 450px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header {
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
  text-align: center;
}

.reset-form {
  margin-top: 1.5rem;
}

.token-error {
  background-color: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 6px;
  text-align: center;
}

.token-error i {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}

.request-new-link {
  display: inline-block;
  margin-top: 1rem;
  color: #0b4a7a;
  font-weight: 500;
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
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

.message:not(.error) {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.message.error {
  background-color: #ffebee;
  color: #c62828;
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
  .password-reset-confirm-container {
    margin: 1rem;
    padding: 1.5rem;
  }
}
</style>
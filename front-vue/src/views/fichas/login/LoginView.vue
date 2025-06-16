<template>
  <div class="login-container">
    <div class="login-wrapper">
      <div class="login-card">
        <!-- Logo superior -->
        <div class="logo-container">
          <img src="@/assets/img/login/logo.png" alt="Logo" class="logo-img" />
        </div>

        <!-- Mensaje de error con animación -->
        <transition name="fade">
          <div v-if="errorMessage" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ errorMessage }}
          </div>
        </transition>

        <!-- Formulario -->
        <form @submit.prevent="handleSubmit" class="login-form">
          <!-- Campo Usuario -->
          <div class="input-group">
            <div class="input-icon">
              <i class="fas fa-user"></i>
            </div>
            <input
              type="text"
              id="username"
              v-model="username"
              @input="handleLowerCASE"
              class="input-field"
              placeholder="Nombre de usuario"
              required
            />
          </div>

          <!-- Campo Contraseña con toggle -->
          <div class="input-group">
            <div class="input-icon">
              <i class="fas fa-lock"></i>
            </div>
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              class="input-field"
              placeholder="Contraseña"
              required
            />
            <div class="password-toggle" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </div>
          </div>

          <!-- Botón de Login con efecto hover -->
          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>
              <i class="fas fa-sign-in-alt"></i> Ingresar
            </span>
          </button>
        </form>

        <!-- Footer -->
        <div class="login-footer">
          <span>OBS Salud V.1</span>
          <div class="footer-decoration"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios';

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const showPassword = ref(false)
const router = useRouter()

const handleLowerCASE = (event) => {
  const targetField = event.target.id;
  if (targetField === 'username') {
    username.value = event.target.value.toLowerCase();
  }
};

const handleSubmit = async () => {
  errorMessage.value = '';
  isLoading.value = true;

  try {
    const response = await api.post('user/login/', {
      username: username.value,
      password: password.value,
    });

    const { access, refresh, is_superuser, is_staff } = response.data;

    if (!access) {
      errorMessage.value = 'No se recibió token de acceso.';
      return;
    }

    localStorage.setItem('auth_token', access);
    if (refresh) localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('is_superuser', is_superuser ? 'true' : 'false');
    localStorage.setItem('is_staff', is_staff ? 'true' : 'false');

    router.push('/about');
    
  } catch (error) {
    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail;
    } else {
      errorMessage.value = 'Error al conectar con el servidor. Por favor intente nuevamente.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Estilos base */
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
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
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Logo */
.logo-container {
  text-align: center;
  margin-bottom: 30px;
}

.logo-img {
  max-width: 180px;
  height: auto;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Mensaje de error */
.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  border-left: 4px solid #c62828;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Campos de entrada */
.input-group {
  position: relative;
  margin-bottom: 20px;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #6e45e2;
  font-size: 18px;
}

.input-field {
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s;
  background-color: rgba(255, 255, 255, 0.8);
}

.input-field:focus {
  border-color: #6e45e2;
  box-shadow: 0 0 0 3px rgba(110, 69, 226, 0.2);
  outline: none;
}

.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #757575;
  cursor: pointer;
  font-size: 18px;
  transition: color 0.3s;
}

.password-toggle:hover {
  color: #6e45e2;
}

/* Botón de login */
.login-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(to right, #6e45e2, #88d3ce);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(110, 69, 226, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(110, 69, 226, 0.4);
}

.login-btn:disabled {
  background: #bdbdbd;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer */
.login-footer {
  margin-top: 30px;
  text-align: center;
  color: #757575;
  font-size: 12px;
  position: relative;
}

.footer-decoration {
  height: 4px;
  background: linear-gradient(to right, #6e45e2, #88d3ce);
  border-radius: 2px;
  margin-top: 8px;
  width: 50%;
  margin-left: auto;
  margin-right: auto;
}
</style>
<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="register-box">

      <div class="card shadow-sm">
        <div class="card-body register-card-body">
          <p class="register-box-msg text-center mb-4">Regístrate con tus credenciales</p>

          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="username">Nombre de usuario</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">
                    <i class="fas fa-user"></i>
                  </span>
                </div>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  class="form-control"
                  placeholder="Nombre de usuario"
                  required
                />
              </div>
              <div v-if="errorMessages.username" class="text-danger">{{ errorMessages.username }}</div>
            </div>

            <div class="form-group">
              <label for="email">Correo electrónico</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">
                    <i class="fas fa-envelope"></i>
                  </span>
                </div>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="form-control"
                  placeholder="Correo electrónico"
                  required
                />
              </div>
              <div v-if="errorMessages.email" class="text-danger">{{ errorMessages.email }}</div>
            </div>

            <div class="form-group">
              <label for="password">Contraseña</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">
                    <i class="fas fa-lock"></i>
                  </span>
                </div>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  class="form-control"
                  placeholder="Contraseña"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password2">Confirmar Contraseña</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">
                    <i class="fas fa-lock"></i>
                  </span>
                </div>
                <input
                  type="password"
                  id="password2"
                  v-model="password2"
                  class="form-control"
                  placeholder="Confirmar Contraseña"
                  required
                />
              </div>
              <div v-if="errorMessages.password2" class="text-danger">{{ errorMessages.password2 }}</div>
            </div>

            <hr />

            <div class="form-group">
              <button type="submit" class="btn btn-primary btn-block">
                <i class="fas fa-user-plus"></i> Registrarse
              </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger mt-3">
              {{ errorMessage }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const errorMessage = ref('')
const errorMessages = ref({})
const router = useRouter()

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/user/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value
    })
    console.log('Registro exitoso', response.data) // Para depuración
    console.log('Redirigiendo a la página de login...');

    // Redirigir al usuario a la página de login
    router.push({ name: 'login' }); // Utiliza el nombre de la ruta
  } catch (error) {
    console.error('Error en el registro:', error) // Para depuración

    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.non_field_errors || 'Error al registrar usuario. Por favor intente de nuevo.'
      errorMessages.value = error.response.data
    } else {
      errorMessage.value = 'Error de red. Por favor intente de nuevo.'
    }
  }
}
</script>

<style>
/* Agrega tus estilos aquí */
</style>

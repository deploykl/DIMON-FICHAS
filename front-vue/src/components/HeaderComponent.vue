<template>
  <header id="header" class="header fixed-top">
    <div class="container-fluid d-flex align-items-center justify-content-between">
      <!-- Logo Section -->
      <div class="d-flex align-items-center">
        <a href="#" class="logo d-flex align-items-center">
          <img :src="require('@/assets/img/logo1.png')" alt="logo" class="logo-img">
          <span class="logo-text">OBS-Salud</span>
        </a>
      </div>

      <!-- Navigation -->
      <nav class="header-nav ms-auto">
        <ul class="d-flex align-items-center gap-3">
          <!-- Clock Component -->
          <li class="nav-item">
            <clock-component-vue />
          </li>

          <!-- User Profile -->
          <li class="nav-item dropdown">
            <a class="nav-profile d-flex align-items-center" href="#" @click="toggleDropdown">
              <div class="avatar-container">
                <img :src="userImage" alt="Profile" class="avatar-img">
              </div>
              <span class="user-name">{{ userName }} {{ userLastName }}</span>
            </a>
          </li>

          <!-- Logout Button -->
          <li class="nav-item">
            <button class="logout-btn" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              <span class="logout-text">Salir</span>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
import ClockComponentVue from '../components/widgets/ClockComponent.vue';

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api, getAuthToken } from '@/components/services/auth_axios';

const userName = ref('');
const userLastName = ref('');
const userImage = ref('');
const router = useRouter();
const imgServerURL = process.env.VUE_APP_IMG_SERVER;
const imgLocalURL = process.env.VUE_APP_IMG_LOCAL;

const fetchUserProfile = async () => {
  const accessToken = localStorage.getItem('auth_token');
  if (accessToken) {
    try {
      const response = await api.get('user/profile/', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      userName.value = response.data.first_name || '';
      userLastName.value = response.data.last_name || '';
      
      // Manejo seguro de la imagen
      if (response.data.image) {
        // Si la imagen ya incluye la ruta completa
        if (response.data.image.startsWith('http')) {
          userImage.value = response.data.image;
        } else {
          // Si es una ruta relativa
          userImage.value = joinUrl(imgServerURL, response.data.image);
        }
      } else {
        // Imagen por defecto
        userImage.value = joinUrl(imgServerURL, 'img/empty.png');
      }
    } catch (error) {
      console.error('Error al obtener el perfil:', error);
      // Imagen por defecto en caso de error
      userImage.value = joinUrl(imgServerURL, 'img/empty.png');
    }
  } else {
    // Imagen por defecto si no hay token
    userImage.value = joinUrl(imgServerURL, 'img/empty.png');
  }
};

function joinUrl(base, path) {
  // Elimina barras finales del base y barras iniciales del path
  const cleanBase = base.replace(/\/+$/, '');
  const cleanPath = path.replace(/^\/+/, '');
  
  // Si el path ya incluye 'media', no lo dupliques
  if (cleanPath.startsWith('media/') || cleanPath.startsWith('/media/')) {
    return `${cleanBase}/${cleanPath}`;
  }
  
  // Construye la URL final
  return `${cleanBase}/media/${cleanPath}`;
}

onMounted(() => {
  fetchUserProfile();
});

const logout = async () => {
  const refreshToken = localStorage.getItem('refreshToken');

  if (!refreshToken) {
    console.error('No se encontró el token de refresco.');
    return;
  }

  try {
    console.log('Token de refresco enviado para blacklist:', refreshToken);

    const response = await api.post('user/logout/', {
      refresh: refreshToken,
    });

    if (response.status === 205) {
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_name');
      localStorage.removeItem('user_lastname');
      router.push('/');
    }
  } catch (error) {
    console.error('Error al cerrar sesión:', error);
  }
};

</script>


<style scoped>
/* Base Styles */
.header {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  height: 70px;
  padding: 0 2rem;
  transition: all 0.3s ease;
  z-index: 1000;
}

.container-fluid {
  height: 100%;
}

/* Logo Styles */
.logo {
  text-decoration: none;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.03);
}

/* Agrega esto al inicio de tus estilos para resetear las listas */
.header-nav ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

.header-nav li {
  list-style: none;
  display: inline-block;
  /* o flex, según necesites */
}

.logo-img {
  height: 40px;
  width: auto;
  object-fit: contain;
}

.logo-text {
  color: white;
  font-size: 1.3rem;
  font-weight: 600;
  margin-left: 10px;
  letter-spacing: 0.5px;
}

/* Toggle Button */
.toggle-sidebar-btn {
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-sidebar-btn:hover {
  color: #f8f9fa;
  transform: scale(1.1);
}

/* User Profile */
.nav-profile {
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

.nav-profile:hover {
  background: rgba(255, 255, 255, 0.15);
}

.avatar-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  margin-left: 10px;
  font-weight: 500;
}

/* Logout Button */
.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.logout-btn:hover {
  background: rgba(231, 76, 60, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Clock Component */
.clock-container {
  color: white;
  font-weight: 500;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50px;
}

/* Estilos existentes... */

/* Ajustes para móvil */
@media (max-width: 768px) {
  .header {
    padding: 0 0.5rem;
  }

  .logo-text {
    font-size: 1rem;
    margin-left: 5px;
  }

  .user-name {
    font-size: 0.8rem;
    margin-left: 5px;
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .logout-text {
    display: none;
  }

  .logout-btn i {
    font-size: 1.2rem;
  }

  .avatar-container {
    width: 32px;
    height: 32px;
  }

  /* Asegúrate que el reloj sea legible */
  .clock-container {
    font-size: 0.8rem;
    padding: 0.3rem 0.5rem;
  }
}
</style>
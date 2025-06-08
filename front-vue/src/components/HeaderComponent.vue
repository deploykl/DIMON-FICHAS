<template>
  <header id="header" class="header fixed-top d-flex align-items-center">
    <div class="d-flex align-items-center justify-content-between">
      <a href="#" class="logo d-flex align-items-center">
        <img :src="require('@/assets/img/logo1.png')" alt="logo">
        <span class="d-none d-lg-block">H-Gestión</span>
      </a>
      <i class="fas fa-bars toggle-sidebar-btn" @click="$emit('toggleAside')"></i>
    </div><!-- End Logo -->

    <!-- 
    <div class="search-bar">
      <form class="search-form d-flex align-items-center" method="POST" action="#">
        <input type="text" name="query" placeholder="Search" title="Enter search keyword">
        <button type="submit" title="Search"><i class="bi bi-search"></i></button>
      </form>
    </div>
    -->

    <nav class="header-nav ms-auto">
      <ul class="d-flex align-items-center">
        <li class="nav-item d-block d-lg-none">
          <a class="nav-link nav-icon search-bar-toggle" href="#">
            <i class="bi bi-search"></i>
          </a>
        </li><!-- End Search Icon -->
        <li class="nav-item me-4">
          <clock-component-vue />
        </li>
       <!-- End Notification Nav -->
        <li class="nav-item dropdown pe-3">
          <a class="nav-link nav-profile d-flex align-items-center pe-0" href="#" @click="toggleDropdown"
            data-bs-toggle="">
            <img :src="userImage" alt="Profile Picture" class="img-fluid rounded-circle">
            <span class="d-none d-md-block  ps-2">{{ userName }} {{ userLastName }}</span>
          </a><!-- End Profile Image Icon -->
          <!-- End ProfiLe Dropdown Items -->
        </li><!-- End Profile Nav -->
        <li class="nav-item dropdown pe-3">
          <a class="btn btn-danger w-100" @click="logout">
            <i class="fa-solid fa-right-from-bracket"></i>
            <span> Salir</span>
          </a class><!-- End Profile Image Icon -->
          <!-- End Profie Dropdown Items -->
        </li>
        <!-- End Dependency Display -->
      </ul>
    </nav><!-- End Icons Navigation -->
  </header><!-- End Header -->
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
      //userImage.value = response.data.image ? `http://127.0.0.1:8000${response.data.image}` : 'http://127.0.0.1:8000/media/img/empty.png';
      userImage.value = response.data.image ? `${imgServerURL}${response.data.image}` : `${imgServerURL}media/img/empty.png`;
    } catch (error) {
      console.error('Error al obtener el perfil:', error);
    }
  }
};

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
a {
  cursor: pointer;
}

button i {
  background-color: rgb(255, 255, 255) !important;
}
</style>

<template>
  <div class="clock-container">
    <span class="clock-icon"><i class="far fa-clock"></i></span>
    <span class="time">{{ time }}</span>
  </div>
</template>


<script>
export default {
  data() {
    return {
      time: this.getCurrentTime(),
      timer: null,
    };
  },
  methods: {
    getCurrentTime() {
      const now = new Date();
      // Formatea la hora en formato 12 horas con AM/PM
      const time = now.toLocaleTimeString('es-PE', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
      });

      // Formatea la fecha en el formato "10 de ago."
      const options = { day: 'numeric', month: 'short' };
      const date = now.toLocaleDateString('es-PE', options).replace('.', ''); // Quita el punto del mes

      return `${date},  ${time}`;
    },
    updateClock() {
      this.time = this.getCurrentTime();
    },
  },
  mounted() {
    // Actualiza el reloj cada segundo
    this.timer = setInterval(this.updateClock, 1000);
  },
  beforeDestroy() {
    // Limpia el intervalo cuando el componente se destruye
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.clock-container {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: white;
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  height: 40px;
}

.clock-icon {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.time {
  letter-spacing: 0.3px;
}

/* Efecto hover para consistencia con el header */
.clock-container:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Responsive para móviles */
@media (max-width: 768px) {
  .clock-container {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .time {
    display: none; /* Oculta el texto en móviles si es necesario */
  }
}
</style>

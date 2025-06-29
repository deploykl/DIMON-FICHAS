<template>
    <footer class="footer-container">
        <div class="footer-content">
            <div class="footer-text">
                <p class="footer-disclaimer">
                    Resolución de Secretaría de Gestión Pública N° 002-2025-PCM - SGP del 23.02.2025 que aprueba la Norma Técnica
                    N° 002-2025-PCM/SGP, Norma Técnica para la Gestión por procesos en las entidades de la Administración Pública
                    y que deja sin efecto la RSGP N° 006-2018-PCM-SGP que aprueba la NT N° 001-2018-PCM/SGP
                </p>
            </div>
            <div class="footer-info">
                <div class="footer-copyright">
                    <p class="m-0">&copy; Sistema  de Monitoreo v.1.0</p>
                    <p class="m-0">Desarrollado por el área de TI de la DGOS-DIMON</p>
                </div>
                <div class="footer-contact">
                    <p class="m-0"><i class="fas fa-phone-alt"></i> (511) 3156600 Anexo 5112</p>
                    <p class="m-0"><i class="fas fa-envelope"></i> bot.reporte.dimon@gmail.com</p>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
</script>

<style scoped>
.footer-container {
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 2rem 1rem;
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    border-top: 4px solid #3498db;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
}

.footer-disclaimer {
    font-size: 0.8rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
    text-align: center;
    opacity: 0.8;
}

.footer-info {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-copyright {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.footer-contact {
    text-align: right;
    font-size: 0.9rem;
}

.footer-contact i {
    margin-right: 8px;
    color: #3498db;
}

@media (max-width: 768px) {
    .footer-info {
        flex-direction: column;
        text-align: center;
    }
    
    .footer-contact {
        text-align: center;
        margin-top: 1rem;
    }
    
    .footer-disclaimer {
        font-size: 0.7rem;
    }
}

/* Efectos hover para elementos interactivos */
.footer-contact p:hover {
    color: #3498db;
    transition: color 0.3s ease;
}

/* Animación sutil al cargar */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.footer-container {
    animation: fadeIn 0.5s ease-out forwards;
}
</style>
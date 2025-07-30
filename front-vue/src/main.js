import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Aura from '@primeuix/themes/aura';
import Tooltip from 'primevue/tooltip';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import OverlayBadge from 'primevue/overlaybadge';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';

// LIBRERÍAS
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';  // Asegúrate de esta línea
import 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';


import '@/assets/lib/fontawesome-v6.5.2/css/all.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-light.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-regular.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-solid.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-thin.css'

import 'primeicons/primeicons.css'

//PERSONALIZADO
import '@/assets/css/font.css'
import '@/assets/css/main.css'

const app = createApp(App)

// Configure and use PrimeVue once
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'false',
            cssLayer: false
        }
    }
});
// Use other plugins
app.use(store)
app.use(router)

// Registra componentes globales
app.component('FloatLabel', FloatLabel)
app.component('InputText', InputText)
app.directive('tooltip', Tooltip);
app.component('Dialog', Dialog);
app.component('Button', Button);
app.component('Badge', Badge);
app.component('OverlayBadge', OverlayBadge);
app.component('Message', Message);
app.component('ProgressSpinner', ProgressSpinner);

// Monta la aplicación
app.mount('#app')

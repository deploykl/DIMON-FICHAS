import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FichasView from "../views/FichasView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import LoginView from "../views/fichas/login/LoginView.vue";
import PasswordResetRequest from '@/views/fichas/login/PasswordResetRequest.vue'
import PasswordResetConfirm from '@/views/fichas/login/PasswordResetConfirm.vue'
import EvaluarFichaView from "../views/EvaluarFichaView.vue";
import MatrizCompromisoView from "../views/MatrizCompromisoView.vue";
import UrlsView from "../views/menu/UrlsView.vue";
import AlertasView from "../views/AlertasView.vue";
import GameView from "../views/etc/GameView.vue";
import SeguimientoMatrizView from "../views/SeguimientoMatriz.vue";
import BoletinView from "../views/BoletinView.vue";
import BoletinView_List from "../views/BoletinView_List.vue";

const routes = [
  {
    path: "/",
    name: "HOME",
    component: HomeView,
    meta: {
      title: "DIMON APP",
    },
  },
  {
    path: "/matriz-list",
    name: "matriz-list",
    component: SeguimientoMatrizView,
    meta: {
      title: "DIMON APP",
    },
  },
  {
    path: "/fichas",
    name: "FICHAS",
    component: FichasView,
    meta: {
      title: "FICHAS",
      requiresAuth: true,
    },
  },
  {
    path: "/fichas/evaluar/:id",
    name: "evaluar-ficha",
    component: EvaluarFichaView,
    props: true,
    meta: {
      title: "Evaluar Ficha",
      requiresAuth: true,
    },
  },
  {
    path: "/matriz-compromiso/matriz/:id",
    name: "matriz-compromiso",
    component: MatrizCompromisoView,
    props: true,
    meta: {
      title: "Matriz de Compromiso",
      requiresAuth: true,
    },
  },
  {
    path: "/alertas",
    name: "ALERTAS",
    component: AlertasView,
    meta: {
      title: "ALERTAS",
      requiresAuth: true,
    },
  },
  {
    path: "/urls",
    name: "enlaces",
    component: UrlsView,
    props: true,
    meta: {
      title: "Enlaces de información",
      requiresAuth: true,
    },
  },
    {
    path: "/game",
    name: "game",
    component: GameView,
    props: true,
    meta: {
      title: "GAME",
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {
      title: "Login",
      requiresUnauth: true,
    },
  },
    {
    path: "/boletin",
    name: "boletin",
    component: BoletinView,
    meta: {
      title: "Boletin",
      requiresAuth: true,
    },
  },
      {
    path: "/boletin-list",
    name: "boletin-list",
    component: BoletinView_List,
    meta: {
      title: "Boletin",
      requiresAuth: true,
    },
  },
  {
    path: "/password-reset",
    name: "password-reset",
    component: PasswordResetRequest,
  },
  {
    path: "/reset-password",
    name: "reset-password",
    component: PasswordResetConfirm,
    props: (route) => ({ token: route.query.token }),
  },
  {
    path: "/:catchAll(.*)",
    name: "not-found",
    component: NotFoundView,
    meta: {
      title: "Página no encontrada",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("auth_token");
  const isStaff = localStorage.getItem("is_staff") === "true";

  // Actualizar título del documento
  document.title = to.meta.title || "DIMON APP";

  // Excepciones para rutas que no requieren autenticación
  const publicRoutes = ['login', 'password-reset', 'reset-password'];
  
  if (publicRoutes.includes(to.name)) {
    next();
    return;
  }

  // Redirecciones según autenticación
  if (to.meta.requiresUnauth && isAuthenticated) {
    next({ name: "FICHAS" });
    return;
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: "login" });
    return;
  }

  // Verificación de staff
  if (to.meta.requiresStaff && !isStaff) {
    next({ name: "HOME" });
    return;
  }

  next();
});

export default router;

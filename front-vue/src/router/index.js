import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FichasView from "../views/FichasView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import LoginView from "../views/fichas/login/LoginView.vue";
import PasswordResetRequest from "@/views/fichas/login/PasswordResetRequest.vue";
import PasswordResetConfirm from "@/views/fichas/login/PasswordResetConfirm.vue";
import EvaluarFichaView from "../views/EvaluarFichaView.vue";
import MatrizCompromisoView from "../views/MatrizCompromisoView.vue";
import UrlsView from "../views/menu/UrlsView.vue";
import AlertasView from "../views/AlertasView.vue";
import GameView from "../views/etc/GameView.vue";
import SeguimientoMatrizView from "../views/SeguimientoMatriz.vue";
import BoletinView from "../views/BoletinView.vue";
import BoletinView_List from "../views/BoletinView_List.vue";
import ReunionesView from "../views/ReunionesView.vue";
import EventosView from "../views/EventosView.vue";
import EventosAdminView from "../views/EventosAdminView.vue";
import ArchivosInteresView from "../views/ArchivosInteresView.vue";
import ConsultaExternaView from "../views/modulos/ConsultaExternaView.vue";

const routes = [
  {
    path: "/",
    name: "HOME",
    component: HomeView,
    meta: {
      title: "DIMON APP",
      requiresUnauth: false, // Explícitamente permite acceso sin autenticación
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
    path: "/archivos",
    name: "archivos",
    component: ArchivosInteresView,
    props: true,
    meta: {
      title: "Enlaces de información",
      requiresAuth: true,
    },
  },
  {
    path: "/reuniones/admin",
    name: "reuniones-admin",
    component: EventosAdminView,
    props: true,
    meta: {
      title: "Eventos Admin",
      requiresAuth: true,
    },
  },
  {
    path: "/reuniones",
    name: "reuniones",
    component: EventosView,
    props: true,
    meta: {
      title: "Eventos",
      requiresAuth: false,
    },
  },
  {
    path: "/reuniones/asistencia",
    name: "reunion-asistencia",
    component: ReunionesView,
    props: true,
    meta: {
      title: "Reuniones",
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
    path: "/consulta-externa",
    name: "consulta-externa",
    component: ConsultaExternaView,
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

  document.title = to.meta.title || "DIMON APP";

  // 🚫 Si la ruta requiere NO estar autenticado, pero el usuario sí lo está
  if (to.meta.requiresUnauth && isAuthenticated) {
    return next({ name: "FICHAS" });
  }

  // Solo redirige al login si explícitamente requiere auth
  if (to.meta.requiresAuth === true && !isAuthenticated) {
    return next({ name: "login" });
  }

  // 🧑‍💼 Si se requiere staff y no lo es
  if (to.meta.requiresStaff && !isStaff) {
    return next({ name: "HOME" });
  }

  next();
});

export default router;

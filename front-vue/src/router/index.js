import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FichasView from "../views/FichasView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import LoginView from "../views/fichas/login/LoginView.vue";
import SeleccionFichaView from "../views/SeleccionFichaView.vue";
import EvaluarFichaView from "../views/EvaluarFichaView.vue";
import MatrizCompromisoView from "../views/MatrizCompromisoView.vue";
import TestLineView from "../views/TestLineView.vue";

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
    path: "/test",
    name: "test",
    component: TestLineView,
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
    path: "/fichas/seleccion",
    name: "seleccion-ficha",
    component: SeleccionFichaView,
    meta: {
      title: "Seleccionar Ficha",
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
    path: '/matriz-compromiso/matriz/:id',
    name: "matriz-compromiso",
    component: MatrizCompromisoView,
    props: true,
    meta: {
      title: "Matriz de Compromiso",
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

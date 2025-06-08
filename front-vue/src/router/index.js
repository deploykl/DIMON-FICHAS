import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import LoginView from "../views/fichas/login/LoginView.vue";

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
    path: "/about",
    name: "FICHAS",
    component: AboutView,
    meta: {
      title: "FICHAS",
      requiresAuth: true,
      requiresStaff: true, // Solo personal autorizado
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {
      title: "Login",
      requiresUnauth: true, // Nueva propiedad meta para rutas que requieren NO estar autenticado
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
  const isAdmin =
    localStorage.getItem("is_superuser") === "true" ||
    localStorage.getItem("is_staff") === "true";

  // Document title
  document.title = to.meta.title || "Fichas App";

  // Si la ruta requiere NO estar autenticado pero el usuario sí lo está
  if (to.meta.requiresUnauth && isAuthenticated) {
    next({ name: "FICHAS" }); // Redirigir al home
    return;
  }

  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: "login" });
    return;
  }

  // Si la ruta requiere admin y el usuario no es admin
  if (to.meta.isAdmin && !isAdmin) {
    next({ name: "HOME" });
    return;
  }

  // En cualquier otro caso, permitir acceso
  next();
});

export default router;

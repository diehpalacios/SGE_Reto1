// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import DashboardCitas from '../components/DashboardCitas.vue';
import ListaClientes from '../components/ListaClientes.vue';
import ListaProfesionales from '../components/ListaProfesionales.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: DashboardCitas },
    { path: '/clientes', name: 'Clientes', component: ListaClientes },
    {path: '/profesionales', name: 'Profesionales', component: ListaProfesionales },
  ]
});

export default router;
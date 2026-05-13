<template>
  <div class="container">
    <div class="header">
      <h2>📅 Dashboard de Citas</h2>
      <button @click="mostrarFormulario = !mostrarFormulario" class="btn-primary">
        {{ mostrarFormulario ? 'Cancelar' : '+ Nueva Cita' }}
      </button>
    </div>

    <div v-if="mostrarFormulario" class="formulario-caja">
      <h3>Crear Nueva Cita</h3>
      <form @submit.prevent="guardarCita" class="grid-form">

        <div class="form-group">
          <label>Fecha:</label>
          <input type="date" v-model="nuevaCita.fecha" required>
        </div>

        <div class="form-group">
          <label>Hora Inicio:</label>
          <input type="time" v-model="nuevaCita.hora_inicio" required>
        </div>

        <div class="form-group">
          <label>Hora Fin:</label>
          <input type="time" v-model="nuevaCita.hora_fin" required>
        </div>

        <div class="form-group">
          <label>Cliente:</label>
          <select v-model="nuevaCita.cliente" required>
            <option v-for="c in clientes" :key="c.id" :value="c.id">
              {{ c.nombre }} {{ c.apellidos }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Profesional:</label>
          <select v-model="nuevaCita.profesional" required>
            <option v-for="p in profesionales" :key="p.id" :value="p.id">
              {{ p.nombre }} {{ p.apellidos }} ({{ p.especialidad }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Servicio:</label>
          <select v-model="nuevaCita.servicio">
            <option v-for="s in servicios" :key="s.id" :value="s.id">
              {{ s.nombre }}
            </option>
          </select>
        </div>

        <div class="form-group full-width">
          <button type="submit" class="btn-success">Guardar Cita</button>
        </div>
      </form>
    </div>

    <div v-if="cargando" class="loading">Cargando datos...</div>

    <table v-else class="tabla-citas">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Hora Inicio</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cita in citas" :key="cita.id">
          <td>{{ cita.fecha }}</td>
          <td>{{ cita.hora_inicio }}</td>
          <td>
            <span :class="'badge badge-' + cita.estado.toLowerCase()">
              {{ cita.estado }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api.js';

// Variables de estado
const citas = ref([]);
const clientes = ref([]);
const profesionales = ref([]);
const servicios = ref([]);
const cargando = ref(true);
const mostrarFormulario = ref(false);

// Modelo para la nueva cita
const nuevaCita = ref({
  fecha: '',
  hora_inicio: '',
  hora_fin: '',
  estado: 'PENDIENTE', // Por defecto
  cliente: '',
  profesional: '',
  servicio: ''
});

// Cargar todos los datos iniciales
onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  cargando.value = true;
  try {
    // Hacemos las peticiones en paralelo para que sea más rápido
    const [resCitas, resClientes, resProfesionales, resServicios] = await Promise.all([
      api.get('citas/'),
      api.get('clientes/'),
      api.get('profesionales/'),
      api.get('servicios/')
    ]);

    citas.value = resCitas.data;
    clientes.value = resClientes.data;
    profesionales.value = resProfesionales.data;
    servicios.value = resServicios.data;
  } catch (error) {
    console.error("Error al cargar datos:", error);
    alert("Hubo un error de conexión.");
  } finally {
    cargando.value = false;
  }
};

// Función para enviar el formulario por POST
const guardarCita = async () => {
  try {
    await api.post('citas/', nuevaCita.value);
    alert("¡Cita creada con éxito!");

    // Ocultar formulario y limpiar datos
    mostrarFormulario.value = false;
    nuevaCita.value = { fecha: '', hora_inicio: '', hora_fin: '', estado: 'PENDIENTE', cliente: '', profesional: '', servicio: '' };

    // Recargar la tabla para ver la nueva cita
    await cargarDatos();
  } catch (error) {
    console.error("Error al crear cita:", error);
    alert("Hubo un error al crear la cita. Revisa la consola.");
  }
};
</script>

<style scoped>
.container { max-width: 900px; margin: 40px auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.btn-primary { background-color: #0056b3; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; }
.btn-success { background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;}
.btn-primary:hover { background-color: #004494; }

/* Estilos del Formulario */
.formulario-caja { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #ddd; }
.grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;}
.form-group { display: flex; flex-direction: column; }
.form-group label { font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; color: #333;}
.form-group input, .form-group select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.full-width { grid-column: 1 / -1; margin-top: 10px;}

/* Estilos de la tabla */
.tabla-citas { width: 100%; border-collapse: collapse; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.tabla-citas th, .tabla-citas td { border-bottom: 1px solid #eee; padding: 15px; text-align: left; }
.tabla-citas th { background-color: #f1f1f1; color: #555;}
.loading { font-size: 1.2rem; color: #666; margin-top: 20px; text-align: center; }

/* Badges */
.badge { padding: 5px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; color: white; }
.badge-pendiente { background-color: #ff9800; }
.badge-confirmada { background-color: #2196f3; }
.badge-realizada { background-color: #4caf50; }
.badge-cancelada { background-color: #f44336; }
</style>
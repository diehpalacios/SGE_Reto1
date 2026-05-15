<template>
  <div class="container">
    <div class="header">
      <h2>👨‍⚕️ Directorio de Profesionales</h2>
      <button @click="toggleFormulario" class="btn-primary">
        {{ mostrarFormulario ? 'Cancelar' : '+ Añadir Profesional' }}
      </button>
    </div>

    <div v-if="mostrarFormulario" class="formulario-caja">
      <h3>{{ editando ? 'Editar Profesional' : 'Registrar Nuevo Profesional' }}</h3>
      <form @submit.prevent="guardarProfesional" class="grid-form">

        <div class="form-group"><label>DNI:</label><input type="text" v-model="formularioProfesional.dni" required maxlength="20"></div>
        <div class="form-group"><label>Nombre:</label><input type="text" v-model="formularioProfesional.nombre" required></div>
        <div class="form-group"><label>Apellidos:</label><input type="text" v-model="formularioProfesional.apellidos" required></div>
        <div class="form-group"><label>Email:</label><input type="email" v-model="formularioProfesional.email" required></div>
        <div class="form-group"><label>Teléfono:</label><input type="text" v-model="formularioProfesional.telefono" required maxlength="15"></div>
        <div class="form-group"><label>Especialidad:</label><input type="text" v-model="formularioProfesional.especialidad" required placeholder="Ej: Pediatría"></div>

        <div class="form-group">
          <label>Estado:</label>
          <select v-model="formularioProfesional.estado" required>
            <option value="ACTIVO">Activo</option>
            <option value="INACTIVO">Inactivo</option>
            <option value="BAJA">De Baja</option>
          </select>
        </div>

        <div class="form-group full-width">
          <label>Servicios que presta (Mantén pulsado Ctrl/Cmd para seleccionar varios):</label>
          <select v-model="formularioProfesional.servicios" multiple class="select-multiple">
            <option v-for="s in listaServicios" :key="s.id" :value="s.id">
              {{ s.nombre }}
            </option>
          </select>
          <small class="hint">Debes seleccionar al menos un servicio.</small>
        </div>

        <div class="form-group full-width">
          <button type="submit" class="btn-success">
            {{ editando ? 'Actualizar Profesional' : 'Guardar Profesional' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="cargando" class="loading">Cargando profesionales...</div>

    <table v-else class="tabla-datos">
      <thead>
        <tr>
          <th>DNI</th>
          <th>Nombre Completo</th>
          <th>Especialidad</th>
          <th>Teléfono</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="profesional in profesionales" :key="profesional.id">
          <td>{{ profesional.dni }}</td>
          <td><strong>{{ profesional.apellidos }}, {{ profesional.nombre }}</strong></td>
          <td><span class="badge badge-info">{{ profesional.especialidad }}</span></td>
          <td>{{ profesional.telefono }}</td>
          <td><strong>{{ profesional.estado }}</strong></td>
          <td>
            <button @click="cargarDatosParaEditar(profesional)" class="btn-warning">Editar</button>
            <button @click="borrarProfesional(profesional.id)" class="btn-danger">Borrar</button>
          </td>
        </tr>
        <tr v-if="profesionales.length === 0">
          <td colspan="6" class="text-center">No hay profesionales registrados.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api.js';

const profesionales = ref([]);
const listaServicios = ref([]); // Lista de servicios desde el backend
const cargando = ref(true);
const mostrarFormulario = ref(false);
const editando = ref(false);

const formularioProfesional = ref({
  id: null,
  dni: '',
  nombre: '',
  apellidos: '',
  email: '',
  telefono: '',
  especialidad: '',
  estado: 'ACTIVO',
  servicios: [] // Añadimos el array vacío para enviar los servicios
});

onMounted(async () => {
  await cargarDatosBase();
});

const cargarDatosBase = async () => {
  try {
    // Cargamos tanto los profesionales como los servicios disponibles
    const [resProfesionales, resServicios] = await Promise.all([
      api.get('profesionales/'),
      api.get('servicios/')
    ]);
    profesionales.value = resProfesionales.data;
    listaServicios.value = resServicios.data;
  } catch (error) {
    console.error("Error al cargar datos:", error);
  } finally {
    cargando.value = false;
  }
};

const toggleFormulario = () => {
  mostrarFormulario.value = !mostrarFormulario.value;
  if (!mostrarFormulario.value) limpiarFormulario();
};

const limpiarFormulario = () => {
  editando.value = false;
  formularioProfesional.value = { id: null, dni: '', nombre: '', apellidos: '', email: '', telefono: '', especialidad: '', estado: 'ACTIVO', servicios: [] };
};

const cargarDatosParaEditar = (profesional) => {
  formularioProfesional.value = { ...profesional };
  editando.value = true;
  mostrarFormulario.value = true;
};

const guardarProfesional = async () => {
  try {
    if (editando.value) {
      await api.put(`profesionales/${formularioProfesional.value.id}/`, formularioProfesional.value);
    } else {
      await api.post('profesionales/', formularioProfesional.value);
    }
    mostrarFormulario.value = false;
    limpiarFormulario();
    // Recargamos datos para ver el nuevo profesional
    await cargarDatosBase();
  } catch (error) {
    if (error.response && error.response.data) {
      console.error("Errores de Django:", error.response.data);
      const mensajes = Object.entries(error.response.data)
        .map(([campo, errores]) => `${campo.toUpperCase()}: ${errores.join(', ')}`)
        .join('\n');
      alert("⚠️ Error al guardar:\n" + mensajes);
    } else {
      alert("Error de conexión. Revisa la consola.");
    }
  }
};

const borrarProfesional = async (id) => {
  if (confirm("¿Borrar este profesional? Se borrarán sus citas asociadas.")) {
    try {
      await api.delete(`profesionales/${id}/`);
      await cargarDatosBase();
    } catch (error) {
      console.error("Error al borrar:", error);
    }
  }
};
</script>

<style scoped>
.container { max-width: 1000px; margin: 20px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.btn-primary { background-color: #0056b3; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; }
.btn-primary:hover { background-color: #004494; }
.btn-success { background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;}
.btn-danger { background-color: #ffebee; color: #c62828; border: 1px solid #ffcdd2; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-warning { background-color: #fff3e0; color: #e65100; border: 1px solid #ffe0b2; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 5px; }
.formulario-caja { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #ddd; }
.grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;}
.form-group { display: flex; flex-direction: column; }
.form-group label { font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; color: #333;}
.form-group input, .form-group select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.select-multiple { height: 100px; }
.hint { color: #666; font-size: 0.8em; margin-top: 4px; }
.full-width { grid-column: 1 / -1; margin-top: 10px;}
.tabla-datos { width: 100%; border-collapse: collapse; margin-top: 10px; }
.tabla-datos th, .tabla-datos td { border-bottom: 1px solid #eee; padding: 12px; text-align: left; }
.tabla-datos th { background-color: #f8f9fa; color: #555; }
.text-center { text-align: center; color: #888; }
.badge-info { background-color: #17a2b8; padding: 5px 10px; border-radius: 12px; color: white; font-size: 0.85em;}
</style>
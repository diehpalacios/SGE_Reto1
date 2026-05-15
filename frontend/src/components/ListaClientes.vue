<template>
  <div class="container">
    <div class="header">
      <h2>👥 Directorio de Clientes</h2>
      <button @click="toggleFormulario" class="btn-primary">
        {{ mostrarFormulario ? 'Cancelar' : '+ Añadir Cliente' }}
      </button>
    </div>

    <div v-if="mostrarFormulario" class="formulario-caja">
      <h3>{{ editando ? 'Editar Cliente' : 'Registrar Nuevo Cliente' }}</h3>
      <form @submit.prevent="guardarCliente" class="grid-form">

        <div class="form-group">
          <label>DNI:</label>
          <input type="text" v-model="formularioCliente.dni" required maxlength="20">
        </div>

        <div class="form-group">
          <label>Nombre:</label>
          <input type="text" v-model="formularioCliente.nombre" required>
        </div>

        <div class="form-group">
          <label>Apellidos:</label>
          <input type="text" v-model="formularioCliente.apellidos" required>
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="formularioCliente.email" required>
        </div>

        <div class="form-group">
          <label>Teléfono:</label>
          <input type="text" v-model="formularioCliente.telefono" required maxlength="15">
        </div>

        <div class="form-group full-width">
          <button type="submit" class="btn-success">
            {{ editando ? 'Actualizar Cliente' : 'Guardar Cliente' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="cargando" class="loading">Cargando clientes...</div>

    <table v-else class="tabla-datos">
      <thead>
        <tr>
          <th>DNI</th>
          <th>Nombre Completo</th>
          <th>Email</th>
          <th>Teléfono</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cliente in clientes" :key="cliente.id">
          <td>{{ cliente.dni }}</td>
          <td><strong>{{ cliente.apellidos }}, {{ cliente.nombre }}</strong></td>
          <td>{{ cliente.email }}</td>
          <td>{{ cliente.telefono }}</td>
          <td>
            <button @click="cargarDatosParaEditar(cliente)" class="btn-warning">Editar</button>
            <button @click="borrarCliente(cliente.id)" class="btn-danger">Borrar</button>
          </td>
        </tr>
        <tr v-if="clientes.length === 0">
          <td colspan="5" class="text-center">No hay clientes registrados.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api.js';

const clientes = ref([]);
const cargando = ref(true);
const mostrarFormulario = ref(false);
const editando = ref(false); // Para saber si estamos creando o editando

// Modelo unificado para el formulario
const formularioCliente = ref({
  id: null,
  dni: '',
  nombre: '',
  apellidos: '',
  email: '',
  telefono: ''
});

onMounted(async () => {
  await cargarClientes();
});

const cargarClientes = async () => {
  try {
    const respuesta = await api.get('clientes/');
    clientes.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar clientes:", error);
  } finally {
    cargando.value = false;
  }
};

// Función para abrir/cerrar el formulario limpiando los datos
const toggleFormulario = () => {
  mostrarFormulario.value = !mostrarFormulario.value;
  if (!mostrarFormulario.value) {
    limpiarFormulario();
  }
};

const limpiarFormulario = () => {
  editando.value = false;
  formularioCliente.value = { id: null, dni: '', nombre: '', apellidos: '', email: '', telefono: '' };
};

// Prepara el formulario con los datos del cliente a editar
const cargarDatosParaEditar = (cliente) => {
  formularioCliente.value = { ...cliente }; // Copiamos los datos para no modificar la tabla en tiempo real
  editando.value = true;
  mostrarFormulario.value = true;
};

// Función dual: Crea (POST) o Actualiza (PUT)
const guardarCliente = async () => {
  try {
    if (editando.value) {
      // Hacemos PUT a la URL específica del cliente (ej: /api/clientes/3/)
      await api.put(`clientes/${formularioCliente.value.id}/`, formularioCliente.value);
      alert("¡Cliente actualizado con éxito!");
    } else {
      // Hacemos POST para crear
      await api.post('clientes/', formularioCliente.value);
      alert("¡Cliente registrado con éxito!");
    }

    mostrarFormulario.value = false;
    limpiarFormulario();
    await cargarClientes(); // Recargamos la tabla
  } catch (error) {
    console.error("Error al guardar:", error);
    alert("Hubo un error al guardar. Revisa la consola.");
  }
};

const borrarCliente = async (id) => {
  if (confirm("¿Estás seguro de que deseas borrar este cliente? Se borrarán también sus citas asociadas.")) {
    try {
      await api.delete(`clientes/${id}/`);
      await cargarClientes();
    } catch (error) {
      console.error("Error al borrar:", error);
      alert("Hubo un error al borrar el cliente.");
    }
  }
};
</script>

<style scoped>
.container { max-width: 1000px; margin: 20px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }

/* Botones */
.btn-primary { background-color: #0056b3; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; }
.btn-primary:hover { background-color: #004494; }
.btn-success { background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;}
.btn-success:hover { background-color: #218838; }
.btn-danger { background-color: #ffebee; color: #c62828; border: 1px solid #ffcdd2; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-danger:hover { background-color: #ffcdd2; }
.btn-warning { background-color: #fff3e0; color: #e65100; border: 1px solid #ffe0b2; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 5px; }
.btn-warning:hover { background-color: #ffe0b2; }

/* Formulario */
.formulario-caja { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #ddd; }
.grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;}
.form-group { display: flex; flex-direction: column; }
.form-group label { font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; color: #333;}
.form-group input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.full-width { grid-column: 1 / -1; margin-top: 10px;}

/* Tabla */
.tabla-datos { width: 100%; border-collapse: collapse; margin-top: 10px; }
.tabla-datos th, .tabla-datos td { border-bottom: 1px solid #eee; padding: 12px; text-align: left; }
.tabla-datos th { background-color: #f8f9fa; color: #555; }
.text-center { text-align: center; color: #888; }
</style>
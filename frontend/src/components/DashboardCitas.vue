<template>
  <div class="container">

    <div class="header">
      <h2 class="titulo-dashboard">📅 Dashboard de Citas</h2>
      <div class="botones-header">
        <button @click="toggleVista" class="btn-outline-primary">
          {{ vistaActual === 'lista' ? '📆 Ver calendario' : '📋 Ver lista' }}
        </button>
        <button @click="toggleFormulario" class="btn-primary">
          {{ mostrarFormulario ? 'Cancelar' : '+ Nueva Cita' }}
        </button>
      </div>
    </div>

    <div v-if="mostrarFormulario" class="formulario-caja">
      <h3>{{ editando ? 'Editar Cita' : 'Crear Nueva Cita' }}</h3>
      <form @submit.prevent="guardarCita" class="grid-form">
        <div class="form-group"><label>Fecha:</label><input type="date" v-model="formularioCita.fecha" required></div>
        <div class="form-group"><label>Hora Inicio:</label><input type="time" v-model="formularioCita.hora_inicio" required></div>
        <div class="form-group"><label>Hora Fin:</label><input type="time" v-model="formularioCita.hora_fin" required></div>
        <div class="form-group">
          <label>Cliente:</label>
          <select v-model="formularioCita.cliente" required>
            <option value="" disabled>Seleccione un cliente...</option>
            <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }} {{ c.apellidos }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Profesional:</label>
          <select v-model="formularioCita.profesional" required>
            <option value="" disabled>Seleccione un profesional...</option>
            <option v-for="p in profesionales" :key="p.id" :value="p.id">{{ p.nombre }} {{ p.apellidos }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Servicio:</label>
          <select v-model="formularioCita.servicio">
            <option value="" disabled>Seleccione un servicio...</option>
            <option v-for="s in servicios" :key="s.id" :value="s.id">{{ s.nombre }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Estado:</label>
          <select v-model="formularioCita.estado" required>
            <option value="PENDIENTE">Pendiente</option>
            <option value="CONFIRMADA">Confirmada</option>
            <option value="REALIZADA">Realizada</option>
            <option value="CANCELADA">Cancelada</option>
          </select>
        </div>
        <div class="form-group full-width">
          <button type="submit" class="btn-primary" style="width: 100%;">
            {{ editando ? 'Actualizar Cita' : 'Guardar Cita' }}
          </button>
        </div>
      </form>
    </div>

    <div class="filtros-caja" v-if="!cargando && citas.length > 0">
      <div class="filtros-grid">
        <div class="filtro-item">
          <label>Filtrar por Fecha:</label>
          <input type="date" v-model="filtroFecha" class="input-filtro">
        </div>
        <div class="filtro-item">
          <label>Filtrar por Profesional:</label>
          <select v-model="filtroProfesional" class="input-filtro">
            <option value="">-- Todos los Profesionales --</option>
            <option v-for="p in profesionales" :key="p.id" :value="p.id">
              {{ p.nombre }} {{ p.apellidos }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="cargando" class="loading">Cargando datos...</div>

    <table v-if="!cargando && vistaActual === 'lista'" class="tabla-citas">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Horario</th>
          <th>Cliente</th>
          <th>Profesional</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cita in citasFiltradas" :key="cita.id">
          <td>{{ cita.fecha }}</td>
          <td>{{ cita.hora_inicio.substring(0,5) }} -<br>{{ cita.hora_fin.substring(0,5) }}</td>
          <td>{{ getNombreCliente(cita.cliente).replace(' ', '\n') }}</td>
          <td>{{ getNombreProfesional(cita.profesional) }}</td>
          <td>
            <span :class="'badge badge-' + cita.estado.toLowerCase()">
              {{ cita.estado }}
            </span>
          </td>
          <td class="acciones-celda">
            <button @click="cargarDatosParaEditar(cita)" class="btn-accion btn-editar">Editar</button>
            <button @click="borrarCita(cita.id)" class="btn-accion btn-borrar">Borrar</button>
          </td>
        </tr>
        <tr v-if="citasFiltradas.length === 0">
          <td colspan="6" class="text-center">No hay citas que coincidan con los filtros.</td>
        </tr>
      </tbody>
    </table>

    <div v-if="!cargando && vistaActual === 'calendario'" class="calendario-contenedor">

      <div class="calendario-tabs">
        <button @click="vistaCalendario = 'diaria'" :class="{'tab-activa': vistaCalendario === 'diaria'}">Vista Diaria</button>
        <button @click="vistaCalendario = 'semanal'" :class="{'tab-activa': vistaCalendario === 'semanal'}">Vista Semanal</button>
      </div>

      <div v-if="vistaCalendario === 'diaria'" class="agenda-diaria">
        <div v-for="hora in horasAgenda" :key="hora" class="franja-horaria">
          <div class="hora-etiqueta">{{ hora }}:00</div>

          <div class="slots-contenedor" v-if="obtenerCitasEnSlot(hora).length > 0">
            <div v-for="cita in obtenerCitasEnSlot(hora)" :key="cita.id" class="slot-cita slot-ocupado">
              <div>
                <strong>{{ cita.hora_inicio.substring(0,5) }} - {{ cita.hora_fin.substring(0,5) }}</strong><br>
                👤 {{ getNombreCliente(cita.cliente) }} <span class="profesional-agenda">({{ getNombreProfesional(cita.profesional) }})</span>
              </div>
              <span :class="'badge badge-' + cita.estado.toLowerCase()">{{ cita.estado }}</span>
            </div>
            <div class="slot-cita slot-extra" v-if="!filtroProfesional">
              <button @click="abrirFormularioPrellenado(hora)" class="btn-nueva-cita-slot btn-sm">+ Nueva Cita</button>
            </div>
          </div>

          <div v-else class="slot-cita slot-libre">
            <span class="texto-libre">+ Huecos Disponibles</span>
            <button @click="abrirFormularioPrellenado(hora)" class="btn-nueva-cita-slot">+ Nueva Cita</button>
          </div>
        </div>
      </div>

      <div v-if="vistaCalendario === 'semanal'" class="agenda-semanal">
        <div v-for="dia in diasSemana" :key="dia.fechaISO" class="dia-columna">
          <div class="dia-cabecera" :class="{'dia-actual': dia.fechaISO === filtroFecha}">
            <span class="nombre-dia">{{ dia.nombreDia }}</span>
            <span class="numero-dia">{{ dia.diaMes }}</span>
          </div>
          <div class="dia-cuerpo">
            <div v-for="cita in obtenerCitasPorDia(dia.fechaISO)" :key="cita.id" class="tarjeta-cita-semana">
              <strong>{{ cita.hora_inicio.substring(0,5) }}</strong><br>
              {{ getNombreCliente(cita.cliente).split(' ')[0] }}<br>
              <span class="profesional-agenda-semana">{{ getNombreProfesional(cita.profesional).split(' ')[0] }}</span>
              <span class="puntito-estado" :class="'bg-' + cita.estado.toLowerCase()"></span>
            </div>
            <div v-if="obtenerCitasPorDia(dia.fechaISO).length === 0" class="sin-citas">
              <span style="display:block; margin-bottom: 8px;">Libre</span>
              <button @click="abrirFormularioPrellenado(null, dia.fechaISO)" class="btn-nueva-cita-slot btn-block">+ Cita</button>
            </div>
            <div v-else class="acciones-semana">
              <button @click="abrirFormularioPrellenado(null, dia.fechaISO)" class="btn-nueva-cita-slot btn-block" style="font-size: 0.75rem;">+ Añadir</button>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated } from 'vue';
import api from '../api.js';

const citas = ref([]);
const clientes = ref([]);
const profesionales = ref([]);
const servicios = ref([]);
const cargando = ref(true);

const mostrarFormulario = ref(false);
const editando = ref(false);

const vistaActual = ref('lista');
const vistaCalendario = ref('diaria');

const hoy = new Date().toISOString().split('T')[0];
const filtroFecha = ref(hoy);
const filtroProfesional = ref('');

const horasAgenda = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'];

const formularioCita = ref({
  id: null, fecha: '', hora_inicio: '', hora_fin: '', estado: 'PENDIENTE', cliente: '', profesional: '', servicio: ''
});

onMounted(async () => {
  await cargarDatos();
});

onActivated(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  cargando.value = true;
  try {
    const [resCitas, resClientes, resProfesionales, resServicios] = await Promise.all([
      api.get('citas/'), api.get('clientes/'), api.get('profesionales/'), api.get('servicios/')
    ]);
    citas.value = resCitas.data;
    clientes.value = resClientes.data;
    profesionales.value = resProfesionales.data;
    servicios.value = resServicios.data;
  } catch (error) {
    console.error("Error al cargar datos:", error);
  } finally {
    cargando.value = false;
  }
};

const citasFiltradas = computed(() => {
  return citas.value.filter(cita => {
    let coincideFecha = true;
    let coincideProfesional = true;
    if (filtroFecha.value) coincideFecha = cita.fecha === filtroFecha.value;
    if (filtroProfesional.value) coincideProfesional = String(cita.profesional) === String(filtroProfesional.value);
    return coincideFecha && coincideProfesional;
  });
});

const obtenerCitasEnSlot = (hora) => {
  return citasFiltradas.value.filter(cita => cita.hora_inicio.split(':')[0] === hora);
};

const diasSemana = computed(() => {
  // 1. Leemos la fecha evitando problemas de zona horaria
  const fechaBase = filtroFecha.value ? filtroFecha.value : hoy;
  const [yearStr, monthStr, dayStr] = fechaBase.split('-');
  const baseDate = new Date(yearStr, monthStr - 1, dayStr); // Creamos la fecha a las 00:00 locales

  // 2. Retrocedemos al Lunes de esa semana de forma segura
  const day = baseDate.getDay() || 7;
  if (day !== 1) {
    baseDate.setDate(baseDate.getDate() - (day - 1));
  }

  const week = [];
  // 3. Generamos los 5 días (Lunes a Viernes)
  for(let i=0; i<5; i++) {
     const d = new Date(baseDate);
     d.setDate(d.getDate() + i);

     // Construimos el YYYY-MM-DD manualmente en HORA LOCAL (Sin usar toISOString)
     const yyyy = d.getFullYear();
     const mm = String(d.getMonth() + 1).padStart(2, '0');
     const dd = String(d.getDate()).padStart(2, '0');

     week.push({
        fechaISO: `${yyyy}-${mm}-${dd}`,
        nombreDia: d.toLocaleDateString('es-ES', { weekday: 'short' }).toUpperCase(),
        diaMes: d.getDate()
     });
  }
  return week;
});

const obtenerCitasPorDia = (fechaISO) => {
   return citas.value.filter(c => {
       let coincideFecha = c.fecha === fechaISO;
       let coincideProfesional = filtroProfesional.value ? String(c.profesional) === String(filtroProfesional.value) : true;
       return coincideFecha && coincideProfesional;
   });
}

const abrirFormularioPrellenado = (hora, fechaSemana = null) => {
  limpiarFormulario();

  formularioCita.value.fecha = fechaSemana ? fechaSemana : filtroFecha.value;
  if (hora) {
    formularioCita.value.hora_inicio = `${hora}:00`;
  }

  if (filtroProfesional.value) {
    formularioCita.value.profesional = filtroProfesional.value;
  }

  mostrarFormulario.value = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Utilidades
const getNombreCliente = (id) => {
  const c = clientes.value.find(c => c.id === id);
  return c ? `${c.nombre} ${c.apellidos}` : 'Desconocido';
};
const getNombreProfesional = (id) => {
  const p = profesionales.value.find(p => p.id === id);
  return p ? `${p.nombre} ${p.apellidos}` : 'Desconocido';
};

const toggleVista = () => {
  vistaActual.value = vistaActual.value === 'lista' ? 'calendario' : 'lista';
};

const toggleFormulario = () => {
  mostrarFormulario.value = !mostrarFormulario.value;
  if (!mostrarFormulario.value) limpiarFormulario();
};

const limpiarFormulario = () => {
  editando.value = false;
  formularioCita.value = { id: null, fecha: '', hora_inicio: '', hora_fin: '', estado: 'PENDIENTE', cliente: '', profesional: '', servicio: '' };
};

const cargarDatosParaEditar = (cita) => {
  formularioCita.value = { ...cita };
  editando.value = true;
  mostrarFormulario.value = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// --- MAGIA AÑADIDA: VALIDACIÓN DE FIN DE SEMANA ---
const guardarCita = async () => {
  // Validación para bloquear sábados (6) y domingos (0)
  if (formularioCita.value.fecha) {
    // Dividimos la fecha (YYYY-MM-DD) para evitar problemas de zona horaria al instanciar Date
    const [year, month, day] = formularioCita.value.fecha.split('-');
    const dateObj = new Date(year, month - 1, day);
    const dayOfWeek = dateObj.getDay();

    if (dayOfWeek === 0 || dayOfWeek === 6) {
      alert("⚠️ Error: La clínica está cerrada los fines de semana. Por favor, selecciona una fecha de Lunes a Viernes.");
      return; // Bloqueamos la ejecución, no se hace el POST ni PUT
    }
  }

  try {
    if (editando.value) {
      await api.put(`citas/${formularioCita.value.id}/`, formularioCita.value);
    } else {
      await api.post('citas/', formularioCita.value);
    }
    mostrarFormulario.value = false;
    limpiarFormulario();
    await cargarDatos();
  } catch (error) {
    if (error.response && error.response.data && error.response.data.error) {
      alert("⚠️ " + error.response.data.error);
    } else {
      alert("Error al guardar. Revisa la consola.");
    }
  }
};

const borrarCita = async (id) => {
  if (confirm("¿Estás seguro de que deseas borrar esta cita?")) {
    try {
      await api.delete(`citas/${id}/`);
      await cargarDatos();
    } catch (error) {
      console.error("Error al borrar:", error);
    }
  }
};
</script>

<style scoped>
/* ========================================= */
/* CLONANDO LA ESTÉTICA DE LA IMAGEN         */
/* ========================================= */

.container { max-width: 1000px; margin: 40px auto; font-family: 'Segoe UI', system-ui, sans-serif; }

/* Cabecera */
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.titulo-dashboard { font-weight: 800; font-size: 1.8rem; color: #1e293b; margin: 0; display: flex; align-items: center; gap: 8px;}
.botones-header { display: flex; gap: 10px; }

/* Botones principales */
.btn-primary { background-color: #0d6efd; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.95rem; }
.btn-primary:hover { background-color: #0b5ed7; }
.btn-outline-primary { background-color: white; color: #0d6efd; border: 2px solid #0d6efd; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.95rem;}
.btn-outline-primary:hover { background-color: #f8f9fa; }

/* Caja de Filtros Gris */
.filtros-caja { background-color: #e9ecef; padding: 25px 20px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #dee2e6; }
.filtros-grid { display: flex; gap: 40px; }
.filtro-item { display: flex; flex-direction: column; flex: 1; }
.filtro-item label { font-weight: 700; color: #495057; margin-bottom: 8px; font-size: 0.95rem; }
.input-filtro { padding: 10px; border: 1px solid #ced4da; border-radius: 6px; font-size: 0.95rem; background-color: white; color: #495057;}

/* Tabla estilo captura */
.tabla-citas { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
.tabla-citas th { background-color: #f8f9fa; color: #6c757d; font-weight: 700; padding: 15px; text-align: left; font-size: 1rem; border-bottom: 1px solid #dee2e6; }
.tabla-citas td { padding: 18px 15px; border-bottom: 1px solid #f1f3f5; color: #212529; font-size: 0.95rem; vertical-align: middle; white-space: pre-line;}

/* Badges de colores exactos */
.badge { padding: 6px 14px; border-radius: 20px; font-weight: 800; font-size: 0.75rem; color: white; display: inline-block; text-align: center; text-transform: uppercase; letter-spacing: 0.5px;}
.badge-pendiente { background-color: #fd7e14; }
.badge-confirmada { background-color: #0d6efd; }
.badge-realizada { background-color: #198754; }
.badge-cancelada { background-color: #dc3545; }

/* Botones de acción pálidos de la captura */
.acciones-celda { display: flex; flex-direction: column; gap: 8px; }
.btn-accion { padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; cursor: pointer; text-align: center; border: 1px solid transparent; width: fit-content;}
.btn-editar { color: #d97706; background-color: #fef3c7; border-color: #fde68a; }
.btn-editar:hover { background-color: #fde68a; }
.btn-borrar { color: #dc3545; background-color: #ffebee; border-color: #ffcdd2; }
.btn-borrar:hover { background-color: #ffcdd2; }

/* ========================================= */
/* ESTILOS DEL CALENDARIO                    */
/* ========================================= */
.calendario-contenedor { background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; }
.calendario-tabs { display: flex; border-bottom: 2px solid #e9ecef; margin-bottom: 20px; }
.calendario-tabs button { flex: 1; padding: 12px; background: none; border: none; font-size: 1rem; font-weight: 600; color: #6c757d; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px;}
.calendario-tabs button.tab-activa { color: #0d6efd; border-bottom-color: #0d6efd; }

/* Diario */
.agenda-diaria { display: flex; flex-direction: column; gap: 8px; }
.franja-horaria { display: flex; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; overflow: hidden; min-height: 60px;}
.hora-etiqueta { width: 80px; background: #e9ecef; color: #495057; display: flex; align-items: center; justify-content: center; font-weight: 700; }
.slots-contenedor { flex: 1; display: flex; flex-direction: column; }
.slot-cita { flex: 1; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; }
.slot-cita:last-child { border-bottom: none; }
.slot-ocupado { background: white; border-left: 4px solid #0d6efd; }
.slot-libre { background: #f8fff9; border-left: 4px solid #198754; color: #198754; font-weight: 600; font-style: italic;}
.profesional-agenda { color: #6c757d; font-size: 0.85rem;}

/* NUEVO BOTÓN DE CITA EN CALENDARIO (Índigo) */
.btn-nueva-cita-slot { background-color: #6366f1; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: 0.2s;}
.btn-nueva-cita-slot:hover { background-color: #4f46e5; }
.btn-sm { font-size: 0.75rem; padding: 4px 10px; }
.btn-block { width: 100%; text-align: center; }
.slot-extra { background-color: #f8f9fa; justify-content: flex-end; padding: 8px 15px; }

/* Semanal */
.agenda-semanal { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.dia-columna { border: 1px solid #dee2e6; border-radius: 6px; overflow: hidden; background: #f8f9fa; min-height: 300px; }
.dia-cabecera { background: #e9ecef; padding: 10px; text-align: center; display: flex; flex-direction: column; border-bottom: 1px solid #dee2e6;}
.dia-actual { background: #cfe2ff; color: #084298; border-bottom-color: #9ec5fe;}
.nombre-dia { font-size: 0.8rem; font-weight: 700; color: #6c757d; }
.numero-dia { font-size: 1.5rem; font-weight: 800; }
.dia-cuerpo { padding: 10px; display: flex; flex-direction: column; gap: 8px; }
.tarjeta-cita-semana { background: white; border: 1px solid #dee2e6; border-left: 3px solid #0d6efd; padding: 8px; border-radius: 4px; font-size: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); position: relative;}
.sin-citas { text-align: center; color: #adb5bd; font-size: 0.85rem; font-style: italic; margin-top: 15px;}
.acciones-semana { text-align: center; margin-top: 10px; }
.puntito-estado { position: absolute; top: 8px; right: 8px; width: 8px; height: 8px; border-radius: 50%; }
.profesional-agenda-semana { color: #6c757d; font-size: 0.75rem; }
.bg-pendiente { background-color: #fd7e14; }
.bg-confirmada { background-color: #0d6efd; }
.bg-realizada { background-color: #198754; }
.bg-cancelada { background-color: #dc3545; }

.formulario-caja { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #ddd; }
.grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;}
.form-group { display: flex; flex-direction: column; }
.form-group label { font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; color: #333;}
.form-group input, .form-group select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.full-width { grid-column: 1 / -1; margin-top: 10px;}
</style>
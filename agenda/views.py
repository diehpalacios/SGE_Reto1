from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita, Cliente
from .forms import CitaForm, ClienteForm

def dashboard_citas(request):
    citas = Cita.objects.all().order_by('fecha', 'hora_inicio')
    return render(request, 'agenda/dashboard_citas.html', {'citas': citas})

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save() # Guarda la cita en la base de datos
            return redirect('dashboard_citas') # Nos devuelve al panel principal
    else:
        form = CitaForm() # Muestra el formulario vacío

    return render(request, 'agenda/crear_cita.html', {'form': form})

def editar_cita(request, cita_id):
    # Buscamos la cita específica en la base de datos
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        # Le pasamos al formulario los datos nuevos (POST) y la cita original (instance)
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('dashboard_citas')
    else:
        # Si entra por primera vez, cargamos el formulario con los datos de la cita
        form = CitaForm(instance=cita)

    return render(request, 'agenda/editar_cita.html', {'form': form, 'cita': cita})


# --- VISTAS DE CLIENTES ---

def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('apellidos', 'nombre')
    return render(request, 'agenda/lista_clientes.html', {'clientes': clientes})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    # Usamos la misma plantilla para crear y editar, pasándole una variable de título 'accion'
    return render(request, 'agenda/formulario_cliente.html', {'form': form, 'accion': '➕ Nuevo Cliente'})


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'agenda/formulario_cliente.html',
                  {'form': form, 'accion': f'✏️ Editar: {cliente.nombre} {cliente.apellidos}'})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'agenda/confirmar_eliminar.html',
                  {'objeto': cliente, 'tipo': 'Cliente', 'url_cancelar': 'lista_clientes'})
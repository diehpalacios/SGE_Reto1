# agenda/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... Rutas de Citas ...
    path('', views.dashboard_citas, name='dashboard_citas'),
    path('cita/nueva/', views.crear_cita, name='crear_cita'),
    path('citas/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),

# ... NUEVAS Rutas de Clientes ...
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]

from django.contrib import admin
from .models import Servicio, Profesional, Cliente, Disponibilidad, Cita

# Configuraciones visuales para que el panel luzca mucho más profesional
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'cliente', 'profesional', 'estado') # Columnas a mostrar
    list_filter = ('estado', 'fecha', 'profesional') # Panel lateral para filtrar
    search_fields = ('cliente__nombre', 'cliente__apellidos') # Barra de búsqueda

class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'especialidad', 'estado')
    list_filter = ('estado', 'especialidad')

class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('profesional', 'dia_semana', 'hora_inicio', 'hora_fin', 'activa')
    list_filter = ('dia_semana', 'profesional')

# Registramos los modelos en Django
admin.site.register(Servicio)
admin.site.register(Profesional, ProfesionalAdmin)
admin.site.register(Cliente)
admin.site.register(Disponibilidad, DisponibilidadAdmin)
admin.site.register(Cita, CitaAdmin)
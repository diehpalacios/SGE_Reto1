# agenda/serializers.py
from rest_framework import serializers
from .models import Servicio, Profesional, Cliente, Disponibilidad, Cita
from django.db.models import Q

class DisponibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class ProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesional
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'

    # Esta función intercepta los datos ANTES de guardarlos
    def validate(self, data):
        profesional = data.get('profesional')
        fecha = data.get('fecha')
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        if hora_inicio >= hora_fin:
            raise serializers.ValidationError({"error": "La hora de fin debe ser posterior a la hora de inicio."})

        solapamientos = Cita.objects.filter(
            profesional=profesional,
            fecha=fecha,
            hora_inicio__lt=hora_fin, # La cita existente empieza ANTES de que termine la nueva
            hora_fin__gt=hora_inicio  # La cita existente termina DESPUÉS de que empiece la nueva
        )

        if self.instance:
            solapamientos = solapamientos.exclude(pk=self.instance.pk)

        if solapamientos.exists():
            raise serializers.ValidationError({"error": "Imposible: El profesional ya tiene una cita asignada que se solapa en ese horario."})

        return data

from django import forms
from .models import Cita
from .models import Cliente


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora_inicio', 'hora_fin', 'cliente', 'profesional', 'servicio', 'estado', 'observaciones']

        widgets = {
            # FIX 1: Añadimos format='%Y-%m-%d' para que el HTML5 cargue la fecha correctamente
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-input'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'cliente': forms.Select(attrs={'class': 'form-input'}),
            'profesional': forms.Select(attrs={'class': 'form-input'}),
            'servicio': forms.Select(attrs={'class': 'form-input'}),
            'estado': forms.Select(attrs={'class': 'form-input'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

    # FIX 2: Mejoramos la validación para evitar solapamientos [cite: 251]
    def clean(self):
        cleaned_data = super().clean()
        profesional = cleaned_data.get('profesional')
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        estado = cleaned_data.get('estado')

        if profesional and fecha and hora_inicio and hora_fin:
            # Si el usuario está marcando la cita como CANCELADA, ignoramos la restricción
            if estado == 'CANCELADA':
                return cleaned_data

            # Buscamos citas en ese horario (ignorando las que ya estén canceladas en el sistema)
            solapamientos = Cita.objects.filter(
                profesional=profesional,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exclude(estado='CANCELADA')

            # EXCEPCIÓN CLAVE: Si estamos editando una cita ya existente, la sacamos de la búsqueda
            # para que no diga que choca consigo misma.
            if self.instance and self.instance.pk:
                solapamientos = solapamientos.exclude(pk=self.instance.pk)

            if solapamientos.exists():
                raise forms.ValidationError(
                    "⚠️ Error: El profesional seleccionado ya tiene una cita ocupando ese tramo horario.")

        return cleaned_data

class ClienteForm(forms.ModelForm):
        class Meta:
            model = Cliente
            fields = '__all__'  # Seleccionamos todos los campos del modelo
            widgets = {
                'dni': forms.TextInput(attrs={'class': 'form-input'}),
                'nombre': forms.TextInput(attrs={'class': 'form-input'}),
                'apellidos': forms.TextInput(attrs={'class': 'form-input'}),
                'email': forms.EmailInput(attrs={'class': 'form-input'}),
                'telefono': forms.TextInput(attrs={'class': 'form-input'}),
            }

import re

from django.utils import timezone

from django import forms

from .models import Cita, Resena, Servicio


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre', 'telefono', 'correo', 'servicio', 'barbero', 'fecha', 'hora']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['correo'].required = True

    def clean_nombre(self):
        return self.cleaned_data['nombre'].strip()

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        digitos = ''.join(c for c in telefono if c.isdigit())
        if len(digitos) < 10:
            raise forms.ValidationError('Escribe un teléfono de al menos 10 dígitos.')
        return telefono

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.localdate():
            raise forms.ValidationError('La fecha no puede ser anterior a hoy.')
        if fecha.weekday() == 6:
            raise forms.ValidationError('Los domingos estamos cerrados.')
        return fecha

    def clean(self):
        datos = super().clean()
        barbero, fecha, hora = datos.get('barbero'), datos.get('fecha'), datos.get('hora')
        if barbero and fecha and hora:
            ocupada = Cita.objects.filter(barbero=barbero, fecha=fecha, hora=hora).exclude(estado=Cita.CANCELADA)
            if ocupada.exists():
                raise forms.ValidationError(f'{barbero} ya tiene una cita el {fecha:%d/%m/%Y} a las {hora}. Elige otro horario u otro barbero.')
        return datos


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['nombre', 'servicio', 'calificacion', 'comentario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['servicio'].required = False

    def clean_nombre(self):
        nombre = ' '.join(self.cleaned_data['nombre'].split())
        if len(nombre) < 2:
            raise forms.ValidationError('Escribe tu nombre.')
        return nombre

    def clean_comentario(self):
        texto = self.cleaned_data['comentario'].strip()
        if len(texto) < 10:
            raise forms.ValidationError('Cuéntanos un poco más: tu opinión debe tener al menos 10 caracteres.')
        if re.search(r'https?://|www\.', texto, re.IGNORECASE):
            raise forms.ValidationError('Por seguridad no se permiten enlaces en las reseñas.')
        return texto

from django import forms
from django.utils import timezone
from .models import Evento, Participante
from django.forms import formset_factory

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ej: Conferencia Django 2026',
                'class': 'form-control',
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control',
            }),
            'ubicacion': forms.TextInput(attrs={
                'placeholder': 'Ej: Auditorio Central, Ciudad',
                'class': 'form-control',
            }),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha <= timezone.now().date():
            raise forms.ValidationError("La fecha debe ser futura.")
        return fecha

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre no puede superar 100 caracteres.")
        return nombre


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ej: Juan Pérez',
                'class': 'form-control',
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'Ej: juan@example.com',
                'class': 'form-control',
            }),
        }

class ParticipanteFormClass(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez', 'class': 'form-control'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ej: juan@example.com', 'class': 'form-control'}))

ParticipanteFormSet = formset_factory(ParticipanteFormClass, extra=1)

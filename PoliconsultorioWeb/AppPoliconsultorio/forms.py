from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib import messages

import datetime

from .medicos import lista_medicos
from .especialidades import lista_especialidades
from .pacientes import lista_pacientes
from .models import Paciente

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto:", max_length=5, required=True,
        widget=forms.TextInput(attrs={"class": "special", "id":"44"}))
    apellido = forms.CharField(label="Apellido de contacto", required=True)
    email = forms.EmailField(required=True)

class ConsultaMedicosForm(forms.Form):
    # Definir campos
    especialidad = forms.ChoiceField(choices=lista_especialidades(), required=True, widget=forms.Select)
    medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),

class ConsultaTurnosForm(forms.Form):
    # Definir campos
    def fecha(desde,cuantos_dias):
        if desde == 'h':
            hasta = datetime.date.today() + datetime.timedelta(days=cuantos_dias)
        else:
            pass
        return hasta.strftime('%Y-%m-%d')

    paciente = forms.CharField(label="Paciente:", max_length=8, min_length=6 ,required=False, validators=[RegexValidator(
                '^[0-9]+$',
                message="Debe contener solo números")],
        widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente","size": 12, "title":"Ingrese entre 6 y 8 dígitos de su número de documento"}))
    especialidad = forms.ChoiceField(label=' Especialidad', choices=lista_especialidades(), required=False, widget=forms.Select)
    medico = forms.ChoiceField(label=' Médico', choices=lista_medicos(), required=False, widget=forms.Select)
    fechaDesde = forms.DateField(label=' Fecha Desde',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',0))
    fechaHasta = forms.DateField(label=' Fecha Hasta',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',60))

    def clean_paciente(self):
        data = self.cleaned_data["paciente"]
        print(data)
        if data != '':
            if not Paciente.objects.filter(dni = int(data)).exists():
                raise ValidationError("Debe ingresar un DNI de paciente válido o dejarlo en blanco")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        dataD = cleaned_data.get("fechaDesde")
        dataH = cleaned_data.get("fechaHasta")

        if dataD is not None and dataH is not None and dataD > dataH:
            raise ValidationError("Debe ingresar un rango de fechas correcto, Fecha Desde <= Fechas Hasta")

        return cleaned_data
        
class BajaTurnoForm(forms.Form):
    paciente = forms.CharField(label="DNI Paciente", max_length=15, widget=forms.TextInput(attrs={'class': 'paciente'}), required=False)

class BajaTurnoDetalleForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(label="Horario", required=True)       
    medico = forms.CharField(label=' Médico', widget=forms.TextInput(attrs={'class': 'paciente'}))
    especialidad = forms.CharField(label=' Especialidad')
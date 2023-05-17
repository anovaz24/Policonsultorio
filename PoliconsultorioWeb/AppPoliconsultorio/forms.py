from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib import messages


from .medicos import lista_medicos
from .especialidades import lista_especialidades
from .pacientes import lista_pacientes

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto:", max_length=5, required=True,
        widget=forms.TextInput(attrs={"class": "special", "id":"44"}))
    apellido = forms.CharField(label="Apellido de contacto", required=True)
    email = forms.EmailField(required=True)

class ConsultaMedicosForm(forms.Form): 
    # Definir campos
    # nombre = forms.CharField(label="Nombre", required=True)
    # especialidad = forms.Select(label="Especialidad", required=False)
    #listado_especialidades = lista_especialidades()
    especialidad = forms.ChoiceField(choices=lista_especialidades(), required=True, widget=forms.Select)
    medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),

class ConsultaTurnosForm(forms.Form):
    # Definir campos
    # nombre = forms.CharField(label="Nombre", required=True)
    # especialidad = forms.Select(label="Especialidad", required=False)
    # paciente = forms.ChoiceField(choices=lista_pacientes(), required=False, widget=forms.Select(attrs={"class": "form-control", "id":"paciente"}))
    paciente = forms.CharField(label="DNI Paciente", widget=forms.TextInput(attrs={'class': 'paciente'}), required=False)
    especialidad = forms.ChoiceField(label=' Especialidad', choices=lista_especialidades(), required=False, widget=forms.Select)
    # # medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    medico = forms.ChoiceField(label=' Médico', choices=lista_medicos(), required=False, widget=forms.Select)
    fechaDesde = forms.DateField(label=' Fecha Desde',widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    fechaHasta = forms.DateField(label=' Fecha Hasta',widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    # def clean_fechaDesde(self):
    #     dataD = self.cleaned_data["fechaDesde"]
    #     dataH = self.cleaned_data["fechaHasta"]

    #     if dataD is not None and dataH is not None and dataD > dataH:
    #         raise ValidationError("La Fecha Desde debe ser anterior a la Fecha Hasta")
        
    #     return dataD
    
    def clean(self):
        cleaned_data = super().clean()
        dataD = cleaned_data.get("fechaDesde")
        dataH = cleaned_data.get("fechaHasta")

        print(cleaned_data)
        print(dataD)
        print(dataH)
        if dataD is not None and dataH is not None: print(dataD > dataH)

        if dataD is not None and dataH is not None and dataD > dataH:
            raise ValidationError("La Fecha Desde debe ser anterior a la Fecha Hasta")
        
        return cleaned_data

class BajaTurnoForm(forms.Form):          
    paciente = forms.CharField(label="Paciente:", max_length=15, required=True, 
        validators=[RegexValidator('^[0-9]+$', message="Debe contener sólo números")],
        widget=forms.TextInput(attrs={"class": "form-paciente", "id":"paciente", "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    # medico = forms.CharField(label="Medico:",max_length=15) ,
    # especialidad =forms.CharField(label="Especialidad", disabled="False")
    # , widget=forms.IntegerField(attrs={"hidden": True}) )


class BajaTurnoDetalleForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(label="Horario", required=True)       
    medico = forms.CharField(label=' Médico', widget=forms.TextInput(attrs={'class': 'paciente'}))
    especialidad = forms.CharField(label=' Especialidad')
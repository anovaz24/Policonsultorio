from django import forms
from django.forms.fields import DateField


class AltaTurnoForm2(forms.Form):

    listado_especialidad = (('Z','Seleccione una especialidad'),('Cardiología','Cardiología'),('Dermatología','Dermatología'),('Neurología','Neurología'),('Oftalmología','Oftalmología'),('Pediatría','Pediatría'))

    listado_medicos = (('Z','Seleccione un médico'),
                       ('1','Dr. Juan Pérez (Cardiología)'),
                       ('2','Dra. María González (Dermatología)'),
                       ('3','Dr. Luis Sánchez (Neurología)'),
                       ('4','Dra. Ana Rodríguez (Oftalmología)'),
                       ('5','Dr. Pedro López (Pediatría)'))

    especialidad = forms.ChoiceField(label="especialidadx:",required=False, choices = listado_especialidad,
        widget=forms.Select(attrs={"class": "form-control", "id":"especialidad"}))
    medico = forms.ChoiceField(label="medicox:", required=False, choices = listado_medicos,
        widget=forms.Select(attrs={"class": "form-control", "id":"medico"}))
    fecha = forms.DateField(label="fechax:",required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "id":"fecha",'type': 'date'}))


from django import forms
from .models import Especialidad

def lista_especialidades():
    #listado_especialidad = (('Z','Seleccione una especialidad'),('C','Cardiología'),('D','Dermatología'),('N','Neurología'),('O','Oftalmología'),('P','Pediatría'))
    opciones_especialidades = [('Z', 'Seleccione una especialidad')]
    opciones_especialidades += [(esp.codigo, esp.descripcion) for esp in Especialidad.objects.all()]
    return opciones_especialidades


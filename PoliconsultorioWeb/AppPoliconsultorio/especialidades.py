
from .models import Especialidad

def lista_especialidades():
    # listado_especialidad = (('Z','Seleccione una especialidad'),('C','Cardiología'),('D','Dermatología'),('N','Neurología'),('O','Oftalmología'),('P','Pediatría'))
    especialidades = Especialidad.objects.all().order_by('descripcion')
    listado_especialidad = [('Z','Seleccione una especialidad')]
    for especialidad in especialidades:
        listado_especialidad.append((especialidad.codigo, especialidad.descripcion))
    return listado_especialidad

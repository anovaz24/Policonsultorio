
from .models import Especialidad

def lista_especialidades():
    especialidades = Especialidad.objects.all().order_by('descripcion')
    listado_especialidad = [('Z','Seleccione una especialidad')]
    for especialidad in especialidades:
        listado_especialidad.append((especialidad.codigo, especialidad.descripcion))
    return listado_especialidad 

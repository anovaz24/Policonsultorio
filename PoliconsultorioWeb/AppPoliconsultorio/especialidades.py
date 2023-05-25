from .models import Especialidad

def lista_especialidades():
    opciones_especialidades = [('Z', 'Seleccione una especialidad')]
    opciones_especialidades += [(esp.codigo, esp.descripcion) for esp in Especialidad.objects.all().order_by('descripcion')]
    return opciones_especialidades

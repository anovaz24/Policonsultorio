from .models import Medico

def lista_medicos():
    medicos = Medico.objects.all().order_by('apellido','nombre')
    listado_medicos = [('Z','Seleccione un medico')]
    for medico in medicos:
        listado_medicos.append((medico.id, f"{medico.apellido} {medico.nombre} ({medico.especialidad.descripcion})"))
    return listado_medicos
from .models import Paciente

def lista_pacientes():
    # listado_pacientes = (
    #     ('Z','Seleccione un paciente'),
    #     ('1','María Pérez'),
    #     ('2','José Armand'),
    #     ('3','Rodrigo Spíndola'),
    #     ('4','Pedro Gómez'),
    #     ('5','Mónica Brest')
    #     )
    # return listado_pacientes

    pacientes = Paciente.objects.all().order_by('apellido','nombre')
    listado_pacientes = [('Z','Seleccione un paciente')]

    for paciente in pacientes:
            listado_pacientes.append((paciente.dni, f"{paciente.apellido} {paciente.nombre} "))
          
    return listado_pacientes 
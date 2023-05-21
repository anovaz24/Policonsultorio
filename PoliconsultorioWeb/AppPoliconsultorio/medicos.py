from .models import Medico

def lista_medicos():
    # listado_medicos = (('Z','Seleccione un médico'),
    #                    ('1','Dr. Juan Pérez (Cardiología)'),
    #                    ('2','Dra. María González (Dermatología)'),
    #                    ('3','Dr. Luis Sánchez (Neurología)'),
    #                    ('4','Dra. Ana Rodríguez (Oftalmología)'),
    #                    ('5','Dr. Pedro López (Pediatría)'))
    medicos = Medico.objects.all().order_by('apellido','nombre')
    listado_medicos = [('Z','Seleccione un medico')]
    for medico in medicos:
        listado_medicos.append((medico.id, f"{medico.apellido} {medico.nombre} ({medico.especialidad.descripcion})"))
    return listado_medicos

def lista_completa_medicos():
    listado_medicos = [{'ID':'1','nombre':'Dr. Juan Pérez (Cardiología)','Especialidad':'Cardiología'},
                       {'ID':'2','nombre':'Dra. María González (Dermatología)','Especialidad':'Dermatología'},
                       {'ID':'3','nombre':'Dr. Luis Sánchez (Neurología)','Especialidad':'Neurología'},
                       {'ID':'4','nombre':'Dra. Ana Rodríguez (Oftalmología)','Especialidad':'Oftalmología'},
                       {'ID':'5','nombre':'Dr. Pedro López (Pediatría)','Especialidad':'Pediatría'}
                       ]    
    return listado_medicos
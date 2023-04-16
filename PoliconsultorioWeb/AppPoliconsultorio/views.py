from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hola a todos")

def index2(request):
    return HttpResponse("Probando git")


def turno_medico(request):

    listado_especialidad = ['Cardiología','Dermatología',
        'Neurología','Oftalmología','Pediatría']

    listado_medicos = [{'ID':'1','nombre':'Dr. Juan Pérez (Cardiología)','Especialidad':'Cardiología'},
                       {'ID':'2','nombre':'Dra. María González (Dermatología)','Especialidad':'Dermatología'},
                       {'ID':'3','nombre':'Dr. Luis Sánchez (Neurología)','Especialidad':'Neurología'},
                       {'ID':'4','nombre':'Dra. Ana Rodríguez (Oftalmología)','Especialidad':'Oftalmología'},
                       {'ID':'5','nombre':'Dr. Pedro López (Pediatría)','Especialidad':'Pediatría'}
                       ]    

    listado_disp_medicos = [{'ID':'1',
                             'horario':'8:00 a 9:00',
                             'descr_disponible':'Disponible',
                             'flag':'enabled',
                             },
                            {'ID':'2',
                            'horario':'9:00 a 10:00',
                            'descr_disponible':'No disponible',
                            'flag':'disabled',
                            },
                            {'ID':'3',
                             'horario':'10:00 a 11:00',
                             'descr_disponible':'Disponible',
                             'flag':'enabled',
                             }]

    context = {
        "listado_especialidad":listado_especialidad,
        "listado_medicos":listado_medicos,
        "listado_disp_medicos":listado_disp_medicos
    }
    return render(request,"AppPoliconsultorio/turnos.html",context)

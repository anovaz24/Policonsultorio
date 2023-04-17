from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
def index(request):
    return HttpResponse("Hola")

def index(request):
    context = {}
    return render (request,"AppPoliconsultorio/index.html", context)


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

def especialidades(request):
    context ={}
    return render (request,"AppPoliconsultorio/especialidades.html", context)

def usuarios(request):
    context ={}
    return render (request,"AppPoliconsultorio/usuarios.html", context)


def contactenos(request):
    context ={}
    return render (request,"AppPoliconsultorio/contactenos.html", context)

def acerca(request):
    context ={}
    return render (request,"AppPoliconsultorio/acerca.html", context)

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .medicos import lista_medicos

# Create your views here.
def index(request):
    
    # Listar todos los turnos del día
    turno = {
        'dia': '20/04/2023',
        'hora': '09:00',
        'medico': 'Dr. Juan Perez',
        'especialidad': 'Cardiología',
        'paciente': 'Adriana Cullen',
    }

    listado_turnos = [
        {
            'dia': '20/04/2023',
            'hora': '09:00',
            'medico': 'Dr. Juan Pérez',
            'especialidad': 'Cardiología',
            'paciente': 'Adriana Cullen',
        },
        {
            'dia': '20/04/2023',
            'hora': '09:00',
            'medico': 'Dra. María González',
            'especialidad': 'Dermatología',
            'paciente': 'José Olleros',
        },
        {
            'dia': '20/04/2023',
            'hora': '11:00',
            'medico': 'Dr. Juan Perez',
            'especialidad': 'Cardiología',
            'paciente': 'Mariano Burgos',
        },
    ]

    context = {
        "hoy": datetime.now,
        "dia": "18/04/2023",
        "turno": turno,
        "listado_turnos": listado_turnos,
        }
    return render(request, "AppPoliconsultorio/index.html", context)

def turno_medico(request):

    listado_especialidad = ['Cardiología','Dermatología',
        'Neurología','Oftalmología','Pediatría']

    listado_medicos = lista_medicos()    

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
        "listado_disp_medicos":listado_disp_medicos,
    }
    return render(request,"AppPoliconsultorio/turnos.html",context)

def consulta_medicos(request):
    # Listar todos los médicos
    listado_medicos = lista_medicos()

    context = {
        "listado_medicos": listado_medicos
    }
    return render(request, "AppPoliconsultorio/consulta_medicos.html", context)

def alta_medico(request):
    # Alta de un Médico
    context = {}
    return render(request, "AppPoliconsultorio/alta_medico.html", context)

def baja_medico(request):
    # Baja de un Médico
    context = {}
    return render(request, "AppPoliconsultorio/baja_medico.html", context)

def especialidades(request):
    context = {}
    return render (request,"AppPoliconsultorio/especialidades.html", context)

def usuarios(request):
    context = {}
    return render (request,"AppPoliconsultorio/usuarios.html", context)


def contactenos(request):
    context = {}
    return render (request,"AppPoliconsultorio/contactenos.html", context)

def acerca(request):
    context = {}
    return render (request,"AppPoliconsultorio/acerca.html", context)

def turnos(request):
    context = {}
    return render (request,"AppPoliconsultorio/turnos.html", context)

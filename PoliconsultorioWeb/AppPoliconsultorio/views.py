from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect,HttpRequest
from django.contrib import messages
from django.db.models import Q

from .forms import *
from .models import Especialidad, Paciente, Medico, Turno
from .turno import *
from .especialidades import lista_especialidades
from .medicos import lista_medicos

# Create your views here.
def index(request):
    context = {}
    return render(request, "AppPoliconsultorio/index.html", context)

def turno_medico(request):

    listado_especialidad = lista_especialidades()

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

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        alta_turno_form = AltaTurnoForm(request.POST)
        # Valido y proceso los datos.
        if alta_turno_form.is_valid():
            if alta_turno_form.cleaned_data['fecha'] is None or alta_turno_form.cleaned_data['especialidad'] == 'Z' or alta_turno_form.cleaned_data['medico'] == 'Z':
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                # Le voy a cambiar a uno de los datos algo
                paciente = 'Mabel Gandulfo'
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
                messages.add_message(request, messages.WARNING, 'Debe elegir una Especialidad, Médico y fecha!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente})
                #Redirect to a new url:
                #return HttpResponseRedirect('/AppPoliconsultorio/turno_medico/')
                #Poner el mensaje falta elegir la fecha

            if alta_turno_form.cleaned_data['fecha'] is not None and request.POST.get("horario") is None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #print(request.POST)
                print('horario: ',request.POST.get("horario"))
                paciente = 'Mabel Gandulfox'
                messages.add_message(request, messages.WARNING, 'Debe elegir un horario!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar','','','')})
            #else:
                #Poner el mensaje falta elegir el turno

            if request.POST.get("horario") is not None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                paciente = 'Mabel Gandulfoz'
                print('registro el alta del turno')
                funcion_de_guardado_de_turno('actualizar',request.POST.get("horario"),'No disponible','disabled')
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente})
                return render(request,"AppPoliconsultorio/thanks.html")  
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
        else:
            #messages.add_message(request, messages.WARNING, alta_turno_form.errors, extra_tags="tag1")
            #print(alta_turno_form.errors)
            error_paciente = alta_turno_form.errors
            alta_turno_form = AltaTurnoForm()
            return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'error_paciente' : error_paciente})

    else:
        # Creo el formulario vacío con los valores por defecto
        alta_turno_form = AltaTurnoForm()
    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form })
    #return render(request,"AppPoliconsultorio/turnos.html",context)

def turno_consulta(request):
    listado_turnos = []
    errores = []
    
    if request.method == "POST":
        turno_consulta_form = ConsultaTurnosForm(request.POST)
        if turno_consulta_form.is_valid():
            filtro_paciente = ""
            filtro_especialidad = ""
            filtro_medico = ""
            filtro_fechaDesde = ""
            filtro_fechaHasta = ""

            # Filtro por Paciente
            paciente_form = request.POST['paciente']
            if paciente_form != '':
                paciente = Paciente.objects.filter(dni = paciente_form)
                filtro_paciente = paciente[0].dni
                # listado_turnos = Turno.objects.filter(paciente = dni)

            # Filtro por Especialidad
            especialidad_form = request.POST['especialidad']
            if especialidad_form != 'Z':
                filtro_especialidad = especialidad_form

            # Filtro por Medico
            medico_form = request.POST['medico']
            if medico_form != 'Z':
                filtro_medico = int(medico_form)

            # Filtro por Fechas
            filtro_fechaDesde = request.POST['fechaDesde']
            filtro_fechaHasta = request.POST['fechaHasta']

            listado_turnos = lista_turnos(filtro_paciente, filtro_especialidad, filtro_medico, filtro_fechaDesde, filtro_fechaHasta)

            # if listado_turnos is None:
            #     turno_consulta_form.errors[]
        else:
            errores = turno_consulta_form.errors
            print("errores: ",errores)
            print("request: ",request)
            for error in errores:
                print("error: ",error)
            if errores is None:
                print(turno_consulta_form.non_field_errors)
                # messages.add_message(request, messages.WARNING, 'Debe ingresar un rango de fechas correcto, Fecha Desde <= Fecha Hasta', extra_tags="tag1")
    else:
        turno_consulta_form = ConsultaTurnosForm()

    context = {
        "listado_turnos": listado_turnos,
        "turno_consulta_form": turno_consulta_form,
        "errores": errores,
    }
    return render(request, "AppPoliconsultorio/turno_consulta.html", context)

def baja_turno(request):
    turnos_otorgados = [
        {
            'dia': '08/05/2023',
            'hora': '09:00',
            'medico': 'Dr. Juan Pérez',
            'especialidad': 'Cardiología',
            'paciente': 'Adriana Cullen',
        },
        {
            'dia': '15/05/2023',
            'hora': '09:00',
            'medico': 'Dra. María González',
            'especialidad': 'Dermatología',
            'paciente': 'José Olleros',
        },
        {
            'dia': '17/06/2023',
            'hora': '11:00',
            'medico': 'Dr. Juan Perez',
            'especialidad': 'Cardiología',
            'paciente': 'Mariano Burgos',
        },
    ]

    context = {
        'nombre': 'ninguno',
        'turnos': turnos_otorgados,
        'paciente': request.POST.get("paciente")
        
   }    
    
    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        bajaturno_form = BajaTurnoForm(request.POST)
      
        if request.POST.get("paciente") is None:   
           print ('ingreso al if')                   
           messages.add_message(request, messages.WARNING, 'Debe ingresar un paciente', extra_tags="tag1")
        return render(request, "AppPoliconsultorio/baja_turno.html", context) 
    
      
        # Valido y proceso los datos.
               
        if bajaturno_form.is_valid():              
           
           return render(request, "AppPoliconsultorio/baja_turno.html", context)      
    else:
            # Creo el formulario vacío con los valores por defecto
        bajaturno_form = BajaTurnoForm()
    return render(request, "AppPoliconsultorio/baja_turno.html", {'bajaturno_form': bajaturno_form })

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

def contacto(request):
    if request.method == "POST":
    # Creo la instancia del formulario con los datos cargados en pantalla
        contacto_form = ContactoForm(request.POST)
        # Valido y proceso los datos.
        if contacto_form.is_valid():
            #Process the data in form.cleaned_data as required # ...
            # De esta manera veo los datos que fueron completados en el formulario
            print('Nombre: ',contacto_form.cleaned_data['nombre'])
            print('Apellido: ',contacto_form.cleaned_data['apellido'])
            print('Email: ',contacto_form.cleaned_data['email'])
            #Redirect to a new url:
            return HttpResponseRedirect('/AppPoliconsultorio/thanks/')
    else:
        # Creo el formulario vacío con los valores por defecto
        contacto_form = ContactoForm()
    return render(request, "AppPoliconsultorio/contacto.html", {'contacto_form': contacto_form})
    
def thanks(request): #new
    context = {}
    return render(request,"AppPoliconsultorio/thanks.html",context)

def turnos(request):
    context = {}
    return render (request,"AppPoliconsultorio/turnos.html", context)

def consulta_medicos(request):
    # Prepara los combos
    listado_especialidad = lista_especialidades()
    listado_medicos = lista_medicos()

    if request.method == "POST":
        consulta_medicos_form = ConsultaMedicosForm(request.POST)
    else:
        consulta_medicos_form = ConsultaMedicosForm()

    context = {
        "listado_especialidad": listado_especialidad,
        "listado_medicos": listado_medicos,
        "form": consulta_medicos_form,
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

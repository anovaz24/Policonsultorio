from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages

from .forms import *
from .turno import *
from .especialidades import lista_especialidades
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

    listado_turnos = lista_turnos()

    context = {
        "hoy": datetime.now,
        "dia": "18/04/2023",
        "turno": turno,
        "listado_turnos": listado_turnos,
        }
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
    
    if request.method == "POST":
        turno_consulta_form = ConsultaTurnosForm(request.POST)
        if turno_consulta_form.is_valid():
            listado_turnos = lista_turnos()
        else:
            print(turno_consulta_form.cleaned_data['fechaDesde'])
            messages.add_message(request, messages.WARNING, 'Debe ingresar un rango de fechas correcto, Fecha Desde <= Fechas Hasta', extra_tags="tag1")
            print(request)
    else:
        turno_consulta_form = ConsultaTurnosForm()

    context = {
        "listado_turnos": listado_turnos,
        "turno_consulta_form": turno_consulta_form,
    }
    return render(request, "AppPoliconsultorio/turno_consulta.html", context)

    
def baja_turno(request):
    listado_turnos = []
    
    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        bajaturno_form = BajaTurnoForm(request.POST)
      
        if bajaturno_form.is_valid():
            # id_turno = bajaturno_form.cleaned_data['ID'] 
            listado_turnos = lista_turnos()
            print("entro por is valid")
            print(request.POST)
            print (request.POST.get("selectbajaturno"))
            print ("xx", request.POST.get("xx.medico"))
            
            if request.POST.get("selectbajaturno") is None :                 
                print("entro selectbaja turno es vacio")
                messages.add_message(request, messages.WARNING, 'Debe ingresar un turno para dar de baja', extra_tags="tag1")

                
            
            else:  
                print("pasa por select baja turno , hay uno seleccionado")
                seleccionado = request.POST.get("selectbajaturno")

                print ("seleccionado2:", listado_turnos)
             
              

        #     else (si esta lleno)
        #         evaluar si hay alguno seleccionado  -> si no, mensaje de error
        #          evaluar cual es que esta seleccionado --> eliminarlo
           
        #    en el html subir la grilla adntro del form
                 
    else:
        #GET
            # Creo el formulario vacío con los valores por defecto
        bajaturno_form = BajaTurnoForm()    
             
    context = {
            'turnos': listado_turnos,
            'paciente': request.POST.get("paciente"),
            'bajaturno_form': bajaturno_form
        }   

    return render(request, "AppPoliconsultorio/baja_turno.html", context)

    #return HttpResponseRedirect('/AppPoliconsultorio/thanks/')






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

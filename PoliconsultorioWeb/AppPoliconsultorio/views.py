from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect,HttpRequest
from django.contrib import messages
from django.db.models import Q

from .forms import *
from .models import Especialidad, Paciente, Medico, Turno
from .turno import *
from .especialidades import lista_especialidades
from .pacientes import lista_pacientes
from .medicos import lista_medicos
from .models import *

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
    listado_turnos = []
    errores = []

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        bajaturno_form = BajaTurnoForm(request.POST)
      
        if bajaturno_form.is_valid():
            dni = int(request.POST['dni'])    
            # id = int(request.POST['id'])    
            pacientes = Paciente.objects.filter(dni=dni)
            turnos_tabla = Turno.objects.filter(paciente=dni )
            # turnos_tabla = Turno.objects.all(id=id)
            # turnos_tabla = Turno.objects.filter()
            nombre = pacientes[0].nombre
            apellido= pacientes[0].apellido
            nombre_completo = f"{ apellido}, {nombre}"
            id = turnos_tabla[0].id
            print ('nombre completo1: ', nombre_completo)
            # aca genero el listado_turnos: gte= mayor o igual a hoy                        
            listado_turnos = Turno.objects.filter(fecha__gte=date.today(), paciente=dni).order_by('fecha')
            
            print ('nombre completo3: ', nombre_completo)
            print ('id ', id)          

            return render(request, "AppPoliconsultorio/baja_turno.html", {'bajaturno_form': bajaturno_form, 'pacientel': nombre_completo, 'listado_turnos': listado_turnos  })
        #     redireccionar 

           

    else: 
                
        bajaturno_form = BajaTurnoForm()
 
    context = {
        "listado_turnos": listado_turnos,
        "bajaturno_form": BajaTurnoForm,
        "errores": errores,
    }
    return render(request, "AppPoliconsultorio/baja_turno.html", context)

    #return HttpResponseRedirect('/AppPoliconsultorio/thanks/')

def eliminar_turno(request, id):
    turno = Turno.objects.get(id=id)
    print('encontrre el turno a eliminar' , turno)

    turno.delete()

    # return redirect('/')

    return render(request, 'Apppoliconsultorio/baja_turnos.html')  

# print('id turno despues del return ' , dni )


def listar_turnos(request):
    context = {}

    listado = Turno.objects.all()

    context['listado_turnos'] = listado
    return render(request, 'Apppoliconsultorio/listar_turnos.html', context)  


def listar_pacientes(request):
    context = {}

    listado = Paciente.objects.all()

    context['listar_pacientes'] = listado
    return render(request, 'Apppoliconsultorio/listar_pacientes.html', context) 


def listar_especialidad(request):
    context = {}

    listado = Especialidad.objects.all()

    context['lista_especialidades'] = listado
    return render (request,"AppPoliconsultorio/listar_especialidad.html", context)
    
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

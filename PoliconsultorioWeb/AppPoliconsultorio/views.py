from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages

from .forms import *
from .especialidades import lista_especialidades
from .medicos import lista_medicos
from .models import Paciente

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

    #listado_turnos = lista_turnos()  # 20-05

    context = {
        "hoy": datetime.date.today(),
        "dia": "18/04/2023",
        "turno": turno,
        #"listado_turnos": listado_turnos, #  20-05
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

    paciente_ya_se_valido = False
    buscar_turnos_ya_se_valido = False
    especialidad_ya_se_valido = True
    #estado_boton_buscar_turnos = 'disabled'
    #estado_boton_guardar_turno = 'disabled'

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        print("en el post la especialidad vuelve: ",request.POST['especialidad'])
        print("en el post la fecha vuelve: ",request.POST['fecha'])
        if request.POST['especialidad'] != 'Z':
            alta_turno_form = AltaTurnoForm(request.POST, especialidad=request.POST['especialidad'])
        if request.POST['especialidad'] == 'Z':
            alta_turno_form = AltaTurnoForm(request.POST)

        # Valido y proceso los datos.
        print(request.POST)

        if alta_turno_form.is_valid():
            if 'validar_paciente' in request.POST:
                #paciente = request.POST.get('paciente', None)
                paciente_consulto_su_existencia = Paciente.buscar_por_dni(request.POST.get('paciente', None))
                #if paciente == '11111111':
                if paciente_consulto_su_existencia != 'No-existe':
                    #paciente = 'Julia Zenko'
                    paciente = paciente_consulto_su_existencia
                    alta_turno_form.fields['paciente'].widget.attrs['readonly'] = True
                    alta_turno_form.fields['paciente'].widget.attrs['disabled'] = True
                    if request.POST.get('validar_paciente') == 'Paciente validado':
                        paciente_ya_se_valido = True
                    print('es el valor que le veo al boton de paciente antes del cambio: ',request.POST.get('validar_paciente'))
                    request.POST = request.POST.copy()
                    request.POST['validar_paciente'] = 'disabled'
                    #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                    print('es el valor que le veo al boton de paciente: ',request.POST.get('validar_paciente'))
                    if paciente_ya_se_valido == False:
                        return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})
                else:
                    #return HttpResponse('Paciente no válido')
                    messages.add_message(request, messages.WARNING, 'Paciente Inexistente', extra_tags="tag1")
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})

            # Nuevo para especialidad
            if alta_turno_form.cleaned_data['especialidad'] == 'Z':
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                # Le voy a cambiar a uno de los datos algo
                #paciente = 'Mabel Gandulfo' # luego comentar ya que lo va a seguir...
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
                messages.add_message(request, messages.WARNING, 'Debe elegir una Especialidad!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
                #Redirect to a new url:
                #return HttpResponseRedirect('/AppPoliconsultorio/turno_medico/')
                #Poner el mensaje falta elegir la fecha
            else:
                #Poner el mensaje falta elegir el turno
                #Hacer todo aqui porque si esta bien ok :)
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                print(request.POST)
                print('horario: ',request.POST.get("horario"))                
                alta_turno_form.fields['especialidad'].widget.attrs['readonly'] = True
                alta_turno_form.fields['especialidad'].widget.attrs['disabled'] = True
                if request.POST.get('validar_especialidad') != 'Especialidad validada':
                    especialidad_ya_se_valido = True
                if request.POST.get('validar_especialidad') == 'Especialidad validada':
                    especialidad_ya_se_valido = False
                print('es el valor que le veo al boton de validar la epecialidad antes del cambio: ',request.POST.get('validar_especialidad'))
                request.POST = request.POST.copy()
                request.POST['validar_especialidad'] = 'disabled'
                #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                print('es el valor que le veo al boton de validar la especialidad: ',request.POST.get('validar_especialidad'))
                if especialidad_ya_se_valido != False:
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'enabled',  'estado_boton_guardar_turno': 'disabled'})
                #no se si poner un else aqui...

            # Fin nuevo para especialidad

            if alta_turno_form.cleaned_data['fecha'] is None or alta_turno_form.cleaned_data['medico'] == 'Z':
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                # Le voy a cambiar a uno de los datos algo
                #paciente = 'Mabel Gandulfo' # luego comentar ya que lo va a seguir...
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
                messages.add_message(request, messages.WARNING, 'Debe elegir un Médico y fecha!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_guardar_turno': 'disabled' })
                #Redirect to a new url:
                #return HttpResponseRedirect('/AppPoliconsultorio/turno_medico/')
                #Poner el mensaje falta elegir la fecha
            else:
                #Poner el mensaje falta elegir el turno
                #Hacer todo aqui porque si esta bien ok :)
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #print(request.POST)
                print('horario: ',request.POST.get("horario"))                
                alta_turno_form.fields['medico'].widget.attrs['readonly'] = True
                alta_turno_form.fields['medico'].widget.attrs['disabled'] = True
                alta_turno_form.fields['fecha'].widget.attrs['readonly'] = True
                alta_turno_form.fields['fecha'].widget.attrs['disabled'] = True  
                if request.POST.get('buscar_turnos') == 'busqueda validada':
                    buscar_turnos_ya_se_valido = True
                print('es el valor que le veo al boton de buscar turno antes del cambio: ',request.POST.get('buscar_turnos'))
                request.POST = request.POST.copy()
                request.POST['buscar_turnos'] = 'disabled'
                #alta_turno_form.fields['validar_paciente'].widget.attrs['disabled'] = True
                print('es el valor que le veo al boton de buscar turnos: ',request.POST.get('buscar_turnos'))
                if buscar_turnos_ya_se_valido == False:
                    print("el medico tiene el valor: ",alta_turno_form.cleaned_data['medico'])
                    #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar','','',''),'estado_boton_guardar_turno': 'enabled'})
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''),'estado_boton_guardar_turno': 'enabled'})
                #no se si poner un else aqui...


            if alta_turno_form.cleaned_data['fecha'] is not None and request.POST.get("horario") is None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #print(request.POST)
                print('horario: ',request.POST.get("horario"))
                #paciente = 'Mabel Gandulfox'
                messages.add_message(request, messages.WARNING, 'Debe elegir un horario!', extra_tags="tag1")
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar','','','')})
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''), 'estado_boton_guardar_turno': 'enabled'})


            if request.POST.get("horario") is not None:
                print('Paciente: ',alta_turno_form.cleaned_data['paciente'])
                print('Especialidad: ',alta_turno_form.cleaned_data['especialidad'])
                print('Medico: ',alta_turno_form.cleaned_data['medico'])
                print('Fecha: ',alta_turno_form.cleaned_data['fecha'])
                print('horario: ',request.POST.get("horario"))
                #print('seleccion_turno: ',alta_turno_form3.cleaned_data['seleccion_turno'])
                #paciente = 'Mabel Gandulfoz'
                print('registro el alta del turno')
                funcion_de_guardado_de_turno('actualizar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],request.POST.get("horario"))
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente})
                return render(request,"AppPoliconsultorio/thanks.html")  
                #return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'alta_turno_form2': alta_turno_form2, 'alta_turno_form3': alta_turno_form3, 'paciente': paciente, 'listado_disp_medicos': listado_disp_medicos})
        else:
            #messages.add_message(request, messages.WARNING, alta_turno_form.errors, extra_tags="tag1")
            #print(alta_turno_form.errors)
            error_formulario = alta_turno_form.errors
            print('el error que viene de validar form: ',error_formulario)
            if 'paciente' in error_formulario:
                #alta_turno_form = AltaTurnoForm() # lo comente porque estoy pasandolo al fomr... 13-05-2023
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'error_formulario' : error_formulario, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
            if 'fecha' in error_formulario:
                paciente = Paciente.buscar_por_dni(request.POST.get('paciente', None))
                #paciente = 'Julia Zenko'
                #especialidad = 'D'  #falta ubicar el valor...
                alta_turno_form.fields['paciente'].widget.attrs['disabled'] = True
                alta_turno_form.fields['especialidad'].widget.attrs['disabled'] = True
                request.POST = request.POST.copy()
                request.POST['validar_paciente'] = 'disabled'
                request.POST['validar_especialidad'] = 'disabled'
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'error_formulario' : error_formulario, 'estado_boton_buscar_turnos': 'enabled', 'estado_boton_guardar_turno': 'disabled' })

    else:
        # Creo el formulario vacío con los valores por defecto
        alta_turno_form = AltaTurnoForm()
    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'estado_boton_buscar_medicos': 'disabled' ,'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
    #return render(request,"AppPoliconsultorio/turnos.html",context)

def turno_consulta(request):
    listado_turnos = []
    
    if request.method == "POST":
        turno_consulta_form = ConsultaTurnosForm(request.POST)
        if turno_consulta_form.is_valid():
            listado_turnos = lista_turnos()
            #return render(request, "AppPoliconsultorio/turno_consulta.html", {'turno_consulta_form': turno_consulta_form })
        else:
            print(turno_consulta_form.cleaned_data['fechaDesde'])
            #messages.add_message(request, messages.WARNING, 'Debe ingresar un rango de fechas correcto, Fecha Desde <= Fechas Hasta', extra_tags="tag1")
            return render(request, "AppPoliconsultorio/turno_consulta.html", {'turno_consulta_form': turno_consulta_form })
            #print(request)
    else:
        turno_consulta_form = ConsultaTurnosForm()

    context = {
        "listado_turnos": listado_turnos,
        "turno_consulta_form": turno_consulta_form,
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

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group

from .forms import *
from .models import *


# Create your views here.
def index(request):
    context = {}
    return render(request, "AppPoliconsultorio/index.html", context)


def acerca(request):
    context = {}
    return render (request,"AppPoliconsultorio/acerca.html", context)


def especialidades(request):
    context = {}
    return render (request,"AppPoliconsultorio/especialidades.html", context)


def listar_especialidad(request):
    context = {}

    listado = Especialidad.objects.all()

    context['lista_especialidades'] = listado
    return render (request,"AppPoliconsultorio/listar_especialidad.html", context)


@permission_required('AppPoliconsultorio.add_medico')
def alta_medico(request):
    # Alta de un Médico
    context = {}
    if request.method == 'POST':
        form = AltaMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Médico incorporado con éxito')
            return redirect('listar_medicos')
    else:
        form = AltaMedicoForm()

    context['form'] = form
    return render(request, "AppPoliconsultorio/alta_medico.html", context)


@login_required
def baja_medico(request):
    # Baja de un Médico
    context = {}
    # En Construcción
    #
    # if request.method == 'POST':
    #     form = BajaMedicoForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.add_message(request, messages.SUCCESS, 'Médico Eliminado del plantel')
    #         return redirect('listar_medicos')
    # else:
    #     form = BajaMedicoForm()

    # context['form'] = form
    return render(request, "AppPoliconsultorio/baja_medico.html", context)


@login_required
def consulta_medicos(request):
    # Prepara los combos
    listado_especialidad = Especialidad.lista_especialidades()
    listado_medicos = Medico.lista_medicos()

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


class listar_medicos(ListView):
    model = Medico
    context_object_name = "medicos"
    template_name = "AppPoliconsultorio\listar_medicos.html"
    ordering = ['apellido', 'nombre']

@login_required
def listar_medicos_por_especialidad(request,cod_especialidad):
    context = {}
    print('El cod_especialidad ingresado es: ',cod_especialidad)

    try:
        especialidad_ob = Especialidad.objects.get(codigo=cod_especialidad)
        print('El id del objeto es: ',especialidad_ob.pk)
        #especialidad_elegida = Especialidad.objects.filter()
        medicos = Medico.objects.filter(especialidad=especialidad_ob)

        #id_especialidad = Especialidad.objects.filter(codigo=cod_especialidad)

        listado_medicos = []

        for medico in medicos:
            print(medico.nombre_completo+' ('+medico.especialidad.descripcion+')')
            listado_medicos.append(medico.nombre_completo+' ('+medico.especialidad.descripcion+')')
        #return listado_medicos 
        #listado = Paciente.objects.all()

        context['listado_medicos'] = listado_medicos
        return render(request, 'Apppoliconsultorio/listar_medicos_por_especialidad.html', context) 
    except:
        listado_medicos = []
        context['listado_medicos'] = listado_medicos
        return render(request, 'Apppoliconsultorio/listar_medicos_por_especialidad.html', context)


@login_required
def alta_paciente(request):
    # Alta de un Paciente
    context = {}
    return render(request, "AppPoliconsultorio/alta_paciente.html", context)


@login_required
def baja_paciente(request):
    # Baja de un Médico
    context = {}
    return render(request, "AppPoliconsultorio/baja_paciente.html", context)


@login_required
def consulta_pacientes(request):
    # Prepara los combos
    listado_pacientes = Paciente.lista_pacientes()

    if request.method == "POST":
        consulta_pacientes_form = ConsultaPacientesForm(request.POST)
    else:
        consulta_pacientes_form = ConsultaPacientesForm()

    context = {
        "listado_pacientes": listado_pacientes,
        "form": consulta_pacientes_form,
    }
    return render(request, "AppPoliconsultorio/consulta_pacientes.html", context)
# **********************************************************************************

def consulta_pacientes_estaba_este(request):
    context = {}

    listado_pacientes = Paciente.objects.all()
    
    if request.method == "POST":
        # consulta_pacientes_form = ConsultaPacientesForm(request.POST)
        # paciente = Paciente.buscar_por_dni(request.POST.get('paciente', None))
        paciente = Paciente.buscar_paciente_completo_por_dni(request.POST.get('paciente', None))
        if consulta_pacientes_form.is_valid():
            
            dni = int(request.POST['dni'])
            listado_pacientes = Paciente.objects.filter(paciente=dni).oder_by('apellido','nombre')
            # consulta_pacientes_form = ConsultaPacientesForm()
            return render(request, "AppPoliconsultorio/consulta_pacientes.html", {'consulta_pacientes_form': consulta_pacientes_form, 'pacientes': listado_pacientes  })
    else:
        consulta_pacientes_form = ConsultaPacientesForm()   
    
    context ={
         "paciente": listado_pacientes,
        
        }
    return render(request, "AppPoliconsultorio/consulta_pacientes.html", context)
# **********************************************************************************     
def consulta_pacientes(request):  
        listado_turnos = []
        errores = []

        if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
            conspac_form = ConsultaPacientesForm(request.POST)
        
            if conspac_form.is_valid():
                dni = int(request.POST['dni'])    
                # seleccionado = (request.POST.get('selectbajaturno'))   
                if dni is None :    
                # pacientes = Paciente.objects.filter(dni=dni)
                #     turnos_tabla = Turno.objects.filter(paciente=dni )                
                #     nombre = pacientes[0].nombre
                #     apellido= pacientes[0].apellido
                #     nombre_completo = f"{ apellido}, {nombre}"
                #     id = turnos_tabla[0].id
                #     # aca genero el listado_turnos: gte= mayor o igual a hoy                        
                #     listado_turnos = Turno.objects.filter(fecha__gte=date.today(), paciente=dni).order_by('fecha')
                # print("dni", dni)
                    return render(request, "AppPoliconsultorio/consulta_pacientes.html", {'conspac_form': conspac_form  })
            else:
                paciente = Paciente.objects.filter(id=dni)
           
        else:                 
            conspac_form = ConsultaPacientesForm()
 
        context = {
           
            "conspac_form": ConsultaPacientesForm,
            "errores": errores,
    }
        
        return render(request, "AppPoliconsultorio/consulta_pacientes.html", context)
   
# **********************************************************************************
def listar_pacientes(request):
    context = {}

    listado = Paciente.objects.all()

    context['listar_pacientes'] = listado
    return render(request, 'Apppoliconsultorio/listar_pacientes.html', context) 


@permission_required(['AppPoliconsultorio.change_turno','AppPoliconsultorio.delete_turno'])
def turno_medico(request):

    listado_especialidad = Especialidad.lista_especialidades()

    listado_medicos = Medico.lista_medicos()

    listado_disp_medicos = []

    context = {
        "listado_especialidad":listado_especialidad,
        "listado_medicos":listado_medicos,
        "listado_disp_medicos":listado_disp_medicos,
    }

    paciente_ya_se_valido = False
    buscar_turnos_ya_se_valido = False
    especialidad_ya_se_valido = True

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        if request.POST['especialidad'] != 'Z':
            alta_turno_form = AltaTurnoForm(request.POST, especialidad=request.POST['especialidad'])
        if request.POST['especialidad'] == 'Z':
            alta_turno_form = AltaTurnoForm(request.POST)

        # Valido y proceso los datos.
        if alta_turno_form.is_valid():
            if 'validar_paciente' in request.POST:
                paciente_consulto_su_existencia = Paciente.buscar_por_dni(request.POST.get('paciente', None))
                if paciente_consulto_su_existencia != 'No-existe':
                    paciente = paciente_consulto_su_existencia
                    alta_turno_form.fields['paciente'].widget.attrs['readonly'] = True
                    alta_turno_form.fields['paciente'].widget.attrs['disabled'] = True
                    if request.POST.get('validar_paciente') == 'Paciente validado':
                        paciente_ya_se_valido = True
                    request.POST = request.POST.copy()
                    request.POST['validar_paciente'] = 'disabled'
                    if paciente_ya_se_valido == False:
                        return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})
                else:
                    messages.add_message(request, messages.WARNING, 'Paciente Inexistente', extra_tags="tag1")
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled'})

            # Nuevo para especialidad
            if alta_turno_form.cleaned_data['especialidad'] == 'Z':
                messages.add_message(request, messages.WARNING, 'Debe elegir una Especialidad!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
            else:
                alta_turno_form.fields['especialidad'].widget.attrs['readonly'] = True
                alta_turno_form.fields['especialidad'].widget.attrs['disabled'] = True
                if request.POST.get('validar_especialidad') != 'Especialidad validada':
                    especialidad_ya_se_valido = True
                if request.POST.get('validar_especialidad') == 'Especialidad validada':
                    especialidad_ya_se_valido = False
                request.POST = request.POST.copy()
                request.POST['validar_especialidad'] = 'disabled'
                if especialidad_ya_se_valido != False:
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_buscar_turnos': 'enabled',  'estado_boton_guardar_turno': 'disabled'})
            # Fin nuevo para especialidad

            if alta_turno_form.cleaned_data['fecha'] is None or alta_turno_form.cleaned_data['medico'] == 'Z':
                messages.add_message(request, messages.WARNING, 'Debe elegir un Médico y fecha!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, 'estado_boton_guardar_turno': 'disabled' })
            else:
                alta_turno_form.fields['medico'].widget.attrs['readonly'] = True
                alta_turno_form.fields['medico'].widget.attrs['disabled'] = True
                alta_turno_form.fields['fecha'].widget.attrs['readonly'] = True
                alta_turno_form.fields['fecha'].widget.attrs['disabled'] = True  
                if request.POST.get('buscar_turnos') == 'busqueda validada':
                    buscar_turnos_ya_se_valido = True
                request.POST = request.POST.copy()
                request.POST['buscar_turnos'] = 'disabled'
                if buscar_turnos_ya_se_valido == False:
                    return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''),'estado_boton_guardar_turno': 'enabled'})

            if alta_turno_form.cleaned_data['fecha'] is not None and request.POST.get("horario") is None:
                messages.add_message(request, messages.WARNING, 'Debe elegir un horario!', extra_tags="tag1")
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'paciente': paciente, "listado_disp_medicos":funcion_de_guardado_de_turno('consultar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],''), 'estado_boton_guardar_turno': 'enabled'})

            if request.POST.get("horario") is not None:
                funcion_de_guardado_de_turno('actualizar',request.POST['paciente'],request.POST['medico'],request.POST['fecha'],request.POST.get("horario"))
                return render(request,"AppPoliconsultorio/thanks.html")  
        else:
            error_formulario = alta_turno_form.errors
            if 'paciente' in error_formulario:
                return render(request, "AppPoliconsultorio/turnos.html", {'alta_turno_form': alta_turno_form, 'error_formulario' : error_formulario, 'estado_boton_buscar_medicos': 'disabled', 'estado_boton_buscar_turnos': 'disabled', 'estado_boton_guardar_turno': 'disabled' })
            if 'fecha' in error_formulario:
                paciente = Paciente.buscar_por_dni(request.POST.get('paciente', None))
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


@login_required
def baja_turno(request):
    listado_turnos = []
    errores = []

    if request.method == "POST":
        # Creo la instancia del formulario con los datos cargados en pantalla
        bajaturno_form = BajaTurnoForm(request.POST)
      
        if bajaturno_form.is_valid():
            dni = int(request.POST['dni'])    
            seleccionado = (request.POST.get('selectbajaturno'))   
            if seleccionado is None :    
                pacientes = Paciente.objects.filter(dni=dni)
                turnos_tabla = Turno.objects.filter(paciente=dni )                
                nombre = pacientes[0].nombre
                apellido= pacientes[0].apellido
                nombre_completo = f"{ apellido}, {nombre}"
                id = turnos_tabla[0].id
                # aca genero el listado_turnos: gte= mayor o igual a hoy                        
                listado_turnos = Turno.objects.filter(fecha__gte=date.today(), paciente=dni).order_by('fecha')
                return render(request, "AppPoliconsultorio/baja_turno.html", {'bajaturno_form': bajaturno_form, 'pacientel': nombre_completo, 'listado_turnos': listado_turnos  })
            else:
                turno = Turno.objects.filter(id=seleccionado)
                funcion_de_guardado_de_turno('anular',request.POST.get('selectbajaturno'),'','','')
    else:                 
        bajaturno_form = BajaTurnoForm()
 
    context = {
        "listado_turnos": listado_turnos,
        "bajaturno_form": BajaTurnoForm,
        "errores": errores,
    }
    return render(request, "AppPoliconsultorio/baja_turno.html", context)
   
def consulta_turnos(request):
    listado_turnos = []
    errores = []
    nombre_completo = ""
    
    if request.method == "POST":
        consulta_turnos_form = ConsultaTurnosForm(request.POST)
        if consulta_turnos_form.is_valid():
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
                nombre_completo = paciente[0].nombre_completo

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

            # Preparo el listado de turnos según los filtros cargados
            listado_turnos = Turno.lista_turnos(filtro_fechaDesde, filtro_fechaHasta, filtro_paciente, filtro_especialidad, filtro_medico)

        else:
            errores = consulta_turnos_form.errors
    else:
        consulta_turnos_form = ConsultaTurnosForm()

    context = {
        "listado_turnos": listado_turnos,
        "consulta_turnos_form": consulta_turnos_form,
        "errores": errores,
        "nombre_completo": nombre_completo,
    }
    return render(request, "AppPoliconsultorio/consulta_turno.html", context)


@login_required
def listar_turnos(request):
    context = {}

    turnos = Turno.objects.all()
    resultado = []
    for turno in turnos:
        item = {
            'dia': turno.fecha,
            'horario': turno.hora,
            'medico': (
                f"{turno.medico.nombre} {turno.medico.apellido} ({turno.medico.especialidad.descripcion})"
                if turno.medico is not None else ''
            ),
            'paciente': (
                f"{turno.paciente.nombre} {turno.paciente.apellido} (DNI: {turno.paciente.dni})"
                if turno.paciente is not None else ' SIN PACIENTE'
            )
        }
        resultado.append(item)

    context['listado_turnos'] = resultado
    return render(request, 'Apppoliconsultorio/listar_turnos.html', context)  


def usuarios(request):
    context = {}
    return render (request,"AppPoliconsultorio/usuarios.html", context)


def contactenos(request):
    context = {}
    return render (request,"AppPoliconsultorio/contactenos.html", context)


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


def registro(request):
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            print(form)
            # Registro en Medico/Paciente el enlace con el usuario
            email = form.cleaned_data['email']
            if Medico.objects.filter(mail = email).exists():
                persona = Medico.objects.filter(mail = email).first()
                grupo = Group.objects.get(name = 'Medicos')
            elif Paciente.objects.filter(mail = email).exists():
                persona = Paciente.objects.filter(mail = email).first()
                grupo = Group.objects.get(name = 'Pacientes')
            else:
                raise ValidationError('Error en la identificación del usuario')
            # Registro en users_groups el enlace con los grupos que definen los perfiles
            usuario = User.objects.get(username=form.cleaned_data["username"])
            persona.user = usuario
            persona.save()
            # Registro en users_groups el enlace con los grupos que definen los perfiles
            usuario.groups.add(grupo)
            # Autenticación y logueo
            user = authenticate(username=form.cleaned_data["username"], password = form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, f"Te has registrado correctamente como {grupo.name}")
            return redirect(to='index')
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form
    }
    return render (request,"registration/registro.html", context)


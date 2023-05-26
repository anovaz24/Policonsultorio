from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime
from .medicos import lista_medicos
from .especialidades import lista_especialidades
from .pacientes import lista_pacientes
from .models import *

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto:", max_length=5, required=True,
        widget=forms.TextInput(attrs={"class": "special", "id":"44"}))
    apellido = forms.CharField(label="Apellido de contacto", required=True)
    email = forms.EmailField(required=True)

class ConsultaMedicosForm(forms.Form):
    # Definir campos
    # nombre = forms.CharField(label="Nombre", required=True)
    # especialidad = forms.Select(label="Especialidad", required=False)
    #listado_especialidades = lista_especialidades()
    especialidad = forms.ChoiceField(choices=lista_especialidades(), required=True, widget=forms.Select)
    medico = forms.CharField(label="Médico", widget=forms.TextInput(attrs={'class': 'medico'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),


class ConsultaTurnosForm(forms.Form):

    def fecha(desde,cuantos_dias):
            if desde == 'h':
                hasta = datetime.date.today() + datetime.timedelta(days=cuantos_dias)
            else:
                pass
            return hasta.strftime('%Y-%m-%d')

    # Definir campos
    # nombre = forms.CharField(label="Nombre", required=True)
    # especialidad = forms.Select(label="Especialidad", required=False)
    # paciente = forms.ChoiceField(choices=lista_pacientes(), required=False, widget=forms.Select(attrs={"class": "form-control", "id":"paciente"}))
    paciente = forms.CharField(label="DNI Paciente", widget=forms.TextInput(attrs={'class': 'paciente'}), required=False)
    especialidad = forms.ChoiceField(label=' Especialidad', choices=lista_especialidades(), required=False, widget=forms.Select)
    medico = forms.ChoiceField(label=' Médico', choices=lista_medicos(), required=False, widget=forms.Select)
    fechaDesde = forms.DateField(label=' Fecha Desde',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',0))
    fechaHasta = forms.DateField(label=' Fecha Hasta',widget=forms.DateInput(attrs={'type': 'date'}), required=False, initial=fecha('h',60))

    # def clean_fechaDesde(self):
    #     dataD = self.cleaned_data["fechaDesde"]
    #     dataH = self.cleaned_data["fechaHasta"]

    #     if dataD is not None and dataH is not None and dataD > dataH:
    #         raise ValidationError("La Fecha Desde debe ser anterior a la Fecha Hasta")
        
    #     return dataD
    
    def clean(self):
        cleaned_data = super().clean()
        dataD = cleaned_data.get("fechaDesde")
        dataH = cleaned_data.get("fechaHasta")

        print(cleaned_data)
        print(dataD)
        print(dataH)
        if dataD is not None and dataH is not None: print(dataD > dataH)

        if dataD is not None and dataH is not None and dataD > dataH:
            raise ValidationError("La Fecha Desde debe ser anterior a la Fecha Hasta")
        
        return cleaned_data



class BajaTurnoForm(forms.Form):          
    # paciente = forms.CharField(label="Paciente:", max_length=15, required=True, 
    #     validators=[RegexValidator('^[0-9]+$', message="Debe contener sólo números")],
    #     widget=forms.TextInput(attrs={"class": "form-paciente", "id":"paciente", "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    dni = forms.IntegerField(label="Paciente:", widget=forms.TextInput(attrs=
         {"class": "form-paciente", "id":"paciente", "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    nombre_completo = forms.CharField(required=False , show_hidden_initial=True)

  
    def clean_dni(self):
        
        data = self.cleaned_data["dni"]
        # nombrep = self.cleaned_data["nombre"]
        # apellidop = self.cleaned_data["apellido"]
        # print("nombrep: ", nombrep)
        # print("apellidop: ", apellidop)   

        # Paciente.objects.all()
        if Paciente.objects.filter(dni=self.cleaned_data["dni"]).exists():
            pass
            # dni=int(self.cleaned_data["dni"])
            # paciente = Paciente.objects.filter(dni=dni)
            # nombre = paciente.nonmbre
            # apellido= paciente.apellido

        #     # apellido=self.cleaned_data["apellido"]
        #     print("encontró el  dni en la tabla - forms")
        #     print("dni: ", dni)
        #     print("pacientep: ", paciente)
                     
              
        else:
            print("NO encontró el  dni en la tabla")
            raise ValidationError("Paciente inexistente")
       
        return data
    
    # def nombre_clean(self):
    #     if Paciente.objects.filter(nombre=self.cleaned_data["nombre"]).exists():
    #         # dni=self.cleaned_data["dni"]
    #         nombre= self.cleaned_data["nombre"]
    #         print('encontro nombre')
    #         # apellido=self.cleaned_data["apellido"]
    #     return nombre

class BajaTurnoDetalleForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(label="Horario", required=True)       
    medico = forms.CharField(label=' Médico', widget=forms.TextInput(attrs={'class': 'paciente'}))
    especialidad = forms.CharField(label=' Especialidad')

class AltaTurnoForm(forms.Form):

    listado_especialidad = lista_especialidades()

    paciente = forms.CharField(label="pacientex:", max_length=8, min_length=7 ,required=True, validators=[RegexValidator(
                '^[0-9]+$',
                message="Debe contener solo números")],
        widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente","size": 12, "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    especialidad = forms.ChoiceField(label="especialidadx:",required=False, choices = listado_especialidad,
        widget=forms.Select(attrs={"class": "form-control", "id":"especialidad"}))
    medico = forms.ChoiceField(label="medicox:", required=False,
        widget=forms.Select(attrs={"class": "form-control", "id":"medico"}))


    def __init__(self, *args, **kwargs):
        codigo_especialidad = kwargs.pop('especialidad', None)
        super().__init__(*args, **kwargs)
        self.fields['medico'].choices = self.get_medicos_choices(codigo_especialidad)

    def get_medicos_choices(self, codigo_especialidad):
        choices = [('Z', 'Seleccione un médico')]
        if codigo_especialidad != None:
            especialidad = Especialidad.objects.get(codigo=codigo_especialidad)
            medicos = Medico.objects.filter(especialidad=especialidad)
            for medico in medicos:
                choice = (str(medico.id), f"{medico.nombre} {medico.apellido} ({medico.especialidad.descripcion})")
                choices.append(choice)
        return choices


    fecha = forms.DateField(label="fechax:",required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "id":"fecha",'type': 'date'}))

    def clean_medico(self):
        especialidad_codigo = self.cleaned_data['especialidad']
        medico_id = self.cleaned_data.get('medico')

        if especialidad_codigo != 'Z':
            self.fields['medico'].choices = self.get_medicos_choices(especialidad_codigo)
            medico_id = self.cleaned_data['medico']
            choices = self.get_medicos_choices(especialidad_codigo)
            # Verificar si el ID del médico seleccionado está en las opciones disponibles
            if medico_id not in [choice[0] for choice in choices]:
                raise forms.ValidationError("Selecciona un médico válido.")

        return medico_id
    
    def clean_paciente(self):
        data = self.cleaned_data["paciente"]
        print("los datos de paciente ingresado son:", data)
        longitud = len(data)
        if longitud > 8 or longitud < 7:
            raise ValidationError("Ingrese entre 7 y 8 dígitos de su número de documento")
        return data

    def clean_fecha(self):
        fecha_elegida = self.cleaned_data['fecha']
        print('la fecha que eligieron: ',fecha_elegida)
        if fecha_elegida != None:
            if fecha_elegida <= datetime.date.today():
                raise forms.ValidationError("La fecha debe ser mayor al día de Hoy!")
            dia_elegido = datetime.date.weekday(fecha_elegida)
            print('El dia elegido tiene el nro: ',dia_elegido)
            if dia_elegido >= 5:
                raise forms.ValidationError("La fecha no puede ser Sábado ni Domingo!")
        return fecha_elegida

    def clean(self):
        print("entro al clean")
        cleaned_data = super().clean()
        medico_id = cleaned_data.get('medico')
        print("Medico id:", medico_id)
        return self



# def lista_turnos():
#     listado_turnos = [
#         {
#             'dia': '20/04/2023',
#             'hora': '09:00',
#             'medico': 'Dr. Juan Pérez',
#             'especialidad': 'Cardiología',
#             'paciente': 'Adriana Cullen',
#         },
#         {
#             'dia': '20/04/2023',
#             'hora': '10:00',
#             'medico': 'Dra. María González',
#             'especialidad': 'Dermatología',
#             'paciente': 'José Olleros',
#         },
#         {
#             'dia': '20/04/2023',
#             'hora': '11:00',
#             'medico': 'Dr. Juan Perez',
#             'especialidad': 'Cardiología',
#             'paciente': 'Mariano Burgos',
#         },
#     ]
#     return listado_turnos


def funcion_de_guardado_de_turno(accion,id,medico,fecha,hora):
    if accion == 'actualizar':
        print("ingreso a actualizar")
        actualizacion = Turno.asignar_turno(id,medico,fecha,hora)
        if actualizacion:
            print("Turno fue registrado correctamente!!!")
        else:
            print("Hay un problema en el guardado del turno")

    if accion == 'consultar':
        id_paciente = Paciente.Obtener_id_Paciente_por_dni(id)
        print("el id del paciente es: ", id_paciente)
        print("el id del medico es el nro:", medico)
        print("la fecha tiene el valor siguiente:", fecha)
        print("ingreso a consultar")
        listado_de_turnos = Turno.obtener_turnos(medico,fecha)
        print("LISTA NUEVITA DE TURNOS! --> :",listado_de_turnos)
        return listado_de_turnos



from django import forms
from django.forms.fields import DateField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from .especialidades import lista_especialidades
from .medicos import lista_medicos
from .models import Turno


   
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
                             },
                             {'ID':'4',
                             'horario':'11:00 a 12:00',
                             'descr_disponible':'Disponible',
                             'flag':'enabled',
                             },
                             {'ID':'5',
                             'horario':'15:00 a 16:00',
                             'descr_disponible':'Disponible',
                             'flag':'enabled',
                             },
                             {'ID':'6',
                             'horario':'16:00 a 17:00',
                             'descr_disponible':'Disponible',
                             'flag':'enabled',
                             }]

class AltaTurnoForm(forms.Form):

    listado_especialidad = lista_especialidades()

    listado_medicos = lista_medicos()

    paciente = forms.CharField(label="pacientex:", max_length=8, min_length=7 ,required=True, validators=[RegexValidator(
                '^[0-9]+$',
                message="Debe contener solo números")],
        widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente","size": 12, "title":"Ingrese entre 7 y 8 dígitos de su número de documento"}))
    especialidad = forms.ChoiceField(label="especialidadx:",required=False, choices = listado_especialidad,
        widget=forms.Select(attrs={"class": "form-control", "id":"especialidad"}))
    medico = forms.ChoiceField(label="medicox:", required=False, choices = listado_medicos,
        widget=forms.Select(attrs={"class": "form-control", "id":"medico"}))
    fecha = forms.DateField(label="fechax:",required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "id":"fecha",'type': 'date'}))

    def clean_paciente(self):
        data = self.cleaned_data["paciente"]
        #if True:
        #    print("llego aki")
        #    raise ValidationError("Ingrese entre 7 y 8 dígitos de su número de documento")
        return None

    def clean(self):
        print("entro al clean")
        pass



def lista_turnos(filtro_paciente='', filtro_especialidad='', filtro_medico='', filtro_fechaDesde='', filtro_fechaHasta=''):
    
    listado_turnos = []
    
    turnos = Turno.objects.all()
    for turno in turnos:
        esta = 1
        print("Turno: ",turno)
        print("Turno.medico: ", turno.medico)
        if filtro_paciente != '':
            if turno.paciente is None:
                esta = 0
            elif turno.paciente.dni != filtro_paciente:
                esta = 0
        if esta and (filtro_especialidad != '' and turno.medico.especialidad.codigo != filtro_especialidad):
            esta = 0
            print("Turno.especialidad: ", turno.medico.especialidad.codigo)
            print("Tipo Turno.especialidad: ", type(turno.medico.especialidad.codigo))
            print("No cumple filtro_especialidad ", filtro_especialidad)
        if esta and (filtro_medico != '' and turno.medico.id != filtro_medico):
            esta = 0
        if esta and (filtro_fechaDesde != '' and turno.fecha < parse_date(filtro_fechaDesde)):
            esta = 0
            print("No cumple filtro_fechaDesde ", filtro_fechaDesde)
        if esta and (filtro_fechaHasta != '' and turno.fecha > parse_date(filtro_fechaHasta)):
            esta = 0
            print("No cumple filtro_fechaHasta ", filtro_fechaHasta)
        if esta:
            print(turno)
            listado_turnos.append(turno)
        # break
    # listado_turnos.sort()

    return listado_turnos



def funcion_de_guardado_de_turno(accion,id,descr_disponible,flag):
    ya_actualizado = 0
    if accion == 'actualizar':
        print("ingreso a actualizar")
        for e in listado_disp_medicos:
            #print('Valores en el diccionario: ',e)
            for j in e.items():
                if j[0] == 'ID' and j[1] == id:
                    print('lo encontre, ahora lo actualizo' )
                    #print ('Antes de modificar: ',e ['descr_disponible'])
                    e ['descr_disponible'] = descr_disponible
                    e ['flag'] = flag
                    ya_actualizado = 1
                    break
            if ya_actualizado == 1:
                break


    if accion == 'consultar':
        print("ingreso a consultar")
        return listado_disp_medicos

#print(funcion_de_guardado_de_turno('consultar','','',''))
#funcion_de_guardado_de_turno('actualizar','3','No disponible','disabled')
#print(funcion_de_guardado_de_turno('consultar','','',''))



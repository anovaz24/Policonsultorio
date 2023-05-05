from django import forms
from django.forms.fields import DateField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .especialidades import lista_especialidades
from .medicos import lista_medicos

   
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



def lista_turnos():
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
            'hora': '10:00',
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



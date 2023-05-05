from django import forms

class AltaTurnoForm3(forms.Form):

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
    turnos = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
    ]
    

    seleccion_turno = forms.ChoiceField(label=turnos,required=False, 
        widget=forms.RadioSelect,choices=turnos, 
    )
    #paciente = forms.CharField(label="pacientex:", max_length=8, min_length=7 ,required=True,
    #    widget=forms.TextInput(attrs={"class": "form-control", "id":"paciente"}))


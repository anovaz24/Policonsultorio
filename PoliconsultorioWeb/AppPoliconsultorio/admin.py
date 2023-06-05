from django.contrib import admin
from .models import Especialidad,Paciente,Medico,Turno

# Register your models here.
admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Turno)
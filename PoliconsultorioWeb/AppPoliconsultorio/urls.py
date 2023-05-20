from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('turno_medico/',views.turno_medico,name="turno_medico"),
    path('turno_consulta/',views.turno_consulta,name="turno_consulta"),
    path('baja_turno/',views.baja_turno,name="baja_turno"),
    path('especialidades/',views.especialidades,name="especialidades"),
    path('usuarios/',views.usuarios,name="usuarios"),
    path('contactenos/', views.contactenos, name='contactenos'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name="contacto"),
    path('thanks/', views.thanks, name="thanks"),
    # path('turnos/<slug:slug>/',views.turnos,name="turnos_rol"),
]
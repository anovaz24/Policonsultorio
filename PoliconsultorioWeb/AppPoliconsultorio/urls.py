from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('turno_medico/',views.turno_medico,name="turno_medico"),
    path('turno_consulta/',views.turno_consulta,name="turno_consulta"),
    path('listar_turnos/',views.listar_turnos,name="listar_turnos"),
    path('baja_turno/',views.baja_turno,name="baja_turno"),
<<<<<<< HEAD
    path('eliminar_turno/dni',views.eliminar_turno,name="eliminar_turno"),
    path('especialidades/',views.especialidades,name="especialidades"),  
    path('listar_especialidad/',views.listar_especialidad,name="listar_especialidad"), 
    path('listar_pacientes/',views.listar_pacientes,name="listar_pacientes"), 
=======
    path('especialidades/',views.especialidades,name="especialidades"),   
>>>>>>> 0a0bb4ffe56bced67285a43cfb2873560718945e
    path('usuarios/',views.usuarios,name="usuarios"),
    path('contactenos/', views.contactenos, name='contactenos'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name="contacto"),
    path('thanks/', views.thanks, name="thanks"),
    #path('turnos/',views.turnos,name="turnos"),
    #path('turnos/<slug:slug>/',views.turnos,name="turnos_rol"),
    path('consulta_medicos/',views.consulta_medicos,name="consulta_medicos"),
    path('alta_medico/',views.alta_medico,name="alta_medico"),
    path('baja_medico/',views.baja_medico,name="baja_medico"),
    path('listar_especialidad/',views.listar_especialidad,name="listar_especialidad"),
    path('listar_pacientes/',views.listar_pacientes,name="listar_pacientes"),
]
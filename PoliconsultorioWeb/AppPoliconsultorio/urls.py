from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('acerca/', views.acerca, name='acerca'),
    path('especialidades/',views.especialidades,name="especialidades"),  
    path('listar_especialidad/',views.listar_especialidad,name="listar_especialidad"), 
    path('alta_medico/',views.alta_medico,name="alta_medico"),
    path('baja_medico/',views.baja_medico,name="baja_medico"),
    path('consulta_medicos/',views.consulta_medicos,name="consulta_medicos"),
    path('listar_medicos/',views.listar_medicos.as_view(),name="listar_medicos"),
    path('listar_medicos_por_especialidad/<str:cod_especialidad>/', views.listar_medicos_por_especialidad, name="listar_medicos_por_especialidad"),
    path('alta_paciente/',views.alta_paciente,name="alta_paciente"),
    path('baja_paciente/',views.baja_paciente,name="baja_paciente"),
    path('consulta_pacientes/',views.consulta_pacientes,name="consulta_pacientes"),
    path('listar_pacientes/',views.listar_pacientes,name="listar_pacientes"), 
    path('turno_medico/',views.turno_medico,name="turno_medico"),
    path('baja_turno/',views.baja_turno,name="baja_turno"),
    # path('eliminar_turno/id',views.eliminar_turno,name="eliminar_turno"),
    path('baja_turno/eliminar_turno', views.eliminar_turno, name="eliminar_turno"),
    path('consulta_turnos/',views.consulta_turnos,name="consulta_turnos"),
    path('listar_turnos/',views.listar_turnos,name="listar_turnos"),
    path('eliminar_turno/dni',views.eliminar_turno,name="eliminar_turno"),
    path('usuarios/',views.usuarios,name="usuarios"),
    path('contactenos/', views.contactenos, name='contactenos'),
    path('contacto/', views.contacto, name="contacto"),
    path('thanks/', views.thanks, name="thanks"),
    #path('turnos/',views.turnos,name="turnos"),
    #path('turnos/<slug:slug>/',views.turnos,name="turnos_rol"),
]
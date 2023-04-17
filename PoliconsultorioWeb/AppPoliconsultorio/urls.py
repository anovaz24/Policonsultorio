from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('turno_medico/',views.turno_medico,name="turno_medico"),      
    path('especialidades/',views.especialidades,name="especialidades"),   
    path('usuarios/',views.usuarios,name="usuarios"),     
    path('contactenos', views.contactenos, name='contactenos'), 
    path('acerca', views.acerca, name='acerca'),
      
                                    
]
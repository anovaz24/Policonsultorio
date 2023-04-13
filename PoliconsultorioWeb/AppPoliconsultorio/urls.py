from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turno_medico/',views.turno_medico,name="turno_medico"),                                         
]
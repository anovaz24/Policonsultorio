from django.db import models

class Medicos(models.Model):
    nombre = models.CharField(max_length=25, verbose_name="Nombre")
    apellido = models.CharField(max_length=25, verbose_name="Apellido")
    dni = models.IntegerField(verbose_name="DNI")
    matricula = models.CharField(max_length=8, verbose_name="Matrícula")
    cod_especialidad = models.CharField(max_length=25, verbose_name="Especialidad")
    # turno = models.Choices() #deberá guardar el código del turno seleccionado
    turno = models.IntegerField(verbose_name="Turno")


class Especialidad(models.Model):
    especialidad_id = models.IntegerField(verbose_name="Código de especialidad")
    descripcion = models.CharField(max_length=128, verbose_name="Especialidad")
    medicos = models.ForeignKey(Medicos, on_delete=models.CASCADE)


class Turnos(models.Model):
    turno_id = models.IntegerField(verbose_name = "Código turno")
    fecha = models.DateField(verbose_name = "Fecha")
    horario = models.CharField(max_length=5, verbose_name="Horario")
    # medico = models.Choices(Medicos)  #deberá guardar el código del turno seleccionado
    medico = models.CharField(max_length=2, verbose_name="Médico")
    medico = models.ManyToManyField(Medicos) 
    # especialidad = models.Choices(Especialidad)  #deberá guardar el código del turno seleccionado
    especialidad = models.CharField(max_length=60, verbose_name="Especialidad")
    especialidad = models.ManyToManyField(Especialidad)


class Pacientes (models.Model):
    paciente_id =models.IntegerField(verbose_name="Codigo paciente")
    nombre_paciente = models.CharField(max_length=25, verbose_name="Nombre Paciente")
    apellido_paciente = models.CharField(max_length=15, verbose_name="Apellido Paciente")
    # turno = models.IntegerChoices(Turnos) #deberá guardar el código del turno seleccionado
    turno = models.CharField(max_length=2,verbose_name="Turno")
    turno = models.ForeignKey(Turnos, on_delete=models.CASCADE)
 
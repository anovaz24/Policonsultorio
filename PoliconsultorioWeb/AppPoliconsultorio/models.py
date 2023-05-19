from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=25, blank=False, verbose_name='Nombre')
    apellido = models.CharField(max_length=25, blank=False, verbose_name='Apellido')
    dni = models.IntegerField(blank=False, verbose_name='DNI')
    email = models.EmailField(max_length=150, verbose_name='Email')
    telefono = models.CharField(max_length=50, verbose_name='Telefono')

    class Meta:
        abstract = True


class Especialidad(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='Descripcion')


class Medico(Persona):
    matricula = models.IntegerField(blank=False, verbose_name='Matricula')
    especialidad = models.ManyToManyField(Especialidad)


class Paciente(Persona):
    GENEROS = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro'),
    ]
    fecha_nacimiento = models.DateField(verbose_name='Fecha Nacimiento')
    genero = models.CharField(max_length=1, choices=GENEROS, verbose_name='Genero')


class Turno(models.Model):
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico =models.ForeignKey(Medico, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

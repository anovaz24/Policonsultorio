from django.db import models
from datetime import timedelta, date

#para crear y migrar
# python manage.py makemigrations AppPoliconsultorio  
# # esta linea de arriba solo creo el archivo en migrate, luego lo tenes que migrar...
# con esta linea lo crea en la base...   
# python manage.py migrate AppPoliconsultorio

# Create your models here.
class Especialidad(models.Model):
    descripcion = models.CharField(max_length=128, verbose_name="Descripcion")
    codigo = models.CharField(max_length=2, verbose_name="Codigo")


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['codigo', 'descripcion'], name='unique_codigo_descripcion_combination'
            )
        ]

    def __str__(self):
        return self.descripcion

    @classmethod
    def migrar_registros_iniciales(cls):
        especialidades_lst = [
            {'descripcion': 'Cardiología', 'codigo': 'C'},
            {'descripcion': 'Dermatología', 'codigo': 'D'},
            {'descripcion': 'Neurología', 'codigo': 'N'},
            {'descripcion': 'Oftalmología', 'codigo': 'O'},
            {'descripcion': 'Pediatría', 'codigo': 'P'},
        ]
        for especialidad in especialidades_lst:
            obj, created = cls.objects.get_or_create(**especialidad)
            if created:
                print(f"Se creó la especialidad: {obj}")

        print("Registros iniciales de especialidades migrados con éxito.")



class Persona(models.Model):
    nombre = models.CharField(max_length=128, verbose_name="Nombre")
    apellido = models.CharField(max_length=128, verbose_name="Apellido")
    telefono = models.CharField(max_length=30, verbose_name="Telefono")
    mail = models.EmailField(max_length=128, verbose_name="Mail")

    class Meta:
        abstract = True





class Paciente(Persona):
    dni = models.IntegerField( verbose_name="dni", primary_key=True)
    obra_social = models.CharField(max_length=128, verbose_name="Obra_social", null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dni'], name='unique_dni_combination'
            )
        ]


    @classmethod
    def migrar_registros_iniciales(cls):
        pacientes = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'telefono': '123456789', 'mail': 'juan@example.com', 'dni': 11111111, 'obra_social': 'Obra Social A'},
            {'nombre': 'María', 'apellido': 'López', 'telefono': '987654321', 'mail': 'maria@example.com', 'dni': 22222222, 'obra_social': 'Obra Social B'},
            {'nombre': 'Carlos', 'apellido': 'González', 'telefono': '555555555', 'mail': 'carlos@example.com', 'dni': 33333333, 'obra_social': 'Obra Social C'},
        ]
        for paciente in pacientes:
            obj, created = cls.objects.get_or_create(**paciente)
            if created:
                print(f"Se creó el paciente: {obj}")

        print("Registros iniciales de pacientes migrados con éxito.")


    @classmethod
    def buscar_por_dni(cls, dni):
        try:
            paciente = cls.objects.get(dni=dni)
            nombre_completo = f"{paciente.nombre} {paciente.apellido}"
            return nombre_completo
        except cls.DoesNotExist:
            return "No-existe"



#Relacion uno a muchos
class Medico(Persona):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    pacientes = models.ManyToManyField(Paciente, through='Turno')

    @classmethod
    def migrar_registros_iniciales(cls):
        
        medicos = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'telefono': '123456789', 'mail': 'correo1@example.com', 'especialidad': 'Cardiología'},
            {'nombre': 'María', 'apellido': 'González', 'telefono': '987654321', 'mail': 'correo2@example.com', 'especialidad': 'Dermatología'},
            {'nombre': 'Celeste', 'apellido': 'Romero', 'telefono': '987616321', 'mail': 'correo3@example.com', 'especialidad': 'Dermatología'},
            {'nombre': 'Luis', 'apellido': 'Sánchez', 'telefono': '456789123', 'mail': 'correo4@example.com', 'especialidad': 'Neurología'},
            {'nombre': 'Ana', 'apellido': 'Rodríguez', 'telefono': '178954987', 'mail': 'correo5@example.com', 'especialidad': 'Oftalmología'},
            {'nombre': 'Mabel', 'apellido': 'Manzotti', 'telefono': '176954987', 'mail': 'correo6@example.com', 'especialidad': 'Oftalmología'},
            {'nombre': 'Jacinta', 'apellido': 'Lee', 'telefono': '174954987', 'mail': 'correo7@example.com', 'especialidad': 'Oftalmología'},
            {'nombre': 'Pedro', 'apellido': 'López', 'telefono': '321654987', 'mail': 'correo8@example.com', 'especialidad': 'Pediatría'},
        ]

        for medico in medicos:
            especialidad = Especialidad.objects.get(descripcion=medico['especialidad'])
            obj, created = cls.objects.get_or_create(
                nombre=medico['nombre'],
                apellido=medico['apellido'],
                telefono=medico['telefono'],
                mail=medico['mail'],
                especialidad=especialidad,
            )
            if created:
                print(f"Se creó el médico: {obj}")

        print("Registros iniciales de médicos migrados con éxito.")


class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null = True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name="fecha")
    hora = models.CharField(max_length=128, verbose_name="horario_turno")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['medico', 'fecha', 'hora'], name='unique_medico_fecha_hora_combination'
            )
        ]

    @classmethod
    def migrar_registros_iniciales(cls):
        fecha_inicial = date.today()
        fecha_final = fecha_inicial + timedelta(days=90)

        horas = ['10:00', '11:00', '12:00', '15:00', '16:00', '17:00']

        medicos = Medico.objects.all()

        for medico in medicos:
            for fecha in daterange(fecha_inicial, fecha_final):
                for hora in horas:
                    obj, created = cls.objects.get_or_create(
                        paciente=None,
                        medico=medico,
                        fecha=fecha,
                        hora=hora,
                    )
                    if created:
                        print(f"Se creó el turno: {obj}")

        print("Registros iniciales de turnos migrados con éxito.")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


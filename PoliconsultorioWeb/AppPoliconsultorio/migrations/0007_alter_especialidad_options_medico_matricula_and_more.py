# Generated by Django 4.2 on 2023-06-17 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppPoliconsultorio', '0006_merge_20230617_1755'),
    ]

    operations = [
        # migrations.AlterModelOptions(
        #     name='especialidad',
        #     options={'verbose_name': 'Especialidad', 'verbose_name_plural': 'Especialidades'},
        # ),
        # migrations.AddField(
        #     model_name='medico',
        #     name='matricula',
        #     field=models.IntegerField(null=True, verbose_name='Matricula'),
        # ),
        # migrations.AddField(
        #     model_name='paciente',
        #     name='fecha_nacimiento',
        #     field=models.DateField(null=True, verbose_name='Fecha Nacimiento'),
        # ),
        # migrations.AddField(
        #     model_name='paciente',
        #     name='genero',
        #     field=models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('O', 'Otro')], max_length=1, null=True, verbose_name='Genero'),
        # ),
        migrations.AddField(
            model_name='paciente',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        # migrations.AlterField(
        #     model_name='especialidad',
        #     name='descripcion',
        #     field=models.CharField(max_length=50, verbose_name='Descripcion'),
        # ),
        # migrations.AlterField(
        #     model_name='medico',
        #     name='apellido',
        #     field=models.CharField(max_length=25, verbose_name='Apellido'),
        # ),
        # migrations.AlterField(
        #     model_name='medico',
        #     name='mail',
        #     field=models.EmailField(max_length=150, verbose_name='Email'),
        # ),
        # migrations.AlterField(
        #     model_name='medico',
        #     name='nombre',
        #     field=models.CharField(max_length=25, verbose_name='Nombre'),
        # ),
        # migrations.AlterField(
        #     model_name='medico',
        #     name='telefono',
        #     field=models.CharField(max_length=50, verbose_name='Telefono'),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='apellido',
        #     field=models.CharField(max_length=25, verbose_name='Apellido'),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='dni',
        #     field=models.IntegerField(primary_key=True, serialize=False, verbose_name='DNI'),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='mail',
        #     field=models.EmailField(max_length=150, verbose_name='Email'),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='nombre',
        #     field=models.CharField(max_length=25, verbose_name='Nombre'),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='telefono',
        #     field=models.CharField(max_length=50, verbose_name='Telefono'),
        # ),
        # migrations.AlterField(
        #     model_name='turno',
        #     name='fecha',
        #     field=models.DateField(verbose_name='Fecha'),
        # ),
        # migrations.AlterField(
        #     model_name='turno',
        #     name='hora',
        #     field=models.CharField(choices=[('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00')], max_length=128, verbose_name='Horario_turno'),
        # ),
        # migrations.AlterField(
        #     model_name='turno',
        #     name='paciente',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppPoliconsultorio.paciente'),
        # ),
        # migrations.AddConstraint(
        #     model_name='medico',
        #     constraint=models.UniqueConstraint(fields=('matricula',), name='unique_matricula_combination'),
        # ),
    ]

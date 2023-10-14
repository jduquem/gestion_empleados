# Generated by Django 4.1 on 2023-10-14 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('identification', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=6, verbose_name='Nombre')),
                ('gender', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=10, verbose_name='Genero')),
                ('email', models.EmailField(max_length=6, verbose_name='Correo')),
                ('numberphone', models.PositiveIntegerField(verbose_name='Numero telefonico')),
                ('salary', models.PositiveIntegerField(verbose_name='Salario')),
                ('cityOfFresidence', models.CharField(max_length=6, verbose_name='Ciudad de recidencia')),
            ],
        ),
        migrations.CreateModel(
            name='hours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryTime', models.DateField(max_length=6, verbose_name='Hora entrada')),
                ('depertureTime', models.DateField(max_length=6, verbose_name='hora salida')),
                ('totalHours', models.IntegerField(max_length=6, verbose_name='Total horas')),
                ('identificationEmployee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='empleados.employee', verbose_name='identificacion del empleado')),
            ],
        ),
    ]

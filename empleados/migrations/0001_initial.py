# Generated by Django 4.1 on 2023-10-14 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('identification', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('gender', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1, verbose_name='Genero')),
                ('email', models.EmailField(max_length=100, verbose_name='Correo')),
                ('numberphone', models.CharField(max_length=10, verbose_name='Numero telefonico')),
                ('salary', models.PositiveIntegerField(verbose_name='Salario')),
                ('city', models.CharField(max_length=50, verbose_name='Ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reg', models.DateField(verbose_name='Fecha de registro')),
                ('entry_time', models.TimeField(verbose_name='Hora entrada')),
                ('deperture_time', models.TimeField(verbose_name='hora salida')),
                ('holiday', models.BooleanField(default=False, verbose_name='Feriado')),
                ('totalHours', models.IntegerField(verbose_name='Total horas')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleados.employee')),
            ],
        ),
    ]

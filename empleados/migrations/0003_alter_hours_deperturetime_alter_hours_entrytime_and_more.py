# Generated by Django 4.1 on 2023-10-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0002_alter_employee_cityoffresidence_alter_employee_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hours',
            name='depertureTime',
            field=models.DateField(verbose_name='hora salida'),
        ),
        migrations.AlterField(
            model_name='hours',
            name='entryTime',
            field=models.DateField(verbose_name='Hora entrada'),
        ),
        migrations.AlterField(
            model_name='hours',
            name='totalHours',
            field=models.IntegerField(verbose_name='Total horas'),
        ),
    ]

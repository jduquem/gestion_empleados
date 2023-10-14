# Generated by Django 4.1 on 2023-10-14 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cityOfFresidence',
            field=models.CharField(max_length=50, verbose_name='Ciudad de recidencia'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='Correo'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
    ]

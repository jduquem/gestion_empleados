# Generated by Django 4.1 on 2023-10-16 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0002_employeeshift_alter_employee_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeshift',
            name='total_hours',
            field=models.FloatField(default=0, verbose_name='Total horas'),
        ),
    ]
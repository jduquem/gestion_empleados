# Generated by Django 4.1 on 2023-10-24 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0010_alter_employee_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['employee_id']},
        ),
    ]
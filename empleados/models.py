from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse

# admin_group, created = Group.objects.get_or_create(name='Administradores')
# employee_group, created = Group.objects.get_or_create(name='Empleados')
# # Obtener un usuario (reemplaza con tu propio método)
# user = User.objects.get(username='nombre_de_usuario')
# # Asignar usuario al grupo de administradores
# user.groups.add(admin_group)
# # Asignar usuario al grupo de empleados
# user.groups.add(employee_group)
# add_miobjeto = Permission.objects.create(codename='add_miobjeto', name='Can add MiObjeto')
# change_miobjeto = Permission.objects.create(codename='change_miobjeto', name='Can change MiObjeto')
# delete_miobjeto = Permission.objects.create(codename='delete_miobjeto', name='Can delete MiObjeto')
# admin_group.permissions.add(add_miobjeto, change_miobjeto, delete_miobjeto)
# employee_group.permissions.add(add_miobjeto)


admin_group = Group.objects.create(name='Administrador')
empleado_group = Group.objects.create(name='Empleado')

# user = User.objects.create_user(username='admin', password='adminpassword')
# user.groups.add(admin_group)

# empleado = User.objects.create_user(username='emleado', password='empleadopassword')

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    identification = models.CharField(max_length=20, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False)
    gender = models.CharField(verbose_name='Genero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    email = models.EmailField(verbose_name='Correo', max_length=100, unique=True)
    numberphone = models.CharField(verbose_name='Numero telefonico', max_length=10)
    salary = models.PositiveIntegerField(verbose_name='Salario')
    city = models.CharField(verbose_name='Ciudad', max_length=50)

    def _str_(self):
        return self.identification

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_reg = models.DateField(verbose_name='Fecha de registro')
    entry_time = models.TimeField(verbose_name='Hora entrada')
    departure_time = models.TimeField(verbose_name='Hora salida')
    holiday = models.BooleanField(verbose_name='Feriado', default=False)
    total_hours = models.FloatField(verbose_name='Total horas', default=0)
    valor_hours = models.FloatField(verbose_name='Total horas', default=0)

    def _str_(self):
        return f"{self.employee} - {self.date_reg}"
        
from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse


# admin_group = Group.objects.create(name='Administrador')
# empleado_group = Group.objects.create(name='Empleado')

# user = User.objects.create_user(username='admin', password='adminpassword')
# user.groups.add(admin_group)

# empleado = User.objects.create_user(username='emleado', password='empleadopassword')

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    identification = models.CharField(max_length=20)
    name = models.CharField(verbose_name = 'Nombre', max_length = 50, null = False, blank = False)
    gender = models.CharField(verbose_name = 'Genero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    email = models.EmailField(verbose_name = 'Correo', max_length = 100, null = False, blank = False)
    numberphone =  models.CharField(verbose_name = 'Numero telefonico', max_length = 10, null = False, blank = False)
    salary =  models.PositiveIntegerField(verbose_name = 'Salario', null = False, blank = False)
    city = models.CharField(verbose_name = 'Ciudad', max_length = 50, null = False, blank = False)
    
    def __str__(self):
        return self.identification

class Employee_Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_reg = models.DateField(verbose_name = 'Fecha de registro', null = False, blank = False)
    entry_time = models.TimeField(verbose_name = 'Hora entrada', null = False, blank = False)
    deperture_time = models.TimeField(verbose_name = 'hora salida', null = False, blank = False)
    holiday = models.BooleanField(verbose_name = 'Feriado', default=False)
    totalHours = models.IntegerField(verbose_name = 'Total horas', null = False, blank = False)

    def __str__(self):
        return self.employee
    
    def save(self, *args, **kwargs):
        self.total_hours=200
        super(Employee_Shift, self).save(*args, **kwargs)
        

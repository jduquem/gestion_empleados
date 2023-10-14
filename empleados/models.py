from django.db import models
from django.contrib.auth.models import User, Group


# admin_group = Group.objects.create(name='Administrador')
# empleado_group = Group.objects.create(name='Empleado')

# user = User.objects.create_user(username='admin', password='adminpassword')
# user.groups.add(admin_group)

# empleado = User.objects.create_user(username='emleado', password='empleadopassword')



class employee(models.Model):
    identification = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(verbose_name = 'Nombre', max_length = 50, null = False, blank = False)
    gender = models.CharField(verbose_name = 'Genero', max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    email = models.EmailField(verbose_name = 'Correo', max_length = 100, null = False, blank = False)
    numberphone =  models.PositiveIntegerField(verbose_name = 'Numero telefonico', null = False, blank = False)
    salary =  models.PositiveIntegerField(verbose_name = 'Salario', null = False, blank = False)
    cityOfFresidence = models.CharField(verbose_name = 'Ciudad de recidencia', max_length = 50, null = False, blank = False)
    
    def __str__(self):
        return self.identification



class hours(models.Model):
    identificationEmployee = models.ForeignKey(employee, verbose_name="identificacion del empleado", blank=True, null=True, on_delete=models.CASCADE)
    entryTime = models.DateField(verbose_name = 'Hora entrada', null = False, blank = False)
    depertureTime = models.DateField(verbose_name = 'hora salida', null = False, blank = False)
    totalHours = models.IntegerField(verbose_name = 'Total horas', null = False, blank = False)

    def __str__(self):
        return self.identificationEmployee

from django.db import models
from django.contrib.auth.models import User

class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    identification = models.CharField(max_length=20, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=50, null=False, blank=False)
    gender = models.CharField(verbose_name='Genero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    email = models.EmailField(verbose_name='Correo', max_length=100, unique=True)
    numberphone = models.CharField(verbose_name='Numero telefonico', max_length=10)
    salary = models.PositiveIntegerField(verbose_name='Salario')
    city = models.CharField(verbose_name='Ciudad', max_length=50)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()

    def __str__(self):
        return self.identification

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_reg = models.DateField(verbose_name='Fecha de registro')
    entry_time = models.TimeField(verbose_name='Hora entrada')
    departure_time = models.TimeField(verbose_name='Hora salida')
    holiday = models.BooleanField(verbose_name='Feriado', default=False)
    total_hours = models.FloatField(verbose_name='Total horas', default=0)
    valor_hours = models.FloatField(verbose_name='Valor horas', default=0)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()  # Adding the custom manager

    def __str__(self):
        return f"{self.employee} - {self.date_reg}"

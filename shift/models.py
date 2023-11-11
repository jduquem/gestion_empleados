from django.db import models
from empleados.models import Employee

class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_reg = models.DateField(verbose_name='Fecha de registro')
    entry_time = models.TimeField(verbose_name='Hora entrada')
    departure_time = models.TimeField(verbose_name='Hora salida')
    holiday = models.BooleanField(verbose_name='Feriado', default=False)
    total_hours = models.FloatField(verbose_name='Total horas', default=0)
    valor_hours = models.FloatField(verbose_name='Valor horas', default=0)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.id} - ({self.employee}) - {self.date_reg}"

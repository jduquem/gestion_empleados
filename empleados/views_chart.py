from .models import Employee, EmployeeShift
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import arreglo
import json
from django.db.models.functions import TruncMonth

class Chart(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_eliminar.html'

    def get(self, request):
        context = {'data':100}
        return render(request, 'nomina/chart.html', context)        


class SalaryAverageByGender(View):
    template_name = 'nomina/chart.html'

    def get(self, request, *args, **kwargs):
        male_average_salary = Employee.objects.filter(gender='M').aggregate(avg_salary=Avg('salary'))['avg_salary']
        female_average_salary = Employee.objects.filter(gender='F').aggregate(avg_salary=Avg('salary'))['avg_salary']
        other_average_salary = Employee.objects.filter(gender='O').aggregate(avg_salary=Avg('salary'))['avg_salary']

        context = {
            'genders': ['Masculino', 'Femenino'],
            'average_salaries': [male_average_salary, female_average_salary, other_average_salary],
        }

        return render(request, 'nomina/chart.html', context)
    
class SalaryTotalByMonth(View):
    template_name = 'tu_template.html'

    def get(self, request, *args, **kwargs):
        monthly_salary_data = EmployeeShift.objects.annotate(
            month=TruncMonth('date_reg')
        ).values('month').annotate(
            total_salary=Sum('employee__salary')
        ).order_by('month')

        labels = [item['month'].strftime('%B %Y') for item in monthly_salary_data]
        data = [item['total_salary'] for item in monthly_salary_data]

        context = {
            'labels': labels,
            'data': data,
        }
        return render(request, self.template_name, context)

class EmployeesByMonth(View):
    template_name = 'nomina/employees_by_month.html'

    def get(self, request, *args, **kwargs):
        try:
            # Obtener datos de la cantidad de empleados por mes
            monthly_employees_data = Employee.objects.annotate(
                month=TruncMonth('date_joined')
            ).values('month').annotate(
                total_employees=Count('id')
            ).order_by('month')

            labels = [item['month'].strftime('%B %Y') for item in monthly_employees_data]
            data = [item['total_employees'] for item in monthly_employees_data]

            return render(request, self.template_name, {'labels': labels, 'data': data})
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class TotalSalary(View):
    template_name = 'tu_template.html'

    def get(self, request, *args, **kwargs):
        total_salary = Employee.objects.aggregate(total_salary=Sum('salary'))['total_salary']

        context = {
            'total_salary': total_salary,
        }

        return render(request, self.template_name, context)
    

class AverageHoursByMonth(View):
    template_name = 'nomina/average_hours_by_month.html'

    def get(self, request, *args, **kwargs):
        try:
            # Obtener datos del promedio de horas por mes
            monthly_hours_data = EmployeeShift.objects.annotate(
                month=TruncMonth('date_reg')
            ).values('month').annotate(
                avg_hours=Avg('total_hours')
            ).order_by('month')

            labels = [item['month'].strftime('%B %Y') for item in monthly_hours_data]
            data = [item['avg_hours'] for item in monthly_hours_data]
            return render(request, self.template_name, {'labels': labels, 'data': data})
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)
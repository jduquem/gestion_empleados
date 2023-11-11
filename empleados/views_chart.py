from .models import Employee
from shift.models import EmployeeShift
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
from django.db.models import Sum, Count

class Chart(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_eliminar.html'

    def get(self, request):
        # context = {'data':100}

        # promedio salario por genero
        male_average_salary = Employee.objects.filter(gender='M').aggregate(avg_salary=Avg('salary'))['avg_salary']
        female_average_salary = Employee.objects.filter(gender='F').aggregate(avg_salary=Avg('salary'))['avg_salary']
        other_average_salary = Employee.objects.filter(gender='O').aggregate(avg_salary=Avg('salary'))['avg_salary']

        # SalaryTotalByMonth
        monthly_salary_data = EmployeeShift.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(total_salary=Sum('employee__salary')).order_by('month')
        campos = [item['month'].strftime('%B %Y') for item in monthly_salary_data]
        valor = [item['total_salary'] for item in monthly_salary_data]

        
        # EmployeesByMonth
        # monthly_employees_data = Employee.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(total_employees=Count('id')).order_by('month')
        # labels = [item['month'].strftime('%B %Y') for item in monthly_employees_data]
        # data = [item['total_employees'] for item in monthly_employees_data]

        total_salary = Employee.objects.aggregate(total_salary=Sum('salary'))['total_salary']

        # AverageHoursByMonth
        monthly_hours_data = EmployeeShift.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(avg_hours=Avg('total_hours')).order_by('month')
        labels = [item['month'].strftime('%B %Y') for item in monthly_hours_data]
        data = [item['avg_hours'] for item in monthly_hours_data]
        
        context = {
            'genders': {'Masculino', 'Femenino', 'Otro'},
            'average_salaries': {male_average_salary, female_average_salary, other_average_salary},
            'campos':campos,
            'valor': valor,
            'total_salary': total_salary,
            'labels':labels,
            'data': data
        }

        return render(request, 'nomina/chart.html', {'context': context})        

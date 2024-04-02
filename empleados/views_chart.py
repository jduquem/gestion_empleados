from .models import Employee
from shift.models EmployeeShift
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import arreglo
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count

class Chart(LoginRequiredMixin, View):

    def get(self, request):

        # cantidad de empleados
        count_employees = Employee.objects.count()

        #salario total
        total_salary = Employee.objects.aggregate(total_salary=Sum('salary'))['total_salary']

        # promedio salario por genero
        male_average_salary = Employee.objects.filter(gender='M').aggregate(avg_salary=Avg('salary'))['avg_salary']
        female_average_salary = Employee.objects.filter(gender='F').aggregate(avg_salary=Avg('salary'))['avg_salary']
        other_average_salary = Employee.objects.filter(gender='O').aggregate(avg_salary=Avg('salary'))['avg_salary']

        # SalaryTotalByMonth
        monthly_salary_data = EmployeeShift.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(total_salary=Sum('employee__salary')).order_by('month')
        months_salary_per_month = [item['month'].strftime('%B %Y') for item in monthly_salary_data]
        total_salary_per_month = [item['total_salary'] for item in monthly_salary_data]

        
        # EmployeesByMonth
        # monthly_employees_data = Employee.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(total_employees=Count('id')).order_by('month')
        # labels = [item['month'].strftime('%B %Y') for item in monthly_employees_data]
        # data = [item['total_employees'] for item in monthly_employees_data]

        # AverageHoursByMonth
        monthly_hours_data = EmployeeShift.objects.annotate(month=TruncMonth('date_reg')).values('month').annotate(avg_hours=Avg('total_hours')).order_by('month')
        months_avg_salary_per_month = [item['month'].strftime('%B %Y') for item in monthly_hours_data]
        total_avg_salary_per_month = [item['avg_hours'] for item in monthly_hours_data]
        
        context = {
            'count_employees':count_employees,
            'total_salary': total_salary,

            'genders': {'Masculino', 'Femenino', 'Otro'},
            'average_salaries_gender': {male_average_salary, female_average_salary, other_average_salary},
            
            'months_salary_per_month':months_salary_per_month,
            'total_salary_per_month': total_salary_per_month,
            
            'months_avg_salary_per_month':months_avg_salary_per_month,
            'total_avg_salary_per_month': total_avg_salary_per_month
        }

        return render(request, 'nomina/chart.html', {'context': context})        


class Dashboard():

    def a():
        return 0

    def a():
        return 0

    def a():
        return 0

    def a():
        return 0
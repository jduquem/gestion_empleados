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


def group_required(user, group_names, request, show=False):
    for group in user.groups.all():
        for group_name in group_names:
            if group_name == 'Empleados': group_name = 'Empleado'
            if group_name == 'Administradores': group_name = 'Administrador'
            if group.name == group_name:
                return True
    if show:
        messages.warning(request, 'Usuario restringido')
    return False

class Index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    
class NomineeSalaryDetails(LoginRequiredMixin, View):
    template_name = 'nomina/NomineeSalaryDetails.html'
    
    def get(self, request, *args, **kwargs):
        if not group_required(request.user, ['Administrador', 'Empleado'], request):
            return HttpResponseRedirect(reverse('index'))
        try:
            if not group_required(request.user, ['Administrador'], request):
                horarios = EmployeeShift.objects.filter(employee_id=Employee.objects.get(user=request.user.id).employee_id).order_by('id')
            else:    
                horarios = EmployeeShift.objects.all().order_by('id')
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)

class Chart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nomina/chart.html')

def NomineeSalaryAverage(request):
    numbers = [1, 2, 3]
    data = [3, 7, 9, 1, 5]  # Sample data for the chart
    labels = ['Label A', 'Label B', 'Label C', 'Label D', 'Label E']
    chart_data = {
        'labels': labels,
        'data': data,
    }
    return json.dumps(chart_data)
    # return JsonResponse(chart_data, safe=False)

# class NomineeSalaryAverage(View):
#     template_name = 'nomina/NomineeSalaryAverage.html'

#     def get(self, request, *args, **kwargs):
#         try:
#             average_salary_per_gender = Employee.objects.values('gender').annotate(average_salary=Avg('salary'))
#             result = list(average_salary_per_gender)

#             return render(request, self.template_name, {'result':result, 'gender':('femenino', 'masculino', 'Otro')})
#             # Output the results
#             for entry in average_salary_per_gender:
#                 gender = entry['gender']
#                 average_salary = entry['average_salary']
#                 print(f"Gender: {gender}, Average Salary: {average_salary}")
#             average_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']

#             if average_salary is None:
#                 average_salary = 0
#             data = {'average_salary': average_salary}
#             print(data)
#             return render(request, self.template_name, {'average_salary':average_salary})
#         except:
#             return render(request, self.template_name)


# class SalaryTotalByMonth(View):
#     template_name = 'nomina/NomineeSalaryAverage.html'

#     def get(self, request, *args, **kwargs):
#         try:
#             # Obtener datos del salario total por mes
#             monthly_salary_data = EmployeeShift.objects.annotate(
#                 month=TruncMonth('date_reg')
#             ).values('month').annotate(
#                 total_salary=Sum('employee__salary')
#             ).order_by('month')

#             labels = [item['month'].strftime('%B %Y') for item in monthly_salary_data]
#             data = [item['total_salary'] for item in monthly_salary_data]
#             import pdb; pdb.set_trace()
#             print(labels)
#             print(data)

#             return render(request, self.template_name, {'labels': json.dumps(labels), 'data': json.dumps(data)})
#         except:
#             return render(request, self.template_name)
        
        


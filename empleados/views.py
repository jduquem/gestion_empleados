from .models import Employee, EmployeeShift
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import arreglo
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
import json
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
### Clase para enviar informacion para el grafico
# @user_passes_test(es_administrador)
class NomineeSalaryAverage(View):
    template_name = 'nomina/NomineeSalaryAverage.html'

    def get(self, request, *args, **kwargs):
        try:
            average_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
            if average_salary is None:
                average_salary = 0
            data = {'average_salary': average_salary}
            print(data)
            return render(request, self.template_name, {'average_salary':average_salary})
        except:
            return render(request, self.template_name)


class NomineeSalaryDetails(View):
    template_name = 'nomina/NomineeSalaryDetails.html'
    # @login_required
    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all().order_by('id')
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)
        
    # def iniciar_sesion(request):
    #     if request.method == 'POST':
    #         form = AuthenticationForm(request, request.POST)
    #         if form.is_valid():
    #             # El usuario ha iniciado sesión exitosamente
    #             # Puedes redirigirlo a una página de inicio, por ejemplo
    #             return HttpResponseRedirect('/inicio/')

    #     else:
    #         form = AuthenticationForm()
        
    #     return render(request, 'login.html', {'form': form})

def es_administrador(user):
    return user.groups.filter(name='Administradores').exists()


class SalaryTotalByMonth(View):
    template_name = 'nomina/NomineeSalaryAverage.html'

    def get(self, request, *args, **kwargs):
        try:
            # Obtener datos del salario total por mes
            monthly_salary_data = EmployeeShift.objects.annotate(
                month=TruncMonth('date_reg')
            ).values('month').annotate(
                total_salary=Sum('employee__salary')
            ).order_by('month')

            labels = [item['month'].strftime('%B %Y') for item in monthly_salary_data]
            data = [item['total_salary'] for item in monthly_salary_data]
            import pdb; pdb.set_trace()
            print(labels)
            print(data)

            return render(request, self.template_name, {'labels': json.dumps(labels), 'data': json.dumps(data)})
        except:
            return render(request, self.template_name)
        
        


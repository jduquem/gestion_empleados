from .models import Employee, EmployeeShift
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test

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

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all()
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
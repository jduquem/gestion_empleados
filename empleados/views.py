from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Employee, EmployeeShift
from django.contrib import messages
from django.urls import reverse
from django.views import View
from datetime import datetime
from .utils import is_holiday, valor_hours, calculo_Horas
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Avg
from django.db.models import Q

### index

class index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

### empleados ###

# Clase para listar el detalle
class listar_detalle(View):
    template_name = 'detalle.html'

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all()
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)

# Clase para listar los empleados
class listar_empleados(View):
    template_name = 'empleado.html'

    def get(self, request, *args, **kwargs):
        try:
            empleados = Employee.objects.all().order_by('employee_id')
            return render(request, self.template_name, {'empleados':empleados})
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            return render(request, self.template_name)

# Clase para agregar los empleados
class empleado_agregar(View):
    template_name = 'empleado_agregar.html'

    def get(self, request, *args, **kwargs):
        try:
            queryset = Employee.objects.all()
            return render(request, self.template_name, {'queryset':queryset})
        except:
            return render(request, self.template_name)    
    
    def post(self, request, *args, **kwargs):
        
        identification = request.POST.get('identification')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        numberphone = request.POST.get('numberphone')
        salary = request.POST.get('salary')
        city = request.POST.get('city')
        if Employee.objects.filter(identification=identification).exists():
            messages.warning(request, 'El empleado con cédula {} ya se encuentra creado'.format(identification))
            return render(request, self.template_name)

        try:
            new_employee = Employee.objects.create(
                identification=identification,
                name=name,
                gender=gender,
                email=email,
                numberphone=numberphone,
                salary=salary,
                city=city
            )
            messages.success(request, 'Se ha creado el empleado con cédula {}'.format(new_employee.identification))
            return HttpResponseRedirect(reverse('listar_empleados'))
        except Exception as e:
            messages.error(request, 'Error al crear el empleado: {}'.format(str(e)))
            return render(request, self.template_name)

# Clase para modificar los empleados
class empleado_actualizar(View):
    template_name = 'empleado_actualizar.html'
    def get(self, request, employee_id):
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
        except Employee.DoesNotExist:
            return render(request, 'listar_empleados.html')
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, *args, **kwargs):
        try:
            employee_id = request.POST['employee_id']
            name=request.POST['name']
            email=request.POST['email']
            numberphone=request.POST['numberphone']
            salary=request.POST['salary']
            city=request.POST['city']

            employee = get_object_or_404(Employee, employee_id=employee_id)
            employee.name = name
            employee.email= email
            employee.numberphone=numberphone
            employee.salary= salary
            employee.city = city
            employee.save()
            return HttpResponseRedirect(reverse('listar_empleados'))
        except Exception as e:
            print(e)
            return render(request, self.template_name)

# Clase para eliminar los empleados
class empleado_eliminar(View):
    template_name = 'empleado_eliminar.html'

    def get(self, request, employee_id):
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
        except Employee.DoesNotExist:
            return render(request, 'listar_empleados.html')
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, *args, **kwargs):
        try:
            employee_id = request.POST['employee_id']
            
            employee = get_object_or_404(Employee, employee_id=employee_id)
            employee.delete()
            
            return HttpResponseRedirect(reverse('listar_empleados'))
        except Exception as e:
            print(e)
            return render(request, self.template_name)



### horarios ###
# Clase para listar los horarios
class listar_horarios(View):
    template_name = 'horario.html'

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all().order_by('id')
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)

# Clase para agregar los horarios
class horario_agregar(View):
    template_name = 'horario_agregar.html'

    def get(self, request, *args, **kwargs):
        try:
            employees = Employee.objects.all()
            return render(request, self.template_name, {'employees':employees})
        except:
            return render(request, self.template_name)    
    
    def post(self, request, *args, **kwargs):
        queryset = EmployeeShift.objects.all()
        for e in queryset:
            if e == request.POST['employee']:
                messages.warning(request, 'El horario para el empleado {} ya se encuentra creado'.format(request.POST['employee']))
                return render(request, 'horario_agregar.html')
            else:
                try:
                    employee_id = int(request.POST['employee'])
                    date_reg = request.POST['date_reg']
                    entry_time_str = request.POST['entry_time']
                    departure_time_str = request.POST['departure_time']

                    # # Comprobar si ya existe un horario para el mismo empleado en la misma fecha
                    # existing_horario = EmployeeShift.objects.filter(employee_id=employee_id, date_reg=date_reg).first()
                    # if existing_horario:
                    #     messages.warning(request, 'El horario para el empleado {} en la fecha {} ya se encuentra creado'.format(employee_id, date_reg))
                    #     return render(request, self.template_name)

                    # Comprobar si el nuevo horario se cruza con horarios existentes

                    import pdb; pdb.set_trace()
                    horarios_Cruzados = EmployeeShift.objects.filter(
                        Q(employee_id=employee_id, date_reg=date_reg) &
                        (
                            Q(entry_time__lte=entry_time_str, departure_time__gte=entry_time_str) |
                            Q(entry_time__lte=departure_time_str, departure_time__gte=departure_time_str)
                        )
                    )

                    if horarios_Cruzados.exists():
                        print(f'el horario {horarios_Cruzados} ya existe')
                        messages.warning(request, 'El nuevo horario se cruza con otros horarios existentes para el mismo empleado en la misma fecha')
                        return render(request, self.template_name)

                    total_hours = calculo_Horas(entry_time_str, departure_time_str)
                    holiday = is_holiday(date_reg)
                    val_hours = 200
                    EmployeeShift.objects.create(employee_id = employee_id, date_reg=date_reg, entry_time=entry_time_str, departure_time=departure_time_str, holiday=holiday, total_hours=total_hours, valor_hours=val_hours)
                    messages.success(request, 'Se ha creado el horario para el empleado')
                    return HttpResponseRedirect(reverse('listar_horarios'))
                except Exception as e:
                    print(f"Se ha producido un error: {e}")
                    return render(request, self.template_name)
        return render(request, self.template_name)

# Clase para modificar los horarios
class horario_actualizar(View):
    template_name = 'horario_actualizar.html'

    def get(self, request, id):
        try:
            horarios = get_object_or_404(EmployeeShift, id=id)
        except Employee.DoesNotExist:
            return render(request, 'listar_horarios.html')
        return render(request, self.template_name, {'horarios': horarios})

    def post(self, request, *args, **kwargs):
        try:
            id = request.POST['id']
            date_reg = request.POST['date_reg'] # fecha
            entry_time_str = request.POST['entry_time'] 
            departure_time_str = request.POST['departure_time']
            entry_time = datetime.strptime(entry_time_str, '%H:%M')
            departure_time = datetime.strptime(departure_time_str, '%H:%M')
            time_difference = departure_time - entry_time
            total_hours = time_difference.total_seconds() / 3600
            holiday = is_holiday(date_reg)
            
            horarios = get_object_or_404(EmployeeShift, id=id)
            horarios.date_reg = date_reg
            horarios.entry_time= entry_time
            horarios.departure_time= departure_time
            horarios.total_hours=total_hours
            horarios.holiday=holiday
            horarios.save()
            return HttpResponseRedirect(reverse('listar_horarios'))
        except Exception as e:
            print(e)
            return render(request, self.template_name)

# Clase para eliminar los horarios
class horario_eliminar(View):
    template_name = 'horario_eliminar.html'

    def get(self, request, id):
        try:
            horarios = get_object_or_404(EmployeeShift, id=id)
        except EmployeeShift.DoesNotExist:
            return render(request, 'listar_horarios.html')
        return render(request, self.template_name, {'horarios': horarios})

    def post(self, request, *args, **kwargs):
        try:
            id = request.POST['id']
            
            horarios = get_object_or_404(EmployeeShift, id=id)
            horarios.delete()
            
            return HttpResponseRedirect(reverse('listar_horarios'))
        except Exception as e:
            print(e)
            return render(request, self.template_name)


### Clase para enviar informacion para el grafico

class EmployeeSalaryChartView(TemplateView):
    template_name = 'employee_salary_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcula el salario promedio de tus empleados
        average_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
        if average_salary is None:
            average_salary = 0
        context['average_salary'] = average_salary
        return context

    def render_to_response(self, context, **response_kwargs):
        # Retorna los datos del salario promedio en formato JSON
        data = {'average_salary': context['average_salary']}
        return JsonResponse(data)

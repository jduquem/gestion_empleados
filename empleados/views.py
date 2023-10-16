from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Employee, EmployeeShift
from django.contrib import messages
from django.urls import reverse
from django.views import View
from datetime import datetime


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
        

    # def get(self, request, *args, **kwargs):
    #     try:
    #         horarios = EmployeeShift.objects.all()
    #         resultados = []

    #         for horario in horarios:
    #             hora_inicio = datetime.strptime(str(horario.entry_time), '%H:%M:%S').time()
    #             hora_fin = datetime.strptime(str(horario.departure_time), '%H:%M:%S').time()

    #             diferencia = datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)

    #             horas_en_rango = diferencia.total_seconds() / 3600

    #             resultados.append({
    #                 'horario': horario,
    #                 'horas_en_rango': horas_en_rango,
    #             })

    #     except:
    #         return render(request, self.template_name, {'horarios':horarios}, {'resultados': resultados})

# Clase para listar los empleados
class listar_empleados(View):
    template_name = 'empleado.html'

    def get(self, request, *args, **kwargs):
        try:
            empleados = Employee.objects.all()
            # import pdb; pdb.set_trace()
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
        # import pdb; pdb.set_trace()
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
            posturl = request.GET.dict()
            print(posturl)
            employee = get_object_or_404(Employee, employee_id=employee_id)
            import pdb; pdb.set_trace()
        except Employee.DoesNotExist:
            return render(request, 'employee_not_found.html')
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, *args, **kwargs):
        try:
            identification = request.POST['identification']
            name=request.POST['name']
            gender=request.POST['gender']
            email=request.POST['email']
            numberphone=request.POST['numberphone']
            salary=request.POST['salary']
            city=request.POST['city']

            empleados = Employee.objects.get(identification =kwargs['identification'])
            empleados.name = name
            empleados.gender= gender
            empleados.email= email
            empleados.numberphone=numberphone
            empleados.salary= salary
            empleados.city = city
            empleados.save()
            return HttpResponseRedirect(reverse('empleado'))
        except:
            return render(request, self.template_name)

# Clase para eliminar los empleados
class empleado_eliminar(View):
    template_name = 'empleado_eliminar.html'

    def get(self, request, *args, **kwargs):
        try:
            empleados = Employee.objects.get(indentification=args)
            empleados.delete()
            messages.warning(request, 'El empleado con cedula {} se elimino correctamente'.format(args))
            return render(request, self.template_name)
        except:
            return render(request, self.template_name)



### horarios ###
# Clase para listar los horarios
class listar_horarios(View):
    template_name = 'horario.html'

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all()
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)

# Clase para agregar los horarios
class horario_agregar(View):
    template_name = 'horario_agregar.html'

    def get(self, request, *args, **kwargs):
        try:
            # queryset = EmployeeShift.objects.all()
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
                    date_reg=request.POST['date_reg']
                    entry_time=request.POST['entry_time']
                    departure_time=request.POST['departure_time']
                    holiday = False
                    total_hours = 6
                    # import pdb; pdb.set_trace()
                    # h_init = datetime.strptime(str(entry_time), '%H:%M').time()
                    # h_end = datetime.strptime(str(entry_time), '%H:%M').time()
                    # diferencia = h_end - h_init
                    # # holiday = festivos(date_reg)
                    # total_hours= diferencia.total_seconds() / 3600 
                    EmployeeShift.objects.create(employee_id = employee_id, date_reg=date_reg, entry_time=entry_time, departure_time=departure_time, holiday=holiday, total_hours=total_hours)
                    messages.success(request, 'Se ha creado el horario para el empleado')
                    return HttpResponseRedirect(reverse('listar_horarios'))
                except Exception as e:
                    print(f"Se ha producido un error: {e}")
                    return render(request, self.template_name)
        return render(request, self.template_name)

# Clase para modificar los horarios
class horario_actualizar(View):
    template_name = 'horario_actualizar.html'

    def get(self, request, *args, **kwargs):
        try:
            queryset = EmployeeShift.objects.all()
            return render(request, self.template_name, {'queryset':queryset})
        except:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            employee=request.POST['employee']
            date_reg=request.POST['date_reg']
            entry_time=request.POST['entry_time']
            departure_time=request.POST['departure_time']
            h_init = datetime.strptime(entry_time, "%H:%M:%S")
            h_end = datetime.strptime(departure_time, "%H:%M:%S")
            diferencia = h_end - h_init
            # holiday = festivos(date_reg)
            total_hours= diferencia.total_seconds() / 3600 

            empleados = EmployeeShift.objects.get(employee=kwargs['employee'])
            empleados.date_reg = date_reg
            empleados.entry_time= entry_time
            empleados.departure_time= departure_time
            empleados.total_hours=total_hours
            empleados.save()
            return HttpResponseRedirect(reverse('horario'))
        except:
            return render(request, self.template_name)

# Clase para eliminar los horarios
class horario_eliminar(View):
    template_name = 'horario_eliminar.html'

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.get(employee=args)
            horarios.delete()
            messages.warning(request, 'El horario para el empleado {} se elimino correctamente'.format(args))
            return render(request, self.template_name)
        except:
            return render(request, self.template_name)
















# def festivos(fecha):
#     # Definir la URL de la API y los parámetros
#     api_url = "https://date.nager.at/api/v3/publicholidays/2023/CO"
#     country_code = "CO"  # Código de país (ejemplo: Colombia)
#     # Parámetros de la solicitud
#     params = {
#         "CountryCode": country_code,
#         "Year": 2023  # Puedes ajustar el año
#     }
#     # Realizar la solicitud a la API
#     response = requests.get(api_url, params=params)
#     # Verificar si la solicitud fue exitosa
#     if response.status_code == 200:
#         # La solicitud fue exitosa
#         holidays = response.json()
#         for holiday in holidays:
#             print(f"{holiday['date']}")
#     else:
#         # La solicitud no fue exitosa
#         print(f"Error {response.status_code}: No se pudo obtener la información de días festivos.")
#     return 

# # Define la fecha que quieres verificar

# fecha = datetime.date(2023, 10, 16)  # Formato: año, mes, día (2023-10-15)

# # Verifica si la fecha es un domingo (0 = lunes, 6 = domingo)
# es_domingo = fecha.weekday() == 6

# if es_domingo:
#     print(f"{fecha} es un domingo.")
# else:
#     print(f"{fecha} no es un domingo.")


# views.py
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Employee
from django.db.models import Avg

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

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Employee
from django.contrib import messages
from django.urls import reverse
from django.views import View


### empleados ###

# Clase para listar los empleados
class listar_empleados(View):
    template_name = 'empleado/empleado.html'

    def get(self, request, *args, **kwargs):
        try:
            empleados = Employee.objects.all().order_by('employee_id')
            return render(request, self.template_name, {'empleados':empleados})
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            return render(request, self.template_name)

# Clase para agregar los empleados
class empleado_agregar(View):
    template_name = 'empleado/empleado_agregar.html'

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
    template_name = 'empleado/empleado_actualizar.html'
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
    template_name = 'empleado/empleado_eliminar.html'

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
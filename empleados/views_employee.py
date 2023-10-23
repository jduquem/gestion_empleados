from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Employee
from .views import group_required
from .populate import populate_employees

class EmployeeList(LoginRequiredMixin, View):
    template_name = 'empleado/empleado.html'

    def get(self, request, *args, **kwargs):
        try:
            
            if not group_required(request.user, ['Administrador', 'Empleado'], request, True):
                return HttpResponseRedirect(reverse('index'))
            if not group_required(request.user, ['Administrador'], request):
                empleados = Employee.objects.filter(user=request.user.id)
            else:    
                empleados = Employee.objects.all().order_by('employee_id')
                populate_employees(2)
            return render(request, self.template_name, {'empleados':empleados})
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            return render(request, self.template_name)


class EmployeeAdd(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_agregar.html'

    def get(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            queryset = Employee.objects.all()
            return render(request, self.template_name, {'queryset':queryset})
        except:
            return render(request, self.template_name)    
    
    def post(self, request, *args, **kwargs):
        if not group_required(request.user, ['Administrador'], request, True):
            return HttpResponseRedirect(reverse('index'))
        username = request.POST.get('identification')
        if Employee.objects.filter(identification=username).exists():
            messages.warning(request, 'El empleado con cédula {} ya se encuentra creado'.format(username))
            return render(request, self.template_name)
        
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'El empleado con cédula {} ya se encuentra creado'.format(username))
            return render(request, self.template_name)
        try:
            
            user = User.objects.create_user(username=username, email='email@gmail.com', password=username)
            if request.POST.get('isadmin'):
                user.groups.add(Group.objects.get(name='Administrador'))
                user.groups.add(Group.objects.get(name='Administradores'))
            else:
                user.groups.add(Group.objects.get(name='Empleado'))
                user.groups.add(Group.objects.get(name='Empleados'))
            user.save()

            identification = request.POST.get('identification')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            numberphone = request.POST.get('numberphone')
            salary = request.POST.get('salary')
            city = request.POST.get('city')
                        
            new_employee = Employee.objects.create(
                user=user,
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


class EmployeeUpdate(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_actualizar.html'
    def get(self, request, employee_id):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            employee = get_object_or_404(Employee, employee_id=employee_id)
        except Employee.DoesNotExist:
            return HttpResponseRedirect(reverse('listar_empleados'))
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
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
            messages.success(request, 'Se ha modificado el empleado con cédula {}'.format(employee.identification))
            return HttpResponseRedirect(reverse('listar_empleados'))
        except Exception as e:
            messages.warning(request, 'Se ha producido un error')
            return HttpResponseRedirect(reverse('listar_empleados'))


class EmployeeDelete(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_eliminar.html'

    def get(self, request, employee_id):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            employee = get_object_or_404(Employee, employee_id=employee_id)
        except Employee.DoesNotExist:
            return HttpResponseRedirect(reverse('listar_empleados'))
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            employee_id = request.POST['employee_id']
            employee = get_object_or_404(Employee, employee_id=employee_id)
            employee.is_deleted=True
            employee.save()
            messages.success(request, 'Se ha eliminado el empleado con cédula {}'.format(employee.identification))
            return HttpResponseRedirect(reverse('listar_empleados'))
        except Exception as e:
            messages.success(request, 'El empleado no se pudo eliminar')
            return HttpResponseRedirect(reverse('listar_empleados'))

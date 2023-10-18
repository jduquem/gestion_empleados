from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Employee, EmployeeShift
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .utils import is_holiday, shift_hours, shift_money, shift_validations
from .views import group_required


class listar_horarios(LoginRequiredMixin, View):
    template_name = 'horario/horario.html'

    def get(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador', 'Empleado'], request, True):
                return HttpResponseRedirect(reverse('index'))
            if not group_required(request.user, ['Administrador'], request):
                horarios = EmployeeShift.objects.filter(employee_id=Employee.objects.get(user=request.user.id).employee_id)
            else:    
                horarios = EmployeeShift.objects.all().order_by('id')
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)


class horario_agregar(LoginRequiredMixin, View):
    template_name = 'horario/horario_agregar.html'

    def get(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            employees = Employee.objects.all()
            return render(request, self.template_name, {'employees':employees})
        except:
            return render(request, self.template_name)    
    
    def post(self, request, *args, **kwargs):
        if not group_required(request.user, ['Administrador'], request, True):
            return HttpResponseRedirect(reverse('index'))
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

                    if shift_validations(employee_id, EmployeeShift, date_reg, entry_time_str, departure_time_str ):
                        print('el horario ya existe')
                        messages.warning(request, 'El nuevo horario se cruza con otros horarios existentes para el mismo empleado en la misma fecha')
                        return render(request, self.template_name)
                    empleado = Employee.objects.get(employee_id = employee_id)
                    total_hours = shift_hours(entry_time_str, departure_time_str)
                    holiday = is_holiday(date_reg)

                    val_hours = shift_money(total_hours, empleado.salary, holiday)
                    EmployeeShift.objects.create(employee_id = employee_id, date_reg=date_reg, entry_time=entry_time_str, departure_time=departure_time_str, holiday=holiday, total_hours=total_hours, valor_hours=val_hours)
                    messages.success(request, 'Se ha creado el horario para el empleado')
                    return HttpResponseRedirect(reverse('listar_horarios'))
                except Exception as e:
                    print(f"Se ha producido un error: {e}")
                    return render(request, self.template_name)
        return render(request, self.template_name)


class horario_actualizar(LoginRequiredMixin, View):
    template_name = 'horario/horario_actualizar.html'

    def get(self, request, id):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            horarios = get_object_or_404(EmployeeShift, id=id)
        except Employee.DoesNotExist:
            return HttpResponseRedirect(reverse('listar_horarios'))
        return render(request, self.template_name, {'horarios': horarios})

    def post(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            employee_id = int(request.POST['employee_id'])
            shift_id = request.POST['id']
            date_reg = request.POST['date_reg'] # fecha
            entry_time_str = request.POST['entry_time'] 
            departure_time_str = request.POST['departure_time']
            if shift_validations(employee_id, EmployeeShift, date_reg, entry_time_str, departure_time_str ):
                print('el horario ya existe')
                messages.warning(request, 'El nuevo horario se cruza con otros horarios existentes para el mismo empleado en la misma fecha')
                return HttpResponseRedirect(reverse('listar_horarios'))
            entry_time = datetime.strptime(entry_time_str, '%H:%M')
            departure_time = datetime.strptime(departure_time_str, '%H:%M')
            time_difference = departure_time - entry_time
            total_hours = time_difference.total_seconds() / 3600
            holiday = is_holiday(date_reg)
            
            horarios = get_object_or_404(EmployeeShift, id=shift_id)
            horarios.date_reg = date_reg
            horarios.entry_time= entry_time
            horarios.departure_time= departure_time
            horarios.total_hours=total_hours
            horarios.holiday=holiday
            horarios.save()
            messages.success(request, 'Se modifico el horario para el empleado')
            return HttpResponseRedirect(reverse('listar_horarios'))
        except Exception as e:
            messages.warning(request, f'No se realizo la modificación {e}')
            return HttpResponseRedirect(reverse('listar_horarios'))


class horario_eliminar(LoginRequiredMixin, View):
    template_name = 'horario/horario_eliminar.html'

    def get(self, request, id):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            horarios = get_object_or_404(EmployeeShift, id=id)
        except EmployeeShift.DoesNotExist:
            return HttpResponseRedirect(reverse('listar_horarios'))
        return render(request, self.template_name, {'horarios': horarios})

    def post(self, request, *args, **kwargs):
        try:
            if not group_required(request.user, ['Administrador'], request, True):
                return HttpResponseRedirect(reverse('index'))
            id = request.POST['id']
            
            horarios = get_object_or_404(EmployeeShift, id=id)
            horarios.delete()
            messages.success(request, 'El horario se elimino correctamente')
            
            return HttpResponseRedirect(reverse('listar_horarios'))
        except Exception as e:
            messages.warning(request, f'El nuevo horario no se pudo eliminar {e}')
            return HttpResponseRedirect(reverse('listar_horarios'))

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Employee, EmployeeShift
from django.contrib import messages
from django.urls import reverse
from django.views import View
from datetime import datetime
from .utils import is_holiday, shift_hours, shift_money

from django.db.models import Q

### horarios ###
# Clase para listar los horarios
class listar_horarios(View):
    template_name = 'horario/horario.html'

    def get(self, request, *args, **kwargs):
        try:
            horarios = EmployeeShift.objects.all().order_by('id')
            return render(request, self.template_name, {'horarios':horarios})
        except:
            return render(request, self.template_name)

# Clase para agregar los horarios
class horario_agregar(View):
    template_name = 'horario/horario_agregar.html'

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

# Clase para modificar los horarios
class horario_actualizar(View):
    template_name = 'horario/horario_actualizar.html'

    def get(self, request, id):
        try:
            horarios = get_object_or_404(EmployeeShift, id=id)
        except Employee.DoesNotExist:
            return render(request, 'horario/listar_horarios.html')
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
# @user_passes_test(es_administrador)
class horario_eliminar(View):
    template_name = 'horario/horario_eliminar.html'

    def get(self, request, id):
        try:
            horarios = get_object_or_404(EmployeeShift, id=id)
        except EmployeeShift.DoesNotExist:
            return render(request, 'horario/listar_horarios.html')
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


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_employee as employee 
from shift.views import ShiftList, ShiftAdd, ShiftUpdate, ShiftDelete
from . import views_chart as chart
from .views import Index, NomineeSalaryAverage, NomineeSalaryDetails, Chart

urlpatterns = [
   
    path('', Index.as_view(), name='index'),
        # empleado
    path('listar_empleados/', employee.EmployeeList.as_view(), name='listar_empleados'),
    path('empleado_agregar/', employee.EmployeeAdd.as_view(), name='empleado_agregar'),
    path('empleado_actualizar/<int:employee_id>/', employee.EmployeeUpdate.as_view(), name='empleado_actualizar'),
    path('empleado_eliminar/<int:employee_id>', employee.EmployeeDelete.as_view(), name='empleado_eliminar'),

   
       # horarios
    path('listar_horarios/', ShiftList.as_view(), name='listar_horarios'),
    path('horario_agregar/', ShiftAdd.as_view(), name='horario_agregar'),
    path('horario_actualizar/<int:id>', ShiftUpdate.as_view(), name='horario_actualizar'),
    path('horario_eliminar/<int:id>', ShiftDelete.as_view(), name='horario_eliminar'),


      # reporte
    path('chart/', chart.Chart.as_view(), name='chart'),
    path('nominee_salary_details/', NomineeSalaryDetails.as_view(), name='nominee_salary_details'),
    
      # login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 ]

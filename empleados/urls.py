from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_employee as employee 
from . import views_shift as shift
from .views import Index, NomineeSalaryAverage, NomineeSalaryDetails

urlpatterns = [
   
    path('', Index.as_view(), name='index'),
        # empleado
    path('listar_empleados/', employee.listar_empleados.as_view(), name='listar_empleados'),
    path('empleado_agregar/', employee.empleado_agregar.as_view(), name='empleado_agregar'),
    path('empleado_actualizar/<int:employee_id>/', employee.empleado_actualizar.as_view(), name='empleado_actualizar'),
    path('empleado_eliminar/<int:employee_id>', employee.empleado_eliminar.as_view(), name='empleado_eliminar'),

   
       # horarios
    path('listar_horarios/', shift.listar_horarios.as_view(), name='listar_horarios'),
    path('horario_agregar/', shift.horario_agregar.as_view(), name='horario_agregar'),
    path('horario_actualizar/<int:id>', shift.horario_actualizar.as_view(), name='horario_actualizar'),
    path('horario_eliminar/<int:id>', shift.horario_eliminar.as_view(), name='horario_eliminar'),


      # reporte
    path('nominee_salary_average/', NomineeSalaryAverage.as_view(), name='nominee_salary_average'),
    path('nominee_salary_details/', NomineeSalaryDetails.as_view(), name='nominee_salary_details'),

    
      # login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 ]

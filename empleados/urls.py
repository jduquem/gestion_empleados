from django.urls import path
from .views import listar_empleados, empleado_agregar, empleado_actualizar, empleado_eliminar, listar_horarios, horario_agregar, horario_actualizar, horario_eliminar, listar_detalle, EmployeeSalaryChartView

urlpatterns = [
        # empleado
    path('listar_detalle/', listar_detalle.as_view(), name='listar_detalle'),    
    path('listar_empleados/', listar_empleados.as_view(), name='listar_empleados'),
    path('empleado_agregar/', empleado_agregar.as_view(), name='empleado_agregar'),
    path('empleado_actualizar/', empleado_actualizar.as_view(), name='empleado_actualizar'),
    path('empleado_actualizar/<int:employee_id>/', empleado_actualizar.as_view(), name='empleado_actualizar'),
    path('empleado_eliminar/', empleado_eliminar.as_view(), name='empleado_eliminar'),
    path('empleado_eliminar/<int:employee_id>', empleado_eliminar.as_view(), name='empleado_eliminar'),

   
       # horarios
    path('listar_horarios/', listar_horarios.as_view(), name='listar_horarios'),
    path('horario_agregar/', horario_agregar.as_view(), name='horario_agregar'),
    path('horaris_actualizar/', horario_actualizar.as_view(), name='horario_actualizar'),
    path('horario_actualizar/<str:identification>', horario_actualizar.as_view(), name='horario_actualizar'),
    path('horario_eliminar/', horario_eliminar.as_view(), name='horario_eliminar'),
    path('horario_eliminar/<str:identification>', horario_eliminar.as_view(), name='horario_eliminar'),


      # reporte
    path('EmployeeSalaryChartView/', EmployeeSalaryChartView.as_view(), name='EmployeeSalaryChartView'),
 ]

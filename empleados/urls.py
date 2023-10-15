from django.urls import path
from . import views
from .views import listar_empleado, empleado_agregar, empleados_actualizar, empleados_eliminar, listar_horarios, horario_agregar, horarios_actualizar, horarios_eliminar 

urlpatterns = [
        # empleados
    path('listar_empleados/', listar_empleado.as_view(), name='listar_empleados'),
    path('empleado_agregar/', empleado_agregar.as_view(), name='empleado_agregar'),
    path('empleados_actualizar/', empleados_actualizar.as_view(), name='empleados_actualizar'),
    path('empleados_actualizar/<str:identification>', empleados_actualizar.as_view(), name='empleados_actualizar'),
    path('empleados_eliminar/', empleados_eliminar.as_view(), name='empleados_eliminar'),
    path('empleados_eliminar/<str:identification>', empleados_eliminar.as_view(), name='empleados_eliminar'),

       # horarios
    path('listar_horarios/', listar_horarios.as_view(), name='listar_horarios'),
    path('horario_agregar/', horario_agregar.as_view(), name='horario_agregar'),
    path('horarios_actualizar/', horarios_actualizar.as_view(), name='horarios_actualizar'),
    path('horarios_actualizar/<str:identification>', horarios_actualizar.as_view(), name='horarios_actualizar'),
    path('horarios_eliminar/', horarios_eliminar.as_view(), name='horarios_eliminar'),
    path('horarios_eliminar/<str:identification>', horarios_eliminar.as_view(), name='horarios_eliminar'),

 ]
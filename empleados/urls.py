from django.urls import path
from . import views

urlpatterns = [
    path('listar_empleados/', views.listar_empleado),
    path('listar_horarios/', views.listar_horarios),
    path('empleado_agregar/', views.empleado_agregar),
    path('new/', views.listar_empleado, name='crear_empleado'),
 ]
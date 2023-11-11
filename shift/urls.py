from django.urls import path
from .views import ShiftList, ShiftAdd, ShiftUpdate, ShiftDelete
from empleados.views import Index

urlpatterns = [
   
    path('', Index.as_view(), name='index'),

       # horarios
    path('listar_horarios/', ShiftList.as_view(), name='listar_horarios'),
    path('horario_agregar/', ShiftAdd.as_view(), name='horario_agregar'),
    path('horario_actualizar/<int:id>', ShiftUpdate.as_view(), name='horario_actualizar'),
    path('horario_eliminar/<int:id>', ShiftDelete.as_view(), name='horario_eliminar'),

 ]

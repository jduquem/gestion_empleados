from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_empleado),
    path('new/', views.crear_empleado, name='crear_empleado'),
 ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar/', views.registrar_ingreso_salida, name='registrar_ingreso_salida')
]
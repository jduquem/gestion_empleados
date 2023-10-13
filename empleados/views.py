from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    return HttpResponse('<h1>Gestion de empleados</h1>')


from django.shortcuts import render
from .models import RegistroIngresoSalida
from .utils import calcular_horas_trabajadas

def registrar_ingreso_salida(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.POST['fecha']
        hora_ingreso = request.POST['hora_ingreso']
        hora_salida = request.POST['hora_salida']
        es_feriado = request.POST.get('es_feriado', False)
        
        # Crea un objeto RegistroIngresoSalida y guarda en la base de datos
        registro = RegistroIngresoSalida(
            fecha=fecha,
            hora_ingreso=hora_ingreso,
            hora_salida=hora_salida,
            es_feriado=es_feriado
        )
        registro.save()
        
        # Calcula las horas trabajadas y otros datos usando la función calcular_horas_trabajadas
        horas_trabajadas, es_nocturno, salario = calcular_horas_trabajadas(registro)
        
        # Puedes mostrar los resultados en otra plantilla o realizar otras acciones según tus necesidades
        return render(request, 'empleados/resultado_registro.html', {
            'registro': registro,
            'horas_trabajadas': horas_trabajadas,
            'es_nocturno': es_nocturno,
            'salario': salario
        })
    else:
        # Si no es una solicitud POST, muestra el formulario
        return render(request, 'empleados/formulario_registro.html')
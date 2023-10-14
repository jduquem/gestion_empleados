from django.shortcuts import render, redirect
from .models import Employee, Employee_Shift

def listar_empleado(request):
    empleados = Employee.objects.all()
    return render(request, 'empleado.html', {'empleados': empleados})

def listar_horarios(request):
    horarios = Employee_Shift.objects.all()
    return render(request, 'horario.html', {'horarios': horarios})

# def crear_empleado(request):
#     identification = request.POST['identification']
#     Nombre = request.POST['Nombre']
#     Correo = request.POST['Correo']
#     Numero_telefonico = request.POST['Numero_telefonico']
#     Salario = request.POST['Salario']
#     Ciudad_de_recidencia = request.POST['Ciudad_de_recidencia']
#     empleado = Employee(identification=identification, Nombre=Nombre, Correo=Correo, 
#                         Numero_telefonico = Numero_telefonico, Salario = Salario, 
#                         Ciudad_de_recidencia = Ciudad_de_recidencia )
#     empleado.save()
#     return redirect("empleado.html")

















































# # Definir la URL de la API y los parámetros
# api_url = "https://date.nager.at/api/v3/publicholidays/2023/CO"
# country_code = "CO"  # Código de país (ejemplo: Colombia)

# # Parámetros de la solicitud
# params = {
#     "CountryCode": country_code,
#     "Year": 2023  # Puedes ajustar el año
# }

# # Realizar la solicitud a la API
# response = requests.get(api_url, params=params)

# # Verificar si la solicitud fue exitosa
# if response.status_code == 200:
#     # La solicitud fue exitosa
#     holidays = response.json()
#     for holiday in holidays:
#         print(f"{holiday['date']}")

# else:
#     # La solicitud no fue exitosa
#     print(f"Error {response.status_code}: No se pudo obtener la información de días festivos.")


# # Define la fecha que quieres verificar
# fecha = datetime.date(2023, 10, 16)  # Formato: año, mes, día (2023-10-15)

# # Verifica si la fecha es un domingo (0 = lunes, 6 = domingo)
# es_domingo = fecha.weekday() == 6

# if es_domingo:
#     print(f"{fecha} es un domingo.")
# else:
#     print(f"{fecha} no es un domingo.")

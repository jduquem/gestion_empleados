import requests
from datetime import datetime
from .models import Employee

### Funcion para revisar feriados incluyendo domingos
def is_holiday(mydate):
    fecha_obj = datetime.strptime(mydate, '%Y-%m-%d')
    if date_is_holiday(fecha_obj) or is_sunday(fecha_obj):
        return True
    return False

### Funcion con la API para consutar festivos
def date_is_holiday(mydate):
    anio = mydate.year
    api_url = f"https://date.nager.at/api/v3/publicholidays/{anio}/CO"
    country_code = "CO"  
    params = {"CountryCode": country_code, "Year": anio}

    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        holidays = response.json()
        for holiday in holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
            if mydate.date() == holiday_date.date():
                return True
    else:
        # La solicitud no fue exitosa
        print(f"Error {response.status_code}: No se pudo obtener la información de días festivos.")
    return False

### Funcion para validar los domingos
def is_sunday(mydate):
    
    fechastr = mydate
    es_domingo = fechastr.weekday() == 6
    if es_domingo:
        print(f"{fechastr} es un domingo.")
        return True
    else:
        print(f"{fechastr} no es un domingo.")
        return False

### Funcion para calcular horas
def calculo_Horas(entry_time_str, departure_time_str):

    entry_time = datetime.strptime(entry_time_str, '%H:%M')
    departure_time = datetime.strptime(departure_time_str, '%H:%M')
    time_difference = departure_time - entry_time
    total_hours = time_difference.total_seconds() / 3600
    return total_hours

### Funcion para calcular el valor de las horas
def valor_hours(employee_id):
    
    salarioEmpleado = Employee.objects.filter(employee_id__in = employee_id)
    import pdb;pdb.set_trace()
    resultados = []

    # for horario in salarioEmpleado:
    #     salario = horario.employee.salary
    #     horas_trabajadas = horario.total_hours
    #     valor_horas = (salario / 240) * horas_trabajadas

    # resultados.append({
    #     'employee_id': horario.employee.employee_id,
    #     'employee_name': horario.employee.name,
    #     'salario': salario,
    #     'horas_trabajadas': horas_trabajadas,
    #     'valor_horas': valor_horas
    # })
    # context = {
        
    #     'resultados': resultados,
    #     'valor_calculado': valor_horas
    # }
    return valor_horas
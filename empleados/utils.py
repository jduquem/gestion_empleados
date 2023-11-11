import requests
from datetime import datetime, timedelta
from .models import Employee
from shift.models import EmployeeShift
import random
from django.db.models import Q

def shift_validations(employee_id, shifts, date_reg, entry_time_str, departure_time_str ):
    horarios_Cruzados = shifts.objects.filter(
        Q(employee_id=employee_id, date_reg=date_reg) &
        (
            Q(entry_time__lte=entry_time_str, departure_time__gte=entry_time_str) |
            Q(entry_time__lte=departure_time_str, departure_time__gte=departure_time_str)
        )
    )

    return horarios_Cruzados.exists()


def shift_validations_2(employee_id, shifts, date_reg, entry_time_str, departure_time_str, current_shift_id=None):
    horarios_Cruzados = shifts.objects.filter(
        Q(employee_id=employee_id, date_reg=date_reg) &
        (
            Q(entry_time__lte=entry_time_str, departure_time__gte=entry_time_str) |
            Q(entry_time__lte=departure_time_str, departure_time__gte=departure_time_str)
        )
    )

    # Exclude the current shift being edited (if provided)
    if current_shift_id:
        horarios_Cruzados = horarios_Cruzados.exclude(pk=current_shift_id)

    return horarios_Cruzados.exists()

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
def shift_hours(entry_time_str, departure_time_str):

    entry_time = datetime.strptime(entry_time_str, '%H:%M')
    departure_time = datetime.strptime(departure_time_str, '%H:%M')
    time_difference = departure_time - entry_time
    total_hours = time_difference.total_seconds() / 3600
    return total_hours

# ### Funcion para calcular el valor de las horas
def shift_money(hours, salary, is_holiday):
    return (salary / 240) * hours * (1.75 if is_holiday else 1)


def arreglo():
    # createshift()
    shifts = EmployeeShift.objects.all()
    try:
        for shift in shifts:
            print(shift.holiday)
            # print(shift.employee.salary)
            # print(shift.total_hours)
            start_datetime = datetime.combine(datetime.today(), shift.entry_time)
            end_datetime = datetime.combine(datetime.today(), shift.departure_time)

        # Calculate the duration as timedelta
            duration = end_datetime - start_datetime
            shift.total_hours = duration.seconds /3600.0
            shift.valor_hours = shift_money(shift.total_hours, shift.employee.salary, shift.holiday)
            shift.save()
    except Exception as e:
        print(e)
def createshift():
    
    shifts = random.randint(1, 10)
    employees = Employee.objects.all()
    
    for employee in employees:
        for i in range(1,50):
            print(employee.name)
            date_reg = fecha()
            entry_time, departure_time = horarios()
            holiday = is_holiday(date_reg)
            total_hours = 8
            valor_hours = 20000
            if shift_validations(employee.employee_id, EmployeeShift, date_reg, entry_time, departure_time ):
                EmployeeShift.objects.create(employee_id = employee.employee_id, date_reg=date_reg, entry_time=entry_time, departure_time=departure_time, holiday=holiday, total_hours=total_hours, valor_hours=valor_hours)



def horarios():
    
    return generate_random_shift()

def fecha():

# Function to generate a random date in yyyy-mm-dd format within the year 2023

    # Generate a random month between 1 and 12
    month = random.randint(1, 12)
    
    # Generate a random day between 1 and the maximum number of days in the selected month and year (2023)
    max_day = (datetime(2023, month % 12 + 1, 1) - timedelta(days=1)).day
    day = random.randint(1, max_day)
    
    # Format the date as yyyy-mm-dd
    random_date = f'2023-{month:02d}-{day:02d}'
    
    return random_date

def generate_random_shift():
    # Specify the start and end times for the shift (in 24-hour format)
    start_time = '08:00:00'
    end_time = '20:00:00'
    
    # Convert start and end times to datetime objects
    start_datetime = datetime.strptime(start_time, '%H:%M:%S')
    end_datetime = datetime.strptime(end_time, '%H:%M:%S')
    
    # Calculate the time duration of the shift
    shift_duration = end_datetime - start_datetime
    
    # Generate random start time within the specified range
    random_start_time = start_datetime + timedelta(seconds=random.randint(0, shift_duration.total_seconds()))
    
    # Generate random end time within the specified range
    random_end_time = random_start_time + timedelta(seconds=random.randint(0, shift_duration.total_seconds()))
    
    # Format the shift times as HH:MM:SS
    random_start = random_start_time.strftime('%H:%M:%S')
    random_end = random_end_time.strftime('%H:%M:%S')
    
    return random_start, random_end
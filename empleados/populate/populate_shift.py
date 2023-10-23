from faker import Faker
from empleados.models import EmployeeShift, Employee
from django.contrib.auth.models import User, Group
import random
from datetime import datetime, timedelta

def populate_shifts(cant):
    try:
        employees = Employee.objects.all()
        
        fake = Faker('es_CO')  # 'es_CO' generates data specifically for Colombia

        for employee in employees:
            n_shift = random.randint(1, 10)
            for _ in range(30):
                date_reg = fake.date_this_year()
                # import pdb;  pdb.set_trace()
                entry_time = datetime.combine(date_reg, datetime.min.time()) + timedelta(hours=random.randint(6, 10))
                departure_time = entry_time + timedelta(hours=random.randint(6, 10))
                holiday = False
                total_hours = 0
                valor_hours = 0

                shift = EmployeeShift(
                    employee=employee,
                    date_reg=date_reg,
                    entry_time=entry_time.time(),
                    departure_time=departure_time.time(),
                    holiday=holiday,
                    total_hours=total_hours,
                    valor_hours=valor_hours
                )
                shift.save()
    except Exception as e:
            print(e)
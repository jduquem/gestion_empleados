from faker import Faker
from empleados.models import Employee

fake = Faker('es_CO')  # 'es_CO' generates data specifically for Colombia

# Assuming you have the Employee model defined already
for _ in range(100):
    name = fake.name()
    gender = fake.random_element(elements=('M', 'F', 'O'))
    email = fake.email()
    numberphone = fake.phone_number()
    salary = fake.random_int(min=20000, max=1000000)  # Random salary between 20,000 and 1,000,000
    city = fake.city()
    
    # Create Employee instance and save to the database
    employee = Employee(
        name=name,
        gender=gender,
        email=email,
        numberphone=numberphone,
        salary=salary,
        city=city
    )
    employee.save()
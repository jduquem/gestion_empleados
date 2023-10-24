from faker import Faker
from empleados.models import Employee
from django.contrib.auth.models import User, Group

def populate_employees(cant):
    fake = Faker('es_CO')  # 'es_CO' generates data specifically for Colombia

    for _ in range(cant):
        try:
            username = str(fake.random_int(min=100000, max=999999))
            name = fake.name()
            gender = fake.random_element(elements=('M', 'F', 'O'))
            email = fake.email()
            numberphone = fake.random_int(min=3000000000, max=3190000000)
            salary = fake.random_int(min=1000000, max=10000000)  # Random salary between 20,000 and 1,000,000
            city = fake.city()

            user = User.objects.create_user(username=username, email=email, password=username)
            user.groups.add(Group.objects.get(name='Empleados'))
            user.save()

            employee = Employee(
                user=user,
                identification=username,
                name=name,
                gender=gender,
                email=email,
                numberphone=numberphone,
                salary=salary,
                city=city
            )
            employee.save()
        except Exception as e:
            print(e)
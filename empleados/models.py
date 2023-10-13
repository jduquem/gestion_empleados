from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

admin_group = Group.objects.create(name='Administrador')
empleado_group = Group.objects.create(name='Empleado')

user = User.objects.create_user(username='admin', password='adminpassword')
user.groups.add(admin_group)

empleado = User.objects.create_user(username='emleado', password='empleadopassword')
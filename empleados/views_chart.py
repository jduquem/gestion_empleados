from .models import Employee, EmployeeShift
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import arreglo
import json

class Chart(LoginRequiredMixin, View):
    template_name = 'empleado/empleado_eliminar.html'

    def get(self, request):
        context = {'data':100}
        return render(request, 'nomina/chart.html', context)        

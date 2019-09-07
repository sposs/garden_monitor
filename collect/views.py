# -*- coding: UTF-8 -*-
from collect.models import Measurement
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse
from collect import grovepi

@never_cache
def list_of_measurements(request):
   measurements = Measurement.objects.all().order_by("date")
   return render(request, "measures.html", {"measures": measurements})

def measure(request):
    sensor = settings.SENSOR
    try:
        measure = grovepi.analogRead(sensor)
    except IOError:
        measure = "Error"
    return HttpResponse(measure)



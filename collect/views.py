# -*- coding: UTF-8 -*-
import random

from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
import logging

from collect.models import Sensor
from collect.utils import get_plot

logger = logging.getLogger("garden_monitor.collect.views")
try:
    from collect import grovepi
except ImportError:
    grovepi = None
    logger.error("Not on the appropriate device")


@never_cache
def list_of_measurements(request):
    sensors = Sensor.objects.all()
    return render(request, "measures.html", {"rnd": random.random(), "sensors": sensors})


@never_cache
def get_data(request):
    sensor = None
    if request.GET.get("sensor_id") is not None:
        sensor = Sensor.objects.get(id=request.GET["sensor_id"])
    f_name = get_plot(request.GET.get("rnd", 0), sensor)
    with open(f_name, "rb") as data:
        res = HttpResponse(data.read(), content_type="image/png")
        return res


def do_measure(request, sensor_id):

    sensor = Sensor.objects.get(id=sensor_id)
    try:
        if sensor.rpi_type == "analog":
            measure = grovepi.analogRead(sensor.rpi_port)
        else:
            measure = grovepi.digitalRead(sensor.rpi_port)
    except IOError:
        measure = "Error"
    except Exception as err:
        measure = "No grovepi"
        logger.exception(err)
    return HttpResponse(measure)



# -*- coding: UTF-8 -*-
import random

from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
import logging

from collect.models import Sensor, EncoderMeasurement
from collect.probes import measure, relay
from collect.utils import get_plot

logger = logging.getLogger("garden_monitor.collect.views")


@never_cache
def list_of_measurements(request):
    sensors = Sensor.objects.all()
    return render(request, "measures.html", {"rnd": random.random(), "sensors": sensors})


@never_cache
def get_data(request):
    sensor = None
    if request.GET.get("sensor_id") is not None:
        sensor = Sensor.objects.get(id=request.GET["sensor_id"])
    p = get_plot(request.GET.get("rnd", 0), sensor)
    res = HttpResponse(p.file.read(), content_type="image/png")
    return res


def do_measure(request, sensor_id):
    value = measure(sensor_id)
    return HttpResponse(value)


def encoder(request, encoder_id):
    measures = EncoderMeasurement.objects.filter(sensor_id=encoder_id)
    if measures.exists():
        value = measures.latest().value
    else:
        value = "Nothing yet"
    return HttpResponse(value)


def relay_req(request, op, relay_id):
    error = relay(op, relay_id)
    return HttpResponse("has error: %s" % error)

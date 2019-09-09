# -*- coding: UTF-8 -*-
import random

from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse
import logging

from collect.utils import get_plot

logger = logging.getLogger("garden_monitor.collect.views")
try:
    from collect import grovepi
except ImportError:
    grovepi = None
    logger.error("Not on the appropriate device")


@never_cache
def list_of_measurements(request):
    return render(request, "measures.html", {"rnd": random.random()})


@never_cache
def get_data(request):
    f_name = get_plot(request.get("rnd", 0))
    with open(f_name, "rb") as data:
        res = HttpResponse(data.read(), content_type="image/png")
        return res


def do_measure(request):
    sensor = settings.SENSOR
    try:
        measure = grovepi.analogRead(sensor)
    except IOError:
        measure = "Error"
    except Exception as err:
        measure = "No grovepi"
        logger.exception(err)
    return HttpResponse(measure)



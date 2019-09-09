# -*- coding: UTF-8 -*-
import os
import random
import tempfile

from collect.models import Measurement
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse
import matplotlib.pyplot as plt
import logging
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
    measurements = Measurement.objects.filter(value__gt=10).order_by("date")
    datax = []
    datay = []
    tmp_dir = tempfile.mkdtemp()
    f_name = os.path.join(tmp_dir, "test%s.png" % request.GET.get("rnd", 0))
    for idx, measure in enumerate(measurements):
        if idx % 20:
            datax.append(measure.date.strftime("%s"))
        else:
            datax.append(None)
        datay.append(measure.value)
    fig, ax = plt.subplots()
    ax.plot(datax, datay)

    ax.set(xlabel='time (s)', ylabel='Moist level',
           title='Moist level evolution')
    fig.savefig(f_name)
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



# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from collect.models import Measurement, Sensor
from collect.probes import measure

try:
    from collect import grovepi
except ImportError:
    grovepi = None
import logging

logger = logging.getLogger("garden_monitor.collect.measure")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sensors = Sensor.objects.filter(state=Sensor.State.ON)
        for sensor in sensors:
            val = measure(sensor.id)
            if not isinstance(val, float):
                continue
            if sensor.min_value is not None and val < sensor.min_value:
                continue
            Measurement.objects.create(sensor=sensor, value=val)

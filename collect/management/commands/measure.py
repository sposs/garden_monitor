# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from collect.models import Measurement, Sensor

try:
    from collect import grovepi
except ImportError:
    grovepi = None
import logging

logger = logging.getLogger("garden_monitor.collect.measure")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sensors = Sensor.objects.all()
        for sensor in sensors:
            try:
                if sensor.rpi_type == "analog":
                    val = grovepi.analogRead(sensor.rpi_port)
                else:
                    val = grovepi.digitalRead(sensor.rpi_port)
            except IOError:
                logger.error("Failed reading")
                return
            except Exception as err:
                logger.exception(err)
                return
            Measurement.objects.create(sensor=sensor, value=val)

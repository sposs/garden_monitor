# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from collect.models import Measurement
try:
    from collect import grovepi
except ImportError:
    grovepi = None
from django.conf import settings
import logging

logger = logging.getLogger("garden_monitor.collect.measure")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            val = grovepi.analogRead(settings.SENSOR)
        except IOError:
            logger.error("Failed reading")
            return
        except Exception as err:
            logger.exception(err)
            return
        Measurement.objects.create(value=val)

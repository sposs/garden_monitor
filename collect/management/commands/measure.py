# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from collect.models import Measurement
from collect import grovepi
from django.conf import settings

class Command(BaseCommand):
   def handle(self, *args, **kwargs):
      try:
          val = grovepi.analogRead(settings.SENSOR)
      except IOError:
          print(error)
          return
      Measurement.objects.create(value=val)

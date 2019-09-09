# -*- coding: UTF-8 -*-
import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import BaseCommand

from collect.models import Sensor
from collect.utils import get_plot


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.utcnow()
        email = EmailMessage(
            'Garden monitor report',
            'Data for %s' % now.strftime("%Y-%m-%d"),
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_RECIPIENT],
            None
        )
        sensors = Sensor.objects.all()
        for sensor in sensors:
            f_name = get_plot(sensor=sensor)
            with open(f_name, "rb") as data:
                email.attach("plot_%s.png" % sensor.name, data.read(), "image/png")
        email.send()

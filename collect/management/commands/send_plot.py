# -*- coding: UTF-8 -*-
import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.utils import timezone

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
        now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
        yesterday = now - datetime.timedelta(days=1)
        sensors = Sensor.objects.all()
        for sensor in sensors:
            f_name = get_plot(sensor=sensor)
            with open(f_name, "rb") as data:
                email.attach("plot_%s.png" % sensor.name, data.read(), "image/png")
            f_name = get_plot(sensor=sensor, from_date=yesterday)
            with open(f_name, "rb") as data:
                email.attach("plot_%s_%s.png" % (sensor.name, yesterday.strftime("%Y%m%d%H%M")),
                             data.read(), "image/png")

        email.send()

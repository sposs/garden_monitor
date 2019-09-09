# -*- coding: UTF-8 -*-
import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import BaseCommand

from collect.utils import get_plot


class Command(BaseCommand):
    def handle(self, *args, **options):
        f_name = get_plot()
        now = datetime.datetime.utcnow()
        email = EmailMessage(
            'Garden monitor report',
            'Data for %s' % now.strftime("%Y-%m-%d"),
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_RECIPIENT],
            None
        )
        with open(f_name, "rb") as data:
            email.attach("plot.png", data.read(), "image/png")
        email.send()

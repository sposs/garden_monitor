import logging

from django.core.management.base import BaseCommand

from collect.models import Encoder

logger = logging.getLogger("garden_monitor.collect.check_encoder")


class Command(BaseCommand):
    def handle(self, *args, **options):
        encoders = Encoder.objects.all()
        for encoder in encoders:
            if encoder.measures.latest() > encoder.limits.max_value:
                logger.error("Alert: upper limit of %s reached", encoder.name)
            if encoder.measures.latest() < encoder.limits.min_value:
                logger.error("Alert: lower limit of %s reached", encoder.name)

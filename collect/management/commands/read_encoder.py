import time

from django.core.management.base import BaseCommand

from collect import grovepi
from collect.models import Encoder, EncoderMeasurement
import logging

logger = logging.getLogger("garden_monitor.collect.encoder")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("encoder_id", help="the encoder ID")

    def handle(self, *args, **options):
        encoder = Encoder.objects.get(id=options["encoder_id"])
        grovepi.encoder_en(pin=encoder.rpi_port, steps=encoder.steps)
        while True:
            try:
                last_value = grovepi.encoderRead(pin=encoder.rpi_port)
                if last_value != EncoderMeasurement.objects.all().latest().value:
                    EncoderMeasurement.objects.create(value=last_value, sensor=encoder)
                time.sleep(encoder.refresh_interval)
            except KeyboardInterrupt:
                break
            except Exception as err:
                logger.exception(err)
                break
        grovepi.encoder_dis(pin=encoder.rpi_port)

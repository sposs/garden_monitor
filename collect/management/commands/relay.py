# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from collect.models import Measurement, Sensor, Relay
from collect.probes import relay, toggle_relay

try:
    from collect import grovepi
except ImportError:
    grovepi = None
import logging

logger = logging.getLogger("garden_monitor.collect.relay")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--relay", dest="relay_name", required=False)
        parser.add_argument("--state", dest="state", choices=[Relay.State.ON, Relay.State.OFF], required=False)

    def handle(self, *args, **options):
        if options.get("relay_name"):
            relays = Relay.objects.filter(name__icontains=options["relay_name"])
        else:
            relays = Relay.objects.all()
        if options.get("state"):
            final_state = options["state"]
        else:
            final_state = None
        for rel in relays:
            if final_state:
                err = relay(final_state, rel.id)
            else:
                err = toggle_relay(rel.id)
            logger.info("Relay %s has error: %s", rel.name, err)

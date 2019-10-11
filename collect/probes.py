# -*- coding: UTF-8 -*-
import logging

from collect.models import Sensor, Relay

logger = logging.getLogger("garden_monitor.collect.probes")
try:
    from collect import grovepi
except ImportError:
    grovepi = None
    logger.warning("Not on the appropriate device")


def measure(sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    try:
        if sensor.rpi_type == "analog":
            value = grovepi.analogRead(sensor.rpi_port)
        else:
            value = grovepi.digitalRead(sensor.rpi_port)
        value = float(value)
    except IOError:
        value = "Error"
    except Exception as err:
        value = "No grovepi"
        logger.exception(err)
    return value


def relay(op, relay_id):
    relaydb = Relay.objects.get(id=relay_id)
    try:
        if relaydb.rpi_type == "analog":
            if op == "on":
                if relaydb.state == relaydb.State.OFF:
                    grovepi.analogWrite(relaydb.rpi_port, 1)
                    relaydb.state = relaydb.State.ON
            else:
                if relaydb.state == relaydb.State.ON:
                    grovepi.analogWrite(relaydb.rpi_port, 0)
                    relaydb.state = relaydb.State.OFF
        else:
            grovepi.pinMode(relaydb.rpi_port, "OUTPUT")
            if op == "on":
                if relaydb.state == relaydb.State.OFF:
                    grovepi.digitalWrite(relaydb.rpi_port, 1)
                    relaydb.state = relaydb.State.ON
            else:
                if relaydb.state == relaydb.State.ON:
                    grovepi.digitalWrite(relaydb.rpi_port, 0)
                    relaydb.state = relaydb.State.OFF
        error = False
        relaydb.save()
    except IOError:
        error = True
    except Exception as err:
        error = "No grovepi"
        logger.exception(err)
    return error


def toggle_relay(relay_id):
    relaydb = Relay.objects.get(id=relay_id)
    if relaydb.state == relaydb.State.ON:
        error = relay("off", relay_id)
    else:
        error = relay("on", relay_id)
    return error

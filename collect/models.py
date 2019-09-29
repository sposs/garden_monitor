# -*- coding: utf-8 -*-
from django.db import models


class Relay(models.Model):

    class State:
        ON = "on"
        OFF = "off"

    name = models.CharField(max_length=50, unique=True)
    rpi_port = models.IntegerField()
    rpi_type = models.CharField(max_length=100, choices=(("analog", "Analog"), ("digital", "Digital")),
                                default="digital")
    state = models.CharField(max_length=4, choices=((State.ON, "On"), (State.OFF, "Off")), default="off")

    def __unicode__(self):
        return u"%s" % self.name


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rpi_port = models.IntegerField()
    rpi_type = models.CharField(max_length=100, choices=(("analog", "Analog"), ("digital", "Digital")),
                                default="analog")
    plot_y_axis_label = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(null=True)

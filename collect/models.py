# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Relay(models.Model):

    class State:
        ON = "on"
        OFF = "off"
        @classmethod
        def state_for_value(cls, val):
            if val.lower() == 'on':
                return cls.ON
            else:
                return cls.OFF

    name = models.CharField(max_length=50, unique=True)
    rpi_port = models.IntegerField()
    rpi_type = models.CharField(max_length=100, choices=(("analog", "Analog"), ("digital", "Digital")),
                                default="digital")
    state = models.CharField(max_length=4, choices=((State.ON, "On"), (State.OFF, "Off")), default="off")

    def __unicode__(self):
        return u"%s" % self.name


class Sensor(models.Model):
    class State:
        ON = "on"
        OFF = "off"
        @classmethod
        def state_for_value(cls, val):
            if val.lower() == 'on':
                return cls.ON
            else:
                return cls.OFF

    name = models.CharField(max_length=50, unique=True)
    rpi_port = models.IntegerField()
    rpi_type = models.CharField(max_length=100, choices=(("analog", "Analog"), ("digital", "Digital")),
                                default="analog")
    plot_y_axis_label = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=4, choices=((State.ON, "On"), (State.OFF, "Off")), default="off")

    max_value = models.IntegerField(null=True, blank=True)
    min_value = models.IntegerField(default=0)

    power_relay = models.ForeignKey(Relay, null=True, blank=True, on_delete=models.SET_NULL, related_name="probes")

    def __unicode__(self):
        return u"%s" % self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, related_name="measures")
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(null=True)


class Encoder(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rpi_port = models.IntegerField(default=2)
    steps = models.IntegerField(default=32)
    refresh_interval = models.IntegerField(help_text="In seconds", default=5)

    def __unicode__(self):
        return u"%s" % self.name


class EncoderMeasurement(models.Model):
    sensor = models.ForeignKey(Encoder, on_delete=models.CASCADE, related_name="measures")
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(null=True)

    class Meta:
        get_latest_by = "date"
        ordering = ("-date", )

    def __unicode__(self):
        return "%s - %s" % (self.sensor, self.value)


class EncoderLimit(models.Model):
    sensor = models.OneToOneField(Encoder, on_delete=models.CASCADE, related_name="limits")
    min_value = models.IntegerField()
    max_value = models.IntegerField()

    def __unicode__(self):
        return self.sensor.name


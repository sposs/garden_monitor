# -*- coding: utf-8 -*-
from django.contrib import admin
from collect.models import Measurement, Sensor


class MeasureAdmin(admin.ModelAdmin):
    list_display = ("date", "value")


class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "rpi_type", "rpi_port")


admin.site.register(Measurement, MeasureAdmin)
admin.site.register(Sensor, SensorAdmin)


# -*- coding: utf-8 -*-
from django.contrib import admin
from collect.models import Measurement, Sensor, Relay, Encoder, EncoderMeasurement, EncoderLimit


class MeasureAdmin(admin.ModelAdmin):
    list_display = ("date", "sensor", "value")
    list_filter = ("sensor", )
    date_hierarchy = "date"


class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "rpi_type", "rpi_port")
    list_filter = ("rpi_type", )


class RelayAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "rpi_type", "rpi_port")
    list_filter = ("state", "rpi_type", )


admin.site.register(Measurement, MeasureAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Relay, RelayAdmin)
admin.site.register(Encoder)
admin.site.register(EncoderMeasurement)
admin.site.register(EncoderLimit)



# -*- coding: utf-8 -*-
from django.contrib import admin
from collect.models import Measurement

class MeasureAdmin(admin.ModelAdmin):
   list_display = ("date", "value")

admin.site.register(Measurement, MeasureAdmin)


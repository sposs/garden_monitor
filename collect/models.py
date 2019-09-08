# -*- coding: utf-8 -*-
from django.db import models


class Measurement(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(null=True)

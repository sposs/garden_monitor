# -*- coding: UTF-8 -*-

from django.conf.urls import url
from collect.views import list_of_measurements, measure

urlpatterns = [
  url(r"^$", list_of_measurements),
  url(r"^measure$", measure),
]

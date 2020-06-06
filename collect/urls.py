# -*- coding: UTF-8 -*-

from django.conf.urls import url
from collect.views import list_of_measurements, do_measure, get_data, relay_req, encoder

urlpatterns = [
  url(r"^$", list_of_measurements, name="index"),
  url(r"^measure/(?P<sensor_id>\d*)$", do_measure, name="measure"),
  url(r"^encoder/(?P<encoder_id>\d*)$", encoder, name="encoder"),
  url(r"^get_data$", get_data, name="get_data"),
  url(r"^relay/(?P<op>on|off)/(?P<relay_id>\d*)$", relay_req, name="relay"),

]

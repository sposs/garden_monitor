# -*- coding: UTF-8 -*-

from django.conf.urls import url
from collect.views import list_of_measurements, do_measure, get_data, relay_req

urlpatterns = [
  url(r"^$", list_of_measurements, name="index"),
  url(r"^measure/(?P<sensor_id>\d*)$", do_measure, name="measure"),
  url(r"^get_data$", get_data, name="get_data"),
  url(r"^relay/(?P<op>on|off)/(?P<relay_id>\d*)$", relay_req, name="relay"),

]

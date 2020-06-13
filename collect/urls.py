# -*- coding: UTF-8 -*-

from django.urls import path, re_path

from collect.views import list_of_measurements, do_measure, get_data, relay_req, encoder
app_name = "collect"
urlpatterns = [
  path("", list_of_measurements, name="index"),
  path("measure/<sensor_id>", do_measure, name="measure"),
  path("encoder/<encoder_id>", encoder, name="encoder"),
  path("get_data", get_data, name="get_data"),
  re_path(r"relay/(?P<op>on|off)/(?P<relay_id>\d*)$", relay_req, name="relay"),

]

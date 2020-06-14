# -*- coding: UTF-8 -*-
import os
import tempfile
import matplotlib.pyplot as plt
from django.core.files import File
from django.core.management import call_command
from matplotlib import dates
from matplotlib.dates import DateFormatter

from collect.models import Measurement, Sensor, Relay, PlotFile
import re

message_re = re.compile(r"^(sensor (?P<sensor_name>[0-9]+|[a-z ]+) (?P<sensor_status>on|off)|relay (?P<relay_name>[0-9]+|[a-z ]+) (?P<relay_status>on|off)|(?P<plot>get plots))", re.I)


def get_plot(rnd=0, sensor=None, from_date=None, to_date=None):
    measurements = Measurement.objects.filter(value__gt=10)
    plot_y_label = "Any"
    if sensor is not None:
        measurements = measurements.filter(sensor=sensor)
        if sensor.plot_y_axis_label:
            plot_y_label = sensor.plot_y_axis_label
    if from_date:
        measurements = measurements.filter(date__gte=from_date)
    if to_date:
        measurements = measurements.filter(date__lte=to_date)
    measurements = measurements.order_by("date")
    datax = []
    datay = []
    tmp_dir = tempfile.mkdtemp()
    f_name = os.path.join(tmp_dir, "test%s.png" % rnd)
    for idx, measure in enumerate(measurements):
        datax.append(measure.date)
        datay.append(measure.value)
    formatter = DateFormatter('%d/%m %H:%M')
    dat = dates.date2num(datax)
    fig, ax = plt.subplots()
    ax.plot_date(dat, datay, "-")
    ax.xaxis.set_major_formatter(formatter)
    plt.gcf().autofmt_xdate()

    ax.set(xlabel='time (s)', ylabel=plot_y_label)
    fig.savefig(f_name)
    pname = sensor.name
    while " " in pname:
        pname = pname.replace(" ", "_")
    p = PlotFile.objects.create(sensor=sensor)
    p.measurements.set(list(measurements))
    with open(f_name) as data:
        p.file.save("plot_%s_%s.png" % (pname, p.date.strftime("%Y%m%d%H%i")), File(data))
    return p


def parse_message(message):
    res = message_re.match(message)
    if not res:
        raise Exception("Invalid string")
    if res.group("sensor_name"):
        try:
            sensor_name = int(res.group("sensor_name"))
            sensor = Sensor.objects.get(id=sensor_name)
        except ValueError:
            sensor_name = res.group("sensor_name")
            sensor = Sensor.objects.get(name__icontains=sensor_name)
        sensor.state = sensor.State.state_for_value(res.group("sensor_status"))
        sensor.save()
    if res.group("relay_name"):
        try:
            relay_name = int(res.group("relay_name"))
            relay = Relay.objects.get(id=relay_name)
        except ValueError:
            relay_name = res.group("relay_name")
            relay = Relay.objects.get(name__icontains=relay_name)
        relay.state = relay.State.state_for_value(res.group("relay_status"))
        relay.save()
    if res.group("plot"):
        call_command("send_plot")

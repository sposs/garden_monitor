# -*- coding: UTF-8 -*-
import os
import tempfile
import matplotlib.pyplot as plt

from collect.models import Measurement, Sensor


def get_plot(rnd=0, sensor=None):
    measurements = Measurement.objects.filter(value__gt=10)
    plot_y_label = "Any"
    if sensor is not None:
        measurements = measurements.filter(sensor=sensor)
        if sensor.plot_y_axis_label:
            plot_y_label = sensor.plot_y_axis_label
    measurements = measurements.order_by("date")
    datax = []
    datay = []
    tmp_dir = tempfile.mkdtemp()
    f_name = os.path.join(tmp_dir, "test%s.png" % rnd)
    for idx, measure in enumerate(measurements):
        if idx % 20:
            datax.append(measure.date.strftime("%s"))
        else:
            datax.append(None)
        datay.append(measure.value)
    fig, ax = plt.subplots()
    ax.plot(datax, datay)

    ax.set(xlabel='time (s)', ylabel=plot_y_label)
    fig.savefig(f_name)
    return f_name

# -*- coding: UTF-8 -*-
import os
import tempfile
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import dates
from matplotlib.dates import DateFormatter

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
        #if idx % 20:
        datax.append(measure.date)
        #else:
        #    datax.append(None)
        datay.append(measure.value)
    formatter = DateFormatter('%d/%m %H:%M')
    dat = dates.date2num(datax)
    fig, ax = plt.subplots()
    ax.plot_date(dat, datay, "-")
    ax.xaxis.set_major_formatter(formatter)
    plt.gcf().autofmt_xdate()

    ax.set(xlabel='time (s)', ylabel=plot_y_label)
    fig.savefig(f_name)
    return f_name

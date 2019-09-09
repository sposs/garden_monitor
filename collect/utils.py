# -*- coding: UTF-8 -*-
import os
import tempfile
import matplotlib.pyplot as plt

from collect.models import Measurement


def get_plot(rnd=0):
    measurements = Measurement.objects.filter(value__gt=10).order_by("date")
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

    ax.set(xlabel='time (s)', ylabel='Moist level',
           title='Moist level evolution')
    fig.savefig(f_name)
    return f_name

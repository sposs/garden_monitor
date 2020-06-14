import datetime
import email
import imaplib

from django.conf import settings
from celery import shared_task

from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone

from collect.models import Sensor, Measurement, PlotFile
from collect.probes import measure
from collect.utils import parse_message, get_plot

logger = get_task_logger(__name__)


@shared_task(ignore_result=True)
def measure_async():
    sensors = Sensor.objects.filter(state=Sensor.State.ON)
    for sensor in sensors:
        val = measure(sensor.id)
        try:
            val = float(val)
        except ValueError:
            logger.error("Not a float %s", val)
            continue
        if sensor.min_value is not None and val < sensor.min_value:
            continue
        logger.info("Saving measurement for sensor %s", sensor.name)
        Measurement.objects.create(sensor=sensor, value=val)


@shared_task(ignore_result=True)
def get_commands_async():
    conn = imaplib.IMAP4_SSL(host=settings.EMAIL_IMAP)
    conn.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    conn.select()
    typ, data = conn.search(None, "(NEW SUBJECT command)")
    if typ != "OK":
        conn.logout()
        logger.exception("Cannot read emails")
        return
    mail_ids = data[0].split()
    for email_id in mail_ids:
        typ, data = conn.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        parts = email_message.get_payload()
        if not isinstance(parts, list):
            parts = [parts]
        message = None
        for part in parts:
            message = part.get_payload().strip()
            break
        try:
            parse_message(message)
        except Exception as err:
            logger.exception(err)
    conn.logout()


@shared_task(ignore_result=True)
def send_plot_async():
    t = loader.get_template("plot_email.html")
    now = timezone.now()
    yesterday = now - datetime.timedelta(days=1)
    sensors = Sensor.objects.all()
    mail = EmailMultiAlternatives(
        'Garden monitor report %s' % now.strftime("%Y-%m-%d"),
        'Data for %s' % now.strftime("%Y-%m-%d"),
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_RECIPIENT],
    )
    c = {"data": {}}
    for sensor in sensors:
        p1 = get_plot(sensor=sensor)
        p2 = get_plot(sensor=sensor, from_date=yesterday)
        c["data"][sensor] = [p1, p2]
        mail.attach(p1.file.name, p1.file.read(), "image/png")
        mail.attach(p2.file.name, p2.file.read(), "image/png")
    message = t.render(c)
    mail.attach_alternative(message, "text/html")
    mail.send()


@shared_task(ignore_result=True)
def clean_old_plots():
    old_times = timezone.now() - datetime.timedelta(days=10)
    old = PlotFile.objects.filter(date__lt=old_times)
    logger.info("Removing %s old plots", old.count())
    for o in old:
        o.file.delete()
        o.delete()

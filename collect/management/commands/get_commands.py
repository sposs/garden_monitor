# -*- coding: UTF-8 -*-
import email
import imaplib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from collect.utils import parse_message
import logging

logger = logging.getLogger("garden_monitor.read_mails")


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = imaplib.IMAP4_SSL(host=settings.EMAIL_IMAP)
        conn.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        conn.select()
        typ, data = conn.search(None, "(NEW SUBJECT command)")
        if typ != "OK":
            conn.logout()
            raise CommandError("Cannot read emails")
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

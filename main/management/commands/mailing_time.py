""""Ручной запуск рассылок"""

import logging
import datetime
import smtplib
from django.core.management import BaseCommand

from django.conf import settings
from django.utils import timezone

from main.models import Mailing, Attempt
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):


    def handle(self, *args, **options):

        cur_time = timezone.now()
        current_time = cur_time.replace(second=0, microsecond=0)

        mailings = Mailing.objects.filter(first_sending__lte=current_time, status='new', is_active=True)
        for mailing in mailings:
            mailing.last_sending = current_time

            if mailing.periodicity == 'daily':
                mailing.next_sending = current_time + datetime.timedelta(days=1)

            elif mailing.periodicity == 'weekly':
                mailing.next_sending = current_time + datetime.timedelta(days=7)

            elif mailing.periodicity == 'monthely':
                mailing.next_sending = current_time + datetime.timedelta(days=30)
            else:
                pass
            mailing.status = 'started'
            mailing.save()

            try:
                send_mail(
                    subject=mailing.notification.subject,
                    message=mailing.notification.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False
                )
                Attempt.objects.create(attempt_time=str(current_time), status=True, server_answer='Success',
                                       mailing=mailing,
                                       owner=mailing.owner)
            except smtplib.SMTPException as error:
                Attempt.objects.create(attempt_time=str(current_time), status=False, server_answer=error,
                                       mailing=mailing,
                                       owner=mailing.owner)

            # self.mailing_status_change(mailing, current_time)

        mailings = Mailing.objects.filter(next_sending__lte=current_time, status='started', is_active=True)
        for mailing in mailings:
            # self.mailing_status_change(mailing, current_time)
            mailing.last_sending = current_time

            if mailing.periodicity == 'daily':
                mailing.next_sending = current_time + datetime.timedelta(days=1)

            elif mailing.periodicity == 'weekly':
                mailing.next_sending = current_time + datetime.timedelta(days=7)

            elif mailing.periodicity == 'monthely':
                mailing.next_sending = current_time + datetime.timedelta(days=30)
            else:
                pass
            mailing.status = 'started'
            mailing.save()

            try:
                send_mail(
                    subject=mailing.notification.subject,
                    message=mailing.notification.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False
                )
                Attempt.objects.create(attempt_time=str(current_time), status=True, server_answer='Success',
                                       mailing=mailing,
                                       owner=mailing.owner)
            except smtplib.SMTPException as error:
                Attempt.objects.create(attempt_time=str(current_time), status=False, server_answer=error,
                                       mailing=mailing,
                                       owner=mailing.owner)

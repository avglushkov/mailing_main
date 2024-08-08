from config import settings
from django.core.mail import send_mail
from django.utils import timezone
from main.models import Mailing, Attempt
import datetime
import smtplib


def mailing_status_change(mailing, current_time):
    """Отправка рассылки с формированием строки в логе"""

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.notification.subject,
                message=mailing.notification.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            Attempt.objects.create(attempt_time=str(current_time), status=True, server_answer='Success', mailing=mailing,
                               owner=mailing.owner, client=client.email)
        except smtplib.SMTPException as error:
            Attempt.objects.create(attempt_time=str(current_time), status=False, server_answer=error, mailing=mailing,
                               owner=mailing.owner, client=client.email)

    mailing.last_sending = current_time
    if mailing.periodicity == 'daily':
        mailing.next_sending = current_time + datetime.timedelta(days=1)
    elif mailing.periodicity == 'weekly':
        mailing.next_sending = current_time + datetime.timedelta(days=7)
    elif mailing.periodicity == 'monthely':
        mailing.next_sending = current_time + datetime.timedelta(days=30)
    else:
        pass
    mailing.save()


def time_check():
    """Получение списка рассылок, которые нужно разослать"""

    cur_time = timezone.now()
    current_time = cur_time.replace(second=0, microsecond=0)
    mailings = Mailing.objects.filter(first_sending__lte=current_time, status='new', is_active=True)

    for mailing in mailings:
        mailing.status = 'started'
        mailing_status_change(mailing, current_time)

    mailings = Mailing.objects.filter(next_sending__lte=current_time, status='active', is_active=True)
    for mailing in mailings:
        mailing_status_change(mailing, current_time)

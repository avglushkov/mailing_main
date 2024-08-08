import logging
import datetime
import smtplib

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.utils import timezone

from main.models import Mailing, Attempt
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


def mailing_blocker():
    """Блокировка рассылки при наступлении даты блокировки"""

    cur_time = timezone.now()
    current_time = cur_time.replace(second=0, microsecond=0)
    mailings = Mailing.objects.filter(block_sending__lte=current_time, is_active=True)
    for mailing in mailings:
        mailing.is_active = False
        mailing.save()


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
            Attempt.objects.create(attempt_time=str(current_time), status=True, server_answer='Success',
                                   mailing=mailing,
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


def mailing_send():
    """Получение списка рассылок"""

    cur_time = timezone.now()
    current_time = cur_time.replace(second=0, microsecond=0)
    mailings = Mailing.objects.filter(first_sending__lte=current_time, status='new', is_active=True)

    for mailing in mailings:
        mailing.status = 'started'
        mailing_status_change(mailing, current_time)

    mailings = Mailing.objects.filter(next_sending__lte=current_time, status='started', is_active=True)
    for mailing in mailings:
        mailing_status_change(mailing, current_time)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(mailing_send,
                          trigger=CronTrigger(second="*/10"),  # Every 10 seconds
                          id="mailing_send",  # The `id` assigned to each job MUST be unique
                          max_instances=1,
                          replace_existing=True,
                          )
        logger.info("Added job 'mailing_send'.")

        scheduler.add_job(mailing_blocker,
                          trigger=CronTrigger(second="*/10"),  # Every 10 seconds
                          id="mailing_blocker",  # The `id` assigned to each job MUST be unique
                          max_instances=1,
                          replace_existing=True,
                          )
        logger.info("Added job 'mailing_blocker'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

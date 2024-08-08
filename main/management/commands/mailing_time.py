from django.core.management import BaseCommand

from main.emailing import time_check


class Command(BaseCommand):
    def handle(self, *args, **options):
        time_check()
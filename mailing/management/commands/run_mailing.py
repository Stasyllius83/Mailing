from django.core.management import BaseCommand
from mailing.cron import daily_mailings



class Command(BaseCommand):
    def handle(self, *args, **options):
        daily_mailings()
        print("run mailing")

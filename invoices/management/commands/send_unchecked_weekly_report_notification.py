import datetime

from django.core.management.base import BaseCommand
from invoices.slack import send_unchecked_weekly_report_notification


class Command(BaseCommand):
    help = 'Send notifications for unchecked weekly reports'

    def handle(self, *args, **options):
        today = datetime.date.today()
        send_unchecked_weekly_report_notification(today.year, today.isocalendar()[1])

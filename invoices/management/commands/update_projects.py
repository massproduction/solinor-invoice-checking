import csv
from django.core.management.base import BaseCommand, CommandError
from invoices.models import HourEntry, Invoice, calculate_entry_stats
import datetime
import django.db.utils
from django.utils import timezone
import sys
from invoices.utils import update_projects

class Command(BaseCommand):
    help = 'Refresh project data from 10000ft'

    def handle(self, *args, **options):
        update_projects()

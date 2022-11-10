from handler.models import Image
import csv
import pandas as pd

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Deletes all entries'
    def handle(self, *args, **options):
        try:
            images = Image.objects.all().delete()
            print(f'Deleted {len(images)}recipes.')
        except Exception as e:
            print(e)
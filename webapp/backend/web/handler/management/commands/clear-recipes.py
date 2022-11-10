from handler.models import Recipe
import csv
import pandas as pd

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Deletes all entries'
    def handle(self, *args, **options):
        try:
            recipes = Recipe.objects.all().delete()
            print(f'Deleted {len(recipes)}recipes.')
        except Exception as e:
            print(e)
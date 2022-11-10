from handler.models import Recipe
from sys import stdout
import csv
import pandas as pd

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Choose a movieset to load into database'
    def add_arguments(self, parser):
        # Positional arguments 
        parser.add_argument('--file',
                            type=str,
                            action='store',
                            help='What file should be loaded',
                            default='item-profiles1',
                            dest='file'
                            )
        parser.add_argument('--file-additional',
                            type=str,
                            action='store',
                            help='add if you have more infomration to add, such as name.',
                            default='item-profiles2',
                            dest='file2'
                            )

        parser.add_argument('--root-data-folder',
                            type=str,
                            action='store',
                            help='If using a different root folder other than /data/all_recipies',
                            default='/data/all_recipes',
                            dest='root_data_folder'
                            )

    def handle(self, *args, **options):
        # Add innitial items
        try:
            df = pd.read_csv(f'{options["root_data_folder"]}/{options["file"]}.csv', sep=';')
            i = 0
            for item in df.itertuples():
                Recipe.objects.create(
                        recipe_id = item._1,
                        label = item.Category.split('>')[-1],
                        description = item.Directions,
                        image_url = f'/api/images/{item._1}.jpg'

                ).save()
                i += 1
                if i % 100 == 0:
                    stdout.write(f'Added {i}th Recipes \n')
        except Exception as e:
            print(e)

        # Add more information:
        
        try:
            df = pd.read_csv(f'{options["root_data_folder"]}/{options["file2"]}.csv', sep=';')
            i = 0
            for item in df.itertuples():
                recipe = Recipe.objects.get(recipe_id = item._1)
                recipe.recipe_name = item.Name
                recipe.save()
                i += 1
                if i % 100 == 0:
                    stdout.write(f'Added name to {i}th Recipes \n')
        except Exception as e:
            print(e)
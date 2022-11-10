from handler.models import Image
import csv
import pandas as pd
from os import listdir
from os.path import isfile, join
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Adds all images from path /data/images to db'
    
    def handle(self, *args, **options):
        mypath = '/data/images'
        images  = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for img in images:
            try:
                db_image = Image(
                    title = img.replace('.jpg', ''),
                    alt = 'Image...',
                    slug = img.replace('.jpg', ''),
                    image = 'images/' + img,
                    status = 'active'
                )
                db_image.save()

            except Exception as e:
                print(e)
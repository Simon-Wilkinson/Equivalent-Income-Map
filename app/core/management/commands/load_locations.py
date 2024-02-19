import csv
import os
import json
from core.models import Location

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        """ loads the location data from the csv files into the database"""
        Location.objects.all().delete()
        #load location data
        with open(os.path.join(settings.STATIC_ROOT, 'core', 'location_data.json'), 'r') as json_file:
            location_data = json.load(json_file)
            for location in location_data:
                new_location = Location()
                for key, value in location.items():
                    if value != 'NA':
                        setattr(new_location, key, value)
                
                new_location.save()
                print(f"Saved {new_location.name}")

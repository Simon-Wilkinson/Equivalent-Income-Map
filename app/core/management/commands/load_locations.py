import csv
import os
import json
from core.models import Location


from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings




class Command(BaseCommand):

    _location_names = [] #the list of country names that we will use, from the world.json file
    _OECD_countries = []

    def filter_location_name(self, name: str) -> str:
        #remove anything in brackets
        if ('(' in name) and (')' in name):
            name = name[:name.find('(')] + name[name.find(')')+1:]
        #remove 'the' 'and', 'of', 'democratic', 'people's'
        filtered_words = ['the ', ' and', 'of ', 'democratic', "people's", 'new ', 'united']
        for word in filtered_words:
            if word.capitalize() in name:
                name = name.replace(word.capitalize(), '')
            if word in name:
                name = name.replace(word, '')
        #remove any trailing spaces
        name = name.strip()
        return name


    def find_matching_location_name(self, search_name : str) -> str:
        """ given an input name, return a name from the list of accepted location names that is a match"""
        search_name = self.filter_location_name(search_name)
        for location in self._location_names:
            for word in search_name.split():
                word = word.replace(" ", "")
                if word.lower() in location.lower():
                    return location
        return None
    



    def handle(self, *args, **options) -> None:
        """ loads the location data from the csv files into the database"""
        Location.objects.all().delete()

        # open world json file that defines the map - populate list of all the map country names
        datafile = os.path.join(settings.STATIC_ROOT, 'world.json')
        with open(datafile, 'r') as json_file:
            json_data = json.load(json_file)
            for feature in json_data['features']:
                name = feature['properties']['name']
                if (name not in self._location_names)& (len(name.strip()) > 0):
                    self._location_names.append(name)

        # only load contries in OECD from the ppp data
        datafile = os.path.join(settings.STATIC_ROOT, 'locations-ppp.csv')
        self.stdout.write(datafile)
        # Open the data file
        with open(datafile, 'r') as csvfile:
            # Create a CSV reader
            reader = csv.reader(csvfile)
            # Skip the header row
            next(reader)
            # Loop through each row...
            for row in reader:
                print(f"searching for {row[0]}")
                matching_location_name = self.find_matching_location_name(row[0])
                print(f"found {matching_location_name}")
                if matching_location_name is None:
                    print(f'No country called {row[0]} from locations-ppp.csv found in world.json data')
                else:
                    try:
                        self._OECD_countries.append(matching_location_name)
                        location = Location()
                        location.name = matching_location_name
                        location.ppp_usa = row[1]
                        location.exchange_rate_dollar = row[2]
                        # Save the country to the database
                        location.save()
                        self.stdout.write(f"Saved PPP index and exchange rate for {location.name}: {location.ppp_usa} {location.exchange_rate_dollar}")
                    except Exception as e:
                        self.stdout.write("Exception loading PPP data for {location.name}: {e}")



        # open country code csv and assign 
        with open(os.path.join(settings.STATIC_ROOT, 'country-codes.csv'), 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                matching_location_name = self.find_matching_location_name(row[0])
                if matching_location_name is None:
                    print(f'No country called {row[0]} from country-codes.csv found in world.json data')
                elif matching_location_name in self._OECD_countries:
                    try:
                        location = Location.objects.get(name=matching_location_name)
                        location.code = row[1]
                        location.save()
                        self.stdout.write(f"Assigned {location.name} a country code of: {location.code}")
                    except Exception as e:
                        self.stdout.write("Exception loading country code data for {location.name}: {e}")
                else:
                    print(f'Country {row[0]} not in OECD, not assigning country code')

        # open currency csv and assign
        with open(os.path.join(settings.STATIC_ROOT, 'currency-code-symbols.csv'), 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                matching_location_name = self.find_matching_location_name(row[0])
                if matching_location_name is None:
                    print(f'No country called {row[0]} from currency-code-symbols.csv found in world.json data')
                elif matching_location_name in self._OECD_countries:
                    try:
                        location = Location.objects.get(name=matching_location_name)
                        location.currency_code = row[3]
                        location.currency_symbol = row[4]
                        location.save()
                        self.stdout.write(f"Assigned {location.name} a currency code of: {location.currency_code} and symbol of {location.currency_symbol}")
                    except Exception as e:
                        self.stdout.write("Exception loading country code data for {location.name}: {e}")
                else:
                    print(f'Country {row[0]} not in OECD, not assigning currency code or symbol')

        # # load worlddata
        # datafile = os.path.join(settings.STATIC_ROOT, 'locations-coli_averageincome_worlddata.csv')
        # self.stdout.write(datafile)
        # # Open the data file
        # with open(datafile, 'r') as csvfile:
        #     # Create a CSV reader
        #     reader = csv.reader(csvfile)
        #     # Loop through each row...
        #     for row in reader:
        #             matching_location_name = self.find_matching_location_name(row[0])
        #             if matching_location_name is None:
        #                 print(f'No country called {row[0]} from locations-coli_averageincome_worlddata.csv found in world.json data')
        #             elif matching_location_name in self._OECD_countries:
        #                 try:
        #                     location = Location.objects.get(name=matching_location_name)
        #                     location.cost_of_living_index = row[1]
        #                     location.average_income = row[2]
        #                     location.save()
        #                     self.stdout.write(f"{location.name} saved data: {location.cost_of_living_index} {location.average_income}")
        #                 except Exception as e:
        #                     self.stdout.write(e)
        #             else:
        #                     print(f'Country {row[0]} not in OECD, not assigning cost of living index or average income')
                
        ## load big mac data
        datafile = os.path.join(settings.STATIC_ROOT, 'big-mac-dollar-price.csv')
        with open(datafile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                matching_location_name = self.find_matching_location_name(row[0])
                if matching_location_name is None:
                    print(f'No country called {row[0]} from big-mac-dollar-price.csv found in world.json data')
                elif matching_location_name in self._OECD_countries:
                    try:
                        location = Location.objects.get(name=matching_location_name)
                        location.big_mac_dollar = row[1]
                        location.save()
                        self.stdout.write(f"{location.name} saved data: {location.big_mac_dollar}")
                    except Exception as e:
                        self.stdout.write(f'Country {location.name} not saved, exception {e}')
                else:
                    print(f'Country {row[0]} not in OECD, not assigning big mac index')


        #load worlddata
        #print all countries
        locations = Location.objects.all()
        for location in locations:
            self.stdout.write(f"{location.name} {location.code} {location.currency_code} {location.currency_symbol} {location.exchange_rate_dollar} {location.ppp_usa} {location.big_mac_dollar}")

            if (any(x is None for x in [location.code, location.currency_code, location.currency_symbol, location.exchange_rate_dollar, location.ppp_usa, location.big_mac_dollar])):
                print(f"Deleting {location.name}")
                location.delete()

        
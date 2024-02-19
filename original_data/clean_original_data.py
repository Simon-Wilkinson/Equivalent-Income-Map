import csv
import os
import json
from django.db import models


# class Location(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=3, null=True)
#     currency_code = models.CharField(max_length=3, null=True)
#     currency_symbol = models.CharField(max_length=10, null=True)
#     exchange_rate_dollar = models.FloatField(null=True)
#     ppp_usa = models.FloatField(null=True)
#     cost_of_living_index = models.FloatField(null=True)
#     big_mac_dollar = models.FloatField(null=True)
#     average_income = models.FloatField(null=True)

#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name_plural = 'Locations'
#         ordering = ['name']

#     def serialise(self):
#         return {
#             'name': self.name,
#             'currency_symbol': self.currency_symbol,
#             'exchange_rate_dollar': self.exchange_rate_dollar,
#             'ppp_usa': self.ppp_usa,
#             'big_mac_dollar': self.big_mac_dollar
#         }
    
class Location:
    name = ""
    code = ""
    currency_code = ""
    currency_symbol = ""
    exchange_rate_dollar = 0.0
    ppp_usa = 0.0
    big_mac_dollar = 0.0

    def serialise(self):
        return {
            'name': self.name,
            'currency_symbol': self.currency_symbol,
            'exchange_rate_dollar': self.exchange_rate_dollar,
            'ppp_usa': self.ppp_usa,
            'big_mac_dollar': self.big_mac_dollar
        }


class OriginalDataCleaner:
    _location_names = [] #the list of country names that we will use, from the world.json file
    ppp_countries = []
    big_mac_countries = []
    locations = []

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

    def count_matching_words(self, search_name: str, location_name: str) -> int:
        count = 0
        for word in search_name.split():
            if word in location_name.split():
                count += 1
        return count


    def find_matching_location_name(self, search_name : str) -> str:
        """ given an input name, return a name from the list of accepted location names that is a match"""
        search_name = self.filter_location_name(search_name)
        potential_matches = {}
        for location in self._location_names:
            #first see if the whole name matches
            if search_name.lower() == location.lower():
                return location
            else:
                for word in search_name.split():
                    word = word.replace(" ", "")
                    # first see if whole word matches
                    #count how many words in the search name are in the location name
                    matches = self.count_matching_words(word, location)
                    if matches > 0:
                        if location in potential_matches.keys():
                            potential_matches[location] += matches
                        else:
                            potential_matches[location] = matches
                        
        if len(potential_matches) == 1:
            return list(potential_matches.keys())[0]
        elif len(potential_matches) > 1:
            #get number of non matching letters
            print(f"Potential matches for {search_name} are {potential_matches}")
        return None

    def clean_original_data(self):
        # load location data
        # open world json file that defines the map - populate list of all the map country names
        datafile = os.path.join(os.path.dirname(__file__), 'world_map.json')
        with open(datafile, 'r') as json_file:
            json_data = json.load(json_file)
            for feature in json_data['features']:
                name = feature['properties']['name']
                if (name not in self._location_names)& (len(name.strip()) > 0):
                    self._location_names.append(name)

        # only load contries in OECD from the ppp data
        datafile = os.path.join(os.path.dirname(__file__), 'locations-ppp.csv')
        # Open the data file
        with open(datafile, 'r') as csvfile:
            # Create a CSV reader
            reader = csv.reader(csvfile)
            # Skip the header row
            # Loop through each row...
            for row in reader:
                matching_location_name = self.find_matching_location_name(row[0])
                if matching_location_name is None:
                    print(f'No country called {row[0]} from locations-ppp.csv found in world.json data')
                else:
                    try:
                        self.ppp_countries.append(matching_location_name)
                        location = Location()
                        location.name = matching_location_name
                        location.ppp_usa = row[1]
                        location.exchange_rate_dollar = row[2]
                        location.big_mac_dollar = 'NA'
                        # Save the country to the database
                        self.locations.append(location)
                    except Exception as e:
                        print("Exception loading PPP data for {location.name}: {e}")

        ## load big mac data
        datafile = os.path.join(os.path.dirname(__file__),  'big-mac-dollar-price.csv')
        with open(datafile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                matching_location_name = self.find_matching_location_name(row[0])
                if matching_location_name is None:
                    print(f'No country called {row[0]} from big-mac-dollar-price.csv found in world.json data')
                else:
                    try:
                        location = list(filter(lambda x: x.name == matching_location_name, self.locations))
                        self.big_mac_countries.append(matching_location_name)
                        if len(location) == 1:
                            location = location[0]
                            location.big_mac_dollar = row[1]
                        else:
                            location = Location()
                            location.name = matching_location_name
                            location.big_mac_dollar = row[1]
                            location.ppp_usa = 'NA'
                            location.exchange_rate_dollar = 'NA'
                            self.locations.append(location)
                    except Exception as e:
                        print(f'Country {matching_location_name} not saved, exception {e}')



        # open currency csv and assign
        with open( os.path.join(os.path.dirname(__file__),'currency-code-symbols.csv'), 'r', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                count = [row[0] in x for x in self.ppp_countries].count(True)
                count += [row[0] in x for x in self.big_mac_countries].count(True)
                if count > 0:
                    matching_location_name = self.find_matching_location_name(row[0])
                    if matching_location_name is None:
                        print(f'No country called {row[0]} from currency-code-symbols.csv found in world.json data')
                    else:
                        location = list(filter(lambda x: x.name == matching_location_name, self.locations))
                        if len(location) == 1:
                            location = location[0]
                            location.currency_code = row[3]
                            location.currency_symbol = row[4]
                        else:
                            print(f'Country {row[0]} not in ppp or bm data, not assigning currency code or symbol')
                



        #load worlddata
        #print all countries
        for location in self.locations:
            print(f"{location.name} {location.code} {location.currency_code} {location.currency_symbol} {location.exchange_rate_dollar} {location.ppp_usa} {location.big_mac_dollar}")

            if (any(x is None for x in [location.code, location.currency_code, location.currency_symbol, location.exchange_rate_dollar, location.ppp_usa, location.big_mac_dollar])):
                print(f"Deleting {location.name}")
                location.delete()

        location_data = []
        for location in self.locations:
            location_data.append({
                "name": location.name,
                "code": location.code,
                "currency_code": location.currency_code,
                "currency_symbol": location.currency_symbol,
                "exchange_rate_dollar": location.exchange_rate_dollar,
                "ppp_usa": location.ppp_usa,
                "big_mac_dollar": location.big_mac_dollar
            })
            
        with open( 'location_data_2.json', 'w') as json_file:
            json.dump(location_data, json_file)


if __name__ == "__main__":
    cleaner = OriginalDataCleaner()
    cleaner.clean_original_data()
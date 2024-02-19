from django.shortcuts import render
from django.conf import settings
from core.models import Location
from core.forms import IncomeForm

import json
import math
import os

# Create your views here.
def home(request):
    with open(os.path.join(settings.STATIC_ROOT, 'world_map.json')) as json_file:
        worldmap_data = json.load(json_file)

    form = IncomeForm()
    form.initial['country'] = 'United States'
    form.initial['income'] = 100000
    form.initial['index'] = 'Purchase Power Parity'

    locations = Location.objects.all()
    location_data = [location.serialise() for location in locations]
    
    data = {
        'worldmap_data': worldmap_data,
        'location_data': location_data,
    }

    return render(request, 'core/home.html', {'all_data': json.dumps(data) , 'form': form})

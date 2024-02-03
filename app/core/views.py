from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from core.models import Location
from core.forms import IncomeForm

import json
import math
import os

# Create your views here.
def home(request):
    with open(os.path.join(settings.STATIC_ROOT , 'world.json')) as json_file:
        json_data = json.load(json_file)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        form.fields['country'].choices = [(name, name) for name in Location.objects.values_list('name', flat=True)]
        if form.is_valid():
            base_location = form.cleaned_data.get('country')
            base_income = form.cleaned_data.get('income')
            index = form.cleaned_data.get('index')
            form.fields['index'].choices = [(index, index) for index in Location.objects.get(name=base_location).available_indexes()]
        else:
            base_location = 'United States'
            base_income = 100000
            index = 'Purchase Power Parity'
    
    else:
        form = IncomeForm()
        base_location = 'United States'
        base_income = 100000
        index = 'Purchase Power Parity'



    locations = Location.objects.all()

    if index == 'Purchase Power Parity':
        form.fields['country'].choices = [(name, name)  for name in Location.objects.values_list('name', flat=True)
                                                        if Location.objects.get(name=name).ppp_usa is not None]
        equivalent_incomes = calculate_equivalent_incomes_ppp(base_income, base_location)
    elif index == 'Cost of Living Index':
        form.fields['country'].choices = [(name, name)  for name in Location.objects.values_list('name', flat=True)
                                                        if Location.objects.get(name=name).cost_of_living_index is not None]
        equivalent_incomes = calculate_equivalent_incomes_coi(base_income, base_location)
    elif index == 'Big Mac Index':
        form.fields['country'].choices = [(name, name)  for name in Location.objects.values_list('name', flat=True)
                                                        if Location.objects.get(name=name).big_mac_dollar is not None]
        equivalent_incomes = calculate_equivalent_incomes_bmi(base_income, base_location)

    


    min_range = math.floor(min(equivalent_incomes.values())/10000)*10000
    max_range = math.ceil(max(equivalent_incomes.values())/10000)*10000


    return render(request, 'core/fromHeros.html', {'json_data': json.dumps(json_data), 'locations': locations, 
                                                   'equivalent_incomes': equivalent_incomes, 'form': form,
                                                   'base_location': base_location, 'base_income': base_income,
                                                   'min_range': min_range, 'max_range': max_range,
                                                   })


def calculate_equivalent_incomes_ppp(base_income, base_location_name):
    locations = Location.objects.all()
    base_location = Location.objects.get(name=base_location_name)
    equivalent_incomes = {}
    for location in locations:
        if location.ppp_usa is not None:
            equivalent_incomes[location.name] = round(base_income * (base_location.ppp_usa / location.ppp_usa),0)

    return equivalent_incomes

def calculate_equivalent_incomes_coi(base_income, base_location_name):
    locations = Location.objects.all()
    base_location = Location.objects.get(name=base_location_name)
    equivalent_incomes = {}
    for location in locations:
        if location.cost_of_living_index is not None:
            equivalent_incomes[location.name] = round(base_income * (location.cost_of_living_index / base_location.cost_of_living_index),0)

    return equivalent_incomes

def calculate_equivalent_incomes_bmi(base_income, base_location_name):
    locations = Location.objects.all()
    base_location = Location.objects.get(name=base_location_name)
    equivalent_incomes = {}
    for location in locations:
        if location.big_mac_dollar is not None:
            equivalent_incomes[location.name] = round(base_income * (location.big_mac_dollar / base_location.big_mac_dollar),0)

    return equivalent_incomes
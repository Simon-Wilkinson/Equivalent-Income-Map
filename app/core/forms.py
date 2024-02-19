# forms.py
from django import forms
from core.models import Location



class IncomeForm(forms.Form):
    
    COUNTRY_CHOICES = [("test", "test")]
    index_choices = [('Purchase Power Parity', 'Purchase Power Parity'),
                     ('Big Mac Index', 'Big Mac Index'),
                     ]
    
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Base Country', show_hidden_initial=True)
    income = forms.FloatField(label='Base Income', min_value=0.0, max_value=1000000000.0)
    index = forms.ChoiceField(choices=index_choices, label='Price Index')

    def __init__(self, *args, **kwargs):
            super(IncomeForm, self).__init__(*args, **kwargs)
            # Dynamically update the choices in the country field
            self.fields['country'].choices = [(location.name, location.name + f" ({location.currency_symbol})" ) for location in Location.objects.all()]
            
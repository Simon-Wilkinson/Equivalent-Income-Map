from django.db import models

# Create your models here.
class Sample(models.Model):
    attachment = models.FileField()


class Location(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, null=True)
    currency_code = models.CharField(max_length=3, null=True)
    currency_symbol = models.CharField(max_length=10, null=True)
    exchange_rate_dollar = models.FloatField(null=True)
    ppp_usa = models.FloatField(null=True)
    cost_of_living_index = models.FloatField(null=True)
    big_mac_dollar = models.FloatField(null=True)
    average_income = models.FloatField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['name']

    def available_indexes(self):
        indexes = []
        if self.ppp_usa is not None:
            indexes.append('Purchase Power Parity')
        if self.cost_of_living_index is not None:
            indexes.append('Cost of Living Index')
        if self.big_mac_dollar is not None:
            indexes.append('Big Mac Index')
        return indexes
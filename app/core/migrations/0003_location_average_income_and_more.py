# Generated by Django 4.2.9 on 2024-01-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='average_income',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='cost_of_living_index',
            field=models.FloatField(null=True),
        ),
    ]

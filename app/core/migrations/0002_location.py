# Generated by Django 4.2.9 on 2024-01-20 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ppp_usa', models.FloatField()),
                ('exchange_rate_dollar', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Locations',
                'ordering': ['name'],
            },
        ),
    ]

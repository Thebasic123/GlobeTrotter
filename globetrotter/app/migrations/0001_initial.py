# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('place_id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=12)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=12)),
                ('picture', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=100)),
                ('attractions', models.TextField()),
                ('restaurants', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=100)),
                ('cities', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('shareable', models.BooleanField(default=False)),
                ('attractions', models.TextField()),
                ('restaurants', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(primary_key=True, serialize=False, max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('itinerary', models.ForeignKey(to='app.Itinerary')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='app.Country'),
        ),
    ]

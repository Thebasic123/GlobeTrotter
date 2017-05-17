# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_user_loggedin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='attractions',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='itinerary',
            name='restaurants',
            field=models.TextField(default=''),
        ),
    ]

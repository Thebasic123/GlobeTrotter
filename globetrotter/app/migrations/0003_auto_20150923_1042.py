# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_restaurant_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cities',
            field=models.TextField(default='[]'),
        ),
    ]

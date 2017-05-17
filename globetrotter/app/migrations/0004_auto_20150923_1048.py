# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150923_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cities',
            field=models.TextField(default='null'),
        ),
    ]

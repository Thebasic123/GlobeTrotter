# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150923_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loggedIn',
            field=models.BooleanField(default=False),
        ),
    ]

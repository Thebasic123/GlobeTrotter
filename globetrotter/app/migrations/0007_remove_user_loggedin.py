# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150923_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='loggedIn',
        ),
    ]

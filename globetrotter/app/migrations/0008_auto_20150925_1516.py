# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_user_loggedin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='attractions',
        ),
        migrations.RemoveField(
            model_name='city',
            name='restaurants',
        ),
        migrations.RemoveField(
            model_name='country',
            name='cities',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='attractions',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='id',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='restaurants',
        ),
        migrations.RemoveField(
            model_name='user',
            name='itinerary',
        ),
        migrations.AddField(
            model_name='attraction',
            name='city',
            field=models.ForeignKey(to='app.City', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attraction',
            name='itinerary',
            field=models.ManyToManyField(to='app.Itinerary'),
        ),
        migrations.AddField(
            model_name='country',
            name='country_code',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='user',
            field=models.OneToOneField(serialize=False, to='app.User', primary_key=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.ForeignKey(to='app.City', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='itinerary',
            field=models.ManyToManyField(to='app.Itinerary'),
        ),
    ]

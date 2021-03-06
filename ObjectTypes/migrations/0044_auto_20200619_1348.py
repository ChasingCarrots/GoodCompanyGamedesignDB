# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-06-19 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0043_auto_20200424_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalspecialflagsproperty',
            name='IsInventoryDistributor',
        ),
        migrations.RemoveField(
            model_name='specialflagsproperty',
            name='IsInventoryDistributor',
        ),
        migrations.AddField(
            model_name='historicalspecialflagsproperty',
            name='IsPuller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalspecialflagsproperty',
            name='IsPusher',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='specialflagsproperty',
            name='IsPuller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='specialflagsproperty',
            name='IsPusher',
            field=models.BooleanField(default=False),
        ),
    ]

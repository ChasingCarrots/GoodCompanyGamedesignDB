# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-11 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0029_auto_20190611_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmodule',
            name='MarketRecoveryFactor',
            field=models.FloatField(default=0.5),
        ),
        migrations.AddField(
            model_name='module',
            name='MarketRecoveryFactor',
            field=models.FloatField(default=0.5),
        ),
    ]

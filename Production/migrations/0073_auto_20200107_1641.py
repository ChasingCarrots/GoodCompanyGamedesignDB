# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-01-07 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0072_auto_20191121_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmarketphase',
            name='MinimumFeatures',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='marketphase',
            name='MinimumFeatures',
            field=models.IntegerField(default=0),
        ),
    ]
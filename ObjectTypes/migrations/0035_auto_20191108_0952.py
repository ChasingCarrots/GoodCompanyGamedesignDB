# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-11-08 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0034_auto_20191023_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildableproperty',
            name='MoneyCost',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='historicalbuildableproperty',
            name='MoneyCost',
            field=models.IntegerField(default=1000),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-25 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0050_auto_20190925_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproducttype',
            name='MarketTier',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicalproducttype',
            name='RequiredDiscoveryPoints',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='producttype',
            name='MarketTier',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='producttype',
            name='RequiredDiscoveryPoints',
            field=models.IntegerField(default=10),
        ),
    ]

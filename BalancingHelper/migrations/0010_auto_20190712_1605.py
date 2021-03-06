# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-12 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0043_auto_20190709_1321'),
        ('BalancingHelper', '0009_auto_20190712_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='criticalmodulepath',
            name='MainFeatureValue',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='criticalmodulepath',
            name='NegativeFeatureValue',
            field=models.FloatField(default=0.2),
        ),
        migrations.AddField(
            model_name='criticalmodulepath',
            name='NegativeFeatures',
            field=models.ManyToManyField(blank=True, related_name='NegativeOnPath', to='Production.ProductFeature'),
        ),
        migrations.AddField(
            model_name='criticalmodulepath',
            name='PositiveFeatureValue',
            field=models.FloatField(default=0.2),
        ),
        migrations.AddField(
            model_name='criticalmodulepath',
            name='PositiveFeatures',
            field=models.ManyToManyField(blank=True, related_name='PositiveOnPath', to='Production.ProductFeature'),
        ),
        migrations.AddField(
            model_name='historicalcriticalmodulepath',
            name='MainFeatureValue',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='historicalcriticalmodulepath',
            name='NegativeFeatureValue',
            field=models.FloatField(default=0.2),
        ),
        migrations.AddField(
            model_name='historicalcriticalmodulepath',
            name='PositiveFeatureValue',
            field=models.FloatField(default=0.2),
        ),
    ]

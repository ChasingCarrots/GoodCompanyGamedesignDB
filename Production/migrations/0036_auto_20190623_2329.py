# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-23 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0035_auto_20190617_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproductfunction',
            name='BaseMarketCurvePotential',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='historicalproductfunction',
            name='BaseMarketMaxPriceFactor',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='productfunction',
            name='BaseMarketCurvePotential',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='productfunction',
            name='BaseMarketMaxPriceFactor',
            field=models.IntegerField(default=5),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-09 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0062_auto_20191008_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproducttype',
            name='BaseMarketDemand',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='producttype',
            name='BaseMarketDemand',
            field=models.IntegerField(default=10),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-09 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0062_historicalproducttypecase_producttypecase_producttypecaseblockingfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='MandatoryFeatures',
            field=models.ManyToManyField(to='Production.ProductFeature'),
        ),
    ]

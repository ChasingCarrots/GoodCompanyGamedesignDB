# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-28 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0069_auto_20191028_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproducttype',
            name='ProductAssetID',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='producttype',
            name='ProductAssetID',
            field=models.CharField(default='', max_length=255),
        ),
    ]

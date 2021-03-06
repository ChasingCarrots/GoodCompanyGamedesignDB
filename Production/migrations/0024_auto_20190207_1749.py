# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-07 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0023_auto_20190123_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfunction',
            name='IconAssetID',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productfunction',
            name='ViableProductTypes',
            field=models.ManyToManyField(related_name='ViableProdictTypes', to='Production.ProductType'),
        ),
    ]

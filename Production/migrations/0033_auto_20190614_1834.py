# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-14 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0032_auto_20190614_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproductfeature',
            name='Type',
            field=models.IntegerField(choices=[(1, 'Binary'), (0, 'Additive')], default=1),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='ComplementaryFeature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MainFeature', to='Production.ProductFeature'),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='Type',
            field=models.IntegerField(choices=[(1, 'Binary'), (0, 'Additive')], default=1),
        ),
    ]
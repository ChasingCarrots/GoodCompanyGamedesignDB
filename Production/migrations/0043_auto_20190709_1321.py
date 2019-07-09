# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-09 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0042_auto_20190704_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfunctionfeaturerequirement',
            name='Function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MandatoryFeatures', to='Production.ProductFunction'),
        ),
    ]
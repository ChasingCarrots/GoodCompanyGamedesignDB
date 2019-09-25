# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-25 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BalancingHelper', '0014_auto_20190925_1214'),
        ('Research', '0010_auto_20190925_1214'),
        ('ObjectTypes', '0030_auto_20190925_1214'),
        ('Production', '0048_auto_20190829_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproductfunction',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctiondrawbacks',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctiondrawbacks',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctiondrawbacks',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionfeaturerequirement',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionfeaturerequirement',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionfeaturerequirement',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionoptionalfeatures',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionoptionalfeatures',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='historicalproductfunctionoptionalfeatures',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproducttype',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='productfunction',
            name='ViableProductTypes',
        ),
        migrations.RemoveField(
            model_name='productfunctiondrawbacks',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='productfunctiondrawbacks',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='productfunctionfeaturerequirement',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='productfunctionfeaturerequirement',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='productfunctionoptionalfeatures',
            name='Feature',
        ),
        migrations.RemoveField(
            model_name='productfunctionoptionalfeatures',
            name='Function',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='Slots',
        ),
        migrations.RemoveField(
            model_name='producttypeslotuiposition',
            name='productType',
        ),
        migrations.RemoveField(
            model_name='producttypeslotuiposition',
            name='slotType',
        ),
        migrations.DeleteModel(
            name='HistoricalProductFunction',
        ),
        migrations.DeleteModel(
            name='HistoricalProductFunctionDrawbacks',
        ),
        migrations.DeleteModel(
            name='HistoricalProductFunctionFeatureRequirement',
        ),
        migrations.DeleteModel(
            name='HistoricalProductFunctionOptionalFeatures',
        ),
        migrations.DeleteModel(
            name='HistoricalProductType',
        ),
        migrations.DeleteModel(
            name='ProductFunction',
        ),
        migrations.DeleteModel(
            name='ProductFunctionDrawbacks',
        ),
        migrations.DeleteModel(
            name='ProductFunctionFeatureRequirement',
        ),
        migrations.DeleteModel(
            name='ProductFunctionOptionalFeatures',
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
        migrations.DeleteModel(
            name='ProductTypeSlotUIPosition',
        ),
    ]

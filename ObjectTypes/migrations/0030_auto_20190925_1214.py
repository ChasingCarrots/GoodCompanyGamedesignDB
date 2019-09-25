# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-25 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0029_auto_20190902_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assemblypropertyproducttypeassemblyduration',
            name='AssemblyProperty',
        ),
        migrations.RemoveField(
            model_name='assemblypropertyproducttypeassemblyduration',
            name='ProductType',
        ),
        migrations.RemoveField(
            model_name='historicalassemblypropertyproducttypeassemblyduration',
            name='AssemblyProperty',
        ),
        migrations.RemoveField(
            model_name='historicalassemblypropertyproducttypeassemblyduration',
            name='ProductType',
        ),
        migrations.RemoveField(
            model_name='historicalassemblypropertyproducttypeassemblyduration',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='AssemblyPropertyProductTypeAssemblyDuration',
        ),
        migrations.DeleteModel(
            name='HistoricalAssemblyPropertyProductTypeAssemblyDuration',
        ),
    ]

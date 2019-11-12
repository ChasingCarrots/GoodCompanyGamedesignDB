# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-21 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0031_assemblypropertyproducttypeassemblyduration_historicalassemblypropertyproducttypeassemblyduration'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalobjectlookproperty',
            name='CanChangeColor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='objectlookproperty',
            name='CanChangeColor',
            field=models.BooleanField(default=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-01 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0008_specialflagsproperty_istrashcan'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialflagsproperty',
            name='IsDraftingTable',
            field=models.BooleanField(default=False),
        ),
    ]

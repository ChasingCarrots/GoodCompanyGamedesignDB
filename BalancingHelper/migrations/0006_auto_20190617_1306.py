# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-17 11:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BalancingHelper', '0005_sampleproduct_automaticgeneration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sampleproduct',
            old_name='AutomaticGeneration',
            new_name='AutoGenerated',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-27 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0054_auto_20190926_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpositivefeature',
            old_name='Min',
            new_name='Max',
        ),
        migrations.RenameField(
            model_name='positivefeature',
            old_name='Min',
            new_name='Max',
        ),
    ]
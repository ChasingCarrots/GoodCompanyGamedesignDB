# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-06 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0012_auto_20180906_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='FitsIntoSlot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FittingModule', to='Production.ModuleSlotType'),
        ),
    ]

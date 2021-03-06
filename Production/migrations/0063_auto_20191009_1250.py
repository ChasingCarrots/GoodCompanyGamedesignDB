# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-09 10:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models



class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0062_auto_20191008_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnegativefeature',
            name='MarketPhase',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Production.MarketPhase'),
        ),
        migrations.AddField(
            model_name='historicalpositivefeature',
            name='MarketPhase',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Production.MarketPhase'),
        ),
        migrations.AddField(
            model_name='negativefeature',
            name='MarketPhase',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='NegativeFeatures', to='Production.MarketPhase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='positivefeature',
            name='MarketPhase',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='PositiveFeatures', to='Production.MarketPhase'),
            preserve_default=False,
        ),        
	migrations.RemoveField(
            model_name='historicalnegativefeature',
            name='ProductType',
        ),
        migrations.RemoveField(
            model_name='historicalpositivefeature',
            name='ProductType',
        ),
        migrations.RemoveField(
            model_name='negativefeature',
            name='ProductType',
        ),
        migrations.RemoveField(
            model_name='positivefeature',
            name='ProductType',
        ),

    ]

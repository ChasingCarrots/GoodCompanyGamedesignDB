# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-11-15 13:05
from __future__ import unicode_literals

import bitfield.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ObjectTypes', '0035_auto_20191108_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTransferTilesProperty',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('ObjectType', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ObjectTypes.ObjectType')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Transfer Tiles Property',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTransferTilesPropertyTile',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('XCoord', models.IntegerField()),
                ('YCoord', models.IntegerField()),
                ('PushDirections', bitfield.models.BitField(['PositiveX', 'PositiveY', 'NegativeX', 'NegativeY'], default=0)),
                ('ReceiveDirections', bitfield.models.BitField(['PositiveX', 'PositiveY', 'NegativeX', 'NegativeY'], default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Transfer tile',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='TransferTilesProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ObjectType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='TransferTilesProperty', to='ObjectTypes.ObjectType')),
            ],
            options={
                'verbose_name': 'Transfer Tiles Property',
                'verbose_name_plural': 'Transfer Tiles Properties',
            },
        ),
        migrations.CreateModel(
            name='TransferTilesPropertyTile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('XCoord', models.IntegerField()),
                ('YCoord', models.IntegerField()),
                ('PushDirections', bitfield.models.BitField(['PositiveX', 'PositiveY', 'NegativeX', 'NegativeY'], default=0)),
                ('ReceiveDirections', bitfield.models.BitField(['PositiveX', 'PositiveY', 'NegativeX', 'NegativeY'], default=0)),
                ('TransferTilesProperty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tiles', to='ObjectTypes.TransferTilesProperty')),
            ],
            options={
                'verbose_name': 'Transfer tile',
                'verbose_name_plural': 'Transfer tiles',
            },
        ),
        migrations.AddField(
            model_name='crafterproperty',
            name='Automatic',
            field=models.BooleanField(default=False, help_text="doesn't need an employee when set to true"),
        ),
        migrations.AddField(
            model_name='crafterpropertymoduleduration',
            name='BatchSize',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicalcrafterproperty',
            name='Automatic',
            field=models.BooleanField(default=False, help_text="doesn't need an employee when set to true"),
        ),
        migrations.AddField(
            model_name='historicalcrafterpropertymoduleduration',
            name='BatchSize',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicaltransfertilespropertytile',
            name='TransferTilesProperty',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ObjectTypes.TransferTilesProperty'),
        ),
        migrations.AddField(
            model_name='historicaltransfertilespropertytile',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]

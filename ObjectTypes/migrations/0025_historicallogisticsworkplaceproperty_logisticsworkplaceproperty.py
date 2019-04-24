# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-24 16:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ObjectTypes', '0024_auto_20190326_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLogisticsWorkplaceProperty',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('Reach', models.IntegerField()),
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
                'verbose_name': 'historical Logistics Workplace Property',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LogisticsWorkplaceProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reach', models.IntegerField()),
                ('ObjectType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='LogisticsWorkplaceProperty', to='ObjectTypes.ObjectType')),
            ],
            options={
                'verbose_name': 'Logistics Workplace Property',
                'verbose_name_plural': 'Logistics Workplace Properties',
            },
        ),
    ]
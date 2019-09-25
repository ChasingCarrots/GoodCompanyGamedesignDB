# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-25 10:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0050_auto_20190925_1219'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ObjectTypes', '0030_auto_20190925_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyPropertyProductTypeAssemblyDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Duration', models.FloatField()),
                ('AssemblyProperty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PossibleProductTypes', to='ObjectTypes.AssemblyProperty')),
                ('ProductType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.ProductType')),
            ],
            options={
                'verbose_name': 'Possible ProductType',
                'verbose_name_plural': 'Possible ProductTypes',
            },
        ),
        migrations.CreateModel(
            name='HistoricalAssemblyPropertyProductTypeAssemblyDuration',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('Duration', models.FloatField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('AssemblyProperty', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ObjectTypes.AssemblyProperty')),
                ('ProductType', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Production.ProductType')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Possible ProductType',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

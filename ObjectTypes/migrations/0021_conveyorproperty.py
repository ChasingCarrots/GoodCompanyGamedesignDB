# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-28 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0020_interfacenodesproperty_interfacenodespropertyinterfacenode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConveyorProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsConveyor', models.BooleanField(default=False)),
                ('IsRollerband', models.BooleanField(default=False)),
                ('IsOverhead', models.BooleanField(default=False)),
                ('ObjectType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ConveyorProperty', to='ObjectTypes.ObjectType')),
            ],
            options={
                'verbose_name': 'Conveyor Property',
                'verbose_name_plural': 'Conveyor Properties',
            },
        ),
    ]
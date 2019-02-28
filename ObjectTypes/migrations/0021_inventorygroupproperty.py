# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-27 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0020_interfacenodesproperty_interfacenodespropertyinterfacenode'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryGroupProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SlotCapacity', models.IntegerField()),
                ('ObjectType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='InventoryGroupProperty', to='ObjectTypes.ObjectType')),
            ],
            options={
                'verbose_name': 'Inventory Group Property',
                'verbose_name_plural': 'Inventory Group Properties',
            },
        ),
    ]

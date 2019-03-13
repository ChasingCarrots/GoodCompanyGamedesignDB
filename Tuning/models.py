# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords

import common

class TuningValue(models.Model):
    history = HistoricalRecords()
    INTEGER = 0
    FLOAT = 1
    STRING = 2
    Name = models.CharField(max_length=255)
    Type = models.IntegerField(
        default=INTEGER,
        choices=(
            (INTEGER, "integer"),
            (FLOAT, "float"),
            (STRING, "string"),
        )
    )
    Value = models.CharField(max_length=255)

    def getJsonValue(self):
        if self.Type == 0:
            return int(self.Value)
        elif self.Type == 1:
            return float(self.Value)
        elif self.Type == 2:
            return self.Value
        raise RuntimeError("Invalid tuning value type " + self.Type)
    
    class Meta:
        verbose_name = 'Tuning Values'
        verbose_name_plural = "Tuning Values"

    def __unicode__(self):
        return unicode(self.Name)

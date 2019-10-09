# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Production.models import *


class LuaTemplates(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Text = models.TextField()

    class Meta:
        verbose_name = 'Lua Template'
        verbose_name_plural = 'Lua Templates'
        ordering = ['Name']

    def __unicode__(self):
        return self.Name

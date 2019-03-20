# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Production.models import *

class SampleProduct(models.Model):
    Name = models.CharField(max_length=255)
    ProductFunction = models.ForeignKey(ProductFunction)
    Modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'Sample Product'
        verbose_name_plural = 'Sample Products'
        ordering = ['id']

    def __unicode__(self):
        return self.Name

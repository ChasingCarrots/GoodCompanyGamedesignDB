# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ResearchDataType(models.Model):
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
        }

    class Meta:
        verbose_name = 'Research Data Type'
        verbose_name_plural = 'Research Data Types'

    def __unicode__(self):
        return unicode(self.Name)

class DevelopmentProjectRequiredData(models.Model):
    DevelopmentProject = models.ForeignKey("DevelopmentProject", related_name="RequiredData")
    DataType = models.ForeignKey(ResearchDataType, related_name="DevelopmentProjects")
    Amount = models.IntegerField()

    def getJsonObject(self):
        return {
            "DataTypeID": self.DataType.id,
            "Amount": self.Amount,
        }

    class Meta:
        verbose_name = 'Development Project Required Data'
        verbose_name_plural = 'Development Project Required Data'

    def __unicode__(self):
        return u"%d x %s" %(self.Amount, unicode(self.DataType))

class DevelopmentProject(models.Model):
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    RequiredProjects = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="RequiredForProjects")

    def getJsonObject(self):
        requiredData = []
        for reqDat in self.RequiredData.all():
            requiredData.append(reqDat.getJsonObject())
        requiredProjects = []
        for reqProj in self.RequiredProjects.all():
            requiredProjects.append(reqProj.id)
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
            "RequiredProjects":requiredProjects,
            "RequiredData":requiredData
        }

    class Meta:
        verbose_name = 'Development Project'
        verbose_name_plural = 'Development Projects'

    def __unicode__(self):
        return unicode(self.Name)


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords

class ResearchDataType(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    NetWorth = models.IntegerField(default=100)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
            "NetWorth": self.NetWorth,
        }

    class Meta:
        verbose_name = 'Research Data Type'
        verbose_name_plural = 'Research Data Types'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)

class DevelopmentProjectRequiredData(models.Model):
    history = HistoricalRecords()
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
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    RequiredProjects = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="RequiredForProjects")
    UnlocksModules = models.ManyToManyField("Production.Module", blank=True, related_name="UnlockedByResearch")
    UnlocksBuildables = models.ManyToManyField("ObjectTypes.ObjectType", blank=True, related_name="UnlockedByResearch")
    UnlocksProductTypes = models.ManyToManyField("Production.ProductType", blank=True, related_name="UnlockedByResearch")
    UnlocksProductFunctions = models.ManyToManyField("Production.ProductFunction", blank=True, related_name="UnlockedByResearch")

    def getJsonObject(self):
        requiredData = [reqDat.getJsonObject() for reqDat in self.RequiredData.all()]
        requiredProjects = [reqProj.id for reqProj in self.RequiredProjects.all()]
        unlocksModules = [module.id for module in self.UnlocksModules.all()]
        unlocksBuildables = [objType.id for objType in self.UnlocksBuildables.all()]
        unlocksProductTypes = [prodType.id for prodType in self.UnlocksProductTypes.all()]
        unlocksProductFunctions = [prodFunc.id for prodFunc in self.UnlocksProductFunctions.all()]

        return {
            "Name": self.Name,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "RequiredProjects": requiredProjects,
            "RequiredData": requiredData,
            "UnlocksModules": unlocksModules,
            "UnlocksBuildables": unlocksBuildables,
            "UnlocksProductTypes": unlocksProductTypes,
            "UnlocksProductFunctions": unlocksProductFunctions
        }

    class Meta:
        verbose_name = 'Development Project'
        verbose_name_plural = 'Development Projects'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)


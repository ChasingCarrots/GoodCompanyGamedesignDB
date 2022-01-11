# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords
from ast import literal_eval
from django.core.validators import validate_comma_separated_integer_list
import common

class ResearchDataType(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    NetWorth = models.IntegerField(default=100)
    DevelopmentTime = models.FloatField(default=1)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
            "NetWorth": self.NetWorth,
            "DevelopmentTime": self.DevelopmentTime,
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


class ProgressNodeRequiredData(models.Model):
    history = HistoricalRecords()
    DevelopmentProject = models.ForeignKey("ProgressNode", related_name="RequiredData")
    DataType = models.ForeignKey(ResearchDataType, related_name="ProgressNodes")
    Amount = models.IntegerField()

    def getJsonObject(self):
        return {
            "DataTypeID": self.DataType.id,
            "Amount": self.Amount,
        }

    class Meta:
        verbose_name = 'Progress Node Required Data'
        verbose_name_plural = 'Progress Node Required Data'

    def __unicode__(self):
        return u"%d x %s" %(self.Amount, unicode(self.DataType))


class ProjectCategory(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    Order = models.IntegerField(default=1)
    IconAssetID = models.CharField(max_length=255, null=True, blank=True)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "Order": self.Order
        }

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __unicode__(self):
        return self.Name


class ProgressNode(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    NodeGroup = models.IntegerField(default=0)
    IsHidden = models.BooleanField(default=False)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    Lane = models.IntegerField(default=0)
    Tier = models.IntegerField(default=0)
    Category = models.IntegerField(choices=common.NodeTreeCategory, blank=False, default=common.CAT_TREE_BIZDEV)
    RequiredProjects = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="RequiredForProjects")
    UnlocksBuildables = models.ManyToManyField("ObjectTypes.ObjectType", blank=True, related_name="UnlockedByProject")
    UnlocksMarkets = models.ManyToManyField("Production.ProductType", blank=True, related_name="UnlockedByProject")
    UnlocksPolicies = models.CharField(validators=[validate_comma_separated_integer_list], max_length=500, default="", blank=True)
    UnlocksSkills = models.ManyToManyField("Production.SkillType", blank=True, related_name="UnlockedByProject")
    RequiredMoney = models.IntegerField(default=0)
    RequiredDiscoveryPoints = models.IntegerField(default=0)
    RequiredSuccessPoints = models.IntegerField(default=0)
    NodeNetWorth = models.IntegerField(default=0)

    def getJsonObject(self):
        requiredData = [reqDat.getJsonObject() for reqDat in self.RequiredData.all()]
        requiredProjects = [reqProj.id for reqProj in self.RequiredProjects.all()]
        unlocksBuildables = [objType.id for objType in self.UnlocksBuildables.all()]
        unlocksMarkets = [prodType.id for prodType in self.UnlocksMarkets.all()]
        skills = [skillType.id for skillType in self.UnlocksSkills.all()]

        policies = []
        if self.UnlocksPolicies != "":
            if isinstance(literal_eval(self.UnlocksPolicies), int):
                policies.append(literal_eval(self.UnlocksPolicies))
            else:
                policies = literal_eval(self.UnlocksPolicies)

        return {
            "Name": self.Name,
            "IsHidden": self.IsHidden,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "Tier": self.Tier,
            "Lane": self.Lane,
            "CategoryID": self.Category,
            "RequiredProjects": requiredProjects,
            "UnlocksBuildables": unlocksBuildables,
            "UnlocksMarkets": unlocksMarkets,
            "UnlocksPolicies": policies,
            "UnlocksSkills": skills,
            "RequiredMoney": self.RequiredMoney,
            "RequiredDiscoveryPoints": self.RequiredDiscoveryPoints,
            "RequiredSuccessPoints": self.RequiredSuccessPoints,
            "RequiredData": requiredData,
            "NodeGroup": self.NodeGroup,
            "NodeNetWorth": self.NodeNetWorth,
        }

    class Meta:
        verbose_name = 'Progress Node'
        verbose_name_plural = 'Progress Node'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)




class DevelopmentProject(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    IsHidden = models.BooleanField(default=True)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    Tier = models.IntegerField(default=1)
    Lane = models.IntegerField(default=0)
    Category = models.ForeignKey(ProjectCategory, related_name="Projects", null=True, blank=True)
    OrderInCategory = models.IntegerField(default=1)
    DiscoveryPoints = models.IntegerField(default=0)
    RequiredProjects = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="RequiredForProjects")
    UnlocksModules = models.ManyToManyField("Production.Module", blank=True, related_name="UnlockedByResearch")
    UnlocksBuildables = models.ManyToManyField("ObjectTypes.ObjectType", blank=True, related_name="UnlockedByResearch")
    UnlocksProductTypes = models.ManyToManyField("Production.ProductType", blank=True, related_name="UnlockedByResearch")

    def getJsonObject(self):
        requiredData = [reqDat.getJsonObject() for reqDat in self.RequiredData.all()]
        requiredProjects = [reqProj.id for reqProj in self.RequiredProjects.all()]
        unlocksModules = [module.id for module in self.UnlocksModules.all()]
        unlocksBuildables = [objType.id for objType in self.UnlocksBuildables.all()]
        unlocksProductTypes = [prodType.id for prodType in self.UnlocksProductTypes.all()]
        category = 0
        if self.Category:
            category = self.Category.id

        return {
            "Name": self.Name,
            "IsHidden": self.IsHidden,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "Tier": self.Tier,
            "Lane": self.Lane,
            "CategoryID": category,
            "OrderInCategory": self.OrderInCategory,
            "DiscoveryPoints": self.DiscoveryPoints,
            "RequiredProjects": requiredProjects,
            "RequiredData": requiredData,
            "UnlocksModules": unlocksModules,
            "UnlocksBuildables": unlocksBuildables,
            "UnlocksProductTypes": unlocksProductTypes
        }

    class Meta:
        verbose_name = 'Development Project'
        verbose_name_plural = 'Development Projects'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)


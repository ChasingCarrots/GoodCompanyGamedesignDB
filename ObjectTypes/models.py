# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import Production
import common

class ObjectType(models.Model):
    Name = models.CharField(max_length=255)

    def getJsonObject(self):
        return {
            "Name": self.Name,
        }

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Object Type'
        verbose_name_plural = 'Object Types'

class MovableProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="MovableProperty", blank=False)
    Width = models.FloatField(default=0, blank=True)
    Height = models.FloatField(default=0, blank=True)
    Radius = models.FloatField(default=0, blank=True)

    def getJsonObject(self):
        movableJson = {}
        if self.Width != 0:
            movableJson["Width"] = self.Width
        if self.Height != 0:
            movableJson["Height"] = self.Height
        if self.Radius != 0:
            movableJson["Radius"] = self.Radius
        return movableJson

    class Meta:
        verbose_name = 'Movable Property'
        verbose_name_plural = 'Movable Properties'

    def __unicode__(self):
        return u"MovableProperty of %s" % (self.ObjectType)


class ObjectLookProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="ObjectLookProperty", blank=False)
    ModelAssetID = models.CharField(max_length=255, blank=False)

    def getJsonObject(self):
        return {
            "ModelAssetID": self.ModelAssetID,
        }

    class Meta:
        verbose_name = 'Object Look Property'
        verbose_name_plural = 'Object Look Properties'

    def __unicode__(self):
        return u"ObjectLookProperty of %s" % (self.ObjectType)


class IconProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="IconProperty", blank=False)
    IconAssetID = models.CharField(max_length=255, help_text="The asset id of the icon for this object.", blank=False)
    TextSpriteAssetID = models.CharField(max_length=255, help_text="The asset id of the TMP spritesheet that contains the text-sprite for this object.", blank=True)
    TextSpriteEntry = models.CharField(max_length=31, help_text="The name of the icon of this object within the TMP spritesheet", blank=True)

    def getJsonObject(self):
        return {
            "IconAssetID": self.IconAssetID,
            "TextSpriteAssetID": self.TextSpriteAssetID,
            "TextSpriteEntry": self.TextSpriteEntry,
        }

    class Meta:
        verbose_name = 'Icon Property'
        verbose_name_plural = 'Icon Properties'

    def __unicode__(self):
        return u"IconProperty of %s" % (self.ObjectType)

class InventoryProperty(models.Model):    
    ObjectType = models.OneToOneField(ObjectType, related_name="InventoryProperty", blank=False)
    SlotType = models.IntegerField(choices=common.SlotTypeChoices, blank=False)
    NumberOfSlots = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "SlotType": self.SlotType,
            "NumberOfSlots": self.NumberOfSlots,
        }

    class Meta:
        verbose_name = 'Inventory Property'
        verbose_name_plural = 'Inventory Properties'

    def __unicode__(self):
        return u"InventoryProperty of %s" % (self.ObjectType)

class StorageProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="StorageProperty", blank=False)
    SizeType = models.IntegerField(choices=common.SizeTypeChoices, blank=False)
    ModelAssetID = models.CharField(max_length=255, help_text="The asset id of the model that should be used to display this object in an inventory view.", blank=True)

    def getJsonObject(self):
        return {
            "SizeType": self.SizeType,
            "ModelAssetID": self.ModelAssetID,
        }

    class Meta:
        verbose_name = 'Storage Property'
        verbose_name_plural = 'Storage Properties'

    def __unicode__(self):
        return u"StorageProperty of %s" % (self.ObjectType)

class BuildablePropertyNeededMaterial(models.Model):
    BuildableProperty = models.ForeignKey("BuildableProperty", related_name="NeededMaterials", blank=False)
    Material = models.ForeignKey(Production.models.Material, blank=False)
    Amount = models.IntegerField(default=0)

    def getJsonObject(self):
        return {
            "MaterialID" : self.Material.id,
            "Amount" : self.Amount,
        }

    class Meta:
        verbose_name = 'NeededMaterial'
        verbose_name_plural = 'NeededMaterials'

    def __unicode__(self):
        return u"%s (%ds)" % (self.Material, self.Amount)

class BuildsObjectConnection(models.Model):
    BuildsObject = models.ForeignKey(ObjectType, related_name="BuildsObjectConnection", blank=False)
    BuiltBy = models.OneToOneField("BuildableProperty", related_name="BuildsObjectConnection", blank=False)

class BuildableProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="BuildableProperty", blank=False)
    BuildDuration = models.FloatField(blank=False)
    BuildCost = models.IntegerField(blank=False)

    def getJsonObject(self):
        neededmats = []
        for mat in self.NeededMaterials.all():
            neededmats.append(mat.getJsonObject())
        return {
            "NeededMaterials":neededmats,
            "BuildDuration":self.BuildDuration,
            "BuildsObjectID":self.BuildsObjectConnection.BuildsObject.id,
            "BuildCost":self.BuildCost,
        }

    class Meta:
        verbose_name = 'Buildable Property'
        verbose_name_plural = 'Buildable Properties'

    def __unicode__(self):
        return u"BuildableProperty of %s" % (self.ObjectType)

class RecurringCostProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="RecurringCostProperty", blank=False)
    RecurringCost = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "RecurringCost":self.RecurringCost,
        }

    class Meta:
        verbose_name = 'RecurringCost Property'
        verbose_name_plural = 'RecurringCost Properties'

    def __unicode__(self):
        return u"RecurringCostProperty of %s" % (self.ObjectType)

class CrafterPropertyModuleStepDuration(models.Model):
    CrafterProperty = models.ForeignKey("CrafterProperty", related_name="PossibleModuleSteps", blank=False)
    ModuleStep = models.ForeignKey(Production.models.ModuleStep, blank=False)
    Duration = models.FloatField(blank=False)

    def getJsonObject(self):
        return {
            "ModuleID": self.ModuleStep.Module.id,
            "StepNumber": self.ModuleStep.StepNumber,
            "Duration": self.Duration
        }

    class Meta:
        verbose_name = 'Possible ModuleStep'
        verbose_name_plural = 'Possible ModuleSteps'

    def __unicode__(self):
        return u"%s (%ds)" % (self.ModuleStep, self.Duration)

class CrafterProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="CrafterProperty", blank=False)
    SwitchingTime = models.FloatField(blank=False, default=1)

    def getJsonObject(self):
        possibleModuleSteps = []
        for step in self.PossibleModuleSteps.all():
            possibleModuleSteps.append(step.getJsonObject())
        return {
            "SwitchingDuration": self.SwitchingTime,
            "PossibleModuleSteps": possibleModuleSteps,
        }

    class Meta:
        verbose_name = 'Crafter Property'
        verbose_name_plural = 'Crafter Properties'

    def __unicode__(self):
        return u"CrafterProperty of %s" % (self.ObjectType)


class AssemblyPropertySlotAssemblyDuration(models.Model):
    AssemblyProperty = models.ForeignKey("AssemblyProperty", related_name="PossibleSlotTypes", blank=False)
    SlotType = models.ForeignKey(Production.models.ModuleSlotType, blank=False)
    Duration = models.FloatField(blank=False)

    class Meta:
        verbose_name = 'Possible SlotType'
        verbose_name_plural = 'Possible SlotTypes'

    def __unicode__(self):
        return u"%s (%ds)" % (self.SlotType, self.Duration)

class AssemblyProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="AssemblyProperty", blank=False)

    def getJsonObject(self):
        slots = []
        for slot in self.PossibleSlotTypes.all():
            slots.append({
                "SlotTypeID":slot.SlotType.id,
                "Duration":slot.Duration,
            })
        return {
            "Slots" : slots,
        }

    class Meta:
        verbose_name = 'Assembly Property'
        verbose_name_plural = 'Assembly Properties'

    def __unicode__(self):
        return u"AssemblyProperty of %s" % (self.ObjectType)

class StaticDimensionPropertyBlockedTile(models.Model):
    StaticDimensionProperty = models.ForeignKey("StaticDimensionProperty", related_name="BlockedTiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)

    class Meta:
        verbose_name = 'Blocked tile'
        verbose_name_plural = 'Blocked tiles'

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)

class StaticDimensionProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="StaticDimensionProperty", blank=False)

    def getJsonObject(self):
        blockedTiles = []
        for tile in self.BlockedTiles.all():
            blockedTiles.append({
                "X": tile.XCoord,
                "Y": tile.YCoord,
            })
        return {
            "BlockedTiles":blockedTiles,
        }

    class Meta:
        verbose_name = 'StaticDimension Property'
        verbose_name_plural = 'StaticDimension Properties'

    def __unicode__(self):
        return u"StaticDimensionProperty of %s" % (self.ObjectType)


class InteractableTilesPropertyInteractableTile(models.Model):
    InteractableTilesProperty = models.ForeignKey("InteractableTilesProperty", related_name="InteractableTiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)

    class Meta:
        verbose_name = 'Interactable tile'
        verbose_name_plural = 'Interactable tiles'

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)


class InteractableTilesProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="InteractableTilesProperty", blank=False)

    def getJsonObject(self):
        interactableTiles = []
        for tile in self.InteractableTiles.all():
            interactableTiles.append({
                "X": tile.XCoord,
                "Y": tile.YCoord,
            })
        return {
            "InteractableTiles": interactableTiles,
        }

    class Meta:
        verbose_name = 'InteractableTiles Property'
        verbose_name_plural = 'InteractableTiles Properties'

    def __unicode__(self):
        return u"InteractableTilesProperty of %s" % (self.ObjectType)


class SpecialFlagsProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="SpecialFlagsProperty", blank=False)
    IsBuyPlace = models.BooleanField(default=False, blank=False)
    IsSellPlace = models.BooleanField(default=False, blank=False)
    IsTrashCan = models.BooleanField(default=False, blank=False)

    def getJsonObject(self):
        return {
            "IsBuyPlace":self.IsBuyPlace,
            "IsSellPlace":self.IsSellPlace,
            "IsTrashCan":self.IsTrashCan
        }

    class Meta:
        verbose_name = 'SpecialFlags Property'
        verbose_name_plural = 'SpecialFlags Properties'

    def __unicode__(self):
        return u"SpecialFlagsProperty of %s" % (self.ObjectType)


class BlueprintPrinterProperty(models.Model):
    ObjectType = models.OneToOneField(ObjectType, related_name="BlueprintPrinterProperty", blank=False)
    PrintingTime = models.FloatField(blank=False)
    NumberOfOutputSlots = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "PrintingTime": self.PrintingTime,
            "NumberOfOutputSlots": self.NumberOfOutputSlots,
        }

    class Meta:
        verbose_name = 'BlueprintPrinter Property'
        verbose_name_plural = 'BlueprintPrinter Properties'

    def __unicode__(self):
        return u"BlueprintPrinterProperty of %s" % (self.ObjectType)

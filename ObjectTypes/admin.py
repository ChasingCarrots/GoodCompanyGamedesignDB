# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from ObjectTypes.models import *

from django.http import HttpResponse

def export_names(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/plain")
    first = True
    for obj in queryset:
        if not first:
            response.write(',\n"%s"' % obj.Name)
        else:
            response.write('"%s"' % obj.Name)
        first = False
    return response

def export_ids(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/plain")
    first = True
    for obj in queryset:
        if not first:
            response.write(',\n%d' % obj.id)
        else:
            response.write('%d' % obj.id)
        first = False
    return response

admin.site.register(BuildabelCategory)

class MovablePropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = MovableProperty
    extra = 0


class ObjectLookPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ObjectLookProperty
    extra = 0


class IconPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = IconProperty
    extra = 0


class InventoryPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = InventoryProperty
    extra = 0


class StoragePropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = StorageProperty
    extra = 0


class BuildablePropertyNeededMaterialInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = BuildablePropertyNeededMaterial
    extra = 0

class BuildablePropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = BuildableProperty
    extra = 0
    inlines = (BuildablePropertyNeededMaterialInlineAdmin,)

class RecurringCostPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = RecurringCostProperty
    extra = 0

class CrafterPropertyModuleDurationInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = CrafterPropertyModuleDuration
    extra = 0

class CrafterPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = CrafterProperty
    extra = 0
    inlines = (CrafterPropertyModuleDurationInlineAdmin,)

class AssemblyPropertyProductTypeAssemblyDurationInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = AssemblyPropertyProductTypeAssemblyDuration
    extra = 0

class AssemblyPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = AssemblyProperty
    extra = 0
    inlines = (AssemblyPropertyProductTypeAssemblyDurationInlineAdmin,)

class InterfaceNodesPropertyInterfaceNodeInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = InterfaceNodesPropertyInterfaceNode
    extra = 0

class InterfaceNodesPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = InterfaceNodesProperty
    extra = 0
    inlines = (InterfaceNodesPropertyInterfaceNodeInlineAdmin,)

class StaticDimensionPropertyBlockedTileInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = StaticDimensionPropertyBlockedTile
    extra = 0

class StaticDimensionPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = StaticDimensionProperty
    extra = 0
    inlines = (StaticDimensionPropertyBlockedTileInlineAdmin,)

class InteractableTilesPropertyInteractableTileInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = InteractableTilesPropertyInteractableTile
    extra = 0

class InteractableTilesPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = InteractableTilesProperty
    extra = 0
    inlines = (InteractableTilesPropertyInteractableTileInlineAdmin,)

class SpecialFlagsPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = SpecialFlagsProperty
    extra = 0

class BlueprintPrinterPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = BlueprintPrinterProperty
    extra = 0

class ResearchAndDevelopmentPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ResearchAndDevelopmentProperty
    extra = 0

class InventoryGroupPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = InventoryGroupProperty
    extra = 0

class ConveyorPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ConveyorProperty
    extra = 0

class LogisticsWorkplaceInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = LogisticsWorkplaceProperty
    extra = 0

class TransferTilesPropertyTileInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = TransferTilesPropertyTile
    extra = 0
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

class TransferTilesPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = TransferTilesProperty
    extra = 0
    inlines = (TransferTilesPropertyTileInlineAdmin,)

class FlagTilesPropertyTileInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = FlagTilesPropertyTile
    extra = 0
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

class FlagTilesPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = FlagTilesProperty
    extra = 0
    inlines = (FlagTilesPropertyTileInlineAdmin,)

class SkillRequirementsInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = SkillRequirementsProperty
    extra = 0

class HasPropertyFilter(admin.SimpleListFilter):
    title = 'Filter title not set'
    parameter_name = 'parameter name not set'

    def lookups(self, request, model_admin):
        return (
            ('not_null', 'Has Property'),
            ('null', 'Doesn\'t have Property'),
        )

    def queryset(self, request, queryset):
        filter_string = self.parameter_name + '__isnull'
        if self.value() == 'not_null':
            is_null_false = {
                filter_string: False
            }
            return queryset.filter(**is_null_false)

        if self.value() == 'null':
            is_null_true = {
                filter_string: True
            }
            return queryset.filter(**is_null_true)

class HasMovablePropertyFilter(HasPropertyFilter):
    title = "Movable Property"
    parameter_name = "MovableProperty"

class HasObjectLookPropertyFilter(HasPropertyFilter):
    title = "ObjectLook Property"
    parameter_name = "ObjectLookProperty"

class HasIconPropertyFilter(HasPropertyFilter):
    title = "Icon Property"
    parameter_name = "IconProperty"

class HasInventoryPropertyFilter(HasPropertyFilter):
    title = "Inventory Property"
    parameter_name = "InventoryProperty"

class HasStoragePropertyFilter(HasPropertyFilter):
    title = "Storage Property"
    parameter_name = "StorageProperty"

class HasBuildablePropertyFilter(HasPropertyFilter):
    title = "Buildable Property"
    parameter_name = "BuildableProperty"

class HasRecurringCostPropertyFilter(HasPropertyFilter):
    title = "RecurringCost Property"
    parameter_name = "RecurringCostProperty"

class HasCrafterPropertyFilter(HasPropertyFilter):
    title = "Crafter Property"
    parameter_name = "CrafterProperty"

class HasAssemblyPropertyFilter(HasPropertyFilter):
    title = "Assembly Property"
    parameter_name = "AssemblyProperty"

class HasInterfaceNodesPropertyFilter(HasPropertyFilter):
    title = "InteractionNodes Property"
    parameter_name = "InteractionNodesProperty"

class HasStaticDimensionPropertyFilter(HasPropertyFilter):
    title = "StaticDimension Property"
    parameter_name = "StaticDimensionProperty"

class HasInteractableTilesPropertyFilter(HasPropertyFilter):
    title = "InteractableTiles Property"
    parameter_name = "InteractableTilesProperty"

class HasSpecialFlagsPropertyFilter(HasPropertyFilter):
    title = "SpecialFlags Property"
    parameter_name = "SpecialFlagsProperty"

class HasBlueprintPrinterPropertyFilter(HasPropertyFilter):
    title = "BlueprintPrinter Property"
    parameter_name = "BlueprintPrinterProperty"

class HasResearchAndDevelopmentPropertyFilter(HasPropertyFilter):
    title = "ResearchAndDevelopment Property"
    parameter_name = "ResearchAndDevelopmentProperty"

class HasInventoryGroupPropertyFilter(HasPropertyFilter):
    title = "InventoryGroup Property"
    parameter_name = "InventoryGroupProperty"

class HasConveyorPropertyFilter(HasPropertyFilter):
    title = "Conveyor Property"
    parameter_name = "ConveyorProperty"

class HasLogisticsWorkplaceFilter(HasPropertyFilter):
    title = "LogisticsWorkplace Property"
    parameter_name = "LogisticsWorkplaceProperty"

class HasSkillRequirementsFilter(HasPropertyFilter):
    title = "SkillRequirements Property"
    parameter_name = "SkillRequirementsProperty"

class ObjectTypeAdmin(SuperModelAdmin):
    actions = [export_names, export_ids]
    list_display = ("id", "__unicode__")
    inlines = (MovablePropertyInlineAdmin,
               ObjectLookPropertyInlineAdmin, 
               IconPropertyInlineAdmin, 
               InventoryPropertyInlineAdmin, 
               StoragePropertyInlineAdmin,
               BuildablePropertyInlineAdmin,
               RecurringCostPropertyInlineAdmin,
               CrafterPropertyInlineAdmin,
               AssemblyPropertyInlineAdmin,
               InterfaceNodesPropertyInlineAdmin,
               StaticDimensionPropertyInlineAdmin,
               InteractableTilesPropertyInlineAdmin,
               SpecialFlagsPropertyInlineAdmin,
               BlueprintPrinterPropertyInlineAdmin,
               ResearchAndDevelopmentPropertyInlineAdmin,
               InventoryGroupPropertyInlineAdmin,
               ConveyorPropertyInlineAdmin,
               LogisticsWorkplaceInlineAdmin,
               TransferTilesPropertyInlineAdmin,
               FlagTilesPropertyInlineAdmin,
               SkillRequirementsInlineAdmin)
    list_filter = (HasMovablePropertyFilter,
                   HasObjectLookPropertyFilter,
                   HasIconPropertyFilter,
                   HasInventoryPropertyFilter,
                   HasStoragePropertyFilter,
                   HasBuildablePropertyFilter,
                   HasRecurringCostPropertyFilter,
                   HasCrafterPropertyFilter,
                   HasAssemblyPropertyFilter,
                   HasInterfaceNodesPropertyFilter,
                   HasStaticDimensionPropertyFilter,
                   HasInteractableTilesPropertyFilter,
                   HasSpecialFlagsPropertyFilter,
                   HasBlueprintPrinterPropertyFilter,
                   HasResearchAndDevelopmentPropertyFilter,
                   HasInventoryGroupPropertyFilter,
                   HasConveyorPropertyFilter,
                   HasLogisticsWorkplaceFilter,
                   HasSkillRequirementsFilter)
admin.site.register(ObjectType, ObjectTypeAdmin)

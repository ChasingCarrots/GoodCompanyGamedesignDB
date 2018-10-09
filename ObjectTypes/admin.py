# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from ObjectTypes.models import *


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

class BuildablePropertyCanBuildInWorkplaceInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = BuildablePropertyCanBuildInWorkplace
    extra = 0

class BuildsObjectConnectionInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = BuildsObjectConnection
    extra = 1

class BuildablePropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = BuildableProperty
    extra = 0
    inlines = (BuildablePropertyNeededMaterialInlineAdmin,
               BuildsObjectConnectionInlineAdmin,
               BuildablePropertyCanBuildInWorkplaceInlineAdmin)


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

class AssemblyPropertySlotAssemblyDurationInlineAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = AssemblyPropertySlotAssemblyDuration
    extra = 0

class AssemblyPropertyInlineAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = AssemblyProperty
    extra = 0
    inlines = (AssemblyPropertySlotAssemblyDurationInlineAdmin,)


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


class ObjectTypeAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
    inlines = (MovablePropertyInlineAdmin,
               ObjectLookPropertyInlineAdmin, 
               IconPropertyInlineAdmin, 
               InventoryPropertyInlineAdmin, 
               StoragePropertyInlineAdmin,
               BuildablePropertyInlineAdmin,
               RecurringCostPropertyInlineAdmin,
               CrafterPropertyInlineAdmin,
               AssemblyPropertyInlineAdmin,
               StaticDimensionPropertyInlineAdmin,
               InteractableTilesPropertyInlineAdmin,
               SpecialFlagsPropertyInlineAdmin,
               BlueprintPrinterPropertyInlineAdmin,
               ResearchAndDevelopmentPropertyInlineAdmin)
    list_filter = (HasMovablePropertyFilter,
                   HasObjectLookPropertyFilter,
                   HasIconPropertyFilter,
                   HasInventoryPropertyFilter,
                   HasStoragePropertyFilter,
                   HasBuildablePropertyFilter,
                   HasRecurringCostPropertyFilter,
                   HasCrafterPropertyFilter,
                   HasAssemblyPropertyFilter,
                   HasStaticDimensionPropertyFilter,
                   HasInteractableTilesPropertyFilter,
                   HasSpecialFlagsPropertyFilter,
                   HasBlueprintPrinterPropertyFilter,
                   HasResearchAndDevelopmentPropertyFilter)
admin.site.register(ObjectType, ObjectTypeAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from Production.models import *


class MaterialSellBuyFilter(admin.SimpleListFilter):
    title = "Sellable/Buyable"
    parameter_name = "sellbuyable"

    def lookups(self, request, model_admin):
        return (
            ("sellable", "Can be sold"),
            ("buyable", "Can be bought"),
        )
    
    def queryset(self, request, queryset):
        if self.value() == "sellable":
            return queryset.filter(SellPrice__gt=0)
        if self.value() == "buyable":
            return queryset.filter(BuyPrice__gt=0)

class MaterialAdmin(SuperModelAdmin):
    list_filter = (MaterialSellBuyFilter, "SizeType",)
    list_display = ("id", "__unicode__", "SizeType",
                    "StackSize", "BuyPrice", "SellPrice",)
admin.site.register(Material, MaterialAdmin)


class ModuleSlotTypeAdmin(SuperModelAdmin):
    list_filter = ("FittingModule", "UsedInProductType",)
    list_display = ("id", "__unicode__", "IsOptional",)
admin.site.register(ModuleSlotType, ModuleSlotTypeAdmin)

class ModuleStepInputMaterialAmountAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleStepInputMaterialAmount
    extra = 0

class ModuleStepOutputMaterialAmountAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleStepOutputMaterialAmount
    extra = 0

class ModuleInputMaterialAmountAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleInputMaterialAmount
    extra = 0

class ModuleStepAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleStep
    inlines = (ModuleStepInputMaterialAmountAdmin,
               ModuleStepOutputMaterialAmountAdmin)
    extra = 0

class ModuleFeatureAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleFeature
    extra = 0

class ModuleAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
    list_filter = ("FitsIntoSlot",)
    inlines = (ModuleInputMaterialAmountAdmin,
               ModuleStepAdmin,
               ModuleFeatureAdmin)
admin.site.register(Module, ModuleAdmin)

class ProductTypeAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
admin.site.register(ProductType, ProductTypeAdmin)

class ProductFeatureAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", "PropagationType", "Unit", "DefaultValue", "MinRange", "MaxRange")
    list_filter = ("PropagationType",)
admin.site.register(ProductFeature, ProductFeatureAdmin)

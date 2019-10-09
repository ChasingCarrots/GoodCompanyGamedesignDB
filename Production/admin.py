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
                    "StackSize", "StackBuyPrice", "getPricePerUnit", "assetCheck")
admin.site.register(Material, MaterialAdmin)


class ModuleSlotTypeAdmin(SuperModelAdmin):
    list_filter = ("FittingModule", "UsedInProductType",)
    list_display = ("id", "__unicode__", "IsOptional",)
admin.site.register(ModuleSlotType, ModuleSlotTypeAdmin)

class ModuleInputMaterialAmountAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleInputMaterialAmount
    extra = 0

class ModuleFeatureAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleFeature
    extra = 0

class ModuleResearchDataYieldAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleResearchDataYield
    extra = 0

class ModuleFieldAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleField
    extra = 0

class ModuleAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", "slot")
    list_filter = ("FitsIntoSlot",)
    inlines = (ModuleInputMaterialAmountAdmin,
               ModuleFeatureAdmin,
               ModuleFieldAdmin,
               ModuleResearchDataYieldAdmin)
admin.site.register(Module, ModuleAdmin)

class ProductTypeSlotUIPositionAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ProductTypeSlotUIPosition
    extra = 0

class ProductTypeFieldAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ProductTypeField
    extra = 0

class PositiveFeatureAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = PositiveFeature
    extra = 0

class NegativeFeatureAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = NegativeFeature
    extra = 0

class MarketPhaseAdmin (SuperInlineModelAdmin, admin.StackedInline):
    model = MarketPhase
    extra = 0
    inlines = (PositiveFeatureAdmin,
               NegativeFeatureAdmin)

class ProductTypeAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
    inlines = (ProductTypeSlotUIPositionAdmin,
               MarketPhaseAdmin,
               ProductTypeFieldAdmin)
admin.site.register(ProductType, ProductTypeAdmin)

class ProductFeatureAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__",)
admin.site.register(ProductFeature, ProductFeatureAdmin)

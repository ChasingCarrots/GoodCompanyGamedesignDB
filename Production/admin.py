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

class ModuleFeatureRequirementAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleFeatureRequirement
    extra = 0

class ModuleResearchDataYieldAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ModuleResearchDataYield
    extra = 0

class ModuleAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", "slot")
    list_filter = ("FitsIntoSlot",)
    inlines = (ModuleInputMaterialAmountAdmin,
               ModuleFeatureAdmin,
               ModuleResearchDataYieldAdmin)
admin.site.register(Module, ModuleAdmin)

class ProductTypeAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
admin.site.register(ProductType, ProductTypeAdmin)

class ProductFeatureAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", "Type",)
    list_filter = ("Type",)
admin.site.register(ProductFeature, ProductFeatureAdmin)

class ProductFunctionFeatureRequirementAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ProductFunctionFeatureRequirement
    extra = 0

class ProductFunctionOptionalFeaturesAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ProductFunctionOptionalFeatures
    extra = 0

class ProductFunctionDrawbacksAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ProductFunctionDrawbacks
    extra = 0

class ProductFunctionAdmin(SuperModelAdmin):
    inlines = (ProductFunctionFeatureRequirementAdmin,
               ProductFunctionOptionalFeaturesAdmin,
               ProductFunctionDrawbacksAdmin,
               )
admin.site.register(ProductFunction, ProductFunctionAdmin)
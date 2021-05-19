# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from Production.models import *

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
    actions = [export_names, export_ids]
    list_filter = (MaterialSellBuyFilter, "SizeType",)
    list_display = ("id", "__unicode__", "SizeType",
                    "StackSize", "StackBuyPrice", "getPricePerUnit", "assetCheck")
admin.site.register(Material, MaterialAdmin)


class ModuleInputMaterialAmountAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleInputMaterialAmount
    extra = 0

class ModuleFeatureAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleFeature
    extra = 0

class ModuleResearchDataYieldAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleResearchDataYield
    extra = 0

class ModuleFieldAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModuleField
    extra = 0

class ModuleCategoryAdmin(SuperModelAdmin):
    pass
admin.site.register(ModuleCategory, ModuleCategoryAdmin)

class ModuleAdmin(SuperModelAdmin):
    actions = [export_names, export_ids]
    list_display = ("id", "__unicode__")
    inlines = (ModuleInputMaterialAmountAdmin,
               ModuleFeatureAdmin,
               ModuleFieldAdmin,
               ModuleResearchDataYieldAdmin)
admin.site.register(Module, ModuleAdmin)

class ProductTypeFieldAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ProductTypeField
    extra = 0

class CaseBlockingFieldAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ProductTypeCaseBlockingField
    extra = 0

class ProductTypeCaseAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ProductTypeCase
    extra = 0
    inlines = (CaseBlockingFieldAdmin,)

class ProductTypeAdmin(SuperModelAdmin):
    actions = [export_names, export_ids]
    list_display = ("id", "__unicode__", )
    inlines = (ProductTypeFieldAdmin,
               ProductTypeCaseAdmin)
admin.site.register(ProductType, ProductTypeAdmin)

class ProductFeatureAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__",)
admin.site.register(ProductFeature, ProductFeatureAdmin)


class SkillTypeCategoryAdmin(SuperModelAdmin):
    pass
admin.site.register(SkillTypeCategory, SkillTypeCategoryAdmin)

class SkillTypeAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__",)
admin.site.register(SkillType, SkillTypeAdmin)
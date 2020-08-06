# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from Research.models import *

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

class ResearchDataTypeAdmin(SuperModelAdmin):
    pass
admin.site.register(ResearchDataType, ResearchDataTypeAdmin)


class DevelopmentProjectRequiredDataAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = DevelopmentProjectRequiredData
    extra = 0

class ProgressNodeRequiredDataAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = ProgressNodeRequiredData
    extra = 0

class ProjectCategoryAdmin(SuperModelAdmin):
    pass
admin.site.register(ProjectCategory, ProjectCategoryAdmin)

class TreeCategoryAdmin(SuperModelAdmin):
    pass
admin.site.register(TreeCategory, TreeCategoryAdmin)


class DevelopmentProjectAdmin(SuperModelAdmin):
    actions = [export_names, export_ids]
    list_filter = ("Tier", "Category")
    list_display = ("id", "__unicode__", "Tier",
                    "Category")
    inlines = (DevelopmentProjectRequiredDataAdmin,)
admin.site.register(DevelopmentProject, DevelopmentProjectAdmin)


class ProgressNodeAdmin(SuperModelAdmin):
    actions = [export_names, export_ids]
    list_filter = ("Tier", "Category")
    list_display = ("id", "__unicode__", "Tier",
                    "Category")
    inlines = (ProgressNodeRequiredDataAdmin,)
admin.site.register(ProgressNode, ProgressNodeAdmin)

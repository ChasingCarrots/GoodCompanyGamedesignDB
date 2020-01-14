# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from Research.models import *

class ResearchDataTypeAdmin(SuperModelAdmin):
    pass
admin.site.register(ResearchDataType, ResearchDataTypeAdmin)

class DevelopmentProjectRequiredDataAdmin(SuperInlineModelAdmin, admin.StackedInline):
    model = DevelopmentProjectRequiredData
    extra = 0

class ProjectCategoryAdmin(SuperModelAdmin):
    pass
admin.site.register(ProjectCategory, ProjectCategoryAdmin)

class DevelopmentProjectAdmin(SuperModelAdmin):
    list_filter = ("Tier", "Category")
    list_display = ("id", "__unicode__", "Tier",
                    "Category")
    inlines = (DevelopmentProjectRequiredDataAdmin,)
admin.site.register(DevelopmentProject, DevelopmentProjectAdmin)

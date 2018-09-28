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

class DevelopmentProjectAdmin(SuperModelAdmin):
    inlines = (DevelopmentProjectRequiredDataAdmin,)
admin.site.register(DevelopmentProject, DevelopmentProjectAdmin)

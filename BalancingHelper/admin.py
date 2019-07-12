# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from BalancingHelper.models import *

admin.site.register(SampleProduct)
admin.site.register(ProgressionValues)

class ModulePathObjectAdmin(SuperInlineModelAdmin, admin.TabularInline):
    model = ModulePathObject
    extra = 0

class CriticalPathAdmin(SuperModelAdmin):
    inlines = (ModulePathObjectAdmin,)
admin.site.register(CriticalModulePath, CriticalPathAdmin)

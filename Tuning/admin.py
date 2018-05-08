# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperModelAdmin

from Tuning.models import TuningValue

class TuningValueAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
admin.site.register(TuningValue, TuningValueAdmin)


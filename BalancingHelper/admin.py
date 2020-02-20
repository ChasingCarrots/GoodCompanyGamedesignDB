# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from BalancingHelper.models import *

class BalanceValueAdmin(SuperModelAdmin):
    list_display = ("id", "__unicode__", )
admin.site.register(BalanceValue, BalanceValueAdmin)

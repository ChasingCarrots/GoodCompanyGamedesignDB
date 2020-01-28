# -*- coding: utf-8 -*-

from Helpers.models import *
from Production.models import *
from Research.models import *
from ObjectTypes.models import *

from StringIO import StringIO
from zipfile import ZipFile

from django.http import HttpResponse


def export_game_data(request):
    output = ""

    output += "local script = {}\n"
    output += "script.materials = {}\n"
    output += "script.modules = {}\n"
    output += "script.module_categories = {}\n"
    output += "script.product_types = {}\n"
    output += "script.features = {}\n"
    output += "script.data_types = {}\n"
    output += "script.researches = {}\n"
    output += "script.buildables = {}\n"
    output += "\n"

    for item in Material.objects.all().order_by("id"):
        output += "script.materials."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in Module.objects.all().order_by("id"):
        output += "script.modules."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in ModuleCategory.objects.all().order_by("id"):
        output += "script.module_categories."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in ProductType.objects.all().order_by("id"):
        output += "script.product_types."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in ProductFeature.objects.all().order_by("id"):
        output += "script.features."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in ResearchDataType.objects.all().order_by("id"):
        output += "script.data_types."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in DevelopmentProject.objects.all().order_by("id"):
        output += "script.researches."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"

    for item in ObjectType.objects.all().order_by("id"):
        output += "script.buildables."+item.Name.replace(" ", "_")+" = "+str(item.id)+"\n"
    output += "\n"
    output += "return script"

    response = HttpResponse(output, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format('gamedata.lua')
    return response

# -*- coding: utf-8 -*-

from Helpers.models import *
from Production.models import *

from StringIO import StringIO
from zipfile import ZipFile

from django.http import HttpResponse


def export_market_progression(request):
    in_memory = StringIO()
    zipfile = ZipFile(in_memory, "a")

    zipfile.writestr("market_handler.lua", str(generate_market_handler_content()))
    for product in ProductType.objects.all():
        path = 'progression_data/progr_' + str(product.Name).lower().replace(' ', '_') + '.lua'
        zipfile.writestr(path, str(generate_market_progression_content(product.id)))

    for file in zipfile.filelist:
       file.create_system = 0

    zipfile.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=goodcompany_basemod_markets.zip"

    in_memory.seek(0)
    response.write(in_memory.read())

    return response


def generate_market_handler_content():
    template = LuaTemplates.objects.filter(Name='market_handler')
    if not template:
        return

    product_template = LuaTemplates.objects.filter(Name='market_handler_product')
    if not product_template:
        return

    output = template[0].Text

    product_text = ""
    for product in ProductType.objects.all():
        text = product_template[0].Text
        text = text.replace("%product_id%", str(product.id))
        text = text.replace("%progression_file%", "progr_" + str(product.Name).lower().replace(" ", "_"))
        product_text = product_text + '\n' + text + '\n'

    output = output.replace("%market_data%", product_text)
    return output

    #response = HttpResponse(output, content_type='text/plain')
    #response['Content-Disposition'] = 'attachment; filename={0}'.format('market_handler.lua')
    #return response


def generate_market_progression_content(product_id):
    product_template = LuaTemplates.objects.filter(Name='market_progression_product')
    if not product_template:
        return

    phase_template = LuaTemplates.objects.filter(Name='market_progression_phase')
    if not phase_template:
        return

    product_data = ProductType.objects.filter(id=product_id)
    if not product_data:
        return

    c = product_template[0].Text
    c = c.replace('%productID%', str(product_data[0].id))
    c = c.replace('%baseDemand%', str(product_data[0].BaseMarketDemand))
    c = c.replace('%basePrice%', str(product_data[0].BaseMarketPrice))

    s = ""
    for phase in MarketPhase.objects.filter(ProductType=product_data):
        phase_text = phase_template[0].Text
        phase_text = phase_text.replace('%phase_id%', str(phase.PhaseIndex))
        phase_text = phase_text.replace('%phase_next_id%', str(phase.PhaseIndex+1))
        phase_text = phase_text.replace('%phase_duration%', str(phase.Duration))
        phase_text = phase_text.replace('%phase_points%', str(phase.DiscoveryPoints))
        phase_text = phase_text.replace('%phase_demand_factor%', str(phase.DemandFactor))
        phase_text = phase_text.replace('%phase_price_factor%', str(phase.PriceFactor))

        text = ""
        count = 0
        for feature in PositiveFeature.objects.filter(MarketPhase=phase):
            count = count + 1
            text = text + "\n\t" + "progression.features["+str(phase.PhaseIndex)+"][" + str(count) + "] = {" + str(feature.Feature.id) + ", " + str(feature.Max) + "}"
        phase_text = phase_text.replace('%phase_features%', text)

        text = ""
        count = 0
        for drawback in NegativeFeature.objects.filter(MarketPhase=phase):
            count = count + 1
            text = text + "\n\t" + "progression.drawbacks["+str(phase.PhaseIndex)+"][" + str(count) + "] = {" + str(drawback.Feature.id) + ", " + str(drawback.Min) + "}"
        phase_text = phase_text.replace('%phase_drawbacks%', text)

        s = s + "\n" + phase_text + "\n\n"
    c = c.replace('%progressionphases%', s)
    return c

    #filename = 'progr_' + str(product_data[0].Name).lower().replace(' ', '_') + '.lua'
    #response = HttpResponse(c, content_type='text/plain')
    #response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)


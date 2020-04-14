"""GoodCompanyGameDesignDB URL Configuration

The `urlpatterns` list routes URLs to view_scripts. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function view_scripts
    1. Add an import:  from my_app import view_scripts
    2. Add a URL to urlpatterns:  url(r'^$', view_scripts.home, name='home')
Class-based view_scripts
    1. Add an import:  from other_app.view_scripts import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from Helpers.views import *
from Helpers.luaExports.gameData import *
from Helpers.view_scripts.modules import *
from Helpers.view_scripts.jsons import *

urlpatterns = [
    url(r'^goodcompany/$', TemplateView.as_view(template_name="helpers/home.html")),
    url(r'^goodcompany/admin/', include(admin.site.urls)),
    url(r'^goodcompany/gamedataManifest/', getManifestJson, name="gamedata"),
    url(r'^goodcompany/json/materials/', json_materials, name="json_materials"),
    url(r'^goodcompany/json/techs/', json_techs, name="json_techs"),
    url(r'^goodcompany/json/equipment/', json_equipment, name="json_equipment"),
    url(r'^goodcompany/viewall/(\w*)', viewAll, name="viewall"),
    url(r'^goodcompany/exportGameData/', export_game_data, name="exportGameData"),
    url(r'^goodcompany/helper/materialoverview/', materialOverview, name="materialoverview"),
    url(r'^goodcompany/helper/materialdetail/(\d+)', materialDetail, name="materialdetail"),
    url(r'^goodcompany/helper/moduleoverview/', module_overview, name="moduleoverview"),
    url(r'^goodcompany/helper/modulecategory/(\d+)', module_category, name="modulecategory"),
    url(r'^goodcompany/helper/moduledetails/(\d+)', module_details, name="moduledetail"),
    url(r'^goodcompany/helper/producttypeoverview/', productTypeOverview, name="producttypeoverview"),
    url(r'^goodcompany/helper/producttypedetail/(\d+)', productTypeDetail, name="producttypedetail"),
    url(r'^goodcompany/helper/productbuilder/', productbuilder, name="productbuilder"),
    url(r'^goodcompany/helper/revertchanges/', revertChangesView, name="revertchanges"),
    url(r'^goodcompany/helper/getbalancingtablejson/(?P<tablename>\w+)/(?P<limitFrom>\d+)/(?P<limitTo>\d+)/(?P<displayMode>\d+)/(?P<logisticTime>\d+)/(?P<option>\w+)', getBalancingTableJson, name="getbalancingtablejson"),
    url(r'^goodcompany/helper/balancingtables', balancingTablesView, name="balancingtables"),
    url(r'^goodcompany/helper/setbalancingtablevalue', setBalancingTableValue, name="setbalancingtablevalue"),
    url(r'^goodcompany/helper/commands', commandsView, name="commands"),
    url(r'^goodcompany/helper/runcommand/(?P<commandname>\w+)/(?P<arguments>[\w|\W]*)', runCommand, name="runcommand"),
    url(r'^goodcompany/helper/researchoverview', researchOverview, name="researchoverview"),
    url(r'^goodcompany/helper/researchdetail/(\d+)', researchDetail, name="researchdetail"),
    url(r'^goodcompany/helper/objectoverview', ObjectOverview, name="objectoverview"),
    url(r'^goodcompany/helper/objectdetailview/(\d+)', ObjectDetails, name="objectdetailview"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

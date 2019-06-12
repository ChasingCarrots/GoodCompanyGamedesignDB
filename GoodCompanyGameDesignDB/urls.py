"""GoodCompanyGameDesignDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
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

urlpatterns = [
    url(r'^goodcompany/$', TemplateView.as_view(template_name="helpers/home.html")),
    url(r'^goodcompany/admin/', include(admin.site.urls)),
    url(r'^goodcompany/gamedataManifest/', getManifestJson),
    url(r'^goodcompany/helper/materialoverview/', materialOverview, name="materialoverview"),
    url(r'^goodcompany/helper/materialdetail/(\d+)', materialDetail, name="materialdetail"),
    url(r'^goodcompany/helper/moduleoverview/', moduleOverview, name="moduleoverview"),
    url(r'^goodcompany/helper/moduledetail/(\d+)', moduleDetail, name="moduledetail"),
    url(r'^goodcompany/helper/producttypeoverview/', productTypeOverview, name="producttypeoverview"),
    url(r'^goodcompany/helper/producttypedetail/(\d+)', productTypeDetail, name="producttypedetail"),
    url(r'^goodcompany/helper/sampleproduct/(\d+)', sampleProduct, name="sampleproduct"),
    url(r'^goodcompany/helper/revertchanges/', revertChangesView, name="revertchanges"),
    url(r'^goodcompany/helper/getbalancingtablejson/(?P<tablename>\w+)/(?P<limitFrom>\d+)/(?P<limitTo>\d+)/(?P<displayMode>\d+)/(?P<logisticTime>\d+)/(?P<option>\w+)', getBalancingTableJson, name="getbalancingtablejson"),
    url(r'^goodcompany/helper/balancingtables', balancingTablesView, name="balancingtables"),
    url(r'^goodcompany/helper/setbalancingtablevalue', setBalancingTableValue, name="setbalancingtablevalue"),
    url(r'^goodcompany/helper/commands', commandsView, name="commands"),
    url(r'^goodcompany/helper/runcommand/(?P<commandname>\w+)/(?P<arguments>\w*)', runCommand, name="runcommand"),
    url(r'^goodcompany/helper/researchoverview', researchOverview, name="researchoverview"),
    url(r'^goodcompany/helper/researchdetail/(\d+)', researchDetail, name="researchdetail"),
    url(r'^goodcompany/helper/functionoverview', functionOverview, name="functionoverview"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

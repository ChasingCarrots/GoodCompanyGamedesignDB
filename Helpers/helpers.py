from django.db.models import Q

from Production.models import *
from ObjectTypes.models import *
from Research.models import *
from Tuning.models import *
from datetime import datetime

def getPossibleCraftersWithBuildCost(module):
    # type: (Module) -> []
    craftersWithBuildCost = []
    compatibleCrafterProperties = CrafterPropertyModuleDuration.objects.filter(Module=module)

    for crafterProp in compatibleCrafterProperties.all():
        crafterObjectType = crafterProp.CrafterProperty.ObjectType
        buildcost = crafterObjectType.BuildableProperty.materialCost()
        craftersWithBuildCost.append({
            "crafter": crafterObjectType,
            "buildcost": buildcost,
        })

    return craftersWithBuildCost

def getNumberOfChangesSince(pointInTime):
    # type: (datetime) -> int
    totalChanges = 0
    for m in models.Model.__subclasses__():
        if hasattr(m, "history"):
            totalChanges += m.history.filter(Q(history_date__gte=pointInTime)).count()
    return totalChanges

def revertChangesTo(pointInTime):
    # type: (datetime) -> int
    numReverted = 0
    for m in models.Model.__subclasses__():
        if hasattr(m, "history"):
            for obj in m.objects.all():
                if obj.history.filter(history_date__gte=pointInTime).exists():
                    objAtPointInTime = obj.history.as_of(pointInTime)
                    objAtPointInTime.save()
                    numReverted += 1
    return numReverted

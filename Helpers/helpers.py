from Production.models import Module
from ObjectTypes.models import CrafterPropertyModuleDuration

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


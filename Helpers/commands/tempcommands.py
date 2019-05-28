from Helpers.balancing.modules import *
from Tuning.models import TuningValue
from commandbase import CommandBase
from Production.models import *
from BalancingHelper.models import *
from ObjectTypes.models import *
from Research.models import *


class InitAllModuleMarketPrices(CommandBase):
    def RunCommand(self, commandline):
        if commandline != "iknow":
            return "THIS WILL OVERWRITE EVERY MODULE'S MARKETPRICE!\nAknowlege this fact by running with the commandline 'iknow'"

        numModules = 0
        addCostPerStep = float(TuningValue.objects.get(Name="ModuleSellPriceAddCostPerStep").Value)
        materialCostFactor = float(TuningValue.objects.get(Name="ModuleSellPriceMaterialCostFactor").Value)
        for module in Module.objects.all():
            price = getComponentProductionSteps(module, True) * addCostPerStep
            price += module.rawMaterialCost() * materialCostFactor
            module.BaseMarketPrice = price
            module.save()
            numModules += 1

        return "Changed the BaseMarketPrice of %d modules" % numModules


def getTreeNode(module, parent, count, materials, parents, amount, amounts, position, positions, depth, depths, maxDepth):
    id = count
    count += 1
    parents.append(parent)
    if (parent != None):
        if type(materials[parent]) == Module:
            amounts.append(float((float(amount) * amounts[parent]) / float(materials[parent].OutputAmount)))
        else:
            amounts.append(float(amount) * amounts[parent])
    else:
        amounts.append(float(amount))
    #modulelist.append(module)
    materials.append(module)
    depth[0] += 1
    depths.append(depth[0])
    positions.append(position[0])
    pos = position[0]
    if (depth[0] > maxDepth[0]):
        maxDepth[0] = depth[0]

    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            count = getTreeNode(moduleMatQuery.all()[0], id, count, materials, parents, float(inputMat.Amount) / float(module.OutputAmount), amounts, position, positions, depth, depths, maxDepth)
        else:
            #if pos > 0:
            #pos += 1
            count += 1
            positions.append(position[0])
            parents.append(id)
            if (parent != None):
                if type(materials[parent]) == Module:
                    amounts.append(float((float(inputMat.Amount) * float(amounts[parent])) / float(module.OutputAmount)))
                else:
                    amounts.append(float(float(inputMat.Amount) * float(amounts[parent])))
            else:
                amounts.append(float(inputMat.Amount))
            materials.append(inputMat.Material)
            depths.append(depth[0]+1)
            position[0] += 1
            if (depth[0]+1 > maxDepth[0]):
                maxDepth[0] = depth[0]+1

    positions[id] = (pos + position[0] - 1) / 2.0
    depth[0] -= 1
    return count

class ProductTree(CommandBase):
    def RunCommand(self, productName):

        productName = str(productName).replace("___", " ")
        output = ""

        count = 0
        depth = []
        position = []
        maxDepth = []

        depth.append(0)
        position.append(0)
        maxDepth.append(0)

        materials = []
        parents = []
        amounts = []
        positions = []
        depths = []

        #productQuery = SampleProduct.objects.filter(Name=str(productName).strip())
        productQuery = SampleProduct.objects.filter(Name=str(productName))
        if productQuery.exists():
            id = count
            count += 1
            parents.append(None)
            amounts.append(float(1))
            materials.append(productQuery.all()[0].ProductFunction)
            depth[0] += 1
            depths.append(depth[0])
            positions.append(position[0])
            pos = position[0]
            if (depth[0] > maxDepth[0]):
                maxDepth[0] = depth[0]
            for module in productQuery.all()[0].Modules.all():
                count = getTreeNode(module, id, count, materials, parents, 1, amounts, position, positions, depth, depths, maxDepth)
            positions[id] = (pos + position[0] - 1) / 2.0


        #moduleQuery = Module.objects.filter(Name=str(productName).strip())
        moduleQuery = Module.objects.filter(Name=productName)
        if moduleQuery.exists():
            count = getTreeNode(moduleQuery.all()[0], None, count, materials, parents, 1, amounts, position, positions, depth, depths, maxDepth)

        paddingX = 160
        paddingY = 80
        size = 40
        distanceX = 0
        distanceY = 0

        output += "<div style='height: "+str((position[0]) * paddingY)+"px; width: "+str((maxDepth[0]) * paddingX)+"px;'>&nbsp;</div>"

        for n in range(count):
            if type(materials[n]) == ProductFunction:
                output += "<a class='tooltip' target='_self' href='/goodcompany/admin/Production/productfunction/"+str(materials[n].id)+"/'>"
                output += "<span class='tooltiptext' style='left: "+str(depths[n] * paddingX + size * 1.2 - paddingX * 0.75)+"px; top: "+str(positions[n] * paddingY + paddingY * 0.5 + size * 0.25)+"px;'>"
                output += materials[n].Name + "</span>"
            if type(materials[n]) == Module:
                output += "<a class='tooltip' target='_self' href='/goodcompany/helper/moduledetail/"+str(materials[n].id)+"/'>"
                output += "<span class='tooltiptext' style='left: "+str(depths[n] * paddingX + size * 1.2 - paddingX * 0.75)+"px; top: "+str(positions[n] * paddingY + paddingY * 0.5 + size * 0.25)+"px;'>"
                output += materials[n].Name + " | output: " + str(materials[n].OutputAmount) + "</span>"
            if type(materials[n]) == Material:
                output += "<a class='tooltip' target='_self' href='/goodcompany/helper/materialdetail/"+str(materials[n].id)+"/'>"
                output += "<span class='tooltiptext' style='left: "+str(depths[n] * paddingX + size * 1.2 - paddingX * 0.75)+"px; top: "+str(positions[n] * paddingY  + paddingY * 0.5 + size * 0.25)+"px;'>"
                output += materials[n].Name + "</span>"

            output += "<img src='/goodcompany/static/img/"+materials[n].IconAssetID+".png' onerror='this.src=\\\"/goodcompany/static/img/unknown.png\\\";' style='z-index: 2;"
            output += "height: "+str(size)+"px; width: "+str(size)+"px; position: absolute; "
            output += "left: "+str(depths[n] * paddingX - paddingX * 0.75)+"px; top: "+str(positions[n] * paddingY + paddingY * 0.5)+"px;' "
            output += "alt='"+materials[n].Name+"'>"

            output += "<p style='position: absolute; z-index: 3; line-height: 80%;"
            output += "height: "+str(size/2)+"px; width: "+str(size*2)+"px; font-size: "+str(size/2)+"px; font-weight: bolder; color: #222; text-align: center; text-shadow: 1px 1px white, -1px 1px white, 1px -1px white, -1px -1px white;"
            output += "left: "+str(depths[n] * paddingX - size * 0.5 - paddingX * 0.75)+"px; top: "+str(positions[n] * paddingY + paddingY * 0.5 + size * 0.5)+"px;'>"


            if type(materials[n]) == ProductFunction:
                output += str("%3.1f" % amounts[n])
            if type(materials[n]) == Module:
                if materials[n].OutputAmount != 1:
                    output += str("%3.1f" % amounts[n])
                    output += "<small><br>("+str("%3.1f" % (amounts[n] / materials[n].OutputAmount))+")</small>"
                else:
                    output += str("%3.1f" % amounts[n])
            if type(materials[n]) == Material:
                output += str("%3.1f" % amounts[n])

            output += "</p></a>"

            if parents[n] != None:
                distanceX = (depths[n] * paddingX - paddingX * 0.75) - (depths[parents[n]] * paddingX - paddingX * 0.75)
                distanceY = (positions[n] * paddingY + paddingY * 0.5 + size * 0.5) - (positions[parents[n]] * paddingY + paddingY * 0.5 + size * 0.5) + 2
                if distanceY >= 0:
                    output += "<svg style='z-index: 1; position: absolute; left: "+str(depths[parents[n]] * paddingX - paddingX * 0.75 + size * 0.5)+"px; top: "+str(positions[parents[n]] * paddingY + paddingY * 0.5 + size * 0.5)+"px;' "
                    output += "width='"+str(distanceX)+"' height='"+str(distanceY)+"'><line x1='0' y1='0' x2='"+str(distanceX)+"' y2='"+str(distanceY)+"' style='stroke:rgb(50,180,250);stroke-width:2' /></svg>"
                else:
                    output += "<svg style='z-index: 1; position: absolute; left: "+str(depths[parents[n]] * paddingX - paddingX * 0.75 + size * 0.5)+"px; top: "+str(positions[n] * paddingY + paddingY * 0.5 + size * 0.5)+"px;' "
                    output += "width='"+str(distanceX)+"' height='"+str(-distanceY)+"'><line x1='0' y1='"+str(-distanceY)+"' x2='"+str(distanceX)+"' y2='0' style='stroke:rgb(50,180,250);stroke-width:2' /></svg>"
        return output
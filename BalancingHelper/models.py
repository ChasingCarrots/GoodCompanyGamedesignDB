# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Production.models import *

class SampleProduct(models.Model):
    Name = models.CharField(max_length=255)
    ProductFunction = models.ForeignKey(ProductFunction)
    Modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'Sample Product'
        verbose_name_plural = 'Sample Products'
        ordering = ['id']

    def __unicode__(self):
        return self.Name

    def collectMaterials(self):
        localMaterials = {}
        for module in self.Modules.all():
            for inputMat in module.InputMaterials.all():
                moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
                if moduleMatQuery.exists():
                    inputModMaterials = moduleMatQuery.all()[0].collectMaterials()
                    for inputModMaterialID, inputModMaterial in inputModMaterials.items():
                        inputModMaterial["amount"] *= inputMat.Amount
                        inputModMaterial["totalcost"] *= inputMat.Amount
                        if inputModMaterialID in localMaterials:
                            localMaterials[inputModMaterialID]["amount"] += inputModMaterial["amount"]
                            localMaterials[inputModMaterialID]["totalcost"] += inputModMaterial["totalcost"]
                        else:
                            localMaterials[inputModMaterialID] = inputModMaterial
                else:
                    inputModMaterialID = inputMat.Material.id
                    if inputModMaterialID in localMaterials:
                        localMaterials[inputModMaterialID]["amount"] += inputMat.Amount
                        localMaterials[inputModMaterialID]["totalcost"] += inputMat.Amount * inputMat.Material.getPricePerUnit()
                    else:
                        localMaterials[inputModMaterialID] = {
                            "name": inputMat.Material.Name,
                            "amount": inputMat.Amount,
                            "totalcost": inputMat.Amount * inputMat.Material.getPricePerUnit(),
                            "icon": inputMat.Material.IconAssetID
                        }
        return localMaterials

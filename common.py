# -*- coding: utf-8 -*-
from __future__ import unicode_literals

NORMALSLOT = 0
LARGESLOT = 1
OBJECTSLOT = 6
MATERIALSLOT = 7
SlotTypeChoices = (
    # accepts small objects and materials, no additional restrictions
    (NORMALSLOT, "NormalSlot"),
    # accepts large objects and materials, no additional restrictions
    (LARGESLOT, "LargeSlot"),
    # accepts all and only objects, additional object restrictions may apply
    (OBJECTSLOT, "ObjectSlot"),
    # accepts all and only materials, additional material restrictions may apply
    (MATERIALSLOT, "MaterialSlot")
)

SizeTypeChoices = (
    # small objects and materials
    (NORMALSLOT, "NormalSlot"),
    # large objects and materials
    (LARGESLOT, "LargeSlot"),
)

MULTIPLICATIVE = 0
MINIMUM = 1
MAXIMUM = 2
ADDITIVE = 3
BOOLEAN_OR = 4
BOOLEAN_AND = 5

PropagationTypeChoices = (
    (MULTIPLICATIVE, "Multiplicative"),
    (MINIMUM, "Minimum"),
    (MAXIMUM, "Maximum"),
    (ADDITIVE, "Additive"),
    (BOOLEAN_OR, "Boolean OR"),
    (BOOLEAN_AND, "Boolean AND"),
)

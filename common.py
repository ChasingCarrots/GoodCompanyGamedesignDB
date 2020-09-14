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

CAT_TREE_BIZDEV = 1
CAT_TREE_MARKET = 2
CAT_TREE_CUSTOM = 99
NodeTreeCategory = (
    # small objects and materials
    (CAT_TREE_BIZDEV, "cat_tree_bizdev"),
    # large objects and materials
    (CAT_TREE_MARKET, "cat_tree_market"),
    # large objects and materials
    (CAT_TREE_CUSTOM, "cat_tree_custom")
)
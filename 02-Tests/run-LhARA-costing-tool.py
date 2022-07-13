#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to execute LhARA costing tool
====================================

  Assumes python path includes LhARA code.

"""

import sys

import Control as Cntrl
iCntrl = Cntrl.Control()

import LhARACostingTool as LCT

##! --------  Initialisation
Debug = False
for arg in sys.argv:
    print(arg)
    if arg == "Debug=true":
        Debug = True
if Debug:
    print(" LhARA costing tool, execution begins.")
    
##! --------  Create instance:
iLCT = LCT.LhARACostingTool(Debug)
print(iLCT)


##! Complete:
print()
print("========  Full LhARA costing data structure created  ========")

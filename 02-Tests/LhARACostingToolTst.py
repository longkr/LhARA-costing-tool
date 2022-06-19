#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "LhARACostingTool" class ... initialisation and get methods
===============================

  LhARACostingTool.py -- set "relative" path to code

"""

import LhARACostingTool as LCT


##! Start:
print("========  LhARACostingTool: tests start  ========")

##! Test singleton class feature:
LhARACostingToolTest = 1
print()
print("LhARACostingToolTest:", LhARACostingToolTest, \
      " check if class is a singleton.")
iLCT  = LCT.LhARACostingTool(False)
iLCT1 = LCT.LhARACostingTool(True)
print("    iLCT singleton test -- OK if 0:", id(iLCT)-id(iLCT1))
if iLCT != iLCT1:
    raise Exception("LhARACostingTool is not a singleton class!")


##! Check built-in methods:
LhARACostingToolTest = 2
print()
print("LhARACostingToolTest:", LhARACostingToolTest, \
      " check built-in methods.")
print("    ----> __repr__:")
print(repr(iLCT))
print("    ----> __str__:")
print(iLCT)


##! Check print and get methods in one fell swoop:
LhARACostingToolTest = 3
print()
print("LhARACostingToolTest:", LhARACostingToolTest, \
      " check Execute method.")
iLCT.Execute()


##! Complete:
print()
print("========  LhARACostingTool: tests complete  ========")

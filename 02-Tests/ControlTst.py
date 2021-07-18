#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Control" class ... initialisation and get methods
===============================

  Control.py -- set "relative" path to code

"""

import os

import Control as cntrl


##! Start:
print("========  Control: tests start  ========")

##! Test singleton class feature:
ControlTest = 1
print()
print("ControlTest:", ControlTest, " check if class is a singleton.")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, \
                         '10-Control/LhARA-costing-tool-control.csv')
iCntrl  = cntrl.Control(filename)
iCntrl1 = cntrl.Control(filename)
print("    iCntrl singleton test:", \
      id(iCntrl), id(iCntrl1), id(iCntrl)-id(iCntrl1))
if iCntrl != iCntrl1:
    raise Exception("Control is not a singleton class!")


##! Check built-in methods:
ControlTest = 2
print()
print("ControlTest:", ControlTest, " check built-in methods.")
print("    ----> __repr__:")
print(repr(iCntrl))
print("    ----> __str__:")
print(iCntrl)


##! Check print and get methods in one fell swoop:
ControlTest = 3
print()
print("ControlTest:", ControlTest, " check get and print methods.")
print("    ----> print() method; tests all get methods")
iCntrl.print()


##! Complete:
print()
print("========  Control: tests complete  ========")

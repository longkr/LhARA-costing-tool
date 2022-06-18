#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Progress" class
================================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import datetime as DT

import WorkPackage as wp
import Task        as Tsk
import Progress    as Prg

##! Start:
print("========  Progress: tests start  ========")

#.. Create dummy task:
print("  Create dummy work package and task instances:")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
Tsk1 = Tsk.Task("LhARA", WP1)
print('    ----> instances WP1 and Tsk1 created.')

#.. Create date:
DateToday = datetime.datetime.now()

##! Check built-in methods:
ProgressTest = 1
print()
print("ProgressTest:", ProgressTest, " check built-in methods.")

#.. __init__
print("  __init__:")
print("    ----> Attempt to create instance with correct call:")
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, 23)
except:
    print('      !!!!> Failed to create instance.')
    raise Exception
print('    <---- instance Prg1 created.')

##! Complete:
print()
print("========  Progress: tests complete  ========")


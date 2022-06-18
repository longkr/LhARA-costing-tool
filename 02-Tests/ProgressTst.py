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
DateToday = DT.datetime.now()
print('    ----> Date instance:', DateToday)

print('  <---- Prerequisits created.')

##! Check built-in methods:
ProgressTest = 1
print()
print("ProgressTest:", ProgressTest, " check built-in methods.")

#.. __init__
print("  __init__:")
print("    ----> Attempt to create instance with correct call:")
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, 23.0)
except:
    print('      !!!!> Failed to create instance.')
    raise Exception
print('    <---- instance Prg1 created.')
#.. __repr__
print("  __repr__:")
print("    ---->", repr(Prg1))
print("    <---- __repr__ done.")
#.. __str__
print("  __str__:")
print(str(Prg1))
print("    <---- __str__ done.")
print("    ----> Check wrong-argument traps:")
Dummy = None
try:
    Prg1 = Prg.Progress(Done, DateToday, 0.15, 23.0)
except:
    print('      ----> Correctly trapped Task instance.')
else:
    print('      !!!!> Failed to trap _Task not instance of Task.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, Dummy, 0.15, 23.0)
except:
    print('      ----> Correctly trapped Date instance.')
else:
    print('      !!!!> Failed to trap _Date not instance of datetime.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, Dummy, 23.0)
except:
    print('      ----> Correctly trapped CompletionFraction error.')
else:
    print('      !!!!> Failed to trap FractionComplete not float.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, Dummy)
except:
    print('      ----> Correctly trapped Spend error.')
else:
    print('      !!!!> Failed to trap Spend not float.')
    raise Exception
print('    <---- Wrong argument tests done.')

##! Complete:
print()
print("========  Progress: tests complete  ========")


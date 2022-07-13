#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "TaskEquip" class
=================================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import numpy as np

import Control as Cntrl
iCntrl = Cntrl.Control()

import WorkPackage as wp
import Task as Tsk
import Equipment as Eqp
import TaskEquipment as TskEqp

##! Start:
print("========  TaskEquip: tests start  ========")

##! Check built-in methods:
TaskEquipTest = 1
print()
print("TaskEquipTest:", TaskEquipTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    TskEqp1 = TskEqp.TaskEquip("TskEqp", "Eqp")
except:
    print('      ----> Strings for i/p: successfully trapped.')
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
Tsk1 = Tsk.Task("LhARA", WP1)
Eqp1 = Eqp.Equipment("LhARA1")
try:
    TskEqp1 = TskEqp.TaskEquipment(Tsk1, Eqp1)
except:
    print('      ----> Instances for input: Failed to create instance.')
    raise Exception
print('      ----> instance TskEqp1 created.')
print("    <---- __init__ done.")

#.. __repr__
print("    __repr__:")
print("      ---->", repr(TskEqp1))
print("    <---- __repr__ done.")

#.. __str__
print("    __str__:")
print(str(TskEqp1))
print("    <---- __str__ done.")


##! Check getInstance method:
TaskEquipTest = 2
print()
print("TaskEquipTest:", TaskEquipTest, " check getInstance method.")
Tsk2 = Tsk.Task("LhARA", WP1)
Eqp2 = Eqp.Equipment("LhARA1")
TskEqp2 = TskEqp.TaskEquipment(Tsk1, Eqp1)
TskEqp3 = TskEqp.TaskEquipment(Tsk2, Eqp1)
TskEqp4 = TskEqp.TaskEquipment(Tsk1, Eqp2)
inst = TskEqp.TaskEquipment.getInstance(Tsk2, Eqp2)
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = TskEqp.TaskEquipment.getInstance(Tsk1, Eqp1)
except TskEqp.DuplicateTaskEquipmentClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = TskEqp.TaskEquipment.getInstance(Tsk2, Eqp1)
if inst == TskEqp3:
    print('      ----> Correctly found: \n', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = TskEqp.TaskEquipment.getInstance(Tsk1, Eqp2)
if inst == TskEqp4:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Check print methods:
TaskEquipTest = 3
print()
print("TaskEquipTest:", TaskEquipTest, " check dump of class contents")
EqpDtFrm = TskEqp.TaskEquipment.print()
print("    <---- Done.")


##! Check print methods:
TaskEquipTest = 4
print()
print("TaskEquipTest:", TaskEquipTest, " check cleaning method")
TskEqp2._Task      = None
TskEqp3._Equipment = None
print("    ----> before clean: number of instances:", \
      TskEqp.TaskEquipment.getNumberOfInstances(), " dump:")
EqpDtFrm = TskEqp.TaskEquipment.print()
nDel = TskEqp.TaskEquipment.clean()
print("    ----> after clean: number of instances:", \
      TskEqp.TaskEquipment.getNumberOfInstances(), " dump:")
EqpDtFrm = TskEqp.TaskEquipment.print()
print("    <---- Done.")


##! Complete:
print()
print("========  TaskEquipment: tests complete  ========")

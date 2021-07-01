#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "TaskStaff" class
=================================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import numpy as np

import WorkPackage as wp
import Task as Tsk
import Staff as Stff
import TaskStaff as TskStff

##! Start:
print("========  TaskStaff: tests start  ========")

##! Check built-in methods:
TaskStaffTest = 1
print()
print("TaskStaffTest:", TaskStaffTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    TskStff1 = TskStff.TaskStaff("TskStff", "Stff")
except:
    print('      ----> Strings for i/p: successfully trapped.')
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
Tsk1 = Tsk.Task("LhARA", WP1)
Stf1 = Stff.Staff("LhARA1", "Vatican")
try:
    TskStff1 = TskStff.TaskStaff(Tsk1, Stf1)
except:
    print('      ----> Instances for input: Failed to create instance.')
    raise Exception
print('      ----> instance TskStff1 created.')
print("    <---- __init__ done.")

#.. __repr__
print("    __repr__:")
print("      ---->", repr(TskStff1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(TskStff1))
print("    <---- __str__ done.")


##! Check getInstance method:
TaskStaffTest = 2
print()
print("TaskStaffTest:", TaskStaffTest, " check getInstance method.")
Tsk2 = Tsk.Task("LhARA", WP1)
Stf2 = Stff.Staff("LhARA1", "Vatican")
TskStf2 = TskStff.TaskStaff(Tsk1, Stf1)
TskStf3 = TskStff.TaskStaff(Tsk2, Stf1)
TskStf4 = TskStff.TaskStaff(Tsk1, Stf2)
inst = TskStff.TaskStaff.getInstance(Tsk2, Stf2)
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = TskStff.TaskStaff.getInstance(Tsk1, Stf1)
except TskStff.DuplicateTaskStaffClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = TskStff.TaskStaff.getInstance(Tsk2, Stf1)
if inst == TskStf3:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = TskStff.TaskStaff.getInstance(Tsk1, Stf2)
if inst == TskStf4:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")


##! Check get/set methods:
TaskStaffTest = 3
print()
print("TaskStaffTest:", TaskStaffTest, " check get/set methods.")
StfFracByYrNQtr = np.array( [[0.1, 0.2, 0.3, 0.4], \
                             [0.1, 0.2, 0.3, 0.4], \
                             [0.1, 0.2, 0.3, 0.4], \
                             [0.1, 0.2, 0.3, 0.4], \
                             [0.1, 0.2, 0.3, 0.4]] )
TskStf2.setStaffFracByYrNQtr(StfFracByYrNQtr)
TskStf2.setStaffFracByYear()
TskStf2.setTotalStaffFrac()
TskStf2.setStaffCostByYear()
TskStf2.setTotalStaffCost()
print(TskStf2)


##! Check costing methods:
TaskStaffTest = 4
print()
print("TaskStaffTest:", TaskStaffTest, " check costing methods.")
print("    ----> Clean TaskStaff instances:")
nDel = TskStff.TaskStaff.clean()
print("    ----> Removed ", nDel, "instances.")
print("    ----> Run doTaskStaffCosting:")
TskStff.TaskStaff.doCosting()
print("          Result:")
for iTskStf in TskStff.TaskStaff.instances:
    print(iTskStf)
print("    <---- Done.")


##! Complete:
print()
print("========  TaskStaff: tests complete  ========")

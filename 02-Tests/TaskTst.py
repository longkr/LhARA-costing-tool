#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Task" class
============================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import numpy as np

import Control as Cntrl
iCntrl = Cntrl.Control()

import WorkPackage as wp
import Task        as Tsk
import TaskStaff   as TskStf

##! Start:
print("========  Task: tests start  ========")

##! Check built-in methods:
TaskTest = 1
print()
print("TaskTest:", TaskTest, " check built-in methods.")
#.. __init__
print("    __init__:")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
try:
    Tsk1 = Tsk.Task("LhARA", WP1)
except:
    print('      ----> Failed to create instance.')
    raise Exception
print('      ----> instance Tsk1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Tsk1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Tsk1))
print("    <---- __str__ done.")

##! Check getInstance method:
TaskTest = 2
print()
print("TaskTest:", TaskTest, " check getInstance method.")
Tsk2 = Tsk.Task("Test-1", WP1)
Tsk3 = Tsk.Task("Test-2", WP1)
Tsk4 = Tsk.Task("Test-2", WP1)
inst = Tsk.Task.getInstance("Dummy", WP1)
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = Tsk.Task.getInstance("Test-2", WP1)
except Tsk.DuplicateTaskClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = Tsk.Task.getInstance("Test-1", WP1)
if inst == Tsk2:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = Tsk.Task.getInstance("LhARA", WP1)
if inst == Tsk1:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Check get/set methods:
TaskTest = 3
print()
print("TaskTest:", TaskTest, " check get/set methods.")
StaffCostByYear = np.array([1., 2., 3., 4., 5.])
Tsk1.setStaffCostByYear(StaffCostByYear)
Tsk1.setCGStaffCostByYear(StaffCostByYear)
Tsk1.setTotalStaffCost()
Tsk1.setTotalCGStaffCost()
Tsk1.setEquipmentCostByYear(StaffCostByYear)
Tsk1.setTotalEquipmentCost()
print(Tsk1)

##! Check creation of pandas dataframe:
TaskTest = 4
print()
print("TaskTest:", TaskTest, " test creation of pandas dataframe.")
TskDtFrm = Tsk.Task.createPandasDataframe()
print("    <---- Done.")


##! Check creation of pandas dataframe:
TaskTest = 5
print()
print("TaskTest:", TaskTest, " test creation of csv file.")
try:
    Tsk.Task.createCSV(TskDtFrm, '99-Scratch/Task.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Check costing methods:
TaskTest = 6
print()
print("TaskTest:", TaskTest, " check costing methods.")
print("    ----> Clean Task instances:")
TskN  = Tsk.Task(None, WP1)
TskN1 = Tsk.Task("Name", None)
nDel = Tsk.Task.clean()
print("    ----> Removed ", nDel, "instances.")
nDel = TskStf.TaskStaff.clean()
TskStf.TaskStaff.doCosting()
print("    ----> Run doTaskCosting:")
Tsk.Task.doCosting()
print("          Result:")
for iTsk in Tsk.Task.instances:
    print(iTsk)
print("    <---- Done.")


##! Complete:
print()
print("========  Task: tests complete  ========")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Project" class
===============================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.  Then works througth the various
  methods in the class.

"""

import numpy as np

import Project     as Prj
import WorkPackage as wp
import Task        as Tsk
import TaskStaff   as TskStf

##! Start:
print("========  Project: tests start  ========")

##! Check built-in methods:
ProjectTest = 1
print()
print("ProjectTest:", ProjectTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    Prj0 = Prj.Project()
except:
    print('      ----> Correctly trapped no-name exception')
try:
    Prj1 = Prj.Project("LhARA")
except:
    print('      ----> Failed to create instance.')
    raise Exception
print('      ----> instance Prj1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Prj1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Prj1))
print("    <---- __str__ done.")


##! Check getInstance method:
ProjectTest = 2
print()
print("ProjectTest:", ProjectTest, " check getInstance method.")
Prj2 = Prj.Project("Test-1")
Prj3 = Prj.Project("Test-2")
Prj4 = Prj.Project("Test-2")
inst = Prj.Project.getInstance("Dummy")
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = Prj.Project.getInstance("Test-2")
except Prj.DuplicateProjectClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = Prj.Project.getInstance("Test-1")
if inst == Prj2:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = Prj.Project.getInstance("LhARA")
if inst == Prj1:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Check get/set methods:
ProjectTest = 3
print()
print("ProjectTest:", ProjectTest, " check get/set methods.")
StaffCostByYear = np.array([1., 2., 3., 4., 5.])
Prj1.setStaffCostByYear(StaffCostByYear)
Prj1.setCGStaffCostByYear(StaffCostByYear)
Prj1.setTotalStaffCost()
Prj1.setTotalCGStaffCost()
Prj1.setEquipmentCostByYear(StaffCostByYear)
Prj1.setTotalEquipmentCost()
Prj1.setTrvlCnsmCostByYear(StaffCostByYear)
Prj1.setTotalTrvlCnsmCost()
print(Prj1)

##! Check creation of pandas dataframe:
ProjectTest = 4
print()
print("ProjectTest:", ProjectTest, " test creation of pandas dataframe.")
PrjDtFrm = Prj.Project.createPandasDataframe()
print("    <---- Done.")


##! Check creation of pandas dataframe:
ProjectTest = 5
print()
print("ProjectTest:", ProjectTest, " test creation of csv file.")
try:
    Prj.Project.createCSV(PrjDtFrm, '99-Scratch/Project.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Check costing methods:
ProjectTest = 6
print()
print("ProjectTest:", ProjectTest, " check costing methods.")
print("    ----> Clean Project instances:")
print("          ----> Before clean:")
for iPrj in Prj.Project.instances:
    print(iPrj)
nDel = Prj.Project.clean()
print("          ----> After clean:")
print("              ----> Removed ", nDel, "instances. \n",
      "                    Instances that remain:")
for iPrj in Prj.Project.instances:
    print(iPrj)
nDel = wp.WorkPackage.clean()
nDel = Tsk.Task.clean()
nDel = TskStf.TaskStaff.clean()
TskStf.TaskStaff.doCosting()
Tsk.Task.doCosting()
wp.WorkPackage.doCosting()
print("    ----> Run doCosting:")
Prj.Project.doCosting()
print("          Result:")
for iPrj in Prj.Project.instances:
    print(iPrj)
print("    <---- Done.")


##! Complete:
print()
print("========  Project: tests complete  ========")

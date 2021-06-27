#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "WorkPackage" class
===================================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""
import os
import numpy as np

import WorkPackage as wp
import Task        as Tsk
import TaskStaff   as TskStf

##! Start:
print("========  WorkPackage: tests start  ========")

##! Check built-in methods:
WorkPackageTest = 1
print()
print("WorkPackageTest:", WorkPackageTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    WP1 = wp.WorkPackage()
except wp.NoFilenameProvided:
    print('      ----> Correctly caught absense of filename exception.')
try:
    WP1 = wp.WorkPackage('NonExistantFile.csv')
except wp.NonExistantFile:
    print('      ----> Correctly caught non-existent file exception.')
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
print('      ----> instance WP1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(WP1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(WP1))
print("    <---- __str__ done.")

##! Check get/set methods:
WorkPackageTest = 2
print()
print("WorkPackageTest:", WorkPackageTest, " check get/set methods.")
print("    ----> CSV filename: ", WP1.getFilename())

##! Check get/set methods:
WorkpackageTest = 3
print()
print("WorkpackageTest:", WorkpackageTest, " check get/set methods.")
StaffCostByYear = np.array([1., 2., 3., 4., 5.])
WP1.setStaffCostByYear(StaffCostByYear)
WP1.setCGStaffCostByYear(StaffCostByYear)
WP1.setTotalStaffCost()
WP1.setTotalCGStaffCost()
WP1.setEquipmentCostByYear(StaffCostByYear)
WP1.setTotalEquipmentCost()
WP1.setTrvlCnsmCostByYear(StaffCostByYear)
WP1.setTotalTrvlCnsmCost()
print(WP1)

##! Check creation of pandas dataframe:
WorkpackageTest = 4
print()
print("WorkpackageTest:", WorkpackageTest, " test creation of pandas dataframe.")
WPDtFrm = wp.WorkPackage.createPandasDataframe()
print("    <---- Done.")


##! Check creation of pandas dataframe:
WorkpackageTest = 5
print()
print("WorkpackageTest:", WorkpackageTest, " test creation of csv file.")
try:
    wp.WorkPackage.createCSV(WPDtFrm, '99-Scratch/Workpackage.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Check costing methods:
WorkpackageTest = 6
print()
print("WorkpackageTest:", WorkpackageTest, " check costing methods.")
print("    ----> Clean Workpackage instances:")
nDel = wp.WorkPackage.clean()
print("    ----> Removed ", nDel, "instances.")
nDel = Tsk.Task.clean()
nDel = TskStf.TaskStaff.clean()
TskStf.TaskStaff.doCosting()
Tsk.Task.doCosting()
print("    ----> Run doCosting:")
wp.WorkPackage.doCosting()
print("          Result:")
for iWP in wp.WorkPackage.instances:
    print(iWP)
print("    <---- Done.")

##! Complete:
print()
print("========  WorkPackage: tests complete  ========")

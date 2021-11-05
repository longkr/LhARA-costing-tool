#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "OtherNonStaff" class
============================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import numpy as np

import OtherNonStaff as ONS
import WorkPackage   as wp

##! Start:
print("========  OtherNonStaff: tests start  ========")


##! Check built-in methods:
OtherNonStaffTest = 1
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    ONS0 = ONS.OtherNonStaff()
except ONS.OtherNonStaffNoWP:
    print('      ----> Successfully trapped OtherNonStaff exception.')
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/Dummy4Test.csv')
WP1 = wp.WorkPackage(filename)
print('      ----> instance WP1 created.')
try:
    ONS1 = ONS.OtherNonStaff("LhARA", WP1)
except:
    print('      ----> Failed to create instance.')
    raise Exception
print('      ----> instance ONS1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(ONS1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(ONS1)
print("    <---- __str__ done.")


##! Check getInstance method:
OtherNonStaffTest = 2
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " check getInstance method.")
ONS2 = ONS.OtherNonStaff("Test-1", WP1)
ONS3 = ONS.OtherNonStaff("Test-2", WP1)
ONS4 = ONS.OtherNonStaff("Test-2", WP1)
inst = ONS.OtherNonStaff.getInstance("Dummy")
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = ONS.OtherNonStaff.getInstance("Test-2")
except ONS.DuplicateOtherNonStaffClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = ONS.OtherNonStaff.getInstance("Test-1")
if inst == ONS2:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = ONS.OtherNonStaff.getInstance("LhARA")
if inst == ONS1:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Check get/set methods:
OtherNonStaffTest = 3
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " test get/set methods.")
print("    ----> Set OtherNonStaff cost and total")
ONSCost = np.array([1., 2., 3., 4., 5.])
ONS1.setOtherNonStaffCost(ONSCost)
ONS2.setOtherNonStaffCost(ONSCost)
ONS3.setOtherNonStaffCost(ONSCost)
ONS4.setOtherNonStaffCost(ONSCost)
ONS1.setTotalOtherNonStaffCost()
ONS2.setTotalOtherNonStaffCost()
ONS3.setTotalOtherNonStaffCost()
ONS4.setTotalOtherNonStaffCost()
print(ONS1)
print(ONS2)
print(ONS3)
print(ONS4)
print("    <---- Done.")


##! Check getInstance method:
OtherNonStaffTest = 4
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " check print method.")
ONS.OtherNonStaff.print()
print("    <---- Done.")


##! Check creation of pandas dataframe:
OtherNonStaffTest = 5
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " test creation of pandas dataframe.")
ONSDtFrm = ONS.OtherNonStaff.createPandasDataframe()
print(ONSDtFrm)
print("    <---- Done.")


##! Check creation of CSV file:
OtherNonStaffTest = 6
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " test creation of csv file.")
try:
    ONS.OtherNonStaff.createCSV(ONSDtFrm, '99-Scratch/OtherNonStaff.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Check cleaning:
OtherNonStaffTest = 7
print()
print("OtherNonStaffTest:", OtherNonStaffTest, " test cleaning of OtherNonStaff list.")
nDel = ONS.OtherNonStaff.clean()
print("    ----> ", nDel, " items of OtherNonStaff deleted")
print("    <---- Done.")


##! Complete:
print()
print("========  OtherNonStaff: tests complete  ========")

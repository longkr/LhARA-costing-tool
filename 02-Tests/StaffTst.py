#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Staff" class
============================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import os
import Staff as Stf

##! Start:
print("========  Staff: tests start  ========")

##! Check built-in methods:
StaffTest = 1
print()
print("StaffTest:", StaffTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    Stf00 = Stf.Staff()
except:
    print('      ----> Correctly trapped no name/no staff code exception.')
try:
    Stf01 = Stf.Staff("StffCd", "LhARA1", None, "Vatican")
except:
    print('      ----> Failed to create instance.')
    raise Exception
try:
    Stf02 = Stf.Staff(62, "LhARA2", None, "Vatican")
except:
    print('      ----> Failed to create instance.')
    raise Exception
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '12-Staff/StaffDatabase.csv')
print("      ----> Staff database file name:", filename)
try:
    Stf1 = Stf.Staff("LhARA", "LhARA", filename)
except:
    print('      ----> Failed to create instance.')
    raise Exception
print('      ----> instance Stf1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
#print("      ---->", repr(Stf1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Stf1))
print("    <---- __str__ done.")

##! Check getInstance method:
StaffTest = 2
print()
print("StaffTest:", StaffTest, " check getInstance method.")
Stf2 = Stf.Staff("Test-1", "Test-1")
Stf3 = Stf.Staff("Test-2", "Vatican")
Stf4 = Stf.Staff("Test-2", "Vatican")
inst = Stf.Staff.getInstance("Dummy")
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = Stf.Staff.getInstance("Test-2")
except Stf.DuplicateStaffClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = Stf.Staff.getInstance("Test-1")
if inst == Stf2:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = Stf.Staff.getInstance("LhARA")
if inst == Stf1:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Load the staff data base:
StaffTest = 3
print()
print("StaffTest:", StaffTest, " test load staff database call.")
print("    ----> parseStaffDatabase load test")
try:
    Tst = Stf.Staff.parseStaffDatabase()
except:
    print("        ----> Correctly trapped no filename.")
try:
    Tst = Stf.Staff.parseStaffDatabase("Dummy")
except:
    print("        ----> Correctly trapped file does not exist.")
try:
    Tst = Stf.Staff.parseStaffDatabase(filename)
    print("        ----> OK!")
except:
    print("        ----> FAILED.")
print("    <---- Load test done")

##! Check get/set methods:
StaffTest = 3
print()
print("StaffTest:", StaffTest, " test get/set methods.")
print("    ----> Set parameters")
Stf1.setAnnualCost(101.)
Stf2.setAnnualCost(102.)
Stf3.setAnnualCost(103.)
Stf4.setAnnualCost(104.)
print(Stf1)
print(Stf2)
print(Stf3)
print(Stf4)
print("    ----> header list check:")
print("      ", Stf.Staff.getHeader())
print("    ----> staff data print check:")
print("      ", Stf2.getData())
print("    ----> Check number of staff:", Stf.Staff.getNumberOfStaff())
print("    <---- Done.")


##! Check creation of pandas dataframe:
StaffTest = 4
print()
print("StaffTest:", StaffTest, " test creation of pandas dataframe.")
StfDtFrm = Stf.Staff.createPandasDataframe()
print("    <---- Done.")

##! Check creation of pandas dataframe:
StaffTest = 5
print()
print("StaffTest:", StaffTest, " test creation of csv file.")
try:
    Stf.Staff.createCSV(StfDtFrm, '99-Scratch/Staff.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Check cleaning of staff databaee:
StaffTest = 5
print()
print("StaffTest:", StaffTest, " test cleaning of staff database.")
iCln = Stf.Staff.cleanStaffDatabase()
print("     cleanStaffDatabase return code: ", iCln)
print("     <---- Done.")


##! Check printing of staff databaee:
StaffTest = 6
print()
print("StaffTest:", StaffTest, " test printing of staff database.")
StfDtFrm = Stf.Staff.createPandasDataframe()
Stf.Staff.printStaffDatabase(StfDtFrm)
print("     <---- Done.")


##! Complete:
print()
print("========  Staff: tests complete  ========")

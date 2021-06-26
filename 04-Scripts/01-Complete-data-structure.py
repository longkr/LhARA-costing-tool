#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate full LhARA costing data structure
====================================================

  Assumes python path includes LhARA code.


"""

import os

import Staff       as Stf
import WorkPackage as wp
import TaskStaff   as TskStf

##! Start:
print("========  Generate full LhARA costing data structure  ========")

print()
print("---->  Read project definition files <----")

##! Read staff data base:
CDSsection = 1
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " read staff data base.")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '12-Staff/StaffDatabase.csv')
nStf = Stf.Staff.parseStaffDatabase(filename)
print("    ----> Staff data base read; ", nStf, " instances of Staff created.")
nDel = Stf.Staff.cleanStaffDatabase()
print("    ----> Staff data base cleaned; ", nDel, " instances of Staff deleted.")
print("          Now ", Stf.Staff.getNumberOfStaff(), " remain.")

##! Read work package definition files:
CDSsection = 2
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " read staff work packages.")
LhARAPATH = os.getenv('LhARAPATH')
DirName  = os.path.join(LhARAPATH, '11-WorkPackages')
wpList    = os.listdir(DirName)
print("    ----> list of WP definition files:", wpList)
wpInst = []
for wpFile in wpList:
    if wpFile.find('.csv') <= 0:
        raise ValueError("Bad file name", wpFile)
    else:
        FileName = os.path.join(DirName, wpFile)
        print("    ----> Reading data from: ", FileName)
        wpInst.append(wp.WorkPackage(FileName))
print("         ", len(wpInst), " work packages intialised:")
for Inst in wpInst:
    print("           ", Inst._WorkpackageName)
print("    <---- Done.")

print()
print("---->  Project definition files Read <----")

print()
print("---->  Do costing! Complete data structure.  <----")

##! TaskStaff
CDSsection = 3
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " cost staff in task staff.")
nDel = TskStf.TaskStaff.cleanTaskStaff()
print("    ----> Removed ", nDel, "instances.")
print("    ----> Run doTaskStaffCosting:")
TskStf.TaskStaff.doTaskStaffCosting()

    

##! Complete:
print()
print("========  Full LhARA costing data structure created  ========")

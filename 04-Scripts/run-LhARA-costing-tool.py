#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to execute LhARA costing tool
====================================

  Assumes python path includes LhARA code.

"""

##! --------  System imports:
import os
import sys


##! --------  Initialisation
Debug = False
for arg in sys.argv:
    if arg == "Debug=true":
        Debug = True
if Debug:
    print(" LhARA costing tool, execution begins.")

    
##! --------  Identify necessary files:
HOMEPATH     = os.getenv('HOMEPATH')

ControlPath1 = os.path.join(HOMEPATH, '10-Control')
ControlPath2 = os.path.join(HOMEPATH, 'Control')
if os.path.isdir(ControlPath1):
    ControlFile  = os.path.join(HOMEPATH, \
                            '10-Control/LhARA-costing-tool-control.csv')
elif os.path.isdir(ControlPath2):
    ControlFile  = os.path.join(HOMEPATH, \
                            'Control/LhARA-costing-tool-control.csv')
else:
    raise NameError('Cant find control file')
if Debug:
    print("    Control file: \n", \
          "            ----> ", ControlFile)
StaffPath1 = os.path.join(HOMEPATH, '12-Staff')
StaffPath2 = os.path.join(HOMEPATH, 'Staff')
if os.path.isdir(StaffPath1):
    StaffDatabaseFile = os.path.join(HOMEPATH, \
                            '12-Staff/StaffDatabase.csv')
elif os.path.isdir(StaffPath2):
    StaffDatabaseFile = os.path.join(HOMEPATH, \
                            'Staff/StaffDatabase.csv')
else:
    raise NameError('Cant find staff database')
if Debug:
    print("    Staff database file: \n", \
          "            ----> ", StaffDatabaseFile)
wpPath1 = os.path.join(HOMEPATH, '11-WorkPackages')
wpPath2 = os.path.join(HOMEPATH, 'WorkPackages')
if os.path.isdir(wpPath1):
    wpDirectory = os.path.join(HOMEPATH, \
                            '11-WorkPackages')
elif os.path.isdir(wpPath2):
    wpDirectory = os.path.join(HOMEPATH, \
                            'WorkPackages')
else:
    raise NameError('Cant find work packages')
if Debug:
    print("    Directory containing work package definitions: \n", \
          "            ----> ", wpDirectory)
REPORTPATH = os.path.join(HOMEPATH, \
                           'Reports')
if Debug:
    print("    Directory in which reports will be placed: \n", \
          "            ----> ", REPORTPATH)

    
##! --------  Create costing control instance:

import Control as cntrl
iCntrl  = cntrl.Control(ControlFile)
if Debug:
    print("    Dump of control parameters: \n", iCntrl)

    
##! --------  LhARA imports:
import LhARACostingTool as LCT
import Staff            as Stf
import WorkPackage      as wp


##! --------  Create staff database instance:
nStf = Stf.Staff.parseStaffDatabase(StaffDatabaseFile)
if Debug:
    print("    Staff data base read; ", nStf, " instances of Staff created.")
nDel = Stf.Staff.cleanStaffDatabase()
if Debug:
    print("    Staff data base cleaned; ", nDel, " instances of Staff deleted.")
    print("        ----> ", Stf.Staff.getNumberOfStaff(), "staff remain.")

    
##! --------  Create work package instances:
wpList    = sorted(os.listdir(wpDirectory))
if Debug:
    print("    Read work package definitions from: \n", \
          "              ---->", wpList)
wpInst = []
for wpFile in wpList:
    if wpFile.find('.csv') <= 0:
        if Debug:
            print("Bad file name", wpFile, " skipping this file.")
    else:
        FileName = os.path.join(wpDirectory, wpFile)
        if Debug:
            print("              ----> Reading data from: ", FileName)
        wpInst.append(wp.WorkPackage(FileName))
if Debug:
    print("              ---->", len(wpInst), " work packages intialised:")
    for Inst in wpInst:
        print("                       ", Inst._Name)
    

##! --------  Create LhARA costing tool instance:
iLCT = LCT.LhARACostingTool(Debug)
if Debug:
    print(iLCT)

iLCT.Execute()

    
##! Complete:
if Debug:
    print()
    print(" LhARA costing tool, execution ends.")

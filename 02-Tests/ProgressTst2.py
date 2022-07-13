#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Second test script for "Progress" class
================================

  Assumes python path includes LhARA code.

  Provides tests for:
    - Class Progress
    - Derived classes:
        - PlannedValue

  Script starts by testing built in methods.

"""

import os
import sys
import datetime as DT


##! Start:
print("========  Progress: tests start  ========")

Debug = False
for arg in sys.argv:
    if arg == "Debug=true":
        Debug = True

DateToday = DT.datetime.now()
print('    ----> Date instance:', DateToday)


##! --------  Identify necessary files:

LhARAPATH    = os.getenv('LhARAPATH')
HOMEPATH     = os.getenv('HOMEPATH')
ControlFile  = os.path.join(HOMEPATH, \
                            '10-Control/LhARA-costing-tool-control.csv')
if Debug:
    print("    Control file: \n", \
          "            ----> ", ControlFile)
StaffDatabaseFile = os.path.join(HOMEPATH, \
                                 '12-Staff/StaffDatabase.csv')
if Debug:
    print("    Staff database file: \n", \
          "            ----> ", StaffDatabaseFile)
wpDirectory = os.path.join(HOMEPATH, \
                           '11-WorkPackages')
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


##! --------  Get the rest of the packages

import Staff            as Stf
import WorkPackage      as wp
import Task             as Tsk
import Progress         as Prg
import LhARACostingTool as LCT
import Report           as Rprt


##! Load costing data structure:
ProgressTest = 1
print()
print("Progress:", ProgressTest, " Load costing data structure.")

#.. Load costing data structure:
nStf = Stf.Staff.parseStaffDatabase(StaffDatabaseFile)
if Debug:
    print("     ----> Staff data base read; ", nStf, \
          " instances of Staff created.")
nDel = Stf.Staff.cleanStaffDatabase()
if Debug:
    print("           Staff data base cleaned; ", nDel, \
          " instances of Staff deleted.")
    print("          ", Stf.Staff.getNumberOfStaff(), "staff remain.")
wpList    = sorted(os.listdir(wpDirectory))
if Debug:
    print("     ----> Read work package definitions from: \n", \
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


#.. Create costing tool instance:
iLCT  = LCT.LhARACostingTool(Debug)
print('    ----> Costing tool instance created.')

print('  <---- Prerequisits created.')

#.. Load costing data structure:
print("     ----> Complete costing data structure:")
print("       ----> Execute costing tool:")
iLCT.Execute()
print('       <---- Costing tool executed.')
print("     <---- Costing data structure complete.")


##! Load progress data:
ProgressTest += 1
print()
print("Progress:", ProgressTest, " Load costing data structure.")

PrgDirectory = os.path.join(HOMEPATH, \
                           '13-ProgressReports')
if Debug:
    print("    Directory containing progress reports: \n", \
          "        ----> ", PrgDirectory)
PrgList    = sorted(os.listdir(PrgDirectory))
for PrgFile in PrgList:
    if PrgFile.find('.csv') <= 0:
        if Debug:
            print("Bad file name", PrgFile, " skipping this file.")
    else:
        FileName = os.path.join(PrgDirectory, PrgFile)
        if Debug:
            print("        ----> Reading data from: ", FileName)
        Prg.Progress.loadProgress(FileName)
print("     ----> Print progress records:")
if Debug:
    print("          ----> progress reports loaded:")
    for iPrg in Prg.Progress.instances:
        print(iPrg)
print("    <---- Progress data loaded.")

##! Earned value:
ProgressTest += 1
print()
print("Progress test:", ProgressTest, " Earned value test.")

#.. For each progress report, calculate earned value:
for iPrg in Prg.Progress.instances:
    if Debug:
        print("    ----> Get earned value for:", iPrg._Task._Name)
    EV1 = Prg.EarnedValue(iPrg._Task, iPrg._Date, iPrg)
    if Debug:
        print("      ----> Earned value:", EV1._EarnedValue)
print("    <---- Earned value loaded.")


##! Check reports:
ProgressTest += 1
print()
print("Progress test:", ProgressTest, \
      " check reports.")

for iTsk in Tsk.Task.instances:
    if iTsk._Name == "Project office support":
        Tsk1 = iTsk
        break
filepath  = os.path.join(LhARAPATH, '99-Scratch')
PrgRpt1 = Rprt.Progress(filepath, "TestProgressReport.csv", Tsk1)

print("    ----> Progress report instance created.")
if Debug:
    print(PrgRpt1)

DataFrame = PrgRpt1.createPandasDataFrame()
PrgRpt1.createCSV(DataFrame)
Prg.Progress.Plot(DataFrame, filepath, "Progress-portrait.pdf", False)
Prg.Progress.Plot(DataFrame, filepath, "Progress-landscape.pdf", True)

print("    <---- Progress report test done.")
print()



##! Complete:
print()
print("========  Progress: tests complete  ========")


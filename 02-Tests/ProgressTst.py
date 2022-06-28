#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Progress" class
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

import Staff            as Stf
import WorkPackage      as wp
import Task             as Tsk
import Progress         as Prg
import LhARACostingTool as LCT
import Report           as Rprt

##! Start:
print("========  Progress: tests start  ========")

Debug = False
for arg in sys.argv:
    if arg == "Debug=true":
        Debug = True

#.. Create dummy task:
print("  Create dummy work package and task instances:")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '11-WorkPackages/WP1.csv')
WP1 = wp.WorkPackage(filename)
Tsk1 = Tsk.Task("LhARA", WP1)
print('    ----> instances WP1 and Tsk1 created.')

#.. Create date:
DateToday = DT.datetime.now()
print('    ----> Date instance:', DateToday)

#.. Create costing tool instance:
iLCT  = LCT.LhARACostingTool(Debug)
print('    ----> Costing tool instance created.')

print('  <---- Prerequisits created.')


##! --------  Identify necessary files:
HOMEPATH     = os.getenv('HOMEPATH')
ControlFile  = os.path.join(HOMEPATH, \
                            'Control/LhARA-costing-tool-control.csv')
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
  

"""

   Progress Tests

"""
##! --------  Progess tests:
#.. Check built-in methods:
ProgressTest = 1
print()
print("Progress: check built-in methods.")

#.. __init__
print("  __init__:")
print("    ----> Attempt to create instance with correct call:")
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, 24.0, 0.15, 23.0)
except:
    print('      !!!!> Failed to create instance.')
    raise Exception
print('    <---- instance Prg1 created.')
#.. __repr__
print("  __repr__:")
print("    ---->", repr(Prg1))
print("    <---- __repr__ done.")
#.. __str__
print("  __str__:")
print(str(Prg1))
print("    <---- __str__ done.")
print("    ----> Check wrong-argument traps:")
Dummy = "String"
try:
    Prg1 = Prg.Progress(Dummy, DateToday, 0.15, 24, 0.15, 23.0)
except:
    print('      ----> Correctly trapped Task instance.')
else:
    print('      !!!!> Failed to trap _Task not instance of Task.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, Dummy, 0.15, 24., 0.15, 23.0)
except:
    print('      ----> Correctly trapped Date instance.')
else:
    print('      !!!!> Failed to trap _Date not instance of datetime.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, Dummy, 24., 0.15, 23.0)
except:
    print('      ----> Correctly trapped PlannedCompletionFraction error.')
else:
    print('      !!!!> Failed to trap PlannedFractionComplete not float.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, Dummy, 0.15, 23.0)
except:
    print('      ----> Correctly trapped PlannedValue error.')
else:
    print('      !!!!> Failed to trap PlannedValue not float.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, 24., Dummy, 23.0)
except:
    print('      ----> Correctly trapped CompletionFraction error.')
else:
    print('      !!!!> Failed to trap FractionComplete not float.')
    raise Exception
try:
    Prg1 = Prg.Progress(Tsk1, DateToday, 0.15, 24., 0.15, Dummy)
except:
    print('      ----> Correctly trapped Spend error.')
else:
    print('      !!!!> Failed to trap Spend not float.')
    raise Exception
print('    <---- Wrong argument tests done.')

del Prg1
Prg.Progress.instances = []

"""

   EarnedValue Tests

"""
##! EarnedValue tests:
#.. Check built-in methods:
ProgressTest += 1
print()
print("Progress:", ProgressTest, \
      " EarnedValue: check built-in methods.")

#.. __init__
print("  __init__:")
print("    ----> Attempt to create instance with correct call:")
try:
    EV1 = Prg.EarnedValue(Tsk1, DateToday)
except:
    print('      !!!!> Failed to create instance.')
    raise Exception
print('    <---- instance EV1 created.')
#.. __repr__
print("  __repr__:")
print("    ---->", repr(EV1))
print("    <---- __repr__ done.")
#.. __str__
print("  __str__:")
print(str(EV1))
print("    <---- __str__ done.")
print("    ----> Check wrong-argument traps:")
Dummy = None
try:
    EV1 = Prg.EarnedValue(Dummy, DateToday)
except:
    print('      ----> Correctly trapped Task instance.')
else:
    print('      !!!!> Failed to trap _Task not instance of Task.')
    raise Exception
try:
    EV1 = Prg.EarnedValue(Tsk1, Dummy)
except:
    print('      ----> Correctly trapped Date instance.')
else:
    print('      !!!!> Failed to trap _Date not instance of datetime.')
    raise Exception
print('    <---- Wrong argument tests done.')

##! Tidy up:
ProgressTest += 1
print()
print("Progress:", ProgressTest, \
      " Clear data structures.")

print("  Clear present set of instances:")
print("    ----> Clear data structure:")
iLCT.ClearDataStructure()
del EV1
Prg.EarnedValue.instances = []
print('    <---- Costing data structure cleared.')


##! Load costing data structure:
ProgressTest += 1
print()
print("Progress:", ProgressTest, " Load costing data structure.")

#.. Load costing data structure:
print("    ----> Load costing data structure:")
import Control as cntrl
iCntrl  = cntrl.Control(ControlFile)
if Debug:
    print("      ----> Dump of control parameters: \n", iCntrl)
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

try:
    filepath  = os.path.join(LhARAPATH, '99-Scratch')
    PrgRpt1 = Rprt.Progress(filepath, "TestProgressReport.csv", None)
except:
    print("     ----> Successfully trapped bad report request!")

for iTsk in Tsk.Task.instances:
    if iTsk._Name == "Project office support":
        Tsk1 = iTsk
        break
PrgRpt1 = Rprt.Progress(filepath, "TestProgressReport.csv", Tsk1)
print("    ----> Progress report instance created.")
if Debug:
    print(PrgRpt1)
DataFrame = PrgRpt1.createPandasDataFrame()
PrgRpt1.createCSV(DataFrame)
Prg.Progress.Plot(DataFrame)

print("    <---- Progress report test done.")
print()



##! Complete:
print()
print("========  Progress: tests complete  ========")


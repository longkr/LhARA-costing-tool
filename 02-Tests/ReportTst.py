#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Reports" class
===============================

  Assumes python path includes LhARA code.

  Script tests the methods written to create reports from the LhARA costing
  data structure.

"""

import os
import numpy as np

import Control     as Cntrl
import Staff       as Stf
import WorkPackage as wp
import Project     as Prj
import Report      as Rprt

##! Start:
print("========  Report tests: initialise controls  ========")
iCntrl = Cntrl.Control()
print(iCntrl)
print("========                Initialisation complete  ========")

##! Start:
print(" ")
print("========  Reports: tests start  ========")

##! Check built-in methods:
ReportsTest = 1
print()
print("ReportsTest:", ReportsTest, " check built in base-class methods.")
#.. __init__
print("    Report.__init__:")
try:
    Rprt1 = Rprt.Report()
except:
    print('      ----> Successfully trapped no input exception`.')
try:
    Rprt1 = Rprt.Report("OnlyOneArgument")
except:
    print('      ----> Successfully trapped "only one argument exception".')
LhARAPATH = os.getenv('LhARAPATH')
try:
    Rprt1 = Rprt.Report("Test report", "BadPath", "TestReport.csv")
except:
    print('      ----> Successfully trapped "bad path exception".')
NoWritePath = os.path.join(LhARAPATH, '98-NoWriteAccess')
try:    
    Rprt1 = Rprt.Report("Test report", NoWritePath, "TestReport.csv")
except:
    print('      ----> Successfully trapped "no write access exception".')
try:    
    Rprt1 = Rprt.Report("Test report", LhARAPATH, "TestReport.csv")
except:
    print('      ----> Failed to create Report instance.')
    raise Exception
print('      ----> instance Rprt1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Rprt1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Rprt1))
print("    <---- __str__ done.")


##! Check reports:
ReportsTest = 2
print()
print()
print("ReportsTest:", ReportsTest, \
      " check Staff list derived class methods.")
LhARAPATH = os.getenv('LhARAPATH')
filename  = os.path.join(LhARAPATH, '12-Staff/StaffDatabase.csv')
Stf.Staff.parseStaffDatabase(filename)
try:
    filepath  = os.path.join(LhARAPATH, '99-Scratch')
    StfRpt = Rprt.StaffList(filepath, "TestStaffReport.csv")
except:
    print("     ----> Failed to create Staff list report instance!",
          "  Execution terminated.")
    raise Exception
print("    ----> Staff list report instance created.")
print(StfRpt)
print("    <---- Staff list report test done.")
print()
print("ReportsTest:", ReportsTest, \
      " check work package list derived class methods.")
LhARAPATH = os.getenv('LhARAPATH')
wpPath    = os.path.join(LhARAPATH, '11-WorkPackages')
wpList    = sorted(os.listdir(wpPath))
print("    ----> list of WP definition files:", wpList)
wpInst = []
for wpFile in wpList:
    if wpFile.find('.csv') <= 0:
        print("        ----> Bad file name", wpFile, ". Skip")
    else:
        FileName = os.path.join(wpPath, wpFile)
        print("    ----> Reading data from: ", FileName)
        wpInst.append(wp.WorkPackage(FileName))
try:
    filepath  = os.path.join(LhARAPATH, '99-Scratch')
    wpRpt = Rprt.WorkPackageList(filepath, "TestWorkPackageReport.csv")
except:
    print("     ----> Failed to work package list report instance!",
          "  Execution terminated.")
    raise Exception
print("    ----> Work package list report instance created.")
print("          Should contain: ", len(wpInst), " work packages.")
print(wpRpt)
print("    <---- Work package list report test done.")
filepath  = os.path.join(LhARAPATH, '99-Scratch')
for iWP in wp.WorkPackage.instances:
    wpSumRpt = Rprt.WorkPackageSummary(filepath, \
                                       iWP._Name + ".csv", \
                                       iWP)
    print("    ----> Work package summary report instances created.")
    print(wpSumRpt)
print("    <---- Work package list report test done.")


##! Test report creation:
ReportsTest = 3
print()
print("ReportsTest:", ReportsTest, " check creation of full staff list.")
StfRpt.asCSV()
print("    <---- CSV staff report generated.")
print()
print("ReportsTest:", ReportsTest, \
      " check creation of workpackage list report.")
wpRpt.asCSV()
print("    <---- CSV work package report generated.")
print()
print("ReportsTest:", ReportsTest, \
      " check creation of workpackage summary report.")
DataFrame = wpSumRpt.createPandasDataFrame()
wpSumRpt.createCSV(DataFrame)
print(DataFrame)
print("    <---- CSV work package summary report generated.")
print()
print("ReportsTest:", ReportsTest, \
      " check creation of staff effort summary report.")
print(Prj.Project.instances)
iPrj = Prj.Project.instances[0]
ByYr = np.array([1, 2, 3, 4, 5])
Yrs  = ['2022/23', '2023/24', '2024/25', '2025/26', '2026/27']
iPrj.setStaffCostByYear(ByYr)
iPrj.setFinancialYears(Yrs)
print(iPrj)
iStfSmRpt = Rprt.StaffEffortSummary(filepath, "StaffEffortSummary.csv", iPrj)
print(iStfSmRpt)
#DataFrame = wpSumRpt.createPandasDataFrame()
#wpSumRpt.createCSV(DataFrame)
#print(DataFrame)
print("    <---- CSV work package summary report generated.")

print("ReportsTest:", ReportsTest, " check Overview derived class methods.")
try:
    Ovrvw1 = Rprt.Overview(LhARAPATH, "TestReport.csv", iPrj)
except:
    print("     ----> Failed to create Overview report instance!",
          "  Execution terminated.")
    raise Exception
print("    ----> Overview report instance created.")
print(Ovrvw1)
print("    <---- Overview report test done.")

##! Complete:
print()
print("========  Reports: tests complete  ========")




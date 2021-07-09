#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate full LhARA costing data structure
====================================================

  Assumes python path includes LhARA code.


"""

import os

import Staff         as Stf
import Equipment     as Eqp
import Project       as Prj
import WorkPackage   as wp
import Task          as Tsk
import TaskStaff     as TskStf
import TaskEquipment as TskEqp
import Report        as Rpt

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
print("Complete LhARA costing data structure: section: ", CDSsection, " read work packages.")
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
    print("           ", Inst._Name)
print("    <---- Done.")

print()
print("        ---->  Project definition files Read <----")


##! TaskStaff
CDSsection = 3
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " cost staff in task staff.")
nDel = TskStf.TaskStaff.clean()
print("    ----> Cleaning: removed ", nDel, "instances.")
print("    ----> Run doCosting:")
TskStf.TaskStaff.doCosting()


##! Task
CDSsection = 4
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " cost tasks.")
nDel = Tsk.Task.clean()
print("    ----> Cleaning: removed ", nDel, "instances.")
print("    ----> Run doCosting:")
Tsk.Task.doCosting()

    
##! Workpage
CDSsection = 5
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " cost work packages.")
nDel = wp.WorkPackage.clean()
print("    ----> Cleaning: removed ", nDel, "instances.")
print("    ----> Run doCosting:")
wp.WorkPackage.doCosting()


##! Project
CDSsection = 6
print()
print("Complete LhARA costing data structure: section: ", CDSsection, " cost project.")
nDel = Prj.Project.clean()
print("    ----> Cleaning: removed ", nDel, "instances.")
print("    ----> Run doCosting:")
Prj.Project.doCosting()


CDSsection = 7
print()
print("Complete LhARA costing data structure: section: ", CDSsection, \
      " costing done. \n     ----> print Project(s):")
for iPrj in Prj.Project.instances:
    print(iPrj)
    print("    Total projec cost: ", iPrj.getTotalProjectCost())


CDSsection = 8
print()
print("Complete LhARA costing data structure: section: ", CDSsection, \
      ".  Now generate reports.")
try:
    filepath  = os.path.join(LhARAPATH, '99-Scratch')
    wpRpt = Rpt.WorkPackageList(filepath, "TestWorkPackageReport.csv")
except:
    print("     ----> Failed to work package list report instance!",
          "  Execution terminated.")
    raise Exception
print("    ----> Work package list report instance created.")
print("          Should contain: ", len(wpInst), " work packages.")
wpRpt.asCSV()
print("    <---- CSV work package report generated.")
for iWP in wp.WorkPackage.instances:
    if iWP._Name == "LaserSpectrometer":
        iWP_LasSpct = iWP
try:
    filepath  = os.path.join(LhARAPATH, '99-Scratch')
    wpSumRpt = Rpt.WorkPackageSummary(filepath, \
                                      "TestWorkPackageSummary.csv", \
                                      iWP_LasSpct)
except:
    print("     ----> Failed to work package list report instance!",
          "  Execution terminated.")
    raise Exception
print("    ----> Work package summary report instance created.")
print(wpSumRpt)
DataFrame = wpSumRpt.createPandasDataFrame()
wpSumRpt.createCSV(DataFrame)
print("    <---- Work package summary report done.")



##! Complete:
print()
print("========  Full LhARA costing data structure created  ========")

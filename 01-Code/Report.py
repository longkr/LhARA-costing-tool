#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Report:
=============

  Collection of derived classes to generate reports, usually in the
  form of a CSV file, based on the Project, WorkPackage, and Task classes

  Class attributes:
  -----------------
  __Debug  : Boolean: set for debug print out
  instances: List of instances of Project class


  Instance attributes:
  --------------------
    _Name      : (str) name of report
    _ReportPath: Path to directory into which report file will be written
    _FileName  : Report filename
    _Header    : List of header fields; initialised to [].  
                 Filled in derived classes.
    _Lines     : Lines of report; initialised to [].
                 Filled in derived classes.

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  Processing methods:
      createPandasDataFrame:  Creates pandas data frame from _Header and _Lines.


  I/o methods:
      createCSV: Creates the report's CSV file.


  Exceptions:
        NoReportNameProvided: Report instance call with invalid name

        NoOutputPathProvided: Path to directory for report is not provided

          NoFilenameProvided: No file name provided for report

           OutputPathInvalid: Path to directory for report invalid

   NoWriteAccessToOutputPath: Can not write into report directory

  WorkPackageInstanceInvalid: Instance of w/p for which report requested is 
                              invalid


Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 02Jul21: First implementation


@author: kennethlong
"""

import os
import copy
from datetime import date
import pandas as pnds
import numpy  as np

import Task          as Tsk
import TaskStaff     as TskStf
import TaskEquipment as TskEqp
import WorkPackage   as wp
import Staff         as Stf

"""
         -------->  Base "Report" class  <--------
"""
class Report:
    __Debug   = False
    instances = []

    
#--------  "Built-in methods":
    def __init__(self, _Name=None, _ReportPath=None, _FileName=None):

        self._Name       = _Name
        self._ReportPath = _ReportPath
        self._FileName   = _FileName
        self._Header     = []
        self._Lines      = []

        if _Name == None:
            raise NoReportNameProvided( \
                  'No report name provided; execution termimated.')
        
        if _ReportPath == None:
            raise NoOutputPathProvided( \
                  'No output path provided; execution termimated.')
        
        if _FileName   == None:
            raise NoFilenameProvided( \
                  'No CSV filename provided; execution termimated.')

        if not os.path.isdir(_ReportPath):
            raise OutputPathInvalid('Output path:', _ReportPath, ' invalid')

        if not os.access(_ReportPath, os.W_OK):
            raise NoWriteAccessToOutputPath( \
                     'No write access to output path:', _ReportPath)
            
        Report.instances.append(self)

    def __repr__(self):
        return "Report(ReportName, PathToDirectory, ReportFile)"

    def __str__(self):
        print(" Report: Name: ", self._Name)
        print("     Output directory path: ", self._ReportPath)
        print("     Report file name: ", self._FileName)
        return "     <---- Report __str__ done."
    

#--------  Processing methods
    def createPandasDataFrame(self):
        Data = []
        Data.append(self._Header)
        for i in range(len(self._Lines)):
            Data.append(self._Lines[i])
        Dataframe = pnds.DataFrame(Data)
        if self.__Debug:
            print(" Report; createPandasDataframe: \n", Dataframe)
        return Dataframe

    
#--------  I/o methods
    def createCSV(self, _DataFrame):
        _filename = os.path.join(self._ReportPath, self._FileName)
        _DataFrame.to_csv(_filename)


"""
Class Overview:   -------->  "Overview" report; derived class  <--------
===============

  Overview derived class creates and formats the Overview report.

"""
class Overview(Report):
    def __init__(self, _ReportPath, _FileName):

        Report.__init__(self, "Overview report", _ReportPath, _FileName)

        self._Overview = []

"""
Class StaffList:   -------->  "Staff" report; derived class  <--------
================

  Staff derived class creates and formats the Overview report.

"""
class StaffList(Report):
    def __init__(self, _ReportPath, _FileName):

        Report.__init__(self, "Staff report: full staff list", _ReportPath, _FileName)

        self._Header = Stf.Staff.getHeader()
        self._Lines = []
        for iStf in Stf.Staff.instances:
            self._Lines.append(iStf.getData())

    def __str__(self):
        print(" Report: Name: ", self._Name)
        print("     Output directory path: ", self._ReportPath)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
        return "     <---- Report __str__ done."

    
#--------  Report:
    def asCSV(self):
        dataframe = Stf.Staff.createPandasDataframe()
        filename = os.path.join(self._ReportPath, self._FileName)
        Stf.Staff.createCSV(dataframe, filename)
        

"""
Class WorkPackageList:  ---->  "WorkPackageList" report; derived class  <----
======================

  WorkPackageList derived class creates and formats the workpackage report.

"""
class WorkPackageList(Report):
    def __init__(self, _ReportPath, _FileName):

        Report.__init__(self, "Work package report: summary of all workpackages", _ReportPath, _FileName)

        self._Header = wp.WorkPackage.getHeader()
        self._Lines = []
        for iWP in wp.WorkPackage.instances:
            self._Lines.append(iWP.getData())

    def __str__(self):
        print(" Report: Name: ", self._Name)
        print("     Output directory path: ", self._ReportPath)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
        return "     <---- Report __str__ done."

    
#--------  Report:
    def asCSV(self):
        dataframe = wp.WorkPackage.createPandasDataframe()
        filename = os.path.join(self._ReportPath, self._FileName)
        wp.WorkPackage.createCSV(dataframe, filename)
        

"""
Class WorkPackageSummary:  ---->  "WorkPackageSummary" report  <----
=========================

  WorkPackageSummary derived class creates and formats the summary
  workpackage report.

"""
class WorkPackageSummary(Report):
    def __init__(self, _ReportPath, _FileName, _wpInst=None):

        if not isinstance(_wpInst, wp.WorkPackage):
            raise WorkPackageInstanceInvalid( \
                          "Invalid instance of work package requested")
        
        Report.__init__(self, "Work package summary", _ReportPath, _FileName)

        self._Header = []
        self._Header.append(_wpInst._Project._Name)
        for i in range(len(_wpInst._FinancialYears)):
            for j in range(2):
                self._Header.append(None)
        self._Header.append("Report date:")
        RptDt = date.today()
        self._Header.append(RptDt.strftime("%d-%b-%Y"))
                       
        self._Lines = []
        Line        = []
        Line.append(_wpInst._Name)
        for i in range(len(_wpInst._FinancialYears)+1):
            for j in range(2):
                Line.append(None)
        self._Lines.append(copy.deepcopy(Line))
        Line[0]  = None
        NullLine = Line
        self._Lines.append(Line)

        Line = self.YearHeader(_wpInst)
        self._Lines.append(Line)

        Line = self.StaffHeader(_wpInst)
        self._Lines.append(Line)

        for iTsk in Tsk.Task.instances:
            if iTsk._WorkPackage == _wpInst:
                Lines = self.TaskStaffLines(_wpInst, iTsk)
                for Line in Lines:
                    self._Lines.append(Line)

        Line = self.RiskMitigationStaff(_wpInst)
        self._Lines.append(Line)
        
        Line = self.StaffTotal(_wpInst)
        self._Lines.append(Line)
        
        Line = self.EquipmentHeader(_wpInst)
        self._Lines.append(Line)
        
        for iTsk in Tsk.Task.instances:
            if iTsk._WorkPackage == _wpInst:
                Lines = self.TaskEquipmentLines(_wpInst, iTsk)
                for Line in Lines:
                    self._Lines.append(Line)

        Line = self.Inflation(_wpInst)
        self._Lines.append(Line)
        
        Line = self.RiskMitigationEquip(_wpInst)
        self._Lines.append(Line)
        
        Line = self.WorkingMargin(_wpInst)
        self._Lines.append(Line)
        
        Line = self.Contingency(_wpInst)
        self._Lines.append(Line)
        
        Line = self.EquipmentTotal(_wpInst)
        self._Lines.append(Line)
        
        Line = self.Consumables(_wpInst)
        self._Lines.append(Line)
        
        Line = self.Travel(_wpInst)
        self._Lines.append(Line)
        
        Line = NullLine
        self._Lines.append(Line)

        Line = self.Total(_wpInst)
        self._Lines.append(Line)
                
        
    def Total(self, _wpInst):
        Line = []
        Line.append("Total:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._StaffCostByYear, np.ndarray) and \
               isinstance(_wpInst._EquipmentCostByYear, np.ndarray):
                Line.append(_wpInst._StaffCostByYear[iYr] + \
                            _wpInst._EquipmentCostByYear[iYr])
            else:
                Line.append(None)
        Line.append(None)
        if isinstance(_wpInst._TotalStaffCost, float) and \
           isinstance(_wpInst._TotalEquipmentCost,float):
            Line.append(_wpInst._TotalStaffCost + \
                        _wpInst._TotalEquipmentCost)
        else:
            Line.append(None)
        return Line

    def WorkingMargin(self, _wpInst):
        Line = []
        Line.append("Working margin (not yet implemented):")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(0.)
        Line.append(None)
        Line.append(0.)
        return Line

    def Contingency(self, _wpInst):
        Line = []
        Line.append("Contingency (not yet implemented):")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(0.)
        Line.append(None)
        Line.append(0.)
        return Line

    def RiskMitigationStaff(self, _wpInst):
        Line = []
        Line.append("Cost of risk mitigation, staff (not yet implemented):")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(0.)
        Line.append(None)
        Line.append(0.)
        return Line

    def RiskMitigationEquip(self, _wpInst):
        Line = []
        Line.append("Cost of risk mitigation, equipment (not yet implemented):")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(0.)
        Line.append(None)
        Line.append(0.)
        return Line

    def Inflation(self, _wpInst):
        Line = []
        Line.append("Inflation (not yet implemented):")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(0.)
        Line.append(None)
        Line.append(0.)
        return Line

    def EquipmentTotal(self, _wpInst):
        Line = []
        Line.append("Equipment total:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._EquipmentCostByYear, np.ndarray):
                Line.append(_wpInst._EquipmentCostByYear[iYr])
            else:
                Line.append(None)
        Line.append(None)
        Line.append(_wpInst._TotalEquipmentCost)
        return Line

    def Consumables(self, _wpInst):
        Line = []
        Line.append("Consumables")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(_wpInst._ConsumeByYear[iYr])
        Line.append(None)
        Line.append(_wpInst._TotalConsume)
        return Line

    def Travel(self, _wpInst):
        Line = []
        Line.append("Travel")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(_wpInst._TravelByYear[iYr])
        Line.append(None)
        Line.append(_wpInst._TotalTravel)
        return Line

    def TaskEquipmentLines(self, _wpInst, _Tsk):
        Lines = []
        Line  = []
    #.. Header:
        Line.append(_Tsk._Name)
        for iYr in range(len(_wpInst._FinancialYears)+1):
            for i in range(2):
                Line.append(None)
        Lines.append(copy.deepcopy(Line))
        print(Line)
    #.. Equipment:
        InstEqp = ""
        Line = []
        InstEqp = None
        for iTskEqp in TskEqp.TaskEquipment.instances:
            Line = []
            if iTskEqp._Task == _Tsk:
                iEqp = iTskEqp._Equipment
                Line.append(iEqp._Name)
                for iYr in range(len(_wpInst._FinancialYears)):
                    Line.append(None)
                    Line.append(iEqp._EquipmentCostByYear[iYr])
                Line.append(None)
                Line.append(iEqp._TotalEquipmentCost)
                Lines.append(copy.deepcopy(Line))
                print(Line)
        return Lines
        
    def EquipmentHeader(self, _wpInst):
        Line = []
        Line.append("Non-staff")
        for iYr in range(len(_wpInst._FinancialYears)+1):
            Line.append(None)
            Line.append("£k")
        return Line
        
    def StaffTotal(self, _wpInst):
        Line = []
        Line.append("Staff total:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._StaffCostByYear, np.ndarray):
                Line.append(_wpInst._StaffCostByYear[iYr])
            else:
                Line.append(None)
        Line.append(None)
        Line.append(_wpInst._TotalStaffCost)
        return Line

    def StaffHeader(self, _wpInst):
        Line = []
        Line.append("Staff")
        for iYr in range(len(_wpInst._FinancialYears)+1):
            Line.append("Fraction")
            Line.append("£k")
        return Line
        
    def TaskStaffLines(self, _wpInst, _Tsk):
        Lines = []
        Line  = []
    #.. Header:
        Line.append(_Tsk._Name)
        for iYr in range(len(_wpInst._FinancialYears)+1):
            for i in range(2):
                Line.append(None)
        Lines.append(copy.deepcopy(Line))
    #.. Staff:
        InstCd = ""
        Line = []
        InstCd = None
        for iTskStf in TskStf.TaskStaff.instances:
            Line = []
            if iTskStf._Task == _Tsk:
                print(iTskStf)
                iStf = iTskStf._Staff
                if InstCd != iStf._InstituteCode:
                    InstCd = iStf._InstituteCode
                    Line.append(iStf._InstituteCode)
                    for iYr in range(len(_wpInst._FinancialYears)+1):
                        for i in range(2):
                            Line.append(None)
                    Lines.append(copy.deepcopy(Line))
                    Line = []
                Line.append(iStf._StaffCode)
                for iYr in range(len(_wpInst._FinancialYears)):
                    Line.append(round(iTskStf._StaffFracByYear[iYr], 2))
                    if isinstance(iTskStf._StaffCostByYear, np.ndarray):
                        Line.append(round(iTskStf._StaffCostByYear[iYr], 2))
                    else:
                        Line.append(None)
                Line.append(round(iTskStf._TotalStaffFrac, 2))
                if iTskStf._TotalStaffCost != None:
                    Line.append(round(iTskStf._TotalStaffCost, 2))
                else:
                    Line.append(None)
                Lines.append(copy.deepcopy(Line))
        return Lines
        
    def YearHeader(self, _wpInst):
        Line = []
        Line.append(None)
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(_wpInst._FinancialYears[iYr])
            Line.append(None)
        Line.append("Total")
        Line.append(None)
        return Line
        

    def __str__(self):
        print(" Report: Name: ", self._Name)
        print("     Output directory path: ", self._ReportPath)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
        return "     <---- Report __str__ done."

    
#--------  Report:
    def asCSV(self):
        dataframe = wp.WorkPackage.createPandasDataframe()
        filename = os.path.join(self._ReportPath, self._FileName)
        wp.WorkPackage.createCSV(dataframe, filename)
        

#--------  Exceptions:
class NoReportNameProvided:
    pass

class NoOutputPathProvided:
    pass

class NoFilenameProvided:
    pass

class OutputPathInvalid:
    pass

class NoWriteAccessToOutputPath:
    pass

class WorkPackageInstanceInvalid:
    pass

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

import Control       as Cntrl

import Task          as Tsk
import TaskStaff     as TskStf
import TaskEquipment as TskEqp
import WorkPackage   as wp
import Project       as Prj
import Staff         as Stf
import OtherNonStaff as ONS

iCntrl = Cntrl.Control()

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
        if self.__Debug:
            print("     Output directory path: ", self._ReportPath)
        else:
            dirname,  basename   = os.path.split(self._ReportPath)
            print("     Output directory path: ", basename)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
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

    
#--------  Report:
    def asCSV(self):

        Data = []
        Data.append(self._Header)
        for i in range(len(self._Lines)):
            Data.append(self._Lines[i])
        if self.__Debug:
            print(Data)
        
        DataFrame = pnds.DataFrame(Data)
        if self.__Debug:
            print(DataFrame)
            
        filename = os.path.join(self._ReportPath, self._FileName)
        if self.__Debug:
            print(filename)

        DataFrame.to_csv(filename)
        
    
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
    __Debug   = False

    def __init__(self, _ReportPath, _FileName, _PrjInst):

        """
           --------> Get started:
        """
        if not isinstance(_PrjInst, Prj.Project):
            raise ProjectInstanceInvalid( \
                          "Project instance requested invalid")
        
        Report.__init__(self, "Overview report", _ReportPath, _FileName)

        self._Header = []
        self._Header.append(_PrjInst._Name)
        self._Header.append(None)
        for i in range(len(_PrjInst._FinancialYears)):
            for j in range(2):
                self._Header.append(None)
        self._Header.append("Report date:")
        RptDt = date.today()
        self._Header.append(RptDt.strftime("%d-%b-%Y"))

        self._Lines = []
        Line        = []
        Lines       = []

        Line.append(None)
        NullLine = Line
        self._Lines.append(Line)

        Lines = self.YearHeader(_PrjInst)
        for iLn in range(len(Lines)):
            Line = Lines[iLn]
            self._Lines.append(Line)

        Line  = []
        Lines = []

        """
           --------> Work through staff cost overview:
        """
        Line.append("Staff effort, summary by institute")
        self._Lines.append(Line)
        Line = []

        nWP = 0
        FrcTot = np.array([])
        CstTot = np.array([])

        for iYr in range(len(_PrjInst._FinancialYears)):
            FrcTot = np.append(FrcTot, 0.)
            CstTot = np.append(CstTot, 0.)

        """
           Loop over work packages:
        """
        if Overview.__Debug:
            print(" Overview(Report): Loop over w/ps to sum staff cost", \
                  " by year")
        for iWP in wp.WorkPackage.instances:
            nWP += 1
            Line.append(nWP)
            Line.append(iWP._Name)
            self._Lines.append(Line)
            Line = []
            if Overview.__Debug:
                print("     ----> Work package: ", iWP.getName())
                
            """
               Loop over institutes contributing staff:
            """
            for InstCode in Stf.Staff.institutes:
                Frc = np.array([])
                Cst = np.array([])
                for iYr in range(len(_PrjInst._FinancialYears)):
                    Frc = np.append(Frc, 0.)
                    Cst = np.append(Cst, 0.)

                """
                   Loop over task staff instances:
                """
                for iTskStf in TskStf.TaskStaff.instances:
                    if iTskStf._Task._WorkPackage == iWP and \
                       iTskStf._Staff._InstituteCode == InstCode:
                        if Overview.__Debug:
                            print("           ----> Institute: Staff code", \
                                  InstCode, iTskStf._Staff.getStaffCode())
                            print("                 Fraction by year:", \
                                  iTskStf._StaffFracByYear)
                            print("                 Cost by year    :", \
                                  iTskStf._StaffCostByYear)
                        Frc    += iTskStf._StaffFracByYear
                        if iTskStf._StaffCostByYear != None:
                            Cst    += iTskStf._StaffCostByYear

                if Overview.__Debug and Frc.size != 0:
                    print("                 WP/institute totals:")
                    print("                     Fraction by year:", Frc)
                    print("                     Cost by year    :", Cst)

                """
                   Now create line for overview table
                """
                if Frc.size != 0:
                    Line.append(None)
                    Line.append(InstCode)
                                    
                    for iYr in range(len(_PrjInst._FinancialYears)):
                        Line.append(Frc[iYr])
                        if Cst.size != 0:
                            Line.append(Cst[iYr])
                        else:
                            Line.append(None)
                            
                    Line.append(np.sum(Frc))
                    Line.append(np.sum(Cst))
                    self._Lines.append(Line)
                    if Overview.__Debug:
                        print("                 Line for csv file:")
                        print("                 ---->", Line)
                    Line = []
                    FrcTot += Frc
                    CstTot += Cst

        """
           Prepare totals line for csv file:
        """
        Line.append(None)
        Line.append("Staff totals")
        
        for iYr in range(len(_PrjInst._FinancialYears)):
            Line.append(FrcTot[iYr])
            Line.append(CstTot[iYr])
        Line.append(np.sum(FrcTot))
        Line.append(np.sum(CstTot))
        self._Lines.append(Line)
        if Overview.__Debug:
            print("           Line for csv file:")
            print("           ---->", Line)
        Line = []

        Line.append("Non-staff cost summary")
        self._Lines.append(Line)
        Line = []

        """
           --------> Work through non-staff cost overview:
        """
        nWP      = 0
        GrnTotNS = np.array([])
        if Overview.__Debug:
            print(" Overview(Report): Loop over w/ps to sum non-staff costs", \
                  " by year")
        for iWP in wp.WorkPackage.instances:
            nWP += 1
            Line.append(nWP)
            Line.append(iWP._Name)
            if Overview.__Debug:
                print("     ----> Work package: ", iWP.getName())

            TotNSByYr = iWP.getTotalNonStaffByYear()
            for iYr in range(len(iWP._FinancialYears)):
                Line.append(None)
                Line.append(TotNSByYr[iYr])
                GrnTotNS       = np.append(GrnTotNS, 0.)
                GrnTotNS[iYr] += TotNSByYr[iYr]
            Line.append(None)
            Line.append(np.sum(TotNSByYr))
            self._Lines.append(Line)
            if Overview.__Debug:
                print("           Line for csv file:")
                print("           ---->", Line)
            Line = []

        Line.append(None)
        Line.append("Non-staff totals")
        for iYr in range(len(iWP._FinancialYears)):
            Line.append(None)
            Line.append(GrnTotNS[iYr])
        Line.append(None)
        Line.append(np.sum(GrnTotNS))
        self._Lines.append(Line)
        Line = []
            
        Line.append("Total staff and non-staff by work package")
        self._Lines.append(Line)
        Line = []

        """
           --------> Sum total staff and non-staff
        """
        if Overview.__Debug:
            print(" Overview(Report): Sum staff and non-staff totals", \
                  " by year")
        nWP      = 0
        for iWP in wp.WorkPackage.instances:
            nWP += 1
            Line.append(nWP)
            Line.append(iWP._Name)
            if Overview.__Debug:
                print("     ----> Work package: ", iWP.getName())

            for iYr in range(len(iWP._FinancialYears)):
                if isinstance(iWP._StaffFracByYear, np.ndarray):
                    Line.append(iWP._StaffFracByYear[iYr])
                if isinstance(iWP._TotalCostByYear, np.ndarray):
                    Line.append(iWP._TotalCostByYear[iYr])
            Line.append(np.sum(iWP._StaffFracByYear))
            Line.append(np.sum(iWP._TotalCostByYear))
            self._Lines.append(Line)
            if Overview.__Debug:
                print("           Line for csv:", Line)
            Line = []
        
        self._Lines.append(Line)
        Line = []

        Line.append("Grand totals")
        Line.append(None)
        TotCst = _PrjInst.getTotalProjectCostByYear()
        for iYr in range(len(_PrjInst._FinancialYears)):
            Line.append(None)
            Line.append(TotCst[iYr])
        Line.append(None)
        Line.append(_PrjInst.getTotalProjectCost())
        self._Lines.append(Line)
        Line = []

    def YearHeader(self, _iPrj):
        Line  = []
        Lines = []
        
        Line.append("Work package")
        Line.append(None)
        for iYr in range(len(_iPrj._FinancialYears)):
            Line.append(_iPrj._FinancialYears[iYr])
            Line.append(None)
        Line.append("Total")
        Line.append(None)
        Lines.append(Line)
        Line = []
        
        Line.append("Id")
        Line.append("Name")
        for iYr in range(len(_iPrj._FinancialYears)+1):
            Line.append("Fraction")
            Line.append("£k")
        Lines.append(Line)

        return Lines

"""
Class StaffList:   -------->  "Staff" report; derived class  <--------
================

  Staff derived class creates and formats the StaffList report.

"""
class StaffList(Report):
    __Debug   = False

    def __init__(self, _ReportPath, _FileName):

        Report.__init__(self, "Staff report: full staff list", \
                        _ReportPath, _FileName)

        self._Header = Stf.Staff.getHeader()
        self._Lines = []
        for iStf in Stf.Staff.instances:
            self._Lines.append(iStf.getData())


    def __str__(self):
        print(" Report: Name: ", self._Name)
        if self.__Debug:
            print("     Output directory path: ", self._ReportPath)
        else:
            dirname,  basename   = os.path.split(self._ReportPath)
            print("     Output directory path: ", basename)
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

  WorkPackageList derived class creates and formats the workpackage list report.

"""
class WorkPackageList(Report):
    __Debug   = False

    def __init__(self, _ReportPath, _FileName):

        Report.__init__(self, \
                        "Work package report: summary of all workpackages", \
                        _ReportPath, _FileName)

        self._Header = wp.WorkPackage.getHeader()
        self._Lines = []
        for iWP in wp.WorkPackage.instances:
            self._Lines.append(iWP.getData())

    def __str__(self):
        print(" Report: Name: ", self._Name)
        if self.__Debug:
            print("     Output directory path: ", self._ReportPath)
        else:
            dirname,  basename   = os.path.split(self._ReportPath)
            print("     Output directory path: ", basename)
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
Class StaffEffortSummary:  ---->  "StaffEffortSummary" report  <----
=========================

  StaffEffortSummary derived class creates and formats the summary
  of the staff effort for a particular project.

"""
class StaffEffortSummary(Report):
    __Debug   = False

    def __init__(self, _ReportPath, _FileName, _PrjInst):

        if not isinstance(_PrjInst, Prj.Project):
            raise ProjectInstanceInvalid( \
                          "Project instance requested invalid")

        """
           --------> Get started:
        """
        if StaffEffortSummary.__Debug:
            print(" ----> StaffEffortSummary: instanciation entered:")

        Report.__init__(self, "Staff effort summary", _ReportPath, _FileName)

        """
           --------> Set header lines:
        """
        self._Header = []
        self._Header.append(_PrjInst._Name)
        for i in range(len(_PrjInst._FinancialYears)):
            for j in range(2):
                self._Header.append(None)
        self._Header.append("Report date:")
        RptDt = date.today()
        self._Header.append(RptDt.strftime("%d-%b-%Y"))

        """
           --------> Financial years:
        """
        self._Lines = []
        Line        = []
        Line.append(None)
        NullLine = Line
        self._Lines.append(Line)

        Lines = self.YearHeader(_PrjInst)
        for iLn in range(len(Lines)):
            Line = Lines[iLn]
            self._Lines.append(Line)

        FrcGrndTot = np.array([])
        CstGrndTot = np.array([])
        for iYr in range(len(_PrjInst._FinancialYears)):
            FrcGrndTot = np.append(FrcGrndTot, 0.)
            CstGrndTot = np.append(CstGrndTot, 0.)

        """
           --------> Process staff list:
        """
        InstCode   = None
        FrcTot     = np.array([])
        CstTot     = np.array([])
        for iStf in Stf.Staff.instances:
            if StaffEffortSummary.__Debug:
                print("     ----> New from Staff instances: ", \
                      iStf._InstituteCode, "; ", iStf._StaffCode)
                print("           Present institute code: ", InstCode)
                      
            Line = []

            #----> Institute:
            if InstCode != iStf._InstituteCode:
                if len(FrcTot) != 0:
                    Line.append("Total")
                    for iYr in range(len(_PrjInst._FinancialYears)):
                        Line.append(FrcTot[iYr])
                        Line.append(CstTot[iYr])
                    Line.append(np.sum(FrcTot))
                    Line.append(np.sum(CstTot))
                    self._Lines.append(Line)
                    Line = []
                    FrcGrndTot += FrcTot
                    CstGrndTot += CstTot
                    
                    if StaffEffortSummary.__Debug:
                        print("         ----> Institute totals: ")
                        print("             ----> Fractions: ", \
                 FrcTot[0], FrcTot[1], FrcTot[2], FrcTot[3], FrcTot[4], \
                              np.sum(FrcTot))
                        print("             ----> Costs    : ", \
                 CstTot[0], CstTot[1], CstTot[2], CstTot[3], CstTot[4], \
                              np.sum(CstTot))

                FrcTot = np.array([])
                CstTot = np.array([])
                for iYr in range(len(_PrjInst._FinancialYears)):
                    FrcTot = np.append(FrcTot, 0.)
                    CstTot = np.append(CstTot, 0.)
                    
                InstCode = iStf._InstituteCode
                Line.append(InstCode)
                self._Lines.append(Line)
                Line = []
                if StaffEffortSummary.__Debug:
                    print("         ----> Staff to task for InstCode: ", \
                          InstCode)

            #----> Staff code:
            Line.append(iStf._StaffCode)
            self._Lines.append(Line)
            Line = []

            #----> Staff fraction and cost by year:
            Frc = np.array([])
            Cst = np.array([])
            iTsk     = None
            wpName   = None
            wpList   = _PrjInst._Name + ": "
            for iYr in range(len(_PrjInst._FinancialYears)):
                Frc = np.append(Frc, 0.)
                Cst = np.append(Cst, 0.)
            for iTskStf in TskStf.TaskStaff.instances:
                if iTskStf._Staff == iStf:
                    if StaffEffortSummary.__Debug:
                        print("             ----> Task matched! \n", \
                "                       Task:", iTskStf._Task._Name, \
                              " - staff code:", iStf._StaffCode)
                    if iTsk != iTskStf._Task:
                        if wpName != iTskStf._Task._WorkPackage._Name:
                            wpName = iTskStf._Task._WorkPackage._Name
                            wpList += wpName + " "
                    if isinstance(iTskStf._StaffFracByYear, np.ndarray):
                        Frc += iTskStf._StaffFracByYear
                    if isinstance(iTskStf._StaffCostByYear, np.ndarray):
                        Cst += iTskStf._StaffCostByYear
            Line.append(wpList)
            for iYr in range(len(_PrjInst._FinancialYears)):
                Line.append(Frc[iYr])
                Line.append(Cst[iYr])
            Line.append(np.sum(Frc))
            Line.append(np.sum(Cst))
            self._Lines.append(Line)
            if StaffEffortSummary.__Debug:
                print("         ----> Staff line: ", Line)
            FrcTot += Frc
            CstTot += Cst

        Line = []
        if len(FrcTot) != 0:
            Line.append("Total")
            for iYr in range(len(_PrjInst._FinancialYears)):
                Line.append(FrcTot[iYr])
                Line.append(CstTot[iYr])
            Line.append(np.sum(FrcTot))
            Line.append(np.sum(CstTot))
            self._Lines.append(Line)
        if StaffEffortSummary.__Debug:
            print("     ----> Total: ", Line)

        FrcGrndTot += FrcTot
        CstGrndTot += CstTot
        Line = []
        Line.append("Grand total")
        for iYr in range(len(_PrjInst._FinancialYears)):
            Line.append(FrcGrndTot[iYr])
            Line.append(CstGrndTot[iYr])
        Line.append(np.sum(FrcGrndTot))
        Line.append(np.sum(CstGrndTot))
        self._Lines.append(Line)
        if StaffEffortSummary.__Debug:
            print("     ----> Grand total: ", Line)

    def YearHeader(self, _iPrj):
        Line  = []
        Lines = []
        
        Line.append("Staff")
        for iYr in range(len(_iPrj._FinancialYears)):
            Line.append(_iPrj._FinancialYears[iYr])
            Line.append(None)
        Line.append("Total")
        Line.append(None)
        Lines.append(Line)
        
        Line = []
        Line.append(None)
        for iYr in range(len(_iPrj._FinancialYears)+1):
            Line.append("Fraction")
            Line.append("£k")
        Lines.append(Line)

        return Lines
    
        
"""
Class WorkPackageSummary:  ---->  "WorkPackageSummary" report  <----
=========================

  WorkPackageSummary derived class creates and formats the summary
  workpackage report.

"""
class WorkPackageSummary(Report):
    __Debug   = False

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

        if WorkPackageSummary.__Debug:
            print(_wpInst)
        Line = self.StaffTotal(_wpInst)
        self._Lines.append(Line)
        
        Line = self.EquipmentHeader(_wpInst)
        self._Lines.append(Line)
        
        for iTsk in Tsk.Task.instances:
            if iTsk._WorkPackage == _wpInst:
                Lines = self.TaskEquipmentLines(_wpInst, iTsk)
                for Line in Lines:
                    self._Lines.append(Line)

        Line = self.EquipmentTotal(_wpInst)
        self._Lines.append(Line)
        
        Line = self.Inflation(_wpInst)
        self._Lines.append(Line)

        for iONS in ONS.OtherNonStaff.instances:
            if iONS._WPInst == _wpInst:
                Line = self.OtherNonStaffLines(_wpInst, iONS)
                self._Lines.append(Line)
                
        Line = self.Consumables(_wpInst)
        self._Lines.append(Line)
        
        Line = self.Travel(_wpInst)
        self._Lines.append(Line)
        
        Line = self.RiskMitigationEquip(_wpInst)
        self._Lines.append(Line)
        
        Line = self.WorkingMargin(_wpInst)
        self._Lines.append(Line)
        
        Lines = self.Contingency(_wpInst)
        for Line in Lines:
            self._Lines.append(Line)
        
        Line = NullLine
        self._Lines.append(Line)

        Line = self.Total(_wpInst)
        self._Lines.append(Line)
                
    def __str__(self):
        print(" Report: Name: ", self._Name)
        if self.__Debug:
            print("     Output directory path: ", self._ReportPath)
        else:
            dirname,  basename   = os.path.split(self._ReportPath)
            print("     Output directory path: ", basename)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
        return "     <---- Report __str__ done."


#--------  Processing methods:
    def Total(self, _wpInst):
        Line = []
        Line.append("Total:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._TotalCostByYear, np.ndarray):
                Line.append(_wpInst._TotalCostByYear[iYr])
            else:
                Line.append(None)
        Line.append(None)
        if isinstance(_wpInst._GrandTotal, float):
            Line.append(_wpInst._GrandTotal)
        else:
            Line.append(None)
        return Line

    def WorkingMargin(self, _wpInst):
        Line = []
        Line.append("Working margin:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._WorkingMarginByYear, np.ndarray):
                Line.append(_wpInst._WorkingMarginByYear[iYr])
            else:
                Line.append(0.)
    
        Line.append(None)
        if isinstance(_wpInst._WorkingMarginTotal, float):
            Line.append(_wpInst._WorkingMarginTotal)
        else:
            Line.append(0.)
            
        return Line

    def Contingency(self, _wpInst):
        Line  = []
        Lines = []
        
        Line.append("Contingency, equipment:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._ContingencyByYear[0], np.ndarray):
               Line.append(_wpInst._ContingencyByYear[0][iYr])
            else:
               Line.append(0.)
        Line.append(None)
        Line.append(_wpInst._ContingencyTotal[0])
        Lines.append(Line)

        Line = []
        Line.append("Contingency, CG staff:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._ContingencyByYear[2], np.ndarray):
               Line.append(_wpInst._ContingencyByYear[2][iYr])
            else:
               Line.append(0.)
        Line.append(None)
        Line.append(_wpInst._ContingencyTotal[1])
        Lines.append(Line)
        
        Line = []
        Line.append("Contingency, all staff:")
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            if isinstance(_wpInst._ContingencyByYear[1], np.ndarray):
               Line.append(_wpInst._ContingencyByYear[1][iYr])
            else:
               Line.append(0.)
        Line.append(None)
        Line.append(_wpInst._ContingencyTotal[1])
        Lines.append(Line)

        return Lines

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
        Line.append("Inflation:")
        for iYr in range(len(_wpInst._FinancialYears)):
            print(" Report.Inflation: iYr, yr to strt:", \
                  iYr, iCntrl._Inflation[2])
            Line.append(None)
            if isinstance(_wpInst._InflationByYr, np.ndarray):
                Line.append(_wpInst._InflationByYr[iYr])
            else:
                Line.append(None)
        Line.append(None)
        Line.append(_wpInst._TotalInflation)
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
        return Lines
        
    def OtherNonStaffLines(self, _wpInst, _iONS):
        Line  = []
        Line.append(_iONS._Name)
        for iYr in range(len(_wpInst._FinancialYears)):
            Line.append(None)
            Line.append(_iONS._OtherNonStaffCostByYear[iYr])
        Line.append(None)
        Line.append(_iONS._TotalOtherNonStaffCost)
        return Line
            
        
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
            if isinstance(_wpInst._StaffFracByYear, np.ndarray):
                Line.append(_wpInst._StaffFracByYear[iYr])
            if isinstance(_wpInst._StaffCostByYear, np.ndarray):
                Line.append(round(_wpInst._StaffCostByYear[iYr], 2))
            else:
                Line.append(None)
        Line.append(_wpInst._TotalStaffFrac)
        if isinstance(_wpInst._TotalStaffCost, float):
            Line.append(round(_wpInst._TotalStaffCost, 2))
        else:
            Line.append(None)
            
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

class ProjectInstanceInvalid:
    pass

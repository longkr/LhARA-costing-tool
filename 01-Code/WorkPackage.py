#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class WorkPackage:
==================

Note to KL: Travel and Consumable attributes need to be added.

  Creates an instance of the work package class and populates the
  attiributes from a csv-format workpackage template that is owned 
  by the workpackage manager.

  The WorkPackage class is the principal driver of the data structure that
  underpins the LhARA costing tool.

  Class attributes:
  -----------------
  __Debug  : Boolean: set for debug print out
  instances: List of instances if the WorkPackage class.
      
  Instance attributes:
  --------------------
   _filename            = Filename, includin path, to csv file containing
                          workpackage specification
   _wpParams            = Pandas dataframe instance containing workpackage 
                          specification
   _Name                = Work package name
   _WPM                 = Work package manager(s)
   _Project             = Instance of Project class to which this work package 
                          belongs
   _StaffCostByYear     = Total cost of staff in £k for this workpackage by FY
   _CGStaffCostByYear   = Cost of CG staff in £k for this workpackage by FY
   _TotalStaffCost      = Summed total staff cost over duration of project (£k)
   _TotalCGStaffCost    = Summed total CG staff cost over duration of project 
                          (£k)
   _EquipmentCostByYear = Total cost of equipment in £k for this workpackage 
                          by FY
   _TotalEquipCost      = Summed total equipment cost over duration of project 
                          (£k)
   _TravelByYear        = Cost of travel (£k) per financial year
   _TotalTravel         = Total cost of travel (£k)
   _ConsumeByYear       = Cost of consumables (£k) per financial year
                          Includes cost of "other non-staff items"
   _TotalConsume        = Total cost of consumables
   _TrvlCnsmCostByYear  = Sum of travel and consumables by financial year (£k)
   _TotalTrvlCnsmCost   = Total of sum of travel and consumables (£k)
   _OtherNonStaffItems  = List of what enters "other non staff items"

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version and values
                of decay-straight parameters used.
      __repr__: One liner with call.
      __str__ : Dump of constants

  I/o methods:
      getWorkPackage: Uses pandas to read csv file that defines the workpackage.
                      Input  : filename -- valid path to csv file
                      Returns: PandaS data frame containing workpackage 
                               specification

      createCSV     : Creates CSV file containing work package paramters.
                      [Classmethod]
                      Input: Instance of Pandas dataframe class containing 
                             parameters
                             String -- path to output file (filename)

  Print methods:
      printWorkPackage: Prints pandas data frame defining workpackage

  Get/set methods:
      getFilename: Returns workpackage specification filename

      setStaffCostByYear    : Set staff cost by financial year (£k)
                              Input: numpy array
        
      setCGStaffCostByYear  : Set CG staff cost by financial year (£k)
                              Input: numpy array

      setTotalStaffCost     : Set total staff cost; sum cost per year (£k)
        
      setTotalCGStaffCost   : Set total staff cost; sum cost per year (£k)

      setEquipmentCostByYear: Set equipment cost by financial year (£k)
                              Input: numpy array
  
      setTotalEquipmentCost : Set total equipment cost; sum cost per year (£k)

      setTravelCostByYear   : Set travel cost by financial 
                              year (£k)
                              Input: numpy array

      setTotalTravelCost    : Set total travel cost; 
                              sum cost per year (£k)

      setConsumeCostByYear  : Set consumable cost by financial 
                              year (£k)
                              Input: numpy array

      setTotalConsumeCost   : Set total consumable cost; 
                              sum cost per year (£k)

      setTrvlCnsmCostByYear : Set travel and consumable cost by financial 
                              year (£k)
                              Input: numpy array

      setTotalTrvlCnsmCost  : Set total travel and consumable cost; 
                              sum cost per year (£k)


  Print methods:
      printWorkPackage: Dumps pandas data frame read from CSV work package
                        definition file


  Processing methods:
      parseWorkPackage: Parses pandas data frame to fill many of the 
                        work package attributes.  
             Returns:
               self._Project
               self._Name
               self._WPM
               self._FinancialYears
               self._TravelByYear
               self._TotalTravel
               self._ConsumeByYear
               self._TotalConsume
               self._OtherNonStaffItems

      clean: Delete incomplete instances of WorkPackage
             [classmethod]

      doCosting: Complete costing of WorkPackage.  Sums data from Tasks
                 related to WorkPackage instance and completes work package
                 costing.
                 Fills:
                    self._StaffCostByYear   
                    self._CGStaffCostByYear 
                    self._TotalStaffCost    
                    self._TotalCGStaffCost  
                    self._EquipmentCostByYear
                    self._TotalEquipmentCost 
                 [Classmethod]

      createPandasDataframe : Create Pandas data frame containing Work package
                              parameters.
                              [Classmethod]
                 Input: None.
                Return: Instance of Pandas class.


  Exceptions:
    NoFilenameProvided: no filename for work package definition CSV file

    NonExistantFile(Exception): filename provided for work package definition
                                does not exist


Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 19Jun21: First implementation

@author: kennethlong
"""
import os as os
import math as mt
import copy
import numpy as np
import pandas as pnds

import Project       as Prj
import Task          as Tsk
import Staff         as Stf
import Equipment     as Eqp
import TaskStaff     as TskStff
import TaskEquipment as TskEqp

class WorkPackage:
    __Debug    = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, filename=None): #, _PrjInst=None):
        if filename == None:
            raise NoFilenameProvided('CSV filename required; execution termimated.')
        elif not os.path.isfile(filename):
            raise NonExistantFile('CSV file' + filename +' does not exist; execution termimated.')

        self._filename        = filename
        self._wpParams        = self.getWorkPackage(filename)
        self._Name = "Place holder"
        if self.__Debug:
            xDummy = self.printWorkPackage()

        self._Name                = None
        self._Project             = None
        self._WPM                 = None
        self._FinancialYears      = None
        self._TravelByYear        = None
        self._TotalTravel         = None
        self._ConsumeByYear       = None
        self._TotalConsume        = None
        self._TrvlCnsmCostByYear  = None
        self._TotalTrvlCnsmCost   = None
        self._OtherNonStaffItems  = []

        #.. Defined, but not filled, at init:
        self._StaffCostByYear     = None
        self._CGStaffCostByYear   = None
        self._TotalStaffCost      = None
        self._TotalCGStaffCost    = None
        self._EquipmentCostByYear = None
        self._TotalEquipmentCost  = None

        self._Project,  \
            self._Name, \
            self._WPM,  \
            self._FinancialYears, \
            self._TravelByYear, \
            self._TotalTravel, \
            self._ConsumeByYear, \
            self._TotalConsume, \
            self._OtherNonStaffItems = \
            self.parseWorkPackage()

        self._TrvlCnsmCostByYear  = self._TravelByYear + self._ConsumeByYear
        self._TotalTrvlCnsmCost   = np.sum(self._TrvlCnsmCostByYear)
        
        WorkPackage.instances.append(self)

    def __repr__(self):
        return "WorkPackage()"

    def __str__(self):
        _PrjName = self._Project._Name
        print(" WorkPackage: name:", _PrjName, " ---->")
        print("     Project:", self._Project._Name, \
              " Manager:", self._WPM, \
              " Financial years:", self._FinancialYears)
        print("     Staff cost by year, total:", self._StaffCostByYear, \
              self._TotalStaffCost)
        print("     CG staff cost by year, total:", self._CGStaffCostByYear, \
              self._TotalCGStaffCost)
        print("     Equipment cost by year, total", self._EquipmentCostByYear, \
              self._TotalEquipmentCost)
        print("     Travel cost by year, total", self._TravelByYear,
              self._TotalTravel)
        print("     Consumables cost by year (including other non-staff):",
              self._ConsumeByYear, self._TotalConsume)
        print("     Other non-staff categories:", self._OtherNonStaffItems)
        print("     Travel and consumable cost by year, total:", \
              self._TrvlCnsmCostByYear, self._TotalTrvlCnsmCost)
        return "     <---- WorkPackage done."
    

#--------  I/o methods:
    def getWorkPackage(self, _filename):
        wpParams = pnds.read_csv(_filename)
        return wpParams

    @classmethod
    def createCSV(cls, _WrkPckgDataFrame, _filename):
        _WrkPckgDataFrame.to_csv(_filename)
    

#--------  Get/set methods:
    def getFilename(self):
        return self._filename

    def setStaffCostByYear(self, _StaffCostByYear):
        self._StaffCostByYear = _StaffCostByYear
        
    def setCGStaffCostByYear(self, _CGStaffCostByYear):
        self._CGStaffCostByYear = _CGStaffCostByYear

    def setTotalStaffCost(self):
        self._TotalStaffCost = np.sum(self._StaffCostByYear)
        
    def setTotalCGStaffCost(self):
        self._TotalCGStaffCost = np.sum(self._CGStaffCostByYear)
        
    def setEquipmentCostByYear(self, _EquipmentCostByYear):
        self._EquipmentCostByYear = _EquipmentCostByYear

    def setTotalEquipmentCost(self):
        self._TotalEquipmentCost = np.sum(self._EquipmentCostByYear)

    def setTravelCostByYear(self, _TravelCostByYear):
        self._TravelCostByYear = _TravelCostByYear

    def setTotalTravelCost(self):
        self._TotalTravelCost = np.sum(self._TravelCostByYear)

    def setConsumeCostByYear(self, _ConsumeCostByYear):
        self._ConsumeCostByYear = _ConsumeCostByYear

    def setTotalConsumeCost(self):
        self._TotalConsumeCost = np.sum(self._ConsumeCostByYear)

    def setTrvlCnsmCostByYear(self, _TrvlCnsmCostByYear):
        self._TrvlCnsmCostByYear = _TrvlCnsmCostByYear
        
    def setTotalTrvlCnsmCost(self):
        self._TotalTrvlCnsmCost = np.sum(self._TrvlCnsmCostByYear)

    @classmethod
    def getHeader(cls):
        HeaderList = ["Name", "Project", "filename", \
                              "Work package manager", \
                              "Number of financial years", \
                              "Staff cost per year (£k)", \
                              "CG staff cost per year (£k)", \
                              "Total staff cost (£k)", \
                              "Total CG staff cost (£k)", \
                              "Equipment cost by year (£k)", \
                              "Total equipment cost (£k)", \
                              "Travel by year (£k)", \
                              "Total travelk (£k)", \
            "Consumables by year (including other non staff items) (£k)", \
                              "Total consumables (£k)", \
                              "Travel and consumables by year (£k)", \
                              "Total travel and consumables (£k)",
                              "Other non staff items"]
        return HeaderList

    def getData(self):
        DataList = [self._Name, \
                    self._Project._Name, \
                    self._filename, \
                    self._WPM, \
                    self._FinancialYears, \
                    self._StaffCostByYear, \
                    self._CGStaffCostByYear, \
                    self._TotalStaffCost, \
                    self._TotalCGStaffCost, \
                    self._EquipmentCostByYear, \
                    self._TotalEquipmentCost, \
                    self._TravelByYear, \
                    self._TotalTravel, \
                    self._ConsumeByYear, \
                    self._TotalConsume, \
                    self._TrvlCnsmCostByYear, \
                    self._TotalTrvlCnsmCost, \
                    self._OtherNonStaffItems]
        return DataList



#--------  Print methods
    def printWorkPackage(self):
        print(self._wpParams)

        
#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        WorkPackageData = []
        WorkPackageData.append(cls.getHeader())
        for inst in WorkPackage.instances:
            WorkPackageData.append(inst.getData())
        WorkPackageDataframe = pnds.DataFrame(WorkPackageData)
        if cls.__Debug:
            print(" WorkPackage; createPandasDataframe: \n", \
                  WorkPackageDataframe)
        return WorkPackageDataframe


#--------  Extracting data from the WorkPackage pandas dataframe:
    def parseWorkPackage(self):
        iRow               = self._wpParams.index
        PrjInst            = None
        WorkPackageName    = "None"
        OtherNonStaffItems = []
        for i in iRow:
            if self.__Debug:
                print(" WorkPackage: parseWorkPackage: processing flag: ", \
                      self._wpParams.iat[i,0])
            if self._wpParams.iat[i,0] == "Project":
                ProjectName = self._wpParams.iloc[i,1]
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: ProjectName = ", \
                          ProjectName)
                PrjInst = Prj.Project.getInstance(ProjectName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Project instance: ",\
                          PrjInst)
                if isinstance(PrjInst, Prj.Project):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Project ", \
                              ProjectName, " exists.")
                else:
                    PrjInst = Prj.Project(ProjectName)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Project ", \
                              ProjectName, " created.")
                PrjInst = Prj.Project.getInstance(ProjectName)
            elif self._wpParams.iat[i,0] == "Work package":
                WorkPackageName = self._wpParams.iloc[i,1]
            elif self._wpParams.iat[i,0] == "Manager":
                WPM = self._wpParams.iloc[i,2]
            elif self._wpParams.iat[i,0] == "Years":
                nYrs = 0
                Yrs  = []
                Yr   = ""
                while Yr != "Total":
                    Yr = self._wpParams.iloc[i,2+nYrs]
                    if Yr != "Total":
                        Yrs.append(Yr)
                        nYrs += 1
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: financial years:", \
                          Yrs)
            elif self._wpParams.iat[i,0] == "Task":
                TaskName = self._wpParams.iloc[i,1]
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Task name = ", \
                          TaskName)
                TskInst = Tsk.Task.getInstance(TaskName, self)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Task instance = ", \
                          TskInst)
                if isinstance(TskInst, Tsk.Task):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Task ", \
                              TaskName, " exists.")
                else:
                    TskInst = Tsk.Task(TaskName, self)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Task ", \
                              TaskName, " created.")
            elif self._wpParams.iat[i,0] == "Staff":
                StaffCode = self._wpParams.iloc[i,1]
                StfInst = Stf.Staff.getInstance(StaffCode)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Staff instance = ", \
                          StfInst)
                if isinstance(StfInst, Stf.Staff):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Staff ", \
                              StaffCode, " exists.")
                else:
                    NameOrPost = "Created for WP " + WorkPackageName
                    StfInst = Stf.Staff(StaffCode, NameOrPost)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: Staff ", \
                              StaffCode, " created.")
                TskStfInst = TskStff.TaskStaff.getInstance(TskInst, StfInst)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: TskStfInst:", \
                          TskStfInst)
                if isinstance(TskStfInst, TskStff.TaskStaff):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: TaskStaff ", \
                              TskInst._Name, StfInst._NameOrPost, \
                              " exists.")
                else:
                    TskStfInst = TskStff.TaskStaff(TskInst, StfInst)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkPackage: TaskStaff ", \
                              TskStfInst, " created.")
                if self.__Debug:
                    print("      ----> fill staff fractions:")
                StfFracByYrNQtr = np.empty(shape=(1,4))
                FracByQtr       = np.array([[0., 0., 0., 0.]])
                for iYr in range(nYrs):
                    for iQtr in range(4):
                        Frac = float(self._wpParams.iat[i, 9+4*iYr+iQtr])
                        if np.isnan(Frac):
                            Frac = 0.
                        FracByQtr[0,iQtr] = Frac
                    if iYr == 0:
                        StfFracByYrNQtr = copy.deepcopy(FracByQtr.reshape(1,4))
                    else:
                        Frac1 = copy.deepcopy(FracByQtr)
                        StfFracByYrNQtr = np.append(StfFracByYrNQtr, \
                                                    Frac1, \
                                                    axis=0)
                if self.__Debug:
                    print("     ", StaffCode, \
                          ": fraction by year and quarter: \n", \
                          StfFracByYrNQtr)
                TskStfInst.setStaffFracByYrNQtr(StfFracByYrNQtr)
                TskStfInst.setStaffFracByYear()
                TskStfInst.setTotalStaffFrac()
                if self.__Debug:
                    print("     ----> staff fractions filled:", TskStfInst)
            elif self._wpParams.iat[i,0] == "Equipment":
                EquipmentName = self._wpParams.iloc[i,1]
                EqpInst = Eqp.Equipment(EquipmentName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Equipment ", \
                              EquipmentName, " created.")
                TskEqpInst = TskEqp.TaskEquipment(TskInst, EqpInst)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: TaskEquipment ", \
                           TskEqpInst, " created.")
                EqpCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    EqpCst = np.append(EqpCst,Cst)
                EqpInst.setEquipmentCost(EqpCst)
                EqpInst.setTotalEquipmentCost()
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: ", \
                          "equipment cost by year:", EqpInst._EquipmentCost, \
                          " Total:", EqpInst._TotalEquipmentCost)
            elif str(self._wpParams.iat[i,0]) == "EndStaff":
                pass
            elif str(self._wpParams.iat[i,0]) == "NonStaffHd":
                pass
            elif str(self._wpParams.iat[i,0]) == "EquipEnd":
                pass
            elif str(self._wpParams.iat[i,0]) == "RiskMitigationEquip":
                pass
            elif str(self._wpParams.iat[i,0]) == "TotalEquip":
                pass
            elif str(self._wpParams.iat[i,0]) == "Consume":
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Consumables")
                CnsCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    CnsCst = np.append(CnsCst,Cst)
                _ConsumeByYear = CnsCst
                _TotalConsume  = np.sum(_ConsumeByYear)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: ", \
                          "consumables cost by year and total:", \
                          _ConsumeByYear, _TotalConsume)
            elif str(self._wpParams.iat[i,0]) == "Travel":
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: Travel")
                TrvCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    TrvCst = np.append(TrvCst,Cst)
                _TravelByYear = TrvCst
                _TotalTravel  = np.sum(_TravelByYear)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: ", \
                          "travel cost by year and total:", \
                          _TravelByYear, _TotalTravel)
            elif str(self._wpParams.iat[i,0]) == "OtherNonStaff":
                OtherNonStaffItems.append(self._wpParams.iat[i,1])
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: other non-staff: ",\
                          self._wpParams.iat[i,1])
                CnsCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    CnsCst = np.append(CnsCst,Cst)
                if not isinstance(_ConsumeByYear, np.ndarray):
                    _ConsumeByYear = CnsCst
                else:
                    _ConsumeByYear += CnsCst
                _TotalConsume  = np.sum(_ConsumeByYear)
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: consumables + ", \
                          "other non-staff cost by year and total:", \
                          _ConsumeByYear, _TotalConsume)
            elif str(self._wpParams.iat[i,0]) == "NonStaffEnd":
                pass
            elif str(self._wpParams.iat[i,0]) == "Flag":
                pass
            elif str(self._wpParams.iat[i,0]) == "nan":
                pass
            else:
                if self.__Debug:
                    print(" WorkPackage; parseWorkPackage: ", \
                          "Unprocessed ---->", self._wpParams.iloc[i,0])

        return PrjInst, WorkPackageName, WPM, Yrs, \
               _TravelByYear, _TotalTravel, \
               _ConsumeByYear, _TotalConsume, \
               OtherNonStaffItems

    @classmethod
    def clean(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iWP in OldInst:
            if iWP._filename == None or \
               not isinstance(iWP._wpParams, pnds.DataFrame) or \
               not isinstance(iWP._Name, str) or \
               not isinstance(iWP._TrvlCnsmCostByYear, np.ndarray):
                del iWP
                nDel += 1
            else:
                NewInst.append(iWP)
        cls.instances = NewInst
        return nDel

    @classmethod
    def doCosting(cls):
        for iWp in cls.instances:
            _StaffCostByYear   = np.array([])
            _CGStaffCostByYear = np.array([])
            _EquipmentCostByYear = np.array([])
            SumInitialised = False
            for iTsk in Tsk.Task.instances:
                if iTsk._WorkPackage == iWp:
                    if not SumInitialised:
                        for iYr in range(len(iTsk._StaffCostByYear)):
                            _StaffCostByYear     = \
                                np.append(_StaffCostByYear,   [0.])
                            _CGStaffCostByYear   = \
                                np.append(_CGStaffCostByYear, [0.])
                            _EquipmentCostByYear = \
                                np.append(_EquipmentCostByYear,   [0.])
                    SumInitialised = True
                    if len(iTsk._StaffCostByYear) > 0:
                        _StaffCostByYear += iTsk._StaffCostByYear
                    if len(iTsk._CGStaffCostByYear) > 0:
                        _CGStaffCostByYear += iTsk._CGStaffCostByYear
                    if len(_EquipmentCostByYear):
                        _EquipmentCostByYear += iTsk._EquipmentCostByYear
                
            iWp._StaffCostByYear = _StaffCostByYear
            iWp.setTotalStaffCost()
            iWp._CGStaffCostByYear = _CGStaffCostByYear
            iWp.setTotalCGStaffCost()
            iWp._EquipmentCostByYear = _EquipmentCostByYear
            iWp.setTotalEquipmentCost()

            
#--------  Exceptions:
class NoFilenameProvided(Exception):
    pass

class NonExistantFile(Exception):
    pass

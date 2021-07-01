#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class WorkPackage:
==================

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
      getWorkpackage: Uses pandas to read csv file that defines the workpackage.
                      Input  : filename -- valid path to csv file
                      Returns: PandaS data frame containing workpackage 
                               specification

      createCSV     : Creates CSV file containing work package paramters.
                      [Classmethod]
                      Input: Instance of Pandas dataframe class containing 
                             parameters
                             String -- path to output file (filename)

  Print methods:
      printWorkpackage: Prints pandas data frame defining workpackage

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
      printWorkpackage: Dumps pandas data frame read from CSV work package
                        definition file


  Processing methods:
      parseWorkpackage: Parses pandas data frame to fill many of the 
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

      clean: Delete incomplete instances of Workpackage
             [classmethod]

      doCosting: Complete costing of Workpackage.  Sums data from Tasks
                 related to Workpackage instance and completes work package
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
        self._wpParams        = self.getWorkpackage(filename)
        self._Name = "Place holder"
        if self.__Debug:
            xDummy = self.printWorkpackage()

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
            self.parseWorkpackage()

        self._TrvlCnsmCostByYear  = self._TravelByYear + self._ConsumeByYear
        self._TotalTrvlCnsmCost   = np.sum(self._TrvlCnsmCostByYear)
        
        WorkPackage.instances.append(self)

    def __repr__(self):
        return "WorkPackage()"

    def __str__(self):
        _PrjName = self._Project._Name
        print(" Workpackage: name:", _PrjName, " ---->")
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
    def getWorkpackage(self, _filename):
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

    def setTrvlCnsmCostByYear(self, _TrvlCnsmCostByYear):
        self._TrvlCnsmCostByYear = _TrvlCnsmCostByYear
        
    def setTotalTrvlCnsmCost(self):
        self._TotalTrvlCnsmCost = np.sum(self._TrvlCnsmCostByYear)


#--------  Print methods
    def printWorkpackage(self):
        print(self._wpParams)

        
#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        WorkpackageData = []
        WorkpackageData.append(["Name", "Project", "filename", \
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
                                "Other non staff items"])
        for inst in WorkPackage.instances:
            WorkpackageData.append([inst._Name, \
                                    inst._Project._Name, \
                                    inst._filename, \
                                    inst._WPM, \
                                    inst._FinancialYears, \
                                    inst._StaffCostByYear, \
                                    inst._CGStaffCostByYear, \
                                    inst._TotalStaffCost, \
                                    inst._TotalCGStaffCost, \
                                    inst._EquipmentCostByYear, \
                                    inst._TotalEquipmentCost, \
                                    inst._TravelByYear, \
                                    inst._TotalTravel, \
                                    inst._ConsumeByYear, \
                                    inst._TotalConsume, \
                                    inst._TrvlCnsmCostByYear, \
                                    inst._TotalTrvlCnsmCost, \
                                    inst._OtherNonStaffItems])
        WorkpackageDataframe = pnds.DataFrame(WorkpackageData)
        if cls.__Debug:
            print(" Workpackage; createPandasDataframe: \n", \
                  WorkpackageDataframe)
        return WorkpackageDataframe


#--------  Extracting data from the Workpackage pandas dataframe:
    def parseWorkpackage(self):
        iRow               = self._wpParams.index
        PrjInst            = None
        WorkpackageName    = "None"
        OtherNonStaffItems = []
        for i in iRow:
            if self._wpParams.iat[i,0] == "Project":
                ProjectName = self._wpParams.iloc[i,1]
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: ProjectName = ", \
                          ProjectName)
                PrjInst = Prj.Project.getInstance(ProjectName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: Project instance: ",\
                          PrjInst)
                if isinstance(PrjInst, Prj.Project):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Project ", \
                              ProjectName, " exists.")
                else:
                    PrjInst = Prj.Project(ProjectName)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Project ", \
                              ProjectName, " created.")
                PrjInst = Prj.Project.getInstance(ProjectName)
            elif self._wpParams.iat[i,0] == "Work package":
                WorkpackageName = self._wpParams.iloc[i,1]
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
                    print(" WorkPackage; parseWorkpackage: financial years:", \
                          Yrs)
            elif self._wpParams.iat[i,0] == "Task":
                TaskName = self._wpParams.iloc[i,1]
                TskInst = Tsk.Task.getInstance(TaskName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: Task instance = ", \
                          TskInst)
                if isinstance(TskInst, Tsk.Task):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Task ", \
                              TaskName, " exists.")
                else:
                    TskInst = Tsk.Task(TaskName, self)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Task ", \
                              TaskName, " created.")
            elif self._wpParams.iat[i,0] == "Staff":
                StaffName = self._wpParams.iloc[i,1]
                StfInst = Stf.Staff.getInstance(StaffName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: Staff instance = ", \
                          StfInst)
                if isinstance(StfInst, Stf.Staff):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Staff ", \
                              StaffName, " exists.")
                else:
                    StfInst = Stf.Staff(StaffName, "Workpackage")
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Staff ", \
                              StaffName, " created.")
                TskStfInst = TskStff.TaskStaff.getInstance(TskInst, StfInst)
                if self.__Debug:
                    print(" Workpackage; parseWorkpackage: TskStfInst:", \
                          TskStfInst)
                if isinstance(TskStfInst, TskStff.TaskStaff):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: TaskStaff ", \
                              TskInst._TaskName, StfInst._NameOrPost, \
                              " exists.")
                else:
                    TskStfInst = TskStff.TaskStaff(TskInst, StfInst)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: TaskStaff ", \
                              TskStfInst, " created.")
                if self.__Debug:
                    print("      ----> fill staff fractions:")
                StfFracByYrNQtr = np.empty(shape=(1,4))
                FracByQtr       = np.array([[0., 0., 0., 0.]])
                for iYr in range(nYrs):
                    for iQtr in range(4):
                        FracByQtr[0,iQtr] = self._wpParams.iat[i, 9+4*iYr+iQtr]
                    if iYr == 0:
                        StfFracByYrNQtr = FracByQtr.reshape(1,4)
                    else:
                        StfFracByYrNQtr = np.append(StfFracByYrNQtr, \
                                                    FracByQtr, axis=0)
                if self.__Debug:
                    print("     ", StaffName, \
                          ": fraction by year and quarter: \n", \
                          StfFracByYrNQtr)
                TskStfInst.setStaffFracByYrNQtr(StfFracByYrNQtr)
                TskStfInst.setStaffFracByYear()
                TskStfInst.setTotalStaffFrac()
                if self.__Debug:
                    print("     ----> staff fractions filled:", TskStfInst)
            elif self._wpParams.iat[i,0] == "Equipment":
                EquipmentName = self._wpParams.iloc[i,1]
                EqpInst = Eqp.Equipment.getInstance(EquipmentName)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: ", \
                          "Equipment instance = ", EqpInst)
                if isinstance(EqpInst, Eqp.Equipment):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Equipment ", \
                              EquipmentName, " exists.")
                else:
                    EqpInst = Eqp.Equipment(EquipmentName)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: Equipment ", \
                              EquipmentName, " created.")
                TskEqpInst = TskEqp.TaskEquipment.getInstance(TskInst, EqpInst)
                if self.__Debug:
                    print(" Workpackage; parseWorkpackage: TskEqpInst:", \
                          TskEqpInst)
                if isinstance(TskEqpInst, TskEqp.TaskEquipment):
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: TaskStaff ", \
                              TskInst._TaskName, EqpInst._EquipName, " exists.")
                else:
                    TskEqpInst = TskEqp.TaskEquipment(TskInst, EqpInst)
                    if self.__Debug:
                        print(" WorkPackage; parseWorkpackage: TaskStaff ", \
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
                    print(" WorkPackage; parseWorkpackage: ", \
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
                    print(" WorkPackage; parseWorkpackage: Consumables")
                CnsCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    CnsCst = np.append(CnsCst,Cst)
                _ConsumeByYear = CnsCst
                _TotalConsume  = np.sum(_ConsumeByYear)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: ", \
                          "consumables cost by year and total:", \
                          _ConsumeByYear, _TotalConsume)
            elif str(self._wpParams.iat[i,0]) == "Travel":
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: Travel")
                TrvCst = np.array([])
                for iYr in range(len(Yrs)):
                    Cst = float(self._wpParams.iat[i,2+iYr])
                    if mt.isnan(Cst):
                        Cst = 0.
                    TrvCst = np.append(TrvCst,Cst)
                _TravelByYear = TrvCst
                _TotalTravel  = np.sum(_TravelByYear)
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: ", \
                          "travel cost by year and total:", \
                          _TravelByYear, _TotalTravel)
            elif str(self._wpParams.iat[i,0]) == "OtherNonStaff":
                OtherNonStaffItems.append(self._wpParams.iat[i,1])
                if self.__Debug:
                    print(" WorkPackage; parseWorkpackage: other non-staff: ",\
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
                    print(" WorkPackage; parseWorkpackage: consumables + ", \
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
                    print(" WorkPackage; parseWorkpackage: ", \
                          "Unprocessed ---->", self._wpParams.iloc[i,0])

        return PrjInst, WorkpackageName, WPM, Yrs, \
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
                for iYr in range(len(iTsk._StaffCostByYear)):
                    if not SumInitialised:
                        _StaffCostByYear     = \
                            np.append(_StaffCostByYear,   [0.])
                        _CGStaffCostByYear   = \
                            np.append(_CGStaffCostByYear, [0.])
                        _EquipmentCostByYear = \
                            np.append(_EquipmentCostByYear,   [0.])
                SumInitialised = True
                _StaffCostByYear += iTsk._StaffCostByYear
                _CGStaffCostByYear += iTsk._CGStaffCostByYear
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

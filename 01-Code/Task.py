#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Task:
===========

  Creates an instance of the Task class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the Task class.

      
  Instance attributes:
  --------------------
   _Name                = Name of task
   _WorkPackage         = Instance of WorkPackage task in which this task 
                          is defined
   _StaffCostByYear     = Total cost of staff in £k for this task by FY
   _CGStaffCostByYear   = Cost of CG staff in £k for this task by FY
   _TotalStaffCost      = Summed total staff cost over duration of project
                          (£k)
   _TotalStaffFrac      = Summed total FTE over duration of project (£k)
   _TotalCGStaffCost    = Summed total CG staff cost over duration of project 
                          (£k)
   _EquipmentCostByYear = Total cost of equipment in £k for this task by FY
   _TotalEquipCost      = Summed total equipment cost over duration of
                          project (£k)
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods:
      createCSV     : Creates CSV file containing Task paramters.
                      [Classmethod]
                      Input: Instance of Pandas dataframe class containing 
                             parameters
                             String -- path to output file (filename)


  Get/set methods:
    getInstance: Finds instance of class with Task._Name
                 Input: _Name -- str -- name of Project to be found
                Return: Instance of class; None if not found or if more than
                        one instance
                   [Classmethod]

    setStaffCostByYear: Set staff cost per year (£k)
      Input: numpy array
        
    setStaffFracByYear: Set staff frac per year (£k)
      Input: numpy array
        
    setCGStaffCostByYear: Set staff cost per year (£k)
      Input: numpy array

    setTotalStaffCost: Set total staff cost (£k)
        Sums staff cost per year.
        
    setTotalStaffFrac: Set total staff frac
        Sums staff FTE per year.
        
    setTotalCGStaffCost: Set total CG staff cost (£k)
        Sums CG staff cost per year.
        
    setEquipmentCostByYear: Set quipment cost per year (£k)
      Input: numpy array

    setTotalEquipmentCost: Set total equipment cost (£k)
        Sums equipment cost per year.


  Processing methods:
      createPandasDataframe : Create Pandas data frame containing Task
                              parameters.
                              [Classmethod]
                 Input: None.
                Return: Instance of Pandas class.

      clean: Delete incomplete instances of Task
             [classmethod]

      doCosting: Complete costing of Task.  Sums data from TaskStaff and
                 TaskEquipment related to Task and completes Task costing.
                 [Classmethod]

  
Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 19Jun21: First implementation

@author: kennethlong
"""

import numpy  as np
import pandas as pd
from operator import attrgetter

import WorkPackage   as wp
import TaskStaff     as TskStf
import TaskEquipment as TskEqp
import Progress      as Prg

class Task:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Name="None", _WPInst=None):

        self._Name        = _Name
        self._WorkPackage = _WPInst

        #.. Defined, but not filled, at init:
        self._StaffFracByYear     = None
        self._StaffCostByYear     = None
        self._CGStaffCostByYear   = None
        self._TotalStaffCost      = None
        self._TotalStaffFrac      = None
        self._TotalCGStaffCost    = None
        self._EquipmentCostByYear = None
        self._TotalEquipmentCost  = None
        
        Task.instances.append(self)
        
    def __repr__(self):
        return "Task(Name)"

    def __str__(self):
        print(" Task:", self._Name)
        print("     ----> WorkPackage:", self._WorkPackage._Name, " \n")
        print("     Staff frac by year:", self._StaffFracByYear)
        print("     Staff cost by year:", self._StaffCostByYear)
        print("     CG staff cost by year:", self._CGStaffCostByYear)
        print("     Total staff frac:", self._TotalStaffFrac)
        print("     Total staff cost:", self._TotalStaffCost)
        print("     Total CG staff cost:", self._TotalCGStaffCost)
        print("     Equipment cost by year:", self._EquipmentCostByYear)
        print("     Total equipment cost:", self._TotalEquipmentCost)
        return "     <---- Task complete."

    
#--------  I/o methods:
    @classmethod
    def createCSV(cls, _TskDataFrame, _filename):
        _TskDataFrame.to_csv(_filename)


#--------  Get/set methods:
    def getName(self):
        return self._Name
        
    def getWorkPackage(self):
        return self._WorkPackage
        
    @classmethod
    def getInstance(cls, _Name, _WPInst):
        InstList = []
        if Task.__Debug:
            print(" Task; getInstance: search for Task name, WP name:", \
                  _Name, _WPInst._Name)
        for inst in cls.instances:
            if Task.__Debug:
                print(" Task; getInstance: instances:", \
                      inst._Name, inst._WorkPackage._Name)
            if inst._Name == _Name and \
               inst._WorkPackage._Name == _WPInst._Name:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateTaskClassInstance(Ninst, "instances of ", _Name)

        if Task.__Debug:
            print(" Task; getInstance: number of instances; return instance:", \
                  Ninst, "\n ", RtnInst)

        return RtnInst

    def getTotalValue(self):
        TV = None
        if self._TotalStaffCost     != None and \
           self._TotalEquipmentCost != None:
            TV = self._TotalStaffCost + self._TotalEquipmentCost
        return TV

    def setStaffCostByYear(self, _StaffCostByYear):
        self._StaffCostByYear = _StaffCostByYear
        
    def setStaffFracByYear(self, _StaffFracByYear):
        self._StaffFracByYear = _StaffFracByYear
        
    def setCGStaffCostByYear(self, _CGStaffCostByYear):
        self._CGStaffCostByYear = _CGStaffCostByYear

    def setTotalStaffCost(self):
        self._TotalStaffCost = np.sum(self._StaffCostByYear)
        
    def setTotalStaffFrac(self):
        self._TotalStaffFrac = np.sum(self._StaffFracByYear)
        
    def setTotalCGStaffCost(self):
        self._TotalCGStaffCost = np.sum(self._CGStaffCostByYear)
        
    def setEquipmentCostByYear(self, _EquipmentCostByYear):
        self._EquipmentCostByYear = _EquipmentCostByYear

    def setTotalEquipmentCost(self):
        self._TotalEquipmentCost = np.sum(self._EquipmentCostByYear)
        

#--------  Processing methods:
    @classmethod
    def createPandasDataframe(cls):
        TaskData = []
        TaskData.append(["Name", \
                         "WorkPackage", \
                         "Staff cost by year (£k)", \
                         "Total staff cost (£k)", \
                         "CG staff cost per year (£k)", \
                         "Total CG staff cost (£k)", \
                         "Equipment cost by year (£k)", \
                         "Total equipment cost (£k)"])
        for inst in Task.instances:
            TaskData.append([inst._Name, \
                             inst._WorkPackage._Name, \
                             inst._StaffFracByYear, inst._TotalStaffFrac, \
                             inst._StaffCostByYear, inst._TotalStaffCost, \
                             inst._CGStaffCostByYear, inst._TotalCGStaffCost, \
                             inst._EquipmentCostByYear, \
                             inst._TotalEquipmentCost])
        TaskDataframe = pd.DataFrame(TaskData)
        if cls.__Debug:
            print(" Task; createPandasDataframe: \n", TaskDataframe)
        return TaskDataframe
    
    @classmethod
    def clean(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iTsk in OldInst:
            if not isinstance(iTsk._Name, str) or \
               not isinstance(iTsk._WorkPackage, wp.WorkPackage):
                del iTsk
                nDel += 1
            else:
                NewInst.append(iTsk)
        cls.instances = NewInst
        return nDel

    @classmethod
    def clear(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iTsk in OldInst:
            del iTsk
            nDel += 1
        cls.instances = NewInst
        return nDel

    @classmethod
    def doCosting(cls):
        for iTsk in cls.instances:
            _StaffFracByYear   = np.array([])
            _StaffCostByYear   = np.array([])
            _CGStaffCostByYear = np.array([])
            SumInitialised = False
            for iTskStf in TskStf.TaskStaff.instances:
                if iTskStf._Task == iTsk:
                    for iYr in range(len(iTskStf._StaffCostByYear)):
                        if not SumInitialised:
                            _StaffFracByYear   = \
                                np.append(_StaffFracByYear,   [0.])
                            _StaffCostByYear   = \
                                np.append(_StaffCostByYear,   [0.])
                            _CGStaffCostByYear = \
                                np.append(_CGStaffCostByYear, [0.])
                    SumInitialised = True
                    _StaffFracByYear += iTskStf._StaffFracByYear
                    _StaffCostByYear += iTskStf._StaffCostByYear
                    if iTskStf._Staff._ProjectOrCG == "CG":
                        _CGStaffCostByYear += iTskStf._StaffCostByYear
            iTsk._StaffFracByYear = _StaffFracByYear
            iTsk._StaffCostByYear = _StaffCostByYear
            iTsk.setTotalStaffFrac()
            iTsk.setTotalStaffCost()
            iTsk._CGStaffCostByYear = _CGStaffCostByYear

        for iTsk in cls.instances:
            _EquipmentCostByYear = np.array([])
            SumInitialised = False
            for iTskEqp in TskEqp.TaskEquipment.instances:
                if iTskEqp._Task == iTsk:
                    iEqp = iTskEqp._Equipment
                    for iYr in range(len(iEqp._EquipmentCostByYear)):
                        if not SumInitialised:
                            _EquipmentCostByYear   = \
                                np.append(_EquipmentCostByYear,   [0.])
                    SumInitialised = True
                    _EquipmentCostByYear += iEqp._EquipmentCostByYear
            iTsk.setEquipmentCostByYear(_EquipmentCostByYear)
            iTsk.setTotalEquipmentCost()


#--------  Exceptions:
class DuplicateTaskClassInstance(Exception):
    pass

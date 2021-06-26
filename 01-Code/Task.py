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

      
  Instance attributes:
  --------------------
   _TaskName            = Name of task
   _Workpackage         = Instance of Workpackage task in which this task is defined
   _StaffCostByYear     = Total cost of staff in £k for this task by FY
   _CGStaffCostByYear   = Cost of CG staff in £k for this task by FY
   _TotalStaffCost      = Summed total staff cost over duration of project (£k)
   _TotalCGStaffCost    = Summed total CG staff cost over duration of project (£k)
   _EquipmentCostByYear = Total cost of equipment in £k for this task by FY
   _TotalEquipCost      = Summed total equipment cost over duration of project (£k)
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.

  I/o methods:
      xx: 

  Get/set methods:
      getXX: 

  
Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 19Jun21: First implementation

@author: kennethlong
"""

import numpy  as np
import pandas as pd

import WorkPackage   as wp
import TaskStaff     as TskStf
import TaskEquipment as TskEqp

class Task:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _TaskName="None", _WPInst=None):
        Task.instances.append(self)
        self._TaskName    = _TaskName
        self._Workpackage = _WPInst

        #.. Defined, but not filled, at init:
        self._StaffCostByYear     = None
        self._CGStaffCostByYear   = None
        self._TotalStaffCost      = None
        self._TotalCGStaffCost    = None
        self._EquipmentCostByYear = None
        self._TotalEquipmentCost  = None
        
    def __repr__(self):
        return "Task(Name)"

    def __str__(self):
        print(" Task:", self._TaskName)
        print("     ----> Workpackage:", self._Workpackage._WorkpackageName, " \n")
        print("     Staff cost by year:", self._StaffCostByYear)
        print("     CG staff cost by year:", self._CGStaffCostByYear)
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
        

#--------  Print methods

#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        TaskData = []
        TaskData.append(["Name", "Workpackage", "Staff cost by year (£k)", "CG staff cost per year (£k)", \
                         "Total staff cost (£k)", "Total CG staff cost (£k)", \
                         "Equipment cost by year (£k)", "Total equipment cost (£k)"])
        for inst in Task.instances:
            TaskData.append([inst._TaskName, inst._Workpackage._WorkpackageName, \
                             inst._StaffCostByYear, inst._CGStaffCostByYear, inst._TotalStaffCost, inst._TotalCGStaffCost, \
                             inst._EquipmentCostByYear, inst._TotalEquipmentCost])
        TaskDataframe = pd.DataFrame(TaskData)
        if cls.__Debug:
            print(" Task; createPandasDataframe: \n", TaskDataframe)
        return TaskDataframe
    

#--------  Class methods:
    @classmethod
    def getInstance(cls, _TaskName):
        InstList = []
        if Task.__Debug:
            print(" Task; getInstance: search for Task name:", _TaskName)
        for inst in cls.instances:
            if Task.__Debug:
                print(" Task; getInstance: instance:", inst._TaskName)
            if inst._TaskName == _TaskName:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateTaskClassInstance(Ninst, "instances of ", _TaskName)
        if Task.__Debug:
            print(" Task; getInstance: number of instances; return instance:", Ninst, "\n ", RtnInst)
        return RtnInst


    @classmethod
    def clean(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iTsk in OldInst:
            if not isinstance(iTsk._TaskName, str) or not isinstance(iTsk._Workpackage, wp.WorkPackage):
                del iTsk
                nDel += 1
            else:
                NewInst.append(iTsk)
        cls.instances = NewInst
        return nDel

    @classmethod
    def doCosting(cls):
        """
        self._EquipmentCostByYear = None
        self._TotalEquipmentCost  = None
        """

        for iTsk in cls.instances:
            _StaffCostByYear   = np.array([])
            _CGStaffCostByYear = np.array([])
            SumInitialised = False
            for iTskStf in TskStf.TaskStaff.instances:
                if iTskStf._Task == iTsk:
                    for iYr in range(len(iTskStf._StaffCostByYear)):
                        if not SumInitialised:
                            _StaffCostByYear   = np.append(_StaffCostByYear,   [0.])
                            _CGStaffCostByYear = np.append(_CGStaffCostByYear, [0.])
                    SumInitialised = True
                    _StaffCostByYear += iTskStf._StaffCostByYear
                    if iTskStf._Staff._ProjectOrCG == "CG":
                        _CGStaffCostByYear += iTskStf._StaffCostByYear
            iTsk._StaffCostByYear = _StaffCostByYear
            iTsk.setTotalStaffCost()
            iTsk._CGStaffCostByYear = _CGStaffCostByYear

        for iTsk in cls.instances:
            _EquipmentCostByYear = np.array([])
            SumInitialised = False
            for iTskEqp in TskEqp.TaskEquipment.instances:
                if iTskEqp._Task == iTsk:
                    iEqp = iTskEqp._Equipment
                    for iYr in range(len(iEqp._EquipmentCost)):
                        if not SumInitialised:
                            _EquipmentCostByYear   = np.append(_EquipmentCostByYear,   [0.])
                    SumInitialised = True
                    _EquipmentCostByYear += iEqp._EquipmentCost
            iTsk._EquipmentCostByYear = _EquipmentCostByYear
            iTsk.setTotalEquipmentCost()

    
#--------  Exceptions:
class DuplicateTaskClassInstance(Exception):
    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Project:
==============

  Creates an instance of the Project class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out

      
  Instance attributes:
  --------------------
   _ProjectName         = Project name
   _StaffCostByYear     = Total cost of staff in £k for this workpackage by FY
   _CGStaffCostByYear   = Cost of CG staff in £k for this workpackage by FY
   _TotalStaffCost      = Summed total staff cost over duration of project (£k)
   _TotalCGStaffCost    = Summed total CG staff cost over duration of project (£k)
   _EquipmentCostByYear = Total cost of equipment in £k for this workpackage by FY
   _TotalEquipCost      = Summed total equipment cost over duration of project (£k)
   _TrvlCnsmCostByYear  = Travel and consumable cost in £k for this workpackage by FY
   _TotalTrvlCnsmCost   = Summed travel and consumable cost in £k for this workpackage

    
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
import pandas as pnds

import WorkPackage as WP

class Project:
    __Debug   = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _ProjectName="None"):
        Project.instances.append(self)
        self._ProjectName = _ProjectName

        #.. Defined, but not filled, at init:
        self._StaffCostByYear     = None
        self._CGStaffCostByYear   = None
        self._TotalStaffCost      = None
        self._TotalCGStaffCost    = None
        self._EquipmentCostByYear = None
        self._TotalEquipmentCost  = None
        self._TrvlCnsmCostByYear  = None
        self._TotalTrvlCnsmCost   = None


    def __repr__(self):
        return "Project(Name)"

    def __str__(self):
        _PrjName = self._ProjectName
        print(" Project: name:", _PrjName, " ---->")
        print("     Staff cost by year, total:", self._StaffCostByYear, self._TotalStaffCost)
        print("     CG staff cost by year, total:", self._CGStaffCostByYear, self._TotalCGStaffCost)
        print("     Equipment cost by year, total", self._EquipmentCostByYear, self._TotalEquipmentCost)
        print("     Travel and consumable cost by year, total:", self._TrvlCnsmCostByYear, self._TotalTrvlCnsmCost)
        return "     <---- Project done."

#--------  I/o methods:
    @classmethod
    def createCSV(cls, _PrjPckgDataFrame, _filename):
        _PrjPckgDataFrame.to_csv(_filename)

        
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

    def setTrvlCnsmCostByYear(self, _TrvlCnsmCostByYear):
        self._TrvlCnsmCostByYear = _TrvlCnsmCostByYear
        
    def setTotalTrvlCnsmCost(self):
        self._TotalTrvlCnsmCost = np.sum(self._TrvlCnsmCostByYear)

        
#--------  Print methods:

#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        ProjectData = []
        ProjectData.append(["Project", \
                            "Staff cost per year (£k)", "CG staff cost per year (£k)", \
                            "Total staff cost (£k)", "Total CG staff cost (£k)", \
                            "Equipment cost by year (£k)", "Total equipment cost (£k)", \
                            "Travel and consumables by year (£k)", "Total travel and consumables (£k)"])
        for inst in Project.instances:
            ProjectData.append([inst._ProjectName, \
                                inst._StaffCostByYear, inst._CGStaffCostByYear, inst._TotalStaffCost, inst._TotalCGStaffCost, \
                                    inst._EquipmentCostByYear, inst._TotalEquipmentCost, inst._EquipmentCostByYear, inst._TotalEquipmentCost])
        ProjectDataframe = pnds.DataFrame(ProjectData)
        if cls.__Debug:
            print(" Project; createPandasDataframe: \n", ProjectDataframe)
        return ProjectDataframe

    
#--------  Class methods:
    @classmethod
    def getInstance(cls, _ProjectName):
        InstList = []
        if Project.__Debug:
            print(" Project; getInstance: search for project name:", _ProjectName)
        for inst in cls.instances:
            if Project.__Debug:
                print(" Project; getInstance: instance:", inst._ProjectName)
            if inst._ProjectName == _ProjectName:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateProjectClassInstance(Ninst, "instances of ", _ProjectName)
        if Project.__Debug:
            print(" Project; getInstance: number of instances; return instance:", Ninst, "\n ", RtnInst)
        return RtnInst

    @classmethod
    def clean(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iPrj in OldInst:
            if not isinstance(iPrj._ProjectName, str):
                del iPrj
                nDel += 1
            else:
                NewInst.append(iPrj)
        cls.instances = NewInst
        return nDel

    @classmethod
    def doCosting(cls):
        for iPrj in cls.instances:
            _StaffCostByYear     = np.array([])
            _CGStaffCostByYear   = np.array([])
            _EquipmentCostByYear = np.array([])
            _TrvlCnsmCostByYear  = np.array([])
            SumInitialised = False
            for iWP in WP.WorkPackage.instances:
                for iYr in range(len(iWP._StaffCostByYear)):
                    if not SumInitialised:
                        _StaffCostByYear     = np.append(_StaffCostByYear,     [0.])
                        _CGStaffCostByYear   = np.append(_CGStaffCostByYear,   [0.])
                        _EquipmentCostByYear = np.append(_EquipmentCostByYear, [0.])
                        _TrvlCnsmCostByYear  = np.append(_TrvlCnsmCostByYear,  [0.])
                SumInitialised     = True
                _StaffCostByYear     += iWP._StaffCostByYear
                _CGStaffCostByYear   += iWP._CGStaffCostByYear
                _EquipmentCostByYear += iWP._EquipmentCostByYear
                _TrvlCnsmCostByYear  += iWP._TrvlCnsmCostByYear
            iPrj._StaffCostByYear = _StaffCostByYear
            iPrj.setTotalStaffCost()
            iPrj._CGStaffCostByYear = _CGStaffCostByYear
            iPrj.setTotalCGStaffCost()
            iPrj._EquipmentCostByYear = _EquipmentCostByYear
            iPrj.setTotalEquipmentCost()
            iPrj._TrvlCnsmCostByYear = _TrvlCnsmCostByYear
            iPrj.setTotalTrvlCnsmCost()


#--------  Exceptions:
class DuplicateProjectClassInstance(Exception):
    pass


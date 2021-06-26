#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class TaskStaff:
================

  Creates an instance of the TaskStaff class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out

      
  Instance attributes:
  --------------------
   _
    
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
 1.0: 20Jun21: First implementation

@author: kennethlong
"""

import numpy as np

import Task as Tsk
import Staff as Stff

class TaskStaff:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Staff=None):
        TaskStaff.instances.append(self)

        self._Task  = _Task
        self._Staff = _Staff

        #.. Defined, but not filled, at init:
        self._StaffFracByYrNQtr   = None
        self._StaffFracByYear     = None
        self._TotalStaffFrac      = None
        self._StaffCostByYear     = None
        self._TotalStaffCost      = None

        if TaskStaff.__Debug:
            print(" TaskStaff; __init__:"
                  "\n     Task:", self._Task, \
                  "\n     Staff:", self._Staff)

        if _Task == None or _Staff == None:
            raise NoTaskOrStaff(" TaskStaff; __init__: Task and/or staff undefined, execution terminated.")
        
        if not isinstance(_Task, Tsk.Task) or not isinstance(_Staff, Stff.Staff):
            raise NotAnInstanceOfTaskOrStaff(" TaskStaff; __init__: Task and/or staff not instance of class, execution terminated.")
        

    def __repr__(self):
        return "TaskStaff(Name)"

    def __str__(self):
        print(" TaskStaff: ---->")
        print(self._Task)
        print(self._Staff)
        print("    Staff fraction by year and quarter:", self._StaffFracByYrNQtr)
        print("    Staff fraction by year:", self._StaffFracByYear)
        print("    Tofal staff fraction:", self._TotalStaffFrac)
        print("    Staff cost by year:", self._StaffCostByYear)
        print("    Total staff cost:", self._TotalStaffCost)
        return " <---- TaskStaff: complete."

#--------  I/o methods:

#--------  Get/set methods:
    def setStaffFracByYrNQtr(self, _StaffFracByYrNQtr):
        self._StaffFracByYrNQtr = _StaffFracByYrNQtr
        
    def setStaffFracByYear(self):
        self._StaffFracByYear = np.average(self._StaffFracByYrNQtr, 1)
        
    def setTotalStaffFrac(self):
        self._TotalStaffFrac = np.sum(self._StaffFracByYear)

    def setStaffCostByYear(self):
        AnnualCost = self._Staff._AnnualCost
        self._StaffCostByYear = AnnualCost * self._StaffFracByYear

    def setTotalStaffCost(self):
        self._TotalStaffCost = np.sum(self._StaffCostByYear)
        

#--------  Print methods

#--------  Class methods:
    @classmethod
    def getInstance(cls, _Task, _Staff):
        InstList = []
        if TaskStaff.__Debug:
            print(" TaskStaff; getInstance: search for Task and Staff:", _Task._TaskName, _Staff._NameOrPost)
        for inst in cls.instances:
            if TaskStaff.__Debug:
                print(" TaskStaff; getInstance: instance Task, Staff:", _Task._TaskName, _Staff._NameOrPost)
            if inst._Task == _Task and inst._Staff == _Staff:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateTaskStaffClassInstance(Ninst, "instances of ", InstList[0])
        if TaskStaff.__Debug:
            print(" TaskStaff; getInstance: number of instances; return instance:", Ninst, "\n ", RtnInst)
        return RtnInst

    @classmethod
    def cleanTaskStaff(cls):
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iTskStf in OldInst:
            if not isinstance(iTskStf._Task, Tsk.Task) or not isinstance(iTskStf._Staff, Stff.Staff) or \
               not isinstance(iTskStf._StaffFracByYrNQtr, np.ndarray) or not isinstance(iTskStf._StaffFracByYear, np.ndarray) or \
               iTskStf._TotalStaffFrac == None:
                del iTskStf
                nDel += 1
            else:
                NewInst.append(iTskStf)
        cls.instances = NewInst
        return nDel

        
    @classmethod
    def doTaskStaffCosting(cls):
        for iTskStf in cls.instances:
            iTskStf.setStaffCostByYear()
            iTskStf.setTotalStaffCost()


#--------  Exceptions:
class DuplicateTaskStaffClassInstance(Exception):
    pass

class NoTaskOrStaff(Exception):
    pass

class NotAnInstanceOfTaskOrStaff(Exception):
    pass

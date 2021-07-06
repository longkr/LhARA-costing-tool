#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class TaskStaff:
================

  Creates an instance of the TaskStaff class and provides access methods
  to complete the attributes.  TaskStaff is a switchyard or pivot table
  relating tasks and staff.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the TaskEquipment class.


  Instance attributes:
  --------------------
     _Task                = Instance of Task class
     _Staff               = Instance of Staff class
     _StaffFracByYrNQtr   = Staff fraction by year and quarter
     _StaffFracByYear     = Staff fraction by year
     _TotalStaffFrac      = Tofal staff fraction
     _StaffCostByYear     = Staff cost by year (£k)
     _TotalStaffCost      = Total staff cost (£k)

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  Get/set methods:
      getInstance: Finds instance of class with specific Task and Staff
                   stored in the two instance attributes.
                 Input: _Task, _Equipment: Task and Project
                Return: Instance of class; None if not found or if more than
                        one instance
                   [Classmethod]

     setStaffFracByYrNQtr: Set staff fraction by year and quarter
                Input: numpy array
        
     setStaffFracByYear  : Set staff fraction by year
              Averages staff fraction by year and quarter
        
     setTotalStaffFrac   : Set totak stff fraction
              Sums staff fraction by year

     setStaffCostByYear  : Staff cost by year (£k)
                Cost per year calculated from staff fraction per year and 
                staff cost

     setTotalStaffCost   :
              Sums staff cost by year


  Processing method:
      clean: Delete incomplete instances of TaskStaff
             [classmethod]

      doCosting: Complete costing of TaskStaff.
                 [Classmethod]


  Exceptions:
     DuplicateTaskStaffClassInstance

     NoTaskOrStaff

     NotAnInstanceOfTaskOrStaff

  
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

        if _Task == None or _Staff == None or \
           not isinstance(_Task, Tsk.Task) or \
           not isinstance(_Staff, Stff.Staff):
            raise NoTaskOrStaff(" TaskStaff; __init__: ", \
                     "Task and/or staff undefined, execution terminated.")
        
        if not isinstance(_Task, Tsk.Task) or \
           not isinstance(_Staff, Stff.Staff):
            raise NotAnInstanceOfTaskOrStaff(" TaskStaff; __init__: ", \
           "Task and/or staff not instance of class, execution terminated.")

        self._Task  = _Task
        self._Staff = _Staff

        #.. Defined, but not filled, at init:
        self._StaffFracByYrNQtr   = None
        self._StaffFracByYear     = None
        self._TotalStaffFrac      = None
        self._StaffCostByYear     = None
        self._TotalStaffCost      = None

        TaskStaff.instances.append(self)
        if TaskStaff.__Debug:
            print(" TaskStaff; __init__:"
                  "\n     Task:", self._Task, \
                  "\n     Staff:", self._Staff)

    def __repr__(self):
        return "TaskStaff(Name)"

    def __str__(self):
        print(" TaskStaff: Task: ", self._Task._Name, \
              " from WP name: :", self._Task._Workpackage._Name, \
              "\n    Staff name: ", self._Staff._NameOrPost, \
              "\n    Fractions: ", self._StaffFracByYrNQtr, \
                           self._StaffFracByYear, self._TotalStaffFrac, \
              "\n    Costs: ", self._StaffCostByYear, self._TotalStaffCost)
        return "     <---- TaskStaff: complete."
    

#--------  Get/set methods:
    def setStaffFracByYrNQtr(self, _StaffFracByYrNQtr):
        self._StaffFracByYrNQtr = _StaffFracByYrNQtr
        
    def setStaffFracByYear(self):
        self._StaffFracByYear = np.average(self._StaffFracByYrNQtr, 1)
        
    def setTotalStaffFrac(self):
        self._TotalStaffFrac = np.sum(self._StaffFracByYear)

    def setStaffCostByYear(self):
        AnnualCost = self._Staff._AnnualCost
        StfFrcByYr = self._StaffFracByYear
        self._StaffCostByYear = AnnualCost * StfFrcByYr

    def setTotalStaffCost(self):
        self._TotalStaffCost = np.sum(self._StaffCostByYear)
        

#--------  Class methods:
    @classmethod
    def getInstance(cls, _Task, _Staff):
        InstList = []
        if TaskStaff.__Debug:
            print(" TaskStaff; getInstance: search for Task and Staff:", \
                  _Task._Name, _Staff._NameOrPost)
        for inst in cls.instances:
            if TaskStaff.__Debug:
                print(" TaskStaff; getInstance: instance Task, Staff:", \
                      _Task._Name, _Staff._NameOrPost)
            if inst._Task == _Task and inst._Staff == _Staff:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateTaskStaffClassInstance(Ninst, "instances of ", \
                                                  InstList[0])
        if TaskStaff.__Debug:
            print(" TaskStaff; getInstance: number of instances; ", \
                  " return instance:", \
                  Ninst, "\n ", RtnInst)
        return RtnInst

    @classmethod
    def clean(cls):
        if cls.__Debug:
            print(" TaskStaff: clean ----> start.")
        OldInst = cls.instances
        NewInst = []
        nDel    = 0
        for iTskStf in OldInst:
            if cls.__Debug:
                print(iTskStf)
            if not isinstance(iTskStf._Task, Tsk.Task) or \
               not isinstance(iTskStf._Staff, Stff.Staff) or \
               not isinstance(iTskStf._StaffFracByYrNQtr, np.ndarray) or \
               not isinstance(iTskStf._StaffFracByYear, np.ndarray) or \
               np.isnan(iTskStf._TotalStaffFrac) or \
               iTskStf._TotalStaffFrac == None:
                del iTskStf
                nDel += 1
                if cls.__Debug:
                    print("    ----> Delete!")
            else:
                if cls.__Debug:
                    print("    ----> Keep!")
                NewInst.append(iTskStf)
        cls.instances = NewInst
        return nDel

        
    @classmethod
    def doCosting(cls):
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

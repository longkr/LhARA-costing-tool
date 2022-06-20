#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This module provides Class:
    Progress

  Derived classes:
    PlannedValue
"""

"""
Class Progress:
===============

  Creates an instance of the Progress class and provides access methods
  to complete the attributes.

  Progress provides the instances and methods for earned-value
  analysis for the LhARA project.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the Progress class.

      
  Instance attributes:
  --------------------
   _Task                = Instance of Task class for which progress is
                          being recorded
   _Date                = Date as a date-time object
   _FractionComplete    = Fractional completion of task at _Date.
                          E.g. if 10% complete _FractionComplete = 0.1
   _Spend               = Spend (£k) to _Date

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods:


  Get/set methods:
    set: set 
      Input: numpy array
        
    get: get 
      Input: numpy array
        


  Processing methods:

  
Created on Wed 17Jun22. Version history:
----------------------------------------
 1.0: 17Jun22: First implementation

@author: kennethlong
"""

import datetime as DT

import Task  as Tsk


class Progress:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Date=None, \
                       _FractionComplete=None, _Spend=None):

        self.setTask(_Task)
        self.setDate(_Date)
        self.setFractionComplete(_FractionComplete)
        self.setSpend(_Spend)
                
        Progress.instances.append(self)
        
    def __repr__(self):
        return "Progress(Task, Date, FractionComplete, Spend)"

    def __str__(self):
        print(" Progress:", self.getTask()._Name)
        print("     Date            :", self.getDate())
        print("     FractionComplete:", self.getFractionComplete())
        print("     Spend           :", self.getSpend())
        return "  <---- Done."

    
#--------  I/o methods:


#--------  Get/set methods:
    def setTask(self, _Task):
        if not isinstance(_Task, Tsk.Task):
            raise ProgressTaskNotValid(" Progress.setTask: _Task " \
                                       "not an instance of Task class")
        self._Task = _Task
        
    def setDate(self, _Date):
        if not isinstance(_Date, DT.datetime):
            raise ProgressDateNotValid(" Progress.setDate: _Date " \
                                       "not an instance of datetime class")
        self._Date = _Date
        
    def setFractionComplete(self, _FractionComplete):
        if not isinstance(_FractionComplete, float):
            raise ProgressFractionCompleteNotValid( \
                                       " Progress.setFractionComplete: " \
                                       "_FractionComplete not a float")
        self._FractionComplete = _FractionComplete
        
    def setSpend(self, _Spend):
        if not isinstance(_Spend, float):
            raise ProgressSpendNotValid(" Progress.setSpend: _Spend " \
                                       "not a float")
        self._Spend = _Spend
        
    def getTask(self):
        return self._Task
        
    def getDate(self):
        return self._Date
        
    def getFractionComplete(self):
        return self._FractionComplete
        
    def getSpend(self):
        return self._Spend
        

#--------  Processing methods:

    
#--------  Exceptions:
class ProgressTaskNotValid(Exception):
    pass

class ProgressDateNotValid(Exception):
    pass

class ProgressFractionCompleteNotValid(Exception):
    pass

class ProgressSpendNotValid(Exception):
    pass

"""
Class PlannedValue:
===================

  Creates an instance of the PlannedValue class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the Progress class.

      
  Instance attributes:
  --------------------
   _Task         = Date as a date-time object
   _Date         = Date as a date-time object
   _PlannedValue = Fractional completion of task at _Date.

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods:


  Get/set methods:
    set: set 
      Input: numpy array
        
    get: get 
      Input: numpy array
        


  Processing methods:

  
Created on Wed 17Jun22. Version history:
----------------------------------------
 1.0: 120un22: First implementation

@author: kennethlong
"""

class PlannedValue(Progress):
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Date=None):

        self.setTask(_Task)
        self.setDate(_Date)
        self.setPlannedValue(None)
                
        PlannedValue.instances.append(self)
        
    def __repr__(self):
        return "PlannedValue(Task, Date)"

    def __str__(self):
        print(" PlannedValue:", self.getTask()._Name)
        print("     Date            :", self.getDate())
        print("     Planned value   :", self.getPlannedValue())
        return "  <---- Done."

    
#--------  I/o methods:


#--------  Get/set methods:
    def setPlannedValue(self, _PV):
        if not isinstance(_PV, float) and not (_PV is None):
            raise PlannedValuePVNotValid(\
                            " PlannedValue.setPlannedValue: " \
                                       "not valid.")
        self._PlannedValue = _PV
        
    def getPlannedValue(self):
        return self._PlannedValue
                

#--------  Processing methods:

    
#--------  Exceptions:
class PlannedValuePVNotValid(Exception):
    pass

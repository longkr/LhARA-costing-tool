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
    loadProgress: Reads progress CSV file and creates Progress, PV, 
                  instances as appropriate.
        Class method


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

import os
import datetime as DT
import pandas   as pnds

import Task  as Tsk
import WorkPackage as wp

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
    @classmethod
    def loadProgress(cls, _filename=None):
        if _filename == None:
            raise NoFilenameProvided( \
                'CSV filename required; execution termimated.')
        elif not os.path.isfile(_filename):
            raise NonExistantFile('CSV file' + _filename + \
                                  ' does not exist; execution termimated.')

        ProgParams = pnds.read_csv(_filename)
        iRow       = ProgParams.index
        # if cls.__Debug:
        print(" Progress.loadProgress: parse progress report")
        ProgList = ProgParams.values.tolist()
        iCnt = 0
        for i in iRow:
            iCnt += 1
            #if cls.__Debug:
            print("   ----> Parse row", iCnt, ProgList[iCnt-1])

            if ProgParams.iloc[i,0] == "Work package":
                #if cls.__Debug:
                print("     ----> Work package:", ProgParams.iloc[i,1])
                wpInst = None
                for wpInstIter in wp.WorkPackage.instances:
                    if wpInstIter._Name == ProgParams.iloc[i,1]:
                        #if cls.__Debug:
                        print("       ----> Identified:")
                    wpInst = wpInstIter
                if wpInst == None:
                    #if cls.__Debug:
                    print("       ----> Not identified!")
                

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

class NoFilenameProvided(Exception):
    pass

class NonExistantFile(Exception):
    pass

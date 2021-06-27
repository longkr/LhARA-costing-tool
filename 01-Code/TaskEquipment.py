#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class TaskEquipment:
====================

  Creates an instance of the TaskEquipment class and provides access methods
  to complete the attributes.  TaskEquipment is a switchyard or pivot table
  relating tasks and equipment.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the TaskEquipment class.

      
  Instance attributes:
  --------------------
     _Task      = Instance of Task class
     _Equipment = Instance of Equipment class

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  Print methods:
     print: Prints attributes of Task and Equipment instances.


  Get/set methods:
      getInstance: Finds instance of class with specific Task and Equipment
                   stored in the two instance attributes.
                 Input: _Task, _Equipment: Task and Project
                Return: Instance of class; None if not found or if more than
                        one instance
                   [Classmethod]


  Exceptions:
     DuplicateTaskEquipmentClassInstance:

     NoTaskOrEquipment:

     NotAnInstanceOfTaskOrEquipment:

  
Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 20Jun21: First implementation

@author: kennethlong
"""

import numpy  as np
import pandas as pd

import Task as Tsk
import Equipment as Eqp

class TaskEquipment:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Equipment=None):
        TaskEquipment.instances.append(self)

        self._Task  = _Task
        self._Equipment = _Equipment
        if TaskEquipment.__Debug:
            print(" TaskEquipment; __init__:"
                  "\n     Task:", self._Task, \
                  "\n     Equipment:", self._Equipment)

        if _Task == None or _Equipment == None:
            raise NoTaskOrEquipment(" TaskEquipment; __init__: ", \
                    "Task and/or staff undefined, execution terminated.")
        
        if not isinstance(_Task, Tsk.Task) or \
           not isinstance(_Equipment, Eqp.Equipment):
            raise NotAnInstanceOfTaskOrEquipment(" TaskEquipment; __init__: ", \
                              "Task and/or staff not instance of class, ", \
                              "execution terminated.")

    def __repr__(self):
        return "TaskEquipment(Name)"

    def __str__(self):
        print(" TaskEquipment:", self._Equipment._Name)
        print(self._Task)
        print(self._Equipment)
        return "     TaskEquipment summary complete."


#--------  Get/set methods:
    @classmethod
    def getInstance(cls, _Task, _Equip):
        InstList = []
        if TaskEquipment.__Debug:
            print(" TaskEquipment; getInstance: search for ",\
                  "TaskEquipment for Task:", _Task, " and Equipment:", \
                  _Equip)
        for inst in cls.instances:
            if TaskEquipment.__Debug:
                print(" TaskEquipment; getInstance: instance:", \
                      inst._Task, inst._Equipment)
            if inst._Task == _Task and inst._Equipment == _Equip:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateTaskEquipmentClassInstance(Ninst, \
                        "instances of ", InstList[0])
        if TaskEquipment.__Debug:
            print(" TaskEquipment; getInstance: number of instances; ", \
                  " return instance:", Ninst, "\n ", RtnInst)
        return RtnInst
    

#--------  Print methods
    @classmethod
    def print(cls):
        iTskEqp = 0
        for inst in TaskEquipment.instances:
            print(" TaskEquipment Id=", iTskEqp)
            print(inst._Task)
            print(inst._Equipment)
            iTskEqp += 1


#--------  Exceptions:
class DuplicateTaskEquipmentClassInstance(Exception):
    pass

class NoTaskOrEquipment(Exception):
    pass

class NotAnInstanceOfTaskOrEquipment(Exception):
    pass

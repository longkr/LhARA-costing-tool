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

           getHeader: Returns header for dump of equipment list
                [Class method]

             getLine: Returns line of equipment list as array of attibutes.

  getNumberOfInstances: Returns number of instances
                [Class method]


  Processing methods:
              clean: Remove invalid instances of class
                [Class method]


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
        if _Task == None or _Equipment == None:
            raise NoTaskOrEquipment(" TaskEquipment; __init__: ", \
                    "Task and/or staff undefined, execution terminated.")
        
        if not isinstance(_Task, Tsk.Task) or \
           not isinstance(_Equipment, Eqp.Equipment):
            raise NotAnInstanceOfTaskOrEquipment(" TaskEquipment; __init__: ", \
                              "Task and/or staff not instance of class, ", \
                              "execution terminated.")

        self._Task  = _Task
        self._Equipment = _Equipment
        if TaskEquipment.__Debug:
            print(" TaskEquipment; __init__:"
                  "\n     Task:", self._Task, \
                  "\n     Equipment:", self._Equipment)

        TaskEquipment.instances.append(self)

    def __repr__(self):
        return "TaskEquipment(Name)"

    def __str__(self):
        if not isinstance(self._Task, Tsk.Task):
            _TaskName = "Bad task"
        else:
            _TaskName = self._Task._Name
        if not isinstance(self._Equipment, Eqp.Equipment):
            _EqpName = "Bad equipment"
        else:
            _EqpName = self._Equipment._Name
        print(" TaskEquipment: Task: ", _TaskName, \
              ", equipment: ", _EqpName)
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
    
    @classmethod
    def getHeader(cls):
        _Header = " Task name, Equipment name"
        return _Header

    def getLine(self):
        _Line = []
        if not isinstance(self._Task, Tsk.Task):
            _Line.append("Bad task")
        else:
            _Line.append(self._Task._Name)
        if not isinstance(self._Equipment, Eqp.Equipment):
            _Line.append("Bad equipment")
        else:
            _Line.append(self._Equipment._Name)
        return _Line

    @classmethod
    def getNumberOfInstances(cls):
        return len(cls.instances)
    

#--------  Print methods
    @classmethod
    def print(cls):
        print(" Task-equipment list: \n",
              "====================")
        print(" ", cls.getHeader())
        for iTskEqp in cls.instances:
            print(" ", iTskEqp.getLine())


#--------  Processing methods:
    @classmethod
    def clean(cls):
        Deletions =[]
        for iTskEqp in cls.instances:
            if not isinstance(iTskEqp._Task, Tsk.Task):
                Deletions.append(iTskEqp)
            if not isinstance(iTskEqp._Equipment, Eqp.Equipment):
                Deletions.append(iTskEqp)
        
        if cls.__Debug:
            for i in range(len(Deletions)):
                print(" Task-equipment; clean: instances marked for ", \
                      "deletion: ", Deletions[i])

        OldInstances = cls.instances
        cls.instances = []
        for iTskEqp in OldInstances:
            try:
                i = Deletions.index(iTskEqp)
                del iTskEqp
            except ValueError:
                cls.instances.append(iTskEqp)

        return len(Deletions)


#--------  Exceptions:
class DuplicateTaskEquipmentClassInstance(Exception):
    pass

class NoTaskOrEquipment(Exception):
    pass

class NotAnInstanceOfTaskOrEquipment(Exception):
    pass

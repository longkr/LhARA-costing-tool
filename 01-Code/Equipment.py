#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Equipment:
===========

  Creates an instance of the Equipment class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out

      
  Instance attributes:
  --------------------
  _        = 

    
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

class Equipment:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _EquipmentName="None"):
        Equipment.instances.append(self)
        self._EquipmentName      = _EquipmentName
        self._EquipmentCost      = np.array([])
        self._TotalEquipmentCost = float("nan")

    def __repr__(self):
        return "Equipment(Name)"

    def __str__(self):
        print(" Equipment: \n     Equipment name:", self._EquipmentName)
        print("     Cost by financial year:", self._EquipmentCost)
        return "     Total cost: %g"%(self._TotalEquipmentCost)


#--------  I/o methods:
    @classmethod
    def createCSV(cls, _EqpDataFrame, _filename):
        _EqpDataFrame.to_csv(_filename)

        
#--------  Get/set methods:
    def setEquipmentCost(self, _EqpCost=None):
        self._EquipmentCost = _EqpCost
    
    def setTotalEquipmentCost(self):
        self._TotalEquipmentCost = np.sum(self._EquipmentCost)

        
#--------  Print methods

#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        EquipData = []
        EquipData.append(["Equipment", "Cost by financial year (£k)", "Total cost (£k)"])
        for inst in Equipment.instances:
            EquipData.append([inst._EquipmentName, inst._EquipmentCost, inst._TotalEquipmentCost])
        EquipDataframe = pd.DataFrame(EquipData)
        if cls.__Debug:
            print(" Equipment; createPandasDataframe: \n", EquipDataframe)
        return EquipDataframe
    
#--------  Class methods:
    @classmethod
    def getInstance(cls, _EquipmentName):
        InstList = []
        if Equipment.__Debug:
            print(" Equipment; getInstance: search for Equipment name:", _EquipmentName)
        for inst in cls.instances:
            if Equipment.__Debug:
                print(" Equipment; getInstance: instance:", inst._EquipmentName)
            if inst._EquipmentName == _EquipmentName:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateEquipmentClassInstance(Ninst, "instances of ", _EquipmentName)
        if Equipment.__Debug:
            print(" Equipment; getInstance: number of instances; return instance:", Ninst, "\n ", RtnInst)
        return RtnInst

#--------  Exceptions:
class DuplicateEquipmentClassInstance(Exception):
    pass

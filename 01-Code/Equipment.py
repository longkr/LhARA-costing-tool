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
  instances: List of instances if the Equipment class.
      
  Instance attributes:
  --------------------
    _Name                = Name of equipment
    _EquipmentCostByYear = Equipment cost by year (£k)
    _TotalEquipmentCost  = Sum of totak equipment cost (£k)
       __init__ fills name only and a defauld "name string" if no name 
       is given

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.

  I/o methods:
      createCSV: Creates CSV file containing Equipment paramters.
                 [Classmethod]
                 Input: Instance of Pandas dataframe class containing 
                        parameters
                        String -- path to output file (filename)
 
  Get/set methods:
      getInstance: Finds instance of class with Equipment._Name
                 Input: _Name -- str -- name of Project to be found
                Return: Instance of class; None if not found or if more than
                        one instance
                 [Classmethod]

     setEquipmentCost: Set equipment cost per year (£k).
               Input: numpy array
    
     setTotalEquipmentCost: Set total eqipment cost (£k).
               Sums equipment cost.

           getHeader: Returns header for dump of equipment list
                [Class method]

             getLine: Returns line of equipment list as array of attibutes.

  Print methods:
           print: Prints dump  of all instances
                [Class method]

  Processing methods:
      createPandasDataframe : Create Pandas data frame containing equiment
                              parameters.
                              [Classmethod]
                 Input: None.
                Return: Instance of Pandas class.


  Exceptions:
     DuplicateEquipmentClassInstance: 2 or more instances of this equipment

  
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
    def __init__(self, _Name="None"):
        if _Name == "None":
            _Name = " Equipment instance created with no content."
        self._Name                = _Name
        self._EquipmentCostByYear = np.array([])
        self._TotalEquipmentCost  = float("nan")

        Equipment.instances.append(self)

    def __repr__(self):
        return "Equipment(Name)"

    def __str__(self):
        print(" Equipment: \n     Equipment name:", self._Name)
        print("     Cost by financial year:", self._EquipmentCostByYear)
        return "     Total cost: %g"%(self._TotalEquipmentCost)


#--------  I/o methods:
    @classmethod
    def createCSV(cls, _EqpDataFrame, _filename):
        _EqpDataFrame.to_csv(_filename)

        
#--------  Get/set methods:
    def setEquipmentCost(self, _EqpCost=None):
        self._EquipmentCostByYear = _EqpCost
    
    def setTotalEquipmentCost(self):
        self._TotalEquipmentCost = np.sum(self._EquipmentCostByYear)

    @classmethod
    def getHeader(cls):
        _Header = " Name, Cost by year (£k), Total cost (£k)"
        return _Header

    def getLine(self):
        _Line = []
        _Line.append(self._Name)
        _Line.append(self._EquipmentCostByYear)
        _Line.append(self._TotalEquipmentCost)
        return _Line

    @classmethod
    def getInstance(cls, _Name):
        InstList = []
        if Equipment.__Debug:
            print(" Equipment; getInstance: search for Equipment name:", _Name)
        for inst in cls.instances:
            if Equipment.__Debug:
                print(" Equipment; getInstance: instance:", inst._Name)
            if inst._Name == _Name:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateEquipmentClassInstance(Ninst, "instances of ", _Name)
        if Equipment.__Debug:
            print(" Equipment; getInstance: number of instances; " \
                  "return instance:", Ninst, "\n ", RtnInst)
        return RtnInst
    
        
#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        EquipData = []
        EquipData.append(["Equipment", \
                          "Cost by financial year (£k)", \
                          "Total cost (£k)"])
        for inst in Equipment.instances:
            EquipData.append([inst._Name,
                              inst._EquipmentCostByYear, \
                              inst._TotalEquipmentCost])
        EquipDataframe = pd.DataFrame(EquipData)
        if cls.__Debug:
            print(" Equipment; createPandasDataframe: \n", EquipDataframe)
        return EquipDataframe
    
#--------  Print methods:
    @classmethod
    def print(cls):
        print(" Equipment list: \n",
              "===============")
        print(" ", cls.getHeader())
        for iEq in cls.instances:
            print(" ", iEq.getLine())


#--------  Processing methods:
    @classmethod
    def clean(cls):
        Deletions =[]
        for iEqp in cls.instances:
            if not isinstance(iEqp._Name, str):
                Deletions.append(iEqp)
            if iEqp._EquipmentCostByYear == np.array([]):
                Deletions.append(iEqp)
            elif np.isnan(iEqp._TotalEquipmentCost):
                Deletions.append(iEqp)
        
        if cls.__Debug:
            for i in range(len(Deletions)):
                print(" Equipment; clean: instances marked for ", \
                      "deletion: ", Deletions[i]._Name)

        OldInstances = cls.instances
        cls.instances = []
        for iEqp in OldInstances:
            try:
                i = Deletions.index(iEqp)
                del iEqp
            except ValueError:
                cls.instances.append(iEqp)

        return len(Deletions)
        

#--------  Exceptions:
class DuplicateEquipmentClassInstance(Exception):
    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class OtherNonStaff:
===========

  Creates an instance of the OtherNonStaff class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the OtherNonStaff class.
      
  Instance attributes:
  --------------------
    _Name                    = Name of non-staff item
    _OtherNonStaffCostByYear = OtherNonStaff cost by year (£k)
    _TotalOtherNonStaffCost  = Sum of total other non-staff cost (£k)
       __init__ fills name only and a default "name string" if no name 
       is given

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.

  I/o methods:
      createCSV: Creates CSV file containing OtherNonStaff paramters.
                 [Classmethod]
                 Input: Instance of Pandas dataframe class containing 
                        parameters
                        String -- path to output file (filename)
 
  Get/set methods:
      getInstance: Finds instance of class with OtherNonStaff._Name
                 Input: _Name -- str -- name of Project to be found
                Return: Instance of class; None if not found or if more than
                        one instance
                 [Classmethod]

     setOtherNonStaffCost: Set other non-staff cost per year (£k).
               Input: numpy array
    
     setTotalOtherNonStaffCost: Set total eqipment cost (£k).
               Sums other non-staff cost.

           getHeader: Returns header for dump of other non-staff list
                [Class method]

             getLine: Returns line of other non-staff list as array of attibutes.

  Print methods:
           print: Prints dump  of all instances
                [Class method]


  Processing methods:
      clean: Remove (delete) instances of class that are not valid.
                [Class method]

      createPandasDataframe : Create Pandas data frame containing other
                              non-staff parameters.
                              [Classmethod]
                 Input: None.
                Return: Instance of Pandas class.


  Exceptions:
     DuplicateOtherNonStaffClassInstance: 2 or more instances of this other 
     non-staff

  
Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 19Jun21: First implementation

@author: kennethlong
"""

import numpy  as np
import pandas as pd

class OtherNonStaff:
    __Debug = True
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Name="None"):
        if _Name == "None":
            _Name = " OtherNonStaff instance created with no content."
            
        self._Name                    = _Name
        self._OtherNonStaffCostByYear = np.array([])
        self._TotalOtherNonStaffCost  = float("nan")

        OtherNonStaff.instances.append(self)

    def __repr__(self):
        return "OtherNonStaff(Name)"

    def __str__(self):
        print(" OtherNonStaff: \n     OtherNonStaff name:", self._Name)
        print("     Cost by financial year:", self._OtherNonStaffCostByYear)
        return "     Total cost: %g"%(self._TotalOtherNonStaffCost)


#--------  I/o methods:
    @classmethod
    def createCSV(cls, _ONSDataFrame, _filename):
        _ONSDataFrame.to_csv(_filename)

        
#--------  Get/set methods:
    def setOtherNonStaffCost(self, _ONSCost=None):
        self._OtherNonStaffCostByYear = _ONSCost
    
    def setTotalOtherNonStaffCost(self):
        self._TotalOtherNonStaffCost = np.sum(self._OtherNonStaffCostByYear)

    @classmethod
    def getHeader(cls):
        _Header = " Name, Cost by year (£k), Total cost (£k)"
        return _Header

    def getLine(self):
        _Line = []
        _Line.append(self._Name)
        _Line.append(self._OtherNonStaffCostByYear)
        _Line.append(self._TotalOtherNonStaffCost)
        return _Line

    @classmethod
    def getInstance(cls, _Name):
        InstList = []
        if OtherNonStaff.__Debug:
            print(" OtherNonStaff; getInstance: search for OtherNonStaff name:",\
                  _Name)
        for inst in cls.instances:
            if OtherNonStaff.__Debug:
                print(" OtherNonStaff; getInstance: instance:", inst._Name)
            if inst._Name == _Name:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateOtherNonStaffClassInstance(Ninst, "instances of ", _Name)
        if OtherNonStaff.__Debug:
            print(" OtherNonStaff; getInstance: number of instances; " \
                  "return instance:", Ninst, "\n ", RtnInst)
        return RtnInst
    
        
#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        OthrNSData = []
        OthrNSData.append(["OtherNonStaff", \
                          "Cost by financial year (£k)", \
                          "Total cost (£k)"])
        for inst in OtherNonStaff.instances:
            OthrNSData.append([inst._Name,
                              inst._OtherNonStaffCostByYear, \
                              inst._TotalOtherNonStaffCost])
        OthrNSDataframe = pd.DataFrame(OthrNSData)
        if cls.__Debug:
            print(" OtherNonStaff; createPandasDataframe: \n", OthrNSDataframe)
        return OthrNSDataframe

    
#--------  Print methods:
    @classmethod
    def print(cls):
        print(" OtherNonStaff list: \n",
              "===============")
        print(" ", cls.getHeader())
        for iEq in cls.instances:
            print(" ", iEq.getLine())


#--------  Processing methods:
    @classmethod
    def clean(cls):
        Deletions =[]
        for iONS in cls.instances:
            if not isinstance(iONS._Name, str):
                Deletions.append(iONS)
            if iONS._OtherNonStaffCostByYear == np.array([]):
                Deletions.append(iONS)
            elif np.isnan(iONS._TotalOtherNonStaffCost):
                Deletions.append(iONS)
        
        if cls.__Debug:
            for i in range(len(Deletions)):
                print(" OtherNonStaff; clean: instances marked for ", \
                      "deletion: ", Deletions[i]._Name)

        OldInstances = cls.instances
        cls.instances = []
        for iONS in OldInstances:
            try:
                i = Deletions.index(iONS)
                del iONS
            except ValueError:
                cls.instances.append(iONS)

        return len(Deletions)
        

#--------  Exceptions:
class DuplicateOtherNonStaffClassInstance(Exception):
    pass

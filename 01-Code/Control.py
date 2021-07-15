#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Control:
==============

  Reads the constants that control the operation of the LhARA costing
  tool.  This class is a singleton class so that there is no ambiguity 
  about which values are in use.

  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
      
  Instance attributes:
  --------------------
   _
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of constants

  Get/set methods:

  
Created on Thu 31Dec20;16:42: Version history:
----------------------------------------------
 1.0: 14Jul21: First implementation

@author: kennethlong
"""

import os
import datetime
import pandas as pnds

class Control(object):
    __instance = None
    __Debug    = True

#--------  "Built-in methods":
    def __new__(cls, _filename):
        if _filename == None:
            raise NoFilenameProvided( \
                       'CSV filename required; execution termimated.')
        elif not os.path.isfile(_filename):
            raise NonExistantFile('CSV file' + \
                                  _filename + \
                                  ' does not exist; execution termimated.')

        if cls.__instance is None:
            cls.__instance = super(Control, cls).__new__(cls)
        
        cls._filename = _filename

        #.. Set defaults:
        cls._CntrlParams       = cls.getControls(_filename)
        cls._IssueDate         = None
        cls._Inflation         = None
        cls._VAT               = None
        cls._WorkingMargin     = None
        cls._Contingency       = None
        cls._fecChargeFraction = None

        cls._cntrlParams = cls.getControls(_filename)
        if cls.__Debug:
            print(" Control: control parameters: \n", \
                  cls._cntrlParams)

        cls._IssueDate, \
            cls._Inflation, \
            cls._VAT, \
            cls._WorkingMargin, \
            cls._Contingency, \
            cls._fecChargeFraction = cls.parseControl()
        
        return cls.__instance

    def __repr__(self):
        return " Control(<filename>)"

    def __str__(self):
        print(" Control paramters:")
        print("          Issue date:", self._IssueDate)
        print("           Inflation:", self._Inflation)
        print("                 VAT:", self._VAT)
        print("       WorkingMargin:", self._WorkingMargin)
        print("         Contingency:", self._Contingency)
        print(" FEC charge fraction:", self._fecChargeFraction)
        return "     <---- Done."

#--------  I/o methods:
    @classmethod
    def getControls(cls, _filename):
        CntrlParams = pnds.read_csv(_filename)
        return CntrlParams

    
#--------  Extracting data from the WorkPackage pandas dataframe:
    @classmethod
    def parseControl(cls):
        Rows = cls._cntrlParams.index
        for i in Rows:
            if cls.__Debug:
                print(" Control: parseControl: processing flag: ", \
                      cls._cntrlParams.iat[i,0])
            if cls._cntrlParams.iat[i,0] == "Issue date":
                DateTime = datetime.datetime.strptime( \
                            cls._cntrlParams.iat[i,1], "%d-%b-%y").date()
            elif cls._cntrlParams.iat[i,0].find("Inflation") >= 0:
                Inflation = []
                Inflation.append( \
                      float(cls._cntrlParams.iat[i,1].strip("%")) / 100. )
                Inflation.append( \
                      float(cls._cntrlParams.iat[i,2].strip("%")) / 100.)
                Inflation.append(float(cls._cntrlParams.iat[i,3]))
            elif cls._cntrlParams.iat[i,0].find("VAT") >= 0:
                VAT = float(cls._cntrlParams.iat[i,1].strip("%")) / 100.
            elif cls._cntrlParams.iat[i,0].find("WorkingMargin") >= 0:
                WorkingMargin = \
                    float(cls._cntrlParams.iat[i,1].strip("%")) / 100.
            elif cls._cntrlParams.iat[i,0].find("Contingency") >= 0:
                Contingency = []
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,1].strip("%")) / 100. )
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,2].strip("%")) / 100.)
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,3].strip("%")) / 100.)
            elif cls._cntrlParams.iat[i,0].find("fEC") >= 0:
                fEC = []
                fEC.append( \
                      float(cls._cntrlParams.iat[i,1].strip("%")) / 100. )
                fEC.append( \
                      float(cls._cntrlParams.iat[i,2].strip("%")) / 100.)
            else:
                print(cls._cntrlParams.iat[i,0], cls._cntrlParams.iat[i,1], \
                      cls._cntrlParams.iat[i,2], cls._cntrlParams.iat[i,2] )
                print(DateTime)

        return DateTime, Inflation, VAT, WorkingMargin, Contingency, fEC

#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    def CdVrsn(self):
        return 1.0

    def PDGref(self):
        return "P.A. Zyla et al. (Particle Data Group), Prog. Theor. Exp. Phys. 2020, 083C01 (2020)."
    
    def mass(self):
        return 105.6583745

    def lifetime(self):
        return 2.1969811E-6

    def Michel(self):
        return [0.75, 0.0, 0.75]

    def SoL(self):
        return 299792458.

#--------  Utilities:
    def print(self):
        print("Control: version:", self.CdVrsn())
        print("Control: PDG reference:", self.PDGref())
        print("Control: mass (MeV):", self.mass())
        print("Control: lifetime (s):", self.lifetime())
        print("Control: SM Michel parameters [rho, eta, delta]:", self.Michel())
        print("Control: speed of light (m/s):", self.SoL())
        

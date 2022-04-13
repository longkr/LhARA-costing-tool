
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
   __filename  : Filename from which parameters have been read.  If None
                 then default values are used.
   _CntrlParams: Pandas data frame instance containing parameters
   _IssueDate         = date.today(); i.e. date when reports etc. are
                        generated 
   _Inflation         = Equipment, Staff, year to start inflation calculation
   _VAT               = VAT charge rate
   _WorkingMargin     = Working margin (fraction), year to start addition of WM
   _Contingency       = Contingency (fraction) equipment, project
                        staff, CG staff, year to start addition of contingency
   _fecChargeFraction = fEC charge fraction on staff, project, CG
    

  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of constants


  Get/set methods:   <-------- believed to be "self documenting"!
     getIssueDate
        
     getInflationCapital
        
     getInflationStaff
        
     getInflationStrtInYr
        
     getVAT
        
     getWorkingMargin
        
     getContingencyMaterial
        
     getContingencyStaffPrj
        
     getContingencyStaffCG

     getfecChargeFractionPrj
        
     getfecChargeFractionCG

  Print methods:
     print: Prints control flag settings



  
Created on Thu 31Dec20;16:42: Version history:
----------------------------------------------
 1.1: 13Sep22: Udated to allow WM, contingency to start in year n
 1.0: 14Jul21: First implementation

@author: kennethlong
"""

import os
import copy
import datetime
import pandas as pnds
from datetime import date

class Control(object):
    __instance = None
    __Debug    = False

#--------  "Built-in methods":
    def __new__(cls, _filename=None):
        if cls.__instance is None:
            cls.__instance = super(Control, cls).__new__(cls)
        
            if _filename == None:
                if  Control.__Debug:
                    print(" Control: no filename provided, take defaults.")
            elif not os.path.isfile(_filename):
                print(" Control: file ", _filename, " does not exist.", \
                      " Raising exception")
                raise NonExistantFile('CSV file' + \
                                      _filename + \
                                      ' does not exist; execution termimated.')

            #.. Set defaults:
            cls._filename          = _filename
            cls._IssueDate         = date.today()
            cls._Inflation         = [0.01, 0.02, 1]
            cls._VAT               = 0.2
            cls._WorkingMargin     = [0.1, 1]
            cls._Contingency       = [0.2, 0.3, 0.4, 1]
            cls._fecChargeFraction = [0.8, 0.8]
            cls._CntrlParams       = None

            #.. Parse control file:
            if _filename != None:
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
        print("                                             Issue date:", \
              self._IssueDate)
        print("                Inflation(capital, staff, start in year:", \
              self._Inflation)
        print("                                                    VAT:", \
              self._VAT)
        print("                          Working margin, start in year:", \
              self._WorkingMargin)
        print(" Contingency (capital, prj stff, CG stff, start in year:", \
              self._Contingency)
        print("                                    FEC charge fraction:", \
              self._fecChargeFraction)
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
                iDm1 = int(cls._cntrlParams.iat[i,3])
                IDm2 = max(0, iDm1-1)
                Inflation.append(IDm2)
                
                
            elif cls._cntrlParams.iat[i,0].find("VAT") >= 0:
                VAT = float(cls._cntrlParams.iat[i,1].strip("%")) / 100.
            elif cls._cntrlParams.iat[i,0].find("WorkingMargin") >= 0:
                WorkingMargin = []
                WorkingMargin.append( \
                    float(cls._cntrlParams.iat[i,1].strip("%")) / 100.)
                WorkingMargin.append(int(cls._cntrlParams.iat[i,2]))
            elif cls._cntrlParams.iat[i,0].find("Contingency") >= 0:
                Contingency = []
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,1].strip("%")) / 100. )
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,2].strip("%")) / 100.)
                Contingency.append( \
                      float(cls._cntrlParams.iat[i,3].strip("%")) / 100.)
                Contingency.append(int(cls._cntrlParams.iat[i,4]))
            elif cls._cntrlParams.iat[i,0].find("fEC") >= 0:
                fEC = []
                fEC.append( \
                      float(cls._cntrlParams.iat[i,1].strip("%")) / 100. )
                fEC.append( \
                      float(cls._cntrlParams.iat[i,2].strip("%")) / 100.)
            else:
                print("    ----> Control.parseControl: ", \
                      " unprocessed control field:", \
                      cls._cntrlParams.iat[i,0], cls._cntrlParams.iat[i,1], \
                      cls._cntrlParams.iat[i,2], cls._cntrlParams.iat[i,2] )

        return DateTime, Inflation, VAT, WorkingMargin, Contingency, fEC


#--------  "Get methods" only
    def getIssueDate(self):
        return self._IssueDate
        
    def getInflationCapital(self):
        return self._Inflation[0]
        
    def getInflationStaff(self):
        return self._Inflation[1]
        
    def getInflationStrtInYr(self):
        return self._Inflation[2]
        
    def getVAT(self):
        return self._VAT
        
    def getWorkingMargin(self):
        return self._WorkingMargin[0]
        
    def getWorkingMarginStrtInYr(self):
        return self._WorkingMargin[1]
        
    def getContingencyMaterial(self):
        return self._Contingency[0]
        
    def getContingencyStaffPrj(self):
        return self._Contingency[1]
        
    def getContingencyStaffCG(self):
        return self._Contingency[2]

    def getContingencyStrtInYr(self):
        return self._Contingency[3]

    def getfecChargeFractionPrj(self):
        return self._fecChargeFraction[0]
        
    def getfecChargeFractionCG(self):
        return self._fecChargeFraction[1]
        
    
#--------  Print methods:
    def print(self):
        print(" Control paramters:")
        print("                                                 Issue date:", \
              self.getIssueDate())
        print("                   Inflation; capital, staff, start in year:", \
              self.getInflationCapital(), self.getInflationStaff(), \
              self.getInflationStrtInYr())
        print("                                                        VAT:", \
              self.getVAT())
        print("                              Working margin, start in year:", \
              self.getWorkingMargin(), self.getWorkingMarginStrtInYr())
        print(" Contingency; material, staff (project & CG), start in year:", \
              self.getContingencyMaterial(), \
              self.getContingencyStaffPrj(), \
              self.getContingencyStaffCG(),  \
              self.getContingencyStrtInYr() )
        print("                           FEC charge fraction; project, CG:", \
              self.getfecChargeFractionPrj(), \
              self.getfecChargeFractionCG() )
        return "     <---- Done."

#--------  Exceptions:
class NonExistantFile(Exception):
    pass

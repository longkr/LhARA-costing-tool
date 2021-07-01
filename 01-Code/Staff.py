#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Staff:
===========

  Creates an instance of the Staff class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out

      
  Instance attributes:
  --------------------
   _filename      = File from which staff information was read
   _StaffCode     = Staff code
   _NameOrPost    = Name or post
   _InstituteCode = Institute code (e.g. Imperial-Physics)
   _Post          = Post name (e.g. post doc)
   _GradeOrLevel  = Grade of level (e.g. Senior Lecturer)
   _AnnualCost    = Total FEC per year
   _ProjectOrCG   = Charged to "Project" or Consolidated Grant
   _Comments      = Free format string field; additional information (e.g. WAG)

    
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

import os as os
import pandas as pnds

class Staff:
    __Debug = True
    instances = []

#--------  "Built-in methods":
    def __init__(self, _StaffCode=None, _NameOrPost=None, _filename=None, \
                       _InstituteCode=None, _GradeOrLevel=None, _AnnualCost=float("nan"), _ProjectOrCG=None, _Comments="None"):

        self._StaffCode  = _StaffCode
        self._NameOrPost = _NameOrPost
        self._filename  = _filename

        if _NameOrPost == "None" or _NameOrPost == None:
            raise NoStaffName(" Staff.__init__: no staff name ==> execution terminated")

        if _filename != None and not os.path.isfile(_filename):
            print(" Staff.__init__: staff database file does not exist, create dummy entry for staff name=", _NameOrPost)
        
        if _filename == None:
            self._InstituteCode = "Institute-Code"
            self._GradeOrLevel  = "Head of House"
            self._AnnualCost    = 400.
            self._ProjectOrCG   = "Project"
            self._Comments      = "Default values filled; staff member not in staff database"
        else:
            self._InstituteCode = _InstituteCode
            self._GradeOrLevel  = _GradeOrLevel
            self._AnnualCost    = _AnnualCost
            self._ProjectOrCG   = _ProjectOrCG
            self._Comments      = _Comments

        Staff.instances.append(self)

    def __repr__(self):
        return "Staff(Name)"

    def __str__(self):
        _filename = self._filename
        if self._filename == None:
            _filename = "None"
        _AnnualCost = self._AnnualCost
        if self._AnnualCost == None:
            _AnnualCost = -100.
        return "Staff: Staff=%s, filename=%s, staff code=%s, institute=%s, grade=%s, cost=%g, source=%s, comment=%s"% \
                (self._NameOrPost, _filename, self._StaffCode, self._InstituteCode, self._GradeOrLevel, \
                self._AnnualCost, self._ProjectOrCG, self._Comments)

#--------  Get/set methods:
    def setAnnualCost(self, _AnnCost=None):
        self._AnnualCost = _AnnCost

    @classmethod
    def getNumberOfStaff(self):
        return len(self.instances)


#--------  Creating the pandas dataframe:
    @classmethod
    def createPandasDataframe(cls):
        StaffData = []
        StaffData.append(["Staff code", "Name or post", "Filename", "institute code", "Grade", "Annnual cost", "Funding source", "Comment"])
        for inst in Staff.instances:
            StaffData.append([inst._StaffCode, inst._NameOrPost, inst._filename, inst._InstituteCode, inst._GradeOrLevel, inst._AnnualCost, inst._ProjectOrCG, inst._Comments])
        StaffDataframe = pnds.DataFrame(StaffData)
        if cls.__Debug:
            print(" Staff; createPandasDataframe: \n", StaffDataframe)
        return StaffDataframe

    
#--------  Class methods:
    @classmethod
    def getInstance(cls, _NameOrPost):
        InstList = []
        if Staff.__Debug:
            print(" Staff; getInstance: search for Staff name:", _NameOrPost)
        for inst in cls.instances:
            if Staff.__Debug:
                print(" Staff; getInstance: instance:", inst._NameOrPost)
            if inst._NameOrPost == _NameOrPost:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateStaffClassInstance(Ninst, "instances of ", _NameOrPost)
        if Staff.__Debug:
            print(" Staff; getInstance: number of instances; return instance:", Ninst, "\n ", RtnInst)
        return RtnInst

    @classmethod
    def parseStaffDatabase(cls, filename=None):

        if filename == None:
            raise NoStaffDataBaseFile(" Staff.parseStaffDatabase: no file name given, execution terminated.")
        elif not os.path.isfile(filename):
            raise StaffDataBaseFileDNE(" Staff.parseStaffDatabase: staff database file does not exist, execution terminated.")

        _StffDtbsParams = cls.getStaffDatabase(filename)
        if cls.__Debug:
            xDummy = cls.printStaffDatabase(_StffDtbsParams)

        iRow = _StffDtbsParams.index
        for i in iRow:
            InstituteCode = _StffDtbsParams.iat[i,0]
            StaffCode     = _StffDtbsParams.iat[i,1]
            NameOrPost    = _StffDtbsParams.iat[i,2]
            GradeOrLevel  = _StffDtbsParams.iat[i,3]
            AnnualCost    = _StffDtbsParams.iat[i,4]
            ProjectOrCG   = _StffDtbsParams.iat[i,5]
            Comments      = _StffDtbsParams.iat[i,6]
            StffDummy     = Staff(StaffCode, NameOrPost, filename, \
                                  InstituteCode,GradeOrLevel, AnnualCost, ProjectOrCG, Comments)

        return len(cls.instances)

    @classmethod
    def getStaffDatabase(cls, _filename):
        StffDBParams = pnds.read_csv(_filename)
        return StffDBParams

    @classmethod
    def printStaffDatabase(cls, _StffDtbsParams):
        print(_StffDtbsParams)

    @classmethod
    def createCSV(cls, _StfDataFrame, _filename):
        _StfDataFrame.to_csv(_filename)

    @classmethod
    def cleanStaffDatabase(cls):
        ErrorCode = 0
        Deletions =[]
        for iStf in cls.instances:
            if not isinstance(iStf._StaffCode, str):
                Deletions.append(iStf)
            if not isinstance(iStf._NameOrPost, str):
                Deletions.append(iStf)
            elif not isinstance(iStf._InstituteCode, str):
                print(Deletions)
            elif not isinstance(iStf._GradeOrLevel, str):
                Deletions.append(iStf)
            elif not isinstance(iStf._AnnualCost, float):
                Deletions.append(iStf)
            elif not isinstance(iStf._ProjectOrCG, str):
                Deletions.append(iStf)
        
        if cls.__Debug:
            for i in range(len(Deletions)):
                print(" Staff; cleanStaffDatabase: instances marked for deletion: ", Deletions[i]._NameOrPost)

        OldInstances = cls.instances
        cls.instances = []
        for iStf in OldInstances:
            try:
                i = Deletions.index(iStf)
                del iStf
            except ValueError:
                cls.instances.append(iStf)

        return len(Deletions)
                
        
#--------  Exceptions:
class DuplicateStaffClassInstance(Exception):
    pass

class NoStaffName(Exception):
    pass

class NoStaffDataBaseFile(Exception):
    pass

class StaffDataBaseFileDNE(Exception):
    pass

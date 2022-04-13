#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Staff:
===========

  Creates an instance of the Staff class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug   : Boolean: set for debug print out
  instances : List of instances if the WorkPackage class.
  institutes: List of institutes contributing staff
      
  Instance attributes:
  --------------------
   _StaffCode     = Staff code (defined in consulation with institute)
   _NameOrPost    = Name or post
   _filename      = File from which staff information was read
   _InstituteCode = Institute code (e.g. Imperial-Physics)
   _GradeOrLevel  = Grade of level (e.g. Senior Lecturer)
   _AnnualCost    = Total FEC per year
   _ProjectOrCG   = Charged to "Project" or Consolidated Grant ("CG")
   _Comments      = Free format string field; additional information 
                    (e.g. WAG)

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of attributes.

  I/o and data-constructor methods:
      parseStaffDatabase: Read staff database CSV file and create Staff
                          instances.
                     Input: Path to CSV file containing staff database.
                    Return: Number of staff instances
                     [Class method]

        getStaffDatabase: Uses pandas to create pandas dataframe from
                          CSV file.  Called from parseStaffDatabase.
                     Input: Path to CSV file containing staff database.
                    Return: Pandas dataframe instance containing staff 
                            data base
                     [Class method]

   createPandasDataframe: Creates pandas data frame from instances of
                          Staff.
                      Return: Pandas dataframe instance
                     [Class method]

               createCSV: Creates CSV file from pandas dataframe.
                       Inputs: Pandas dataframe instance
                               Path to output file


  Get/set methods:
      setAnnualCost: Set self._AnnualCost
                 Input: Annual cost (float); defaults to float(nan))

   getNumberOfStaff: Returns integer length of instances, i.e. number of 
                     staff.
                     [Class method]

        getInstance: Finds instance of Staff, addressed by "NameOrPost"/
                  Input: Str: NameOrPost
                 Return: Instance of Staff class if it exists.  Returns "None" 
                         if NameOrPost is not found or there is more than one 
                         instance with the same name or post.
                     [Class method]

          getHeader: Return string list containing column headers.
                     [Class method]

            getData: Return string list containing staff data entries.

  
  Print methods:
    printStaffDatabase: Prints pandas dataframe containing the StaffDatabase
                     [Class method]

  Processing methods:
    cleanStaffDatabase: Parse all instances of Staff and remove those with 
                        invalid values in the attributes.
                Return: Number of staff entries remaining
                     [Class method]


  Exceptions:
        DuplicateStaffClassInstance: Two instances with same NameOrPost found.

                        NoStaffName: NameOrStaff not found.

                NoStaffDataBaseFile: Staff database file not found at read.


Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 19Jun21: First implementation

@author: kennethlong
"""

import os     as os
import pandas as pnds
import math   as mth

class Staff:
    __Debug    = False
    instances  = []
    institutes = []

#--------  "Built-in methods":
    def __init__(self, _StaffCode=None, _NameOrPost=None, _filename=None, \
                       _InstituteCode=None, _GradeOrLevel=None, \
                       _AnnualCost=float("nan"), _ProjectOrCG=None, \
                       _Comments="None"):

        self._StaffCode  = _StaffCode
        self._NameOrPost = _NameOrPost
        self._filename  = _filename

        if _NameOrPost == "None" or _NameOrPost == None or \
           _StaffCode  == "None" or _StaffCode  == None:
            raise NoStaffName(" Staff.__init__: no staff name ", \
                              "==> execution terminated")

        if _filename != None and not os.path.isfile(_filename):
            print(" Staff.__init__: staff database file does not ", \
                  "exist, create new/dummy entry for staff name=", _NameOrPost)
        
        if _InstituteCode == None:
            _InstituteCode = "Institute-Code"

        if _GradeOrLevel == None:
            _GradeOrLevel = "Head of House"

        if mth.isnan(_AnnualCost):
            _AnnualCost    = 100.

        if _ProjectOrCG == None:
            _ProjectOrCG   = "Project"

        if _Comments == "None":
            _Comments = "Dummy comment: default values filled; " \
                 + "staff member not read from staff database"

        self._InstituteCode = _InstituteCode
        self._GradeOrLevel  = _GradeOrLevel
        self._AnnualCost    = _AnnualCost
        self._ProjectOrCG   = _ProjectOrCG
        self._Comments      = _Comments

        if not (_InstituteCode in Staff.institutes):
            Staff.institutes.append(_InstituteCode)

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
        print("Staff (name or post):", self._NameOrPost)
        if self.__Debug:
            print("     File name: ", _filename)
        else:
            dirname,   basename   = os.path.split(_filename)
            dirname1,  subdirname = os.path.split(dirname)
            print("    File name: ", subdirname + "/" + basename)
        print("    Staff code:", self._StaffCode, \
              "; Institute code:", self._InstituteCode, \
              "; Grade or level:", self._GradeOrLevel, \
              "; Annual FEC:", _AnnualCost, \
              "; Project or CG:", self._ProjectOrCG)
        return "    Comments: %s"%(self._Comments)

    
#--------  I/o and data-constructor methods:
    @classmethod
    def parseStaffDatabase(cls, filename=None):

        if filename == None:
            raise NoStaffDataBaseFile(" Staff.parseStaffDatabase: \
                         no file name given, execution terminated.")
        elif not os.path.isfile(filename):
            raise StaffDataBaseFileDNE(" Staff.parseStaffDatabase: \
                   staff database file ", filename, \
                   " does not exist, execution terminated.")

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
                                  InstituteCode,GradeOrLevel, AnnualCost, \
                                  ProjectOrCG, Comments)

        return len(cls.instances)

    @classmethod
    def getStaffDatabase(cls, _filename):
        StffDBParams = pnds.read_csv(_filename)
        return StffDBParams

    @classmethod
    def createPandasDataframe(cls):
        StaffData = []
        StaffData.append(cls.getHeader())
        for inst in Staff.instances:
            StaffData.append(inst.getData())
        StaffDataframe = pnds.DataFrame(StaffData)
        if cls.__Debug:
            print(" Staff; createPandasDataframe: \n", StaffDataframe)
        return StaffDataframe

    @classmethod
    def createCSV(cls, _StfDataFrame, _filename):
        _StfDataFrame.to_csv(_filename)


#--------  Get/set methods:
    def setAnnualCost(self, _AnnCost=float("nan")):
        self._AnnualCost = _AnnCost

    @classmethod
    def getNumberOfStaff(cls):
        return len(cls.instances)

    @classmethod
    def getInstance(cls, _InstCode, _StaffCode):
        InstList = []
        if Staff.__Debug:
            print(" Staff; getInstance: search for InstCode, StaffCode:", _InstCode, _StaffCode)
        for inst in cls.instances:
            if Staff.__Debug:
                print(" Staff; getInstance: instance:", inst._InstituteCode, inst._StaffCode)
            if inst._InstituteCode == _InstCode and inst._StaffCode == _StaffCode:
                InstList.append(inst)
        Ninst = len(InstList)
        if Ninst == 0:
            RtnInst = None
        if Ninst == 1:
            RtnInst = InstList[0]
        if Ninst >= 2:
            RtnInst = None
            raise DuplicateStaffClassInstance(Ninst, "instances of ", \
                                              _StaffCode)
        if Staff.__Debug:
            print(" Staff; getInstance: number of instances; ", \
                  "return instance:", Ninst, "\n ", RtnInst)
        return RtnInst

    @classmethod
    def getHeader(cls):
        HeaderList = ["Staff code", "Name or post", "Filename", \
                      "institute code", "Grade", "Annnual cost", \
                      "Funding source", "Comment"]
        return HeaderList

    def getData(self):
        StaffDataList = [self._StaffCode, self._NameOrPost, \
                         self._filename, self._InstituteCode, \
                         self._GradeOrLevel, self._AnnualCost, \
                         self._ProjectOrCG, self._Comments]
        return StaffDataList

    def getStaffCode(self):
        return self._StaffCode
        
#--------  Print methods:
    @classmethod
    def printStaffDatabase(cls, _StffDtbsParams):
        print(_StffDtbsParams)


#--------  Processing methods
    @classmethod
    def cleanStaffDatabase(cls):
        Deletions =[]
        for iStf in cls.instances:
            if not isinstance(iStf._StaffCode, str):
                Deletions.append(iStf)
            if not isinstance(iStf._NameOrPost, str):
                Deletions.append(iStf)
            elif not isinstance(iStf._InstituteCode, str):
                Deletions.append(iStf)
            elif not isinstance(iStf._GradeOrLevel, str):
                Deletions.append(iStf)
            elif mth.isnan(iStf._AnnualCost):
                Deletions.append(iStf)
            elif not isinstance(iStf._ProjectOrCG, str):
                Deletions.append(iStf)
        
        if cls.__Debug:
            for i in range(len(Deletions)):
                print(" Staff; cleanStaffDatabase: instances marked for ", \
                      "deletion: ", Deletions[i]._NameOrPost)

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

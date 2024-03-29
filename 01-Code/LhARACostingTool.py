#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class LhARACostingTool:
=======================

  Master class the does the costing of the LhARA progeramme.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.

      
  Instance attributes:
  --------------------
    _Debug: Debug flag

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class
      __repr__: One liner with call.
      __str__ : Dump of constants


  Methods:
    Execute: Execute Costing, class method.
             Assumes staff, work package and associated data has been read.
             Works through costing and generates reports.

  
Created on Thu 23Dec20: Version history:
----------------------------------------
 1.0: 23Jul21: First implementation

@author: kennethlong
"""

import os
from datetime import date

import Staff         as Stf
import Equipment     as Eqp
import Project       as Prj
import WorkPackage   as wp
import Task          as Tsk
import TaskStaff     as TskStf
import TaskEquipment as TskEqp
import Report        as Rpt

class LhARACostingTool(object):
    __instance = None

#--------  "Built-in methods":
    def __new__(cls, _Debug=False):
        if cls.__instance is None:
            cls.__instance = super(LhARACostingTool, cls).__new__(cls)
        
        cls._Debug = _Debug

        if cls._Debug:
            print(" LhARACostingTool: instance created.")
            
        return cls.__instance

    def __repr__(self):
        return " LhARACostingTool(DebugFlag)"

    def __str__(self):
        print(" LhARA costing tool:")
        print("     Debug flag:", self._Debug)
        return "     <---- Done."

    @classmethod
    def Execute(cls):
        if cls._Debug:
            print("    ----> Execution starts.")

        """
               Do costing
        """
        
        #.. TaskStaff
        if cls._Debug:
            print("          TaskStaff: clean")
        nDel = TskStf.TaskStaff.clean()
        if cls._Debug:
            print("                   ", nDel, " instances deleted")
            print("                     Run doCosting")
        TskStf.TaskStaff.doCosting()
        if cls._Debug:
            print("                    <---- done")

        #..  Task
        if cls._Debug:
            print("          Task: clean")
        nDel = Tsk.Task.clean()
        if cls._Debug:
            print("              ", nDel, " instances deleted")
            print("                Run doCosting")
        Tsk.Task.doCosting()
        if cls._Debug:
            print("               <---- done")

        #..  Workpage
        if cls._Debug:
            print("          WorkPackage: clean")
        nDel = wp.WorkPackage.clean()
        if cls._Debug:
            print("                     ", nDel, " instances deleted")
            print("                       Run doCosting")
        wp.WorkPackage.doCosting()
        if cls._Debug:
            print("                      <---- done")

        #..  Project
        if cls._Debug:
            print("                   Run doCosting")
        Prj.Project.doCosting()
        if cls._Debug:
            print("          Project: clean")
        nDel = Prj.Project.clean()
        if cls._Debug:
            print("                 ", nDel, " instances deleted")
            print("                  <---- done")

        """
               Make reports
        """

        #-------->  Report path handling:
        BaseREPORTPATH = os.getenv('REPORTPATH')
        RptDt = date.today()
        if BaseREPORTPATH == None or not os.path.isdir(BaseREPORTPATH):
            print("     ----> REPORTPATH not set, no reports generated.")
        else:
            REPORTPATH = os.path.join(BaseREPORTPATH, \
                                      RptDt.strftime("%Y-%m-%d"))
            if not os.path.isdir(REPORTPATH):
                os.mkdir(REPORTPATH)
            if cls._Debug:
                print("          Report path: \n",
                      "                      ", REPORTPATH)

            #-------->  Workpackage report handling:
            if cls._Debug:
                print("          Report: list work packages")
            wpRpt = Rpt.WorkPackageList(REPORTPATH, \
                                        "WorkPackageReportList.csv")
            wpRpt.asCSV()
            if cls._Debug:
                print("                  <---- done")
                            
            if cls._Debug:
                print("          Report: work package summaries")
            for iWP in wp.WorkPackage.instances:
                filepath = REPORTPATH
                filename = iWP._Code + ".csv"
                if cls._Debug:
                    print("                 ----> ", iWP._Name)
                wpSumRpt = Rpt.WorkPackageSummary(filepath, \
                                                  filename, \
                                                  iWP)
                DataFrame = wpSumRpt.createPandasDataFrame()
                wpSumRpt.createCSV(DataFrame)
            if cls._Debug:
                print("                  <---- done")
   
            #-------->  Staff report handling:
            if cls._Debug:
                print("          Report: list all staff")
            StfLstAll = Rpt.StaffList(REPORTPATH, "StaffReportList.csv")
            StfLstAll.asCSV()

            if len(Prj.Project.instances) == 1:
                iPrj = Prj.Project.instances[0]
                iStfSmRpt = Rpt.StaffEffortSummary(REPORTPATH, \
                                        "StaffEffortSummary.csv", \
                                                   iPrj)
                iStfSmRpt.asCSV()
                
            if cls._Debug:
                print("                  <---- done")
   
            #-------->  Overview report handling:
            if cls._Debug:
                print("          Report: project overview")
                
            if len(Prj.Project.instances) == 1:
                iPrj = Prj.Project.instances[0]
                Ovrvw = Rpt.Overview(REPORTPATH, "Overview.csv", iPrj)
                Ovrvw.asCSV()
                
            if cls._Debug:
                print("                  <---- done")

    @classmethod
    def ClearDataStructure(cls):
        if cls._Debug:
            print("    ----> LhARACostingTool: Clear data structure.")

        #.. TaskStaff
        if cls._Debug:
            print("          TaskStaff: clear")
        nDel = TskStf.TaskStaff.clear()
        if cls._Debug:
            print("                   ", nDel, " instances deleted")

        #..  Task
        if cls._Debug:
            print("          Task: clear")
        nDel = Tsk.Task.clear()
        if cls._Debug:
            print("              ", nDel, " instances deleted")

        #..  Workpage
        if cls._Debug:
            print("          WorkPackage: clear")
        nDel = wp.WorkPackage.clear()
        if cls._Debug:
            print("                     ", nDel, " instances deleted")

        #..  Project
        if cls._Debug:
            print("          Project: clear")
        nDel = Prj.Project.clear()
        if cls._Debug:
            print("                 ", nDel, " instances deleted")

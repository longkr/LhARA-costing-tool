#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  This module provides Class:
    Progress

  Derived classes:
    PlannedValue
"""

"""
Class Progress:
===============

  Creates an instance of the Progress class and provides access methods
  to complete the attributes.

  Progress provides the instances and methods for earned-value
  analysis for the LhARA project.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the Progress class.

      
  Instance attributes:
  --------------------
   _Task                    = Instance of Task or workpackage class for
                              which progress is being recorded
   _Date                    = Date as a date-time object
   _PlannedFractionComplete = Fractional completion of task at _Date
                              E.g. if 10% complete _FractionComplete = 0.1
   _PlannedValue            = Fractional completion of task at _Date
   _FractionComplete        = Fractional completion of task at _Date
   _Spend                   = Spend (£k) to _Date

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods:
    loadProgress: Reads progress CSV file and creates Progress, PV, 
                  instances as appropriate.
        Input: file name, full path to file containing progress data
        Class method


  Get/set methods:
    setPrjWPorTsk: Set class (Project, WorkPackage or Task) for which
                   Progress is being reported.
              Input: PrjWPorTsk: Instance of Project, WorkPackage, or Task

          setDate: sets Date.
              Input: Date as  datetime instance

setPlannedFractionComplete: sets planned fraction complete.
              Input: Planned fraction complete as float

  setPlannedValue: Set planned value
              Input: Planned value, £k

setFractionCompelte: sets fraction complete.
              Input: Fraction complete as float

         setSpend: Set spend to date
              Input: Spend, £k

    getPrjWPorTsk: get instance: Project, WorkPackage or Task
        
        getDate: get date as datetime object
        
getPlannedFractionComplete: get planned fraction complete as float
        
getPlannedValue: get planned value in £k
                
getFractionComplete: get fraction complete as float
        
         getSpend: get spend £k
        
   getEarnedValue: get earmned value, £k


  Processing methods:
   takePrjWPorTsk: True if input is valid instance of Project,
                   WorkPackage or Task
              Input: Instance of Project, WorkPackage or Task to be
                   checked
              Class method

  WPorPrjProgress: Compute progress values for WorkPackage or Project
                   instance.
              Input: Instance of Project or WorkPackage

             Plot: Make progress plots (PV, EV, etc.); landscape and
                   portrait formats
              Input:
               - DataFrame: Pandas data frame with progress report
               -  PlotPath: Path to directory where plots to be written
               -  FileName: Stem of plot file name.  Landscape or portrait
                            will be appended as appropriate
               - Landscate: If True, you get a plot in landscape format


       Exceptions:
             ProgressPrjWPorTskNotValid: Requested instance neither Project
                                         WorkPackage or Task

                   ProgressDateNotValid: Date not datetime object

       ProgressFractionCompleteNotValid: fraction neither float nor null

ProgressPlannedFractionCompleteNotValid: fraction neither float nor null

           ProgressPlannedValueNotValid: value not float

                  ProgressSpendNotValid: value not float

                      OutputPathInvalid: invalid path for plot

              NoWriteAccessToOutputPath: cant write to plot path

                 PrjOrWpInstanceInvalid: Cant process progress data for
                                         Project or WorkPackage instance


  
Created on Wed 17Jun22. Version history:
----------------------------------------
 1.0: 17Jun22: First implementation

@author: kennethlong
"""

import os
import datetime as DT
import pandas   as pnds
import math     as mt
import matplotlib.pyplot as plt
import matplotlib as mpl
from operator import attrgetter

import Task        as Tsk
import WorkPackage as wp
import Project     as Prj
#import Progress    as Prg

class Progress:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _PrjWPorTsk=None, _Date=None, \
                       _PlannedFractionComplete=None, \
                       _PlannedValue=None, \
                       _FractionComplete=None, _Spend=None):

        self.setPrjWPorTsk(_PrjWPorTsk)
        self.setDate(_Date)
        self.setPlannedFractionComplete(_PlannedFractionComplete)
        self.setPlannedValue(_PlannedValue)
        self.setFractionComplete(_FractionComplete)
        self.setSpend(_Spend)
                
        Progress.instances.append(self)
        
    def __repr__(self):
        return "Progress(PrjWPorTsk, Date, PlannedFractionComplete, " \
               "PlannedValue, FractionComplete, Spend)"

    def __str__(self):
        print(" Progress:", self.getPrjWPorTsk()._Name)
        print("     Date                   :", self.getDate())
        print("     PlannedFractionComplete:", \
              self.getPlannedFractionComplete())
        print("     PlannedValue           :", self.getPlannedValue())
        print("     FractionComplete       :", self.getFractionComplete())
        print("     Spend                  :", self.getSpend())
        return "  <---- Done."

    
#--------  I/o methods:
    @classmethod
    def loadProgress(cls, _filename=None):
        if _filename == None:
            raise NoFilenameProvided( \
                'CSV filename required; execution termimated.')
        elif not os.path.isfile(_filename):
            raise NonExistantFile('CSV file' + _filename + \
                                  ' does not exist; execution termimated.')

        ProgParams = pnds.read_csv(_filename)
        iRow       = ProgParams.index
        if cls.getDebug():
            print(" Progress.loadProgress: parse progress report")
        ProgList = ProgParams.values.tolist()
        iCnt = 0
        for i in iRow:
            wpInst = None
            TskInst = None
            iCnt += 1
            if cls.getDebug():
                print("     ----> Parse row", iCnt, ProgList[iCnt-1])

            if ProgParams.iloc[i,0] == "Work package":
                if cls.getDebug():
                    print("         ----> Work package:", \
                          ProgParams.iloc[i,1])
                for wpInstIter in wp.WorkPackage.instances:
                    if wpInstIter._Name == ProgParams.iloc[i,1]:
                        if cls.getDebug():
                            print("         ----> Identified:")
                    wpInst = wpInstIter
                if wpInst == None:
                    if cls.getDebug():
                        print("         <---- Not identified!")

            elif ProgParams.iloc[i,0] == "ProgressLine":
                if cls.getDebug():
                    print("         ----> Progress line for task:", \
                      ProgParams.iloc[i,1])
                for TskInstIter in Tsk.Task.instances:
                    if TskInstIter._Name == ProgParams.iloc[i,1]:
                        if cls.getDebug():
                            print("             ----> Identified.")
                        TskInst = TskInstIter
                if TskInst == None:
                    if cls.getDebug():
                        print("         <---- Not identified!")
                    
            if TskInst != None:
                if cls.getDebug():
                    print("                 ----> Progress line:", \
                      DT.datetime.strptime(ProgParams.iloc[i,3],'%d %B %Y'),\
                      ProgParams.iloc[i,4], \
                      ProgParams.iloc[i,5], \
                      ProgParams.iloc[i,6], \
                      ProgParams.iloc[i,7])
                PrgInst = Progress(TskInst, \
                    DT.datetime.strptime(ProgParams.iloc[i,3],'%d %B %Y'), \
                                   float(ProgParams.iloc[i,4]), \
                                   float(ProgParams.iloc[i,5])/1000., \
                                   float(ProgParams.iloc[i,6]), \
                                   float(ProgParams.iloc[i,7])/1000. )
        if cls.getDebug():
            print("     <---- data frame:")
            print(PrgInst)
            print(" <----  Progress.loadProgress done.")
            
                
#--------  Get/set methods:
    @classmethod
    def setDebug(cls, Debug):
        cls.__Debug = False
        
    def setPrjWPorTsk(self, _PrjWPorTsk):
        if not isinstance(_PrjWPorTsk, Tsk.Task) and \
           not isinstance(_PrjWPorTsk, wp.WorkPackage) and \
           not isinstance(_PrjWPorTsk, Prj.Project):
            raise ProgressPrjWPorTskNotValid( \
                                " Progress.setPrjWPorTsk: _PrjWPorTsk " \
                                "not an instance of Task class")
        self._PrjWPorTsk = _PrjWPorTsk
        
    def setDate(self, _Date):
        if not isinstance(_Date, DT.datetime):
            raise ProgressDateNotValid(" Progress.setDate: _Date " \
                                       "not an instance of datetime class")
        self._Date = _Date
        
    def setPlannedFractionComplete(self, _PlannedFractionComplete):
        if isinstance(_PlannedFractionComplete, float) or \
            mt.isnan(float(_PlannedFractionComplete)):
            self._PlannedFractionComplete = _PlannedFractionComplete
        else:
            raise ProgressPlannedFractionCompleteNotValid( \
                               " Progress.setPlannedFractionComplete: " \
                               "_PlannedFractionComplete not a float")
        
    def setPlannedValue(self, _PlannedValue):
        if isinstance(_PlannedValue, float) or \
            mt.isnan(float(_PlannedValue)):
            self._PlannedValue = _PlannedValue
        else:
            raise ProgressPlannedValueNotValid( \
                               " Progress.setPlannedValue: " \
                               "_PlannedValue not a float")
        
    def setFractionComplete(self, _FractionComplete):
        if _FractionComplete == "nan" or \
           isinstance(_FractionComplete, float):
            self._FractionComplete = _FractionComplete
        else:
            raise ProgressFractionCompleteNotValid( \
                                       " Progress.setFractionComplete: " \
                                       "_FractionComplete not a float")
        
    def setSpend(self, _Spend):
        if isinstance(_Spend, float) or \
           _Spend == "nan":
           self._Spend = _Spend
        else:
            raise ProgressSpendNotValid(" Progress.setSpend: _Spend " \
                                       "not a float")

    @classmethod
    def getDebug(cls):
        return cls.__Debug
    
    def getPrjWPorTsk(self):
        return self._PrjWPorTsk
        
    def getDate(self):
        return self._Date
        
    def getPlannedFractionComplete(self):
        return self._PlannedFractionComplete
        
    def getPlannedValue(self):
        return self._PlannedValue
                
    def getFractionComplete(self):
        return self._FractionComplete
        
    def getSpend(self):
        return self._Spend
        
    def getEarnedValue(self):

        EV = None
        for iEV in EarnedValue.instances:
            if iEV.getProgress() == self:
                EV = iEV._EarnedValue
        
        return EV
        

#--------  Processing methods:

    @classmethod
    def takePrjWPorTsk(cls, _iTsk, _PrjOrWPInst):
        
        tkTsk  = False

        iWP  = _iTsk._WorkPackage
        iPrj = iWP._Project

        if isinstance(_PrjOrWPInst, wp.WorkPackage) and \
           iWP == _PrjOrWPInst:
            tkTsk = True
        elif isinstance(_PrjOrWPInst, Prj.Project) and \
             iPrj == _PrjOrWPInst:
            tkTsk = True
            
        return tkTsk
        
    @classmethod
    def WPorPrjProgress(cls, _WPorPrjInst):

        if not isinstance(_WPorPrjInst, wp.WorkPackage) and \
           not isinstance(_WPorPrjInst, Prj.Project):
            raise PrjOrWpInstanceInvalid()

        if cls.getDebug() == True:
            print(" Progress.WPorPrjProgress: wpName:", \
                  _WPorPrjInst._Name)

        SortedPrgRprt = sorted(Progress.instances, \
                          key=attrgetter('_Date', '_PrjWPorTsk._Name'), \
                                 )

        DtRef   = None

        nTsks   = 0
        wpPFC   = 0.
        wpFC    = 0.
        wpPV    = 0.
        wpEV    = 0.
        wpSpend = 0.

        Loaded  = False
        
        #.. Loop over progress instances in date order:
        for iPrg in SortedPrgRprt:
            if cls.getDebug():
                print("     ----> Consider Prj, WP, or Tsk:", \
                      iPrg.getPrjWPorTsk().getName())
            iWPorTsk = iPrg.getPrjWPorTsk()

            #.. Take Task entries for requested work package only:
            if isinstance(iWPorTsk, Tsk.Task):
                iTsk = iWPorTsk
                if cls.getDebug():
                    print("         ----> Process task:", \
                          iTsk.getName(), iTsk.getWorkPackage().getName())

                if cls.takePrjWPorTsk(iTsk,_WPorPrjInst):
                    if cls.getDebug() == True:
                        print("             ----> WP or Tsk name:", \
                              iWPorTsk.getName())
                    
                    Dt   = iPrg.getDate()
                    if cls.getDebug() == True:
                        print("             ----> Date, reference date:", \
                              Dt, DtRef)
                    if DtRef == None:
                        DtRef = Dt
                    
                    #.. Handle new date; create wp progress instance and
                    #   zero counters:
                    if Dt != DtRef:
                        if cls.getDebug() == True:
                            print("                 ----> New date:", Dt)
                        if nTsks != 0:
                            #.. Create work-package progress instance
                            wpPFC = wpPFC / nTsks
                            wpFC  = wpFC  / nTsks
                            if cls.getDebug() == True:
                                print( \
               "                       Creating WP progress instance:")
                                print("                           ---->", \
                                      " nTsks, PFC, FC, PV, EV, Spend:",\
                                      nTsks, wpPFC, wpFC, wpPV, wpEV, wpSpend)
                            iwpPrg = Progress(_WPorPrjInst, DtRef, wpPFC, \
                                                  wpPV, wpFC, wpSpend)
                            iwpEV  = EarnedValue(_WPorPrjInst, DtRef, \
                                                     iwpPrg, wpEV)
                            if not Loaded: Loaded = True
                            if cls.getDebug() == True:
                                print( \
      "                 <---- Progress and EarnedValue instances created:",
                                       iwpPrg.getPrjWPorTsk().getName(), \
                                       iwpEV.getPrjWPorTsk().getName())
                            
                        #----> Progress(<arguments>)
                        #.. Set date reference, zero task count
                        DtRef   = Dt
                        nTsks   = 0.
                        wpPFC   = 0.
                        wpFC    = 0.
                        wpPV    = 0.
                        wpEV    = 0.
                        wpSpend = 0.
                        if cls.getDebug() == True:
                            print("                 <---- Reset done.")

                    if cls.getDebug() == True:
                        print("             <---- Load and increment.")
                        
                    #.. Get incremental data
                    PFC  = iPrg.getPlannedFractionComplete()
                    FC   = iPrg.getFractionComplete()
                    PV   = iPrg.getPlannedValue()
                    EV   = iPrg.getEarnedValue()
                    Spnd = iPrg.getSpend()
                    if cls.getDebug() == True:
                        print("         <----", \
                              " PFC, FC, PV, EV, Spnd:", \
                              PFC, FC, PV, EV, Spnd)

                    #.. Increment spend, progress etc.
                    nTsks   += 1.
                    wpPFC   += PFC
                    wpFC    += FC
                    wpPV    += PV
                    wpEV    += EV
                    wpSpend += Spnd

                
                #.. End of work-package-check if block
            #.. End of is a Task check if block
        #.. End of loop over progress entries

        if cls.getDebug() == True:
            print("     <----> Flush last entry:")
            if nTsks != 0:
                #.. Create work-package progress instance
                wpPFC = wpPFC / nTsks
                wpFC  = wpFC  / nTsks
                if cls.getDebug() == True:
                    print("           Creating WP progress instance:")
                    print("               ---->", \
                          " nTsks, PFC, FC, PV, EV, Spend:",\
                          nTsks, wpPFC, wpFC, wpPV, wpEV, wpSpend)
                iwpPrg = Progress(_WPorPrjInst, DtRef, wpPFC, \
                                  wpPV, wpFC, wpSpend)
                iwpEV  = EarnedValue(_WPorPrjInst, DtRef, \
                                     iwpPrg, wpEV)
                if cls.getDebug() == True:
                    print("               <---- Final Progress", \
                          " and EarnedValue instances created:", \
                          iwpPrg.getPrjWPorTsk().getName(), \
                          iwpEV.getPrjWPorTsk().getName())
        
        
        #.. End of processing

        return Loaded
        
    @classmethod
    def Plot(cls, DataFrame, \
             _PlotPath=None, \
             _FileName=None, \
             landscape = False):
        """
        Generates a figure of the Progress Plots
        
        Arguments:
        ==========
            DataFrame: Pandas DataFrame containing the progress data.
                       Columns:
                          Task/Work package name
                          Date
                          Planned value (£k)
                          Earned value (£k)
                          Spend (£k)
                          Schedule variance (£k)
                          Cost variance (£k)
                          Budget variance variance (£k)
                          Schedule performance index
                          Cost performance index
                          Issue date
        
            _PlotPath: Path to where plots to be written

            _FileName: File name (appended to _PlotPath)

            landscape: Boolean
                       Default = False
                       If False: Generates a portrait figure
                       If True: Generates landscape figure
        
        Returns:
        ========
            An image of the Progress Plots saved as _FileName

        """

        nEntries = DataFrame.count()
        pTitle   = DataFrame.columns.values.tolist()[0]

        mpl.rcParams.update({'font.size': 10})
        
        if cls.getDebug() == True:
            pnds.set_option('display.max_columns', None)
            print(" Progress.Plot called to plot DataFrame: \n",   \
                  "     ----> Number of entries:", nEntries, "\n", \
                  DataFrame)
            
        #.. Create figure and remove unneeded x-axis ticks
        if landscape is False:
            fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize = (10,14),  
                    gridspec_kw={'height_ratios':[2,5,2]})
            ax1.set_xticks([])
            ax1.set_xticklabels([])
            ax2.set_xticks([])
            ax2.set_xticklabels([])
            ax3.xaxis.set_tick_params(labelsize=15)
            ax1.yaxis.set_tick_params(labelsize=15)
            ax2.yaxis.set_tick_params(labelsize=15)
            ax3.yaxis.set_tick_params(labelsize=15)
        else:
            fig = plt.figure(figsize = (14, 10))
            ax1 = plt.subplot2grid(shape=(2, 2), loc=(0,1), rowspan=1)
            ax2 = plt.subplot2grid(shape=(2, 2), loc=(0,0), rowspan=2)
            ax3 = plt.subplot2grid(shape=(2, 2), loc=(1,1), rowspan=1)
            ax1.set_xticks([])
            ax1.set_xticklabels([])

        #.. Remove extra space around figure
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        
        #.. Add Title
        fig.suptitle(pTitle, \
                     fontsize='25', \
                     fontweight='bold')
        
        #.. Remove vertical white space between subplots
        fig.subplots_adjust(hspace=0)
        
        #.. Scatter Plot all Data
        
        #.. Ax1 - Performance Index
        DataFrame.plot.scatter(x='Date',y='Schedule performance index', \
                               ax=ax1, marker = 'o', c = "C{}".format(0), \
                               label='Schedule performace index')
        DataFrame.plot(x='Date',y='Schedule performance index', ax=ax1,
                c = "C{}".format(0), linestyle = ' ', label='')
        DataFrame.plot.scatter(x='Date', y='Cost performance index', ax=ax1,\
                    marker = 'o', c="C{}".format(1), \
                    label='Cost performance index')
        DataFrame.plot(x='Date',y='Cost performance index', ax=ax1,
                c = "C{}".format(1), linestyle = ' ', label='')
        
        #.. Ax2 - Value
        DataFrame.plot.scatter(x='Date', y="Planned value (£k)",ax=ax2,
                       marker='o', c="C{}".format(0), \
                       label='Planned value (£k)')
        DataFrame.plot(x='Date',y='Planned value (£k)', ax=ax2,
                c = "C{}".format(0), linestyle = ' ', label = '')
        DataFrame.plot.scatter(x='Date', y='Earned value (£k)',ax=ax2,
                        marker='o', c = "C{}".format(1), label='Earned value (£k)')
        DataFrame.plot(x='Date',y='Earned value (£k)', ax=ax2,
                c = "C{}".format(1), linestyle = ' ', label='')
        
        ###########Spend needs to be changed to Actual value#############
        DataFrame.plot.scatter(x='Date', y= 'Spend (£k)', ax=ax2, 
                marker='o', c="C{}".format(2), label='Spend (£k)')
        DataFrame.plot(x='Date', y='Spend (£k)', ax=ax2, 
                c = "C{}".format(2), linestyle=' ', label='')  
        #Ax3 - Variance
        DataFrame.plot.scatter(x='Date', y='Schedule variance (£k)', ax=ax3, \
                    marker='o', c="C{}".format(0), \
                            label='Schedule variance (£k)')
        DataFrame.plot(x='Date',y='Schedule variance (£k)', ax=ax3,
                c = "C{}".format(0), linestyle = ' ', label='')
        DataFrame.plot.scatter(x='Date', y='Cost variance (£k)', ax=ax3,
                    marker='o',c = "C{}".format(1), label='Cost variance (£k)')
        DataFrame.plot(x='Date',y='Cost variance (£k)', ax=ax3,
                c = "C{}".format(1), linestyle = ' ', label = '')
        DataFrame.plot.scatter(x='Date', y='Budget variance variance (£k)', \
                               ax=ax3, marker='o', c = "C{}".format(2), \
                               label='Budget variance (£k)')
        DataFrame.plot(x='Date',y='Budget variance variance (£k)', ax=ax3,
                c = "C{}".format(2), linestyle = ' ', label='')
        #Label y-axes and rotate to be horizontal
        ax1.set_ylabel(ylabel = r'Performance' '\n' 'Index',
                       fontsize = '15', 
                fontweight='bold' , rotation = 'vertical')
        ax2.set_ylabel(ylabel = 'Value', fontsize = '15', 
                fontweight='bold', rotation = 'vertical')
        ax3.set_ylabel(ylabel = 'Variance', fontsize ='15', 
                fontweight = 'bold', rotation = 'vertical')
        if landscape is False:
            ax1.yaxis.set_label_coords(-0.1, 0.5)
            ax2.yaxis.set_label_coords(-0.1, 0.5)
            ax3.yaxis.set_label_coords(-0.1, 0.5)
        else:
            ax1.yaxis.set_label_coords(1.25, 0.56)
            ax2.yaxis.set_label_coords(-0.2, 0.49)
            ax3.yaxis.set_label_coords(1.25, 0.56)
        #Adjust x-ticks so they can be read better -
        #rotates and skips every other date
        for tick in ax3.get_xticklabels():
            tick.set_rotation(45)
        for tick in ax3.get_xticklabels()[::2]:
            tick.set_visible(False)
        #ax3.set_xlabel(xlabel='Date', fontsize='large', fontweight='bold')
        ax3.set_xlabel(xlabel=None)
        if landscape is True:
            for tick in ax2.get_xticklabels():
                tick.set_rotation(45)
            for tick in ax2.get_xticklabels()[::2]:
                tick.set_visible(False)
            ax2.set_xlabel(xlabel='Date', fontsize='large', fontweight='bold')
        #Add legends labels and locations
        if landscape is False:
            legend_locations = ['center left', 'center left', 'center left']
            bbox_anchor = [(0.55, 0.70), (0.6, 0.25),(0.6, 0.25)]
        else:
            legend_locations = ['center left', 'center right', 'center left']
            bbox_anchor = [(1.0, 0.42), (-0.04, 0.39), (1.0, 0.42)]
        ax1.legend(loc = legend_locations[0], bbox_to_anchor= bbox_anchor[0], 
                    fontsize ='15', frameon=False)
        ax2.legend(loc = legend_locations[1], bbox_to_anchor=bbox_anchor[1], 
                fontsize='15', frameon=False)
        ax3.legend(loc = legend_locations[2], bbox_to_anchor=bbox_anchor[2], 
                fontsize='15', frameon=False)

        # Save plot:
        if not os.path.isdir(_PlotPath):
            raise OutputPathInvalid('Output path:', _PlotPath, ' invalid')

        if not os.access(_PlotPath, os.W_OK):
            raise NoWriteAccessToOutputPath( \
                     'No write access to output path:', _PlotPath)

        if _FileName == None:
            _FileName = "NoFileNameGiven"
        filename = os.path.join(_PlotPath, _FileName)
        
        plt.savefig(filename, bbox_inches='tight')

    
#--------  Exceptions:
class ProgressPrjWPorTskNotValid(Exception):
    pass

class ProgressDateNotValid(Exception):
    pass

class ProgressFractionCompleteNotValid(Exception):
    pass

class ProgressPlannedFractionCompleteNotValid(Exception):
    pass

class ProgressPlannedValueNotValid(Exception):
    pass

class ProgressSpendNotValid(Exception):
    pass

class OutputPathInvalid(Exception):
    pass

class NoWriteAccessToOutputPath(Exception):
    pass

class PrjOrWpInstanceInvalid(Exception):
    pass
                  

"""
Class EarnedValue:
===================

  Creates an instance of the EarnedValue class and provides access methods
  to complete the attributes.


  Class attributes:
  -----------------
  __Debug : Boolean: set for debug print out
  instances: List of instances if the Progress class.

      
  Instance attributes:
  --------------------
   _PrjWPorTsk  = Instance of Project, WorkPackage or Task
   _Date        = Date as a date-time object
   _Progress    = Progress instance to which this EarnedValue instance
                  relates
   _EarnedValue = FLoat or None.  If None earned value (£k) will be
                  calculated from FractionComplete and total value of
                  Project, WorkPackage, or Task instance

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods: None


  Get/set methods:
    setEarnedValue: set earned value, input is earned value in £k or None.
                    If None, then earned value (£k) will be calculated
                    from FractionComplete and total value of Project,
                    WorkPackage, or Task instance
      Input: Float, earned value, £k

       setProgress: set self._Progress with Progress instance associated
                    with this EarnedValue instance
      Input: instance of Progress

       getProgress: return Progress instance

    getEarnedValue: return earned value, float, £k
        

  Processing methods: None

          Exceptions:
EarnedValueEVNotValid: Earned value neither float nor None

  
Created on Wed 17Jun22. Version history:
----------------------------------------
 1.0: 120un22: First implementation

@author: kennethlong
"""

class EarnedValue(Progress):
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _PrjWPorTsk=None, _Date=None, _Prg=None, _EV=None):

        self.setPrjWPorTsk(_PrjWPorTsk)
        self.setDate(_Date)
        self.setProgress(_Prg)
        self.setEarnedValue(_EV)

        EarnedValue.instances.append(self)
        
    def __repr__(self):
        return "EarnedValue(Task, Date)"

    def __str__(self):
        print(" EarnedValue:", self.getPrjWPorTsk()._Name)
        print("     Date             :", self.getDate())
        print("     Planned value    :", self.getEarnedValue())
        print("     Progress instance:", self.getProgress())
        return "  <---- Done."

    
#--------  I/o methods:


#--------  Get/set methods:
    @classmethod
    def getinstances(cls):
        return cls.instances
    
    def setEarnedValue(self, _EV):
        if not isinstance(_EV, float) and not (_EV is None):
            raise EarnedValueEVNotValid(\
                            " EarnedValue.setEarnedValue: " \
                                       "not valid.")
        
        EV = None

        if _EV is None:
            PrjWPorTskTotVal = self._PrjWPorTsk.getTotalValue()
            if PrjWPorTskTotVal != None:
                if self.__Debug:
                    print("  Progress.setEarnedValue:", \
                          "    ----> Task:", self._PrjWPorTsk._Name, \
                          "          PrjWPorTskTotVal:", PrjWPorTskTotVal, \
                  "          Fraction complete:", \
                          self._Progress._FractionComplete)
                EV =  PrjWPorTskTotVal * self._Progress._FractionComplete
        else:
            EV = _EV

        self._EarnedValue = EV
        
    def setProgress(self, _Prg):
        _setPrg = None
        if isinstance(_Prg, Progress):
            _setPrg = _Prg
        self._Progress = _Prg

    def getProgress(self):
        return self._Progress
                
    def getEarnedValue(self):
        return self._EarnedValue
                

#--------  Processing methods:


#--------  Exceptions:
class EarnedValueEVNotValid(Exception):
    pass

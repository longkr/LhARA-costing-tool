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
   _Task                    = Instance of Task class for which progress is
                              being recorded
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
        Class method


  Get/set methods:
    set: set 
      Input: numpy array
        
    get: get 
      Input: numpy array
        


  Processing methods:

  
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

import Task  as Tsk
import WorkPackage as wp

class Progress:
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Date=None, \
                       _PlannedFractionComplete=None, \
                       _PlannedValue=None, \
                       _FractionComplete=None, _Spend=None):

        self.setTask(_Task)
        self.setDate(_Date)
        self.setPlannedFractionComplete(_PlannedFractionComplete)
        self.setPlannedValue(_PlannedValue)
        self.setFractionComplete(_FractionComplete)
        self.setSpend(_Spend)
                
        Progress.instances.append(self)
        
    def __repr__(self):
        return "Progress(Task, Date, PlannedFractionComplete " \
               "FractionComplete, Spend)"

    def __str__(self):
        print(" Progress:", self.getTask()._Name)
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
        if cls.__Debug:
            print(" Progress.loadProgress: parse progress report")
        ProgList = ProgParams.values.tolist()
        iCnt = 0
        for i in iRow:
            wpInst = None
            TskInst = None
            iCnt += 1
            if cls.__Debug:
                print("   ----> Parse row", iCnt, ProgList[iCnt-1])

            if ProgParams.iloc[i,0] == "Work package":
                if cls.__Debug:
                    print("     ----> Work package:", ProgParams.iloc[i,1])
                for wpInstIter in wp.WorkPackage.instances:
                    if wpInstIter._Name == ProgParams.iloc[i,1]:
                        if cls.__Debug:
                            print("       ----> Identified:")
                    wpInst = wpInstIter
                if wpInst == None:
                    if cls.__Debug:
                        print("       ----> Not identified!")

            elif ProgParams.iloc[i,0] == "ProgressLine":
                if cls.__Debug:
                    print("       ----> Progress line for task:", \
                      ProgParams.iloc[i,1])
                for TskInstIter in Tsk.Task.instances:
                    if TskInstIter._Name == ProgParams.iloc[i,1]:
                        if cls.__Debug:
                            print("         ----> Identified.")
                        TskInst = TskInstIter
                if TskInst == None:
                    if cls.__Debug:
                        print("         ----> Not identified!")
                    
            if TskInst != None:
                if cls.__Debug:
                    print("           ----> Progress line:", \
                      DT.datetime.strptime(ProgParams.iloc[i,3],'%d %B %Y'),\
                      ProgParams.iloc[i,4], \
                      ProgParams.iloc[i,5], \
                      ProgParams.iloc[i,6], \
                      ProgParams.iloc[i,7])
                PrgInst = Progress(TskInst, \
                    DT.datetime.strptime(ProgParams.iloc[i,3],'%d %B %Y'), \
                                   float(ProgParams.iloc[i,4]), \
                                   float(ProgParams.iloc[i,5]), \
                                   float(ProgParams.iloc[i,6]), \
                                   float(ProgParams.iloc[i,7]) )

#--------  Get/set methods:
    def setTask(self, _Task):
        if not isinstance(_Task, Tsk.Task):
            raise ProgressTaskNotValid(" Progress.setTask: _Task " \
                                       "not an instance of Task class")
        self._Task = _Task
        
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
        
    def getTask(self):
        return self._Task
        
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
        
    def getEarnedValue(self, _Date):
        EV = None
        for iEV in EarnedValue.instances:
            if iEV._Date == _Date:
                EV = iEV._EarnedValue
            
        return EV
        

#--------  Processing methods:

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
                          Project office support
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
        if Progress.__Debug == True:
            print(" Progress.Plot called to plot DataFrame: \n",   \
                  "     ----> Number of entries:", nEntries, "\n", \
                  DataFrame)
            
        #.. Create figure and remove unneeded x-axis ticks
        if landscape is False:
            fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize = (10,14),  
                    gridspec_kw={'height_ratios':[2,5,2]})
            ax1.set_xticks([],[])
            ax2.set_xticks([],[])
        else:
            fig = plt.figure(figsize = (14, 10))
            ax1 = plt.subplot2grid(shape=(2, 2), loc=(0,1), rowspan=1)
            ax2 = plt.subplot2grid(shape=(2, 2), loc=(0,0), rowspan=2)
            ax3 = plt.subplot2grid(shape=(2, 2), loc=(1,1), rowspan=1)
            ax1.set_xticks([],[])
            
        #.. Remove extra space around figure
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        
        #.. Add Title
        fig.suptitle('Progress Plots', \
                     fontsize='xx-large', \
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
        DataFrame.plot.scatter(x='Date', y='Schedule variance (£k)', ax=ax3,
                    marker='o', c="C{}".format(0), label='Schedule variance (£k)')
        DataFrame.plot(x='Date',y='Schedule variance (£k)', ax=ax3,
                c = "C{}".format(0), linestyle = ' ', label='')
        DataFrame.plot.scatter(x='Date', y='Cost variance (£k)', ax=ax3,
                    marker='o',c = "C{}".format(1), label='Cost variance (£k)')
        DataFrame.plot(x='Date',y='Cost variance (£k)', ax=ax3,
                c = "C{}".format(1), linestyle = ' ', label = '')
        DataFrame.plot.scatter(x='Date', y='Budget variance variance (£k)', ax=ax3,
                    marker='o', c = "C{}".format(2), label='Budget variance (£k)')
        DataFrame.plot(x='Date',y='Budget variance variance (£k)', ax=ax3,
                c = "C{}".format(2), linestyle = ' ', label='')
        #Label y-axes and rotate to be horizontal
        ax1.set_ylabel(ylabel = r'Performance' '\n' 'Index', fontsize = 'large', 
                fontweight='bold' , rotation = 'horizontal')
        ax2.set_ylabel(ylabel = 'Value', fontsize = 'large', 
                fontweight='bold', rotation = 'horizontal')
        ax3.set_ylabel(ylabel = 'Variance', fontsize ='large', 
                fontweight = 'bold', rotation = 'horizontal')
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
        ax3.set_xlabel(xlabel='Date', fontsize='large', fontweight='bold')
        if landscape is True:
            for tick in ax2.get_xticklabels():
                tick.set_rotation(45)
            for tick in ax2.get_xticklabels()[::2]:
                tick.set_visible(False)
            ax2.set_xlabel(xlabel='Date', fontsize='large', fontweight='bold')
        #Add legends labels and locations
        if landscape is False:
            legend_locations = ['center left', 'center left', 'center left']
            bbox_anchor = [(1.0, 0.5), (1.0, 0.5),(1.0, 0.5)]
        else:
            legend_locations = ['center left', 'center right', 'center left']
            bbox_anchor = [(1.0, 0.42), (-0.04, 0.39), (1.0, 0.42)]
        ax1.legend(loc = legend_locations[0], bbox_to_anchor= bbox_anchor[0], 
                    fontsize ='large', frameon=False)
        ax2.legend(loc = legend_locations[1], bbox_to_anchor=bbox_anchor[1], 
                fontsize='large', frameon=False)
        ax3.legend(loc = legend_locations[2], bbox_to_anchor=bbox_anchor[2], 
                fontsize='large', frameon=False)

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
class ProgressTaskNotValid(Exception):
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
   _Task         = Date as a date-time object
   _Date         = Date as a date-time object
   _EarnedValue = Fractional completion of task at _Date.
   _Progress     = Optional -- filled if PV relates to a Progress instance.

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  I/o methods:


  Get/set methods:
    set: set 
      Input: numpy array
        
    get: get 
      Input: numpy array
        


  Processing methods:

  
Created on Wed 17Jun22. Version history:
----------------------------------------
 1.0: 120un22: First implementation

@author: kennethlong
"""

class EarnedValue(Progress):
    __Debug = False
    instances = []

#--------  "Built-in methods":
    def __init__(self, _Task=None, _Date=None, _Prg=None):

        self.setTask(_Task)
        self.setDate(_Date)
        self.setProgress(_Prg)
        self.setEarnedValue(None)

        EarnedValue.instances.append(self)
        
    def __repr__(self):
        return "EarnedValue(Task, Date)"

    def __str__(self):
        print(" EarnedValue:", self.getTask()._Name)
        print("     Date             :", self.getDate())
        print("     Planned value    :", self.getEarnedValue())
        print("     Progress instance:", self.getProgress())
        return "  <---- Done."

    
#--------  I/o methods:


#--------  Get/set methods:
    def setEarnedValue(self, _EV):
        EV = None
        if not isinstance(_EV, float) and not (_EV is None):
            raise EarnedValueEVNotValid(\
                            " EarnedValue.setEarnedValue: " \
                                       "not valid.")
        if isinstance(self._Progress, Progress):
            TskTotVal = self._Task.getTotalValue()
            if TskTotVal != None:
                if self.__Debug:
                    print("  Progress.setEarnedValue:", \
                          "    ----> Task:", self._Task._Name, \
                          "          TskTotVal:", TskTotVal, \
                  "          Fraction complete:", \
                          self._Progress._FractionComplete)
                EV =  TskTotVal * self._Progress._FractionComplete
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

class NoFilenameProvided(Exception):
    pass

class NonExistantFile(Exception):
    pass

# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompanying license for more details.
# ------------------------------------------------------------------------------


"""Main windows and dialogs of the App """


#region -------------------------------------------------------------> Imports
import _thread
import os
import shutil
import webbrowser
from itertools import zip_longest
from math      import ceil
from pathlib   import Path
from typing    import Optional, Literal, Union

import matplotlib         as mpl
import matplotlib.patches as mpatches
import numpy              as np
import pandas             as pd
import requests
from scipy import stats

from Bio       import pairwise2
from Bio.Align import substitution_matrices

from reportlab.lib.pagesizes      import A4
from reportlab.platypus           import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.styles         import getSampleStyleSheet, ParagraphStyle

import wx
import wx.richtext
import wx.adv                    as adv
import wx.lib.agw.aui            as aui
import wx.lib.agw.customtreectrl as wxCT
import wx.lib.agw.hyperlink      as hl

import config.config  as mConfig
import data.file      as mFile
import data.check     as mCheck
import data.method    as mMethod
import data.exception as mException
import data.statistic as mStatistic
import gui.menu       as mMenu
import gui.method     as gMethod
import gui.tab        as mTab
import gui.pane       as mPane
import gui.widget     as mWidget
import gui.validator  as mValidator
#endregion ----------------------------------------------------------> Imports


# Pandas lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region --------------------------------------------------------> Base Classes
class BaseWindowResultOnePlotFA(BaseWindowResultOnePlot):
    """Base Window for Further Analysis with one Plot, e.g. AA.

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default None
        menuData : dict
            Data to build the Tool menu of the window. See structure in child
            class.

        Attributes
        ----------


        Raises
        ------


        Methods
        -------

    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent  : Optional[wx.Window]=None,
        menuData: dict={},
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent, menuData=menuData)
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def ExportData(self, df: Optional[pd.DataFrame]=None) -> bool:
        """Export data to a csv file

            Returns
            -------
            bool
        """
        if df is None:
            df = self.rData                                                     # type: ignore
        return super().ExportData(df=df)
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Close window and uncheck section in UMSAPFile window. Assumes
            self.parent is an instance of UMSAPControl.
            Override as needed.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update parent
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].remove(self)           # type: ignore
        #endregion --------------------------------------------> Update parent

        #region ------------------------------------> Reduce number of windows
        mConfig.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class WindowResProtProf(BaseWindowResultListTextNPlot):
    """Plot results in the Proteome Profiling section of an UMSAP file.

        Parameters
        ----------
        parent : UMSAPControl

        Attributes
        ----------
        dKeyMethod : dict
            Keys are str and values methods to manage the window.
        rAutoFilter : bool
            Apply defined filters (True) when changing date or not (False).
            Default is False.
        rCI : dict
            CI dict for the current date.
        rColor: str
            Color mode.
        rCondC : str
            Condition currently selected.
        rCorrP : bool
            Use corrected P values (True) or not (False). Default is False.
        rData : dict
            Dict with the configured data for this section from UMSAPFile.
        rDate : list of str
            List of available dates in the section.
        rDateC : str
            Currently selected date.
        rDf : pd.DataFrame
            DF with the data currently display in the window.
        rFcXLabel : list of str
            List of labels for the x axis in the FC plot.
        rFcXRange : list of float
            Min and Max value for the x axis in the FC plot.
        rFcYMax : list of float
            Max log2FC value on all conditions for the relevant points.
        rFcYMin : list of float
            Min log2FC value on all conditions for the relevant points.
        rFcYRange : list of float
            Min and Max value for the y axis in the FC Plot including the CI.
        rFilterList : list
            List of applied filters. e.g. [['Key', {kwargs}], 'StatusBarText']
        rGreenP : matplotlib object
            Reference to the green dot shown in the Volcano plot after selecting
            a protein in the wx.ListCtrl.
        rLabelProt: list
            List of proteins to label
        rLCIdx: int or None
            Selected row in the wx.ListCtrl.
        rLockScale : str
            Lock plot scale to No, Date or Project.
        rLog2FC: float
            Limit for the Log2FC value.
        rObj : UMSAPFile
            Reference to the UMSAPFile object.
        rP: float
            Limit for the P values.
        rPickLabel: bool
            Pick labels or show data of selected protein.
        rProtLine : matplotlib object
            Protein line drawn in the FC plot after selecting a protein in the
            wx.ListCtrl.
        rRpC : str
            Currently selected relevant point.
        rS0 : float
            s0 value to calculate the hyperbolic curve
        rShowAll : bool
            Show (True) fcYMax and fcYMin in the FC plot or not (False).
            Default is True.
        rT0: float
            t0 value to calculate the hyperbolic curve
        rVolLines: list[str]
            Lines to plot in the Volcano plot.
        rVXRange : list of float
            Min and Max values for the x axis in the Vol plot.
        rVYRange : list of float
            Min and Max values for the y axis in the Vol plot.
        rZ: float
            Z Value for the Volcano plot.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwProtProf
    cSection = mConfig.nmProtProf
    #------------------------------> Labels
    cLProtLAvail  = 'Displayed Proteins'
    cLProtLShow   = 'Proteins to Label'
    cLFZscore     = 'Z'
    cLFLog2FC     = 'Log2FC'
    cLFPValAbs    = 'P'
    cLFPValLog    = 'pP'
    cLFFCUp       = 'FC > 0'
    cLFFCUpL      = 'FC > 0'
    cLFFCDown     = 'FC < 0'
    cLFFCDownL    = 'FC < 0'
    cLFFCUpMon    = 'FC Incr'
    cLFFCUpMonL   = 'FC Increases'
    cLFFCDownMon  = 'FC Decr'
    cLFFCDownMonL = 'FC Decreases'
    cLFFCNo       = 'FC No Change'
    cLFFCOpposite = 'FC Opposite'
    cLFDiv        = 'FC Diverges'
    cLFCSel       = 'Selected'
    cLFCAny       = 'Any'
    cLFCAll       = 'All'
    cLCol         = ['#', 'Gene', 'Protein']
    cLFFCDict     = {
        cLFFCUp      : cLFFCUpL,
        cLFFCDown    : cLFFCDownL,
        cLFFCUpMon   : cLFFCUpMonL,
        cLFFCDownMon : cLFFCDownMonL,
        cLFFCOpposite: cLFFCOpposite,
        cLFDiv       : cLFDiv,
        cLFFCNo      : cLFFCNo,
    }
    cLFCOpt = {
        cLFCSel : cLFCSel,
        cLFCAny : cLFCAny,
        cLFCAll : cLFCAll,
    }
    #--------------> Id of the plots
    cLNPlot   = ['Vol', 'FC']
    #------------------------------> Title
    cTList = 'Protein List'
    cTText = 'Profiling Details'
    #------------------------------> Sizes
    cSWindow = mConfig.sWinModPlot
    cSCol    = [45, 70, 100]
    #------------------------------> Hints
    cHSearch = 'Protein List'
    #------------------------------> Other
    cNPlotCol = 2
    cImgName   = {
        'Vol': '{}-Vol-{}.pdf',
        'FC' : '{}-Evol-{}.pdf',
    }
    #------------------------------> Color
    cColor = mConfig.confColor[cName]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: 'WindowUMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj            = parent.rObj
        self.rData           = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        #------------------------------>
        self.ReportPlotDataError()
        #------------------------------>
        self.cTitle       = f"{parent.cTitle} - {self.cSection}"
        self.rDf          = pd.DataFrame()
        self.rDateC       = self.rDate[0]
        self.rCondC       = menuData['crp'][self.rDate[0]]['C'][0]
        self.rRpC         = menuData['crp'][self.rDate[0]]['RP'][0]
        self.rGreenP      = None
        self.rCorrP       = False
        self.rShowAll     = True
        self.rAutoFilter  = False
        self.rT0          = 0.1
        self.rS0          = 1.0
        self.rZ           = 10.0
        self.rP           = self.rData[self.rDateC]['Alpha']
        self.rLog2FC      = 0.1
        self.rColor       = 'Hyperbolic Curve Color'
        self.rLockScale   = 'Analysis'
        self.rVXRange     = []
        self.rVYRange     = []
        self.rFcXRange    = []
        self.rFcYRange    = []
        self.rFcXLabel    = []
        self.rProtLine    = []
        self.rFilterList  = []
        self.rLabelProt   = []
        self.rLabelProtD  = {}
        self.rPickLabel   = False
        self.rVolLines    = ['Hyperbolic Curve Line']
        #------------------------------>
        super().__init__(parent, menuData=menuData)
        #------------------------------> Methods
        dKeyMethod = {
            #------------------------------> Set Range of Plots
            'No'          : self.LockScale,
            'Analysis'    : self.LockScale,
            'Project'     : self.LockScale,
            'No Set'      : self.SetRangeNo,
            'Analysis Set': self.SetRangeDate,
            'Project Set' : self.SetRangeProject,
            #------------------------------> Get DF for Text Intensities
            mConfig.oControlTypeProtProf['OC']   : self.GetDF4TextInt_OC,
            mConfig.oControlTypeProtProf['OCC']  : self.GetDF4TextInt_OCC,
            mConfig.oControlTypeProtProf['OCR']  : self.GetDF4TextInt_OCR,
            mConfig.oControlTypeProtProf['Ratio']: self.GetDF4TextInt_RatioI,
            #------------------------------> Colors
            mConfig.kwToolVolPlotColorConf  : self.VolColorConf,
            mConfig.kwToolVolPlotColorScheme: self.VolDraw,
            'Hyperbolic Curve Color'        : self.GetColorHyCurve,
            'P - Log2FC Color'              : self.GetColorPLog2FC,
            'Z Score Color'                 : self.GetColorZScore,
            #------------------------------> Lines
            'Hyperbolic Curve Line': self.DrawLinesHypCurve,
            'P - Log2FC Line'      : self.DrawLinesPLog2FC,
            'Z Score Line'         : self.DrawLinesZScore,
            #------------------------------> Filter methods
            mConfig.lFilFCEvol  : self.Filter_FCChange,
            mConfig.lFilHypCurve: self.Filter_HCurve,
            mConfig.lFilFCLog   : self.Filter_Log2FC,
            mConfig.lFilPVal    : self.Filter_PValue,
            mConfig.lFilZScore  : self.Filter_ZScore,
            'Apply All'         : self.FilterApply,
            'Remove Last'       : self.FilterRemoveLast,
            'Remove Any'        : self.FilterRemoveAny,
            'Remove All'        : self.FilterRemoveAll,
            'Copy'              : self.FilterCopy,
            'Paste'             : self.FilterPaste,
            'Save Filter'       : self.FilterSave,
            'Load Filter'       : self.FilterLoad,
            'AutoApplyFilter'   : self.AutoFilter,
            #------------------------------>
            'Labels'      : self.ClearLabel,
            'Selection'   : self.ClearSel,
            'AllClear'    : self.ClearAll,
            #------------------------------>
            mConfig.kwToolVolPlotLabelPick : self.LabelPick,
            mConfig.kwToolVolPlotLabelProt : self.ProtLabel,
            #------------------------------>
            mConfig.kwToolFCShowAll : self.FCChange,
            #------------------------------>
            mConfig.kwToolExportDataFiltered : self.ExportDataFiltered,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wStatBar.SetFieldsCount(2, [100, -1])
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.wPlot.dPlot['Vol'].rCanvas.mpl_connect('pick_event', self.OnPick)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def StatusBarFilterText(self, text: str) -> bool:
        """Update the StatusBar text.

            Parameters
            ----------
            text : str
                New text to add.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Old Text
        text_now = self.wStatBar.GetStatusText(1)
        #endregion -------------------------------------------------> Old Text

        #region ----------------------------------------------------> Add Text
        text_new = f'{text_now} | {text}'
        #endregion -------------------------------------------------> Add Text

        #region ------------------------------------------> Add to wx.StatusBar
        self.wStatBar.SetStatusText(text_new, 1)
        #endregion ---------------------------------------> Add to wx.StatusBar

        return True
    #---

    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.rDate list and the menuData dict needed to build the Tool
            menu.

            Returns
            -------
            tuple of list and dict
            The list is a list of str with the dates in the analysis.
            The dict has the following structure:
                {
                    'MenuDate' : [List of dates],
                    'crp' : {
                        'date1' : {
                            'C' : [List of conditions],
                            'RP': [List of relevant points],
                        }
                        .......
                        'dateN'
                    }
                }
        """
        #region ---------------------------------------------------> Fill dict
        #------------------------------> Variables
        date = []
        menuData = {'crp' : {}, 'MenuDate': []}
        #------------------------------> Fill
        for k in self.rData.keys():
            if k != 'Error':
                #------------------------------>
                date.append(k)
                #------------------------------>
                menuData['crp'][k] = {
                    'C' : self.rObj.rData[self.cSection][k]['CI']['Cond'],
                    'RP': self.rObj.rData[self.cSection][k]['CI']['RP']
                }
            else:
                pass
        #------------------------------>
        menuData['MenuDate'] = date
        #endregion ------------------------------------------------> Fill dict

        return (date, menuData)
    #---

    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        info = super().WinPos()
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> Set Position
        x = info['D']['xo'] + info['W']['N']*self.cSDeltaWin
        y = (
            ((info['D']['h']/2) - (info['W']['h']/2))
            + info['W']['N']*self.cSDeltaWin
        )
        self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def FillListCtrl(self) -> bool:
        """Update the protein list for the given analysis.

            Returns
            -------
            bool

            Notes
            -----
            Entries are read from self.rDf.
        """
        #region --------------------------------------------------> Delete old
        self.wLC.wLCS.wLC.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old

        #region ----------------------------------------------------> Get Data
        data = self.rDf.iloc[:,0:2]                                             # type: ignore
        data.insert(0, 'kbr', self.rDf.index.values.tolist())
        data = data.astype(str)
        data = data.values.tolist()                                             # type: ignore
        #endregion -------------------------------------------------> Get Data

        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.wLC.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl

        #region ---------------------------------------> Update Protein Number
        self._mgr.GetPane(self.wLC).Caption(f'{self.cTList} ({len(data)})')
        self._mgr.Update()
        #endregion ------------------------------------> Update Protein Number

        return True
    #---

    def GetFCMinMax(self) -> list[list[float]]:
        """Get the maximum and minimum values of FC for each studied RP,
            excluding the CI.

            Returns
            -------
            list of list of float
                First list is the list with the maximum values.
        """
        #region ---------------------------------------------------> Variables
        idx = pd.IndexSlice
        #------------------------------> First point is a control with 0 log2FC
        ymax = [0.0]
        ymin = [0.0]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Fill List
        for c in self.rCI['RP']:
            #------------------------------>
            df = self.rData[self.rDateC]['DF'].loc[:,idx[:,c,'FC']]
            #------------------------------>
            ymax.append(df.max().max())
            ymin.append(df.min().min())
        #endregion ------------------------------------------------> Fill List

        return [ymax, ymin]
    #---

    def VolDraw(self, colorLabel: str='') -> bool:
        """Create/Update the Volcano plot.

            Parameters
            ----------
            colorLabel: str

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rColor = f'{colorLabel} Color' if colorLabel else self.rColor
        #endregion ------------------------------------------------>

        #region --------------------------------------------------------> Axes
        self.VolSetAxis()
        #endregion -----------------------------------------------------> Axes

        #region --------------------------------------------------------> Data
        #------------------------------> X
        x = self.rDf.loc[:,[(self.rCondC,self.rRpC,'FC')]]
        #------------------------------> Y
        if self.rCorrP:
            y = -np.log10(
                self.rDf.loc[:,[(self.rCondC,self.rRpC,'Pc')]])
        else:
            y = -np.log10(
                self.rDf.loc[:,[(self.rCondC,self.rRpC,'P')]])
        #------------------------------> Color
        color = self.dKeyMethod[self.rColor](x, y)                              # type: ignore
        #endregion -----------------------------------------------------> Data

        #region --------------------------------------------------------> Plot
        self.wPlot.dPlot['Vol'].rAxes.scatter(
            x, y,
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = color,
            picker    = True,
        )
        #------------------------------>
        for l in self.rVolLines:
            self.dKeyMethod[l]()                                                # type: ignore
        #------------------------------> Lock Scale or Set it manually
        if self.rVXRange and self.rVYRange:
            self.wPlot.dPlot['Vol'].rAxes.set_xlim(*self.rVXRange)
            self.wPlot.dPlot['Vol'].rAxes.set_ylim(*self.rVYRange)
        else:
            self.VolXYRange(x.squeeze(), y.squeeze())
        #------------------------------> Zoom level
        self.wPlot.dPlot['Vol'].ZoomResetSetValues()
        #------------------------------> Show
        self.wPlot.dPlot['Vol'].rCanvas.draw()
        #endregion -----------------------------------------------------> Plot

        #region -------------------------------------> Update selected protein
        self.DrawGreenPoint()
        #endregion ----------------------------------> Update selected protein

        #region --------------------------------------------------->
        self.AddProtLabel()
        #endregion ------------------------------------------------>

        return True
    #---

    def VolSetAxis(self) -> bool:
        """Set the axis in the volcano plot.

            Returns
            -------
            bool
        """
        #------------------------------> Clear
        self.wPlot.dPlot['Vol'].rAxes.clear()
        #------------------------------>
        self.wPlot.dPlot['Vol'].rAxes.grid(True, linestyle=":")
        #------------------------------> Labels
        self.wPlot.dPlot['Vol'].rAxes.set_title(
            f'C: {self.rCondC} RP: {self.rRpC}')
        self.wPlot.dPlot['Vol'].rAxes.set_xlabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        self.wPlot.dPlot['Vol'].rAxes.set_ylabel(
            "-log$_{10}$[P values]", fontweight="bold")
        #------------------------------>
        return True
    #---

    def DrawGreenPoint(self) -> bool:
        """Draw the green dot in the Volcano plot after selecting a protein in
            the wx.ListCtrl.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Index
        if (idx := self.wLC.wLCS.wLC.GetFirstSelected()) < 0:
            #------------------------------>
            if self.rGreenP is None:
                pass
            else:
                self.rGreenP.remove()
                self.rGreenP = None
            #------------------------------>
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index

        #region ------------------------------------------------> Volcano Plot
        #------------------------------> Get new data
        x = self.rDf.at[self.rDf.index[idx], (self.rCondC, self.rRpC, 'FC')]
        #-------------->
        if self.rCorrP:
            y = -np.log10(
                self.rDf.at[self.rDf.index[idx], (self.rCondC, self.rRpC, 'Pc')])
        else:
            y = -np.log10(
                self.rDf.at[self.rDf.index[idx], (self.rCondC, self.rRpC, 'P')])
        #------------------------------> Remove old point
        if self.rGreenP is None:
            pass
        else:
            self.rGreenP.remove()
        #------------------------------> Add new one
        self.rGreenP = self.wPlot.dPlot['Vol'].rAxes.scatter(
            x, y,
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = self.cColor['VolSel'],
        )
        #------------------------------> Draw
        self.wPlot.dPlot['Vol'].rCanvas.draw()
        #endregion ---------------------------------------------> Volcano Plot

        return True
    #---

    def AddProtLabel(self, draw=False, checkKey=False) -> bool:
        """Add the protein label in the Volcano plot.

            Parameters
            ----------
            draw: bool
                Update (True) or not (False) the canvas.
            checkKey: bool
                Avoid to draw the same key more than twice (True) or not.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.rLabelProt:
            pass
        else:
            if draw:
                self.wPlot.dPlot['Vol'].rCanvas.draw()
            else:
                pass
            return True
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        idx = pd.IndexSlice
        fc = idx[(self.rCondC, self.rRpC, 'FC')]
        if self.rCorrP:
            p = idx[(self.rCondC, self.rRpC, 'Pc')]
        else:
            p = idx[(self.rCondC, self.rRpC, 'P')]
        #------------------------------>
        dX = self.wPlot.dPlot['Vol'].rAxes.get_xlim()
        dX = dX[1] - dX[0]
        dX = dX * 0.002

        dY = self.wPlot.dPlot['Vol'].rAxes.get_ylim()
        dY = dY[1] - dY[0]
        dY = dY * 0.002
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for prot in self.rLabelProt:
            tIdx = int(prot[0])
            tKey = prot[0]
            #------------------------------>
            if tKey in self.rLabelProtD.keys() and checkKey:
                continue
            else:
                pass
            #------------------------------>
            try:
                x,y  = self.rDf.loc[tIdx,[fc,p]].to_numpy().tolist()
            except KeyError:
                continue
            y = -np.log10(y)
            #------------------------------>
            if x > 0:
                self.rLabelProtD[tKey] = self.wPlot.dPlot['Vol'].rAxes.text(
                    x+dX,y-dY, prot[1], va='top')
            else:
                self.rLabelProtD[tKey] = self.wPlot.dPlot['Vol'].rAxes.text(
                    x+dX,y-dY, prot[1], ha='right',va='top')
        #------------------------------>
        self.wPlot.dPlot['Vol'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def FCDraw(self) -> bool:
        """Draw Fold Change Evolution plot.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Axis
        self.FCSetAxis()
        #endregion -----------------------------------------------------> Axis

        #region ----------------------------------------------------> Plot All
        #------------------------------>
        if self.rShowAll:
            #------------------------------>
            color = self.cColor['FCAll']
            x = list(range(0,len(self.rFcYMin)))
            #------------------------------>
            self.wPlot.dPlot['FC'].rAxes.plot(self.rFcYMax, color=color)
            self.wPlot.dPlot['FC'].rAxes.plot(self.rFcYMin, color=color)
            #------------------------------>
            self.wPlot.dPlot['FC'].rAxes.fill_between(
                x, self.rFcYMax, self.rFcYMin, color=color, alpha=0.2)
        else:
            pass
        #------------------------------> Lock Scale
        if self.rFcXRange and self.rFcYRange:
            self.wPlot.dPlot['FC'].rAxes.set_xlim(*self.rFcXRange)
            self.wPlot.dPlot['FC'].rAxes.set_ylim(*self.rFcYRange)
        else:
            xRange, yRange = self.GetFcXYRange(self.rDateC)
            self.wPlot.dPlot['FC'].rAxes.set_xlim(*xRange)
            self.wPlot.dPlot['FC'].rAxes.set_ylim(*yRange)
        #------------------------------> Zoom level
        self.wPlot.dPlot['FC'].ZoomResetSetValues()
        #------------------------------>
        self.wPlot.dPlot['FC'].rCanvas.draw()
        #endregion -------------------------------------------------> Plot All

        #region ----------------------------------------------> Plot Prot Line
        self.DrawProtLine()
        #endregion -------------------------------------------> Plot Prot Line

        return True
    #---

    def FCSetAxis(self) -> bool:
        """Set the axis in the FC plot.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot.dPlot['FC'].rAxes.clear()
        #endregion ----------------------------------------------------> Clear

        #region ------------------------------------------------------> Labels
        self.wPlot.dPlot['FC'].rAxes.grid(True, linestyle=":")
        self.wPlot.dPlot['FC'].rAxes.set_xlabel(
            'Relevant Points', fontweight="bold")
        self.wPlot.dPlot['FC'].rAxes.set_ylabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        #endregion ---------------------------------------------------> Labels

        #region ---------------------------------------------------> X - Axis
        self.wPlot.dPlot['FC'].rAxes.set_xticks(
            range(0, len(self.rFcXLabel), 1))
        self.wPlot.dPlot['FC'].rAxes.set_xticklabels(self.rFcXLabel)
        #endregion ------------------------------------------------> X - Axis

        return True
    #---

    def DrawProtLine(self) -> bool:
        """Draw the protein line in the FC plot after selecting a protein in the
            wx.ListCtrl.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Index
        if (idxL := self.wLC.wLCS.wLC.GetFirstSelected()) < 0:
            #------------------------------>
            if not self.rProtLine:
                pass
            else:
                #------------------------------>
                for k in self.rProtLine:
                    k[0].remove()
                #------------------------------>
                self.rProtLine = []
            #------------------------------>
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index

        #region --------------------------------------------> Remove Old Lines
        #------------------------------>
        for k in self.rProtLine:
            k.remove()
        #------------------------------>
        self.rProtLine = []
        legend = []
        #endregion -----------------------------------------> Remove Old Lines

        #region -----------------------------------------------------> FC Plot
        #------------------------------> Variables
        idx = pd.IndexSlice
        colorN = len(self.cColor['FCLines'])
        x = list(range(0, len(self.rCI['RP'])+1))
        #------------------------------>
        for k,c in enumerate(self.rCI['Cond']):
            #------------------------------> FC values
            y = self.rDf.loc[self.rDf.index[[idxL]],idx[c,:,'FC']]              # type: ignore
            y = [0.0] + y.values.tolist()[0]                                    # type: ignore
            #------------------------------> Errors
            yError = self.rDf.loc[self.rDf.index[[idxL]],idx[c,:,'CI']]         # type: ignore
            yError = [0] + yError.values.tolist()[0]                            # type: ignore
            #------------------------------> Colors
            color = self.cColor['FCLines'][k%colorN]
            #------------------------------> Plot line
            self.rProtLine.append(
                self.wPlot.dPlot['FC'].rAxes.errorbar(
                    x, y, yerr=yError, color=color, fmt='o-', capsize=5
            ))
            #------------------------------> Legend
            legend.append(mpatches.Patch(color=color, label=c))
        #endregion --------------------------------------------------> FC Plot

        #region -------------------------------------------------------> Title
        self.wPlot.dPlot['FC'].rAxes.set_title(f'Protein {idxL}')
        #endregion ----------------------------------------------------> Title

        #region ------------------------------------------------------> Legend
        self.wPlot.dPlot['FC'].rAxes.legend(handles=legend, loc='upper left')
        #endregion ---------------------------------------------------> Legend

        #region --------------------------------------------------------> Draw
        self.wPlot.dPlot['FC'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        return True
    #---

    def SetText(self) -> bool:
        """Set the text with information about the selected protein.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Index
        if self.rLCIdx < 0:                                                     # type: ignore
            #------------------------------>
            self.wText.Freeze()
            self.wText.SetValue('')
            self.wText.Thaw()
            #------------------------------>
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index

        #region ---------------------------------------------------> Add Text
        #------------------------------> Delete all
        self.Freeze()
        self.wText.SetValue('')
        #------------------------------> Protein ID
        number = self.wLC.wLCS.wLC.GetItemText(self.rLCIdx, col=0)
        gene = self.wLC.wLCS.wLC.GetItemText(self.rLCIdx, col=1)
        name = self.wLC.wLCS.wLC.GetItemText(self.rLCIdx, col=2)
        self.wText.AppendText(
            f'--> Selected Protein:\n\n#: {number}, Gene: {gene}, '
            f'Protein ID: {name}\n\n'
        )
        #------------------------------> P and FC values
        self.wText.AppendText('--> P and Log2(FC) values:\n\n')
        self.wText.AppendText(
            self.GetDF4TextPFC(self.rLCIdx).to_string(index=False))             # type: ignore
        self.wText.AppendText('\n\n')
        #------------------------------> Ave and st for intensity values
        self.wText.AppendText(
            '--> Intensity values after data preparation:\n\n')
        dfList = self.dKeyMethod[self.rCI['ControlT']](self.rLCIdx)             # type: ignore
        for df in dfList: # type: ignore
            self.wText.AppendText(df.to_string(index=False))
            self.wText.AppendText('\n\n')
        #------------------------------> Go back to beginning
        self.wText.SetInsertionPoint(0)
        self.Thaw()
        #endregion ------------------------------------------------> Add Text

        return True
    #---

    def GetDF4Text(
        self,
        col : list[str],
        rp  : list[str],
        cond: list[str],
        ) -> pd.DataFrame:
        """Creates the empty dataframe to be used in GetDF4Text functions.

            Parameters
            ----------
            col : list of str
                Name of the columns in the df.
            rp : list of str
                List of relevant points.
            cond : list of str
                List of conditions.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Variables
        nCol = len(col)
        idx = pd.IndexSlice
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------> Multi Index
        #------------------------------>
        a = ['']
        b = ['Conditions']
        #------------------------------>
        for t in rp:
            a = a + nCol * [t]
            b = b + col
        #------------------------------>
        mInd = pd.MultiIndex.from_arrays([a[:], b[:]])
        #endregion -----------------------------------------------> Multi Index

        #region ----------------------------------------------------> Empty DF
        dfo = pd.DataFrame(columns=mInd, index=range(0,len(cond)))
        #endregion -------------------------------------------------> Empty DF

        #region ----------------------------------------------------> Add Cond
        dfo.loc[:,idx[:,'Conditions']] = cond                                   # type: ignore
        #endregion -------------------------------------------------> Add Cond

        return dfo
    #---

    def GetDF4TextPFC(self, pID: int) -> pd.DataFrame:
        """Get the dataframe to print the P and FC +/- CI values to the text.

            Parameters
            ----------
            pID : int
                To select the protein in self.rDf.

            Returns
            -------
            pd.Dataframe
                     RP1            RPN
                     FC (CI)   P
                Cond
                C1   4.5 (0.3) 0.05
                CN
        """
        #region ----------------------------------------------------------> DF
        dfo = self.GetDF4Text(
            ['FC (CI)', 'P'], self.rCI['RP'], self.rCI['Cond'])
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.rCI['Cond']):
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                p = self.rDf.at[self.rDf.index[pID],(c,t,'P')]
                fc = self.rDf.at[self.rDf.index[pID],(c,t,'FC')]
                ci = self.rDf.at[self.rDf.index[pID],(c,t,'CI')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'P')] = p
                dfo.at[dfo.index[k], (t,'FC (CI)')] = f'{fc} ({ci})'
        #endregion -----------------------------------------------> Add Values

        return dfo
    #---

    def GetDF4TextInt_OC(self, pID: int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID : int
                To select the protein in self.rDf.

            Returns
            -------
            list[pd.Dataframe]
                     RP1            RPN
                     FC (CI)   P
                Cond
                C1   4.5 (0.3) 0.05
                CN
        """
        #region ----------------------------------------------------------> DF
        #------------------------------>
        aveC = self.rDf.at[
            self.rDf.index[pID],(self.rCI['Cond'][0], self.rCI['RP'][0], 'aveC')]
        stdC = self.rDf.at[
            self.rDf.index[pID], (self.rCI['Cond'][0], self.rCI['RP'][0], 'stdC')]
        #------------------------------>
        dfc = pd.DataFrame({
            'Condition': self.rCI['ControlL'],
            'Ave'      : [aveC],
            'Std'      : [stdC]
        })
        #endregion -------------------------------------------------------> DF

        #region ---------------------------------------------------------> DFO
        dfo = self.GetDF4TextInt_RatioI(pID)
        #endregion ------------------------------------------------------> DFO

        return [dfc] + dfo
    #---

    def GetDF4TextInt_OCC(self, pID: int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control per Column.

            Parameters
            ----------
            pID : int
                To select the protein in self.rDf.

            Returns
            -------
            list[pd.Dataframe]
                        RP1      RPN
                        ave  std
                Cond
                Control 4.5 0.05
                C1
                CN
        """
        #region ----------------------------------------------------------> DF
        dfo = self.GetDF4Text(
            ['Ave', 'Std'], self.rCI['RP'], self.rCI['ControlL']+self.rCI['Cond'])
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for c in self.rCI['Cond']:
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                aveC = self.rDf.at[self.rDf.index[pID],(c,t,'aveC')]
                stdC = self.rDf.at[self.rDf.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[0], (t,'Ave')] = aveC
                dfo.at[dfo.index[0], (t,'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.rCI['Cond'], start=1):
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                ave = self.rDf.at[self.rDf.index[pID],(c,t,'ave')]
                std = self.rDf.at[self.rDf.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values

        return [dfo]
    #---

    def GetDF4TextInt_OCR(self, pID: int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID : int
                To select the protein in self.rDf.

            Returns
            -------
            list[pd.Dataframe]
                     RP1            RPN
                     FC (CI)   P
                Cond
                C1   4.5 (0.3) 0.05
                CN
        """
        #region ----------------------------------------------------------> DF
        dfo = self.GetDF4Text(
            ['Ave', 'Std'], self.rCI['ControlL']+self.rCI['RP'], self.rCI['Cond'])
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for k,c in enumerate(self.rCI['Cond']):
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                aveC = self.rDf.at[self.rDf.index[pID],(c,t,'aveC')]
                stdC = self.rDf.at[self.rDf.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (self.rCI['ControlL'],'Ave')] = aveC
                dfo.at[dfo.index[k], (self.rCI['ControlL'],'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.rCI['Cond']):
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                ave = self.rDf.at[self.rDf.index[pID],(c,t,'ave')]
                std = self.rDf.at[self.rDf.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values

        return [dfo]
    #---

    def GetDF4TextInt_RatioI(self, pID: int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID : int
                To select the protein in self.rDf

            Returns
            -------
            list[pd.Dataframe]
                     RP1            RPN
                     FC (CI)   P
                Cond
                C1   4.5 (0.3) 0.05
                CN
        """
        #region ----------------------------------------------------------> DF
        dfo = self.GetDF4Text(['Ave', 'Std'], self.rCI['RP'], self.rCI['Cond'])
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.rCI['Cond']):
            for t in self.rCI['RP']:
                #------------------------------> Get Values
                ave = self.rDf.at[self.rDf.index[pID],(c,t,'ave')]
                std = self.rDf.at[self.rDf.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values

        return [dfo]
    #---

    def SetRangeNo(self) -> bool:
        """Do nothing. Just to make the dict self.dKeyMethod work.

            Returns
            -------
            bool
        """
        return True
    #---

    def SetRangeDate(self):
        """Set Plot Range to the range in the given date.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Vol Range
        self.rVXRange, self.rVYRange = self.GetVolXYRange(self.rDateC)
        #endregion ------------------------------------------------> Vol Range

        #region ----------------------------------------------------> FC Range
        self.rFcXRange, self.rFcYRange = self.GetFcXYRange(self.rDateC)
        #endregion -------------------------------------------------> FC Range

        return True
    #---

    def SetRangeProject(self):
        """Set Plot Range to the range in the given project.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        vXLim  = 0
        vYMin  = 0
        vYMax  = 0
        fcXMin = 0
        fcXMax = 0
        fcYMin = 0
        fcYMax = 0
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Range
        #------------------------------> Get larger range in project
        for date in self.rDate:
            #------------------------------>
            x,y = self.GetVolXYRange(date)
            xFC, yFC = self.GetFcXYRange(date)
            #------------------------------>
            vXLim = x[1] if x[1] >= vXLim else vXLim
            vYMin = y[0] if y[0] <= vYMin else vYMin
            vYMax = y[1] if y[1] >= vYMax else vYMax
            #------------------------------>
            fcXMin = xFC[0] if xFC[0] <= fcXMin else fcXMin
            fcXMax = xFC[1] if xFC[1] >= fcXMax else fcXMax
            fcYMin = yFC[0] if yFC[0] <= fcYMin else fcYMin
            fcYMax = yFC[1] if yFC[1] >= fcYMax else fcYMax
        #------------------------------> Set attributes
        self.rVXRange = [-vXLim, vXLim]
        self.rVYRange = [vYMin, vYMax]
        #------------------------------>
        self.rFcXRange = [fcXMin, fcXMax]
        self.rFcYRange = [fcYMin, fcYMax]
        #endregion ----------------------------------------------------> Range

        return True
    #---

    def GetVolXYRange(self, date: str) -> list[list[float]]:
        """Get the XY range for the volcano plot for the given date.

            Parameters
            ----------
            date : str
                A valid date from the project.

            Returns
            -------
            list of list of floats
                [xRange, yRange] e.g. [[-0.3, 0.3], [-0.1, 4.5]]
        """
        #region ---------------------------------------------------> Variables
        idx = pd.IndexSlice
        #------------------------------>
        x = self.rData[date]['DF'].loc[:, idx[:,:,'FC']]
        #------------------------------>
        if self.rCorrP:
            y = self.rData[date]['DF'].loc[:, idx[:,:,'Pc']]
        else:
            y = self.rData[date]['DF'].loc[:, idx[:,:,'P']]
        #------------------------------>
        y = -np.log10(y)
        #------------------------------>
        xRange = []
        yRange = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Get Range
        #------------------------------> X
        xmin = abs(x.min().min())
        xmax = abs(x.max().max())
        #-------------->  To make it symmetric
        if xmin >= xmax:
            lim = xmin
        else:
            lim = xmax
        #-------------->
        dm = 2 * lim * mConfig.confGeneral['MatPlotMargin']
        #-------------->
        xRange.append(-lim - dm)
        xRange.append(lim + dm)
        #------------------------------> Y
        ymax = y.max().max()
        #-------------->
        dm = 2 * ymax * mConfig.confGeneral['MatPlotMargin']
        #-------------->
        yRange.append(0 - dm)
        yRange.append(ymax + dm)
        #endregion ------------------------------------------------> Get Range

        return [xRange, yRange]
    #---

    def GetFcXYRange(self, date: str) -> list[list[float]]:
        """Get the XY range for the FC plot, including the CI.

            Parameters
            ----------
            date : str
                The selected date.

            Returns
            -------
            list of list of floats
                [xRange, yRange] e.g. [[-0.3, 3.3], [-0.1, 4.5]]
        """
        #region ---------------------------------------------------> Variables
        idx = pd.IndexSlice
        #------------------------------>
        y = self.rData[date]['DF'].loc[:, idx[:,:,'FC']]
        yCI = self.rData[date]['DF'].loc[:, idx[:,:,'CI']]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Get Range
        #------------------------------> X
        dm = len(self.rCI['RP']) * mConfig.confGeneral['MatPlotMargin']
        #-------------->
        xRange = [-dm, len(self.rCI['RP'])+dm]
        #------------------------------> Y
        #-------------->
        yMax  = y.max().max()
        yMin  = y.min().min()
        ciMax = yCI.max().max()
        #-------------->
        yminLim = yMin - ciMax
        ymaxLim = yMax + ciMax
        #-------------->
        dm = (ymaxLim - yminLim) * mConfig.confGeneral['MatPlotMargin']
        #-------------->
        yRange = [yminLim - dm, ymaxLim + dm]
        #endregion ------------------------------------------------> Get Range

        return [xRange, yRange]
    #---

    def VolXYRange(self, x, y) -> bool:
        """Get the XY range for the volcano plot based on the x,y values.

            Parameters
            ----------
            x : pd.Series or list
                Values for x.
            y : pd.Series or list
                Values for y.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Check input
        if isinstance(x, pd.Series):
            if x.empty:
                x = [-1, 1]
                y = [-1, 1]
            elif x.shape[0] == 1:
                x = [-x.iloc[0], x.iloc[0]]
                y = [-y.iloc[0], y.iloc[0]]
            else:
                pass
        else:
            x = [-x, x]
            y = [-y, y]
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Get Range
        xR = mStatistic.DataRange(x, margin=mConfig.confGeneral['MatPlotMargin'])
        yR = mStatistic.DataRange(y, margin=mConfig.confGeneral['MatPlotMargin'])
        #endregion ------------------------------------------------> Get Range

        #region ---------------------------------------------------> Set Range
        self.wPlot.dPlot['Vol'].rAxes.set_xlim(*xR)
        self.wPlot.dPlot['Vol'].rAxes.set_ylim(*yR)
        #endregion ------------------------------------------------> Set Range

        return True
    #---

    def DrawLinesHypCurve(self) -> bool:
        """Draw the Hyperbolic Curve in the Volcano Plot.

            Returns
            -------
            bool
        """
        lim = self.rT0*self.rS0
        xCP = np.arange(lim+0.001, 20, 0.001)
        yCP = abs((abs(xCP)*self.rT0)/(abs(xCP)-lim))
        self.wPlot.dPlot['Vol'].rAxes.plot(
            xCP,  yCP, color=self.cColor['CV'])
        self.wPlot.dPlot['Vol'].rAxes.plot(
            -xCP, yCP, color=self.cColor['CV'])
        return True
    #---

    def DrawLinesPLog2FC(self) -> bool:
        """Draw the P - Log2FC lines in the Volcano Plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        p = -np.log10(self.rP)
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.wPlot.dPlot['Vol'].rAxes.hlines(
            p, -100, 100, color=self.cColor['CV'])
        self.wPlot.dPlot['Vol'].rAxes.vlines(
            self.rLog2FC, -100, 100, color=self.cColor['CV'])
        self.wPlot.dPlot['Vol'].rAxes.vlines(
            -self.rLog2FC, -100, 100, color=self.cColor['CV'])
        #endregion ------------------------------------------------>

        return True
    #---

    def DrawLinesZScore(self) -> bool:
        """Draw no lines. Needed for completion.

            Returns
            -------
            bool
        """
        return True
    #---

    def GetColorHyCurve(self, *args) -> list:
        """Get color for Volcano plot when schemes is Hyp Curve.

            Returns
            -------
            list
                List with a color for each protein.
        """
        #region ---------------------------------------------------> Variables
        color = []
        lim = self.rT0*self.rS0
        x = args[0]
        y = args[1]
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Color
        for k,v in enumerate(x.values):
            if v < -lim:
                if abs((abs(v)*self.rT0)/(abs(v)-lim)) < y.values[k]:
                    color.append(self.cColor['Vol'][0])
                else:
                    color.append(self.cColor['Vol'][1])
            elif v > lim:
                if abs((abs(v)*self.rT0)/(abs(v)-lim)) < y.values[k]:
                    color.append(self.cColor['Vol'][2])
                else:
                    color.append(self.cColor['Vol'][1])
            else:
                color.append(self.cColor['Vol'][1])
        #endregion ----------------------------------------------------> Color

        #region --------------------------------------------------->
        self.rVolLines = ['Hyperbolic Curve Line']
        #endregion ------------------------------------------------>

        return color
    #---

    def GetColorZScore(self, *args) -> list:                                    # pylint: disable=unused-argument
        """Get the color by z value.

            Returns
            -------
            list
                List of colors.
        """
        #region ---------------------------------------------------> Variables
        zVal = stats.norm.ppf(1.0-(self.rZ/100.0))
        #------------------------------>
        idx = pd.IndexSlice
        col = idx[self.rCondC,self.rRpC,'FCz']
        val = self.rDf.loc[:,col]                                               # type: ignore
        #------------------------------>
        cond = [val < -zVal, val > zVal]
        choice = [self.cColor['Vol'][0], self.cColor['Vol'][2]]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.rVolLines = ['Z Score Line']
        #endregion ------------------------------------------------>

        return np.select(cond, choice, default=self.cColor['Vol'][1])           # type: ignore
    #---

    def GetColorPLog2FC(self, *args) -> list:                                   # pylint: disable=unused-argument
        """Get the color by P - Log2FC.

            Returns
            -------
            list
                List of colors
        """
        #region -------------------------------------------------------->
        idx = pd.IndexSlice
        colP = idx[self.rCondC, self.rRpC,'P']
        valP = self.rDf.loc[:,colP]                                             # type: ignore
        colF = idx[self.rCondC, self.rRpC,'FC']
        valF = self.rDf.loc[:,colF]                                             # type: ignore
        cond = [(valP < self.rP) & (valF < -self.rLog2FC),
                (valP < self.rP) & (valF > self.rLog2FC),]
        choice = [self.cColor['Vol'][0], self.cColor['Vol'][2]]
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.rVolLines = ['P - Log2FC Line']
        #endregion ------------------------------------------------>

        return np.select(cond, choice, default=self.cColor['Vol'][1])           # type: ignore
    #---

    def PickLabel(self, ind: list[int]) -> bool:
        """Show label for the picked protein.

            Parameters
            ----------
            ind: list[int]

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        col = [('Gene','Gene','Gene'),('Protein','Protein','Protein')]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for k in ind:
            idx = self.rDf.index[k]
            idxS = str(idx)
            row = [idxS]+self.rDf.loc[idx,col].to_numpy().tolist()
            if row in self.rLabelProt:
                self.rLabelProtD[idxS].remove()
                self.rLabelProtD.pop(idxS)
                self.rLabelProt.remove(row)
            else:
                self.rLabelProt.append(row)
        #------------------------------>
        self.AddProtLabel(draw=True, checkKey=True)
        #endregion ------------------------------------------------>

        return True
    #---

    def PickShow(self, ind: list[int]) -> bool:
        """Show info about the picked protein.

            Parameters
            ----------
            ind: list[int]

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Pick
        if len(ind) == 1:
            self.wLC.wLCS.wLC.Select(ind[0], on=1)
            self.wLC.wLCS.wLC.EnsureVisible(ind[0])
            self.wLC.wLCS.wLC.SetFocus()
            self.OnListSelect('fEvent')
        else:
            #------------------------------> Disconnect events to avoid zoom in
            # while interacting with the modal window
            self.wPlot.dPlot['Vol'].DisconnectEvent()
            #------------------------------> sort ind
            ind = sorted(ind, key=int)
            #------------------------------>
            msg = ('The selected point is an overlap of several proteins.')
            tException = (
                'The numbers of the proteins included in the selected '
                'point are:\n {str(ind)[1:-1]}')
            DialogNotification(
                'warning',
                msg        = msg,
                setText    = True,
                tException = tException,
                parent     = self.wPlot.dPlot['Vol'],
            )
            #------------------------------> Reconnect event
            self.wPlot.dPlot['Vol'].ConnectEvent()
            return False
        #endregion ------------------------------------------------> Pick

        return True
    #---

    def UpdateResultWindow(
        self,
        tDate  : str='',
        cond   : str='',
        rp     : str='',
        corrP  : Optional[bool]=None,
        showAll: Optional[bool]=None,
        t0     : Optional[float]=None,
        s0     : Optional[float]=None
        ) -> bool:
        """Configure window to update Volcano and FC plots when date changes.

            Parameters
            ----------
            tDate : str
                Selected date.
            cond : str
                Selected condition.
            rp : str
                Selected relevant point.
            corrP : bool
                Use corrected P values (True) or not (False).
            showAll : bool
                Show FC range of values or not.
            to: float
                T0 value for the calculation of the hyperbolic curve.
            so: float
                S0 value for the calculation of the hyperbolic curve.

            Returns
            -------
            bool
        """
        #region --------------------------------------------> Update variables
        self.rDateC      = tDate if tDate else self.rDateC
        self.rCondC      = cond if cond else self.rCondC
        self.rRpC        = rp if rp else self.rRpC
        self.rCorrP      = corrP if corrP is not None else self.rCorrP
        self.rShowAll    = showAll if showAll is not None else self.rShowAll
        self.rT0         = t0 if t0 is not None else self.rT0
        self.rS0         = s0 if s0 is not None else self.rS0
        self.rCI         = self.rObj.rData[self.cSection][self.rDateC]['CI']
        self.rDf         = self.rData[self.rDateC]['DF'].copy()
        self.rLabelProt  = [] if tDate else self.rLabelProt
        self.rLabelProtD = {} if tDate else self.rLabelProtD
        #endregion -----------------------------------------> Update variables

        #region --------------------------------------------------> Update GUI
        if self.rAutoFilter:
            self.FilterApply(reset=False)
        else:
            pass
        #------------------------------> Clean & Reload Protein List
        self.FillListCtrl()
        #------------------------------> Clean text
        self.wText.SetValue('')
        #endregion -----------------------------------------------> Update GUI

        #region -------------------------------------------> Update FC x label
        self.rFcXLabel = self.rCI['ControlL'] + self.rCI['RP']
        #endregion ----------------------------------------> Update FC x label

        #region ---------------------------------------------------> FC minMax
        self.rFcYMax, self.rFcYMin = self.GetFCMinMax()
        #endregion ------------------------------------------------> FC minMax

        #region --------------------------------------------------> Lock Scale
        if self.rLockScale:
            self.LockScale(self.rLockScale)
        else:
            pass
        #endregion -----------------------------------------------> Lock Scale

        #region ---------------------------------------------------------> Vol
        self.VolDraw()
        #endregion ------------------------------------------------------> Vol

        #region ----------------------------------------------------------> FC
        self.FCDraw()
        #endregion -------------------------------------------------------> FC

        #region ------------------------------------------------------> Title
        self.PlotTitle()
        #endregion ---------------------------------------------------> Title

        return True
    #---

    def LockScale(self, mode: str, updatePlot: bool=True) -> bool:
        """Lock the scale of the volcano and FC plot.

            Parameters
            ----------
            mode : str
                One of No, Date, Project
            updatePlot : bool
                Apply the new axis limit ot the plots (True) or not.
                Default is True.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Update Attr
        self.rLockScale = mode
        self.rVXRange   = []
        self.rVYRange   = []
        self.rFcXRange  = []
        self.rFcYRange  = []
        #endregion ----------------------------------------------> Update Attr

        #region ---------------------------------------------------> Get Range
        self.dKeyMethod[f'{mode} Set']()                                        # type: ignore
        #endregion ------------------------------------------------> Get Range

        #region ---------------------------------------------------> Set Range
        if updatePlot:
            #------------------------------> Vol
            #-------------->
            self.wPlot.dPlot['Vol'].rAxes.set_xlim(*self.rVXRange)
            self.wPlot.dPlot['Vol'].rAxes.set_ylim(*self.rVYRange)
            #-------------->
            self.wPlot.dPlot['Vol'].rCanvas.draw()
            #-------------->
            self.wPlot.dPlot['Vol'].ZoomResetSetValues()
            #------------------------------> FC
            #-------------->
            self.wPlot.dPlot['FC'].rAxes.set_xlim(*self.rFcXRange)
            self.wPlot.dPlot['FC'].rAxes.set_ylim(*self.rFcYRange)
            #-------------->
            self.wPlot.dPlot['FC'].rCanvas.draw()
            #-------------->
            self.wPlot.dPlot['FC'].ZoomResetSetValues()
        else:
            pass
        #endregion ------------------------------------------------> Set Range

        return True
    #---

    def UpdateGUI(self) -> bool:
        """Update content of the wx.ListCtrl and Plots

            Returns
            -------
            bool
        """
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        return True
    #---

    def ExportImgAll(self) -> bool:
        """Export all plots to a pdf image.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = DialogDirSelect(parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            try:
                for k, v in self.wPlot.dPlot.items():
                    #------------------------------>
                    if k == 'Vol':
                        nameP = f'{self.rCondC}-{self.rRpC}'
                    else:
                        nameP = f'{self.rLCIdx}'
                    #------------------------------> file path
                    fPath = p / self.cImgName[k].format(self.rDateC, nameP)
                    #------------------------------> Write
                    v.rFigure.savefig(fPath)
            except Exception as e:
                DialogNotification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Images'),
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---

    def LabelPick(self) -> bool:
        """

            Returns
            -------
            bool
        """
        self.rPickLabel = not self.rPickLabel
        return True
    #---

    def ProtLabel(self) -> bool:
        """

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        data = self.rDf.iloc[:,0:2]                                             # type: ignore
        data.insert(0, 'kbr', self.rDf.index.values.tolist())
        data = data.astype(str)
        data = data.values.tolist()                                             # type: ignore
        #endregion ------------------------------------------------>

        #region -------------------------------------------------> Get New Sel
        #------------------------------> Create the window
        dlg = DialogListSelect(
            data,
            self.cLCol,
            self.cSCol,
            tSelOptions = self.rLabelProt,
            title       = 'Select Proteins',
            tBtnLabel   = 'Add Protein',
            color       = mConfig.confColor['Zebra'],
            tStLabel    = [self.cLProtLAvail, self.cLProtLShow],
        )
        #------------------------------> Get the selected values
        if dlg.ShowModal():
            #------------------------------>
            rowN = dlg.wLCtrlO.GetItemCount()
            rowL = [dlg.wLCtrlO.GetRowContent(x) for x in range(0, rowN)]
            #------------------------------>
            for z in reversed(self.rLabelProt):
                if z not in rowL:
                    self.rLabelProtD[z[0]].remove()
                    self.rLabelProtD.pop(z[0])
                    self.rLabelProt.remove(z)
                else:
                    pass
            #------------------------------>
            for y in rowL:
                if y in self.rLabelProt:
                    pass
                else:
                    self.rLabelProt.append(y)
        else:
            pass
        #endregion ----------------------------------------------> Get New Sel

        #region -------------------------------------------------------->
        self.AddProtLabel(draw=True, checkKey=True)
        #endregion ----------------------------------------------------->

        dlg.Destroy()
        return True
    #---

    def VolColorConf(self) -> bool:
        """Adjust the color scheme for the proteins.

            Returns
            -------
            bool
        """
        #------------------------------>
        dlg = DialogVolColorScheme(
            self.rT0,
            self.rS0,
            self.rZ,
            self.rP,
            self.rLog2FC,
            parent=self,
        )
        #------------------------------>
        if dlg.ShowModal():
            self.rT0, self.rS0, self.rP, self.rLog2FC, self.rZ = (
                dlg.GetVal())
            self.VolDraw()
        else:
            return False
        #------------------------------>
        dlg.Destroy()
        return True
    #---

    def FCChange(self, showAll: bool) -> bool:
        """Configure window to plot FC Evolution.

            Parameters
            ----------
            showAll : bool
                Show FC range of values or not.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rShowAll = showAll
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Plot
        self.FCDraw()
        #endregion -----------------------------------------------------> Plot

        return True
    #---

    def ClearSel(self) -> bool:
        """Clear selection.

            Returns
            -------
            bool
        """
        if self.rLCIdx is not None:
            #------------------------------>
            self.wLC.wLCS.wLC.Select(self.rLCIdx, on=0)
            self.rLCIdx = None
            #------------------------------>
            self.rGreenP.remove()                                               # type: ignore
            self.rGreenP = None
            self.wPlot.dPlot['Vol'].rCanvas.draw()
            #------------------------------>
            self.FCDraw()
            #------------------------------>
            self.wText.Clear()
        else:
            pass
        return True
    #---

    def ClearLabel(self) -> bool:
        """Clear Labels.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        for t in self.rLabelProtD.values():
            t.remove()
        #------------------------------>
        self.rLabelProtD = {}
        self.rLabelProt = []
        #------------------------------>
        self.wPlot.dPlot['Vol'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearAll(self) -> bool:
        """Clear All selections.

            Returns
            -------
            bool
        """
        self.ClearSel()
        self.ClearLabel()
        return True
    #---

    def UpdateStatusBarFilterText(self) -> bool:
        """Update the filter list in the statusbar.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Delete
        self.wStatBar.SetStatusText('', 1)
        #endregion ---------------------------------------------------> Delete

        #region ---------------------------------------------------------> Add
        for k in self.rFilterList:
            self.StatusBarFilterText(k[2])
        #endregion ------------------------------------------------------> Add

        return True
    #---

    def AutoFilter(self, mode: bool) -> bool:
        """Auto apply filter when changing date.

            Parameters
            ----------
            mode : bool
                Apply filters (True) or not (False).

            Returns
            -------
            bool
        """
        self.rAutoFilter = mode
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region ---------------------------------------------------> Event Methods
    def OnPick(self, event) -> bool:
        """Process a pick event in the volcano plot.

            Parameters
            ----------
            event: matplotlib pick event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        ind = event.ind
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Pick
        if self.rPickLabel:
            return self.PickLabel(ind)
        else:
            return self.PickShow(ind)
        #endregion ------------------------------------------------> Pick
    #---

    def OnListSelect(self, event: Union[wx.CommandEvent, str]) -> bool:
        """Select an element in the wx.ListCtrl.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Check Sel
        super().OnListSelect(event)
        #endregion ------------------------------------------------> Check Sel

        #region ------------------------------------------------> Volcano Plot
        self.DrawGreenPoint()
        #endregion ---------------------------------------------> Volcano Plot

        #region ------------------------------------------------> FC Evolution
        self.DrawProtLine()
        #endregion ---------------------------------------------> FC Evolution

        #region --------------------------------------------------------> Text
        self.SetText()
        #endregion -----------------------------------------------------> Text

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Filter Methods
    def Filter_FCChange(self, choice: dict={}, updateL: bool=True) -> bool:     # pylint: disable=dangerous-default-value
        """Filter results based on FC evolution.

            Parameters
            ----------
            choice : dict
                Keys are int 0 to 1. Value in 0 is the filter to apply and
                in 1 the conditions to consider.
            updateL : bool
                Update (True) or not (False) the GUI. Default is True.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Get Value
        if choice:
            choice0, choice1 = choice.values()
        else:
            dlg = DialogMultipleCheckBox(
                'Filter results by FC evolution.',
                [self.cLFFCDict, self.cLFCOpt],
                [2, 3],
                label       = ['Options', 'Conditions to use'],
                multiChoice = [False, False],
                parent      = self,
            )
            #------------------------------>
            if dlg.ShowModal():
                #------------------------------>
                choice = dlg.GetChoice() # The value of choice is needed below
                choice0, choice1 = choice.values()
                #------------------------------>
                dlg.Destroy()
            else:
                dlg.Destroy()
                return False
        #endregion ------------------------------------------------> Get Value

        #region ----------------------------------------------------------> DF
        idx = pd.IndexSlice
        #------------------------------>
        if choice1 == self.cLFCSel:
            df = self.rDf.loc[:,idx[self.rCondC,:,'FC']]                        # type: ignore
        else:
            df = self.rDf.loc[:,idx[:,:,'FC']]                                  # type: ignore
        #------------------------------>
        if choice0 == self.cLFFCUp:
            mask = df.groupby(level=0, axis=1).apply(lambda x: (x > 0).all(axis=1))                                                                                     # type: ignore
        elif choice0 == self.cLFFCDown:
            mask = df.groupby(level=0, axis=1).apply(lambda x: (x < 0).all(axis=1))                                                                                     # type: ignore
        elif choice0 == self.cLFFCNo:
            # pylint disable=invalid-unary-operand-type
            mask = df.groupby(level=0, axis=1).apply(lambda x: ((x > -self.rT0*self.rS0) & (x < self.rT0*self.rS0)).all(axis=1))                                        # type: ignore
        elif choice0 == self.cLFFCUpMon:
            mask = df.groupby(level=0, axis=1).apply(lambda x: x.apply(lambda x: ((x.is_monotonic_increasing) & (x > 0)).all(), axis=1))                                # type: ignore
        elif choice0 == self.cLFFCDownMon:
            mask = df.groupby(level=0, axis=1).apply(lambda x: x.apply(lambda x: ((x.is_monotonic_decreasing) & (x < 0)).all(), axis=1))                                # type: ignore
        elif choice0 == self.cLFDiv:
            maskUp = self.rDf.loc[:,idx[:,:,'FC']].groupby(level=0, axis=1).apply(lambda x: x.apply(lambda x: ((x.is_monotonic_increasing) & (x > 0)).all(), axis=1))   # type: ignore
            maskUp = maskUp.any(axis=1)                                                                                                                                 # type: ignore
            maskDown = self.rDf.loc[:,idx[:,:,'FC']].groupby(level=0, axis=1).apply(lambda x: x.apply(lambda x: ((x.is_monotonic_decreasing) & (x < 0)).all(), axis=1)) # type: ignore
            maskDown = maskDown.any(axis=1)                                                                                                                             # type: ignore
        elif choice0 == self.cLFFCOpposite:
            maskUp = self.rDf.loc[:,idx[:,:,'FC']].groupby(level=0, axis=1).apply(lambda x: (x > 0).all(axis=1))                                                        # type: ignore
            maskUp = maskUp.any(axis=1)                                                                                                                                 # type: ignore
            maskDown = self.rDf.loc[:,idx[:,:,'FC']].groupby(level=0, axis=1).apply(lambda x: (x < 0).all(axis=1))                                                      # type: ignore
            maskDown = maskDown.any(axis=1)                                                                                                                             # type: ignore
        else:
            return False
        #------------------------------>
        if choice0 not in [self.cLFDiv, self.cLFFCOpposite]:
            if choice1 == self.cLFCAny:
                mask = mask.any(axis=1)                                         # type: ignore
            else:
                mask = mask.all(axis=1)                                         # type: ignore
        else:
            mask = pd.concat([maskUp, maskDown], axis=1).all(axis=1)            # type: ignore
        #------------------------------>
        self.rDf = self.rDf[mask]
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Update GUI
        if updateL:
            self.UpdateGUI()
            #------------------------------>
            self.StatusBarFilterText(f'{choice0} ({choice1[0:3]})')
            #------------------------------>
            self.rFilterList.append(
                [mConfig.lFilFCEvol,
                 {'choice':choice, 'updateL': False},
                 f'{choice0} ({choice1[0:3]})']
            )
        else:
            pass
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def Filter_HCurve(self, updateL: bool=True, **kwargs) -> bool:              # pylint: disable=unused-argument
        """Filter results based on Hyperbolic Curve.

            Parameters
            ----------
            updateL : bool
                Update (True) or not (False) the GUI. Default is True.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        filterText = mConfig.lFilHypCurve
        lim = self.rT0 * self.rS0
        fc = self.rDf.loc[:,[(self.rCondC,self.rRpC,'FC')]]
        p = -np.log10(self.rDf.loc[:,[(self.rCondC,self.rRpC,'P')]])
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> H Curve
        cond = [fc < -lim, fc > lim]
        choice = [
            mMethod.HCurve(fc, self.rT0, self.rS0),
            mMethod.HCurve(fc, self.rT0, self.rS0),
        ]
        pH = np.select(cond, choice, np.nan)
        #endregion ------------------------------------------------> H Curve

        #region ---------------------------------------------------> Filter
        cond = [pH < p, pH > p]
        choice = [True, False]
        npBool = np.select(cond, choice)
        npBool = npBool.astype(bool)
        self.rDf = self.rDf[npBool]
        #endregion ------------------------------------------------> Filter

        #region --------------------------------------------------> Update GUI
        if updateL:
            self.UpdateGUI()
            #------------------------------>
            self.StatusBarFilterText(f'{filterText}')
            #------------------------------>
            self.rFilterList.append(
                [filterText,
                 {'choice':filterText, 'updateL': False},
                 f'{filterText}']
            )
        else:
            pass
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def Filter_Log2FC(self, gText: str='', updateL: bool=True) -> bool:
        """Filter results by log2FC.

            Parameters
            ----------
            gText : str
                FC threshold and operand, e.g. < 10 or > 3.4
            updateL : bool
                Update filterList and StatusBar (True) or not (False)

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            #------------------------------>
            dlg = DialogUserInputText(
                'Filter results by Log2(FC) value.',
                ['Threshold'],
                ['log2(FC) value. e.g. < 2.3 or > -3.5'],
                [mValidator.Comparison(numType='float', op=['<', '>'])],
                parent = self,
            )
            #------------------------------>
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.GetValue()
                #------------------------------>
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        #endregion -------------------------------------------> Text Entry Dlg

        #region ------------------------------------------> Get Value and Plot
        op, val = uText[0].strip().split()
        val = float(val)
        #------------------------------>
        idx = pd.IndexSlice
        col = idx[self.rCondC,self.rRpC,'FC']
        if op == '<':
            self.rDf = self.rDf[self.rDf[col] <= val]
        else:
            self.rDf = self.rDf[self.rDf[col] >= val]
        #endregion ---------------------------------------> Get Value and Plot

        #region ------------------------------------------> Update Filter List
        if updateL:
            self.UpdateGUI()
            #------------------------------>
            self.StatusBarFilterText(f'{self.cLFLog2FC} {op} {val}')
            #------------------------------>
            self.rFilterList.append(
                [mConfig.lFilFCLog,
                 {'gText': uText, 'updateL': False},
                 f'{self.cLFLog2FC} {op} {val}']
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List

        return True
    #---

    def Filter_PValue(
        self,
        gText  : str='',
        absB   : Optional[bool]=None,
        updateL: bool=True,
        ) -> bool:
        """Filter results by P value.

            Parameters
            ----------
            gText : str
                P value threshold and operand, e.g. < 10 or > 3.4
            absB : bool
                Use absolute values (True) or -log10 values (False)
            updateL : bool
                Update filterList and StatusBar (True) or not (False)

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            dlg = DialogFilterPValue(
                'Filter results by P value.',
                'Threshold',
                'Absolute or -log10(P) value. e.g. < 0.01 or > 1',
                self.wPlot.dPlot['Vol'],
                mValidator.Comparison(numType='float', op=['<', '>'], vMin=0),
            )
            #------------------------------>
            if dlg.ShowModal():
                #------------------------------>
                uText, absB  = dlg.GetValue()
                #------------------------------>
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        #endregion -------------------------------------------> Text Entry Dlg

        #region ------------------------------------------> Get Value and Plot
        op, val = uText.strip().split()
        val = float(val)
        #------------------------------> Apply to regular or corrected P values
        idx = pd.IndexSlice
        if self.rCorrP:
            col = idx[self.rCondC,self.rRpC,'Pc']
        else:
            col = idx[self.rCondC,self.rRpC,'P']
        #------------------------------> Given value is abs or -log10 P value
        df = self.rDf.copy()
        if absB:
            pass
        else:
            df.loc[:,col] = -np.log10(df.loc[:,col])                            # type: ignore
        #------------------------------>
        if op == '<':
            self.rDf = self.rDf[df[col] <= val]
        else:
            self.rDf = self.rDf[df[col] >= val]
        #endregion ---------------------------------------> Get Value and Plot

        #region ------------------------------> Update Filter List & StatusBar
        if updateL:
            self.UpdateGUI()
            #------------------------------>
            label = self.cLFPValAbs if absB else self.cLFPValLog
            #------------------------------>
            self.StatusBarFilterText(f'{label} {op} {val}')
            #------------------------------>
            self.rFilterList.append(
                [mConfig.lFilPVal,
                 {'gText': uText, 'absB': absB, 'updateL': False},
                 f'{label} {op} {val}']
            )
        else:
            pass
        #endregion ---------------------------> Update Filter List & StatusBar

        return True
    #---

    def Filter_ZScore(self, gText: str='', updateL: bool=True) -> bool:
        """Filter results by Z score.

            Parameters
            ----------
            gText : str
                Z score threshold and operand, e.g. < 10 or > 3.4.
            updateL : bool
                Update filterList and StatusBar (True) or not (False).

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            dlg = DialogUserInputText(
                'Filter results by Z score.',
                ['Threshold (%)'],
                ['Decimal value between 0 and 100. e.g. < 10.0 or > 20.4'],
                [mValidator.Comparison(
                    numType='float', vMin=0, vMax=100, op=['<', '>']
                )],
                parent = self,
            )
            #------------------------------>
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.GetValue()[0]
                #------------------------------>
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        #endregion -------------------------------------------> Text Entry Dlg

        #region ------------------------------------------> Get Value and Plot
        op, val = uText.strip().split()
        zVal = stats.norm.ppf(1.0-(float(val.strip())/100.0))
        #------------------------------>
        idx = pd.IndexSlice
        col = idx[self.rCondC,self.rRpC,'FCz']
        if op == '<':
            self.rDf = self.rDf[
                (self.rDf[col] >= zVal) | (self.rDf[col] <= -zVal)]
        else:
            self.rDf = self.rDf[
                (self.rDf[col] <= zVal) | (self.rDf[col] >= -zVal)]
        #endregion ---------------------------------------> Get Value and Plot

        #region ------------------------------------------> Update Filter List
        if updateL:
            self.UpdateGUI()
            #------------------------------>
            self.StatusBarFilterText(f'{self.cLFZscore} {op} {val}')
            #------------------------------>
            self.rFilterList.append(
                [mConfig.lFilZScore,
                 {'gText': uText, 'updateL': False},
                 f'{self.cLFZscore} {op} {val}']
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List

        return True
    #---

    def FilterApply(self, reset: bool=True) -> bool:
        """Apply all filter to the current date.

            Parameters
            ----------
            reset : bool
                Reset self.rDf. Default is True.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Reset df
        if reset:
            self.rDf = self.rData[self.rDateC]['DF'].copy()
        else:
            pass
        #endregion -------------------------------------------------> Reset df

        #region -----------------------------------------------> Apply Filters
        for k in self.rFilterList:
            self.dKeyMethod[k[0]](**k[1])
        #endregion --------------------------------------------> Apply Filters

        #region --------------------------------------------------> Update GUI
        self.UpdateGUI()
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def FilterRemoveAll(self) -> bool:
        """Remove all filter.

            Returns
            -------
            bool
        """
        #region -------------------------------------------> Update Attributes
        self.rDf         = self.rData[self.rDateC]['DF'].copy()
        self.rFilterList = []
        self.wStatBar.SetStatusText('', 1)
        #endregion ----------------------------------------> Update Attributes

        #region --------------------------------------------------> Update GUI
        self.UpdateGUI()
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def FilterRemoveLast(self) -> bool:
        """Remove last applied filter.

            Returns
            -------
            bool
        """
        #region -----------------------------------> Check Something to Delete
        if not self.rFilterList:
            return True
        else:
            pass
        #endregion --------------------------------> Check Something to Delete

        #region -------------------------------------------> Update Attributes
        del self.rFilterList[-1]
        #endregion ----------------------------------------> Update Attributes

        #region --------------------------------------------------> Update GUI
        self.FilterApply()
        self.UpdateStatusBarFilterText()
        self.UpdateGUI()
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def FilterRemoveAny(self) -> bool:
        """Remove selected filters.

            Returns
            -------
            bool
        """
        #region -----------------------------------> Check Something to Delete
        if not self.rFilterList:
            return True
        else:
            pass
        #endregion --------------------------------> Check Something to Delete

        #region ------------------------------------------------------> Dialog
        dlg = DialogFilterRemoveAny(self.rFilterList, self)
        if dlg.ShowModal():
            lo = dlg.GetChecked()
            #------------------------------>
            dlg.Destroy()
            #------------------------------>
            if lo:
                pass
            else:
                return True
        else:
            dlg.Destroy()
            return True
        #endregion ---------------------------------------------------> Dialog

        #region ---------------------------------------------------> Variables
        for k in reversed(lo):
            del self.rFilterList[k]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------> Update GUI
        if self.rFilterList:
            self.FilterApply()
            self.UpdateStatusBarFilterText()
            self.UpdateGUI()
        else:
            self.FilterRemoveAll()
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def FilterCopy(self) -> bool:
        """Copy the applied filters.

            Returns
            -------
            bool
        """
        self.cParent.rCopiedFilters = [x for x in self.rFilterList]             # type: ignore
        return True
    #---

    def FilterPaste(self) -> bool:
        """Paste the copied filters.

            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Copy
        self.rFilterList = [x for x in self.cParent.rCopiedFilters]             # type: ignore
        #endregion ------------------------------------------------> Copy

        #region --------------------------------------------------->
        self.FilterApply()
        self.UpdateStatusBarFilterText()
        self.UpdateGUI()
        #endregion ------------------------------------------------>

        return True
    #---

    def FilterSave(self) -> bool:
        """Save the filters.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        filterDict = {x[0]: x[1:] for x in self.rFilterList}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rObj.rData[self.cSection][self.rDateC]['F'] = filterDict
        #------------------------------>
        if self.rObj.Save():
            self.rData[self.rDateC]['F'] = filterDict
        else:
            pass
        #endregion ------------------------------------------------>

        return True
    #---

    def FilterLoad(self) -> bool:
        """Load the filters.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rFilterList = [
            [k]+v for k,v in self.rData[self.rDateC]['F'].items()]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        autoF = self.rAutoFilter
        self.rAutoFilter = True
        #------------------------------>
        self.UpdateResultWindow()
        #------------------------------>
        self.rAutoFilter = autoF
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wStatBar.SetStatusText('', 1)
        for k in self.rFilterList:
            self.StatusBarFilterText(k[2])
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion -----------------------------------------------> Filter Methods
#---


class WindowResTarProt(BaseWindowResultListText2PlotFragments):
    """Plot the results of a Targeted Proteolysis analysis.

        Parameters
        ----------
        parent: wx.Window
            Parent of the window.

        Attributes
        ----------
        rAlpha: float
            Significance level of the Analysis.
        rCtrl:
        rData: dict
            Keys are dates and values the data for the plot.
        rDate: list[str]
            Dates for the analysis
        rDateC: str
            Current Date.
        rDf: pd.DataFrame
            Copy of the data used to plot
        rExp: list[str]
            Experiments in the analysis.
        rFragments: dict
            Dict with the info for the fragments. See mMethod.Fragments.
        rFragSelC: list[band, lane, fragment]
            Coordinates for the currently selected fragment. 0 based.
        rFragSelLine: matplotlib line
            Line to highlight the currently selected fragment.
        rIdxP: pd.IndexSlice
            To access the P columns in the data frame.
        rLCIdx: int
            Row selected in the wx.ListCtrl.
        rNatSeqC: str
            Sequence of the current native protein.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPeptide: str
            Sequence of the selected peptide in the wx.ListCtrl.
        rProtLength: int
            Length of hte Recombinant Protein used in the analysis.
        rProtLoc: list[int, int]
            Location of the Native Sequence in the Recombinant Sequence.
        rRecSeq: dict
            Keys are date and values a list with the sequence of the recombinant
            and native protein.
        rRecSeqC: list[str]
            Sequence of the recombinant and native protein for the current date.
     """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwTarProt
    cSection = mConfig.nmTarProt
    #------------------------------> Label
    cLPaneSec = 'Intensity'
    #------------------------------>
    cSWindow = (1100, 800)
    #------------------------------>
    cImgName   = {
        'Main': '{}-Protein-Fragments.pdf',
        'Sec' : '{}-Intensity-Representation.pdf',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: 'WindowUMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle       = f'{parent.cTitle} - {self.cSection}'
        self.rObj         = parent.rObj
        self.rData        = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        #------------------------------>
        self.ReportPlotDataError()
        #------------------------------>
        self.rDateC  = self.rDate[0]
        self.rRecSeq = {}
        #------------------------------>
        super().__init__(parent, menuData=menuData)
        #------------------------------>
        dKeyMethod = {
            'Peptide'  : self.ClearPept,
            'Fragment' : self.ClearFrag,
            'All'      : self.ClearAll,
            #------------------------------>
            'AA-Item'                     : self.AASelect,
            'AA-New'                      : self.AANew,
            'Hist-Item'                   : self.HistSelect,
            'Hist-New'                    : self.HistNew,
            mConfig.kwToolFACleavageEvol  : self.CEvol,
            mConfig.kwToolFACleavagePerRes: self.CpR,
            mConfig.kwToolFAPDBMap        : self.PDBMap,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------> Window position
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage Methods
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        # info = super().WinPos()
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> Set Position
        # x = info['D']['xo'] + info['W']['N']*config.deltaWin
        # y = (
        #     ((info['D']['h']/2) - (info['W']['h']/2))
        #     + info['W']['N']*config.deltaWin
        # )
        # self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.rDate list and the menuData dict needed to build the Tool
            menu.

            Returns
            -------
            tuple of list and dict
            The list is a list of str with the dates in the analysis.
            The dict has the following structure:
                {
                    'MenuDate' : [List of dates],
                }
        """
        #region ---------------------------------------------------> Fill dict
        #------------------------------> Variables
        date = []
        menuData = {
            'MenuDate': [],
            'FA'      : {},
        }
        #------------------------------> Fill
        for k,v in self.rData.items():
            if k != 'Error':
                #------------------------------>
                date.append(k)
                #------------------------------>
                menuData['FA'][k] = {}
                aa = v.get('AA', {})
                hist = v.get('Hist',{})
                menuData['FA'][k]['AA'] = [x for x in aa.keys()]
                menuData['FA'][k]['Hist'] = [x for x in hist.keys()]
            else:
                pass
        #------------------------------>
        menuData['MenuDate'] = date
        #endregion ------------------------------------------------> Fill dict

        return (date, menuData)
    #---

    def UpdateResultWindow(self, tDate: str='') -> bool:
        """Update the GUI and attributes when a new date is selected.

            Parameters
            ----------
            date : str
                Selected date.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rDateC       = tDate if tDate else self.rDateC
        self.rDf          = self.rData[self.rDateC]['DF'].copy()
        self.rAlpha       = self.rData[self.rDateC]['PI']['Alpha']
        self.rProtLoc     = self.rData[self.rDateC]['PI']['ProtLoc']
        self.rProtLength  = self.rData[self.rDateC]['PI']['ProtLength'][0]
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        self.rExp         = self.rData[self.rDateC]['PI']['Exp']
        self.rCtrl        = self.rData[self.rDateC]['PI']['Ctrl']
        self.rIdxP        = pd.IndexSlice[self.rExp,'P']
        self.rPeptide     = None
        self.rRecSeqC, self.rNatSeqC = (
            self.rRecSeq.get(self.rDateC)
            or
            self.rObj.GetSeq(self.cSection, self.rDateC)
        )
        self.rRecSeq[self.rDateC] = (self.rRecSeqC, self.rNatSeqC)
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl

        #region ---------------------------------------------------> Fragments
        self.rFragments = mMethod.Fragments(
            self.GetDF4FragmentSearch(),
            self.rAlpha,
            'le',
            self.rProtLength,
            self.rProtLoc,
        )
        #------------------------------>
        self.DrawFragments()
        #endregion ------------------------------------------------> Fragments

        #region -----------------------------------------------------> Peptide
        self.SetAxisInt()
        self.wPlot['Sec'].rCanvas.draw()
        #endregion --------------------------------------------------> Peptide

        #region ---------------------------------------------------> Win Title
        self.PlotTitle()
        #endregion ------------------------------------------------> Win Title

        return True
    #---

    def DrawFragments(self) -> bool:
        """Draw the fragments associated with the date.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        tKeyLabel = {}
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Keys
        for k,v in enumerate(self.rExp):
            tKeyLabel[f"{(v, 'P')}"] = f'{k}'
        #endregion -----------------------------------------------------> Keys

        #region -------------------------------------------------------> Super
        super().DrawFragments(tKeyLabel)
        #endregion ----------------------------------------------------> Super

        return True
    #---

    def SetFragmentAxis(self) -> bool:
        """Set the axis for the plot showing the fragments.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot['Main'].rAxes.clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        #------------------------------>
        if self.rProtLoc[0] is not None:
            xtick = [1] + list(self.rProtLoc) + [self.rProtLength]
        else:
            xtick = [1] + [self.rProtLength]
        self.wPlot['Main'].rAxes.set_xticks(xtick)
        self.wPlot['Main'].rAxes.set_xticklabels(xtick)
        #------------------------------>
        self.wPlot['Main'].rAxes.set_yticks(range(1, len(self.rExp)+2))
        self.wPlot['Main'].rAxes.set_yticklabels(self.rExp+['Protein'])
        self.wPlot['Main'].rAxes.set_ylim(0.5, len(self.rExp)+1.5)
        #------------------------------>
        ymax = len(self.rExp)+0.8
        #------------------------------>
        self.wPlot['Main'].rAxes.tick_params(length=0)
        #------------------------------>
        self.wPlot['Main'].rAxes.set_xlim(0, self.rProtLength+1)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rAxes.vlines(
            xtick, 0, ymax, linestyles='dashed', linewidth=0.5, color='black')
        #endregion ------------------------------------------------>

        #region ------------------------------------------------> Remove Frame
        self.wPlot['Main'].rAxes.spines['top'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['right'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['bottom'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['left'].set_visible(False)
        #endregion ---------------------------------------------> Remove Frame

        return True
    #---

    def ShowPeptideLoc(self) -> bool:
        """Show the location of the selected peptide.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Fragments
        #------------------------------> Remove old
        for k in self.rRectsFrag:
            k.set_linewidth(self.cGelLineWidth)
        #------------------------------> Get Keys
        fKeys = [f'{(x, "P")}' for x in self.rExp]
        #------------------------------> Highlight
        j = 0
        for k in fKeys:
            for p in self.rFragments[k]['SeqL']:
                if self.rPeptide in p:
                    self.rRectsFrag[j].set_linewidth(2.0)
                else:
                    pass
                j = j + 1
        #------------------------------> Show
        self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------> Fragments

        #region ---------------------------------------------------> Intensity
        #------------------------------> Variables
        nc = len(self.cColor['Spot'])                                           # type: ignore
        #------------------------------> Clear Plot
        self.wPlot['Sec'].rAxes.clear()
        #------------------------------> Axis
        self.SetAxisInt()
        #------------------------------> Row
        row = self.rDf.loc[self.rDf[('Sequence', 'Sequence')] == self.rPeptide]
        row =row.loc[:,pd.IndexSlice[:,('Int','P')]]                            # type: ignore
        #------------------------------> Values
        x = []
        y = []
        for k,c in enumerate(self.rCtrl+self.rExp, start=1):
            #------------------------------> Variables
            intL, P = row[c].values.tolist()[0]
            intL = list(map(float, intL[1:-1].split(',')))
            P = float(P)
            intN = len(intL)
            #------------------------------> Color, x & y
            if k == 1:
                color = self.cColor['Ctrl']                                     # type: ignore
                x = [1]
                y = [sum(intL)/intN]
            else:
                color = self.cColor['Spot'][(k-2)%nc]                           # type: ignore
            #------------------------------> Ave
            if P <= self.rAlpha:
                x.append(k)
                y.append(sum(intL)/intN)
            else:
                pass
            #------------------------------> Plot
            self.wPlot['Sec'].rAxes.scatter(
                intN*[k], intL, color=color, edgecolor='black', zorder=3)
        #------------------------------>
        self.wPlot['Sec'].rAxes.scatter(
            x,
            y,
            edgecolor = 'black',
            marker    = 'D',
            color     = 'cyan',
            s         = 120,
            zorder    = 2,
        )
        self.wPlot['Sec'].rAxes.plot(x,y, zorder=1)
        #------------------------------> Show
        self.wPlot['Sec'].ZoomResetSetValues()
        self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------> Intensity

        return True
    #---

    def SetAxisInt(self) -> bool:
        """Set the axis of the Intensity plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        nExp = len(self.rExp)
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------------> Values
        self.wPlot['Sec'].rAxes.clear()
        self.wPlot['Sec'].rAxes.set_xticks(range(1,nExp+2))
        self.wPlot['Sec'].rAxes.set_xticklabels(self.rCtrl+self.rExp)
        #------------------------------>
        self.wPlot['Sec'].rAxes.set_xlim(0.5, nExp+1.5)
        #------------------------------>
        self.wPlot['Sec'].rAxes.set_ylabel('Intensity (after DP)')
        #endregion ---------------------------------------------------> Values

        return True
    #---

    def PrintFragmentText(
        self,
        tKey : str,
        fragC: list[int],
        ) -> bool:
        """Print information about a selected Fragment.

            Parameters
            ----------
            tKey: tuple(str, str)
                Tuple with the column name in the pd.DataFrame with the results.
            fragC: list[int]
                Fragment coordinates.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Info
        #------------------------------> Fragments
        frag =  (f'{self.rFragments[tKey]["NFrag"][0]}'
                 f'({self.rFragments[tKey]["NFrag"][1]})')
        clSiteExp = (f'{self.rFragments[tKey]["NcT"][0]}'
                     f'({self.rFragments[tKey]["NcT"][1]})')
        seqExp = (f'{sum(self.rFragments[tKey]["Np"])}'
                  f'({sum(self.rFragments[tKey]["NpNat"])})')
        #------------------------------> Res Numbers
        n, c = self.rFragments[tKey]["Coord"][fragC[1]]
        nf, cf = self.rFragments[tKey]["CoordN"][fragC[1]]
        #------------------------------> Sequences
        tNP = (f'{self.rFragments[tKey]["Np"][fragC[1]]}'
              f'({self.rFragments[tKey]["NpNat"][fragC[1]]})')
        #------------------------------> Cleavages
        clSite = (f'{self.rFragments[tKey]["Nc"][fragC[1]]}'
                  f'({self.rFragments[tKey]["NcNat"][fragC[1]]})')
        #------------------------------> Labels
        expL, fragL = mMethod.StrEqualLength(
            [self.rExp[fragC[0]], f'Fragment {fragC[1]+1}'])
        emptySpace = (2+ len(expL))*' '
        #endregion ------------------------------------------------> Info

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.AppendText(
            f'Details for {self.rExp[fragC[0]]} - Fragment {fragC[1]+1}\n\n')
        self.wText.AppendText(f'{expL}: Fragments {frag}, Cleavage sites {clSiteExp}\n')
        self.wText.AppendText(f'{emptySpace}Peptides {seqExp}\n\n')
        self.wText.AppendText(f'{fragL}: Nterm {n}({nf}), Cterm {c}({cf})\n')
        self.wText.AppendText(f'{emptySpace}Peptides {tNP}, Cleavage sites {clSite}\n\n')
        self.wText.AppendText('Sequences in the fragment:\n\n')
        self.wText.AppendText(f'{self.rFragments[tKey]["Seq"][fragC[1]]}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        return True
    #---

    def SeqExport(self) -> bool:
        """Export the sequence alignment.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = DialogFABtnText(
            'File',
            'Path to the output file',
            mConfig.elPDF,
            mValidator.OutputFF('file'),
            'Length',
            'Residues per line in the output file, e.g. 100',
            mValidator.NumberList('int', vMin=1, vMax=100, nN=1),
            parent = self,
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            fileP  = dlg.wBtnTc.wTc.GetValue()
            length = int(dlg.wLength.wTc.GetValue())
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        try:
            mMethod.R2SeqAlignment(
                self.rDf,
                self.rAlpha,
                self.rRecSeqC,
                self.rNatSeqC,                                                  # type: ignore
                fileP,
                length,                                                         # type: ignore
            )
        except Exception as e:
            msg = 'Export of Sequence Alignments failed.'
            DialogNotification('errorF', msg=msg, tException=e)
        #endregion ------------------------------------------------> Run

        dlg.Destroy()
        return True
    #---

    def ClearPept(self, plot: bool=True) -> bool:
        """Clear the Peptide selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if (rID := self.wLC.wLCS.wLC.GetFirstSelected()):
            self.wLC.wLCS.wLC.Select(rID, on=0)
        else:
            pass
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for r in self.rRectsFrag:
            r.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            self.wPlot['Main'].rCanvas.draw()
            self.SetAxisInt()
            self.wPlot['Sec'].rCanvas.draw()
        else:
            pass
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rPeptide = None
        self.rLCIdx = None
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearFrag(self, plot=True) -> bool:
        """Clear the Fragment selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
            self.rFragSelLine = None
            if plot:
                self.wPlot['Main'].rCanvas.draw()
            else:
                pass
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rFragSelC = [None, None]
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearAll(self) -> bool:
        """Clear all selections.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.ClearPept(plot=False)
        self.ClearFrag(plot=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rCanvas.draw()
        self.SetAxisInt()
        self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        return True
    #---

    def AANew(self) -> bool:
        """Perform a new AA analysis.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = DialogUserInputText(
            'New AA Distribution Analysis',
            ['Positions'],
            ['Number of residues around the cleavage site to consider, e.g. 5'],
            parent    = self,
            validator = [mValidator.NumberList('int', vMin=1, nN=1)],
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            pos = int(dlg.rInput[0].wTc.GetValue())
            dateC = mMethod.StrNow()
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        dfI = self.rData[self.rDateC]['DF']
        idx = pd.IndexSlice
        dfI = dfI.loc[:,idx[['Sequence']+self.rExp,['Sequence', 'P']]]
        dfO = mMethod.R2AA(
            dfI, self.rRecSeqC, self.rAlpha, self.rProtLength, pos=pos)
        #endregion ------------------------------------------------> Run

        #region -----------------------------------------------> Save & Update
        #------------------------------> File
        date = f'{self.rDateC.split(" - ")[0]}'
        section = f'{self.cSection.replace(" ", "-")}'
        folder = f'{date}_{section}'
        fileN = f'{dateC}_AA-{pos}.txt'
        fileP = self.rObj.rStepDataP/folder/fileN
        mFile.WriteDF2CSV(fileP, dfO)
        #------------------------------> Umsap
        self.rObj.rData[self.cSection][self.rDateC]['AA'][f'{date}_{pos}'] = fileN
        self.rObj.Save()
        #------------------------------> Refresh
        #--------------> UMSAPControl
        self.cParent.UpdateFileContent()                                        # type: ignore
        #--------------> TarProt
        self.rObj = self.cParent.rObj                                           # type: ignore
        self.rData = self.rObj.dConfigure[self.cSection]()
        #--------------> Menu
        _, menuData = self.SetDateMenuDate()
        self.mBar.mTool.mFurtherA.UpdateFurtherAnalysis(
            self.rDateC, menuData['FA'])
        #--------------> GUI
        self.AASelect(f'{date}_{pos}')
        #endregion --------------------------------------------> Save & Update

        dlg.Destroy()
        return True
    #---

    def AASelect(self, aa:str) -> bool:
        """Show an AA analysis.

            Parameters
            ----------
            aa: str
                Date for the analysis

            Returns
            -------
            bool
        """
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            WindowResAA(
                self, self.rDateC, aa, self.rData[self.rDateC]['AA'][aa]))
        return True
    #---

    def HistSelect(self, hist:str) -> bool:
        """Show a Histogram.

            Parameters
            ----------
            hist: str
                Selected date.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            WindowResHist(
                self, self.rDateC, hist, self.rData[self.rDateC]['Hist'][hist]))
        #endregion ------------------------------------------------>

        return True
    #---

    def HistNew(self) -> bool:
        """Create a new histogram.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = DialogUserInputText(
            'New Histogram Analysis',
            ['Histograms Windows'],
            ['Size of the histogram windows, e.g. 50 or 50 100 200'],
            parent    = self,
            validator = [mValidator.NumberList(numType='int', vMin=0, sep=' ')],
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            win = [int(x) for x in dlg.rInput[0].wTc.GetValue().split()]
            dateC = mMethod.StrNow()
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        dfI = self.rData[self.rDateC]['DF']
        idx = pd.IndexSlice
        a = mConfig.dfcolTarProtFirstPart[2:]+self.rExp
        b = mConfig.dfcolTarProtFirstPart[2:]+len(self.rExp)*['P']
        dfI = dfI.loc[:,idx[a,b]]
        dfO = mMethod.R2Hist(
            dfI, self.rAlpha, win, self.rData[self.rDateC]['PI']['ProtLength'])
        #endregion ------------------------------------------------> Run

        #region -----------------------------------------------> Save & Update
        #------------------------------> File
        date = f'{self.rDateC.split(" - ")[0]}'
        section = f'{self.cSection.replace(" ", "-")}'
        folder = f'{date}_{section}'
        fileN = f'{dateC}_Hist-{win}.txt'
        fileP = self.rObj.rStepDataP/folder/fileN
        mFile.WriteDF2CSV(fileP, dfO)
        #------------------------------> Umsap
        self.rObj.rData[self.cSection][self.rDateC]['Hist'][f'{date}_{win}'] = fileN
        self.rObj.Save()
        #------------------------------> Refresh
        #--------------> UMSAPControl
        self.cParent.UpdateFileContent()                                        # type: ignore
        #--------------> TarProt
        self.rObj = self.cParent.rObj                                           # type: ignore
        self.rData = self.rObj.dConfigure[self.cSection]()
        #--------------> Menu
        _, menuData = self.SetDateMenuDate()
        self.mBar.mTool.mFurtherA.UpdateFurtherAnalysis(
            self.rDateC, menuData['FA'])
        #--------------> GUI
        self.HistSelect(f'{date}_{win}')
        #endregion --------------------------------------------> Save & Update

        dlg.Destroy()
        return True
    #---

    def CpR(self) -> bool:
        """Show the Cleavage per Residue results.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            WindowResCpR(self, self.rDateC, self.rData[self.rDateC]['CpR']))
        #endregion ------------------------------------------------>

        return True
    #---

    def PDBMap(self) -> bool:
        """Map results to a PDB.

            Returns
            -------
            bool
        """
        def Helper(pdbObj, tExp, tAlign, tDF, name):
            """Writes to file

                Parameters
                ----------
                pdbObj: mFile.PDBFile
                    PDB Object
                tExp: str
                    Current experiment
                tAlign: BioPython alignment
                    Sequence alignment
                tDF: pd.DataFrame
                    To get the beta values
                name: str
                    Part of the file name

                Returns
                -------
                bool
            """
            #region -------------------------------------------------------->
            idx = pd.IndexSlice
            #------------------------------>
            for e in tExp:
                #------------------------------>
                betaDict = {}
                p = 0
                s = 0
                #------------------------------>
                for j,r in enumerate(tAlign[0].seqB):
                    if r != '-':
                        #------------------------------>
                        if tAlign[0].seqA[j] != '-':
                            betaDict[pdbRes[p]] = tDF.iat[s, tDF.columns.get_loc(idx['Rec',e])]
                            p = p + 1
                        else:
                            pass
                        #------------------------------>
                        s = s + 1
                    else:
                        pass
                #------------------------------>
                pdbObj.SetBeta(pdbObj.rChain[0], betaDict)
                pdbObj.WritePDB(
                    pdbO/f'{name[0]} - {e} - {name[1]}.pdb', pdbObj.rChain[0])
            #endregion ----------------------------------------------------->

            return True
        #---
        #region ---------------------------------------------------> dlg
        dlg = DialogFA2Btn(
            ['PDB', 'Output'],
            ['Path to the PDB file', 'Path to the output folder'],
            [mConfig.elPDB, mConfig.elPDB],
            [mValidator.InputFF('file'), mValidator.OutputFF('folder')],
            parent = self
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal():
            pdbI = dlg.wBtnI.wTc.GetValue()
            pdbO = Path(dlg.wBtnO.wTc.GetValue())
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Path

        #region ---------------------------------------------------> Variables
        pdbObj   = mFile.PDBFile(pdbI)
        pdbSeq   = pdbObj.GetSequence(pdbObj.rChain[0])
        pdbRes   = pdbObj.GetResNum(pdbObj.rChain[0])
        cut      = self.rObj.GetCleavagePerResidue(self.cSection, self.rDateC)
        cEvol    = self.rObj.GetCleavageEvolution(self.cSection, self.rDateC)
        blosum62 = substitution_matrices.load("BLOSUM62")
        #endregion ------------------------------------------------> Variables

        #region -----------------------------------------------> Run
        align = pairwise2.align.globalds(                                       # type: ignore
            pdbSeq, self.rRecSeqC, blosum62, -10, -0.5)
        #------------------------------>
        Helper(pdbObj, self.rExp, align, cut, (self.rDateC, 'CpR'))
        Helper(pdbObj, self.rExp, align, cEvol, (self.rDateC, 'CEvol'))
        #endregion --------------------------------------------> Run

        dlg.Destroy()
        return True
    #---

    def CEvol(self) -> bool:
        """Show the Cleavage Evolution results.

            Returns
            -------
            bool
        """
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            WindowResCEvol(self, self.rDateC, self.rData[self.rDateC]['CEvol']))
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region ----------------------------------------------------> Event Methods
    def OnPickFragment(self, event) -> bool:
        """Display info about the selected fragment.

            Parameters
            ----------
            event: matplotlib pick event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        art = event.artist
        fragC = list(map(int, art.get_label().split('.')))
        #------------------------------>
        if self.rFragSelC != fragC:
            self.rFragSelC = fragC
        else:
            return True
        #------------------------------>
        x, y = event.artist.xy
        x = round(x)
        y = round(y)
        #------------------------------>
        tKey = f'{(self.rExp[fragC[0]], "P")}'
        #------------------------------>
        x1, x2 = self.rFragments[tKey]['Coord'][fragC[1]]
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------> Highlight Fragment
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
        else:
            pass
        #------------------------------
        self.rFragSelLine = self.wPlot['Main'].rAxes.plot(
            [x1+2, x2-2], [y,y], color='black', linewidth=4)
        #------------------------------>
        self.wPlot['Main'].rCanvas.draw()
        #endregion ---------------------------------------> Highlight Fragment

        #region -------------------------------------------------------> Print
        self.PrintFragmentText(tKey, fragC)
        #endregion ----------------------------------------------------> Print

        return True
    #---
    #endregion -------------------------------------------------> Event Methods
#---


class WindowResAA(BaseWindowResultOnePlotFA):
    """Show the results of an AA analysis.

        Parameters
        ----------
        parent: WindowResTarProt
            Parent of the window.
        dateC: str
            Current date
        key: str
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rBandStart: float
            Start x coordinates for the bands.
        rBandWidth: float
            Width of the bands.
        rData: pd.DataFrame
            Data with the results.
        rExp: bool
            Show experiments (True) or Positions (False).
        rLabel: list[str]
            Experiment names.
        rLabelC: str
            Currently selected experiment.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPos: list[str]
            Positions in the results.
        rRecSeq: str
            Sequence of the recombinant protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwAAPlot
    cSection = mConfig.nuAA
    cColor   = mConfig.confColor[cName]
    #------------------------------>
    rBandWidth = 0.8
    rBandStart = 0.4
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent: WindowResTarProt,
        dateC : str,
        key   : str,
        fileN : str,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle  = f"{parent.cTitle} - {dateC} - {self.cSection} - {key}"
        self.cDateC  = dateC
        self.cKey    = key
        self.cFileN  = fileN
        self.rUMSAP  = parent.cParent
        self.rObj    = parent.rObj
        self.rData   = self.rObj.GetFAData(
            parent.cSection, parent.rDateC, fileN, [0,1])
        self.rRecSeq = self.rObj.GetRecSeq(parent.cSection, dateC)
        menuData     = self.SetMenuDate()
        self.rPos    = menuData['Pos']
        self.rLabel  = menuData['Label']
        self.rExp    = True
        self.rLabelC = ''
        #------------------------------>
        super().__init__(parent, menuData=menuData)
        #------------------------------>
        dKeyMethod = {
            mConfig.kwToolAAExp : self.PlotExp,
            mConfig.kwToolAAPos : self.PlotPos,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Plot
        self.PlotExp(menuData['Label'][0])
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the menu data.

            Returns
            -------
            dict
        """
        menuData = {}
        menuData['Label'] = [k for k in self.rData.columns.unique(level=0)[1:-1]]
        menuData['Pos'] = [k for k in self.rData[menuData['Label'][0]].columns.unique(level=0)]
        return menuData
    #---

    def SetAxisExp(self) -> bool:
        """General details of the plot area.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot[0].rFigure.clear()
        self.wPlot[0].rAxes = self.wPlot[0].rFigure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear

        #region ---------------------------------------------------> Set ticks
        self.wPlot[0].rAxes.set_ylabel('AA distribution (%)')
        self.wPlot[0].rAxes.set_xlabel('Positions')
        self.wPlot[0].rAxes.set_xticks(range(1,len(self.rPos)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(self.rPos)
        self.wPlot[0].rAxes.set_xlim(0,len(self.rPos)+1)
        #endregion ------------------------------------------------> Set ticks

        return True
    #---

    def PlotExp(self, label: str) -> bool:
        """Plot the results for the selected experiment.

            Parameters
            ----------
            label: str
                Name of the experiment.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        self.rExp = True
        self.rLabelC = label
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.SetAxisExp()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Data
        idx = pd.IndexSlice
        df = self.rData.loc[:,idx[('AA', label),:]].iloc[0:-1,:]                # type: ignore
        df.iloc[:,1:] = 100*(df.iloc[:,1:]/df.iloc[:,1:].sum(axis=0))
        #endregion ------------------------------------------------> Data

        #region ---------------------------------------------------> Bar
        col = df.loc[:,idx[label,:]].columns.unique(level=1)                    # type: ignore
        for k,c in enumerate(col, start=1):
            #------------------------------> Prepare DF
            dfB = df.loc[:,idx[('AA',label),('AA',c)]]                          # type: ignore
            dfB = dfB[dfB[(label,c)] != 0]
            dfB = dfB.sort_values(by=[(label,c),('AA','AA')], ascending=False)  # type: ignore
            #------------------------------> Supp Data
            cumS = [0]+dfB[(label,c)].cumsum().values.tolist()[:-1]
            #-------------->
            color = []
            text = []
            r = 0
            for row in dfB.itertuples(index=False):
                #-------------->
                color.append(self.cColor['BarColor'][row[0]]
                     if row[0] in mConfig.lAA1 else self.cColor['Xaa'])
                #-------------->
                if row[1] >= 10.0:
                    s = f'{row[0]}\n{row[1]:.1f}'
                    y = (2*cumS[r]+row[1])/2
                    text.append([k,y,s])
                else:
                    pass
                r = r + 1
            #------------------------------> Bar
            self.wPlot[0].rAxes.bar(
                k,
                dfB[(label,c)].values.tolist(),
                bottom    = cumS,
                color     = color,
                edgecolor = 'black',
            )
            #------------------------------> Text
            for x,y,t in text:
                self.wPlot[0].rAxes.text(
                    x,y,t,
                    fontsize            = 9,
                    horizontalalignment = 'center',
                    verticalalignment   = 'center',
                )
        #endregion ------------------------------------------------> Bar

        #region --------------------------------------------------> Tick Color
        chi = self.rData.loc[:,idx[('AA', label),:]].iloc[-1,1:].values         # type: ignore
        self.wPlot[0].rAxes.set_title(label)
        for k,v in enumerate(chi):
            color = self.cColor['Chi'][v]
            self.wPlot[0].rAxes.get_xticklabels()[k].set_color(color)
        #endregion -----------------------------------------------> Tick Color

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxisPos(self) -> bool:
        """ General details of the plot area.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot[0].rFigure.clear()
        self.wPlot[0].rAxes = self.wPlot[0].rFigure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear

        #region ---------------------------------------------------> Set ticks
        self.wPlot[0].rAxes.set_ylabel('AA distribution (%)')
        self.wPlot[0].rAxes.set_xlabel('Amino acids')
        self.wPlot[0].rAxes.set_xticks(range(1,len(mConfig.lAA1)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(mConfig.lAA1)
        self.wPlot[0].rAxes.set_xlim(0,len(mConfig.lAA1)+1)
        #endregion ------------------------------------------------> Set ticks

        return True
    #---

    def PlotPos(self, label: str) -> bool:
        """Plot the results for a position.

            Parameters
            ----------
            label: str
                Name of the position.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        self.rExp = False
        self.rLabelC = label
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.SetAxisPos()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Data
        idx = pd.IndexSlice
        df = self.rData.loc[:,idx[:,label]].iloc[0:-1,0:-1]                     # type: ignore
        df = 100*(df/df.sum(axis=0))
        #endregion ------------------------------------------------> Data

        #region ---------------------------------------------------> Bar
        n = len(self.rLabel)
        for row in df.itertuples():
            s = row[0]+1-self.rBandStart
            w = self.rBandWidth/n
            for x in range(0,n,1):
                self.wPlot[0].rAxes.bar(
                    s+x*w,
                    row[x+1],
                    width     = w,
                    align     = 'edge',
                    color     = self.cColor['Spot'][x%len(self.cColor['Spot'])],
                    edgecolor = 'black',
                )
        #endregion ------------------------------------------------> Bar

        #region ------------------------------------------------------> Legend
        leg = []
        legLabel = self.rData.columns.unique(level=0)[1:-1]
        for i in range(0, n, 1):
            leg.append(mpatches.Patch(
                color = self.cColor['Spot'][i],
                label = legLabel[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion ---------------------------------------------------> Legend

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(label)
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def UpdateStatusBarExp(self, x: float, y: float) -> bool:
        """Update the wx.StatusBar text when plotting an experiment.

            Parameters
            ----------
            x: float
                Mouse x coordinate.
            y: float
                Mouse y coordinate.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if 1 <= (xf := round(x)) <= len(self.rPos):
            pass
        else:
            self.wStatBar.SetStatusText('')
            return False
        pos = self.rPos[xf-1]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        df = self.rData.loc[:,[('AA', 'AA'),(self.rLabelC, pos)]].iloc[0:-1,:]
        df['Pc'] = 100*(df.iloc[:,1]/df.iloc[:,1].sum(axis=0))
        df = df.sort_values(
            by=[(self.rLabelC, pos),('AA','AA')], ascending=False)              # type: ignore
        df['Sum'] = df['Pc'].cumsum()
        df = df.reset_index(drop=True)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        try:
            row = df[df['Sum'].gt(y)].index[0]
        except Exception:
            self.wStatBar.SetStatusText('')
            return False
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        aa    = df.iat[row,0]
        pc    = f'{df.iat[row,-2]:.1f}'
        absV  = f'{df.iat[row,1]:.0f}'
        inSeq = self.rRecSeq.count(aa)
        text = (f'Pos={pos}  AA={aa}  {pc}%  Abs={absV}  InSeq={inSeq}')
        #endregion ------------------------------------------------>

        self.wStatBar.SetStatusText(text)
        return True
    #---

    def UpdateStatusBarPos(self, x: float, y: float) -> bool:                   # pylint: disable=unused-argument
        """Update the wx.StatusBar text when plotting a positions.

            Parameters
            ----------
            x: float
                Mouse x coordinate.
            y: float
                Mouse y coordinate.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if 1 <= (xf := round(x)) <= len(mConfig.lAA1):
            pass
        else:
            self.wStatBar.SetStatusText('')
            return False
        aa = mConfig.lAA1[xf-1]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        n = len(self.rLabel)
        w = self.rBandWidth / n
        e = xf - self.rBandStart + (self.rBandWidth / n)
        k = 0
        for k in range(0, n, 1):
            if e < x:
                e = e + w
            else:
                break
        exp = self.rLabel[k]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        df = self.rData.loc[:,[('AA', 'AA'),(exp, self.rLabelC)]].iloc[0:-1,:]
        df['Pc'] = 100*(df.iloc[:,1]/df.iloc[:,1].sum(axis=0))
        df = df.sort_values(
            by=[(exp, self.rLabelC),('AA','AA')], ascending=False)              # type: ignore
        df['Sum'] = df['Pc'].cumsum()
        df = df.reset_index(drop=True)
        row = df.loc[df[('AA', 'AA')] == aa].index[0]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        pc    = f'{df.iat[row, 2]:.1f}'
        absV  = f'{df.iat[row, 1]:.0f}'
        inSeq = self.rRecSeq.count(aa)
        text  = (f'AA={aa}  Exp={exp}  {pc}%  Abs={absV}  InSeq={inSeq}')
        #endregion ------------------------------------------------>

        self.wStatBar.SetStatusText(text)
        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            WindowResAA(self.cParent, self.cDateC, self.cKey, self.cFileN)      # type: ignore
        )
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnUpdateStatusBar(self, event) -> bool:
        """Update the statusbar info.

            Parameters
            ----------
            event: matplotlib event
                Information about the event

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            #------------------------------>
            x, y = event.xdata, event.ydata
            #------------------------------>
            if self.rExp:
                return self.UpdateStatusBarExp(x,y)
            else:
                #------------------------------> Position
                return self.UpdateStatusBarPos(x,y)
        else:
            self.wStatBar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class WindowResHist(BaseWindowResultOnePlotFA):
    """Plot hte results for a cleavage histogram.

        Parameters
        ----------
        parent: WindowResTarProt
            Parent of the window.
        dateC: str
            Current date
        key: str
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rAllC: str
            Show all cleavage or not.
        rBandStart: float
            Start x coordinates for the bands.
        rBandWidth: float
            Width of the bands.
        rData: pd.DataFrame
            Data with the results.
        rLabel: list[str]
            List of experiment labels.
        rNat: str
            Plot recombinant or native sequence.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rProtLength: list[int]
            Length of the recombinant and native protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwHistPlot
    cSection = mConfig.nuHist
    cColor   = mConfig.confColor[cName]
    cRec = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    cAll = {
        True    : 'Unique',
        False   : 'All',
        'All'   : 'All Cleavages',
        'Unique': 'Unique Cleavages',
    }
    #------------------------------>
    rBandWidth = 0.8
    rBandStart = 0.4
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent: WindowResTarProt,
        dateC : str,
        key   : str,
        fileN : str,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle  = f"{parent.cTitle} - {dateC} - {self.cSection} - {key}"
        self.cDateC  = dateC
        self.cKey    = key
        self.cFileN   = fileN
        self.rUMSAP  = parent.cParent
        self.rObj    = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, parent.rDateC,fileN, [0,1,2])
        self.rLabel      = self.rData.columns.unique(level=2).tolist()[1:]
        self.rProtLength = parent.rData[self.cDateC]['PI']['ProtLength']
        menuData         = self.SetMenuDate()
        self.rNat = 'Rec'
        self.rAllC = 'All'
        #------------------------------>
        super().__init__(parent, menuData)
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Plot
        self.UpdateResultWindow()
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the data for the menu.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1] is not None:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(
        self,
        nat : Optional[bool]=None,
        allC: Optional[bool]=None,
        ) -> bool:
        """Update the window.

            Parameters
            ----------
            nat: bool or None
                Show native or recombinant sequence.
            allC: bool or None
                Show all cleavages or not.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rNat  = self.cRec[nat] if nat is not None else self.rNat
        self.rAllC = self.cAll[allC] if allC is not None else self.rAllC
        #------------------------------>
        idx = pd.IndexSlice
        df = self.rData.loc[:,idx[self.rNat,['Win',self.rAllC],:]]              # type: ignore
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.SetAxis(df.loc[:,idx[:,:,'Win']])                                  # type: ignore
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Plot
        n = len(self.rLabel)
        w = self.rBandWidth / n
        df = df.iloc[:,range(1,n+1,1)]
        df = df[(df.notna()).all(axis=1)]                                       # type: ignore
        for row in df.itertuples():
            s = row[0]+1-self.rBandStart
            for x in range(0,n,1):
                self.wPlot[0].rAxes.bar(
                    s+x*w,
                    row[x+1],
                    width     = w,
                    align     = 'edge',
                    color     = self.cColor['Spot'][x%len(self.cColor['Spot'])],
                    edgecolor = 'black',
                )
        #endregion ------------------------------------------------> Plot

        #region ------------------------------------------------------> Legend
        leg = []
        for i in range(0, n, 1):
            leg.append(mpatches.Patch(
                color = self.cColor['Spot'][i],
                label = self.rLabel[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion ---------------------------------------------------> Legend

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(f'{self.cRec[self.rNat]} - {self.cAll[self.rAllC]}')
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxis(self, win: pd.Series) -> bool:
        """Set the axis of the plot.

            Parameters
            ----------
            win: pd.Series
                Windows of the histograms.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot[0].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        #------------------------------>
        win = win.dropna().astype('int').to_numpy().flatten()                   # type: ignore
        label = []
        for k,w in enumerate(win[1:]):
            label.append(f'{win[k]}-{w}')
        #------------------------------>
        self.wPlot[0].rAxes.set_xticks(range(1,len(label)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(label)
        self.wPlot[0].rAxes.set_xlim(0, len(label)+1)
        self.wPlot[0].rAxes.tick_params(axis='x', labelrotation=45)
        self.wPlot[0].rAxes.yaxis.get_major_locator().set_params(integer=True)
        self.wPlot[0].rAxes.set_xlabel('Windows')
        self.wPlot[0].rAxes.set_ylabel('Number of Cleavages')
        #endregion ------------------------------------------------> Label

        return True
    #---

    def DupWin(self) -> bool:
        """ Export data to a csv file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            WindowResHist(self.cParent, self.cDateC, self.cKey, self.cFileN))   # type: ignore
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnUpdateStatusBar(self, event) -> bool:
        """Update the statusbar info.

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if event.inaxes:
            x, _ = event.xdata, event.ydata
            xf = round(x)
        else:
            self.wStatBar.SetStatusText('')
            return True
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        idx = pd.IndexSlice
        df = self.rData.loc[:,idx[self.rNat,['Win',self.rAllC],:]]              # type: ignore
        df = df.dropna(how='all')
        if 0 < xf < df.shape[0]:
            pass
        else:
            self.wStatBar.SetStatusText('')
            return False
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        n = len(self.rLabel)
        w = self.rBandWidth / n
        e = xf - self.rBandStart + (self.rBandWidth / n)
        k = 0
        for k in range(0, n, 1):
            if e < x:
                e = e + w
            else:
                break
        exp = self.rLabel[k]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = f'{df.iat[xf-1, 0]:.0f}-{df.iat[xf, 0]:.0f}'
        clv = f'{df.iat[xf-1,df.columns.get_loc(idx[self.rNat,self.rAllC,exp])]}'
        text = (f'Win={win}  Exp={exp}  Cleavages={clv}')
        #------------------------------>
        self.wStatBar.SetStatusText(text)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class WindowResCEvol(BaseWindowResultListTextNPlot):
    """Show the results for a Cleavage Evolution analysis.

        Parameters
        ----------
        parent: WindowResTarProt
            Parent of the window.
        dateC: str
            Current date
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rData: dict
            Keys are dates and values is the data to create the plot.
        rDf: pd.DataFrame
            Results for the current selected options.
        rIdx: dict
            Information about selected rows in the wx.ListCtrl.
        rLabel: list[str]
            Experiment names.
        rMon: bool
            Plot monotonic results (True) or all results (False)
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rProtLength: list[int]
            Length of the recombinant and native protein.
        rRec: bool
            Plot data for recombinant or native sequence.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwCEvolPlot
    cSection = mConfig.nuCEvol
    #------------------------------>
    cTList   = 'Residue Numbers'
    cTPlot   = 'Plot'
    cLNPlot  = ['M']
    cLCol    = ['Residue']
    #------------------------------>
    cHSearch = 'Residue Number'
    #------------------------------>
    cRec = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent: WindowResTarProt,
        dateC : str,
        fileN : str,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f"{parent.cTitle} - {dateC} - {self.cSection}"
        self.cDateC = dateC
        self.cFileN = fileN
        self.rUMSAP = parent.cParent
        self.rObj   = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, parent.rDateC, fileN, [0,1])
        self.rLabel = self.rData.columns.unique(level=1).tolist()
        self.rIdx   = {}
        self.rProtLength = parent.rData[self.cDateC]['PI']['ProtLength']
        menuData         = self.SetMenuDate()
        #------------------------------>
        super().__init__(parent, menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------->
        self._mgr.DetachPane(self.wText)
        self._mgr.Update()
        self.wText.Destroy()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Plot
        self.UpdateResultWindow(False, False)
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage Methods
    def SetMenuDate(self) -> dict:
        """Set the menu data.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1] is not None:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(
        self,
        nat: Optional[bool]=None,
        mon: Optional[bool]=None,
        ) -> bool:
        """Update the plot.

            Parameters
            ----------
            nat: bool or None
                Plot results for the recombinant or native protein.
            mon: bool or None
                Plot monotonic or all results.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        #------------------------------>
        if nat is not None:
            self.rRec = self.cRec[nat]
        else:
            pass
        #------------------------------>
        self.rMon = mon if mon is not None else self.rMon
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        idx = pd.IndexSlice
        if self.rRec:
            self.rDF = self.rData.loc[:,idx[self.rRec,:]]                       # type: ignore
        else:
            self.rDF = self.rData.loc[:,idx[self.rRec,:]]                       # type: ignore
        #------------------------------>
        self.rDF = self.rDF[self.rDF.any(axis=1)]
        #------------------------------>
        if self.rMon:
            self.rDF = self.rDF[self.rDF.apply(
                lambda x: x.is_monotonic_increasing or x.is_monotonic_decreasing,
                axis=1
            )]
        else:
            pass
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.FillListCtrl(self.rDF.index.tolist())
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.SetAxis()
        self.wPlot.dPlot['M'].ZoomResetSetValues()
        self.wPlot.dPlot['M'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def FillListCtrl(self, tRes: list[int]) -> bool:
        """Fill the wx.ListCtrl.

            Parameters
            ----------
            tRes: list[int]
                List of residue numbers.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wLC.wLCS.wLC.DeleteAllItems()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        data = []
        for k in tRes:
            data.append([str(k+1)])
        self.wLC.wLCS.wLC.SetNewData(data)
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxis(self) -> bool:
        """Set the axis.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot.dPlot['M'].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        self.wPlot.dPlot['M'].rAxes.set_xticks(range(1,len(self.rLabel)+1))
        self.wPlot.dPlot['M'].rAxes.set_xticklabels(self.rLabel)
        self.wPlot.dPlot['M'].rAxes.set_xlim(0, len(self.rLabel)+1)
        self.wPlot.dPlot['M'].rAxes.set_xlabel('Experiment Label')
        self.wPlot.dPlot['M'].rAxes.set_ylabel('Relative Cleavage Rate')
        #------------------------------>
        self.wPlot.dPlot['M'].rAxes.set_title(self.cRec[self.rRec])
        #endregion ------------------------------------------------> Label

        return True
    #---

    def Plot(self) -> bool:
        """Plot the data.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.SetAxis()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for idx,v in self.rIdx.items():
            x = range(1,len(self.rLabel)+1)
            y = self.rDF.iloc[idx,:]
            self.wPlot.dPlot['M'].rAxes.plot(x,y, label=f'{v[0]}')
        #------------------------------>
        if len(self.rIdx) > 1:
            self.wPlot.dPlot['M'].rAxes.legend()
        else:
            pass
        #------------------------------>
        self.wPlot.dPlot['M'].ZoomResetSetValues()
        self.wPlot.dPlot['M'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            WindowResCEvol(self.cParent, self.cDateC, self.cFileN))             # type: ignore
        #------------------------------>
        return True
    #---

    def ExportData(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        return super().ExportData(df=self.rData)
    #---

    def ExportImg(self) -> bool:
        """Save an image of the plot.

            Returns
            -------
            bool
        """
        return self.wPlot.dPlot['M'].SaveImage(
            mConfig.elMatPlotSaveI, parent=self)
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Close window and uncheck section in UMSAPFile window. Assumes
            self.parent is an instance of UMSAPControl.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update parent
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].remove(self)           # type: ignore
        #endregion --------------------------------------------> Update parent

        #region ------------------------------------> Reduce number of windows
        mConfig.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---

    def OnListSelect(self, event: Union[wx.CommandEvent, str]) -> bool:
        """What to do after selecting a row in the wx.ListCtrl.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        super().OnListSelect(event)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rIdx = self.wLC.wLCS.wLC.GetSelectedRows(True)
        self.Plot()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class WindowResCpR(BaseWindowResultOnePlotFA):
    """Plot the Cleavage per Residue for an analysis.

        Parameters
        ----------
        parent: WindowResTarProt
            Parent of the window.
        dateC: str
            Current date.
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rData: dict
            Keys are dates and values is the data to create the plot.
        rLabel: list[str]
            Label of the experiment.
        rLabelC: str
            Currently selected label.
        rNat: str
            Plot results for the native or recombinant protein.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rProtLength: list[int]
            Length of the recombinant and native protein.
        rProtLoc: list[int]
            Location of the native protein in the sequence of the recombinant
            protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.nwCpRPlot
    cSection = mConfig.nuCpR
    cColor   = mConfig.confColor[cName]
    #------------------------------>
    cNat = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent: WindowResTarProt,
        dateC : str,
        fileN : str
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f"{parent.cTitle} - {dateC} - {self.cSection}"
        self.cDateC = dateC
        self.cFileN = fileN
        self.rUMSAP = parent.cParent
        self.rObj   = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, parent.rDateC,fileN, [0,1])
        self.rLabel = self.rData.columns.unique(level=1).tolist()
        self.rProtLength = parent.rData[self.cDateC]['PI']['ProtLength']
        self.rProtLoc    = parent.rData[self.cDateC]['PI']['ProtLoc']
        menuData         = self.SetMenuDate()
        #------------------------------>
        super().__init__(parent, menuData)
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Plot
        self.UpdateResultWindow(nat=False, label=[menuData['Label'][0]])        # type: ignore
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the data to build the Tool menu.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1] is not None:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(
        self,
        nat    : bool,
        label  : str,
        protLoc: bool=True
        ) -> bool:
        """Update the results shown in the window.

            Parameters
            ----------
            nat: bool
                Plot results for the native (True) or recombinant (False)
                protein.
            label: str
                Plot results for this experiment.
            protLoc: bool
                Show native protein location (True) or not (False).

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rNat  = self.cNat[nat]
        self.rLabelC = label
        #------------------------------>
        idx = pd.IndexSlice
        #------------------------------>
        if nat:
            tXIdx = range(0, self.rProtLength[1])
        else:
            tXIdx = range(0, self.rProtLength[0])
        x = [x+1 for x in tXIdx]
        #------------------------------>
        color = []
        #------------------------------>
        yMax = self.rData.loc[:,idx[self.rNat,label]].max().max()               # type: ignore
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.SetAxis()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Plot
        for e in label:
            #------------------------------>
            y = self.rData.iloc[tXIdx, self.rData.columns.get_loc(idx[self.rNat,e])]                # type: ignore
            tColor = self.cColor['Spot'][
                self.rLabel.index(e)%len(self.cColor['Spot'])]
            color.append(tColor)
            #------------------------------>
            self.wPlot[0].rAxes.plot(x,y, color=tColor)
        #------------------------------>
        if self.rNat == self.cNat[False] and protLoc:
            if self.rProtLoc[0] is not None:
                self.wPlot[0].rAxes.vlines(
                    self.rProtLoc[0],0,yMax,linestyles='dashed',color='black',zorder=1)
                self.wPlot[0].rAxes.vlines(
                    self.rProtLoc[1],0,yMax,linestyles='dashed',color='black',zorder=1)
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> Plot

        #region ----------------------------------------------------> Legend
        leg = []
        for i in range(0, len(label), 1):
            leg.append(mpatches.Patch(
                color = color[i],
                label = label[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion -------------------------------------------------> Legend

        #region ---------------------------------------------------> Zoom
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(f'{self.cNat[self.rNat]}')
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------> Zoom

        return True
    #---

    def SetAxis(self) -> bool:
        """Set the axis of the plot.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot[0].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        self.wPlot[0].rAxes.yaxis.get_major_locator().set_params(integer=True)
        self.wPlot[0].rAxes.set_xlabel('Residue Number')
        self.wPlot[0].rAxes.set_ylabel('Number of Cleavages')
        #endregion ------------------------------------------------> Label

        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            WindowResCpR(self.cParent, self.cDateC, self.cFileN))               # type: ignore
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnUpdateStatusBar(self, event) -> bool:
        """Update the statusbar info

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            #------------------------------>
            x = event.xdata
            xf = round(x)
            idx = pd.IndexSlice
            #------------------------------>
            y = []
            try:
                for l in self.rLabelC:
                    col = self.rData.columns.get_loc(idx[self.rNat,l])
                    y.append(self.rData.iat[xf-1,col])
            except IndexError:
                self.wStatBar.SetStatusText('')
                return False
            #------------------------------>
            s = ''
            for k,l in enumerate(self.rLabelC):
                s = f'{s}{l}={y[k]}   '
            self.wStatBar.SetStatusText(f'Res={xf}   {s}')

        else:
            self.wStatBar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion ----------------------------------------------------------> Classes


#region -----------------------------------------------------------> wx.Dialog
class DialogMultipleCheckBox(BaseDialogOkCancel):
    """Present multiple choices as checkboxes.

        Parameters
        ----------
        title : str
            Title for the wx.Dialog.
        items : dict
            Keys are the name of the wx.CheckBox and values the label.
            Keys are also used to return the checked elements.
        nCol : int
            wx.CheckBox will be distributed in a grid of nCol and as many as
            needed rows.
        label : str
            Label for the wx.StaticBox.
        multiChoice : bool
            More than one wx.Checkbox can be selected (True) or not (False).
        parent : wx.Window
            Parent of the wx.Dialog.

        Attributes
        ----------
        rDict: dict
            Keys are 0 to N where N is the number of elements in items, nCol,
            label and multiChoice.
            {
                0: {
                    stBox  : wx.StaticBox,
                    checkB : [wx.CheckBox],
                    sFlex  : wx.FlexGridSizer,
                    sStBox : wx.StaticBoxSizer,
                },
            }
        checked : dict
            Keys are int 0 to N and values the names of the checked wx.CheckBox
            after pressing the OK button. The names are the keys in the
            corresponding item group.

        Notes
        -----
        At least one option must be selected for the OK button to close the
        wx.Dialog.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title      : str,
        items      : list[dict[str, str]],
        nCol       : list[int],
        label      : list[str]=['Options'],
        multiChoice: list[bool]=[False],
        parent     : Optional[wx.Window]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------>
        self.rDict = {}
        self.rChecked = {}
        #------------------------------>
        super().__init__(title=title, parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        try:
            for k,v in enumerate(label):
                self.rDict[k] = {}
                #------------------------------> wx.StaticBox
                self.rDict[k]['stBox'] = wx.StaticBox(self, label=v)
                #------------------------------> wx.CheckBox
                self.rDict[k]['checkB'] = []
                for j,i in items[k].items():
                    self.rDict[k]['checkB'].append(
                        wx.CheckBox(
                            self.rDict[k]['stBox'],
                            label = i,
                            name  = f'{j}-{k}'
                    ))
                #------------------------------> wx.Sizer
                self.rDict[k]['sFlex'] =(
                    wx.FlexGridSizer(ceil(len(items[k])/nCol[k]), nCol[k], 1,1))
                self.rDict[k]['sStBox'] = wx.StaticBoxSizer(
                    self.rDict[k]['stBox'], orient=wx.VERTICAL)
                #------------------------------> Bind
                if not multiChoice[k]:
                    [x.Bind(wx.EVT_CHECKBOX, self.OnCheck) for x in self.rDict[k]['checkB']]
                else:
                    pass
        except IndexError:
            msg = ('items, nCol, label and multiChoice must have the same '
                   'number of elements.')
            raise mException.InputError(msg)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        for k,v in self.rDict.items():
            #------------------------------> Add check to Flex
            for c in v['checkB']:
                v['sFlex'].Add(c, 0, wx.ALIGN_LEFT|wx.ALL, 7)
            #------------------------------> Add Flex to StaticBox
            v['sStBox'].Add(v['sFlex'], 0, wx.ALIGN_CENTER|wx.ALL, 5)
            #------------------------------> Add to Sizer
            self.sSizer.Add(v['sStBox'], 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------>
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnCheck(self, event:wx.CommandEvent) -> bool:
        """Deselect all other selected options.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Deselect
        if event.IsChecked():
            #------------------------------>
            tCheck = event.GetEventObject()
            group = int(tCheck.GetName().split('-')[1])
            #------------------------------>
            [k.SetValue(False) for k in self.rDict[group]['checkB']]
            #------------------------------>
            tCheck.SetValue(True)
        else:
            pass
        #endregion -------------------------------------------------> Deselect

        return True
    #---

    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Validate
        #------------------------------>
        for k in self.rDict:
            for c in self.rDict[k]['checkB']:
                if c.IsChecked():
                    self.rChecked[k] = c.GetName().split('-')[0]
                else:
                    pass
        #------------------------------>
        if self.rChecked and len(self.rChecked) == len(self.rDict):
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion -------------------------------------------------> Validate

        return True
    #---

    def GetChoice(self) -> dict:
        """Get the selected checkbox.

            Returns
            -------
            dict
                The keys are 0 to N and values the items corresponding to the
                checked wx.CheckBox in each group.
        """
        return self.rChecked
    #---
    #endregion ------------------------------------------------> Class methods
#---


class DialogUserInputText(BaseDialogOkCancel):
    """Present a modal window with N wx.TextCtrl for user input.

        Parameters
        ----------
        title : str
            Title of the dialog.
        label : list[str]
            Labels for the wx.StaticText in the dialog.
        hint : list[str]
            Hint for the wx.TextCtrl in the dialog.
        parent : wx.Window or None
            To center the dialog on the parent.
        validator : list[wx.Validator]
            The validator is expected to comply with the return of validators in
            mValidator.
        size : wx.Size
            Size of the window. Default is (100, 70)

        Attributes
        ----------
        rInput : list[mWidget.StaticTextCtrl]

        Notes
        -----
        A valid input must be given for the wx.Dialog to be closed after
        pressing the OK button.
        The number of mWidget.StaticTextCtrl to be created is taken from
        the label parameter.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title    : str,
        label    : list[str],
        hint     : list[str],
        validator: list[wx.Validator],
        parent   : Union[wx.Window, None]=None,
        values   : list[str]=[],
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent, title=title)
        #------------------------------>
        self.rInput = []
        if values:
            self.rValues = values
        else:
            self.rValues = ['' for x in label]
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        for k,v in enumerate(label):
            self.rInput.append(mWidget.StaticTextCtrl(
                self,
                stLabel   = v,
                tcHint    = hint[k],
                validator = validator[k],
            ))
            self.rInput[k].wTc.SetValue(self.rValues[k])
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        #------------------------------>
        for k in self.rInput:
            self.sSizer.Add(k.wSt, 0, wx.ALIGN_LEFT|wx.UP|wx.LEFT|wx.RIGHT, 5)
            self.sSizer.Add(k.wTc, 0, wx.EXPAND|wx.DOWN|wx.LEFT|wx.RIGHT, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        wrong = []
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Validate
        for k in self.rInput:
            if k.wTc.GetValidator().Validate()[0]:
                pass
            else:
                wrong.append(k)
                k.wTc.SetValue('')
        #endregion -------------------------------------------------> Validate

        #region ---------------------------------------------------> Return
        if not wrong:
            self.EndModal(1)
            self.Close()
            return True
        else:
            return False
        #endregion ------------------------------------------------> Return
    #---

    def GetValue(self) -> list[str]:
        """Get the values of the wx.TextCtrl.

            Returns
            -------
            list[str]
        """
        #region --------------------------------------------------->
        listO = []
        #------------------------------>
        for k in self.rInput:
            listO.append(k.wTc.GetValue())
        #endregion ------------------------------------------------>

        return listO
    #---
    #endregion ------------------------------------------------> Class methods
#---


class DialogFilterRemoveAny(BaseDialogOkCancel):
    """Dialog to select Filters to remove in ProtProfPlot.

        Parameters
        ----------
        filterList : list
            List of already applied filter, e.g.:
            [['Text', {kwargs} ], ...]
        parent : wx.Window
            Parent of the window.

        Attributes
        ----------
        rCheckB: list[wx.CheckBox]
            List of wx.CheckBox to show in the window
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.ndFilterRemoveAny
    #------------------------------>
    cSize = (900, 580)
    #------------------------------>
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #------------------------------>
    cTitle = 'Remove Selected Filters'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        filterList: list,
        parent    : Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCheckB = []
        #------------------------------>
        super().__init__(title=self.cTitle, parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(self, label='Select Filters to remove.')
        #------------------------------>
        for k in filterList:
            self.rCheckB.append(wx.CheckBox(
                self, label=f'{k[0]} {k[1].get("gText", "")}'))
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        #------------------------------>
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        #------------------------------>
        self.sSizer.Add(self.wSt, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        for k in self.rCheckB:
            self.sSizer.Add(k, 0 , wx.ALIGN_LEFT|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ----------------------------------------------------> Sizer

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage methods
    def GetChecked(self) -> list[int]:
        """Get the number of the checked wx.CheckBox.

            Returns
            -------
            list of int
                The index in self.checkB of the checked wx.CheckBox
        """
        #region ---------------------------------------------------> Variables
        lo = []
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Get Checked
        for k,cb in enumerate(self.rCheckB):
            lo.append(k) if cb.IsChecked() else None
        #endregion ----------------------------------------------> Get Checked

        return lo
    #---
    #endregion -----------------------------------------------> Manage methods
#---


class DialogFilterPValue(DialogUserInputText):
    """Dialog to filter values by P value.

        Parameters
        ----------
        cTitle : str
            Title of the wx.Dialog
        cLabel : str
            Label for the wx.StaticText
        cHint : str
            Hint for the wx.TextCtrl.
        cParent : wx.Window
            Parent of the wx.Dialog
        cValidator : wx.Validator
            Validator for the wx.TextCtrl
        cSize : wx.Size
            Size of the wx.Dialog. Default is (420, 170)
    """
    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title    : str,
        label    : str,
        hint     : str,
        parent   : Union[wx.Window, None]=None,
        validator: wx.Validator=wx.DefaultValidator,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(
            title     = title,
            label     = [label],
            hint      = [hint],
            parent    = parent,
            validator = [validator],
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wCbAbs = wx.CheckBox(self, label='Absolute P Value')
        self.wCbLog = wx.CheckBox(self, label='-Log10(P) Value')
        self.rCheck = [self.wCbAbs, self.wCbLog]
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------>
        self.sCheck = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.sCheck.Add(self.wCbAbs, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sCheck.Add(self.wCbLog, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer.Detach(self.sBtn)
        #------------------------------>
        self.sSizer.Add(self.sCheck, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.rInput[0].wTc.Bind(wx.EVT_TEXT, self.OnTextChange)
        for x in self.rCheck:
            x.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnTextChange(self, event: wx.Event) -> bool:
        """Select -log10P if the given value is > 1.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Check
        if self.rInput[0].wTc.GetValidator().Validate()[0]:
            #------------------------------> Get val
            val = float(self.rInput[0].wTc.GetValue().strip().split(' ')[1])
            #------------------------------>
            if val > 1:
                self.wCbAbs.SetValue(False)
                self.wCbLog.SetValue(True)
            else:
                pass
        else:
            pass
        #endregion ----------------------------------------------------> Check

        return True
    #---

    def OnCheck(self, event: wx.CommandEvent) -> bool:
        """Allow only one check box to be marked at any given time.

            Parameters
            ----------
            event: wx.Event
             Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Deselect
        if event.IsChecked():
            #------------------------------>
            tCheck = event.GetEventObject()
            #------------------------------>
            [k.SetValue(False) for k in self.rCheck]
            #------------------------------>
            tCheck.SetValue(True)
        else:
            pass
        #endregion -------------------------------------------------> Deselect

        return True
    #---

    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            True
        """
        #region ----------------------------------------------------> Validate
        #------------------------------> Operand and Value
        tca = self.rInput[0].wTc.GetValidator().Validate()[0]
        #------------------------------> CheckBox
        absB = self.wCbAbs.IsChecked()
        logB = self.wCbLog.IsChecked()
        if absB and logB:
            tcb = False
        elif absB or logB:
            tcb = True
        else:
            tcb = False
        #------------------------------> All
        if tca and tcb:
            self.EndModal(1)
            self.Close()
        else:
            self.rInput[0].wTc.SetValue('')
        #endregion -------------------------------------------------> Validate

        return True
    #---

    def GetValue(self) -> tuple[str, bool]:
        """Get user values.

            Returns
            -------
            tuple(str, bool)
        """
        uText = self.rInput[0].wTc.GetValue()
        absB  = self.wCbAbs.IsChecked()

        return (uText, absB)
    #---
    #endregion ------------------------------------------------> Event methods
#---


class DialogVolColorScheme(BaseDialogOkCancel):
    """Dialog for the setup of the color in the volcano plot of ProtProf.

        Parameters
        ----------
        t0: float
        s0: float
        z: str
            '< 10' or '> 1.56'
        color: str
            Color scheme to use
        hcurve : bool
            Show (True) or not (False) the H Curve
        parent: wx.Window
            Parent of the wx.Dialog
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        t0    : float,
        s0    : float,
        z     : float,
        p     : float,
        fc    : float,
        parent: Optional[wx.Window]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rValInit = {
            'T0': str(t0),
            'S0': str(s0),
            'Z' : str(z),
            'P' : str(p),
            'FC': str(fc),
        }
        #------------------------------>
        super().__init__(title='Color Scheme Parameters', parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wsbHC = wx.StaticBox(self, label='Hyperbolic Curve')
        self.wT0 = mWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = 't0',
            tcHint    = 'e.g. 1.0',
            tcSize    = (100,22),
            validator = mValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wT0.wTc.SetValue(self.rValInit['T0'])

        self.wS0 = mWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = 's0',
            tcHint    = 'e.g. 0.1',
            tcSize    = (100,22),
            validator = mValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wS0.wTc.SetValue(self.rValInit['S0'])

        self.wsbPFC = wx.StaticBox(self, label='Log2FC - P')
        self.wP = mWidget.StaticTextCtrl(
            self.wsbPFC,
            stLabel   = 'P',
            tcHint    = 'e.g. 0.05',
            tcSize    = (100,22),
            validator = mValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wP.wTc.SetValue(self.rValInit['P'])

        self.wFC = mWidget.StaticTextCtrl(
            self.wsbPFC,
            stLabel   = 'log2FC',
            tcHint    = 'e.g. 0.1',
            tcSize    = (100,22),
            validator = mValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wFC.wTc.SetValue(self.rValInit['FC'])

        self.wsbZ = wx.StaticBox(self, label='Z Score')
        self.wZ = mWidget.StaticTextCtrl(
            self.wsbZ,
            stLabel   = 'Z Score',
            tcHint    = 'e.g. 10.0',
            tcSize    = (100,22),
            validator = mValidator.NumberList(
                    numType='float', vMin=0, vMax=100, nN=1),
        )
        self.wZ.wTc.SetValue(self.rValInit['Z'])
        #------------------------------>
        self.rWList = {
            'T0': self.wT0.wTc,
            'S0': self.wS0.wTc,
            'P' : self.wP.wTc,
            'FC': self.wFC.wTc,
            'Z' : self.wZ.wTc,
        }
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sFlexHC = wx.FlexGridSizer(2,2,1,1)
        self.sFlexHC.Add(self.wT0.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexHC.Add(self.wT0.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexHC.Add(self.wS0.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexHC.Add(self.wS0.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexHC.AddGrowableCol(1,1)

        self.sFlexPFC = wx.FlexGridSizer(2,2,1,1)
        self.sFlexPFC.Add(self.wP.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexPFC.Add(self.wP.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexPFC.Add(self.wFC.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexPFC.Add(self.wFC.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexPFC.AddGrowableCol(1,1)

        self.sFlexZ = wx.FlexGridSizer(2,2,1,1)
        self.sFlexZ.Add(self.wZ.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.Add(self.wZ.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.AddGrowableCol(1,1)

        self.ssbHC = wx.StaticBoxSizer(self.wsbHC, wx.VERTICAL)
        self.ssbHC.Add(self.sFlexHC, 0, wx.EXPAND|wx.ALL, 5)

        self.ssbPFC = wx.StaticBoxSizer(self.wsbPFC, wx.VERTICAL)
        self.ssbPFC.Add(self.sFlexPFC, 0, wx.EXPAND|wx.ALL, 5)

        self.ssbZ = wx.StaticBoxSizer(self.wsbZ, wx.VERTICAL)
        self.ssbZ.Add(self.sFlexZ, 0, wx.EXPAND|wx.ALL, 5)

        self.sFlexVal = wx.FlexGridSizer(1,3,1,1)
        self.sFlexVal.Add(self.ssbHC, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlexVal.Add(self.ssbPFC, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlexVal.Add(self.ssbZ, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlexVal.AddGrowableCol(0,1)
        self.sFlexVal.AddGrowableCol(1,1)
        self.sFlexVal.AddGrowableCol(2,1)

        self.sSizer.Add(self.sFlexVal, 0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Validate
        res = []
        #------------------------------>
        for k,w in self.rWList.items():
            if w.GetValidator().Validate()[0]:
                res.append(True)
            else:
                w.SetValue(self.rValInit[k])
                res.append(False)
        #endregion -------------------------------------------------> Validate

        #region --------------------------------------------------->
        if all(res):
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion ------------------------------------------------>

        return True
    #---

    def GetVal(self):
        """Get the selected values.

            Returns
            -------
            bool
        """
        return (
            float(self.wT0.wTc.GetValue()),
            float(self.wS0.wTc.GetValue()),
            float(self.wP.wTc.GetValue()),
            float(self.wFC.wTc.GetValue()),
            float(self.wZ.wTc.GetValue()),
        )
    #---
    #endregion ------------------------------------------------> Class methods
#---


class DialogFABtnText(BaseDialogOkCancel):
    """Further Analysis Dialog with a wx.Button and wx.TextCtrl.

        Parameters
        ----------
        btnLabel: str
            Label for the wx.Button.
        btnHint: str
            Hint for the wx.Button.
        ext: str
            Extension for selecting file.
        btnValidator: wx.Validator
            Validator for user input.
        stLabel: str
            Label for the wx.StaticText.
        stHint: str
            Hint for the wx.StaticText.
        stValidator: wx.Validator
            Validator for the wx.TextCtrl.
        parent: wx.Window or None
            Parent for the wx.Dialog.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        btnLabel    : str,
        btnHint     : str,
        ext         : str,
        btnValidator: wx.Validator,
        stLabel     : str,
        stHint      : str,
        stValidator : wx.Validator,
        parent      : Optional[wx.Window]=None):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(title='Export Sequence Alignments', parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnTc = mWidget.ButtonTextCtrlFF(
            self,
            btnLabel  = btnLabel,
            tcHint    = btnHint,
            ext       = ext,
            mode      = 'save',
            validator = btnValidator,
        )
        self.wLength = mWidget.StaticTextCtrl(
            self,
            stLabel   = stLabel,
            tcHint    = stHint,
            validator = stValidator,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sFlex = wx.FlexGridSizer(2,2,1,1)
        self.sFlex.Add(self.wBtnTc.wBtn, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.Add(self.wBtnTc.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.Add(self.wLength.wSt, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sFlex.Add(self.wLength.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.AddGrowableCol(1,1)
        #------------------------------>
        self.sSizer.Add(self.sFlex, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool

            Notes
            -----
            Basic implementation. Override as needed.
        """
        #region --------------------------------------------------->
        errors = 0
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        print(self.wBtnTc.wTc.GetValidator().Validate())
        print(self.wLength.wTc.GetValidator().Validate())
        if self.wBtnTc.wTc.GetValidator().Validate()[0]:
            pass
        else:
            errors += 1
            self.wBtnTc.wTc.SetValue('')

        if self.wLength.wTc.GetValidator().Validate()[0]:
            pass
        else:
            errors += 1
            self.wLength.wTc.SetValue('')
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        if not errors:
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion ----------------------------------------------------->

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class DialogFA2Btn(BaseDialogOkCancel):
    """Further Analysis Dialog with two wx.Buttons.

        Parameters
        ----------
        btnLabel: list[str]
            Label for the wx.Buttons.
        btnHint: list[str]
            Hints for the wx.Buttons.
        ext: list[str]
            Extensions for the files.
        btnValidator: list[wx.Validator]
            User input validators
        parent: wx.Window or None
            Parent of the wx.Dialog.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        btnLabel    : list[str],
        btnHint     : list[str],
        ext         : list[str],
        btnValidator: list[wx.Validator],
        parent      : Optional[wx.Window]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(title='PDB Mapping', parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnI = mWidget.ButtonTextCtrlFF(
            self,
            btnLabel  = btnLabel[0],
            tcHint    = btnHint[0],
            ext       = ext[0],
            mode      = 'openO',
            validator = btnValidator[0],
        )

        self.wBtnO = mWidget.ButtonTextCtrlFF(
            self,
            btnLabel  = btnLabel[1],
            tcHint    = btnHint[1],
            ext       = ext[1],
            mode      = 'folder',
            validator = btnValidator[1],
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sFlex = wx.FlexGridSizer(2,2,1,1)
        self.sFlex.Add(self.wBtnI.wBtn, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.Add(self.wBtnI.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.Add(self.wBtnO.wBtn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sFlex.Add(self.wBtnO.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sFlex.AddGrowableCol(1,1)

        self.sSizer.Add(self.sFlex, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool

            Notes
            -----
            Basic implementation. Override as needed.
        """
        #region --------------------------------------------------->
        errors = 0
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if self.wBtnI.wTc.GetValidator().Validate()[0]:
            pass
        else:
            errors += 1
            self.wBtnI.wTc.SetValue('')

        if self.wBtnO.wTc.GetValidator().Validate()[0]:
            pass
        else:
            errors += 1
            self.wBtnO.wTc.SetValue('')
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        if not errors:
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion ----------------------------------------------------->

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion --------------------------------------------------------> wx.Dialog

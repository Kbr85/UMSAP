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


"""Windows for the protpof module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Union, Optional, Literal, TYPE_CHECKING

import numpy  as np
import pandas as pd

import matplotlib.patches as mpatches

from scipy import stats

import wx

from config.config import config as mConfig
from core     import statistic as cStatistic
from core     import validator as cValidator
from core     import method    as cMethod
from core     import widget    as cWidget
from core     import window    as cWindow
from main     import menu      as mMenu
from protprof import method    as protMethod

if TYPE_CHECKING:
    from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


LIT_Z_LINES = Literal[
    f'{mConfig.prot.lmFilterZScore} Line',
    f'{mConfig.prot.lmFilterHypCurve} Line',
    f'{mConfig.prot.lmColorSchemePLog2} Line'
]


#region -------------------------------------------------------------> Classes
class ResProtProf(cWindow.BaseWindowResultListTextNPlot):
    """Plot results in the Proteome Profiling section of an UMSAP file.

        Parameters
        ----------
        parent: resWindow.UMSAPControl

        Attributes
        ----------
        dKeyMethod: dict
            Keys are str and values methods to manage the window.
        rAutoFilter: bool
            Apply defined filters (True) when changing date or not (False).
            Default is False.
        rColor: str
            Color mode.
        rCondC: str
            Condition currently selected.
        rCorrP: bool
            Use corrected P values (True) or not (False). Default is False.
        rData: cMethod.BaseAnalysis
            For each Proteome Profiling analysis a new attribute 'Date-ID' is
            added with value protMethod.ProtAnalysis.
        rDataC: protMethod.ProtAnalysis
            Data for currently selected date
        rDate: list of str
            List of available dates in the section.
        rDateC: str
            Currently selected date.
        rDf: pd.DataFrame
            DF with the data currently display in the window.
        rFcXLabel: list of str
            List of labels for the x axis in the FC plot.
        rFcXRange: list of float
            Min and Max value for the x axis in the FC plot.
        rFcYMax: list of float
            Max log2FC value on all conditions for the relevant points.
        rFcYMin: list of float
            Min log2FC value on all conditions for the relevant points.
        rFcYRange: list of float
            Min and Max value for the y axis in the FC Plot including the CI.
        rFilterList: list
            List of applied filters. e.g. [['Key', {kwargs}], 'StatusBarText']
        rGreenP: matplotlib object
            Reference to the green dot shown in the Volcano plot after selecting
            a protein in the wx.ListCtrl.
        rLabelProt: list
            List of proteins to label
        rLCIdx: int or None
            Selected row in the wx.ListCtrl.
        rLockScale: str
            Lock plot scale to No, Date or Project.
        rLog2FC: float
            Limit for the Log2FC value.
        rObj: UMSAPFile
            Reference to the UMSAPFile object.
        rP: float
            Limit for the P values.
        rPickLabel: bool
            Pick labels or show data of selected protein.
        rProtLine: matplotlib object
            Protein line drawn in the FC plot after selecting a protein in the
            wx.ListCtrl.
        rRpC: str
            Currently selected relevant point.
        rS0: float
            s0 value to calculate the hyperbolic curve
        rShowAll: bool
            Show (True) fcYMax and fcYMin in the FC plot or not (False).
            Default is True.
        rT0: float
            t0 value to calculate the hyperbolic curve
        rVolLines: list[str]
            Lines to plot in the Volcano plot.
        rVXRange: list of float
            Min and Max values for the x axis in the Vol plot.
        rVYRange: list of float
            Min and Max values for the y axis in the Vol plot.
        rZ: float
            Z Value for the Volcano plot.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.prot.nwRes
    cSection = mConfig.prot.nMod
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
    cLNPlot = ['Vol', 'FC']
    #------------------------------> Title
    cTList = 'Protein List'
    cTText = 'Profiling Details'
    #------------------------------> Sizes
    cSWindow = mConfig.core.sWinModPlot
    cSCol    = [45, 70, 100]
    #------------------------------> Hints
    cHSearch = 'Protein List'
    #------------------------------> Other
    cNPlotCol = 2
    cImgName   = {
        mConfig.prot.kwVol: '{}-Vol-{}.tiff',
        mConfig.prot.kwFC : '{}-Evol-{}.tiff',
    }
    #------------------------------> Color
    cCV      = mConfig.prot.cCV
    cFCAll   = mConfig.prot.cFCAll
    cFCLines = mConfig.prot.cFCLines
    cVol     = mConfig.prot.cVol
    cVolSel  = mConfig.prot.cVolSel
    #------------------------------> Columns in DF
    cColGene = mConfig.prot.dfColGene
    cColProt = mConfig.prot.dfColProt
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:'resWindow.UMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj            = parent.rObj
        self.rData:cMethod.BaseAnalysis = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        #------------------------------>
        self.ReportPlotDataError()
        #------------------------------>
        self.cTitle       = f"{parent.cTitle} - {self.cSection}"
        self.rDf          = pd.DataFrame()
        self.rDateC       = self.rDate[0]
        self.rDataC:protMethod.ProtAnalysis = getattr(self.rData, self.rDateC)
        self.rCondC       = menuData['crp'][self.rDate[0]]['C'][0]
        self.rRpC         = menuData['crp'][self.rDate[0]]['RP'][0]
        self.rGreenP      = None
        self.rCorrP       = False
        self.rShowAll     = True
        self.rAutoFilter  = False
        self.rT0          = 0.1
        self.rS0          = 1.0
        self.rZ           = 10.0
        self.rP           = getattr(self.rData, self.rDateC).alpha
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
        self.rVolLinesZ   = f'{mConfig.prot.lmFilterZScore} Line'
        #------------------------------>
        super().__init__(parent)
        #------------------------------> Methods
        dKeyMethod = {
            #------------------------------> Set Range of Plots
            mConfig.prot.kwScaleNo               : self.LockScale,
            mConfig.prot.kwScaleAnalysis         : self.LockScale,
            mConfig.prot.kwScaleProject          : self.LockScale,
            f'{mConfig.prot.lmScaleNo} Set'      : self.SetRangeNo,
            f'{mConfig.prot.lmScaleAnalysis} Set': self.SetRangeDate,
            f'{mConfig.prot.lmScaleProject} Set' : self.SetRangeProject,
            #------------------------------> Get DF for Text Intensities
            mConfig.prot.oControlType['OC']   : self.GetDF4TextInt_OC,
            mConfig.prot.oControlType['OCC']  : self.GetDF4TextInt_OCC,
            mConfig.prot.oControlType['OCR']  : self.GetDF4TextInt_OCR,
            mConfig.prot.oControlType['Ratio']: self.GetDF4TextInt_RatioI,
            #------------------------------> Colors
            mConfig.prot.kwVolPlotColorConf           : self.VolColorConf,
            mConfig.prot.kwVolPlotColorScheme         : self.VolDraw,
            f'{mConfig.prot.lmFilterHypCurve} Color'  : self.GetColorHyCurve,
            f'{mConfig.prot.lmColorSchemePLog2} Color': self.GetColorPLog2FC,
            f'{mConfig.prot.lmFilterZScore} Color'    : self.GetColorZScore,
            #------------------------------> Lines
            f'{mConfig.prot.lmFilterHypCurve} Line'  : self.DrawLinesHypCurve,
            f'{mConfig.prot.lmColorSchemePLog2} Line': self.DrawLinesPLog2FC,
            f'{mConfig.prot.lmFilterZScore} Line'    : self.DrawLinesZScore,
            #------------------------------> Filter methods
            mConfig.prot.kwFilterApplyAll  : self.FilterApply,
            mConfig.prot.kwFilterApplyAuto : self.AutoFilter,
            mConfig.prot.kwFilterCopy      : self.FilterCopy,
            mConfig.prot.kwFilterFCEvol    : self.Filter_FCChange,
            mConfig.prot.kwFilterFCLog     : self.Filter_Log2FC,
            mConfig.prot.kwFilterHypCurve  : self.Filter_HCurve,
            mConfig.prot.kwFilterLoad      : self.FilterLoad,
            mConfig.prot.kwFilterPaste     : self.FilterPaste,
            mConfig.prot.kwFilterPVal      : self.Filter_PValue,
            mConfig.prot.kwFilterRemoveAll : self.FilterRemoveAll,
            mConfig.prot.kwFilterRemoveAny : self.FilterRemoveAny,
            mConfig.prot.kwFilterRemoveLast: self.FilterRemoveLast,
            mConfig.prot.kwFilterSave      : self.FilterSave,
            mConfig.prot.kwFilterZScore    : self.Filter_ZScore,
            #------------------------------>
            mConfig.prot.kwClearSelLabel: self.ClearLabel,
            mConfig.prot.kwClearSelSel  : self.ClearSel,
            mConfig.prot.kwClearSelAll  : self.ClearAll,
            #------------------------------>
            mConfig.prot.kwVolPlotLabelPick : self.LabelPick,
            mConfig.prot.kwVolPlotLabelProt : self.ProtLabel,
            #------------------------------>
            mConfig.prot.kwFCShowAll : self.FCChange,
            #------------------------------>
            mConfig.prot.kwExportDataFiltered : self.ExportDataFiltered,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wStatBar.SetFieldsCount(2, [100, -1])
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

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
    def StatusBarFilterText(self, text:str) -> bool:
        """Update the StatusBar text.

            Parameters
            ----------
            text: str
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
        date     = self.rData.date
        menuData = {'crp' : {}, 'MenuDate': []}
        #------------------------------> Fill
        for k in self.rData.date:
            data = getattr(self.rData, k)
            #------------------------------>
            menuData['crp'][k] = {
                'C' : data.labelA,
                'RP': data.labelB,
            }
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
        data.insert(0, 'kbr', self.rDf.index.values.tolist())                   # type: ignore
        data = data.astype(str)                                                 # type: ignore
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
        for c in self.rDataC.labelB:
            #------------------------------>
            df = self.rDataC.df.loc[:,idx[:,c,'FC']]                            # type: ignore
            #------------------------------>
            ymax.append(df.max().max())
            ymin.append(df.min().min())
        #endregion ------------------------------------------------> Fill List

        return [ymax, ymin]
    #---

    def VolDraw(self, colorLabel:str='') -> bool:
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
            "log$_{2}$[FC]", fontweight="bold")
        self.wPlot.dPlot['Vol'].rAxes.set_ylabel(
            "-log$_{10}$[p]", fontweight="bold")
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
            if self.rGreenP is not None:
                self.rGreenP.remove()
                self.rGreenP = None
            #------------------------------>
            return False
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
        if self.rGreenP is not None:
            self.rGreenP.remove()
        #------------------------------> Add new one
        self.rGreenP = self.wPlot.dPlot['Vol'].rAxes.scatter(
            x, y,
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = self.cVolSel,
        )
        #------------------------------> Draw
        self.wPlot.dPlot['Vol'].rCanvas.draw()
        #endregion ---------------------------------------------> Volcano Plot

        return True
    #---

    def AddProtLabel(self, draw:bool=False, checkKey:bool=False) -> bool:
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
        if not self.rLabelProt:
            if draw:
                self.wPlot.dPlot['Vol'].rCanvas.draw()
            #------------------------------>
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
        dX = dX * 0.01

        dY = self.wPlot.dPlot['Vol'].rAxes.get_ylim()
        dY = dY[1] - dY[0]
        dY = dY * 0.01
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for prot in self.rLabelProt:
            tIdx = int(prot[0])
            tKey = prot[0]
            #------------------------------>
            if tKey in self.rLabelProtD.keys() and checkKey:
                continue
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
                    x-dX,y-dY, prot[1], ha='right',va='top')
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
            color = self.cFCAll
            x = list(range(0,len(self.rFcYMin)))
            #------------------------------>
            self.wPlot.dPlot['FC'].rAxes.plot(self.rFcYMax, color=color)
            self.wPlot.dPlot['FC'].rAxes.plot(self.rFcYMin, color=color)
            #------------------------------>
            self.wPlot.dPlot['FC'].rAxes.fill_between(
                x, self.rFcYMax, self.rFcYMin, color=color, alpha=0.2)
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
            "log$_{2}$[FC]", fontweight="bold")
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
            if self.rProtLine:
                for k in self.rProtLine:
                    k[0].remove()
                #------------------------------>
                self.rProtLine = []
            #------------------------------>
            return False
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
        colorN = len(self.cFCLines)
        x = list(range(0, len(self.rDataC.labelB)+1))
        #------------------------------>
        for k,c in enumerate(self.rDataC.labelA):
            #------------------------------> FC values
            y = self.rDf.loc[self.rDf.index[[idxL]],idx[c,:,'FC']]              # type: ignore
            y = [0.0] + y.values.tolist()[0]                                    # type: ignore
            #------------------------------> Errors
            yError = self.rDf.loc[self.rDf.index[[idxL]],idx[c,:,'CI']]         # type: ignore
            yError = [0] + yError.values.tolist()[0]                            # type: ignore
            #------------------------------> Colors
            color = self.cFCLines[k%colorN]
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
        dfList = self.dKeyMethod[self.rDataC.ctrlType](self.rLCIdx)             # type: ignore
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
        col:list[str],
        rp:list[str],
        cond:list[str],
        ) -> pd.DataFrame:
        """Creates the empty dataframe to be used in GetDF4Text functions.

            Parameters
            ----------
            col: list of str
                Name of the columns in the df.
            rp: list of str
                List of relevant points.
            cond: list of str
                List of conditions.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Variables
        nCol = len(col)
        idx  = pd.IndexSlice
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

    def GetDF4TextPFC(self, pID:int) -> pd.DataFrame:
        """Get the dataframe to print the P and FC +/- CI values to the text.

            Parameters
            ----------
            pID: int
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
        dfo  = self.GetDF4Text(
            ['FC (CI)', 'P'], self.rDataC.labelB, self.rDataC.labelA)
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.rDataC.labelA):
            for t in self.rDataC.labelB:
                #------------------------------> Get Values
                p  = self.rDf.at[self.rDf.index[pID],(c,t,'P')]
                fc = self.rDf.at[self.rDf.index[pID],(c,t,'FC')]
                ci = self.rDf.at[self.rDf.index[pID],(c,t,'CI')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'P')] = p
                dfo.at[dfo.index[k], (t,'FC (CI)')] = f'{fc} ({ci})'
        #endregion -----------------------------------------------> Add Values

        return dfo
    #---

    def GetDF4TextInt_OC(self, pID:int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID: int
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
        aveC = self.rDf.at[
            self.rDf.index[pID],(self.rDataC.labelA[0], self.rDataC.labelB[0], 'aveC')]
        stdC = self.rDf.at[
            self.rDf.index[pID], (self.rDataC.labelA[0], self.rDataC.labelB[0], 'stdC')]
        #------------------------------>
        dfc = pd.DataFrame({
            'Condition': self.rDataC.ctrlName,
            'Ave'      : [aveC],
            'Std'      : [stdC]
        })
        #endregion -------------------------------------------------------> DF

        #region ---------------------------------------------------------> DFO
        dfo = self.GetDF4TextInt_RatioI(pID)
        #endregion ------------------------------------------------------> DFO

        return [dfc] + dfo
    #---

    def GetDF4TextInt_OCC(self, pID:int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control per Column.

            Parameters
            ----------
            pID: int
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
            ['Ave', 'Std'],
            self.rDataC.labelB,
            [self.rDataC.ctrlName]+self.rDataC.labelA,
        )
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for c in self.rDataC.labelA:
            for t in self.rDataC.labelB:
                #------------------------------> Get Values
                aveC = self.rDf.at[self.rDf.index[pID],(c,t,'aveC')]
                stdC = self.rDf.at[self.rDf.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[0], (t,'Ave')] = aveC
                dfo.at[dfo.index[0], (t,'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.rDataC.labelA, start=1):
            for t in self.rDataC.labelB:
                #------------------------------> Get Values
                ave = self.rDf.at[self.rDf.index[pID],(c,t,'ave')]
                std = self.rDf.at[self.rDf.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values

        return [dfo]
    #---

    def GetDF4TextInt_OCR(self, pID:int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID: int
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
            ['Ave', 'Std'],
            [self.rDataC.ctrlName]+self.rDataC.labelB,
            self.rDataC.labelA,
        )
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for k,c in enumerate(self.rDataC.labelA):
            for t in self.rDataC.labelB:
                #------------------------------> Get Values
                aveC = self.rDf.at[self.rDf.index[pID],(c,t,'aveC')]
                stdC = self.rDf.at[self.rDf.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (self.rDataC.ctrlName,'Ave')] = aveC
                dfo.at[dfo.index[k], (self.rDataC.ctrlName,'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.rDataC.labelA):
            for t in self.rDataC.labelB:
                #------------------------------> Get Values
                ave = self.rDf.at[self.rDf.index[pID],(c,t,'ave')]
                std = self.rDf.at[self.rDf.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values

        return [dfo]
    #---

    def GetDF4TextInt_RatioI(self, pID:int) -> list[pd.DataFrame]:
        """Get the dataframe to print the ave and std for intensities for
            control type One Control.

            Parameters
            ----------
            pID: int
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
        dfo = self.GetDF4Text(
            ['Ave', 'Std'],
            self.rDataC.labelB,
            self.rDataC.labelA,
        )
        #endregion -------------------------------------------------------> DF

        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.rDataC.labelA):
            for t in self.rDataC.labelB:
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

    def GetVolXYRange(self, date:str) -> list[list[float]]:
        """Get the XY range for the volcano plot for the given date.

            Parameters
            ----------
            date: str
                A valid date from the project.

            Returns
            -------
            list of list of floats
                [xRange, yRange] e.g. [[-0.3, 0.3], [-0.1, 4.5]]
        """
        #region ---------------------------------------------------> Variables
        data = getattr(self.rData, date)
        idx  = pd.IndexSlice
        #------------------------------>
        x = data.df.loc[:, idx[:,:,'FC']]
        #------------------------------>
        if self.rCorrP:
            y = data.df.loc[:, idx[:,:,'Pc']]
        else:
            y = data.df.loc[:, idx[:,:,'P']]
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
        dm = 2 * lim * mConfig.core.MatPlotMargin
        #-------------->
        xRange.append(-lim - dm)
        xRange.append(lim + dm)
        #------------------------------> Y
        ymax = y.max().max()
        #-------------->
        dm = 2 * ymax * mConfig.core.MatPlotMargin
        #-------------->
        yRange.append(0 - dm)
        yRange.append(ymax + dm)
        #endregion ------------------------------------------------> Get Range

        return [xRange, yRange]
    #---

    def GetFcXYRange(self, date:str) -> list[list[float]]:
        """Get the XY range for the FC plot, including the CI.

            Parameters
            ----------
            date: str
                The selected date.

            Returns
            -------
            list of list of floats
                [xRange, yRange] e.g. [[-0.3, 3.3], [-0.1, 4.5]]
        """
        #region ---------------------------------------------------> Variables
        data = getattr(self.rData, date)
        idx  = pd.IndexSlice
        #------------------------------>
        y   = data.df.loc[:, idx[:,:,'FC']]
        yCI = data.df.loc[:, idx[:,:,'CI']]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Get Range
        #------------------------------> X
        dm = len(self.rDataC.labelB) * mConfig.core.MatPlotMargin
        #-------------->
        xRange = [-dm, len(self.rDataC.labelB) + dm]
        #------------------------------> Y
        #-------------->
        yMax  = y.max().max()
        yMin  = y.min().min()
        ciMax = yCI.max().max()
        #-------------->
        yminLim = yMin - ciMax
        ymaxLim = yMax + ciMax
        #-------------->
        dm = (ymaxLim - yminLim) * mConfig.core.MatPlotMargin
        #-------------->
        yRange = [yminLim - dm, ymaxLim + dm]
        #endregion ------------------------------------------------> Get Range

        return [xRange, yRange]
    #---

    def VolXYRange(
        self,
        x:Union[list, pd.Series, np.ndarray],
        y:Union[list, pd.Series, np.ndarray],
        ) -> bool:
        """Get the XY range for the volcano plot based on the x,y values.

            Parameters
            ----------
            x: pd.Series or list
                Values for x.
            y: pd.Series or list
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
                y = [-y.iloc[0], y.iloc[0]]                                     # type: ignore
        else:
            x = [-x, x]                                                         # type: ignore
            y = [-y, y]                                                         # type: ignore
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Get Range
        xR = cStatistic.DataRange(x, margin=mConfig.core.MatPlotMargin)
        yR = cStatistic.DataRange(y, margin=mConfig.core.MatPlotMargin)
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
            xCP,  yCP, color=self.cCV)
        self.wPlot.dPlot['Vol'].rAxes.plot(
            -xCP, yCP, color=self.cCV)
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
            p, -100, 100, color=self.cCV)
        self.wPlot.dPlot['Vol'].rAxes.vlines(
            self.rLog2FC, -100, 100, color=self.cCV)
        self.wPlot.dPlot['Vol'].rAxes.vlines(
            -self.rLog2FC, -100, 100, color=self.cCV)
        #endregion ------------------------------------------------>

        return True
    #---

    def DrawLinesZScore(self) -> bool:
        """Draw no lines. Needed for completion.

            Returns
            -------
            bool
        """
        if self.rVolLinesZ != f'{mConfig.prot.lmFilterZScore} Line':
            self.dKeyMethod[self.rVolLinesZ]()                                  # type: ignore
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
                    color.append(self.cVol[0])
                else:
                    color.append(self.cVol[1])
            elif v > lim:
                if abs((abs(v)*self.rT0)/(abs(v)-lim)) < y.values[k]:
                    color.append(self.cVol[2])
                else:
                    color.append(self.cVol[1])
            else:
                color.append(self.cVol[1])
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
        cond   = [val < -zVal, val > zVal]
        choice = [self.cVol[0], self.cVol[2]]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.rVolLines = ['Z Score Line']
        #endregion ------------------------------------------------>

        return np.select(cond, choice, default=self.cVol[1])           # type: ignore
    #---

    def GetColorPLog2FC(self, *args) -> list:                                   # pylint: disable=unused-argument
        """Get the color by P - Log2FC.

            Returns
            -------
            list
                List of colors
        """
        #region -------------------------------------------------------->
        idx  = pd.IndexSlice
        colP = idx[self.rCondC, self.rRpC,'P']
        valP = self.rDf.loc[:,colP]                                             # type: ignore
        colF = idx[self.rCondC, self.rRpC,'FC']
        valF = self.rDf.loc[:,colF]                                             # type: ignore
        cond = [(valP < self.rP) & (valF < -self.rLog2FC),
                (valP < self.rP) & (valF > self.rLog2FC),]
        choice = [self.cVol[0], self.cVol[2]]
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.rVolLines = ['P - Log2FC Line']
        #endregion ------------------------------------------------>

        return np.select(cond, choice, default=self.cVol[1])           # type: ignore
    #---

    def PickLabel(self, ind:list[int]) -> bool:
        """Show label for the picked protein.

            Parameters
            ----------
            ind: list[int]

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        col = [self.cColGene, self.cColProt]
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

    def PickShow(self, ind:list[int]) -> bool:
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
                f'The numbers of the proteins included in the selected '
                f'point are:\n {str(ind)[1:-1]}')
            cWindow.Notification(
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
        tDate:str              = '',
        cond:str               = '',
        rp:str                 = '',
        corrP:Optional[bool]   = None,
        showAll:Optional[bool] = None,
        t0:Optional[float]     = None,
        s0:Optional[float]     = None
        ) -> bool:
        """Configure window to update Volcano and FC plots when date changes.

            Parameters
            ----------
            tDate: str
                Selected date.
            cond: str
                Selected condition.
            rp: str
                Selected relevant point.
            corrP: bool
                Use corrected P values (True) or not (False).
            showAll: bool
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
        self.rDf         = getattr(self.rData, self.rDateC).df.copy()
        self.rLabelProt  = self.UpdateLabelProt() if tDate else self.rLabelProt
        self.rLabelProtD = {} if tDate else self.rLabelProtD
        #endregion -----------------------------------------> Update variables

        #region --------------------------------------------------> Update GUI
        if self.rAutoFilter:
            self.FilterApply(reset=False)
        #------------------------------> Clean & Reload Protein List
        self.FillListCtrl()
        #------------------------------> Clean text
        self.wText.SetValue('')
        #endregion -----------------------------------------------> Update GUI

        #region -------------------------------------------> Update FC x label
        self.rFcXLabel = [self.rDataC.ctrlName] + self.rDataC.labelB
        #endregion ----------------------------------------> Update FC x label

        #region ---------------------------------------------------> FC minMax
        self.rFcYMax, self.rFcYMin = self.GetFCMinMax()
        #endregion ------------------------------------------------> FC minMax

        #region --------------------------------------------------> Lock Scale
        if self.rLockScale:
            self.LockScale(self.rLockScale)
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

    def UpdateLabelProt(self) -> list:
        """Update the LabelProt list when the date changes.

            Returns
            -------
            list
                Row in the new self.rDf that matches the gene and protein in
                self.rLabelProt
        """
        #region -------------------------------------------------------->
        listO = []
        #------------------------------>
        for r in self.rLabelProt:
            dfR = self.rDf.loc[
                (self.rDf[self.cColGene]==r[1]) & (self.rDf[self.cColProt]==r[2])]
            #------------------------------>
            if not dfR.empty:
                row = dfR.index.tolist()[0]
                listO.append(
                    [str(row),
                     dfR.loc[row,self.cColGene],
                     dfR.loc[row,self.cColProt]
                ])
        #endregion ----------------------------------------------------->

        return listO
    #---

    def LockScale(self, mode:str, updatePlot:bool=True) -> bool:
        """Lock the scale of the volcano and FC plot.

            Parameters
            ----------
            mode: str
                One of No, Date, Project
            updatePlot: bool
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
        #------------------------------>
        return True
    #---

    def ExportImgAll(self) -> bool:
        """Export all plots to a tiff image.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = cWindow.DirSelect(parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p    = Path(dlg.GetPath())
            date = cMethod.StrNow()
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
                    #------------------------------> Do not overwrite
                    if fPath.exists():
                        fPath = fPath.with_stem(f"{fPath.stem} - {date}")
                    #------------------------------> Write
                    v.rFigure.savefig(fPath)
            except Exception as e:
                cWindow.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Images'),
                    tException = e,
                    parent     = self,
                )
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
        dlg = cWindow.ListSelect(
            data,
            self.cLCol,
            self.cSCol,
            tSelOptions = self.rLabelProt,
            title       = 'Select Proteins',
            tBtnLabel   = 'Add Protein',
            color       = mConfig.core.cZebra,
            tStLabel    = [self.cLProtLAvail, self.cLProtLShow],
            allowEmpty  = True,
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
            #------------------------------>
            for y in rowL:
                if y not in self.rLabelProt:
                    self.rLabelProt.append(y)
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
        dlg = VolColorScheme(
            self.rT0,
            self.rS0,
            self.rZ,
            self.rP,
            self.rLog2FC,
            parent    = self,
            checkInit = self.rVolLinesZ,
        )
        #------------------------------>
        if dlg.ShowModal():
            self.rT0, self.rS0, self.rP, self.rLog2FC, self.rZ, self.rVolLinesZ = (
                dlg.GetVal())
            self.VolDraw()
        else:
            return False
        #------------------------------>
        dlg.Destroy()
        return True
    #---

    def FCChange(self, showAll:bool) -> bool:
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
        #region --------------------------------------------------->
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
        #endregion ------------------------------------------------>

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

    def AutoFilter(self, mode:bool) -> bool:
        """Auto apply filter when changing date.

            Parameters
            ----------
            mode: bool
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
        #------------------------------>
        return self.PickShow(ind)
        #endregion ------------------------------------------------> Pick
    #---

    def OnListSelect(self, event:Union[wx.CommandEvent, str]) -> bool:
        """Select an element in the wx.ListCtrl.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

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
    def Filter_FCChange(self, choice:dict={}, updateL:bool=True) -> bool:       # pylint: disable=dangerous-default-value
        """Filter results based on FC evolution.

            Parameters
            ----------
            choice: dict
                Keys are int 0 to 1. Value in 0 is the filter to apply and
                in 1 the conditions to consider.
            updateL: bool
                Update (True) or not (False) the GUI. Default is True.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Get Value
        if choice:
            choice0, choice1 = choice.values()
        else:
            dlg = cWindow.MultipleCheckBox(
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
            # pylint: disable=invalid-unary-operand-type
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
                [mConfig.prot.kwFilterFCEvol,
                 {'choice':choice, 'updateL': False},
                 f'{choice0} ({choice1[0:3]})']
            )
        else:
            pass
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def Filter_HCurve(self, updateL:bool=True, **kwargs) -> bool:              # pylint: disable=unused-argument
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
        filterText = mConfig.prot.kwFilterHypCurve
        lim        = self.rT0 * self.rS0
        fc         = self.rDf.loc[:,[(self.rCondC,self.rRpC,'FC')]]
        p          = -np.log10(self.rDf.loc[:,[(self.rCondC,self.rRpC,'P')]])
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> H Curve
        cond   = [fc < -lim, fc > lim]
        choice = [
            protMethod.HCurve(fc, self.rT0, self.rS0),
            protMethod.HCurve(fc, self.rT0, self.rS0),
        ]
        pH = np.select(cond, choice, np.nan)
        #endregion ------------------------------------------------> H Curve

        #region ---------------------------------------------------> Filter
        cond     = [pH < p, pH > p]
        choice   = [True, False]
        npBool   = np.select(cond, choice)
        npBool   = npBool.astype(bool)
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
        #endregion -----------------------------------------------> Update GUI

        return True
    #---

    def Filter_Log2FC(self, gText:str='', updateL:bool=True) -> bool:
        """Filter results by log2FC.

            Parameters
            ----------
            gText: str
                FC threshold and operand, e.g. < 10 or > 3.4.
            updateL: bool
                Update filterList and StatusBar (True) or not (False).

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            #------------------------------>
            dlg = cWindow.UserInputText(
                'Filter results by Log2(FC) value.',
                ['Threshold'],
                ['log2(FC) value. e.g. < 2.3 or > -3.5'],
                [cValidator.Comparison(numType='float', op=['<', '>'])],
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
                [mConfig.prot.kwFilterFCLog,
                 {'gText': uText, 'updateL': False},
                 f'{self.cLFLog2FC} {op} {val}']
            )
        #endregion ---------------------------------------> Update Filter List

        return True
    #---

    def Filter_PValue(
        self,
        gText:str           = '',
        absB:Optional[bool] = None,
        updateL:bool        = True,
        ) -> bool:
        """Filter results by P value.

            Parameters
            ----------
            gText: str
                P value threshold and operand, e.g. < 10 or > 3.4
            absB: bool
                Use absolute values (True) or -log10 values (False)
            updateL: bool
                Update filterList and StatusBar (True) or not (False)

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            dlg = FilterPValue(
                'Filter results by P value.',
                'Threshold',
                'Absolute or -log10(P) value. e.g. < 0.01 or > 1',
                self.wPlot.dPlot['Vol'],
                cValidator.Comparison(numType='float', op=['<', '>'], vMin=0),
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
        if not absB:
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
                [mConfig.prot.kwFilterPVal,
                 {'gText': uText, 'absB': absB, 'updateL': False},
                 f'{label} {op} {val}']
            )
        #endregion ---------------------------> Update Filter List & StatusBar

        return True
    #---

    def Filter_ZScore(self, gText:str='', updateL:bool=True) -> bool:
        """Filter results by Z score.

            Parameters
            ----------
            gText: str
                Z score threshold and operand, e.g. < 10 or > 3.4.
            updateL: bool
                Update filterList and StatusBar (True) or not (False).

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText:
            uText = gText
        else:
            dlg = cWindow.UserInputText(
                'Filter results by Z score.',
                ['Threshold (%)'],
                ['Decimal value between 0 and 100. e.g. < 10.0 or > 20.4'],
                [cValidator.Comparison(
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
                [mConfig.prot.kwFilterZScore,
                 {'gText': uText, 'updateL': False},
                 f'{self.cLFZscore} {op} {val}']
            )
        #endregion ---------------------------------------> Update Filter List

        return True
    #---

    def FilterApply(self, reset:bool=True) -> bool:
        """Apply all filter to the current date.

            Parameters
            ----------
            reset: bool
                Reset self.rDf. Default is True.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Reset df
        if reset:
            self.rDf = getattr(self.rData, self.rDateC).df.copy()
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
        self.rDf         = getattr(self.rData, self.rDateC).df.copy()
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
        #endregion --------------------------------> Check Something to Delete

        #region ------------------------------------------------------> Dialog
        dlg = FilterRemoveAny(self.rFilterList, self)
        if dlg.ShowModal():
            lo = dlg.GetChecked()
            #------------------------------>
            dlg.Destroy()
            #------------------------------>
            if not lo:
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
        mConfig.prot.lFilter = [x for x in self.rFilterList]                    # type: ignore
        return True
    #---

    def FilterPaste(self) -> bool:
        """Paste the copied filters.

            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Copy
        self.rFilterList = [x for x in mConfig.prot.lFilter]                    # type: ignore
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
        self.rObj.rData[mConfig.prot.nMod][self.rDateC]['F'] = filterDict
        #------------------------------>
        if self.rObj.Save():
            getattr(self.rData, self.rDateC).filterS = filterDict
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
            [k]+v for k,v in getattr(self.rData, self.rDateC).filterS.items()]
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


class VolColorScheme(cWindow.BaseDialogOkCancel):
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
    #region -----------------------------------------------------> Class Setup
    cNLineNone = f'{mConfig.prot.lmFilterZScore} Line'
    cNLineHyp  = f'{mConfig.prot.lmFilterHypCurve} Line'
    cNLinePLog = f'{mConfig.prot.lmColorSchemePLog2} Line'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        t0:float,
        s0:float,
        z:float,
        p:float,
        fc:float,
        parent:Optional[wx.Window]=None,
        checkInit:LIT_Z_LINES = f'{mConfig.prot.lmFilterZScore} Line',
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
        self.rCheck = checkInit
        #------------------------------>
        super().__init__(title='Color Scheme Parameters', parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wsbHC = wx.StaticBox(self, label='Hyperbolic Curve')
        self.wT0 = cWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = 't0',
            tcHint    = 'e.g. 1.0',
            tcSize    = (100,22),
            validator = cValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wT0.wTc.SetValue(self.rValInit['T0'])

        self.wS0 = cWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = 's0',
            tcHint    = 'e.g. 0.1',
            tcSize    = (100,22),
            validator = cValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wS0.wTc.SetValue(self.rValInit['S0'])

        self.wsbPFC = wx.StaticBox(self, label='P - Log2[FC]')
        self.wP = cWidget.StaticTextCtrl(
            self.wsbPFC,
            stLabel   = 'P',
            tcHint    = 'e.g. 0.05',
            tcSize    = (100,22),
            validator = cValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wP.wTc.SetValue(self.rValInit['P'])

        self.wFC = cWidget.StaticTextCtrl(
            self.wsbPFC,
            stLabel   = 'log2FC',
            tcHint    = 'e.g. 0.1',
            tcSize    = (100,22),
            validator = cValidator.NumberList('float', vMin=0, nN=1)
        )
        self.wFC.wTc.SetValue(self.rValInit['FC'])

        self.wsbZ = wx.StaticBox(self, label='Z Score')
        self.wZ = cWidget.StaticTextCtrl(
            self.wsbZ,
            stLabel   = 'Z Score',
            tcHint    = 'e.g. 10.0',
            tcSize    = (100,22),
            validator = cValidator.NumberList(
                    numType='float', vMin=0, vMax=100, nN=1),
        )
        self.wZ.wTc.SetValue(self.rValInit['Z'])
        self.wStShow = wx.StaticText(self.wsbZ, label='Show')
        self.wCbNone = wx.RadioButton(
            self.wsbZ, label='None', name=self.cNLineNone)
        self.wCbHyp  = wx.RadioButton(
            self.wsbZ, label='Hyperbolic Curve', name=self.cNLineHyp)
        self.wCbPLog = wx.RadioButton(
            self.wsbZ, label='P - Log2[FC] Lines', name=self.cNLinePLog)
        self.FindWindowByName(self.rCheck, self).SetValue(True)
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

        self.sFlexZ = wx.FlexGridSizer(4,2,1,1)
        self.sFlexZ.Add(self.wZ.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.Add(self.wZ.wTc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.Add(self.wStShow, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.Add(self.wCbNone, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.AddStretchSpacer()
        self.sFlexZ.Add(self.wCbHyp, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sFlexZ.AddStretchSpacer()
        self.sFlexZ.Add(self.wCbPLog, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
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

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_RADIOBUTTON, self.OnCheckChange)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnCheckChange(self, event:wx.CommandEvent) -> bool:
        """Update

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        self.rCheck = event.GetEventObject().GetName()
        return True
    #---

    def OnOK(self, event:wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event: wx.Event
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
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class methods
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
            self.rCheck,
        )
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FilterPValue(cWindow.UserInputText):
    """Dialog to filter values by P value.

        Parameters
        ----------
        cTitle: str
            Title of the wx.Dialog
        cLabel: str
            Label for the wx.StaticText
        cHint: str
            Hint for the wx.TextCtrl.
        cParent: wx.Window
            Parent of the wx.Dialog
        cValidator: wx.Validator
            Validator for the wx.TextCtrl
        cSize: wx.Size
            Size of the wx.Dialog. Default is (420, 170)
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title:str,
        label:str,
        hint:str,
        parent:Union[wx.Window, None]=None,
        validator:wx.Validator=wx.DefaultValidator,
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
    def OnTextChange(self, event:wx.Event) -> bool:                             # pylint: disable=unused-argument
        """Select -log10P if the given value is > 1.

            Parameters
            ----------
            event: wx.Event
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
        #endregion ----------------------------------------------------> Check

        return True
    #---

    def OnCheck(self, event:wx.CommandEvent) -> bool:
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
            [k.SetValue(False) for k in self.rCheck]                            # pylint: disable=expression-not-assigned
            #------------------------------>
            tCheck.SetValue(True)
        #endregion -------------------------------------------------> Deselect

        return True
    #---

    def OnOK(self, event:wx.CommandEvent) -> bool:
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


class FilterRemoveAny(cWindow.BaseDialogOkCancel):
    """Dialog to select Filters to remove in ProtProfPlot.

        Parameters
        ----------
        filterList: list
            List of already applied filter, e.g.:
            [['Text', {kwargs} ], ...]
        parent: wx.Window
            Parent of the window.

        Attributes
        ----------
        rCheckB: list[wx.CheckBox]
            List of wx.CheckBox to show in the window
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.prot.ndFilterRemoveAny
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
        filterList:list,
        parent:Optional[wx.Window] = None,
        ) -> None:
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
            if cb.IsChecked():
                lo.append(k)
        #endregion ----------------------------------------------> Get Checked

        return lo
    #---
    #endregion -----------------------------------------------> Manage methods
#---
#endregion ----------------------------------------------------------> Classes

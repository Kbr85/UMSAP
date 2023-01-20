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


"""Windows for the corr module of the app"""


#region -------------------------------------------------------------> Imports
from typing import Optional, TYPE_CHECKING

import matplotlib as mpl

from config.config import config as mConfig
from core import method as cMethod
from core import window as cWindow
from corr import method as corrMethod
from main import menu   as mMenu

if TYPE_CHECKING:
    from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ResCorrA(cWindow.BaseWindowResultOnePlot):
    """Creates the window showing the results of a correlation analysis.

        Parameters
        ----------
        parent: 'UMSAPControl'
            Parent of the window.

        Attributes
        ----------
        rBar: Boolean
            Show (True) or not (False) the color bar in the plot
        rCmap: Matplotlib cmap
            CMAP to use in the plot
        rCol: Boolean
            Plot column names (True) or numbers (False)
        rData: cMethod.BaseAnalysis
            For each CorrA a new attribute 'Date-ID' is added with value
            corrMethod.CorrAnalysis.
        rDataPlot: pd.DF
            Data to plot and search the values for the wx.StatusBar.
        rDate: [parent.obj.confData[Section].keys()]
            List of dates available for plotting.
        rDateC: one of rDate
            Current selected date
        rNorm: mpl.colors.Normalize
        rObj: parent.obj
            Pointer to the UMSAPFile object in parent.
        rSelColIdx: list[int]
            Selected columns index in self.rData[self.rDateC]['DF'].
        rSelColName: list[int]
            Selected columns name to plot.
        rSelColNum: list[int]
            Selected columns numbers to plot.

        Notes
        -----
        The structure of menuData is:
        {
            'MenuDate' : [list of dates in the section],
        }
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.corr.nwRes
    cSection = mConfig.corr.nUtil
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:'resWindow.UMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj  = parent.rObj
        self.rData:cMethod.BaseAnalysis = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        #------------------------------> Nothing found
        self.ReportPlotDataError()
        #------------------------------>
        self.rDateC = self.rDate[0]
        self.rDataC:corrMethod.CorrAnalysis = getattr(self.rData, self.rDateC)
        self.rBar   = False
        self.rCol   = True
        self.rNorm  = mpl.colors.Normalize(vmin=-1, vmax=1)
        self.rCmap  = cMethod.MatplotLibCmap(
            N   = mConfig.corr.CMAP['N'],
            c1  = mConfig.corr.CMAP['c1'],
            c2  = mConfig.corr.CMAP['c2'],
            c3  = mConfig.corr.CMAP['c3'],
            bad = mConfig.corr.CMAP['NA'],
        )
        self.rSelColNum  = []
        self.rSelColIdx  = []
        self.rSelColName = []
        #------------------------------>
        self.cParent = parent
        self.cTitle  = f"{parent.cTitle} - {self.cSection} - {self.rDateC}"
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.corr.kwCol: self.SelectColumn,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------->
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion ------------------------------------------------>

        #region ----------------------------------------------------> Position
        self.SetColDetails(self.rDateC)
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion -------------------------------------------------> Position
    #---
    #endregion -----------------------------------------------> Instance setup

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
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            try:
                #------------------------------> Set x,y,z
                x, y = event.xdata, event.ydata
                #------------------------------>
                xf = int(x)
                yf = int(y)
                zf = f'{self.rDataPlot.iat[yf,xf]:.2f}'
                #------------------------------>
                if self.rCol:
                    xs = self.rSelColName[xf]
                    ys = self.rSelColName[yf]
                else:
                    xs = self.rSelColNum[xf]
                    ys = self.rSelColNum[yf]
                #------------------------------> Print
                self.wStatBar.SetStatusText(
                    f"x = '{str(xs)}'   y = '{str(ys)}'   cc = {str(zf)}"
                )
            except Exception:
                self.wStatBar.SetStatusText('')
        else:
            self.wStatBar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Manage Methods
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Super
        info = super().WinPos()
        #endregion -----------------------------------------------------> Super

        #region ------------------------------------------------> Set Position
        self.SetPosition(pt=(
            info['D']['w'] - (info['W']['N']*self.cSDeltaWin + info['W']['w']),
            info['D']['yo'] + info['W']['N']*self.cSDeltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def SetColDetails(self, tDate:str) -> bool:
        """"Set the values of self.rSelColX to its default values, all values
            in the analysis.

            Parameters
            ----------
            tDate: str
                A date in the section e.g. '20210129-094504 - bla'

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        data = getattr(self.rData, tDate)
        self.rSelColName = data.df.columns.values
        self.rSelColNum  = data.numColList
        self.rSelColIdx  = [x for x,_ in enumerate(self.rSelColNum)]
        #endregion ----------------------------------------------------->

        return True
    #---

    def UpdateResultWindow(
        self,
        tDate:str          = '',
        col:Optional[bool] = None,
        bar:Optional[bool] = None,
        ) -> bool:
        """Plot data from a given date.

            Parameters
            -----------
            tDate: str
                A date in the section e.g. '20210129-094504 - bla'
            col: bool
                Show column name (True) or numbers (False)
            bar: bool
                Show or not the color bar.

            Returns
            -------
            bool
        """
        #region -------------------------------------------> Update parameters
        tDate = tDate if tDate else self.rDateC
        if tDate != self.rDateC:
            self.SetColDetails(tDate)
        #------------------------------>
        self.rDateC = tDate
        self.rDataC = getattr(self.rData, self.rDateC)
        self.rCol   = col if col is not None else self.rCol
        self.rBar   = bar if bar is not None else self.rBar
        #endregion ----------------------------------------> Update parameters

        #region --------------------------------------------------------> Axis
        self.SetAxis()
        #endregion -----------------------------------------------------> Axis

        #region --------------------------------------------------------> Plot
        self.rDataPlot = self.rDataC.df.iloc[self.rSelColIdx,self.rSelColIdx]
        #------------------------------>
        self.wPlot[0].rAxes.pcolormesh(
            self.rDataPlot,
            cmap        = self.rCmap,
            vmin        = -1,
            vmax        = 1,
            antialiased = True,
            edgecolors  = 'k',
            lw          = 0.005,
        )
        #------------------------------>
        if self.rBar:
            self.wPlot[0].rFigure.colorbar(
                mpl.cm.ScalarMappable(norm=self.rNorm, cmap=self.rCmap),        # type: ignore
                orientation = 'vertical',
                ax          = self.wPlot[0].rAxes,
            )
        #endregion -----------------------------------------------------> Plot

        #region -------------------------------------------------> Zoom & Draw
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rCanvas.draw()
        #endregion ----------------------------------------------> Zoom & Draw

        #region --------------------------------------------------->
        self.PlotTitle()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxis(self) -> bool:
        """General details of the plot area.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot[0].rFigure.clear()
        self.wPlot[0].rAxes = self.wPlot[0].rFigure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear

        #region ---------------------------------------------------> Variables
        xLabel    = []
        xTicksLoc = []

        if (tLen := len(self.rSelColIdx)) <= 30:
            step = 1
        elif tLen > 30 and tLen <= 60:
            step = 2
        else:
            step = 3
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Grid
        self.wPlot[0].rAxes.grid(True)
        #endregion -----------------------------------------------------> Grid

        #region --------------------------------------------------> Axis range
        self.wPlot[0].rAxes.set_xlim(0, tLen)
        self.wPlot[0].rAxes.set_ylim(0, tLen)
        #endregion -----------------------------------------------> Axis range

        #region ---------------------------------------------------> Set ticks
        if self.rCol:
            theLabel = self.rSelColName
        else:
            theLabel = self.rSelColNum
        for i in range(0, tLen, step):
            xTicksLoc.append(i + 0.5)
            xLabel.append(theLabel[i])
        #------------------------------>
        self.wPlot[0].rAxes.set_xticks(xTicksLoc)
        self.wPlot[0].rAxes.set_xticklabels(xLabel, rotation=90)
        #------------------------------>
        self.wPlot[0].rAxes.set_yticks(xTicksLoc)
        self.wPlot[0].rAxes.set_yticklabels(xLabel)
        #endregion ------------------------------------------------> Set ticks

        #region -----------------------------------------------> Adjust figure
        self.wPlot[0].rFigure.subplots_adjust(bottom=0.13)
        #endregion --------------------------------------------> Adjust figure

        return True
    #---

    def SelectColumn(self, showAllCol:str) -> bool:
        """Plot only selected columns.

            Parameters
            ----------
            showAllCol: str
                Show all columns or select columns to show.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> All
        if showAllCol == mConfig.corr.lmAllCol:
            self.SetColDetails(self.rDateC)
            self.UpdateResultWindow()
            return True
        #endregion ------------------------------------------------> All

        #region -----------------------------------------------------> Options
        allCol = []
        #------------------------------>
        for k,c in enumerate(self.rDataC.df.columns):
            allCol.append([str(self.rDataC.numColList[k]), c])
        #------------------------------>
        selCol = []
        for c in self.rSelColIdx:
            selCol.append([str(self.rDataC.numColList[c]), self.rDataC.df.columns[c]])
        #endregion --------------------------------------------------> Options

        #region -------------------------------------------------> Get New Sel
        #------------------------------> Create the window
        dlg = cWindow.ListSelect(
            allCol,
            mConfig.core.lLCtrlColNameI,
            mConfig.core.sLCtrlColI,
            tSelOptions = selCol,
            title       = 'Select the columns to show in the correlation plot',
            tBtnLabel   = 'Add selection',
            tStLabel = ['Columns in the current results', 'Selected columns'],
        )
        #------------------------------> Get the selected values
        if dlg.ShowModal():
            self.rSelColNum  = dlg.wLCtrlO.GetColContent(0)
            self.rSelColIdx  = []
            self.rSelColName = []
            #------------------------------>
            for k in self.rSelColNum:
                tIDX = self.rDataC.numColList.index(int(k))
                self.rSelColIdx.append(tIDX)
                #------------------------------>
                self.rSelColName.append(self.rDataC.df.columns[tIDX])
            #------------------------------>
            self.UpdateResultWindow()
        #endregion ----------------------------------------------> Get New Sel

        dlg.Destroy()
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---
#endregion ----------------------------------------------------------> Classes

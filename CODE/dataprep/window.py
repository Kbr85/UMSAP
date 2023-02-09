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


"""Windows for the dataprep module of the app"""


#region -------------------------------------------------------------> Imports
import shutil
from pathlib import Path
from typing  import Union, Optional, TYPE_CHECKING

import pandas as pd
import numpy as np
from pubsub import pub
from scipy  import stats

import wx

from config.config import config as mConfig
from core     import method    as cMethod
from core     import statistic as cStatistic
from core     import window    as cWindow
from main     import menu      as mMenu
from dataprep import method    as dataMethod

if TYPE_CHECKING:
    from result import file   as resFile
    from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def CreateResDataPrep(
    parent:'resWindow.UMSAPControl',
    title:str    = '',
    tSection:str = '',
    tDate:str    = '',
    ) -> bool:
    """Launch ResDataPrep from PubSub message.

        Parameters
        ----------
        parent: resWindow.UMSAPControl
            Parent of the window.
        title: str or None
            Title of the window. Default is None.
        tDate: str
            Selected Date.
        tSection: str
            Section of the Analysis.

        Return
        ------
        bool
    """
    #region --------------------------------------------------->
    try:
        ResDataPrep(parent, title=title, tSection=tSection, tDate=tDate)
    except Exception as e:
        msg = 'Failed to create the Data Preparation Result window.'
        cWindow.Notification('errorU', msg=msg, tException=e, parent=parent)
        return False
    #endregion ------------------------------------------------>

    return True
#---
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
class ResDataPrep(cWindow.BaseWindowResultListTextNPlot):
    """Window to check the data preparation steps.

        Parameters
        ----------
        parent: resWindow.UMSAPControl
            Parent of the window.
        title: str or None
            Title of the window. Default is None.
        tDate: str
            Selected Date.
        tSection: str
            Section of the Analysis.

        Attributes
        ----------
        rData: cMethod.BaseAnalysis
            For each DataPrep a new attribute 'Date-ID' is added with value
            dataMethod.DataPrepAnalysis.
        rDataC: dataMethod.DataPrepAnalysis
            Data for currently selected date - ID.
        rDataPlot: dict[str: pd.DataFrame]
            DataFrames with the data.
        rDate: list of str
            List of available dates in the section.
        rDateC: str
            Date selected. Needed to export the data and images.
        rFromUMSAPFile: bool
            The window is invoked from an UMSAP File window (True) or not (False)
        rObj: UMSAPFile
            Reference to the UMSAPFile object.

        Notes
        -----
        Requires a 'NumColList' key in self.rData.tDate with a list
        of all columns involved in the analysis with the column numbers in the
        original data file.
        """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.data.nwRes
    cSection = mConfig.data.nUtil
    #------------------------------>
    cLCol    = mConfig.core.lLCtrlColNameI
    cHSearch = 'Column Names'
    cTList   = 'Column Names'
    cTText   = 'Statistic Information'
    #------------------------------>
    cLNPlot   = ['Init', 'Transf', 'Norm', 'Imp']
    cNPlotCol = 2
    #------------------------------>
    cSWindow = (900,800)
    #------------------------------>
    cLCStyle = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL
    #------------------------------> Label
    cLDFData = ['Floated', 'Transformed', 'Normalized', 'Imputed']
    cLdfCol  = [
        'Data', 'N', 'NaN', 'Mean', 'Median', 'SD', 'Kurtosis', 'Skewness']
    #------------------------------> Other
    cFileName = {
        mConfig.core.ltDPKeys[0] : '{}-01-Floated-{}.{}',
        mConfig.core.ltDPKeys[1] : '{}-02-Transformed-{}.{}',
        mConfig.core.ltDPKeys[2] : '{}-03-Normalized-{}.{}',
        mConfig.core.ltDPKeys[3] : '{}-04-Imputed-{}.{}',
    }
    cImgName = {
        cLNPlot[0] : '{}-01-Floated-{}.{}',
        cLNPlot[1] : '{}-02-Transformed-{}.{}',
        cLNPlot[2] : '{}-03-Normalized-{}.{}',
        cLNPlot[3] : '{}-04-Imputed-{}.{}',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:'resWindow.UMSAPControl',
        title:str    = '',
        tSection:str = '',
        tDate:str    = '',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj:'resFile.UMSAPFile' = parent.rObj
        self.cTitle   = title
        self.tSection = tSection if tSection else self.cSection
        self.tDate    = tDate
        self.SetWindow(parent, tSection, tDate)
        #------------------------------>
        try:
            self.ReportPlotDataError()
        except ValueError as e:
            raise ValueError from e
        #------------------------------>
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wPlot.dPlot['Transf'].rAxes2 = self.wPlot.dPlot['Transf'].rAxes.twinx()
        self.wPlot.dPlot['Norm'].rAxes2   = self.wPlot.dPlot['Norm'].rAxes.twinx()
        self.wPlot.dPlot['Imp'].rAxes2    = self.wPlot.dPlot['Imp'].rAxes.twinx()
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(
            self.cName, menuData={'MenuDate': self.rDate})
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ---------------------------------------------> Window position
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event:wx.CloseEvent) -> bool:
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
        if self.rFromUMSAPFile:
            self.cParent.UnCheckSection(self.cSection, self)                    # type: ignore
        #endregion --------------------------------------------> Update parent

        #region ------------------------------------> Reduce number of windows
        mConfig.core.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---

    def OnListSelect(self, event:Union[wx.CommandEvent, str]) -> bool:
        """Plot data for the selected column.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------>
        super().OnListSelect(event)
        #endregion --------------------------------------------->

        #region ------------------------------------------------> Get Selected
        #------------------------------> If nothing is selected clear the plot
        if self.rLCIdx < 0:
            self.ClearPlots()
            return True
        #endregion ---------------------------------------------> Get Selected

        #region ---------------------------------------------------------> dfF
        try:
            self.PlotdfF(self.rLCIdx)
        except Exception as e:
            #------------------------------>
            msg = ('It was not possible to build the histograms for the '
                   'selected column.')
            cWindow.Notification('errorU', msg=msg, tException=e, parent=self)
            #------------------------------>
            self.ClearPlots()
            #------------------------------>
            return False
        #endregion ------------------------------------------------------> dfF

        #region ---------------------------------------------------------> dfT
        self.PlotdfT(self.rLCIdx)
        #endregion ------------------------------------------------------> dfT

        #region ---------------------------------------------------------> dfN
        self.PlotdfN(self.rLCIdx)
        #endregion ------------------------------------------------------> dfN

        #region --------------------------------------------------------> dfIm
        self.PlotdfIm(self.rLCIdx)
        #endregion -----------------------------------------------------> dfIm

        #region --------------------------------------------------------> Text
        self.SetText(self.rLCIdx)
        #endregion -----------------------------------------------------> Text

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Manage Methods
    def SetWindow(
        self,
        parent:wx.Window,
        tSection:str = '',
        tDate:str    = '',
        ) -> bool:
        """Configure the window.

            Parameters
            ----------
            parent: wx.Window
                Parent of the window.
            tSection: str
                Name of the section.
            tDate: str
                Selected Date.

            Returns
            -------
            bool

            Notes
            -----
            If self.cTitle is None the window is invoked from the main Data
            Preparation section of a UMSAP File window
        """
        #region -----------------------------------------------> Set Variables
        if self.cTitle:
            self.rFromUMSAPFile = False
            self.rData  = self.rObj.dConfigure[self.cSection](tSection, tDate)
            self.rDate  = []
            self.rDateC = parent.rDateC                                         # type:ignore
        else:
            self.rFromUMSAPFile = True
            self.rData  = self.rObj.dConfigure[self.cSection]()
            self.rDate  = self.rData.date
            self.rDateC = self.rDate[0]
            self.cTitle = (
                f"{parent.cTitle} - {self.cSection} - {self.rDateC}")           # type: ignore
        #------------------------------>
        self.rDataC:dataMethod.DataAnalysis = getattr(self.rData, self.rDateC)
        #endregion --------------------------------------------> Set Variables

        return True
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
        x = info['D']['xo'] + info['W']['N']*mConfig.core.deltaWin
        y = (
            ((info['D']['h']/2) - (info['W']['h']/2))
            + info['W']['N']*mConfig.core.deltaWin
        )
        self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def DupWin(self) -> bool:
        """Duplicate window.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.rFromUMSAPFile:
            super().DupWin()
        else:
            ResDataPrep(
                self.cParent,                                                   # type: ignore
                title    = self.cTitle,
                tSection = self.tSection,
                tDate    = self.tDate,
            )
        #endregion ------------------------------------------------>

        return True
    #---

    def FillListCtrl(self) -> bool:
        """Update the column names for the given analysis.

            Returns
            -------
            bool

            Notes
            -----
            Entries are read from self.ddDF['dfF']
        """
        #region --------------------------------------------------> Delete old
        self.wLC.wLCS.wLC.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old

        #region ----------------------------------------------------> Get Data
        data = []
        for k,n in enumerate(self.rDataPlot['dfF'].columns.values.tolist()):
            colN = str(self.rDataC.numColList[k])
            data.append([colN, n])
        #endregion -------------------------------------------------> Get Data

        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.wLC.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl

        #region ----------------------------------------> Update Column Number
        self._mgr.GetPane(self.wLC).Caption(f'{self.cTList} ({len(data)})')
        self._mgr.Update()
        #endregion -------------------------------------> Update Column Number

        return True
    #---

    def PlotdfF(self, col:int) -> bool:
        """Plot the histograms for dfF.

            Parameters
            ----------
            col: int
                Column to plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x = self.rDataPlot['dfF'].iloc[:,col]
        x = x[np.isfinite(x)]
        #------------------------------>
        nBin = cStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Plot
        #------------------------------>
        self.wPlot.dPlot['Init'].rAxes.clear()
        #------------------------------> title
        self.wPlot.dPlot['Init'].rAxes.set_title("Floated")
        #------------------------------>
        a = self.wPlot.dPlot['Init'].rAxes.hist(x, bins=nBin, density=False)
        #------------------------------>
        self.wPlot.dPlot['Init'].rAxes.set_xlim(*cStatistic.DataRange(
            a[1], margin=mConfig.core.MatPlotMargin))
        self.wPlot.dPlot['Init'].ZoomResetSetValues()
        #------------------------------>
        self.wPlot.dPlot['Init'].rCanvas.draw()
        #endregion -----------------------------------------------------> Plot

        return True
    #---

    def PlotdfT(self, col:int) -> bool:
        """Plot the histograms for dfT.

            Parameters
            ----------
            col: int
                Column to plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x = self.rDataPlot['dfT'].iloc[:,col]
        x = x[np.isfinite(x)]
        #------------------------------>
        nBin = cStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Draw
        self.wPlot.dPlot['Transf'].rAxes.clear()
        #------------------------------> title
        self.wPlot.dPlot['Transf'].rAxes.set_title("Transformed")
        #------------------------------>
        a = self.wPlot.dPlot['Transf'].rAxes.hist(x, bins=nBin, density=False)
        #------------------------------>
        xRange = cStatistic.DataRange(
            a[1], margin=mConfig.core.MatPlotMargin)
        self.wPlot.dPlot['Transf'].rAxes.set_xlim(*xRange)
        self.wPlot.dPlot['Transf'].rAxes.set_ylim(*cStatistic.DataRange(
            a[0], margin=mConfig.core.MatPlotMargin))
        self.wPlot.dPlot['Transf'].ZoomResetSetValues()
        #------------------------------>
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlot.dPlot['Transf'].rAxes2.clear()
        self.wPlot.dPlot['Transf'].rAxes2.plot(
            gausX, gausY.pdf(gausX), color='C1')
        self.wPlot.dPlot['Transf'].rAxes2.set_yticks([])
        self.wPlot.dPlot['Transf'].rAxes2.set_yticklabels([])
        #------------------------------>
        self.wPlot.dPlot['Transf'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        return True
    #---

    def PlotdfN(self, col:int) -> bool:
        """Plot the histograms for dfN.

            Parameters
            ----------
            col: int
                Column to plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x = self.rDataPlot['dfN'].iloc[:,col]
        x = x[np.isfinite(x)]
        #------------------------------>
        nBin = cStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Draw
        self.wPlot.dPlot['Norm'].rAxes.clear()
        #------------------------------> title
        self.wPlot.dPlot['Norm'].rAxes.set_title("Normalized")
        #------------------------------>
        a = self.wPlot.dPlot['Norm'].rAxes.hist(x, bins=nBin, density=False)
        #------------------------------>
        xRange = cStatistic.DataRange(
            a[1], margin=mConfig.core.MatPlotMargin)
        self.wPlot.dPlot['Norm'].rAxes.set_xlim(*xRange)
        self.wPlot.dPlot['Norm'].rAxes.set_ylim(*cStatistic.DataRange(
            a[0], margin=mConfig.core.MatPlotMargin))
        self.wPlot.dPlot['Norm'].ZoomResetSetValues()
        #------------------------------>
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlot.dPlot['Norm'].rAxes2.clear()
        self.wPlot.dPlot['Norm'].rAxes2.plot(
            gausX, gausY.pdf(gausX), color='C1')
        self.wPlot.dPlot['Norm'].rAxes2.set_yticks([])
        self.wPlot.dPlot['Norm'].rAxes2.set_yticklabels([])
        #------------------------------>
        self.wPlot.dPlot['Norm'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        return True
    #---

    def PlotdfIm(self, col:int) -> bool:
        """Plot the histograms for dfIm.

            Parameters
            ----------
            col : int
                Column to plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x = self.rDataPlot['dfIm'].iloc[:,col]
        x = x[np.isfinite(x)]
        #------------------------------>
        nBin = cStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Draw
        self.wPlot.dPlot['Imp'].rAxes.clear()
        #------------------------------> title
        self.wPlot.dPlot['Imp'].rAxes.set_title("Imputed")
        #------------------------------>
        a = self.wPlot.dPlot['Imp'].rAxes.hist(x, bins=nBin, density=False)
        #------------------------------>
        xRange = cStatistic.DataRange(
            a[1], margin=mConfig.core.MatPlotMargin)
        self.wPlot.dPlot['Imp'].rAxes.set_xlim(*xRange)
        self.wPlot.dPlot['Imp'].rAxes.set_ylim(*cStatistic.DataRange(
            a[0], margin=mConfig.core.MatPlotMargin))
        self.wPlot.dPlot['Imp'].ZoomResetSetValues()
        #------------------------------>
        idx = np.where(self.rDataPlot['dfF'].iloc[:,col].isna())[0]
        if len(idx) > 0:
            y = self.rDataPlot['dfIm'].iloc[idx,col]
            if y.count() > 0:
                self.wPlot.dPlot['Imp'].rAxes.hist(
                    y, bins=nBin, density=False, color='C2')
        #------------------------------>
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlot.dPlot['Imp'].rAxes2.clear()
        self.wPlot.dPlot['Imp'].rAxes2.plot(gausX, gausY.pdf(gausX), color='C1')
        self.wPlot.dPlot['Imp'].rAxes2.set_yticks([])
        self.wPlot.dPlot['Imp'].rAxes2.set_yticklabels([])
        self.wPlot.dPlot['Imp'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        return True
    #---

    def SetText(self, col:int) -> bool:
        """Set the text with the descriptive statistics about the data
            preparation steps.

            Parameters
            ----------
            col: int
                Column to plot.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(columns=self.cLdfCol)
        df['Data'] = self.cLDFData
        #endregion -------------------------------------------------> Empty DF

        #region --------------------------------------------> Calculate values
        for r,k in enumerate(self.rDataPlot):
            #------------------------------> N
            df.iat[r,1] = self.rDataPlot[k].shape[0]
            #------------------------------> NA
            df.iat[r,2] = self.rDataPlot[k].iloc[:,col].isnull().sum()
            #------------------------------> Mean
            df.iat[r,3] = self.rDataPlot[k].iloc[:,col].mean()
            #------------------------------> Median
            df.iat[r,4] = self.rDataPlot[k].iloc[:,col].median()
            # #------------------------------> SD
            df.iat[r,5] = self.rDataPlot[k].iloc[:,col].std()
            # #------------------------------> Kurtosis
            df.iat[r,6] = self.rDataPlot[k].iloc[:,col].kurt()
            # #------------------------------> Skewness
            df.iat[r,7] = self.rDataPlot[k].iloc[:,col].skew()
        #endregion -----------------------------------------> Calculate values

        #region ---------------------------------------------> Remove Old Text
        self.wText.Clear()
        #endregion ------------------------------------------> Remove Old Text

        #region ------------------------------------------------> Add New Text
        self.wText.AppendText(df.to_string(index=False))
        self.wText.SetInsertionPoint(0)
        #endregion ---------------------------------------------> Add New Text

        return True
    #---

    def UpdateResultWindow(self, tDate:str='') -> bool:
        """Update window when a new date is selected.

            Parameters
            ----------
            date: str
                Given date to plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        if tDate:
            self.rDateC = tDate
            self.rDataC = getattr(self.rData, self.rDateC)
        #------------------------------>
        self.rDataPlot = self.rDataC.dp
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl

        #region --------------------------------------------------------> Plot
        self.ClearPlots()
        #endregion -----------------------------------------------------> Plot

        #region --------------------------------------------------------> Text
        self.wText.Clear()
        #endregion -----------------------------------------------------> Text

        #region -------------------------------------------------------> Title
        if self.rFromUMSAPFile:
            self.PlotTitle()
        #endregion ----------------------------------------------------> Title

        return True
    #---

    def ClearPlots(self) -> bool:
        """Clear the plots.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot.dPlot[self.cLNPlot[0]].rAxes.clear()
        self.wPlot.dPlot[self.cLNPlot[0]].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for p in self.cLNPlot[1:]:
            self.wPlot.dPlot[p].rAxes.clear()
            self.wPlot.dPlot[p].rAxes2.clear()
            self.wPlot.dPlot[p].rAxes2.set_yticks([])
            self.wPlot.dPlot[p].rAxes2.set_yticklabels([])
            self.wPlot.dPlot[p].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def ExportData(self, df:Optional[pd.DataFrame]=None) -> bool:
        """Export data from each plot to a csv file.

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
            p = Path(dlg.GetPath())
            #------------------------------> Export
            try:
                date = self.rDateC.split(' - ')[0]
                sec = self.cSection.replace(' ', '-')
                origin = self.rObj.rStepDataP / f'{date}_{sec}'
                for k in origin.iterdir():
                    name = f'{self.rDateC} - {(k.stem).split("_")[1]}'
                    dest = p / f'{name}{k.suffix}'
                    #------------------------------>
                    shutil.copy(k, dest)
            except Exception as e:
                cWindow.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Data'),
                    tException = e,
                    parent     = self,
                )
        #endregion ------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---

    def ExportImgAll(self) -> bool:
        """Export all plots to a pdf image.

            Returns
            -------
            bool
        """
        #region -----------------------------------> Check Something to Export
        if self.rLCIdx < 0:
            msg = 'Please select one of the analyzed columns first.'
            cWindow.Notification('warning', msg=msg)
            return False
        #endregion --------------------------------> Check Something to Export

        #region --------------------------------------------------> Dlg window
        dlg = cWindow.DirSelect(parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p    = Path(dlg.GetPath())
            col  = self.wLC.wLCS.wLC.OnGetItemText(self.rLCIdx, 1)
            date = cMethod.StrNow()
            #------------------------------> Export
            try:
                for k, v in self.wPlot.dPlot.items():
                    #------------------------------> file path
                    fPath = p / self.cImgName[k].format(self.rDateC, col, 'pdf')
                    #------------------------------> Do not overwrite
                    if fPath.exists():
                        fPath = fPath.with_stem(f"{fPath.stem} - {date}")
                    #------------------------------> Write
                    v.rFigure.savefig(fPath)
            except Exception as e:
                cWindow.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Image'),
                    tException = e,
                    parent     = self,
                )
        #endregion ------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---
#endregion ----------------------------------------------------------> Classes

#region ------------------------------------------------> PubSub Subscriptions
pub.subscribe(CreateResDataPrep, mConfig.data.psResDataPrep)
#endregion ---------------------------------------------> PubSub Subscriptions

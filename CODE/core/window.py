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


"""Core Windows for the app"""


#region -------------------------------------------------------------> Imports
from math    import ceil
from pathlib import Path
from typing  import Optional, Union, Literal

import matplotlib.patches as mpatches
import pandas             as pd
from pubsub  import pub

import wx
from wx import aui

from config.config import config as mConfig
from core   import file   as cFile
from core   import method as cMethod
from core   import pane   as cPane
from core   import tab    as cTab
from core   import widget as cWidget
from result import file   as resFile
#endregion ----------------------------------------------------------> Imports


LIT_Notification = Literal['errorF', 'errorU', 'warning', 'success', 'question']
LIT_FSelect      = Literal['openO', 'openM', 'save']


#region --------------------------------------------------------------> Frames
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.

        Attributes
        ----------
        dKeyMethod: dict
            Keys are str and values classes or methods. Link menu items to
            windows methods.
    """
    #region -----------------------------------------------------> Class setup
    cSDeltaWin = mConfig.core.deltaWin
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent:Optional[wx.Window] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------> Def values if not given in child class
        self.cName    = getattr(self, 'cName',    mConfig.core.nwDef)
        self.cSWindow = getattr(self, 'cSWindow', mConfig.core.sWinFull)
        self.cTitle   = getattr(self, 'cTitle',   self.cName)
        #------------------------------>
        self.dKeyMethod = {}
        #------------------------------>
        super().__init__(
            parent, size=self.cSWindow, title=self.cTitle, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wStatBar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event:wx.CloseEvent) -> bool:                             # pylint: disable=unused-argument
        """Destroy window.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------> Reduce win number
        try:
            mConfig.core.winNumber[self.cName] -= 1
        except Exception:
            pass
        #endregion ----------------------------------------> Reduce win number

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Manage Methods
    def WinPos(self) -> dict:
        """Adjust win number and return information about the size of the
            window.

            Return
            ------
            dict
                Information about the size of the window and display and number
                of windows. See also data.method.GetDisplayInfo

            Notes
            -----
            Final position of the window on the display must be set in child
            class.
        """
        #region ---------------------------------------------------> Variables
        info = cMethod.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Update N
        mConfig.core.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return info
    #---
    #endregion ------------------------------------------------> Manage Methods
#---


class BaseWindowResult(BaseWindow):
    """Base class for windows showing results.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.

        Attributes
        ----------
        rData: cMethod.BaseAnalysis
            A new attribute 'Date-ID' is added to the class with value
            being the corresponding data class for each analysis done for the
            utility/module.
        rDate: list[str]
            List of available dates.
        rDateC: str
            Current selected date.
        rDf: pd.DataFrame
            DataFrame with the data for the currently selected date.

        Notes
        -----
        At least one plot is expected in the window.
    """

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cSWindow = getattr(self, 'cSWindow', mConfig.core.sWinPlot)
        self.cSection = getattr(self, 'cSection', '')
        #------------------------------>
        self.cMsgExportFailed = getattr(
            self, 'cMsgExportFailed', 'Export {} failed.')
        #------------------------------>
        self.rDate  = getattr(self, 'rDate',  [])
        self.rDateC = getattr(self, 'rDateC', '')
        self.rData  = getattr(self, 'rData',  cMethod.BaseAnalysis())
        self.rDataC = getattr(self, 'rDataC', pd.DataFrame())
        self.rDf    = getattr(self, 'rDf',    pd.DataFrame())
        self.rObj: resFile.UMSAPFile
        #------------------------------>
        super().__init__(parent=parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.core.kwWinUpdate   : self.UpdateResultWindow,
            mConfig.core.kwDupWin      : self.DupWin,
            mConfig.core.kwExpData     : self.ExportData,
            mConfig.core.kwExpImgAll   : self.ExportImgAll,
            mConfig.core.kwZoomResetAll: self.ZoomResetAll,
            mConfig.core.kwCheckDP     : self.CheckDataPrep,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event:wx.CloseEvent) -> bool:
        """Close window and uncheck section in UMSAPFile window. Assumes
            self.cParent is an instance of UMSAPControl.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update parent
        self.cParent.UnCheckSection(self.cSection, self)                        # type: ignore
        #endregion --------------------------------------------> Update parent

        #region ------------------------------------> Reduce number of windows
        mConfig.core.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class methods
    def ReportPlotDataError(self) -> bool:
        """Check that there is something to plot after reading a section in
            an UMSAP Plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------> Nothing to Plot
        if len(self.rData.date) < 1:
            msg = (f'All entries for {self.cSection} in file '
                   f'{self.rObj.rFileP.name} are corrupted or were not found.')
            Notification('errorU', msg=msg)
            raise ValueError(msg)
        #endregion ------------------------------------------> Nothing to Plot

        #region -------------------------------------------------> Some Errors
        if self.rData.error:
            #------------------------------>
            fileList = '\n'.join(self.rData.error)
            #------------------------------>
            if len(self.rData.error) == 1:
                msg = (f'The data for analysis:\n{fileList}\n '
                       f'contains errors or was not found.')
            else:
                msg = (f'The data for analysis:\n{fileList}\n '
                       f'contain errors or were not found.')
            #------------------------------>
            Notification('warning', msg=msg)
        #endregion ----------------------------------------------> Some Errors

        return True
    #---

    def DupWin(self) -> bool:
        """Duplicate window.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Duplicate
        self.cParent.rWindow[self.cSection]['Main'].append(                     # type: ignore
            self.cParent.dPlotMethod[self.cSection](self.cParent)               # type: ignore
        )
        #endregion ------------------------------------------------> Duplicate

        return True
    #---

    def ExportData(self, df:Optional[pd.DataFrame]=None) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool

            Notes
            -----
            It requires child class to define self.rDateC to catch the current
            date being plotted.
        """
        #region --------------------------------------------------> Dlg window
        dlg = FileSelect('save', mConfig.core.elData, parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p   = Path(dlg.GetPath())
            tDF = df
            if tDF is None:
                tDF = self.rDataC.df if df is None else df
            #------------------------------> Export
            try:
                cFile.WriteDF2CSV(p, tDF)                                       # type: ignore
            except Exception as e:
                Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Data'),
                    tException = e,
                    parent     = self,
                )
        #endregion ------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---

    def ExportDataFiltered(self, df: Optional[pd.DataFrame]=None) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = FileSelect('save', mConfig.core.elData, parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            tDF = self.rDf if df is None else df
            #------------------------------> Export
            try:
                cFile.WriteDF2CSV(p, tDF)
            except Exception as e:
                Notification(
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
        """Create and image of all plots in the window.

            Returns
            -------
            bool
        """
        return True
    #---

    def ZoomResetAll(self) -> bool:
        """Reset the zoom of all plots in the window.

            Returns
            -------
            bool
        """
        return True
    #---

    def UpdateResultWindow(self) -> bool:
        """Update the result window.

            Returns
            -------
            bool
        """
        return True
    #---

    def PlotTitle(self) -> bool:
        """Set the title of a plot window.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has self.cSection and self.rDateC and the parent
            is an UMSAPControl window
        """
        self.SetTitle(
            f"{self.cParent.cTitle} - {self.cSection} - {self.rDateC}")         # type: ignore

        return True
    #---

    def CheckDataPrep(self) -> bool:
        """Launch the Check Data Preparation Window.

            Returns
            -------
            bool
        """
        # PubSub is used here to avoid a cyclic import when launching
        # dataWindow.ResDataPrep
        #region --------------------------------------------------->
        pub.sendMessage(
            mConfig.data.psResDataPrep,
            parent   = self,
            title    = f'{self.GetTitle()} - {mConfig.data.nUtil}',
            tSection = self.cSection,
            tDate    = self.rDateC
        )
        #endregion ------------------------------------------------>

        return True
    #---

    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.rDate list and the menuData dict needed to build the
            Tool menu.

            Returns
            -------
            tuple of list and dict
            The list is a list of str with the dates in the analysis.
            The dict has the following structure:
                {
                    'MenuDate' : [List of dates],
                }
        """
        return (self.rData.date, {'MenuDate':self.rData.date})
    #---

    def UpdateUMSAPData(self) -> bool:
        """Update the window after the UMSAP file have been updated.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rObj  = self.cParent.rObj                                          # type: ignore
        self.rData = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        menuBar = self.GetMenuBar()
        menuBar.GetMenu(menuBar.FindMenu('Tools')).UpdateDateItems(menuData)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseWindowResultOnePlot(BaseWindowResult):
    """Base class for windows showing results.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.

        Notes
        -----
        At least one plot is expected in the window.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None,) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Widget
        self.wPlot = {0:cWidget.MatPlotPanel(self)}
        self.wPlot[0].SetStatBar(self.wStatBar, self.OnUpdateStatusBar)
        #endregion ------------------------------------------------> Widget

        #region ---------------------------------------------------> Sizers
        self.sSizer.Add(self.wPlot[0], 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sSizer)
        #endregion ------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def ExportImgAll(self) -> bool:
        """Create and image of all plots in the window.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            self.wPlot[0].SaveImage(
                ext=mConfig.core.elMatPlotSaveI, parent=self)
        except Exception as e:
            msg = "The image of the plot could not be saved."
            Notification('errorU', msg=msg, tException=e, parent=self)
        #endregion ------------------------------------------------>

        return True
    #---

    def ZoomResetAll(self) -> bool:
        """Reset the zoom of all plots in the window.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            self.wPlot[0].ZoomResetPlot()
        except Exception as e:
            msg = 'The zoom level of the plot could not be reset.'
            Notification('errorU', msg=msg, tException=e, parent=self)
        #endregion ------------------------------------------------>

        return True
    #---

    def OnUpdateStatusBar(self, event) -> bool:                                 # pylint: disable=unused-argument
        """Update the statusbar info.

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseWindowResultListText(BaseWindowResult):
    """Base window for results with a wx.ListCtrl and wx.TextCtrl.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCol    = getattr(self, 'cLCol', ['#', 'Item'])
        self.cSCol    = getattr(self, 'cSCol', [45, 100])
        self.cHSearch = getattr(self, 'cHSearch', 'Table')
        self.cLCStyle = getattr(
            self, 'cLCStyle', wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
        self.rLCIdx   = getattr(self, 'rLCIdx', -1)
        #------------------------------>
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wText = wx.TextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.wText.SetFont(mConfig.core.fSeqAlign)
        #------------------------------> wx.ListCtrl
        self.wLC = cPane.ListCtrlSearchPlot(
            self,
            colLabel = self.cLCol,
            colSize  = self.cSCol,
            style    = self.cLCStyle,
            tcHint   = f'Search {self.cHSearch}'
        )
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #endregion ------------------------------------------------------> AUI

        #region --------------------------------------------------------> Bind
        self.wLC.wLCS.wLC.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)
        self.wLC.wLCS.wLC.Bind(wx.EVT_LEFT_UP, self.OnListSelectEmpty)
        self.wLC.wLCS.wSearch.Bind(wx.EVT_SEARCH, self.OnSearch)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnSearch(self, event:wx.Event) -> bool:                                 # pylint: disable=unused-argument
        """Search for a given string in the wx.ListCtrl.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool

            Notes
            -----
            See mWidget.MyListCtrl.Search for more details.
        """
        #region ---------------------------------------------------> Get index
        tStr = self.wLC.wLCS.wSearch.GetValue()
        iEqual, iSimilar = self.wLC.wLCS.wLC.Search(tStr)
        #endregion ------------------------------------------------> Get index

        #region ----------------------------------------------> Show 1 Results
        if len(iEqual) == 1:
            self.SearchSelect(iEqual[0])
            return True
        #------------------------------>
        if len(iSimilar) == 1:
            self.SearchSelect(iSimilar[0])
            return True
        #endregion -------------------------------------------> Show 1 Results

        #region ----------------------------------------------> Show N Results
        if iSimilar:
            msg = (f'The string, {tStr}, was found in multiple rows.')
            tException = (
                f'The row numbers where the string was found are:\n '
                f'{str(iSimilar)[1:-1]}')
            Notification(
                'warning',
                msg        = msg,
                setText    = True,
                tException = tException,
                parent     = self,
            )
        else:
            msg = (f'The string, {tStr}, was not found.')
            Notification(
                'warning',
                msg        = msg,
                setText    = True,
                parent     = self,
            )
        #endregion -------------------------------------------> Show N Results

        return True
    #---

    def OnListSelect(self, event:Union[wx.CommandEvent, str]) -> bool:          # pylint: disable=unused-argument
        """Processes a wx.ListCtrl event.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        self.rLCIdx = self.wLC.wLCS.wLC.GetLastSelected()
        return True
    #---

    def OnListSelectEmpty(self, event: wx.CommandEvent) -> bool:
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
        idx = self.wLC.wLCS.wLC.GetFirstSelected()
        #------------------------------>
        if idx < 0 and self.rLCIdx > -1:
            self.wLC.wLCS.wLC.Select(self.rLCIdx, on=1)
        #endregion ------------------------------------------------>

        event.Skip()
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def SearchSelect(self, tRow: int) -> bool:
        """Select one of the row in the wx.ListCtrl.

            Parameters
            ----------
            tRow: int

            Returns
            -------
            bool

            Notes
            -----
            Helper to OnSearch
        """
        self.wLC.wLCS.wLC.Select(tRow, on=1)
        self.wLC.wLCS.wLC.EnsureVisible(tRow)
        self.wLC.wLCS.wLC.SetFocus()
        self.OnListSelect('fEvent')
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class BaseWindowResultListTextNPlot(BaseWindowResultListText):
    """Base window for results with a wx.ListCtrl, wx.TextCtrl and mPane.NPlots.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.
        statusbar: wx.StatusBar or None
            To print info from plots to the wx.StatusBar. Default is None.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window]=None,
        statusbar:Optional[wx.StatusBar]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLNPlot   = getattr(self, 'cLNPlot',   ['Plot 1', 'Plot 2'])
        self.cNPlotCol = getattr(self, 'cNPlotCol', 1)
        self.cTPlot    = getattr(self, 'cTPlot',    'Plots')
        self.cTText    = getattr(self, 'cTText',    'Details')
        self.cTList    = getattr(self, 'cTList',    'Table')
        #------------------------------>
        super().__init__(parent=parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.core.kwExpImg   : self.ExportImg,
            mConfig.core.kwZoomReset: self.ZoomReset,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wPlot = cPane.NPlots(
            self, self.cLNPlot, self.cNPlotCol, statusbar=statusbar)
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        self._mgr.AddPane(
            self.wPlot,
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.cTPlot
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        self._mgr.AddPane(
            self.wText,
            aui.AuiPaneInfo(
                ).Bottom(
                ).Layer(
                    0
                ).Caption(
                    self.cTText
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        self._mgr.AddPane(
            self.wLC,
            aui.AuiPaneInfo(
                ).Left(
                ).Layer(
                    1
                ).Caption(
                    self.cTList
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.Update()
        #endregion ------------------------------------------------------> AUI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def ZoomResetAll(self) -> bool:
        """Reset Zoom of all plots.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        for v in self.wPlot.dPlot.values():
            v.ZoomResetPlot()
        #endregion ------------------------------------------------>

        return True
    #---

    def ExportImg(self, tKey: str) -> bool:
        """Export an image of one of the plots in self.wPlot.dPlot.

            Parameters
            ----------
            tKey: str
                Key in self.wPlot.dPlot

            Returns
            -------
            bool
        """
        try:
            self.wPlot.dPlot[tKey].SaveImage(
                mConfig.core.elMatPlotSaveI, parent=self)
        except Exception as e:
            Notification(
                'errorU',
                msg        = self.cMsgExportFailed.format('Image'),
                tException = e,
                parent     = self,
                )
            return False
        return True
    #---

    def ZoomReset(self, tKey: str) -> bool:
        """Reset the zoom of one of the plots in self.wPlot.dPlot.

            Parameters
            ----------
            tKey: str
                Key in self.wPlot.dPlot

            Returns
            -------
            bool
        """
        try:
            self.wPlot.dPlot[tKey].ZoomResetPlot()
        except Exception as e:
            msg = 'It was not possible to reset the zoom on the selected plot.'
            Notification('errorU', msg=msg, tException=e, parent=self)
            return False
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class BaseWindowResultListText2Plot(BaseWindowResultListText):
    """Base class to create a window like Limited Proteolysis.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default is None.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Labels
        self.cLPaneMain = getattr(self, 'cLPaneMain', 'Protein Fragments')
        self.cLPaneSec  = getattr(self, 'cLPaneSec', 'Gel Representation')
        self.cLPaneText = getattr(self, 'cLPaneText', 'Selection Details')
        self.cLPaneList = getattr(self, 'cLPaneList', 'Peptide List')
        self.cLCol      = getattr(self, 'cLCol', ['#', 'Peptides'])
        self.cImgName   = getattr(self, 'cImgName', {})
        #------------------------------>
        self.cGelLineWidth = getattr(self, 'cGelLineWidth', 0.5)
        #------------------------------> Hints
        self.cHSearch = getattr(self, 'cHSearch', 'Peptides')
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.core.kwExpImg   : self.ExportImg,
            mConfig.core.kwZoomReset: self.ZoomReset,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wPlot = {
            'Main' : cWidget.MatPlotPanel(self),
            'Sec'  : cWidget.MatPlotPanel(self),
        }
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        self._mgr.AddPane(
            self.wPlot['Main'],
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.cLPaneMain
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.AddPane(
            self.wPlot['Sec'],
            aui.AuiPaneInfo(
                ).Bottom(
                ).Layer(
                    0
                ).Caption(
                    self.cLPaneSec
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.AddPane(
            self.wText,
            aui.AuiPaneInfo(
                ).Bottom(
                ).Layer(
                    0
                ).Caption(
                    self.cLPaneText
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.AddPane(
            self.wLC,
            aui.AuiPaneInfo(
                ).Left(
                ).Layer(
                    2
                ).Caption(
                    self.cLPaneList
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.Update()
        #endregion ------------------------------------------------------> AUI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def ExportImg(self, tKey:str) -> bool:
        """Save an image of the selected plot.

            Parameters
            ----------
            tKey: str
                Key in self.wPlot

            Returns
            -------
            bool
        """
        return self.wPlot[tKey].SaveImage(
            ext=mConfig.core.elMatPlotSaveI, parent=self)
    #---

    def ZoomReset(self, tKey:str) -> bool:
        """Reset the Zoom of the selected plot.

            Parameters
            tKey: str
                Key in self.wPlot.

            Returns
            -------
            bool
        """
        return self.wPlot[tKey].ZoomResetPlot()
    #---

    def ExportImgAll(self) -> bool:
        """Export all plots to a tiff image.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = DirSelect(parent=self)
        #endregion -----------------------------------------------> Dlg window

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p    = Path(dlg.GetPath())
            date = cMethod.StrNow()
            #------------------------------> Export
            try:
                for k, v in self.wPlot.items():
                    fPath = p / self.cImgName[k].format(self.rDateC)
                    #------------------------------> Do not overwrite
                    if fPath.exists():
                        fPath = fPath.with_stem(f"{fPath.stem} - {date}")
                    #------------------------------> Write
                    v.rFigure.savefig(fPath)
            except Exception as e:
                Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed.format('Images'),
                    tException = e,
                    parent     = self,
                )
        #endregion ------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---

    def ZoomResetAll(self) -> bool:
        """Reset the zoom of all plots in the window.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        for v in self.wPlot.values():
            v.ZoomResetPlot()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class BaseWindowResultListText2PlotFragments(BaseWindowResultListText2Plot):
    """Base Window for results showing a Fragments panel.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None
        menuData : dict
            Data to build the Tool menu of the window. See structure in child
            class.
    """
    #region -----------------------------------------------------> Class Setup
    cCNatProt = mConfig.core.cNatProt
    cCRecProt = mConfig.core.cRecProt
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cSpot = getattr(self, 'cSpot', mConfig.core.cFragments)
        #------------------------------>
        self.rIdxSeqNC = getattr(
            self, 'rIdxSeqNC', pd.IndexSlice[mConfig.core.dfcolSeqNC,:,:])
        self.rAlpha       = getattr(self, 'rAlpha', 0.05)
        self.rFragSelLine = None
        self.rFragments   = {}
        self.rProtLoc     = []
        self.rProtLength  = None
        self.rPeptide     = None
        self.rFragSelC    = [None, None, None]
        self.rRectsFrag   = []
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.core.kwExpSeq : self.SeqExport,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Bind
        self.wPlot['Main'].rCanvas.mpl_connect(
            'pick_event', self.OnPickFragment)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def GetDF4FragmentSearch(self) -> pd.DataFrame:
        """Get the pd.Dataframe needed to create the fragments.

            Returns
            -------
            pd.DataFrame
            Seq Nrec Crec Nnat Cnat Col1 Col2 ColN

            Notes
            -----
            Col1 to ColN is expected to hold the P values from the analysis.
        """
        a = self.rDf.loc[:,self.rIdxSeqNC]                                      # type: ignore
        b = self.rDf.loc[:,self.rIdxP]                                          # type: ignore
        #------------------------------>
        return pd.concat([a,b], axis=1)
    #---

    def SetEmptyFragmentAxis(self) -> bool:
        """Set the axis for an empty fragment state.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
        #------------------------------>
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rAxes.clear()
        self.wPlot['Main'].rAxes.set_xticks([])
        self.wPlot['Main'].rAxes.set_yticks([])
        self.wPlot['Main'].rAxes.tick_params(length=0)
        self.wPlot['Main'].rAxes.spines['top'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['right'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['bottom'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['left'].set_visible(False)
        self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def FillListCtrl(self) -> bool:
        """Update the protein list for the given analysis.

            Attributes
            ----------
            tIDX: pd.IndexSlice
                To select columns used to filter self.rDf by alpha value

            Returns
            -------
            bool

            Notes
            -----
            Entries are read from self.rDf
        """
        #region --------------------------------------------------> Delete old
        self.wLC.wLCS.wLC.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old

        #region ----------------------------------------------------> Get Data
        col = [self.rDf.columns.get_loc(c) for c in self.rDf.loc[:,self.rIdxP].columns.values]      # type: ignore
        data = cMethod.DFFilterByColN(self.rDf, col, self.rAlpha, 'le')
        data = data.iloc[:,0:2].reset_index(drop=True)
        data.insert(0, 'kbr', data.index.values.tolist())
        data = data.astype(str)
        data = data.iloc[:,0:2].values.tolist()
        #endregion -------------------------------------------------> Get Data

        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.wLC.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl

        #region ---------------------------------------> Update Protein Number
        self._mgr.GetPane(self.wLC).Caption(f'{self.cLPaneList} ({len(data)})')
        self._mgr.Update()
        #endregion ------------------------------------> Update Protein Number

        return True
    #---

    def DrawFragments(self, tKeyLabel:dict) -> bool:
        """Draw the fragments associated with the given keys.

            Parameters
            ----------
            tKeyLabel: dict
                Keys are the key to plot and values the associated labels.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rRectsFrag = []
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Set Axis
        self.SetFragmentAxis()
        #endregion -------------------------------------------------> Set Axis

        #region ---------------------------------------------------> Fragments
        nc = len(self.cSpot)
        #------------------------------>
        k = 1
        for k,v in enumerate(tKeyLabel, start=1):
            frag = getattr(self.rFragments, v)
            for j,f in enumerate(frag.coord):
                self.rRectsFrag.append(mpatches.Rectangle(
                    (f[0], k-0.2),
                    (f[1]-f[0]),
                    0.4,
                    picker    = True,
                    linewidth = self.cGelLineWidth,
                    facecolor = self.cSpot[(k-1)%nc],
                    edgecolor = 'black',
                    label     = f'{tKeyLabel[v]}.{j}',
                ))
                self.wPlot['Main'].rAxes.add_patch(self.rRectsFrag[-1])
        #endregion ------------------------------------------------> Fragments

        #region -----------------------------------------------------> Protein
        self.DrawProtein(k+1)
        #endregion --------------------------------------------------> Protein

        #region --------------------------------------------------------> Draw
        self.wPlot['Main'].ZoomResetSetValues()

        self.wPlot['Main'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        #region --------------------------------------------------->
        if self.rPeptide is not None:
            self.ShowPeptideLoc()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetFragmentAxis(self, showAll: list[str]=[]) -> bool:                   # pylint: disable=unused-argument, dangerous-default-value
        """Set the axis of the Fragments plot.

            Parameters
            ----------
            showAll: list[str]
                List of labels when selecting the entire gel.

            Returns
            -------
            bool
        """
        return True
    #---

    def SeqExport(self) -> bool:
        """Export the recombinant sequence

            Returns
            -------
            bool
        """
        return True
    #---

    def OnPickFragment(self, event) -> bool:                     # pylint: disable=dangerous-default-value, unused-argument
        """Display info about the selected fragment.

            Parameters
            ----------
            event: matplotlib pick event.

            Returns
            -------
            bool
        """
        return True
    #---

    def ShowPeptideLoc(self) -> bool:
        """Show the location of the selected peptide.

            Returns
            -------
            bool
        """
        return True
    #---

    def DrawProtein(self, y: int) -> bool:
        """Draw the protein fragment

            Parameters
            ----------
            y: int
                Y coordinate to draw the protein.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        recProt = []
        natProt = []
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        if self.rProtLoc[0] > -1:
            #------------------------------>
            natProt.append(self.rProtLoc)
            a, b = self.rProtLoc
            #------------------------------>
            if a == 1 and b == self.rProtLength:
                pass
            elif a == 1 and b < self.rProtLength:
                recProt.append((b, self.rProtLength))
            elif a > 1 and b == self.rProtLength:
                recProt.append((1, a))
            else:
                recProt.append((1, a))
                recProt.append((b, self.rProtLength))
        else:
            recProt.append((1, self.rProtLength))
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Draw Rect
        for r in natProt:
            self.wPlot['Main'].rAxes.add_patch(mpatches.Rectangle(
                (r[0], y-0.2),
                r[1] - r[0],
                0.4,
                edgecolor = 'black',
                facecolor = self.cCNatProt,
            ))
        #------------------------------>
        for r in recProt:
            self.wPlot['Main'].rAxes.add_patch(mpatches.Rectangle(
                (r[0], y-0.2),
                r[1] - r[0],
                0.4,
                edgecolor = 'black',
                facecolor = self.cCRecProt,
            ))
        #endregion ------------------------------------------------> Draw Rect

        return True
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnListSelect(self, event:Union[wx.CommandEvent, str]) -> bool:
        """Process a wx.ListCtrl select event.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rLCIdx = self.wLC.wLCS.wLC.GetFirstSelected()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rPeptide = self.wLC.wLCS.wLC.GetItemText(self.rLCIdx, col=1)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.ShowPeptideLoc()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class BaseWindowResultOnePlotFA(BaseWindowResultOnePlot):
    """Base Window for Further Analysis with one Plot, e.g. AA.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None
        menuData: dict
            Data to build the Tool menu of the window. See structure in child
            class.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def ExportData(self, df:Optional[pd.DataFrame]=None) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        if df is None:
            df = self.rData                                                     # type: ignore
        #------------------------------>
        return super().ExportData(df=df)
    #---
    #endregion ------------------------------------------------> Class methods

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event:wx.CloseEvent) -> bool:
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
        mConfig.core.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion -----------------------------------------------------------> Frames


#region -------------------------------------------------------------> Dialogs
class BaseDialogOkCancel(wx.Dialog):
    """Basic wx.Dialog with a Cancel Ok Button.

        Parameters
        ----------
        title: str
            Title of the wx.Dialog.
        parent: wx.Window or None
            To center the dialog on the parent.
        size: wx.Size
            Size of the wx.Dialog.

        Attributes
        ----------
        sBtn: wx.Sizer
            Sizer with the Cancel, OK buttons.
        sSizer: wx.BoxSizer(wx.Vertical)
            Main Sizer of the wx.Dialog
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title:str                  = '',
        parent:Optional[wx.Window] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cStyle = getattr(
            self, 'cStyle', wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER)
        self.cSize = getattr(self, 'cSize', (600, 900))
        #------------------------------>
        super().__init__(
            parent, title=title, style=self.cStyle, size=self.cSize)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.sBtn = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK,     id = wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id = wx.ID_CANCEL)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event:wx.CommandEvent) -> bool:                              # pylint: disable=unused-argument
        """Validate user information and close the window.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool

            Notes
            -----
            Basic implementation. Override as needed.
        """
        self.EndModal(1)
        self.Close()
        #------------------------------>
        return True
    #---

    def OnCancel(self, event:wx.CommandEvent) -> bool:                          # pylint: disable=unused-argument
        """The macOs implementation has a bug here that does not discriminate
            between the Cancel and Ok button and always return self.EndModal(1).

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            True
        """
        self.EndModal(0)
        self.Close()
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class ListSelect(BaseDialogOkCancel):
    """Select values from a list of options.

        Parameters
        ----------
        color: str
            Alternating color for the wx.ListCtrl
        parent: wx.Window
            Parent of the window
        rightDelete: bool
            Delete content of the right wx.ListCtrl with a right click
        tBtnLabel: str
            Label for the Add wx.Button
        tColLabel: list[str]
            Label for the name of the columns in the wx.ListCtrl. It is assumed
            both wx.ListCtrl have the same column labels.
        tColSize: list[int]
            Size of the columns in the wx.ListCtrl. It is assumed both
            wx.ListCtrl have the same size.
        title: str
            Title of the window
        tOptions: list[list[str]]
            Available options.
        tSelOptions: list[list[str]]
            Already selected options. Optional
        tStLabel: list[str]
            Label to show on top of the wx.ListCtrl.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        tOptions:list[list[str]],
        tColLabel:list[str],
        tColSize:list[int],
        tSelOptions:list[list[str]] = [],
        title:str                   = '',
        tStLabel:list[str]          = [],
        tBtnLabel:str               = '',
        parent:Optional[wx.Window]  = None,
        color:str                   = mConfig.core.cZebra,
        rightDelete:bool            = True,
        style:int                   = wx.LC_REPORT|wx.LC_VIRTUAL,
        allowEmpty:bool             = False,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rAllowEmpty = allowEmpty
        #------------------------------>
        if tStLabel:
            self.cStLabel = tStLabel
        else:
            self.cStLabel = ['Available options', 'Selected options']
        #------------------------------>
        if tBtnLabel:
            self.cBtnLabel = tBtnLabel
        else:
            self.cBtnLabel = 'Add options'
        #------------------------------>
        if not title:
            title = 'Select options'
        #------------------------------>
        super().__init__(parent=parent, title=title)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.StaticText
        self.wStListI = wx.StaticText(self, label=self.cStLabel[0])
        self.wStListO = wx.StaticText(self, label=self.cStLabel[1])
        #------------------------------> dtsWidget.ListZebra
        self.wLCtrlI = cWidget.MyListCtrlZebra(self,
            color           = color,
            colLabel        = tColLabel,
            colSize         = tColSize,
            copyFullContent = True,
            style           = style,
        )
        self.wLCtrlI.SetNewData(tOptions)

        self.wLCtrlO = cWidget.MyListCtrlZebra(self,
            color           = color,
            colLabel        = tColLabel,
            colSize         = tColSize,
            canPaste        = True,
            canCut          = True,
            copyFullContent = True,
        )
        for r in tSelOptions:
            self.wLCtrlO.Append(r)
        #------------------------------> wx.Button
        self.wAddCol = wx.Button(self, label=self.cBtnLabel)
        self.wAddCol.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), dir = wx.RIGHT)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sList = wx.FlexGridSizer(2,3,5,5)
        self.sList.Add(self.wStListI, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.AddStretchSpacer(1)
        self.sList.Add(self.wStListO, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.Add(self.wLCtrlI,  0, wx.EXPAND|wx.ALL,       5)
        self.sList.Add(self.wAddCol,  0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.Add(self.wLCtrlO,  0, wx.EXPAND|wx.ALL,       5)
        self.sList.AddGrowableCol(0,1)
        self.sList.AddGrowableCol(2,1)
        self.sList.AddGrowableRow(1,1)
        #------------------------------>
        self.sSizer.Add(self.sList, 1, wx.EXPAND|wx.ALL,      5)
        self.sSizer.Add(self.sBtn,  0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region ----------------------------------------------------> Tooltips
        self.wStListI.SetToolTip(
            f"Selected rows can be copied ({mConfig.core.copyShortCut}+C) but "
            f"the list cannot be modified.")
        self.wStListO.SetToolTip(
            f"New rows can be pasted ({mConfig.core.copyShortCut}+V) after the "
            f"last selected element and existing ones cut/deleted "
            f"({mConfig.core.copyShortCut}+X) or copied "
            f"({mConfig.core.copyShortCut}+C)." )
        self.wAddCol.SetToolTip(
            'Add selected rows in the left list to the '
            'right list. New columns will be added after the last selected '
            'row in the right list. Duplicate columns are discarded.')
        #endregion -------------------------------------------------> Tooltips

        #region --------------------------------------------------------> Bind
        self.wAddCol.Bind(wx.EVT_BUTTON, self.OnAdd)
        #------------------------------>
        if rightDelete:
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
            self.wLCtrlO.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event:wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        if self.rAllowEmpty:
            self.EndModal(1)
            self.Close()
            return True
        #endregion ----------------------------------------------------->

        #region ----------------------------------------------------> Validate
        if self.wLCtrlO.GetItemCount() > 0:
            self.EndModal(1)
            self.Close()
        else:
            return False
        #endregion -------------------------------------------------> Validate

        return True
    #---

    def OnAdd(self, event:Union[wx.Event, str]) -> bool:                        # pylint: disable=unused-argument
        """Add columns to analyze using the button.

            Parameters
            ----------
            event: wx.Event
                Event information.

            Returns
            -------
            bool
        """
        self.wLCtrlI.OnCopy('')
        self.wLCtrlO.OnPaste('')
        #------------------------------>
        return True
    #---

    def OnRightDelete(self, event:Union[wx.Event, str]) -> bool:                # pylint: disable=unused-argument
        """Delete list with a right click.

            Parameters
            ----------
            event: wx.Event
                Event information.

            Returns
            -------
            bool
        """
        self.wLCtrlO.DeleteAllItems()
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class Progress(wx.Dialog):
    """Custom progress dialog.

        Parameters
        ----------
        parent: wx.Window
            Parent of the dialogue.
        title: str
            Title of the dialogue.
        count: int
            Number of steps for the wx.Gauge
        img: Path, str or None
            Image to show in the dialogue.
        style: wx style
            Style of the dialogue.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window],
        title:str,
        count:int,
        img:Path  = mConfig.core.fImgIcon,
        style:int = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=title, style=style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(self, label='')
        self.wG  = wx.Gauge(self, range=count, size=(400, 10))
        self.wStTime = wx.StaticText(self, label='')
        self.wStLabel = wx.StaticText(self, label='')
        self.wStLabel.SetFont(self.wStLabel.GetFont().MakeBold())
        self.wTcError = wx.TextCtrl(
            self,
            size  = (565, 100),
            style = wx.TE_READONLY|wx.TE_MULTILINE,
        )
        if img is not None:
            self.img = wx.StaticBitmap(
                self,
                bitmap = wx.Bitmap(str(img), wx.BITMAP_TYPE_PNG),
            )
        else:
            self.img = None
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sBtn = self.CreateButtonSizer(wx.OK)

        self.sStG = wx.BoxSizer(wx.VERTICAL)
        self.sStG.Add(self.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 5)
        self.sStG.Add(self.wG, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sStG.Add(self.wStTime, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)

        self.sProgress = wx.GridBagSizer(1,1)
        if self.img is not None:
            self.sProgress.Add(
                self.img,
                pos    = (0,0),
                flag   = wx.ALIGN_CENTER|wx.ALL,
                border = 5,
            )

        if self.img is not None:
            pos = (0,1)
        else:
            pos = (0,0)

        self.sProgress.Add(
            self.sStG,
            pos    = pos,
            flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5
        )
        self.sProgress.AddGrowableCol(pos[1],1)

        self.sError = wx.BoxSizer(wx.VERTICAL)
        self.sError.Add(self.wStLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sError.Add(self.wTcError, 1, wx.EXPAND|wx.ALL, 5)

        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(self.sProgress, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sError, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)

        self.sSizer.Hide(self.sError, recursive=True)
        self.sSizer.Hide(self.sBtn, recursive=True)

        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers
        if parent is not None:
            self.CenterOnParent()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def UpdateStG(self, text:str, step:int=1) -> bool:
        """Update the step message and the gauge step.

            Parameters
            ----------
            text: str
                Text for the wx.StaticText.
            step: int
                Number of steps to increase the gauge.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update values
        self.wG.SetValue(self.wG.GetValue()+step)
        self.wSt.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def UpdateG(self, step:int=1) -> bool:
        """Update only the gauge of the dialogue.

            Parameters
            ----------
            step: int
                Number of steps to increase the gauge.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update values
        self.wG.SetValue(self.wG.GetValue()+step)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def UpdateSt(self, text:str) -> bool:
        """Update the step message.

            Parameters
            ----------
            text : str
                Text for the wx.StaticText
        """
        #region -----------------------------------------------> Update values
        self.wSt.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def SuccessMessage(self, label:str, eTime:str='') -> bool:
        """Show a Success message.

            Parameters
            ----------
            label: str
                All done message.
            eTime: str
                Secondary message to display below the gauge. e.g. Elapsed time.
        """
        #region ------------------------------------------------------> Labels
        self.wSt.SetLabel(label)
        self.wSt.SetFont(self.wSt.GetFont().MakeBold())
        if eTime:
            self.wStTime.SetLabel(eTime)
        #endregion ---------------------------------------------------> Labels

        #region -------------------------------------------------------> Sizer
        #------------------------------> Center Success message
        self.sStG.GetItem(self.wSt).SetFlag(wx.ALIGN_CENTRE|wx.TOP|wx.LEFT)
        #------------------------------> Show buttons
        self.sSizer.Show(self.sBtn, recursive=True)
        #------------------------------> Layout & Show
        self.sSizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer

        return True
    #---

    def ErrorMessage(
        self,
        label:str,
        error:str                      = '',
        tException:Optional[Exception] = None,
        ) -> bool:
        """Show error message.

            Parameters
            ----------
            label: str
                Label to show.
            error: str
                Error message.
            tException : Exception or None
                Exception raised to offer full traceback.
        """
        #region -------------------------------------------------> Check input
        if not error and tException is None:
            msg = ("Both error and tException cannot be None")
            raise ValueError(msg)
        #endregion ----------------------------------------------> Check input

        #region ------------------------------------------------------> Labels
        self.wStLabel.SetLabel(label)
        #------------------------------>
        if error:
            self.wTcError.SetValue(error)
        #------------------------------>
        if tException is not None:
            if error:
                self.wTcError.AppendText('\n\nFurther details:\n')
            self.wTcError.AppendText(cMethod.StrException(tException))
        #------------------------------>
        self.wTcError.SetInsertionPoint(0)
        #endregion ---------------------------------------------------> Labels

        #region -------------------------------------------------------> Sizer
        self.sSizer.Show(self.sError, recursive=True)
        self.sSizer.Show(self.sBtn, recursive=True)

        self.sSizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class Notification(wx.Dialog):
    """Show a custom notification dialog.

        Parameters
        ----------
        mode: str
            One of 'errorF', 'errorU', 'warning', 'success', 'question'
        msg: str
            General message to place below the Notification type. This cannot be
            copied by the user.
        tException: str, Exception or None
            The message and traceback to place in the wx.TextCtrl. This
            can be copied by the user. If str then only an error message will
            be placed in the wx.TextCtrl.
        parent: wx widget or None
            Parent of the dialog.
        button: int
            Kind of buttons to show. 1 is wx.OK else wx.OK|wx.CANCEL
        setText: bool
            Set wx.TextCtrl for message independently of the mode of the window.
            Default is False.
    """
    #region -----------------------------------------------------> Class setup
    style = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    error = ['errorF', 'errorU']
    img   = mConfig.core.fImgIcon
    #------------------------------>
    cTitle = 'UMSAP - Notification'
    #------------------------------>
    oNotification = {
        'errorF' : 'Fatal Error',
        'errorU' : 'Unexpected Error',
        'warning': 'Warning',
        'success': 'Success',
        'question':'Please answer the following question:',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        mode:LIT_Notification,
        msg:str                          = '',
        tException:Union[Exception, str] = '',
        parent:Optional[wx.Window]       = None,
        button:int                       = 1,
        setText:bool                     = False,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        if not msg and not tException:
            msg = "The message and exception received were both empty."
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=self.cTitle, style=self.style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wType = wx.StaticText(
            self,
            label = self.oNotification[mode],
        )
        self.wType.SetFont(self.wType.GetFont().MakeBold())

        if msg:
            self.wMsg = wx.StaticText(self, label=msg)
        else:
            self.wMsg = None

        if mode in self.error or setText:
            self.wError = wx.TextCtrl(
                self,
                size  = (565, 100),
                style = wx.TE_READONLY|wx.TE_MULTILINE,
            )
            self.SetErrorText(msg, tException)

        self.wImg = wx.StaticBitmap(
            self,
            bitmap = wx.Bitmap(str(self.img), wx.BITMAP_TYPE_PNG),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Create Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sTop   = wx.GridBagSizer(1,1)
        if button == 1:
            self.sBtn = self.CreateButtonSizer(wx.OK)
        else:
            self.sBtn = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        #------------------------------> Top Sizer
        self.sTop.Add(
            self.wImg,
            pos    = (0,0),
            flag   = wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
            border = 5,
            span   = (3,0),
        )
        self.sTop.Add(
            self.wType,
            pos    = (0,1),
            flag   = wx.ALIGN_LEFT|wx.ALL,
            border = 5
        )
        if self.wMsg is not None:
            self.sTop.Add(
                self.wMsg,
                pos    = (1,1),
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )

        if getattr(self, 'wError', False):
            #------------------------------>
            if self.wMsg is not None:
                pos = (2,1)
            else:
                pos = (1,1)
            #------------------------------>
            self.sTop.Add(
                self.wError,
                pos    = pos,
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )
        #--------------> Add Grow Col to Top Sizer
        self.sTop.AddGrowableCol(1,1)
        if getattr(self, 'wError', False):
            if self.wMsg is not None:
                self.sTop.AddGrowableRow(2,1)
            else:
                self.sTop.AddGrowableRow(1,1)
        #------------------------------> Main Sizer
        self.sSizer.Add(self.sTop, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        if parent is not None:
            self.CenterOnParent()
        #------------------------------>
        self.ShowModal()
        self.Destroy()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetErrorText(
        self,
        msg:str                          = '',
        tException:Union[Exception, str] = '',
        ) -> bool:
        """Set the error text in the wx.TextCtrl.

            Parameters
            ----------
            msg: str
                Error message.
            tException: Exception, str
                To display full traceback or a custom further details message.
        """
        #region -----------------------------------------------------> Message
        if msg:
            self.wError.AppendText(msg)
        #endregion --------------------------------------------------> Message

        #region ---------------------------------------------------> Exception
        if tException:
            if msg:
                self.wError.AppendText('\n\nFurther details:\n\n')
            if isinstance(tException, str):
                self.wError.AppendText(tException)
            else:
                self.wError.AppendText(cMethod.StrException(tException))
        #endregion ------------------------------------------------> Exception

        self.wError.SetInsertionPoint(0)
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ResControlExp(BaseDialogOkCancel):
    """Creates the dialog to type values for Results - Control Experiments.

        Parameters
        ----------
        parent: wx.Window
            This is the pane calling the dialog.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.core.ndResCtrlExp
    cTitle = mConfig.core.twResCtrl
    #------------------------------>
    cSize = (900, 580)
    #------------------------------>
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        if (iFile := parent.wIFile.wTc.GetValue())  == '': # type: ignore
            #------------------------------>
            dlg = FileSelect('openO', mConfig.core.elData, parent=parent)
            #------------------------------>
            if dlg.ShowModal() == wx.ID_OK:
                iFile = dlg.GetPath()
                parent.wIFile.wTc.SetValue(iFile) # type: ignore
                dlg.Destroy()
            else:
                dlg.Destroy()
                raise RuntimeError("No input file selected.")
        else:
            pass
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(title=self.cTitle, parent=mConfig.main.mainWin)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wConf = cTab.ResControlExp(self, iFile, parent)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        self.sSizer.Add(self.wConf, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ----------------------------------------------------> Sizer

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        if parent is not None:
            self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event:wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.wConf.wConf.OnOK():
            self.EndModal(1)
            self.Close()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class FileSelect(wx.FileDialog):
    """Creates a dialog to select a file to read/save content from/into.

        Parameters
        ----------
        mode: str
            One of 'openO', 'openM', 'save'.
        wildcard: str
            File extensions, 'txt files (*.txt)|*.txt'.
        parent: wx.Window or None
            Parent of the window. If given modal window will be centered on it.
        message: str
            Message to show in the window.
        defPath: Path, str or None
            Default value for opening wx.FileDialog.

        Attributes
        ----------
        rTitle: dict
            Default titles for the dialog.
        rStyle: dict
            Style for the dialog.
    """
    #region -----------------------------------------------------> Class setup
    rTitle = {
        'openO': 'Select a file',
        'openM': 'Select files',
        'save' : 'Select a file',
    }

    rStyle = {
        'openO': wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW,
        'openM': wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW|wx.FD_MULTIPLE,
        'save' : wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        mode:LIT_FSelect,
        ext:str,
        parent:Optional['wx.Window']   = None,
        msg:str                        = '',
        defPath:Union[Path, str, None] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------------> Message
        msg = self.rTitle[mode] if msg is None else msg
        #endregion --------------------------------------------------> Message

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent,
            message    = msg,
            wildcard   = ext,
            style      = self.rStyle[mode],
            defaultDir = '' if defPath is None else str(defPath),
        )

        if parent is not None:
            self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class DirSelect(wx.DirDialog):
    """Creates a dialog to select a folder.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. If given modal window will be centered on it.
        message: str
            Message to show in the window.
        defPath: Path or str
            Default value for opening wx.DirDialog.
    """
    #region -----------------------------------------------------> Class setup
    title = 'Select a folder'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window] = None,
        message:str                = '',
        defPath:Union[str,Path]    = '',
        ) -> None:
        """ """
        #region -------------------------------------------------> Check input
        msg = self.title if message else message
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent,
            message     = msg,
            defaultPath = str(defPath),
        )
        if parent is not None:
            self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class FABtnText(BaseDialogOkCancel):
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
        title: str
            Title of the wx.Dialog.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        btnLabel:str,
        btnHint:str,
        ext:str,
        btnValidator:wx.Validator,
        stLabel:str,
        stHint:str,
        stValidator :wx.Validator,
        parent:Optional[wx.Window] = None,
        title:str = 'Export Sequence Alignments',
        ):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(title=title, parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnTc = cWidget.ButtonTextCtrlFF(
            self,
            btnLabel  = btnLabel,
            tcHint    = btnHint,
            ext       = ext,
            mode      = 'save',
            validator = btnValidator,
        )
        self.wLength = cWidget.StaticTextCtrl(
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
    def OnOK(self, event:wx.CommandEvent) -> bool:
        """Validate user information and close the window

            Parameters
            ----------
            event: wx.Event
                Information about the event.

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
        if not self.wBtnTc.wTc.GetValidator().Validate()[0]:
            errors += 1
            self.wBtnTc.wTc.SetValue('')

        if not self.wLength.wTc.GetValidator().Validate()[0]:
            errors += 1
            self.wLength.wTc.SetValue('')
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        if not errors:
            self.EndModal(1)
            self.Close()
        #endregion ----------------------------------------------------->

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FA2Btn(BaseDialogOkCancel):
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
        title: str
            Title of the wx.Dialog.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        btnLabel:list[str],
        btnHint:list[str],
        ext:list[str],
        btnValidator:list[wx.Validator],
        parent:Optional[wx.Window] = None,
        title:str = 'PDB Mapping',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(title=title, parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnI = cWidget.ButtonTextCtrlFF(
            self,
            btnLabel  = btnLabel[0],
            tcHint    = btnHint[0],
            ext       = ext[0],
            mode      = 'openO',
            validator = btnValidator[0],
        )

        self.wBtnO = cWidget.ButtonTextCtrlFF(
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
    def OnOK(self, event:wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

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
        if not self.wBtnI.wTc.GetValidator().Validate()[0]:
            errors += 1
            self.wBtnI.wTc.SetValue('')

        if not self.wBtnO.wTc.GetValidator().Validate()[0]:
            errors += 1
            self.wBtnO.wTc.SetValue('')
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        if not errors:
            self.EndModal(1)
            self.Close()
        #endregion ----------------------------------------------------->

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class UserInputText(BaseDialogOkCancel):
    """Present a modal window with N wx.TextCtrl for user input.

        Parameters
        ----------
        title: str
            Title of the dialog.
        label: list[str]
            Labels for the wx.StaticText in the dialog.
        hint: list[str]
            Hint for the wx.TextCtrl in the dialog.
        parent: wx.Window or None
            To center the dialog on the parent.
        validator: list[wx.Validator]
            The validator is expected to comply with the return of validators in
            mValidator.
        size: wx.Size
            Size of the window. Default is (100, 70)

        Attributes
        ----------
        rInput: list[mWidget.StaticTextCtrl]

        Notes
        -----
        A valid input must be given for the wx.Dialog to be closed after
        pressing the OK button.
        The number of mWidget.StaticTextCtrl to be created is taken from
        the label parameter.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        title:str,
        label:list[str],
        hint:list[str],
        validator:list[wx.Validator],
        parent:Union[wx.Window, None] = None,
        values:list[str]              = [],
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
            self.rInput.append(cWidget.StaticTextCtrl(
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
        #region ---------------------------------------------------> Variables
        wrong = []
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Validate
        for k in self.rInput:
            if not k.wTc.GetValidator().Validate()[0]:
                wrong.append(k)
                k.wTc.SetValue('')
        #endregion -------------------------------------------------> Validate

        #region ---------------------------------------------------> Return
        if not wrong:
            self.EndModal(1)
            self.Close()
            return True
        #------------------------------>
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


class MultipleCheckBox(BaseDialogOkCancel):
    """Present multiple choices as checkboxes.

        Parameters
        ----------
        title: str
            Title for the wx.Dialog.
        items: dict
            Keys are the name of the wx.CheckBox and values the label.
            Keys are also used to return the checked elements.
        nCol: int
            wx.CheckBox will be distributed in a grid of nCol and as many as
            needed rows.
        label: str
            Label for the wx.StaticBox.
        multiChoice: bool
            More than one wx.Checkbox can be selected (True) or not (False).
        parent: wx.Window
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
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        title:str,
        items:list[dict[str, str]],
        nCol:list[int],
        label:list[str]            = ['Options'],
        multiChoice:list[bool]     = [False],
        parent:Optional[wx.Window] = None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rDict    = {}
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
                    [x.Bind(wx.EVT_CHECKBOX, self.OnCheck) for x in self.rDict[k]['checkB']] # pylint: disable=expression-not-assigned
                else:
                    pass
        except IndexError as e:
            msg = ('items, nCol, label and multiChoice must have the same '
                   'number of elements.')
            raise ValueError(msg) from e
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
            group = int(tCheck.GetName().split('-')[1])
            #------------------------------>
            [k.SetValue(False) for k in self.rDict[group]['checkB']]            # pylint: disable=expression-not-assigned
            #------------------------------>
            tCheck.SetValue(True)
        #endregion -------------------------------------------------> Deselect

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
        #------------------------------>
        for k in self.rDict:
            for c in self.rDict[k]['checkB']:
                if c.IsChecked():
                    self.rChecked[k] = c.GetName().split('-')[0]
        #------------------------------>
        if self.rChecked and len(self.rChecked) == len(self.rDict):
            self.EndModal(1)
            self.Close()
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
#endregion ----------------------------------------------------------> Dialogs

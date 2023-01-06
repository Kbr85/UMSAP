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


"""Bases Windows for the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Optional, Union, Literal

import pandas as pd

import wx
from wx import aui

from config.config import config as mConfig
from core   import method as cMethod
from core   import tab    as cTab
from core   import widget as cWidget
from core   import pane   as cPane
from core   import file   as cFile
from result import file   as resFile
from data   import window as dataWindow
#endregion ----------------------------------------------------------> Imports


LIT_Notification = Literal['errorF', 'errorU', 'warning', 'success', 'question']
LIT_FSelect      = Literal['openO', 'openM', 'save']


#region --------------------------------------------------------------> Frames
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default None.

        Attributes
        ----------
        dKeyMethod : dict
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
    def OnClose(self, event: wx.CloseEvent) -> bool:                            # pylint: disable=unused-argument
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
        rData: dict
            Keys are the elements in rDate and values the analysis data.
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
        self.rDate  = getattr(self, 'rDate', [])
        self.rDateC = getattr(self, 'rDateC', '')
        self.rData  = getattr(self, 'rData', {})
        self.rDf    = getattr(self, 'rDf', pd.DataFrame())
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
        self.cParent.UnCheckSection(self.cSection, self) # type: ignore
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
        if not len(self.rData.keys()) > 1:
            msg = (f'All {self.cSection} in file {self.rObj.rFileP.name} are '  # type: ignore
                f'corrupted or were not found.')
            raise ValueError(msg)
        #endregion ------------------------------------------> Nothing to Plot

        #region -------------------------------------------------> Some Errors
        if self.rData['Error']:
            #------------------------------>
            fileList = '\n'.join(self.rData['Error'])
            #------------------------------>
            if len(self.rData['Error']) == 1:
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
            p = Path(dlg.GetPath())
            tDF = self.rData[self.rDateC]['DF'] if df is None else df
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
        else:
            pass
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

    def CheckDataPrep(self, tDate: str) -> bool:                                # pylint: disable=unused-argument
        """Launch the Check Data Preparation Window.

            Parameters
            ----------
            tDate: str
                Date + ID to find the analysis in the umsap file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            dataWindow.ResDataPrep(
                self,
                f'{self.GetTitle()} - {mConfig.data.nUtil}',
                tSection = self.cSection,
                tDate    = self.rDateC,
            )
        except Exception as e:
            Notification(
                'errorU',
                msg        = 'Data Preparation window failed to launch.',
                tException = e,
                parent     = self,
            )
            return False
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
        #region ---------------------------------------------------> Fill dict
        date = [x for x in self.rData if x != 'Error']
        #endregion ------------------------------------------------> Fill dict

        return (date, {'MenuDate':date})
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseWindowResultOnePlot(BaseWindowResult):
    """Base class for windows showing results.

        Parameters
        ----------
        parent : wx.Window or None
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
    def OnSearch(self, event: wx.Event) -> bool:                                # pylint: disable=unused-argument
        """Search for a given string in the wx.ListCtrl.

            Parameters
            ----------
            event:wx.Event
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

    def OnListSelect(self, event: Union[wx.CommandEvent, str]) -> bool:         # pylint: disable=unused-argument
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
        if idx < 0 and self.rLCIdx is not None:
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
        return True
    #---

    def UpdateUMSAPData(self) -> bool:
        """Update the window after the UMSAP file have been updated.

            Parameters
            ----------


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
    #endregion ------------------------------------------------> Class Methods
#---


class BaseWindowResultListTextNPlot(BaseWindowResultListText):
    """Base window for results with a wx.ListCtrl, wx.TextCtrl and mPane.NPlots.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. Default None.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
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
            self, self.cLNPlot, self.cNPlotCol, statusbar=self.wStatBar)
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
        return True
    #---

    def OnCancel(self, event: wx.CommandEvent) -> bool:                         # pylint: disable=unused-argument
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
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
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
        mode : str
            One of 'errorF', 'errorU', 'warning', 'success', 'question'
        msg : str
            General message to place below the Notification type. This cannot be
            copied by the user.
        tException : str, Exception or None
            The message and traceback to place in the wx.TextCtrl. This
            can be copied by the user. If str then only an error message will
            be placed in the wx.TextCtrl.
        parent : wx widget or None
            Parent of the dialog.
        button : int
            Kind of buttons to show. 1 is wx.OK else wx.OK|wx.CANCEL
        setText : bool
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
    cName = mConfig.core.ndResControlExp
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
        super().__init__(title=self.cName, parent=mConfig.main.mainWin)
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
        #region --------------------------------------------------->
        if self.wConf.wConf.OnOK():
            self.EndModal(1)
            self.Close()
        else:
            pass
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
#endregion ----------------------------------------------------------> Dialogs

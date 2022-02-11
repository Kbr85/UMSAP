# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


"""Main windows and dialogs of the App """


#region -------------------------------------------------------------> Imports
import _thread
from pathlib import Path
from typing import Optional, Literal

import matplotlib as mpl
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import requests
from scipy import stats

import wx
import wx.adv as adv
import wx.lib.agw.aui as aui
import wx.lib.agw.customtreectrl as wxCT

import dat4s_core.data.check as dtsCheck
import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.data.statistic as dtsStatistic
import dat4s_core.generator.generator as dtsGenerator
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
import data.file as file
import data.method as dmethod
import gui.dtscore as dtscore
import gui.menu as menu
import gui.method as method
import gui.pane as pane
import gui.tab as tab
import gui.window as window
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def UpdateCheck(
    ori: Literal['menu', 'main'], win: Optional[wx.Window]=None
    ) -> bool:
    """ Check for updates for UMSAP from another thread.
        
        Parameters
        ----------
        ori: str
            Origin of the request, 'menu' or 'main'
        win : wx widget
            To center the result window in this widget
            
        Return
        ------
        bool
    """
    #region ---------------------------------> Get web page text from Internet
    try:
        r = requests.get(config.urlUpdate)
    except Exception as e:
        msg = 'Check for Updates failed. Please try again later.'
        wx.CallAfter(dtscore.Notification, 'errorU', msg=msg, tException=e)
        return False
    #endregion ------------------------------> Get web page text from Internet
    
    #region --------------------------------------------> Get Internet version
    if r.status_code == requests.codes.ok:
        #------------------------------> 
        text = r.text.split('\n')
        #------------------------------>
        versionI = ''
        for i in text:
            if '<h1>UMSAP' in i:
                versionI = i
                break
            else:
                pass
        #------------------------------> 
        versionI = versionI.split('UMSAP')[1].split('</h1>')[0]
        versionI = versionI.strip()
    else:
        msg = 'Check for Updates failed. Please try again later.'
        wx.CallAfter(dtscore.Notification, 'errorU', msg=msg)
        return False
    #endregion -----------------------------------------> Get Internet version

    #region -----------------------------------------------> Compare & message
    #------------------------------> Compare
    updateAvail = dtsCheck.VersionCompare(versionI, config.version)[0]
    #------------------------------> Message
    if updateAvail:
        wx.CallAfter(CheckUpdateResult, cParent=win, cCheckRes=versionI)
    elif not updateAvail and ori == 'menu':
        wx.CallAfter(CheckUpdateResult, cParent=win, cCheckRes=None)
    else:
        pass
    #endregion --------------------------------------------> Compare & message
    
    return True
#---
#endregion ----------------------------------------------------------> Methods


#region --------------------------------------------------------> Base Classes
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        cParent : wx.Window or None
            Parent of the window
        cMenuData : dict
            Data to build the Tool menu of the window. See structure in child 
            class.
            
        Attributes
        ----------
        dKeyMethod : dict
            Keys are str and values classes or methods. Use in SavePlot. etc.
    """
    #region -----------------------------------------------------> Class setup
    cSDeltaWin = config.deltaWin
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: Optional[wx.Window]=None, cMenuData: Optional[dict]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = cParent
        #------------------------------> Def values if not given in child class
        self.cName    = getattr(self, 'cName',    config.nDefName)
        self.cSWindow = getattr(self, 'cSWindow', config.sWinRegular)
        self.cTitle = getattr(
            self, 'cTitle', config.t.get(self.cName, config.tdW))
        self.cMsgExportFailed = getattr(
            self, 'cMsgExportFailed', config.mDataExport)
        #------------------------------> 
        self.dKeyMethod = {
            #------------------------------> Save Plot Images
            'PlotImageOne': self.OnPlotSaveImageOne,
            'AllImg'      : self.OnPlotSaveAllImage,
            #------------------------------> Reset Zoom Level
            'PlotZoomResetOne': self.OnPlotZoomResetOne,
            'AllZoom'         : self.OnPlotZoomResetAll,
        }
        #------------------------------> 
        super().__init__(
            cParent, size=self.cSWindow, title=self.cTitle, name=self.cName,
        )
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------------------> Widgets
        self.wStatBar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.mBar = menu.ToolMenuBar(self.cName, cMenuData)
        self.SetMenuBar(self.mBar)		
        #endregion -----------------------------------------------------> Menu
        
        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Destroy window. Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
                
            Returns
            -------
            bool
        """
        #region -------------------------------------------> Reduce win number
        try:
            config.winNumber[self.cName] -= 1
        except Exception:
            pass
        #endregion ----------------------------------------> Reduce win number
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def OnPlotSaveImageOne(self) -> bool:
        """Save an image of the plot. Override as needed. 
        
            Returns
            -------
            bool
        
            Notes
            -----
            Assumes window has a wPlot attribute (dtsWidget.MatPlotPanel).
        """
        try:
            #------------------------------> 
            self.wPlot.SaveImage(ext=config.elMatPlotSaveI, parent=self)
            #------------------------------> 
            return True
        except Exception as e:
            #------------------------------> 
            dtscore.Notification(
                'errorF', msg=str(e), tException=e, parent=self)
            #------------------------------> 
            return False
    #---
    
    def OnPlotSaveAllImage(self) -> bool:
        """ Export all plots to a pdf image. Override as needed.
        
            Returns
            -------
            bool
        """
        return True	
    #---
    
    def OnPlotZoomResetOne(self) -> bool:
        """Reset the zoom of the plot.
    
            Returns
            -------
            True
            
            Notes
            -----
            It is assumed the wPlot is in self.wPlot (dtsWidget.MatPlotPanel)
        """
        #------------------------------> Try reset
        try:
            self.wPlot.ZoomResetPlot()
        except Exception as e:
            #------------------------------> 
            msg = 'It was not possible to reset the zoom level of the plot.'
            dtsWindow.NotificationDialog(
                'errorU', msg=msg, tException=e, parent=self)
            #------------------------------> 
            return False
        #------------------------------> 
        return True
    #---
    
    def OnPlotZoomResetAll(self) -> bool:
        """Reset the Zoom level of all plots in the window. Override as needed.
    
            Returns
            -------
            bool
        """
        return True
    #---
    
    def OnCheckDataPrep(self, tDate: str) -> bool:
        """Launch the Check Data Preparation Window.
    
            Parameters
            ----------
            tDate: str
                Date + ID to find the analysis in the umsap file.
    
            Returns
            -------
            bool
    
            Raise
            -----
            
        """
        CheckDataPrep(
            self, 
            f'{self.GetTitle()} - {config.nuDataPrep}', 
            tSection = self.cSection,
            tDate    = self.rDateC,
        )
        
        return True
    #---

    def OnDupWin(self) -> bool:
        """Duplicate window. Used by Result windows. Override as needed.
    
            Returns
            -------
            True
        """
        #------------------------------> 
        self.cParent.rWindow[self.cSection].append(
            self.cParent.dPlotMethod[self.cSection](self.cParent)
        )
        #------------------------------> 
        return True
    #---
    
    def OnExportPlotData(self) -> bool:
        """ Export data to a csv file 
        
            Returns
            -------
            bool
        
            Notes
            -----
            It requires child class to define self.rDateC to catch the current
            date being plotted.
        """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.FileSelectDialog('save', config.elData, parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            try:
                dtsFF.WriteDF2CSV(p, self.rData[self.rDateC]['DF'])
            except Exception as e:
                dtscore.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
    
    def OnExportFilteredData(self) -> bool:
        """Export filtered data to a csv file. 
        
            Returns
            -------
            bool
        
            Notes
            -----
            Assumes filtered data is in self.rDf 
        """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.FileSelectDialog('save', config.elData, parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            try:
                dtsFF.WriteDF2CSV(p, self.rDf)
            except Exception as e:
                dtscore.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---	
    #endregion ------------------------------------------------> Event Methods
    
    #region ---------------------------------------------------> Manage Methods
    def WinPos(self) -> dict:
        """Adjust win number and return information about the size of the 
            window.
            
            See Notes below for more details.
            
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
        info = method.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return info
    #---
    
    def PlotTitle(self) -> bool:
        """Set the title of a plot window.
    
            Parameters
            ----------
            
    
            Returns
            -------
            bool
            
            Notes
            -----
            Assumes child class has self.cSection and self.rDateC and the parent
            is an UMSAPControl window
        """
        self.SetTitle(
            f"{self.cParent.cTitle} - {self.cSection} - {self.rDateC}")
        
        return True
    #---
    #endregion ------------------------------------------------> Manage Methods
#---


class BaseWindowPlot(BaseWindow):
    """Base class for windows showing only a plot.

        Parameters
        ----------
        cParent : 'UMSAPControl'
            Parent of the window.
        cMenuData : dict
            Data to build the Tool menu of the window. See structure in child 
            class.
            
        Notes
        -----
        - Method OnSavePlotImage assumes that this window has an attribute
        wPlot (dtsWidget.MatPlotPanel). Override as needed.
        - Method OnClose assumes the parent is an instance of UMSAPControl. 
        Override as needed.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: Optional[wx.Window]=None, 
        cMenuData: Optional[dict]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cSWindow = getattr(self, 'cSWindow', config.sWinPlot)
        #------------------------------> 
        super().__init__(cParent=cParent, cMenuData=cMenuData)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wPlot = dtsWidget.MatPlotPanel(
            self, 
            statusbar    = self.wStatBar,
            statusMethod = self.UpdateStatusBar,
            dpi          = config.general['DPI'],
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer.Add(self.wPlot, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
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
        self.cParent.UnCheckSection(self.cSection, self)		
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class BaseWindowNPlotLT(BaseWindow):
    """Base class to create a window like ProtProfPlot

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default is None.
        menuData : dict or None
            Data to build the Tool menu of the window. Default is None.
            See Child class for more details.
            
        Attributes
        ----------
        dKeyMethod : dict
            Keys are str and values methods to manage the window.

        Notes
        -----
        Child class is expected to define:
        - cLNPlots : list of str
            To id the plots in the window.
        - cNPlotsCol : int
            Number of columns in the wx.FLexGrid to distribute the plots.
        - cLCol : list of str
            Column names in the wx.ListCtrl
        - cSCol : list of int
            Size of the columns in the wx.ListCtrl
        - cHSearch : str
            Hint for the wx.SearchCtrl. The hint will start with 'Search ', 
            independently of the value of cHSearch
        - cTText : str
            Title for the text pane
        - cTList : str
            Title for the wx.ListCtrl pane
        
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: Optional[wx.Window]=None, cMenuData: Optional[dict]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(cParent, cMenuData=cMenuData)
        #------------------------------> 
        dKeyMethod = {
            'PlotZoomResetAllinOne' : self.OnPlotZoomResetAllinOne,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> 
        self.wStatBar.SetFieldsCount(3, config.sbPlot3Fields)
        #------------------------------>  Plot
        self.wPlots = dtsWindow.NPlots(
            self, self.cLNPlots, self.cNPlotsCol, statusbar=self.wStatBar)
        #------------------------------> Text details
        self.wText = wx.TextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.wText.SetFont(config.font['SeqAlign'])
        #------------------------------> wx.ListCtrl
        self.wLC = pane.ListCtrlSearchPlot(
            self, 
            cColLabel = self.cLCol,
            cColSize  = self.cSCol,
            cStyle    = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_SINGLE_SEL, 
            cTcHint   = f'Search {self.cHSearch}'
        )
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.wPlots, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    'Plots'
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

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)
        self.Bind(wx.EVT_SEARCH, self.OnSearch)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    def OnSearch(self, event: wx.Event) -> bool:
        """Search for a given string in the wx.ListCtrl.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
            Returns
            -------
            bool
    
            Notes
            -----
            See dtsWidget.MyListCtrl.Search for more details.
        """
        #region ---------------------------------------------------> Get index
        tStr = self.wLC.wLCS.search.GetValue()
        iEqual, iSimilar = self.wLC.wLCS.lc.Search(tStr)
        #endregion ------------------------------------------------> Get index
        
        #region ----------------------------------------------> Show 1 Results
        if len(iEqual) == 1:
            #------------------------------> 
            self.wLC.wLCS.lc.Select(iEqual[0], on=1)
            self.wLC.wLCS.lc.EnsureVisible(iEqual[0])
            self.wLC.wLCS.lc.SetFocus()
            #------------------------------> 
            return True
        elif len(iSimilar) == 1:
            #------------------------------> 
            self.wLC.wLCS.lc.Select(iSimilar[0], on=1)
            self.wLC.wLCS.lc.EnsureVisible(iSimilar[0])
            self.wLC.wLCS.lc.SetFocus()
            #------------------------------> 
            return True
        else:
            pass
        #endregion -------------------------------------------> Show 1 Results
        
        #region ----------------------------------------------> Show N Results
        msg = (f'The string, {tStr}, was found in multiple rows.')
        tException = (
            f'The row numbers where the string was found are:\n '
            f'{str(iSimilar)[1:-1]}')
        dtscore.Notification(
            'warning', 
            msg        = msg,
            setText    = True,
            tException = tException,
            parent     = self,
        )
        #endregion -------------------------------------------> Show N Results
        
        return True
    #---
    
    def OnListSelect(self, event: wx.CommandEvent) -> bool:
        """What to do after selecting a row in hte wx.ListCtrl. 
            Override as needed
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
    
            Returns
            -------
            bool
        """
        return True
    #---
    
    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Close window and uncheck section in UMSAPFile window. 
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
                
            Notes
            -----
            Assumes self.cParent is an instance of UMSAPControl.
            Override as needed.
        """
        #region -----------------------------------------------> Update parent
        self.cParent.UnCheckSection(self.cSection, self)		
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def OnPlotZoomResetAllinOne(self) -> bool:
        """Reset all the plots in the window.
        
            Returns
            -------
            bool
    
            Notes
            -----
            It is assumed plots are in a dict self.wPlots.dPlot in which
            keys are string and values are instances of dtsWidget.MatPlotPanel
        """
        #region --------------------------------------------------> Reset Zoom
        try:
            for v in self.wPlots.dPlot.values():
                v.ZoomResetPlot()
        except Exception as e:
            #------------------------------> 
            msg = (
                'It was not possible to reset the zoom level of one of the '
                'plots.')
            dtsWindow.NotificationDialog(
                'errorU', msg=msg, tException=e, parent=self)
            #------------------------------> 
            return False
        #endregion -----------------------------------------------> Reset Zoom
    
        return True	
    #---	
    #endregion ------------------------------------------------> Event Methods
#---


class BaseWindowProteolysis(BaseWindow):
    """Base class to create a window like Limited Proteolysis

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default is None.
        menuData : dict or None
            Data to build the Tool menu of the window. Default is None.
            See Child class for more details.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: Optional[wx.Window]=None, cMenuData: Optional[dict]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Labels
        self.cLPaneMain = getattr(self, 'cLPaneMain', 'Protein Fragments')
        self.cLPaneText = getattr(self, 'cLPaneText', 'Selection Details')
        self.cLPaneList = getattr(self, 'cLPaneList', 'Peptide List')
        self.cLPanePlot = getattr(self, 'cLPanePlot', 'Gel Representation')
        self.cLCol      = getattr(self, 'cLCol', ['#', 'Peptides'])
        #------------------------------> 
        self.cGelLineWidth = getattr(self, 'cGelLineWidth', 0.5)
        #------------------------------> Sizes
        self.cSCol = getattr(self, 'cSCol', [45, 100])
        #------------------------------> Hints
        self.cHSearch = getattr(self, 'cHSearch', self.cLPaneList)
        #------------------------------> 
        super().__init__(cParent, cMenuData=cMenuData)
        #------------------------------> 
        dKeyMethod = {
            #------------------------------> Images
            'MainImg'  : self.OnImageMain,
            'BottomImg': self.OnImageBottom,
            #------------------------------> Zoom Reset
            'MainZoom'  : self.OnZoomResetMain,
            'BottomZoom': self.OnZoomResetBottom,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wPlotM = dtsWidget.MatPlotPanel(self, statusbar=self.wStatBar)
        #------------------------------>  Plot
        self.wPlot = dtsWidget.MatPlotPanel(self, statusbar=self.wStatBar)
        #------------------------------> Text details
        self.wText = wx.TextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.wText.SetFont(config.font['SeqAlign'])
        #------------------------------> wx.ListCtrl
        self.wLC = pane.ListCtrlSearchPlot(
            self, 
            cColLabel = self.cLCol,
            cColSize  = self.cSCol,
            cStyle    = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_SINGLE_SEL, 
            cTcHint   = f'Search {self.cHSearch}'
        )
        #------------------------------> 
        self.wStatBar.SetFieldsCount(2, config.sbPlot2Fields)
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.wPlotM, 
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
        
        self._mgr.AddPane( 
            self.wPlot, 
            aui.AuiPaneInfo(
                ).Bottom(
                ).Layer(
                    0
                ).Caption(
                    self.cLPanePlot
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
        
        self._mgr.AddPane( 
            self.wLC, 
            aui.AuiPaneInfo(
                ).Left(
                ).Layer(
                    1    
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

        #region --------------------------------------------------------> Bind
        self.wLC.wLCS.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
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
        self.cParent.UnCheckSection(self.cSection, self)		
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def OnListSelect(self, event: wx.CommandEvent) -> bool:
        """Process a wx.ListCtrl select event.

            Parameters
            ----------
            event:wx.Event
                Information about the event


            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.rPeptide = self.wLC.wLCS.lc.GetItemText(
            self.wLC.wLCS.lc.GetFirstSelected(), col=1)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.ShowPeptideLoc()
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnPlotZoomResetAll(self) -> bool:
        """Reset the zoom of the main and bottom plot.
        
            Returns
            -------
            bool
        """
        self.OnZoomResetMain()
        self.OnZoomResetBottom()
        
        return True
    #---
    
    def OnZoomResetMain(self) -> bool:
        """Reset the Zoom of the Main plot.
        
            Returns
            -------
            bool
        """
        return self.wPlotM.ZoomResetPlot()
    #---
    
    def OnZoomResetBottom(self) -> bool:
        """Reset the Zoom of the Bottom plot.
    
            Returns
            -------
            bool
        """
        return self.wPlot.ZoomResetPlot()
    #---
    
    def OnImageMain(self) -> bool:
        """Save an image of the Main plot. 
        
            Returns
            -------
            bool
        """
        return self.wPlotM.SaveImage(ext=config.elMatPlotSaveI, parent=self)
    #---
    
    def OnImageBottom(self) -> bool:
        """Save an image of the Bottom plot.
    
            Returns
            -------
            bool
        """
        return self.wPlot.SaveImage(ext=config.elMatPlotSaveI, parent=self)
    #---
    #endregion ------------------------------------------------> Event Methods
    
    #region --------------------------------------------------> Manage Methods
    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.rDate list and the menuData dict needed to build the Tool
            menu.

            Returns
            -------
            tuple of list and dict
            The list is a list of str with the dates in the analysis.
            The dict has the following structure:
                {
                    'menudate' : [List of dates],
                }                    
        """
        #region ---------------------------------------------------> Fill dict
        #------------------------------> Variables
        date = []
        menuData = {}
        #------------------------------> Fill 
        for k in self.rData.keys():
            #------------------------------> 
            date.append(k)
            #------------------------------> 
        #------------------------------> 
        menuData['menudate'] = date
        #endregion ------------------------------------------------> Fill dict
        
        return (date, menuData)
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
        self.wLC.wLCS.lc.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old
        
        #region ----------------------------------------------------> Get Data
        col = [self.rDf.columns.get_loc(c) for c in self.rDf.loc[:,self.rIdxP].columns.values]
        data = dtsMethod.DFFilterByColN(self.rDf, col, self.rAlpha, 'le')
        data = data.iloc[:,0:2].reset_index(drop=True)
        data.insert(0, 'kbr', data.index.values.tolist())
        data = data.astype(str)
        data = data.iloc[:,0:2].values.tolist()
        #endregion -------------------------------------------------> Get Data
        
        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.lc.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl
        
        #region ---------------------------------------> Update Protein Number
        self._mgr.GetPane(self.wLC).Caption(f'{self.cLPaneList} ({len(data)})')
        self._mgr.Update()
        #endregion ------------------------------------> Update Protein Number
        
        return True
    #---
    
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
        a = self.rDf.loc[:,self.rIdxSeqNC]
        b = self.rDf.loc[:,self.rIdxP]

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
        else:
            pass
        
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wPlotM.axes.clear()
        self.wPlotM.axes.set_xticks([])
        self.wPlotM.axes.set_yticks([])
        self.wPlotM.axes.tick_params(length=0)
        self.wPlotM.axes.spines['top'].set_visible(False)
        self.wPlotM.axes.spines['right'].set_visible(False)
        self.wPlotM.axes.spines['bottom'].set_visible(False)
        self.wPlotM.axes.spines['left'].set_visible(False)
        self.wPlotM.canvas.draw()
        #endregion ------------------------------------------------> 
        
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
        if self.rProtLoc[0] is not None:
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
            self.wPlotM.axes.add_patch(mpatches.Rectangle(
                (r[0], y-0.2),
                r[1] - r[0],
                0.4,
                edgecolor = 'black',
                facecolor = self.cCNatProt,
            ))
        
        for r in recProt:
            self.wPlotM.axes.add_patch(mpatches.Rectangle(
                (r[0], y-0.2),
                r[1] - r[0],
                0.4,
                edgecolor = 'black',
                facecolor = self.cCRecProt,
            ))
        #endregion ------------------------------------------------> Draw Rect
       
        return True
    #---
    
    def DrawFragments(self, tKeyLabel: dict) -> bool:
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
        nc = len(self.cColor['Spot'])
        #------------------------------> 
        for k,v in enumerate(tKeyLabel, start=1):
            for j,f in enumerate(self.rFragments[v]['Coord']):
                self.rRectsFrag.append(mpatches.Rectangle(
                    (f[0], k-0.2), 
                    (f[1]-f[0]), 
                    0.4,
                    picker    = True,
                    linewidth = self.cGelLineWidth,
                    facecolor = self.cColor['Spot'][(k-1)%nc],
                    edgecolor = 'black',
                    label     = f'{tKeyLabel[v]}.{j}',
                ))
                self.wPlotM.axes.add_patch(self.rRectsFrag[-1])
        #endregion ------------------------------------------------> Fragments
        
        #region -----------------------------------------------------> Protein
        self.DrawProtein(k+1)
        #endregion --------------------------------------------------> Protein
       
        #region --------------------------------------------------------> Draw
        self.wPlotM.ZoomResetSetValues()
        
        self.wPlotM.canvas.draw()
        #endregion -----------------------------------------------------> Draw
        
        #region ---------------------------------------------------> 
        if self.rPeptide is not None:
            self.ShowPeptideLoc()
        else:
            pass
        #endregion ------------------------------------------------> 

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class MainWindow(BaseWindow):
    """Creates the main window of the App.
    
        Parameters
        ----------
        cParent : wx widget or None
            Parent of the main window.
        
        Attributes
        ----------
        dTab: dict
            Methods to create the tabs.
    """
    #region -----------------------------------------------------> Class Setup
    cName = config.nwMain
    
    dTab = { # Keys are the unique names of the tabs
        config.ntStart   : tab.Start,
        config.ntCorrA   : tab.BaseConfTab,
        config.ntDataPrep: tab.BaseConfListTab,
        config.ntLimProt : tab.BaseConfListTab,
        config.ntProtProf: tab.BaseConfListTab,
        config.ntTarProt : tab.BaseConfListTab,
    }
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: Optional[wx.Window]=None) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(cParent=cParent)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> StatusBar fields
        self.wStatBar.SetFieldsCount(2, config.sSbarFieldSizeI)
        self.wStatBar.SetStatusText(f"{config.softwareF} {config.version}", 1)
        #------------------------------> Notebook
        self.wNotebook = aui.auibook.AuiNotebook(
            self,
            agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer.Add(self.wNotebook, 1, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------> Create Start Tab
        self.OnCreateTab(config.ntStart)
        self.wNotebook.SetCloseButton(0, False)
        #endregion -----------------------------------------> Create Start Tab

        #region ---------------------------------------------> Position & Show
        self.Center()
        self.Show()
        #endregion ------------------------------------------> Position & Show

        #region	------------------------------------------------------> Update
        if config.general["checkUpdate"]:
            _thread.start_new_thread(UpdateCheck, ("main", self))
        else:
            pass
        #endregion	--------------------------------------------------> Update

        #region --------------------------------------------------------> Bind
        self.wNotebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class Methods
    #region ---------------------------------------------------> Event methods
    def OnTabClose(self, event: wx.Event) -> bool:
        """Make sure to show the Start Tab if no other tab exists
        
            Parameters
            ----------
            event : wx.aui.Event
                Information about the event
                
            Returns
            -------
            bool
        """
        #------------------------------> Close Tab
        event.Skip()
        #------------------------------> Number of tabs
        pageC = self.wNotebook.GetPageCount() - 1
        #------------------------------> Update tabs & close buttons
        if pageC == 1:
            #------------------------------> Remove close button from Start tab
            if (win := self.FindWindowByName(config.ntStart)) is not None:
                self.wNotebook.SetCloseButton(
                    self.wNotebook.GetPageIndex(win), 
                    False,
                )
            else:
                pass
        elif pageC == 0:
            #------------------------------> Show Start Tab with close button
            self.OnCreateTab(config.ntStart)
            self.wNotebook.SetCloseButton(
                self.wNotebook.GetPageIndex(
                    self.FindWindowByName(config.ntStart)), 
                False,
            )
        else:
            pass
        
        return True
    #---

    def OnCreateTab(self, name: str, dataI: Optional[dict]=None) -> bool:
        """Create a tab.
        
            Parameters
            ----------
            name : str
                One of the values in section Names of config for tabs
            dataI: dict or None
                Initial data for the tab
                
            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Get tab
        win = self.FindWindowByName(name)
        #endregion --------------------------------------------------> Get tab
        
        #region ------------------------------------------> Find/Create & Show
        if win is None:
            #------------------------------> Create tab
            self.wNotebook.AddPage(
                self.dTab[name](self.wNotebook, name, dataI),
                config.t.get(name, config.tdT),
                select = True,
            )
        else:
            #------------------------------> Focus
            self.wNotebook.SetSelection(self.wNotebook.GetPageIndex(win))
            #------------------------------> Initial Data
            win.wConf.SetInitialData(dataI)
        #endregion ---------------------------------------> Find/Create & Show

        #region ---------------------------------------------------> Start Tab
        if self.wNotebook.GetPageCount() > 1:
            winS = self.FindWindowByName(config.ntStart)
            if winS is not None:
                self.wNotebook.SetCloseButton(
                    self.wNotebook.GetPageIndex(winS), 
                    True,
                )
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> Start Tab
        
        return True
    #---

    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Destroy window and set config.winMain to None.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
                
            Returns
            -------
            bool
        """
        #------------------------------> 
        self.Destroy()
        #------------------------------> 
        config.winMain = None
        #------------------------------> 
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class CorrAPlot(BaseWindowPlot):
    """Creates the window showing the results of a correlation analysis.
    
        See Notes below for more details.

        Parameters
        ----------
        cParent : 'UMSAPControl'
            Parent of the window

        Attributes
        ----------
        rBar : Boolean
            Show (True) or not (False) the Colorbar in the plot
        rCmap : Matplotlib cmap
            CMAP to use in the plot
        rCol : str one of 'Name', 'Number'
            Plot column names or numbers
        rData : parent.obj.confData[Section]
            Data for the Correlation Analysis section.
        rDataPlot : pd.DF
            Data to plot and search the values for the wx.StatusBar.
        rDate : [parent.obj.confData[Section].keys()]
            List of dates availables for plotting.
        rDateC : one of rDate
            Current selected date
        rObj : parent.obj
            Pointer to the UMSAPFile object in parent.
        rSelColIdx : list[int]
            Selected columns index in self.rData[self.rDateC]['DF'].
        rSelColName : list[int]
            Selected columns name to plot.            
        rSelColNum : list[int]
            Selected columns numbers to plot.
        
            
        Notes
        -----
        The structure of menuData is:
        {
            'menudate' : [list of dates in the section],
        }
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> To id the window
    cName = config.nwCorrAPlot
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nuCorrA
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.rObj     = cParent.rObj
        self.rData    = self.rObj.dConfigure[self.cSection]()
        self.rDate    = [x for x in self.rData.keys()]
        self.rDateC   = self.rDate[0]
        self.rBar     = None
        self.rNorm    = mpl.colors.Normalize(vmin=-1, vmax=1)
        self.rCmap    = dtsMethod.MatplotLibCmap(
            N   = config.color[self.cSection]['CMAP']['N'],
            c1  = config.color[self.cSection]['CMAP']['c1'],
            c2  = config.color[self.cSection]['CMAP']['c2'],
            c3  = config.color[self.cSection]['CMAP']['c3'],
            bad = config.color[self.cSection]['CMAP']['NA'],
        )
        #------------------------------> 
        self.cParent = cParent
        self.cTitle  = f"{cParent.cTitle} - {self.cSection} - {self.rDateC}"
        #------------------------------> 
        super().__init__(cParent, {'menudate' : self.rDate})
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers

        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ----------------------------------------------------> Position
        self.SetColDetails(self.rDateC)
        self.UpdateDisplayedData(self.rDateC, 'Name', False)
        self.WinPos()
        self.Show()
        #endregion -------------------------------------------------> Position
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #------------------------------> Class methods
    #region ----------------------------------------------------> Event Manage
    def OnZoomReset(self) -> bool:
        """Reset the zoon of the plot comming from the menu item.
    
            Returns
            -------
            bool
        """
        return self.OnZoomResetOne()
    #---
    
    def OnSelectColumns(self) -> bool:
        """Plot only selected columns
    
            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Options
        allCol = []
        for k,c in enumerate(self.rData[self.rDateC]['DF'].columns):
            allCol.append([self.rData[self.rDateC]['NumColList'][k], c])
        
        selCol = []
        for c in self.rSelColIdx:
            selCol.append([
                self.rData[self.rDateC]['NumColList'][c], 
                self.rData[self.rDateC]['DF'].columns[c]])    
        #endregion --------------------------------------------------> Options

        #region -------------------------------------------------> Get New Sel
        #------------------------------> Create the window
        dlg = dtsWindow.ListSelect(
            allCol, 
            config.lLCtrlColNameI, 
            config.sLCtrlColI, 
            tSelOptions = selCol,
            title       = 'Select the columns to show in the correlation plot',            
            tBtnLabel   = 'Add selection',
            color       = config.color['Zebra'],
            tStLabel = ['Columns in the current results', 'Selected columns'],
        )
        #------------------------------> Get the selected values
        if dlg.ShowModal():
            self.rSelColNum  = dlg.wLCtrlO.GetColContent(0)
            self.rSelColIdx  = []
            self.rSelColName = []
            #------------------------------> 
            for k in self.rSelColNum:
                #------------------------------> 
                tIDX = self.rData[self.rDateC]['NumColList'].index(int(k))
                self.rSelColIdx.append(tIDX)
                #------------------------------> 
                self.rSelColName.append(
                    self.rData[self.rDateC]['DF'].columns[tIDX])
            #------------------------------> 
            self.UpdateDisplayedData(self.rDateC, self.rCol, self.rBar)
        else:
            pass
        
        #endregion ----------------------------------------------> Get New Sel
        
        dlg.Destroy()
        return True
    #---
    #endregion -------------------------------------------------> Event Manage

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
    
    def SetColDetails(self, tDate: str) -> bool:
        """"Set the values of self.rSelColX to its default values, all values
            in the analysis.
            
            Returns
            -------
            bool
        """
        self.rSelColName = self.rData[tDate]['DF'].columns.values
        self.rSelColNum  = self.rData[tDate]['NumColList']
        self.rSelColIdx  = [x for x,_ in enumerate(self.rSelColNum)]
        
        return True
    #---
    
    def UpdateDisplayedData(
        self, tDate: str, col: Literal['Name', 'Number'], bar: bool
        ) -> bool:
        """ Plot data from a given date.
        
            Paramenters
            -----------
            tDate : str
                A date in the section e.g. '20210129-094504 - bla'
            col: One of Name or Number
                Set the information to display in the axis
            bar: bool
                Show or not the colorbar
                
            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Update date
        if tDate == self.rDateC:
            pass
        else:
            self.SetColDetails(tDate)
        #------------------------------>     
        self.rDateC = tDate
        self.rCol   = col
        self.rBar   = bar
        #endregion ----------------------------------------------> Update date
        
        #region --------------------------------------------------------> Axis
        self.SetAxis()
        #endregion -----------------------------------------------------> Axis

        #region --------------------------------------------------------> Plot
        #------------------------------> 
        self.rDataPlot = self.rData[self.rDateC]['DF'].iloc[self.rSelColIdx,self.rSelColIdx]
        #------------------------------> 
        self.wPlot.axes.pcolormesh(
            self.rDataPlot, 
            cmap        = self.rCmap,
            vmin        = -1,
            vmax        = 1,
            antialiased = True,
            edgecolors  = 'k',
            lw          = 0.005,
        )
        
        if bar:
            self.wPlot.figure.colorbar(
                mpl.cm.ScalarMappable(norm=self.rNorm, cmap=self.rCmap),
                orientation = 'vertical',
                ax          = self.wPlot.axes,
            )
        else:
            pass
        #endregion -----------------------------------------------------> Plot
        
        #region -------------------------------------------------> Zoom & Draw
        #------------------------------> Zoom Out level
        self.wPlot.ZoomResetSetValues()
        #------------------------------> Draw
        self.wPlot.canvas.draw()
        #endregion ----------------------------------------------> Zoom & Draw 

        #region ---------------------------------------------------> Statusbar
        self.PlotTitle()
        #endregion ------------------------------------------------> Statusbar
        
        return True
    #---

    def SetAxis(self) -> bool:
        """ General details of the plot area 
        
            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot.figure.clear()
        self.wPlot.axes = self.wPlot.figure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear
        
        #region ---------------------------------------------------> Variables
        xlabel    = []
        xticksloc = []
        
        if (tLen := len(self.rSelColIdx)) <= 30:
            step = 1
        elif tLen > 30 and tLen <= 60:
            step = 2
        else:
            step = 3
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Grid
        self.wPlot.axes.grid(True)		
        #endregion -----------------------------------------------------> Grid
        
        #region --------------------------------------------------> Axis range
        self.wPlot.axes.set_xlim(0, tLen)
        self.wPlot.axes.set_ylim(0, tLen) 
        #endregion -----------------------------------------------> Axis range
        
        #region ---------------------------------------------------> Set ticks
        if self.rCol == 'Name':
            for i in range(0, tLen, step):
                xticksloc.append(i + 0.5)		
                xlabel.append(self.rSelColName[i])
        else:
            for i in range(0, tLen, step):
                xticksloc.append(i + 0.5)
                xlabel.append(self.rSelColNum[i])

        self.wPlot.axes.set_xticks(xticksloc)
        self.wPlot.axes.set_xticklabels(xlabel, rotation=90)

        self.wPlot.axes.set_yticks(xticksloc)
        self.wPlot.axes.set_yticklabels(xlabel)
        #endregion ------------------------------------------------> Set ticks
        
        #region -----------------------------------------------> Adjust figure
        self.wPlot.figure.subplots_adjust(bottom=0.13)
        #endregion --------------------------------------------> Adjust figure

        return True
    #---

    def UpdateStatusBar(self, event) -> bool:
        """Update the statusbar info
    
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
            try:
                #------------------------------> Set x,y,z
                x, y = event.xdata, event.ydata
                
                xf = int(x)
                yf = int(y)
                zf = '{:.2f}'.format(self.rDataPlot.iat[yf,xf])
                
                if self.rCol == 'Name':
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
    #endregion -----------------------------------------------> Manage Methods
#---


class ProtProfPlot(BaseWindowNPlotLT):
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
        rCondC : str
            Condiction currently selected.
        rCorrP : bool
            Use corrected P values (True) or not (False). Default is False. 
        rData : dict
            Dict with the configured data for this section from UMSAPFile.
        rDate : list of str
            List of available dates in the section.
        rDateC : str
            Currently seclected date.
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
            List of applied filters. e.g. [['StatusBarText', {kwargs}], ...]
        rGreenP : matplotlib object
            Reference to the green dot shown in the Volcano plot after selecting
            a protein in the wx.ListCtrl.
        rLockScale : str
            Lock plot scale to No, Date or Project.
        rLog10alpha : float
            -log10(alpha) value to plot in the Volcano plot.
        rObj : UMSAPFile
            Refernece to the UMSAPFile object.
        rProtLine : matplotlib object
            Protein line drawn in the FC plot after selecting a protein in the
            wx.ListCtrl.
        rRpC : str
            Currently selected relevant point.
        rShowAll : bool
            Show (True) fcYMax and fcYMin in the FC plot or not (False).
            Default is True.
        rVXRange : list of float
            Min and Max values for the x axis in the Vol plot.
        rVYRange : list of float
            Min and Max values for the y axis in the Vol plot.
        rZScore : float
            Z score as absolut value.
        rZScoreL : str
            Z score value as percent.
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> To id the window
    cName = config.nwProtProf
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nmProtProf
    #------------------------------> Labels
    cLFZscore     = 'Z Score'
    cLFLog2FC     = 'Log2FC'
    cLFPValAbs    = 'P(abs)'
    cLFPValLog    = 'P(p)'
    cLFFCUp       = 'FC Up'
    cLFFCUpL      = 'FC Above 0'
    cLFFCUpAbs    = 'FC Up Abs'
    cLFFCUpAbsL   = 'FC Increases Strictly'
    cLFFCUpMon    = 'FC Up Mon'
    cLFFCUpMonL   = 'FC Increases Monotonically'
    cLFFCDown     = 'FC Down'
    cLFFCDownL    = 'FC Below 0'
    cLFFCDownAbs  = 'FC Down Abs'
    cLFFCDownAbsL = 'FC Decreases Strictly'
    cLFFCDownMon  = 'FC Down Mon'
    cLFFCDownMonL = 'FC Decreases Monotonically'
    cLFFCBoth     = 'FC Up/Down'
    cLFFCBothL    = 'FC Above/Below 0'
    cLFFCBothAbs  = 'FC Up/Down Abs'
    cLFFCBothAbsL = 'FC Increases/Decreases Strictly'
    cLFFCBothMon  = 'FC Up/Down Mon'
    cLFFCBothMonL = 'FC Increases/Decreases Monotonically'
    cLFFCNo       = 'FC No Change'
    cLFDiv        = 'FC Diverge'
    cLCol         = ['#', 'Gene', 'Protein']
    cLFFCDict     = {
        cLFFCUp      : cLFFCUpL,
        cLFFCDown    : cLFFCDownL,
        cLFFCBoth    : cLFFCBothL,
        cLFFCUpAbs   : cLFFCUpAbsL,
        cLFFCDownAbs : cLFFCDownAbsL,
        cLFFCBothAbs : cLFFCBothAbsL,
        cLFFCUpMon   : cLFFCUpMonL,
        cLFFCDownMon : cLFFCDownMonL,
        cLFFCBothMon : cLFFCBothMonL,
    }
    cLFFCMode = {
        'Up'  : cLFFCUp,
        'Down': cLFFCDown,
        'Both': cLFFCBoth,
        'No'  : cLFFCNo,
    }
    #--------------> Id of the plots
    cLNPlots = ['Vol', 'FC']
    #------------------------------> Title
    cTList = 'Protein List'
    cTText = 'Profiling details'
    #------------------------------> Sizes
    cSWindow = config.sWinModPlot
    cSCol    = [45, 70, 100]
    #------------------------------> Hints
    cHSearch = 'Protein List'
    #------------------------------> Other
    cNPlotsCol = 2
    cImgName   = {
        'Vol': '{}-Vol.pdf',
        'FC' : '{}-Evol.pdf',
    }
    #------------------------------> Color
    cColor = config.color[cName]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle       = f"{cParent.cTitle} - {self.cSection}"
        self.rObj         = cParent.rObj
        self.rData        = self.rObj.dConfigure[self.cSection]()
        self.rDf          = None
        self.rLog10alpha  = None
        self.rZScore      = stats.norm.ppf(0.9)
        self.rZScoreL     = '10%'
        self.rDateC       = None
        self.rCondC       = None
        self.rRpC         = None
        self.rGreenP      = None
        self.rCorrP       = False
        self.rShowAll     = True
        self.rAutoFilter  = False
        self.rCI          = None
        self.rFcYMax      = None
        self.rFcYMin      = None
        self.rLockScale   = None
        self.rVXRange     = []
        self.rVYRange     = []
        self.rFcXRange    = []
        self.rFcYRange    = []
        self.rFcXLabel    = []
        self.rProtLine    = []
        self.rFilterList  = []
        self.rDate, cMenuData = self.SetDateMenuDate()
        #------------------------------> 
        super().__init__(cParent, cMenuData=cMenuData)
        #------------------------------> Methods
        dKeyMethod = {
            #------------------------------> Set Range of Plots
            'No'     : self.SetRangeNo,
            'Date'   : self.SetRangeDate,
            'Project': self.SetRangeProject,
            #------------------------------> Get DF for Text Intensities
            config.oControlTypeProtProf['OC']   : self.GetDF4TextInt_OC,
            config.oControlTypeProtProf['OCC']  : self.GetDF4TextInt_OCC,
            config.oControlTypeProtProf['OCR']  : self.GetDF4TextInt_OCR,
            config.oControlTypeProtProf['Ratio']: self.GetDF4TextInt_RatioI,
            #------------------------------> Filter methods
            self.cLFZscore   : self.Filter_ZScore,
            self.cLFLog2FC   : self.Filter_Log2FC,
            self.cLFPValAbs  : self.Filter_PValue,
            self.cLFPValLog  : self.Filter_PValue,
            self.cLFFCUp     : self.Filter_FCChange,
            self.cLFFCDown   : self.Filter_FCChange,
            self.cLFFCBoth   : self.Filter_FCChange,
            self.cLFFCUpAbs  : self.Filter_FCChange,
            self.cLFFCDownAbs: self.Filter_FCChange,
            self.cLFFCBothAbs: self.Filter_FCChange,
            self.cLFFCUpMon  : self.Filter_FCChange,
            self.cLFFCDownMon: self.Filter_FCChange,
            self.cLFFCBothMon: self.Filter_FCChange,
            self.cLFFCNo     : self.Filter_FCNoChange,
            self.cLFDiv      : self.Filter_Divergent,
            #------------------------------> Save Image
            'VolcanoImg': self.OnSaveVolcanoImage,
            'FCImage'   : self.OnSaveFCImage,
            #------------------------------> Zoom Reset
            'VolcanoZoom' : self.OnZoomResetVol,
            'FCZoom'      : self.OnZoomResetFC,
            'AllZoom'     : self.OnPlotZoomResetAllinOne,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        
        #endregion ----------------------------------------------> Aui control

        #region --------------------------------------------------------> Bind
        self.wPlots.dPlot['Vol'].canvas.mpl_connect('pick_event', self.OnPick)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        #------------------------------> 
        self.UpdateDisplayedData(
            self.rDate[0], 
            cMenuData['crp'][self.rDate[0]]['C'][0],
            cMenuData['crp'][self.rDate[0]]['RP'][0],
            self.rCorrP,
            self.rShowAll,
        )
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods    
    #region --------------------------------------------------> Manage Methods
    def StatusBarFilterText(self, text: str) -> bool:
        """Update the StatusBar text
    
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
                    'menudate' : [List of dates],
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
        menuData = {
            'crp' : {},
        }
        #------------------------------> Fill 
        for k in self.rData.keys():
            #------------------------------> 
            date.append(k)
            #------------------------------> 
            menuData['crp'][k] = {
                'C' : self.rObj.rData[self.cSection][k]['CI']['Cond'],
                'RP': self.rObj.rData[self.cSection][k]['CI']['RP']
            }
        #------------------------------> 
        menuData['menudate'] = date
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

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---
    
    def FillListCtrl(self) -> bool:
        """Update the protein list for the given analysis.
    
            Returns
            -------
            bool
            
            Notes
            -----
            Entries are read from self.rDf
        """
        #region --------------------------------------------------> Delete old
        self.wLC.wLCS.lc.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old
        
        #region ----------------------------------------------------> Get Data
        data = self.rDf.iloc[:,0:2]
        data.insert(0, 'kbr', self.rDf.index.values.tolist())
        data = data.astype(str)
        data = data.values.tolist()
        #endregion -------------------------------------------------> Get Data
        
        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.lc.SetNewData(data)
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
    
    def VolDraw(self) -> bool:
        """Create/Update the Volcano plot.
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Axes
        self.VolSetAxis()
        #endregion -----------------------------------------------------> Axes
        
        #region --------------------------------------------------------> Data
        #------------------------------> 
        x = self.rDf.loc[:,[(self.rCondC,self.rRpC,'FC')]]
        #------------------------------> 
        if self.rCorrP:
            y = -np.log10(
                self.rDf.loc[:,[(self.rCondC,self.rRpC,'Pc')]])
        else:
            y = -np.log10(
                self.rDf.loc[:,[(self.rCondC,self.rRpC,'P')]])
        #------------------------------> 
        zFC = self.rDf.loc[:,[(self.rCondC,self.rRpC,'FCz')]]
        zFC = zFC.squeeze().tolist()
        #-------------->  One item series squeeze to float
        zFC = zFC if type(zFC) == list else [zFC]
        #------------------------------> 
        color = dtsMethod.AssignProperty(
            zFC, self.cColor['Vol'], [-self.rZScore, self.rZScore])
        #endregion -----------------------------------------------------> Data
        
        #region --------------------------------------------------------> Plot
        self.wPlots.dPlot['Vol'].axes.scatter(
            x, y, 
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = color,
            picker    = True,
        )
        #------------------------------> Lock Scale or Set it manually
        if self.rVXRange and self.rVYRange:
            self.wPlots.dPlot['Vol'].axes.set_xlim(*self.rVXRange)
            self.wPlots.dPlot['Vol'].axes.set_ylim(*self.rVYRange)
        else:
            self.VolXYRange(x.squeeze(), y.squeeze())
        #------------------------------> Zoom level
        self.wPlots.dPlot['Vol'].ZoomResetSetValues()
        #------------------------------> Show
        self.wPlots.dPlot['Vol'].canvas.draw()
        #endregion -----------------------------------------------------> Plot
        
        #region -------------------------------------> Update selected protein
        self.DrawGreenPoint()
        #endregion ----------------------------------> Update selected protein
    
        return True
    #---
    
    def VolSetAxis(self) -> bool:
        """Set the axis in the volcano plot.
        
            Returns
            -------
            bool
        """
        #------------------------------> Clear
        self.wPlots.dPlot['Vol'].axes.clear()
        #------------------------------> 
        self.wPlots.dPlot['Vol'].axes.grid(True, linestyle=":")
        self.wPlots.dPlot['Vol'].axes.axhline(
            y=self.rLog10alpha, color="black", dashes=(5, 2, 1, 2), alpha=0.5)
        #------------------------------> Labels
        self.wPlots.dPlot['Vol'].axes.set_title(
            f'C: {self.rCondC} RP: {self.rRpC} ' + 'Z$_{score}$: ' + f'{self.rZScoreL}')
        self.wPlots.dPlot['Vol'].axes.set_xlabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        self.wPlots.dPlot['Vol'].axes.set_ylabel(
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
        if (idx := self.wLC.wLCS.lc.GetFirstSelected()) < 0:
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
        self.rGreenP = self.wPlots.dPlot['Vol'].axes.scatter(
            x, y, 
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = self.cColor['VolSel'],
        )
        #------------------------------> Draw
        self.wPlots.dPlot['Vol'].canvas.draw()
        #endregion ---------------------------------------------> Volcano Plot
        
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
            self.wPlots.dPlot['FC'].axes.plot(self.rFcYMax, color=color)
            self.wPlots.dPlot['FC'].axes.plot(self.rFcYMin, color=color)
            #------------------------------> 
            self.wPlots.dPlot['FC'].axes.fill_between(
                x, self.rFcYMax, self.rFcYMin, color=color, alpha=0.2)
        else:
            pass
        #------------------------------> Lock Scale
        if self.rFcXRange and self.rFcYRange:
            self.wPlots.dPlot['FC'].axes.set_xlim(*self.rFcXRange)
            self.wPlots.dPlot['FC'].axes.set_ylim(*self.rFcYRange)
        else:
            xRange, yRange = self.GetFCXYRange(self.rDateC)
            self.wPlots.dPlot['FC'].axes.set_xlim(*xRange)
            self.wPlots.dPlot['FC'].axes.set_ylim(*yRange)
        #------------------------------> Zoom level
        self.wPlots.dPlot['FC'].ZoomResetSetValues()
        #------------------------------> 
        self.wPlots.dPlot['FC'].canvas.draw()
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
        self.wPlots.dPlot['FC'].axes.clear()
        #endregion ----------------------------------------------------> Clear
        
        #region ------------------------------------------------------> Labels
        self.wPlots.dPlot['FC'].axes.grid(True, linestyle=":")
        self.wPlots.dPlot['FC'].axes.set_xlabel(
            'Relevant Points', fontweight="bold")
        self.wPlots.dPlot['FC'].axes.set_ylabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        #endregion ---------------------------------------------------> Labels

        #region ---------------------------------------------------> X - Axis
        self.wPlots.dPlot['FC'].axes.set_xticks(
            range(0, len(self.rFcXLabel), 1))
        self.wPlots.dPlot['FC'].axes.set_xticklabels(self.rFcXLabel)
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
        if (idxl := self.wLC.wLCS.lc.GetFirstSelected()) < 0:
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
            y = self.rDf.loc[self.rDf.index[[idxl]],idx[c,:,'FC']]
            y = [0.0] + y.values.tolist()[0]
            #------------------------------> Errors
            yError = self.rDf.loc[self.rDf.index[[idxl]],idx[c,:,'CI']]
            yError = [0] + yError.values.tolist()[0]
            #------------------------------> Colors
            color = self.cColor['FCLines'][k%colorN]
            #------------------------------> Plot line
            self.rProtLine.append(
                self.wPlots.dPlot['FC'].axes.errorbar(
                    x, y, yerr=yError, color=color, fmt='o-', capsize=5
            ))
            #------------------------------> Legend
            legend.append(mpatches.Patch(color=color, label=c))
        #endregion --------------------------------------------------> FC Plot
        
        #region -------------------------------------------------------> Title
        self.wPlots.dPlot['FC'].axes.set_title(f'Protein {idxl}')
        #endregion ----------------------------------------------------> Title
        
        #region ------------------------------------------------------> Legend
        self.wPlots.dPlot['FC'].axes.legend(handles=legend, loc='upper left')
        #endregion ---------------------------------------------------> Legend
        
        #region --------------------------------------------------------> Draw
        self.wPlots.dPlot['FC'].canvas.draw()
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
        if (idx := self.wLC.wLCS.lc.GetFirstSelected()) < 0:
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
        number = self.wLC.wLCS.lc.GetItemText(idx, col=0)
        gene = self.wLC.wLCS.lc.GetItemText(idx, col=1)
        name = self.wLC.wLCS.lc.GetItemText(idx, col=2)
        self.wText.AppendText(
            f'--> Selected Protein:\n\n#: {number}, Gene: {gene}, '
            f'Protein ID: {name}\n\n'
        )
        #------------------------------> P and FC values
        self.wText.AppendText('--> P and Log2(FC) values:\n\n')
        self.wText.AppendText(self.GetDF4TextPFC(idx).to_string(index=False))
        self.wText.AppendText('\n\n')
        #------------------------------> Ave and st for intensity values
        self.wText.AppendText(
            '--> Intensity values after data preparation:\n\n')
        dfList = self.dKeyMethod[self.rCI['ControlT']](idx)
        for df in dfList:
            self.wText.AppendText(df.to_string(index=False))
            self.wText.AppendText('\n\n')
        #------------------------------> Go back to begining
        self.wText.SetInsertionPoint(0)
        self.Thaw()
        #endregion ------------------------------------------------> Add Text
        
        return True
    #---
    
    def GetDF4Text(
        self, col: list[str], rp: list[str], cond: list[str],
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
        
        #region --------------------------------------------------> Multiindex
        #------------------------------> 
        a = ['']
        b = ['Conditions']
        #------------------------------> 
        for t in rp:
            a = a + nCol * [t]
            b = b + col
        #------------------------------> 
        mInd = pd.MultiIndex.from_arrays([a[:], b[:]])
        #endregion -----------------------------------------------> Multiindex
        
        #region ----------------------------------------------------> Empty DF
        dfo = pd.DataFrame(columns=mInd, index=range(0,len(cond)))
        #endregion -------------------------------------------------> Empty DF
        
        #region ----------------------------------------------------> Add Cond
        dfo.loc[:,idx[:,'Conditions']] = cond
        #endregion -------------------------------------------------> Add Cond
        
        return dfo
    #---
    
    def GetDF4TextPFC(self, pID: int) -> pd.DataFrame:
        """Get the dataframe to print the P and FC +/- CI values to the text.
    
            Parameters
            ----------
            pID : int 
                To select the protein in self.rDf
            
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
            
            See Notes below for more details.
    
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
            
            See Notes below for more details.
    
            Parameters
            ----------
            pID : int 
                To select the protein in self.rDf
            
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
            
            See Notes below for more details.
    
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
            
            See Notes below for more details.
    
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
        self.rFcXRange, self.rFcYRange = self.GetFCXYRange(self.rDateC)
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
        vXLim = 0
        vYMin = 0
        vYMax = 0
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
            xFC, yFC = self.GetFCXYRange(date)
            #------------------------------> 
            vXLim = x[1] if x[1] >= vXLim else vXLim
            vYMin = y[0] if y[0] <= vYMin else vYMin
            vYMax = y[1] if y[1] >= vYMax else vYMax
            
            fcXMin = xFC[0] if xFC[0] <= fcXMin else fcXMin
            fcXMax = xFC[1] if xFC[1] >= fcXMax else fcXMax
            fcYMin = yFC[0] if yFC[0] <= fcYMin else fcYMin
            fcYMax = yFC[1] if yFC[1] >= fcYMax else fcYMax
        #------------------------------> Set attributes
        self.rVXRange = [-vXLim, vXLim]
        self.rVYRange = [vYMin, vYMax]
        
        self.rFcXRange = [fcXMin, fcXMax]
        self.rFcYRange = [fcYMin, fcYMax]
        #endregion ----------------------------------------------------> Range
        
        return True
    #---
    
    def GetVolXYRange(self, date: str) -> list[list[float]]:
        """Get the XY range for the volcano plot for the given date
    
            Parameters
            ----------
            date : str
                A valid date from the project
    
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
        
        y = -np.log10(y)
        #------------------------------> 
        xRange = []
        yRange = []
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Get Range
        #------------------------------> X
        xmin = abs(x.min().min())
        xmax = abs(x.max().max())
        #-------------->  To make it symetric
        if xmin >= xmax:
            lim = xmin
        else:
            lim = xmax
        #--------------> 
        dm = 2 * lim * config.general['MatPlotMargin']
        #--------------> 
        xRange.append(-lim - dm)
        xRange.append(lim + dm)
        #------------------------------> Y
        ymax = y.max().max()
        #--------------> 
        dm = 2 * ymax * config.general['MatPlotMargin']
        #--------------> 
        yRange.append(0 - dm)
        yRange.append(ymax + dm)
        #endregion ------------------------------------------------> Get Range
        
        return [xRange, yRange]
    #---
    
    def GetFCXYRange(self, date: str) -> list[list[float]]:
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
        #--------------> 
        dm = len(self.rCI['RP']) * config.general['MatPlotMargin']
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
        dm = (ymaxLim - yminLim) * config.general['MatPlotMargin']
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
        xR = dtsStatistic.DataRange(x, margin= config.general['MatPlotMargin'])
        yR = dtsStatistic.DataRange(y, margin= config.general['MatPlotMargin'])
        #endregion ------------------------------------------------> Get Range
        
        #region ---------------------------------------------------> Set Range
        self.wPlots.dPlot['Vol'].axes.set_xlim(*xR)
        self.wPlots.dPlot['Vol'].axes.set_ylim(*yR)
        #endregion ------------------------------------------------> Set Range
        
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
    
    #region ---------------------------------------------------> Event Methods
    def UpdateDisplayedData(
        self, tDate: str, cond: str, rp:str, corrP: bool, showAll: bool,
        ) -> bool:
        """Configure window to update Volcano and FC plots when date changes.
    
            Parameters
            ----------
            tDate : str
                Selected date.
            cond : str
                Selected condition
            rp : str
                Selected relevant point
            corrP : bool
                Use corrected P values (True) or not (False)
            showAll : bool
                Show FC rnge of values or not.
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------> Update variables
        self.rDateC   = tDate
        self.rCondC   = cond
        self.rRpC     = rp
        self.rCorrP   = corrP
        self.rShowAll = showAll
        self.rCI      = self.rObj.rData[self.cSection][self.rDateC]['CI']
        self.rDf      = self.rData[self.rDateC]['DF'].copy()
        #endregion -----------------------------------------> Update variables
        
        #region --------------------------------------------------> Update GUI
        if self.rAutoFilter:
            self.FilterApply()
        else:
            pass
        #------------------------------> Clean & Reload Protein List
        self.FillListCtrl()
        #------------------------------> Alpha
        self.rLog10alpha = -np.log10(float(self.rCI['Alpha']))
        #------------------------------> Clean text
        self.wText.SetValue('')
        #endregion -----------------------------------------------> Update GUI
        
        #region -------------------------------------------> Update FC x label
        self.rFcXLabel = self.rCI['ControlL'] + self.rCI['RP']        
        #endregion ----------------------------------------> Update FC x label
        
        #region ---------------------------------------------------> FC minmax
        self.rFcYMax, self.rFcYMin = self.GetFCMinMax()
        #endregion ------------------------------------------------> FC minmax
        
        #region --------------------------------------------------> Lock Scale
        if self.rLockScale is not None:
            self.OnLockScale(self.rLockScale)
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
    
    def OnVolChange(self, cond: str, rp:str, corrP: bool) -> bool:
        """Update the Volcano plot.
    
            Parameters
            ----------
            cond : str
                Selected condition
            rp : str
                Selected relevant point
            corrP : bool
                Use corrected P values (True) or not (False)
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------> Update variables
        self.rCondC   = cond
        self.rRpC     = rp
        self.rCorrP   = corrP
        #endregion -----------------------------------------> Update variables
        
        #region ---------------------------------------------------------> Vol
        self.VolDraw()
        #endregion ------------------------------------------------------> Vol
        
        return True
    #---
    
    def OnFCChange(self, showAll: bool) -> bool:
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
    
    def OnZScore(self) -> bool:
        """Change Z score to plot.
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        dlg = dtsWindow.UserInput1Text(
            'Z score threshold.',
            'Z score threshold (%)',
            'Decimal value between 0 and 100. e.g. 10',
            self.wPlots.dPlot['Vol'],
            dtsValidator.NumberList(
                numType = 'float',
                vMin    = 0,
                vMax    = 100,
                nN      = 1,
            )
        )
        #endregion -------------------------------------------> Text Entry Dlg
        
        #region ------------------------------------------> Get Value and Plot
        if dlg.ShowModal():
            #------------------------------> 
            val = float(dlg.input.tc.GetValue())
            #------------------------------> 
            self.rZScoreL = f'{val}%'
            self.rZScore = stats.norm.ppf(1.0-(val/100.0))
            #------------------------------> 
            self.VolDraw()
        else:
            pass
        #endregion ---------------------------------------> Get Value and Plot
        
        dlg.Destroy()
        return True
    #---
    
    def OnSaveVolcanoImage(self) -> bool:
        """Save an image of the volcano plot.
    
            Returns
            -------
            bool
        """
        return self.wPlots.dPlot['Vol'].SaveImage(
            config.elMatPlotSaveI, parent=self.wPlots.dPlot['Vol']
        )
    #---
    
    def OnSaveFCImage(self) -> bool:
        """Save an image of the volcano plot.
    
            Returns
            -------
            bool
        """
        return self.wPlots.dPlot['FC'].SaveImage(
            config.elMatPlotSaveI, parent=self.wPlots.dPlot['FC']
        )
    #---
    
    def OnPlotSaveAllImage(self) -> bool:
        """ Export all plots to a pdf image
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.DirSelectDialog(parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            try:
                for k, v in self.wPlots.dPlot.items():
                    #------------------------------> file path
                    fPath = p / self.cImgName[k].format(self.rDateC)
                    #------------------------------> Write
                    v.figure.savefig(fPath)
            except Exception as e:
                dtscore.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
    
    def OnPick(self, event) -> bool:
        """Process a pick event in the volcano plot.
    
            Parameters
            ----------
            event: matplotlib pick event
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        ind = event.ind
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Pick
        if len(ind) == 1:
            self.wLC.wLCS.lc.Select(ind[0], on=1)
            self.wLC.wLCS.lc.EnsureVisible(ind[0])
            self.wLC.wLCS.lc.SetFocus()
        else:
            #------------------------------> Disconnect events to avoid zoom in
            # while interacting with the modal window
            self.wPlots.dPlot['Vol'].DisconnectEvent()
            #------------------------------> sort ind
            ind = sorted(ind, key=int)
            #------------------------------> 
            msg = (f'The selected point is an overlap of several proteins.')
            tException = (
                f'The numbers of the proteins included in the selected '
                f'point are:\n {str(ind)[1:-1]}')
            dtscore.Notification(
                'warning', 
                msg        = msg,
                setText    = True,
                tException = tException,
                parent     = self.wPlots.dPlot['Vol'],
            )
            #------------------------------> Reconnect event
            self.wPlots.dPlot['Vol'].ConnectEvent()
            return False
        #endregion ------------------------------------------------> Pick
        
        return True
    #---
    
    def OnListSelect(self, event) -> bool:
        """Select an element in the wx.ListCtrl.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
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
    
    def OnZoomResetVol(self) -> bool:
        """Reset the zoom level in the Volcano plot.
        
            Returns
            -------
            bool
        """
        return self.wPlots.dPlot['Vol'].ZoomResetPlot()
    #---
    
    def OnZoomResetFC(self) -> bool:
        """Reset the zoom level in the FC plot.
    
            Returns
            -------
            bool
        """
        return self.wPlots.dPlot['FC'].ZoomResetPlot()
    #---
    
    def OnLockScale(self, mode: str, updatePlot: bool=True) -> bool:
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
        self.dKeyMethod[mode]()
        #endregion ------------------------------------------------> Get Range
        
        #region ---------------------------------------------------> Set Range
        if updatePlot:
            #------------------------------> Vol
            #--------------> 
            self.wPlots.dPlot['Vol'].axes.set_xlim(*self.rVXRange)
            self.wPlots.dPlot['Vol'].axes.set_ylim(*self.rVYRange)
            #--------------> 
            self.wPlots.dPlot['Vol'].canvas.draw()
            #--------------> 
            self.wPlots.dPlot['Vol'].ZoomResetSetValues()
            #------------------------------> FC
            #--------------> 
            self.wPlots.dPlot['FC'].axes.set_xlim(*self.rFcXRange)
            self.wPlots.dPlot['FC'].axes.set_ylim(*self.rFcYRange)
            #--------------> 
            self.wPlots.dPlot['FC'].canvas.draw()
            #--------------> 
            self.wPlots.dPlot['FC'].ZoomResetSetValues()
        else:
            pass    
        #endregion ------------------------------------------------> Set Range
        
        return True
    #---
    
    def OnAutoFilter(self, mode: bool) -> bool:
        """Auto apply filter when changing date.
    
            Parameters
            ----------
            mode : bool
                Apply filters (True) or not (False).
    
            Returns
            -------
            bool
    
            Raise
            -----
            
        """
        self.rAutoFilter = mode
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Filter Methods
    def FilterApply(self) -> bool:
        """Apply all filter to the current date.
    
            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Apply Filters
        for k in self.rFilterList:
            self.dKeyMethod[k[0]](**k[1])
        #endregion --------------------------------------------> Apply Filters
        
        return True
    #---
    
    def FilterRemoveAll(self) -> bool:
        """Remove all filter.
    
            Returns
            -------
            bool
        """
        #region -------------------------------------------> Update Attributes
        self.rFilterList = []
        self.rDf = self.rData[self.rDateC]['DF'].copy()
        self.wStatBar.SetStatusText('', 1)
        #endregion ----------------------------------------> Update Attributes
        
        #region --------------------------------------------------> Update GUI
        self.UpdateDisplayedData(
            self.rDateC, self.rCondC, self.rRpC, self.rCorrP, self.rShowAll)
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
        #------------------------------> 
        del self.rFilterList[-1]
        self.rDf = self.rData[self.rDateC]['DF'].copy()
        #------------------------------> 
        text = self.wStatBar.GetStatusText(1)
        text = text.split("|")[0:-1]
        text = [x.strip() for x in text if x.strip() != '']
        if text:
            text = f' | {" | ".join(text)}'
        else:
            text = ''
        self.wStatBar.SetStatusText(text, 1)
        #endregion ----------------------------------------> Update Attributes
        
        #region --------------------------------------------------> Update GUI
        self.UpdateDisplayedData(
            self.rDateC, self.rCondC, self.rRpC, self.rCorrP, self.rShowAll)
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
        dlg = window.FilterRemoveAny(self.rFilterList, self.wPlots.dPlot['Vol'])
        if dlg.ShowModal():
            #------------------------------> 
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
        text = ''
        #------------------------------> 
        for k in reversed(lo):
            del self.rFilterList[k]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------> Update GUI
        if self.rFilterList:
            #------------------------------> 
            self.rDf = self.rData[self.rDateC]['DF'].copy()
            #------------------------------> 
            self.FilterApply()
            #------------------------------> 
            for k in self.rFilterList:
                #------------------------------> 
                gText = k[1].get("gText", "")
                #------------------------------> 
                if gText:
                    text = f'{text} | {k[0]} {gText}'
                else:
                    text = f'{text} | {k[0]}'
            #------------------------------> 
            self.wStatBar.SetStatusText(text, 1)
        else:
            self.FilterRemoveAll()
        #endregion -----------------------------------------------> Update GUI
        
        return True
    #---
    
    def Filter_ZScore(
        self, gText: Optional[str]=None, updateL: bool=True
        ) -> bool:
        """Filter results by Z score.
    
            Parameters
            ----------
            gText : str
                Z score threshold and operand, e.g. < 10 or > 3.4
            updateL : bool
                Update filterList and StatusBar (True) or not (False)
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Text Entry Dlg
        if gText is None:
            #------------------------------> 
            dlg = dtsWindow.UserInput1Text(
                'Filter results by Z score.',
                'Threshold (%)',
                'Decimal value between 0 and 100. e.g. < 10.0 or > 20.4',
                self.wPlots.dPlot['Vol'],
                dtsValidator.Comparison(
                    numType='float', vMin=0, vMax=100, op=['<', '>']
                ),
            )
            #------------------------------> 
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.input.tc.GetValue()
                #------------------------------> 
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        else:
            try:
                #------------------------------> 
                a, b = dtsCheck.Comparison(
                    gText, 'int', vMin=0, vMax=100, op=['<', '>'])
                #------------------------------> 
                if a:
                    uText = gText
                else:
                    #------------------------------> 
                    msg = 'It was not possible to apply the Z Score filter.'
                    tException = b[2]
                    #------------------------------> 
                    dtsWindow.NotificationDialog(
                        'errorU', 
                        msg        = msg,
                        tException = tException,
                        parent     = self,
                        setText    = True,
                    )
                    #------------------------------> 
                    return False
            except Exception as e:
                raise e
        #endregion -------------------------------------------> Text Entry Dlg
        
        #region ------------------------------------------> Get Value and Plot
        op, val = uText.strip().split()
        zVal = stats.norm.ppf(1.0-(float(val.strip())/100.0))
        #------------------------------> 
        idx = pd.IndexSlice
        col = idx[:,:,'FCz']
        if op == '<':
            self.rDf = self.rDf[(
                (self.rDf.loc[:,col] >= zVal) | (self.rDf.loc[:,col] <= -zVal)
            ).any(axis=1)]
        else:
            self.rDf = self.rDf[(
                (self.rDf.loc[:,col] <= zVal) | (self.rDf.loc[:,col] >= -zVal)
            ).any(axis=1)]
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #endregion ---------------------------------------> Get Value and Plot
        
        #region ------------------------------------------> Update Filter List
        if updateL:
            #------------------------------> 
            self.StatusBarFilterText(f'{self.cLFZscore} {op} {val}')
            #------------------------------> 
            self.rFilterList.append(
                [self.cLFZscore, {'gText': uText, 'updateL': False}]
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List
        
        return True
    #---
    
    def Filter_Log2FC(
        self, gText: Optional[str]=None, updateL: bool=True) -> bool:
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
        if gText is None:
            #------------------------------> 
            dlg = dtsWindow.UserInput1Text(
                'Filter results by Log2(FC) value.',
                'Threshold',
                'Absolute log2(FC) value. e.g. < 2.3 or > 3.5',
                self.wPlots.dPlot['Vol'],
                dtsValidator.Comparison(numType='float', op=['<', '>'], vMin=0),
            )
            #------------------------------> 
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.input.tc.GetValue()
                #------------------------------> 
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        else:
            try:
                #------------------------------> 
                a, b = dtsCheck.Comparison(
                    gText, numType='float', op=['<', '>'], vMin=0)
                #------------------------------> 
                if a:
                    uText = gText
                else:
                    #------------------------------> 
                    msg = 'It was not possible to apply the Log2FC filter.'
                    tException = b[2]
                    #------------------------------> 
                    dtsWindow.NotificationDialog(
                        'errorU', 
                        msg        = msg,
                        tException = tException,
                        parent     = self,
                        setText    = True,
                    )
                    #------------------------------> 
                    return False
            except Exception as e:
                raise e
        #endregion -------------------------------------------> Text Entry Dlg
        
        #region ------------------------------------------> Get Value and Plot
        op, val = uText.strip().split()
        val = float(val)
        #------------------------------> 
        idx = pd.IndexSlice
        col = idx[:,:,'FC']
        if op == '<':
            self.rDf = self.rDf[(
                (self.rDf.loc[:,col] <= val) & (self.rDf.loc[:,col] >= -val)
            ).any(axis=1)]
        else:
            self.rDf = self.rDf[(
                (self.rDf.loc[:,col] >= val) | (self.rDf.loc[:,col] <= -val)
            ).any(axis=1)]
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #endregion ---------------------------------------> Get Value and Plot
        
        #region ------------------------------------------> Update Filter List
        if updateL:
            #------------------------------> 
            self.StatusBarFilterText(f'{self.cLFLog2FC} {op} {val}')
            #------------------------------> 
            self.rFilterList.append(
                [self.cLFLog2FC, {'gText': uText, 'updateL': False}]
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List
        
        return True
    #---
    
    def Filter_PValue(
        self, gText: Optional[str]=None, absB: Optional[bool]=None, 
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
        if gText is None:
            #------------------------------> 
            dlg = window.FilterPValue(
                'Filter results by P value.',
                'Threshold',
                'Absolute or -log10(P) value. e.g. < 0.01 or > 1',
                self.wPlots.dPlot['Vol'],
                dtsValidator.Comparison(numType='float', op=['<', '>'], vMin=0),
            )
            #------------------------------> 
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.input.tc.GetValue()
                absB  = dlg.wCbAbs.IsChecked()
                #------------------------------> 
                dlg.Destroy()
            else:
                dlg.Destroy()
                return True
        else:
            try:
                #------------------------------> 
                a, b = dtsCheck.Comparison(
                    gText, numType='float', op=['<', '>'], vMin=0)
                #------------------------------> 
                if a:
                    uText = gText
                else:
                    #------------------------------> 
                    msg = 'It was not possible to apply the P value filter.'
                    tException = b[2]
                    #------------------------------> 
                    dtsWindow.NotificationDialog(
                        'errorU', 
                        msg        = msg,
                        tException = tException,
                        parent     = self,
                        setText    = True,
                    )
                    #------------------------------> 
                    return False
            except Exception as e:
                raise e
        #endregion -------------------------------------------> Text Entry Dlg
        
        #region ------------------------------------------> Get Value and Plot
        op, val = uText.strip().split()
        val = float(val)
        #------------------------------> Apply to regular or corrected P values
        idx = pd.IndexSlice
        if self.rCorrP:
            col = idx[:,:,'Pc']
        else:
            col = idx[:,:,'P']
        #------------------------------> Given value is abs or -log10 P value
        df = self.rDf.copy()
        if absB:
            pass
        else:
            df.loc[:,col] = -np.log10(df.loc[:,col])
        #------------------------------> 
        if op == '<':
            self.rDf = self.rDf[(df.loc[:,col] <= val).any(axis=1)]
        else:
            self.rDf = self.rDf[(df.loc[:,col] >= val).any(axis=1)]
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #endregion ---------------------------------------> Get Value and Plot
        
        #region ------------------------------> Update Filter List & StatusBar
        if updateL:
            #------------------------------> 
            label = self.cLFPValAbs if absB else self.cLFPValLog
            #------------------------------> 
            self.StatusBarFilterText(f'{label} {op} {val}')
            #------------------------------> 
            self.rFilterList.append(
                [label, {'gText': uText, 'absB': absB, 'updateL': False}]
            )
        else:
            pass
        #endregion ---------------------------> Update Filter List & StatusBar
        
        return True
    #---
    
    def Filter_FCNoChange(self, updateL: bool=True) -> bool:
        """Filter results by No FC change.
    
            Parameters
            ----------
            updateL : bool
                Update filterList and StatusBar (True) or not (False)
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------------------> DF
        idx = pd.IndexSlice
        df = self.rDf.loc[:,idx[:,:,'FC']]
        #endregion -------------------------------------------------------> DF
        
        #region ------------------------------------------> Get Value and Plot
        self.rDf = self.rDf[df.apply(
            lambda x: any([(x.loc[idx[y,:,'FC']] == 0).all() for y in self.rCI['Cond']]), axis=1
        )]
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #endregion ---------------------------------------> Get Value and Plot
        
        #region ------------------------------------------> Update Filter List
        if updateL:
            #------------------------------> 
            self.StatusBarFilterText(f'{self.cLFFCNo}')
            #------------------------------> 
            self.rFilterList.append(
                [self.cLFFCNo, {'updateL': False}]
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List
        
        return True
    #---
    
    def Filter_FCChange(
        self, choice: Optional[str]=None, updateL: bool=True,
        ) -> bool:
        """Filter results based on FC change
    
            Parameters
            ----------
            choice : str
                One of the keys in self.cLFFCDict
            updateL : bool
                Update filterList and StatusBar (True) or not (False)
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Get Value
        if choice is None:
            #------------------------------> 
            dlg = dtsWindow.MultipleCheckBox(
                'Filter results by FC evolution.', 
                self.cLFFCDict, 
                3, 
                parent=self.wPlots.dPlot['FC'],
            )
            #------------------------------> 
            if dlg.ShowModal():
                #------------------------------> 
                choice = dlg.GetChoice()[0]
                #------------------------------> 
                dlg.Destroy()
            else:
                dlg.Destroy()
                return False
        else:
            pass
        #endregion ------------------------------------------------> Get Value
        
        #region ----------------------------------------------------------> DF
        #------------------------------> 
        idx = pd.IndexSlice
        df = self.rDf.loc[:,idx[:,:,'FC']]
        #------------------------------> 
        if choice == self.cLFFCUp:
            self.rDf = self.rDf[df.apply(
                lambda x: any([(x.loc[idx[y,:,'FC']] > 0).all() for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCUpAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any([np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) > 0) for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCUpMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any([x.loc[idx[['C',y],:,'FC']].is_monotonic_increasing for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDown:
            self.rDf = self.rDf[df.apply(
                lambda x: any([(x.loc[idx[y,:,'FC']] < 0).all() for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDownAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any([np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) < 0) for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDownMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any([x.loc[idx[['C',y],:,'FC']].is_monotonic_decreasing for y in self.rCI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCBoth:
            self.rDf = self.rDf[df.apply(
                lambda x: any(
                    [(x.loc[idx[y:,:'FC']] > 0).all() for y in self.rCI['Cond']] + 
                    [(x.loc[idx[y:,:'FC']] < 0).all() for y in self.rCI['Cond']]
                ), 
                axis=1,
            )]
        elif choice == self.cLFFCBothAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any(
                    [np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) > 0) for y in self.rCI['Cond']] + 
                    [np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) < 0) for y in self.rCI['Cond']]
                ), 
                axis=1,
            )]
        elif choice == self.cLFFCBothMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.rDf = self.rDf[df.apply(
                lambda x: any(
                    [x.loc[idx[['C',y],:,'FC']].is_monotonic_increasing for y in self.rCI['Cond']] +
                    [x.loc[idx[['C',y],:,'FC']].is_monotonic_decreasing for y in self.rCI['Cond']] 
                ), 
                axis=1,
            )]
        else:
            return False
        #endregion -------------------------------------------------------> DF
    
        #region --------------------------------------------------> Update GUI
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #------------------------------> 
        if updateL:
            #------------------------------> 
            self.StatusBarFilterText(f'{choice}')
            #------------------------------> 
            self.rFilterList.append(
                [choice, {'choice':choice, 'updateL': False}]
            )
        else:
            pass
        #endregion -----------------------------------------------> Update GUI
            
        return True
    #---
        
    def Filter_Divergent(self, updateL: bool=True) -> bool:
        """Filter results based on the simultaneous presence of a increasing and 
            decreasing FC behavior in the conditions.
    
            Parameters
            ----------
            updateL : bool
                Update filterList and StatusBar (True) or not (False)
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------------------> DF
        idx = pd.IndexSlice
        df = self.rDf.loc[:,idx[:,:,'FC']]
        #endregion -------------------------------------------------------> DF
        
        #region ------------------------------------------> Get Value and Plot
        self.rDf = self.rDf[df.apply(self.Filter_Divergent_Helper, axis=1)]
        #------------------------------> 
        self.FillListCtrl()
        self.VolDraw()
        self.FCDraw()
        #endregion ---------------------------------------> Get Value and Plot
        
        #region ------------------------------------------> Update Filter List
        if updateL:
            #------------------------------> 
            self.StatusBarFilterText(f'{self.cLFDiv}')
            #------------------------------> 
            self.rFilterList.append(
                [self.cLFDiv, {'updateL': False}]
            )
        else:
            pass
        #endregion ---------------------------------------> Update Filter List
        
        return True
    #---
    
    def Filter_Divergent_Helper(self, x: pd.Series) -> bool:
        """Determine whether x shows divergent behavior
    
            Parameters
            ----------
            x : pd.Series
                Row in self.rDf
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        idx = pd.IndexSlice
        res = []
        #endregion ------------------------------------------------> Variables
        
        #region -----------------------------------------------------> Compare
        for y in self.rCI['Cond']:
            if (x.loc[idx[y,:,'FC']] > 0).all():
                res.append(True)
            elif (x.loc[idx[y,:,'FC']] == 0).all():
                res.append(None)
            elif (x.loc[idx[y,:,'FC']] < 0).all():    
                res.append(False)
            else:
                pass
        #endregion --------------------------------------------------> Compare
        
        #region ---------------------------------------------------------> Set 
        resS = set(res)
        if resS and len(resS) > 1:
            return True
        else:
            return False
        #endregion ------------------------------------------------------> Set 
    #---
    #endregion -----------------------------------------------> Filter Methods
#---


class LimProtPlot(BaseWindowProteolysis):
    """Plot the results of a Limited Proteolysis analysis.

        Parameters
        ----------
        cParent: wx.Window
            Parent of the window

        Attributes
        ----------
        dClearMethod: dict
            Methods to clear the selections in the window.
        rAlpha: float
            Significance level of the analysis
        rBands: list[str]
            Label for the bands
        rBlSelC: list[int, int]
            Coordinates for the Band/Lane selected from 1 to N
        rBlSelRect: mpatch
            Rectangle used to highlight the selected Band/Lane
        rData: dict
            Data for the Limited Proteolysis section of the UMSAP File.
        rDate: list[str]
            Avalaible dates.
        rDateC: str
            Currently selected date.
        rDf: pd.DataFrame
            Copy of the data used to plot
        rFragments: dict
            Dict with the info for the fragments. See dmethod.Fragments.
        rFragSelC: list[band, lane, fragment]
            Coordinates for the currently selected fragment. 0 based.
        rFragSelLine: matplotlib line
            Line to highlight the currently selected fragment.
        rGelSelC: list[band, lane]
            Coordinated for the currently selected gel spot. 1 based.
        rGelSpotPicked: bool
            Gel spot was selected (True) or not (False).
        rLanes: list[str]
            Name of the lanes.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPeptide: str
            Sequence of the selected peptide in the wx.ListCtrl.
        rProtDelta: int
            Diference between the residue numbers in the recombinant and native 
            protein.
        rProtLength: int
            Length of hte Recombinant Protein used in the analysis.
        rProtLoc: list[int, int]
            Location of the Native Sequence in the Recombinant Sequence.
        rProtTarget: str
            Name of the Recombinant protein used in the analysis.
        rRectsFrag: list[mpatches]
            Rectangles used in the Fragment plot.
        rRectsGel: list[mpatches]
            Rectangles used in the Gel spot.
        rSelBands: bool
            Select Bands (True) or Lanes (False).
        rSpotSelLine: line
            Line to highlight the selected Gel spot.
        rUpdateColors: bool
            Update Gel colors (True) or not (False).
    """
    #region -----------------------------------------------------> Class setup
    cName = config.nwLimProt
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nmLimProt
    #------------------------------> Colors
    cCNatProt = config.color['NatProt']
    cCRecProt = config.color['RecProt']
    cColor = config.color[cName]
    #------------------------------> 
    rIdxP     = pd.IndexSlice[:,:,'Ptost']
    rIdxSeqNC = pd.IndexSlice[config.dfcolSeqNC,:,:]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle         = f'{cParent.cTitle} - {self.cSection}'
        self.rObj           = cParent.rObj
        self.rData        = self.rObj.dConfigure[self.cSection]()
        self.rDateC         = None
        self.rBands         = None
        self.rLanes         = None
        self.rFragments     = None
        self.rRectsGel      = []
        self.rRectsFrag     = []
        self.rSelBands      = True
        self.rBlSelRect     = None
        self.rSpotSelLine   = None
        self.rFragSelLine   = None
        self.rBlSelC        = [None, None]
        self.rGelSelC       = [None, None]
        self.rFragSelC      = [None, None, None]
        self.rGelSpotPicked = False
        self.rUpdateColors  = False
        self.rAlpha         = None
        self.rProtLoc       = None
        self.rProtLength    = None
        self.rProtDelta     = None
        self.rProtTarget    = None
        self.rPeptide       = None
        #------------------------------> 
        self.rDate, cMenuData = self.SetDateMenuDate()
        #------------------------------> 
        super().__init__(cParent, cMenuData=cMenuData)
        #------------------------------> 
        dKeyMethod = {
            'Peptide'  : self.OnClearPept,
            'Fragment' : self.OnClearFrag,
            'Gel Spot' : self.OnClearGel,
            'Band/Lane': self.OnClearBL,
            'All'      : self.OnClearAll,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wPlot.canvas.mpl_connect('pick_event', self.OnPickGel)
        self.wPlot.canvas.mpl_connect('button_press_event', self.OnPressMouse)
        self.wPlotM.canvas.mpl_connect('pick_event', self.OnPickFragment)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.UpdateDisplayedData(self.rDate[0])
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #------------------------------> Class methods
    #region --------------------------------------------------> Manage Methods
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.
            
            Returns
            -------
            bool
        """
        # #region ---------------------------------------------------> Variables
        info = super().WinPos()
        # #endregion ------------------------------------------------> Variables
                
        # #region ------------------------------------------------> Set Position
        # x = info['D']['xo'] + info['W']['N']*config.deltaWin
        # y = (
        #     ((info['D']['h']/2) - (info['W']['h']/2)) 
        #     + info['W']['N']*config.deltaWin
        # )
        # self.SetPosition(pt=(x,y))
        # #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---
    
    def UpdateDisplayedData(self, date) -> bool:
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
        self.rDateC      = date
        self.rDf         = self.rData[self.rDateC]['DF'].copy()
        self.rBands      = self.rData[self.rDateC]['PI']['Bands']
        self.rLanes      = self.rData[self.rDateC]['PI']['Lanes']
        self.rAlpha      = self.rData[self.rDateC]['PI']['Alpha']
        self.rProtLoc    = self.rData[self.rDateC]['PI']['ProtLoc']
        self.rProtLength = self.rData[self.rDateC]['PI']['ProtLength']
        self.rProtDelta  = self.rData[self.rDateC]['PI']['ProtDelta']
        self.rProtTarget = self.rData[self.rDateC]['PI']['Prot']
        self.rRectsGel   = []
        self.rRectsFrag  = []
        self.rBlSelC     = [None, None]
        self.rGelSelC    = [None, None]
        self.rFragSelC   = [None, None, None]
        self.rPeptide    = None
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 
        
        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl
        
        #region ----------------------------------------------------> Gel Plot
        self.DrawGel()
        #endregion -------------------------------------------------> Gel Plot
        
        #region ---------------------------------------------------> Fragments
        self.rFragments = dmethod.Fragments(
            self.GetDF4FragmentSearch(), self.rAlpha,'le')
                
        self.SetEmptyFragmentAxis()
        #endregion ------------------------------------------------> Fragments

        #region ---------------------------------------------------> Win Title
        self.PlotTitle()
        #endregion ------------------------------------------------> Win Title
        
        return True
    #---
    
    def DrawGel(self) -> bool:
        """Draw the Gel representation on the window.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------> Remove Old Selections
        #------------------------------> Select Gel Spot 
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
        else:
            pass
        
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
            self.rBlSelRect = None
        else:
            pass
        #endregion ------------------------------------> Remove Old Selections
       
        #region --------------------------------------------------------> Axis
        self.SetGelAxis()
        #endregion -----------------------------------------------------> Axis

        #region ---------------------------------------------------> Draw Rect
        for nb,_ in enumerate(self.rBands, start=1):
            for nl,_ in enumerate(self.rLanes, start=1):
                self.rRectsGel.append(mpatches.Rectangle(
                    ((nl-0.4),(nb-0.4)), 
                    0.8, 
                    0.8, 
                    edgecolor = 'black',
                    linewidth = self.cGelLineWidth,
                    facecolor = self.SetGelSpotColor(nb-1,nl-1),
                    picker    = True,
                ))
                self.wPlot.axes.add_patch(self.rRectsGel[-1])
        #endregion ------------------------------------------------> Draw Rect
       
        #region --------------------------------------------------> Zoom Reset
        self.wPlot.ZoomResetSetValues()
        #endregion -----------------------------------------------> Zoom Reset
       
        #region --------------------------------------------------------> Draw
        self.wPlot.canvas.draw()
        #endregion -----------------------------------------------------> Draw
       
        return True
    #---
    
    def SetGelAxis(self) -> bool:
        """Configure the axis for the Gel representation.
    
            Returns
            -------
            bool        
        """
        #region ----------------------------------------------------> Variables
        nLanes = len(self.rLanes)
        nBands = len(self.rBands)
        #endregion -------------------------------------------------> Variables
       
        #region ---------------------------------------------------> 
        self.wPlot.axes.clear()
        self.wPlot.axes.set_xticks(range(1, nLanes+1))
        self.wPlot.axes.set_xticklabels(self.rLanes)
        self.wPlot.axes.set_yticks(range(1, nBands+1))
        self.wPlot.axes.set_yticklabels(self.rBands)
        self.wPlot.axes.tick_params(length=0)
        #------------------------------> 
        self.wPlot.axes.set_xlim(0.5, nLanes+0.5)
        self.wPlot.axes.set_ylim(0.5, nBands+0.5)
        #endregion ------------------------------------------------> 
        
        #region ------------------------------------------------> Remove Frame
        self.wPlot.axes.spines['top'].set_visible(False)
        self.wPlot.axes.spines['right'].set_visible(False)
        self.wPlot.axes.spines['bottom'].set_visible(False)
        self.wPlot.axes.spines['left'].set_visible(False)
        #endregion ---------------------------------------------> Remove Frame
    
        return True 
    #---
    
    def SetGelSpotColor(
        self, nb: int, nl: int, showAll: bool=False
        ) -> str:
        """Get the color for each gel spot.
    
            Parameters
            ----------
            nb: int
                Number of bands in the gel.
            nl: int
                Number of lanes in the gel.
            showAll: bool
                Show all fragments in the gel or not.
    
            Returns
            -------
            str
                Gel spot color
        """
        #region ---------------------------------------------------> Variables  
        b = self.rBands[nb]
        l = self.rLanes[nl]
        c = self.rDf.loc[:,(b,l,'Ptost')].isna().all()
        nc = len(self.cColor['Spot'])
        #endregion ------------------------------------------------> Variables  

        #region -------------------------------------------------------> Color
        if c:
            return 'white'
        elif showAll:
            if self.rSelBands:
                return self.cColor['Spot'][nb%nc]
            else:
                return self.cColor['Spot'][nl%nc]
        else:
            if self.rSelBands:
                return self.cColor['Spot'][nl%nc]
            else:
                return self.cColor['Spot'][nb%nc]
        #endregion ----------------------------------------------------> Color
    #---
    
    def DrawBLRect(self, x: int, y: int) -> bool:
        """Draw the red rectangle to highlight the selected band/lane.
    
            Parameters
            ----------
            x: int
                X coordinate of the band/lane
            y: int
                Y coordinate of the band/lane
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.UpdateGelColor()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> Variables
        if self.rSelBands:
            xy = (0.55, y-0.45)
            w = len(self.rLanes) - 0.1
            h = 0.9
        else:
            xy = (x-0.45, 0.55)
            w = 0.9
            h = len(self.rBands) - 0.1
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------> Remove Old Rect
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
        else:
            pass
        #endregion ------------------------------------------> Remove Old Rect
        
        #region -----------------------------------------------> Draw New Rect
        self.rBlSelRect = mpatches.Rectangle(
            xy, w, h,
            linewidth = 1.5,
            edgecolor = 'red',
            fill      = False,
        )

        self.wPlot.axes.add_patch(self.rBlSelRect)
        
        self.wPlot.canvas.draw()
        #endregion --------------------------------------------> Draw New Rect
        
        return True
    #---
    
    def DrawFragments(self, x: int, y: int) -> bool:
        """Draw the fragments associated with the selected band/lane.
    
            Parameters
            ----------
            x: int
                X coordinate of the band/lane
            y: int
                Y coordinate of the band/lane
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        b = self.rBands[y-1]
        l = self.rLanes[x-1]
        tKeyLabel = {}
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Keys
        if self.rSelBands:
            for k,tL in enumerate(self.rLanes):
                tKeyLabel[f"{(b, tL, 'Ptost')}"] = f'{y-1}.{k}'
        else:
            for k,tB in enumerate(self.rBands):
                tKeyLabel[f"{(tB, l, 'Ptost')}"] = f'{k}.{x-1}'
        #endregion -----------------------------------------------------> Keys
        
        #region -------------------------------------------------------> Super
        super().DrawFragments(tKeyLabel)
        #endregion ----------------------------------------------------> Super
        
        return True
    #---
    
    def SetFragmentAxis(self, showAll=False) -> bool:
        """Set the axis for the plot showing the fragments.
    
            Parameters
            ----------
            showAll: bool
                Show all fragments or not. Default is False.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.wPlotM.axes.clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        #------------------------------>
        if self.rProtLoc[0] is not None:
            xtick = [1] + list(self.rProtLoc) + [self.rProtLength]
        else:
            xtick = [1] + [self.rProtLength]
        self.wPlotM.axes.set_xticks(xtick)
        self.wPlotM.axes.set_xticklabels(xtick)
        #------------------------------> 
        if showAll:
            self.wPlotM.axes.set_yticks(range(1, len(showAll)+2))
            self.wPlotM.axes.set_yticklabels(showAll+['Protein'])
            self.wPlotM.axes.set_ylim(0.5, len(showAll)+1.5)
            #------------------------------> 
            ymax = len(showAll)+0.8
        else:
            if self.rSelBands:
                #------------------------------> 
                self.wPlotM.axes.set_yticks(range(1, len(self.rLanes)+2))
                self.wPlotM.axes.set_yticklabels(self.rLanes+['Protein'])            
                self.wPlotM.axes.set_ylim(0.5, len(self.rLanes)+1.5)
                #------------------------------> 
                ymax = len(self.rLanes)+0.8
            else:
                #------------------------------> 
                self.wPlotM.axes.set_yticks(range(1, len(self.rBands)+2))
                self.wPlotM.axes.set_yticklabels(self.rBands+['Protein'])   
                self.wPlotM.axes.set_ylim(0.5, len(self.rBands)+1.5)
                #------------------------------> 
                ymax = len(self.rBands)+0.8
        #------------------------------> 
        self.wPlotM.axes.tick_params(length=0)
        #------------------------------> 
        self.wPlotM.axes.set_xlim(0, self.rProtLength+1)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wPlotM.axes.vlines(
            xtick, 0, ymax, linestyles='dashed', linewidth=0.5, color='black')
        #endregion ------------------------------------------------> 
       
        #region ------------------------------------------------> Remove Frame
        self.wPlotM.axes.spines['top'].set_visible(False)
        self.wPlotM.axes.spines['right'].set_visible(False)
        self.wPlotM.axes.spines['bottom'].set_visible(False)
        self.wPlotM.axes.spines['left'].set_visible(False)
        #endregion ---------------------------------------------> Remove Frame
        
        return True
    #---
    
    def PrintBLText(self, x: int, y: int) -> bool:
        """Print the text for selected band/lane.
    
            Parameters
            ----------
            x: int
                X coordinates of the selected band/lane
            y: int
                Y coordinates of the selected band/lane

            Returns
            -------
            bool
        """
        if self.rSelBands:
            return self.PrintBText(y)
        else:
            return self.PrintLText(x)
    #---
    
    def PrintLBGetInfo(self, tKeys: list[int]) -> dict:
        """Helper method to get information about the selected Band/Lane.
    
            Parameters
            ----------
            tKeys: str
                List of keys for the information.        
    
            Returns
            -------
            dict:
                {
                    'LanesWithFP': ,
                    'Fragments': ,
                    'FP': ,
                    'NCO': ,
                    'NCONat': ,
                }
        """
        #region ---------------------------------------------------> 
        dictO = {}
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        lanesWithFP = []
        fragments = []
        fP = []
        ncL = []
        ncO = []
        #------------------------------> 
        for tKey in tKeys:
            #--------------> 
            x = f'{tKey}'
            nF = len(self.rFragments[x]['Coord'])
            #--------------> 
            if nF:
                if self.rSelBands:
                    lanesWithFP.append(tKey[1])
                else:
                    lanesWithFP.append(tKey[0])
                fragments.append(nF)
                fP.append(sum(self.rFragments[x]['Np']))
            else:
                pass
            #------------------------------> 
            ncL = ncL + self.rFragments[x]['Coord']
        #------------------------------> 
        dictO['LanesWithFP'] = (
            f'{len(lanesWithFP)} (' + f'{lanesWithFP}'[1:-1] + f')')
        dictO['Fragments'] = (
            f'{len(fragments)} (' + f'{fragments}'[1:-1] + f')')
        dictO['FP'] = (
            f'{sum(fP)} (' +f'{fP}'[1:-1] + f')')
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        ncL.sort()
        n,c = ncL[0]
        for nc,cc in ncL[1:]:
            if nc <= c:
                if cc <= c:
                    pass
                else:
                    c = cc
            else:
                ncO.append((n,c))
                n = nc
                c = cc
        ncO.append((n,c))
        #------------------------------> 
        if self.rProtDelta is not None:
            ncONat = []
            for a,b in ncO:
                aX = a+self.rProtDelta
                bX = b+self.rProtDelta
                ncONat.append((aX,bX))
        else:
            ncONat = 'NA' 
        #------------------------------>     
        dictO['NCO'] = ncO
        dictO['NCONat'] = ncONat
        #endregion ------------------------------------------------> 

        return dictO
    #---
    
    def PrintBText(self, band: int) -> bool:
        """Print information about a Band.
    
            Parameters
            ----------
            band: int
                Index of the selected band in self.rBands
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Get Values
        #------------------------------> Keys
        tKeys = [(self.rBands[band], x, 'Ptost') for x in self.rLanes]
        #------------------------------> Info
        infoDict = self.PrintLBGetInfo(tKeys)           
        #endregion -----------------------------------------------> Get Values
        
        #region -------------------------------------------------------> Clear
        self.wText.Clear()
        #endregion ----------------------------------------------------> Clear
        
        #region ----------------------------------------------------> New Text
        self.wText.AppendText(f'Details for {self.rBands[band]}\n\n')
        self.wText.AppendText(f'--> Analyzed Lanes\n\n')
        self.wText.AppendText(f'Total Lanes  : {len(self.rLanes)}\n')
        self.wText.AppendText(f'Lanes with FP: {infoDict["LanesWithFP"]}\n')
        self.wText.AppendText(f'Fragments    : {infoDict["Fragments"]}\n')
        self.wText.AppendText(f'Number of FP : {infoDict["FP"]}\n\n')
        self.wText.AppendText(f'--> Detected Protein Regions:\n\n')
        self.wText.AppendText(f'Recombinant Sequence:\n')
        self.wText.AppendText(f'{infoDict["NCO"]}'[1:-1]+'\n\n')
        self.wText.AppendText(f'Native Sequence:\n')
        self.wText.AppendText(f'{infoDict["NCONat"]}'[1:-1])
        
        self.wText.SetInsertionPoint(0)
        #endregion -------------------------------------------------> New Text
        
        return True
    #---
    
    def PrintLText(self, lane: int) -> bool:
        """Print information about a Lane.
    
            Parameters
            ----------
            lane: int
                Index of the selected lane in self.rLanes
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Get Values
        #------------------------------> Keys
        tKeys = [(x, self.rLanes[lane], 'Ptost') for x in self.rBands]
        #------------------------------> Info
        infoDict = self.PrintLBGetInfo(tKeys)           
        #endregion -----------------------------------------------> Get Values
        
        #region -------------------------------------------------------> Clear
        self.wText.Clear()
        #endregion ----------------------------------------------------> Clear
        
        #region ----------------------------------------------------> New Text
        self.wText.AppendText(f'Details for {self.rLanes[lane]}\n\n')
        self.wText.AppendText(f'--> Analyzed Lanes\n\n')
        self.wText.AppendText(f'Total Lanes  : {len(self.rBands)}\n')
        self.wText.AppendText(f'Lanes with FP: {infoDict["LanesWithFP"]}\n')
        self.wText.AppendText(f'Fragments    : {infoDict["Fragments"]}\n')
        self.wText.AppendText(f'Number of FP : {infoDict["FP"]}\n\n')
        self.wText.AppendText(f'--> Detected Protein Regions:\n\n')
        self.wText.AppendText(f'Recombinant Sequence:\n')
        self.wText.AppendText(f'{infoDict["NCO"]}'[1:-1]+'\n\n')
        self.wText.AppendText(f'Native Sequence:\n')
        self.wText.AppendText(f'{infoDict["NCONat"]}'[1:-1])
        
        self.wText.SetInsertionPoint(0)
        #endregion -------------------------------------------------> New Text
        
        return True
    #---
      
    def PrintGelSpotText(self, x: int, y: int) -> bool:
        """Print information about a selected Gel spot.
    
            Parameters
            ----------
            x: int
                X coordinate of the selected Gel spot.
            y: int
                Y coordinate od the selected Gel spot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        tKey = f'{(self.rBands[y], self.rLanes[x], "Ptost")}'
        #------------------------------> 
        fragments = len(self.rFragments[tKey]['Coord'])
        if fragments == 0:
            self.wText.Clear()
            self.wText.AppendText(
                f'Details for {self.rLanes[x]} - {self.rBands[y]}\n\n')
            self.wText.AppendText(
                f'There were no peptides from {self.rProtTarget} detected here.')
            return True
        else:
            pass
        #------------------------------> 
        fp = (
            f'{sum(self.rFragments[tKey]["Np"])} (' + 
            f'{self.rFragments[tKey]["Np"]}'[1:-1] + ')'
        )
        #------------------------------> 
        if self.rProtDelta is not None:
            ncONat = []
            for a,b in self.rFragments[tKey]['Coord']:
                aX = a+self.rProtDelta
                bX = b+self.rProtDelta
                ncONat.append((aX,bX))
        else:
            ncONat = 'NA' 
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wText.AppendText(
            f'Details for {self.rLanes[x]} - {self.rBands[y]}\n\n')
        self.wText.AppendText(f'--> Fragments: {fragments}\n\n')
        self.wText.AppendText(f'--> Number of FP: {fp}\n\n')
        self.wText.AppendText(f'--> Detected Protein Regions:\n\n')
        self.wText.AppendText(f'Recombinant Protein:\n')
        self.wText.AppendText(f'{self.rFragments[tKey]["Coord"]}'[1:-1]+'\n\n')
        self.wText.AppendText(f'Native Protein:\n')
        self.wText.AppendText(f'{ncONat}'[1:-1])
        
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def PrintFragmentText(
        self, tKey: tuple[str, str,str], fragC: list[int]):
        """Print information about a selected Fragment
    
            Parameters
            ----------
            tKey: tuple(str, str, str)
                Tuple with the column name in the pd.DataFrame with the results.
            fragC: list[int]
                Fragment coordinates.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Info
        n, c = self.rFragments[tKey]["Coord"][fragC[2]]
        
        if n >= self.rProtLoc[0] and n <= self.rProtLoc[1]:
            nnat = n + self.rProtDelta
        else:
            nnat = 'NA'
        if c >= self.rProtLoc[0] and c <= self.rProtLoc[1]:
            cnat = c + self.rProtDelta
        else:
            cnat = 'NA'
        resNum = f'Nterm {n}({nnat}) - Cterm {c}({cnat})'
        
        np = (f'{self.rFragments[tKey]["Np"][fragC[2]]} '
              f'({self.rFragments[tKey]["NpNat"][fragC[2]]})')
        clsite = (f'{self.rFragments[tKey]["Nc"][fragC[2]]} '
                  f'({self.rFragments[tKey]["NcNat"][fragC[2]]})')
        #endregion ------------------------------------------------> Info

        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wText.AppendText(
            f'Details for {self.rLanes[fragC[1]]} - {self.rBands[fragC[0]]} - Fragment {fragC[2]+1}\n\n')
        self.wText.AppendText(f'Residue Numbers: {resNum}\n')
        self.wText.AppendText(f'Sequences: {np}\n')
        self.wText.AppendText(f'Cleavage Sites: {clsite}\n\n')
        self.wText.AppendText(f'Sequences in the fragment:\n\n')
        self.wText.AppendText(f'{self.rFragments[tKey]["Seq"][fragC[2]]}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------> 
        
        return True
    #---
    
    def ShowPeptideLoc(self) -> bool:
        """Show the location of the selected peptide.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        for k in self.rRectsGel:
            k.set_linewidth(self.cGelLineWidth)
        
        for k in self.rRectsFrag:
            k.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------->
        j = 0 
        for b in self.rBands:
            for l in self.rLanes:
                for p in self.rFragments[f'{(b,l, "Ptost")}']['SeqL']:
                    if self.rPeptide in p:
                        self.rRectsGel[j].set_linewidth(2.0)
                        break
                    else:
                        pass
                j = j + 1
        #endregion ------------------------------------------------> 
        
        #region --------------------------------------------------->
        if self.rBlSelC != [None, None]:
            #------------------------------> 
            fKeys = []
            #------------------------------> 
            if self.rSelBands:
                for l in self.rLanes:
                    fKeys.append(f'{(self.rBands[self.rBlSelC[0]], l, "Ptost")}')
            else:
                for b in self.rBands:
                    fKeys.append(f'{(b, self.rLanes[self.rBlSelC[1]], "Ptost")}')
            #------------------------------> 
            j = 0
            for k in fKeys:
                for p in self.rFragments[k]['SeqL']:
                    if self.rPeptide in p:
                        self.rRectsFrag[j].set_linewidth(2.0)
                    else:
                        pass
                    j = j + 1
        else:
            pass
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wPlot.canvas.draw()
        self.wPlotM.canvas.draw()
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def UpdateGelColor(self, showAll=False) -> bool:
        """Update the Gel colors.
    
            Parameters
            ----------
            showAll: bool
                Show all fragments or not. Default is False.
    
            Returns
            -------
            bool
        """
        #------------------------------> 
        j = 0
        #------------------------------> 
        for nb,b in enumerate(self.rBands):
            for nl,l in enumerate(self.rLanes):
                self.rRectsGel[j].set_facecolor(
                    self.SetGelSpotColor(nb,nl, showAll=showAll)
                )
                j = j + 1
        #------------------------------> 
        self.wPlot.canvas.draw()
        
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region ---------------------------------------------------> Event Methods
    def OnPickFragment(self, event) -> bool:
        """Display info about the selected fragment.
    
            Parameters
            ----------
            event: matplotlib pick event
    
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
        tKey = f'{(self.rBands[fragC[0]], self.rLanes[fragC[1]], "Ptost")}'
        #------------------------------> 
        x1, x2 = self.rFragments[tKey]['Coord'][fragC[2]]
        #endregion ------------------------------------------------> Variables
        
        #region ------------------------------------------> Highlight Fragment
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
        else:
            pass
        #------------------------------> 
        self.rFragSelLine = self.wPlotM.axes.plot(
            [x1+2, x2-2], [y,y], color='black', linewidth=4)
        #------------------------------> 
        self.wPlotM.canvas.draw()
        #endregion ---------------------------------------> Highlight Fragment
        
        #region -------------------------------------------------------> Print
        self.PrintFragmentText(tKey, fragC)
        #endregion ----------------------------------------------------> Print
        
        #region -------------------------------------------> Remove Sel in Gel
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
            self.wPlot.canvas.draw()
            self.rGelSelC = [None, None]
        else:
            pass
        #endregion ----------------------------------------> Remove Sel in Gel

        return True
    #---
    
    def OnPickGel(self, event) -> bool:
        """Display info about the selected Gel spot.
    
            Parameters
            ----------
            event: matplotlib pick event
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x, y = event.artist.xy
        x = round(x)
        y = round(y)
        #endregion ------------------------------------------------> Variables
        
        #region -------------------------------------------------> Flag picked
        self.rGelSpotPicked = True
        #endregion ----------------------------------------------> Flag picked
        
        #region -----------------------------------------------> Spot Selected
        spotC = [y-1, x-1]
        if self.rGelSelC != spotC:
            self.rGelSelC = spotC
        else:
            return True
        #endregion --------------------------------------------> Spot Selected
        
        #region ---------------------------------------------> Remove Old Line
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
        else:
            pass
        #endregion ------------------------------------------> Remove Old Line
        
        #region -----------------------------------------------> Draw New Line
        self.rSpotSelLine = self.wPlot.axes.plot(
            [x-0.3, x+0.3], [y,y], color='black', linewidth=4)
        #------------------------------> 
        self.wPlot.canvas.draw()
        #endregion --------------------------------------------> Draw New Line
        
        #region --------------------------------------------------------> Info
        self.PrintGelSpotText(x-1,y-1)
        #endregion -----------------------------------------------------> Info
        
        #region ----------------------------------------> Remove Sel from Frag
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
            self.rFragSelLine = None
            self.wPlotM.canvas.draw()
            self.rFragSelC = [None, None, None]
        else:
            pass
        #endregion -------------------------------------> Remove Sel from Frag
        
        #region ---------------------------------------------------> 
        if self.rUpdateColors:
            self.UpdateGelColor()
            self.rUpdateColors = False
        else:
            pass
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnPressMouse(self, event) -> bool:
        """Press mouse event in the Gel.

            Parameters
            ----------
            event:wx.Event
                Information about the event


            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> In axis
        if event.inaxes:
            pass
        else:
            return False
        #endregion ------------------------------------------------> In axis

        #region ---------------------------------------------------> Variables
        x = round(event.xdata)
        y = round(event.ydata)
        #endregion ------------------------------------------------> Variables
        
        #region -----------------------------------------------> Redraw or Not
        blSel = [y-1, x-1]
        if self.rSelBands and self.rBlSelC[0] != blSel[0]:
            self.rBlSelC = [blSel[0], None]
        elif not self.rSelBands and self.rBlSelC[1] != blSel[1]:
            self.rBlSelC = [None, blSel[1]]
        else:
            #------------------------------> 
            if self.rGelSpotPicked:
                self.rGelSpotPicked = False
            else:
                #------------------------------> 
                if self.rSpotSelLine is not None:
                    self.rSpotSelLine[0].remove()
                    self.rSpotSelLine = None
                    self.rGelSelC = [None, None]
                    self.wPlot.canvas.draw()
                else:
                    pass
                #------------------------------> 
                self.PrintBLText(x-1,y-1)
            #------------------------------> 
            if self.rFragSelLine is not None:
                self.rFragSelLine[0].remove()
                self.rFragSelLine = None
                self.wPlotM.canvas.draw()
                self.rFragSelC = [None, None, None]
            else:
                pass
            #------------------------------>
            if self.rUpdateColors:
                self.UpdateGelColor()
                self.rUpdateColors = False
            else:
                pass
            #------------------------------> 
            return True
        #endregion --------------------------------------------> Redraw or Not

        #region -----------------------------------------------> Draw New Rect
        self.DrawBLRect(x,y)
        #endregion --------------------------------------------> Draw New Rect
        
        #region ----------------------------------------------> Draw Fragments
        self.DrawFragments(x,y)
        #endregion -------------------------------------------> Draw Fragments

        #region ---------------------------------------------------> 
        if self.rGelSpotPicked:
            self.rGelSpotPicked = False
        else:
            #------------------------------> 
            if self.rSpotSelLine is not None:
                self.rSpotSelLine[0].remove()
                self.rSpotSelLine = None
                self.rGelSelC = [None, None]
                self.wPlot.canvas.draw()
            else:
                pass
            #------------------------------> 
            self.PrintBLText(x-1,y-1)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        if self.rUpdateColors:
            self.UpdateGelColor()
            self.rUpdateColors = False
        else:
            pass
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnLaneBand(self, state: bool) -> bool:
        """Change Band/Lane selectio mode.
    
            Parameters
            ----------
            state: bool
    
            Returns
            -------
            bool
        """
        self.rSelBands = not state
        self.rUpdateColors = True
        
        return True
    #---
    
    def OnPlotSaveAllImage(self) -> bool:
        """ Export all plots to a pdf image
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.DirSelectDialog(parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            if self.rSelBands:
                fName = p / f'{self.rDateC}-{self.rBands[self.rBlSelC[0]]}-fragments.pdf'
            else:
                fName = p / f'{self.rDateC}-{self.rLanes[self.rBlSelC[1]]}-fragments.pdf'
            self.wPlotM.figure.savefig(fName)
            #------------------------------> 
            fName = p / f'{self.rDateC}-gel.pdf'
            self.wPlot.figure.savefig(fName)
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
        
    def OnClearPept(self, plot: bool=True) -> bool:
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
        if (rID := self.wLC.wLCS.lc.GetFirstSelected()):
            self.wLC.wLCS.lc.Select(rID, on=0)
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        for r in self.rRectsFrag:
            r.set_linewidth(self.cGelLineWidth)
        
        
        for r in self.rRectsGel:
            r.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        if plot:
            self.wPlotM.canvas.draw()
            self.wPlot.canvas.draw()
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rPeptide = None
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearFrag(self, plot=True) -> bool:
        """Clear the FRagment selection.
    
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
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        if plot:
            self.wPlotM.canvas.draw()
            if self.rFragSelC != [None, None, None]:
                self.wText.Clear()
                #------------------------------> 
                if self.rSelBands:
                    self.PrintBText(self.rBlSelC[0])
                else:
                    self.PrintLText(self.rBlSelC[1])
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rFragSelC = [None, None, None]
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearGel(self, plot=True) -> bool:
        """Clear the Gel spot selection.
    
            Parameters
            ----------
            plot: bool
                Redraw the canvas.
            
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        if plot:
            self.wPlot.canvas.draw()
            if self.rGelSelC != [None, None]:
                self.wText.Clear()
                #------------------------------> 
                if self.rSelBands:
                    self.PrintBText(self.rBlSelC[0])
                else:
                    self.PrintLText(self.rBlSelC[1])
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rGelSelC = [None, None]
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearBL(self, plot=True) -> bool:
        """Clear the Band/Lane selection.
    
            Parameters
            ----------
            plot: bool
                Redraw the canvas.
            
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.SetEmptyFragmentAxis()
        self.OnClearGel(plot=False)
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
            self.rBlSelRect = None
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        if plot:
            self.wPlot.canvas.draw()
            self.wText.Clear()
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rBlSelC = [None, None]
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearAll(self) -> bool:
        """Clear all selections.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.OnClearPept(plot=False)
        self.OnClearFrag(plot=False)
        self.OnClearGel(plot=False)
        self.OnClearBL(plot=False)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wPlotM.canvas.draw()
        self.wPlot.canvas.draw()
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnShowAll(self) -> bool:
        """Show all Fragments.
        
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.OnClearAll()
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.UpdateGelColor(showAll=True)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.rBlSelRect = mpatches.Rectangle(
            (0.55, 0.55), len(self.rLanes)-0.1, len(self.rBands)-0.1,
            linewidth = 1.5,
            edgecolor = 'red',
            fill      = False,
        )
        #------------------------------> 
        self.wPlot.axes.add_patch(self.rBlSelRect)
        #------------------------------> 
        self.wPlot.canvas.draw()
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        #------------------------------> 
        tKeys   = []
        tLabel  = []
        tColor  = []
        tYLabel = []
        self.rRectsFrag = []
        #------------------------------> 
        if self.rSelBands:
            for bk, b in enumerate(self.rBands):
                for lk, l in enumerate(self.rLanes):
                    tKeys.append(f"{(b, l, 'Ptost')}")
                    tYLabel.append(f"{b}-{l}")
                    tColor.append(bk)
                    tLabel.append(f'{bk}.{lk}')
        else:
            for lk, l in enumerate(self.rLanes):
                for bk, b in enumerate(self.rBands):
                    tKeys.append(f"{(b, l, 'Ptost')}")
                    tYLabel.append(f"{l}-{b}")
                    tColor.append(lk)
                    tLabel.append(f'{bk}.{lk}')
        #------------------------------> 
        self.SetFragmentAxis(showAll=tYLabel)
        #------------------------------> 
        nc = len(self.cColor['Spot'])
        #------------------------------> 
        for k,v in enumerate(tKeys, start=1):
            for j,f in enumerate(self.rFragments[v]['Coord']):
                self.rRectsFrag.append(mpatches.Rectangle(
                    (f[0], k-0.2), 
                    (f[1]-f[0]), 
                    0.4,
                    picker    = True,
                    linewidth = self.cGelLineWidth,
                    facecolor = self.cColor['Spot'][(tColor[k-1])%nc],
                    edgecolor = 'black',
                    label     = f'{tLabel[k-1]}.{j}',
                ))
                self.wPlotM.axes.add_patch(self.rRectsFrag[-1])
        #------------------------------> 
        self.DrawProtein(k+1)
        #------------------------------> 
        self.wPlotM.ZoomResetSetValues()
        self.wPlotM.canvas.draw()
        #endregion ------------------------------------------------> 
        
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class TarProtPlot(BaseWindowProteolysis):
    """Plot the results of a Targeted Proteolysis analysis.

        Parameters
        ----------
        cParent: wx.Window
            Parent of the window
    
        Attributes
        ----------
    """
    #region -----------------------------------------------------> Class setup
    cName = config.nwTarProt
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nmTarProt
    #------------------------------> Label
    cLPanePlot = 'Intensity'
    #------------------------------> Colors
    cCNatProt = config.color['NatProt']
    cCRecProt = config.color['RecProt']
    cColor = config.color[cName]
    #------------------------------>
    rIdxSeqNC = pd.IndexSlice[config.dfcolSeqNC,:]
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle       = f'{cParent.cTitle} - {self.cSection}'
        self.rObj         = cParent.rObj
        self.rData        = self.rObj.dConfigure[self.cSection]()
        self.rDateC       = None
        self.rAlpha       = None
        self.rFragments   = None
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        self.rRectsFrag   = []
        self.rProtLoc     = None
        self.rProtLength  = None
        self.rExp         = None
        self.rCtrl        = None
        self.rIdxP        = None
        self.rPeptide     = None
        #------------------------------> 
        self.rDate, cMenuData = self.SetDateMenuDate()
        #------------------------------> 
        super().__init__(cParent, cMenuData=cMenuData)
        #------------------------------> 
        dKeyMethod = {
            'Peptide'  : self.OnClearPept,
            'Fragment' : self.OnClearFrag,
            'All'      : self.OnClearAll,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wPlotM.canvas.mpl_connect('pick_event', self.OnPickFragment)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.UpdateDisplayedData(self.rDate[0])
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #------------------------------> Class methods
    #region --------------------------------------------------> Manage Methods
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.
            
            Returns
            -------
            bool
        """
        # #region ---------------------------------------------------> Variables
        info = super().WinPos()
        # #endregion ------------------------------------------------> Variables
                
        # #region ------------------------------------------------> Set Position
        # x = info['D']['xo'] + info['W']['N']*config.deltaWin
        # y = (
        #     ((info['D']['h']/2) - (info['W']['h']/2)) 
        #     + info['W']['N']*config.deltaWin
        # )
        # self.SetPosition(pt=(x,y))
        # #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---
    
    def UpdateDisplayedData(self, date) -> bool:
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
        self.rDateC       = date
        self.rDf          = self.rData[self.rDateC]['DF'].copy()
        self.rAlpha       = self.rData[self.rDateC]['PI']['Alpha']
        self.rProtLoc     = self.rData[self.rDateC]['PI']['ProtLoc']
        self.rProtLength  = self.rData[self.rDateC]['PI']['ProtLength']
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        self.rExp         = self.rData[self.rDateC]['PI']['Exp']
        self.rCtrl        = self.rData[self.rDateC]['PI']['Ctrl']
        self.rIdxP        = pd.IndexSlice[self.rExp,'P']
        self.rPeptide     = None
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 
        
        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl
        
        #region ---------------------------------------------------> Fragments
        self.rFragments = dmethod.Fragments(
            self.GetDF4FragmentSearch(), self.rAlpha, 'le')
        
        self.DrawFragments()
        #endregion ------------------------------------------------> Fragments
        
        #region -----------------------------------------------------> Peptide
        self.SetAxisInt()
        self.wPlot.canvas.draw()
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
    
    def SetFragmentAxis(self, showAll=False) -> bool:
        """Set the axis for the plot showing the fragments.
    
            Parameters
            ----------
            showAll: bool
                Show all fragments or not. Default is False.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.wPlotM.axes.clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        #------------------------------>
        if self.rProtLoc[0] is not None:
            xtick = [1] + list(self.rProtLoc) + [self.rProtLength]
        else:
            xtick = [1] + [self.rProtLength]
        self.wPlotM.axes.set_xticks(xtick)
        self.wPlotM.axes.set_xticklabels(xtick)
        #------------------------------> 
        self.wPlotM.axes.set_yticks(range(1, len(self.rExp)+2))
        self.wPlotM.axes.set_yticklabels(self.rExp+['Protein'])   
        self.wPlotM.axes.set_ylim(0.5, len(self.rExp)+1.5)
        #------------------------------> 
        ymax = len(self.rExp)+0.8
        #------------------------------> 
        self.wPlotM.axes.tick_params(length=0)
        #------------------------------> 
        self.wPlotM.axes.set_xlim(0, self.rProtLength+1)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wPlotM.axes.vlines(
            xtick, 0, ymax, linestyles='dashed', linewidth=0.5, color='black')
        #endregion ------------------------------------------------> 
       
        #region ------------------------------------------------> Remove Frame
        self.wPlotM.axes.spines['top'].set_visible(False)
        self.wPlotM.axes.spines['right'].set_visible(False)
        self.wPlotM.axes.spines['bottom'].set_visible(False)
        self.wPlotM.axes.spines['left'].set_visible(False)
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
        self.wPlotM.canvas.draw()
        #endregion ------------------------------------------------> Fragments
        
        #region ---------------------------------------------------> Intensity
        #------------------------------> Variables
        nExp = len(self.rExp)
        nc = len(self.cColor['Spot'])
        #------------------------------> Clear Plot
        self.wPlot.axes.clear()
        #------------------------------> Axis
        self.SetAxisInt()
        #------------------------------> Row
        row = self.rDf.loc[self.rDf[('Sequence', 'Sequence')] == self.rPeptide]
        row =row.loc[:,pd.IndexSlice[:,('Int','P')]]
        #------------------------------> Values
        for k,c in enumerate(self.rCtrl+self.rExp, start=1):
            #------------------------------> Variables
            intL, P = row[c].values.tolist()[0]
            intL = list(map(float, intL[1:-1].split(',')))
            P = float(P)
            intN = len(intL)
            #------------------------------> Color
            if k == 1:
                color = self.cColor['Ctrl']
                x = [1]
                y = [sum(intL)/intN]
            else:
                color = self.cColor['Spot'][(k-2)%nc]
            #------------------------------> Ave
            if P <= self.rAlpha:
                x.append(k)
                y.append(sum(intL)/intN)
            else:
                pass
            #------------------------------> Plot
            self.wPlot.axes.scatter(
                intN*[k], intL, color=color, edgecolor='black', zorder=3)
        #------------------------------> 
        self.wPlot.axes.scatter(
            x, 
            y, 
            edgecolor = 'black',
            marker    = 'D',
            color     = 'cyan',
            s         = 120,
            zorder    = 2,
        )
        self.wPlot.axes.plot(x,y, zorder=1)
        #------------------------------> Show
        self.wPlot.ZoomResetSetValues()
        self.wPlot.canvas.draw()
        #endregion ------------------------------------------------> Intensity

        return True
    #---
    
    def SetAxisInt(self) -> bool:
        """Set the axis of the Intensity plot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        nExp = len(self.rExp)
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------------> Values
        self.wPlot.axes.clear()
        self.wPlot.axes.set_xticks(range(1,nExp+2))
        self.wPlot.axes.set_xticklabels(self.rCtrl+self.rExp)
        #------------------------------> 
        self.wPlot.axes.set_xlim(0.5, nExp+1.5)
        #------------------------------> 
        self.wPlot.axes.set_ylabel('Intensity (after DP)')
        #endregion ---------------------------------------------------> Values

        return True
    #---
    
    def PrintFragmentText(
        self, tKey: tuple[str, str], fragC: list[int]):
        """Print information about a selected Fragment
    
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
        clsiteExp = (f'{self.rFragments[tKey]["NcT"][0]}'
                     f'({self.rFragments[tKey]["NcT"][1]})')
        seqExp = (f'{sum(self.rFragments[tKey]["Np"])}'
                  f'({sum(self.rFragments[tKey]["NpNat"])})')
        #------------------------------> Res Numbers
        n, c = self.rFragments[tKey]["Coord"][fragC[1]]
        nf, cf = self.rFragments[tKey]["CoordN"][fragC[1]]
        resNum = f'Nterm {n}({nf}) - Cterm {c}({cf})'
        #------------------------------> Sequences
        np = (f'{self.rFragments[tKey]["Np"][fragC[1]]}'
              f'({self.rFragments[tKey]["NpNat"][fragC[1]]})')
        #------------------------------> Cleavages
        clsite = (f'{self.rFragments[tKey]["Nc"][fragC[1]]}'
                  f'({self.rFragments[tKey]["NcNat"][fragC[1]]})')
        #------------------------------> Labels
        expL, fragL = dtsMethod.StrEqualLength(
            [self.rExp[fragC[0]], f'Fragment {fragC[1]+1}'])
        emptySpace = (2+ len(expL))*' '
        #endregion ------------------------------------------------> Info

        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wText.AppendText(
            f'Details for {self.rExp[fragC[0]]} - Fragment {fragC[1]+1}\n\n')
        self.wText.AppendText(f'{expL}: Fragments {frag}, Cleavage sites {clsiteExp}\n')
        self.wText.AppendText(f'{emptySpace}Peptides {seqExp}\n\n')
        self.wText.AppendText(f'{fragL}: Nterm {n}({nf}), Cterm {c}({cf})\n')
        self.wText.AppendText(f'{emptySpace}Peptides {np}, Cleavage sites {clsite}\n\n')
        self.wText.AppendText(f'Sequences in the fragment:\n\n')
        self.wText.AppendText(f'{self.rFragments[tKey]["Seq"][fragC[1]]}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------> 
        
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
    
    #region ----------------------------------------------------> Event Methods
    def OnPickFragment(self, event) -> bool:
        """Display info about the selected fragment.
    
            Parameters
            ----------
            event: matplotlib pick event
    
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
        #------------------------------> 
        self.rFragSelLine = self.wPlotM.axes.plot(
            [x1+2, x2-2], [y,y], color='black', linewidth=4)
        #------------------------------> 
        self.wPlotM.canvas.draw()
        #endregion ---------------------------------------> Highlight Fragment
        
        #region -------------------------------------------------------> Print
        self.PrintFragmentText(tKey, fragC)
        #endregion ----------------------------------------------------> Print

        return True
    #---
    
    def OnPlotSaveAllImage(self) -> bool:
        """ Export all plots to a pdf image
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.DirSelectDialog(parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            #------------------------------> Export
            fName = p / f'{self.rDateC}-fragments.pdf'
            self.wPlotM.figure.savefig(fName)
            #------------------------------> 
            fName = p / f'{self.rDateC}-intensities.pdf'
            self.wPlot.figure.savefig(fName)
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
    
    def OnClearPept(self, plot: bool=True) -> bool:
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
        if (rID := self.wLC.wLCS.lc.GetFirstSelected()):
            self.wLC.wLCS.lc.Select(rID, on=0)
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        for r in self.rRectsFrag:
            r.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        if plot:
            self.wPlotM.canvas.draw()
            self.wPlot.canvas.draw()
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rPeptide = None
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearFrag(self, plot=True) -> bool:
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
            self.wPlotM.canvas.draw()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.rFragSelC = [None, None]
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClearAll(self) -> bool:
        """Clear all selections.
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        self.OnClearPept(plot=False)
        self.OnClearFrag(plot=False)
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wPlotM.canvas.draw()
        self.wPlot.canvas.draw()
        #endregion ------------------------------------------------> 
        
        #region ---------------------------------------------------> 
        self.wText.Clear()
        #endregion ------------------------------------------------> 

        return True
    #---
    #endregion -------------------------------------------------> Event Methods
#---


class CheckDataPrep(BaseWindowNPlotLT):
    """Window to check the data preparation steps

        Parameters
        ----------
        cParent: wx.Window
            Parent of the window
        cTitle : str or None
            Title of the window. Default is None
        rDpDF : dict[pd.DataFrame] or None
            The dictionary has the following structure:
            {
                "dfS" : pd.DataFrame, Data after excluding and filter by Score
                "dfT" : pd.DataFrame, Data after transformation
                "dfN" : pd.DataFrame, Data after normalization
                "dfIm": pd.DataFrame, Data after Imputation
            }
            Default is None

        Attributes
        ----------
        rData : dict
            Dict with the configured data for this section from UMSAPFile.
        rDate : list of str
            List of available dates in the section.
        rDateC : str
            Date selected. Needed to export the data and images.
        rDpDF : dict[pd.DataFrame]
            See dpDF in Parameters
        rFromUMSAPFile : bool
            The window is invoked from an UMSAP File window (True) or not (False)
        rObj : UMSAPFile
            Refernece to the UMSAPFile object.
        """
    #region -----------------------------------------------------> Class setup
    cName = config.nwCheckDataPrep
    #------------------------------> Needed by BaseWindowNPlotLT
    cLNPlots   = ['Init', 'Transf', 'Norm', 'Imp']
    cNPlotsCol = 2
    cLCol      = config.lLCtrlColNameI
    cSCol      = [45, 100]
    cHSearch   = 'Colum names'
    cTList     = 'Column names'
    cTText     = 'Statistic information'
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nuDataPrep
    #------------------------------> Label
    cLDFData = ['Filtered', 'Transformed', 'Normalized', 'Imputed']
    cLdfCol = config.dfcolDataCheck
    #------------------------------> Other
    cFileName = {
        config.ltDPKeys[0] : '{}-01-Filtered-{}.{}',
        config.ltDPKeys[1] : '{}-02-Transformed-{}.{}',
        config.ltDPKeys[2] : '{}-03-Normalized-{}.{}',
        config.ltDPKeys[3] : '{}-04-Imputed-{}.{}',
    }
    cImgName = {
        cLNPlots[0] : '{}-01-Filtered-{}.{}',
        cLNPlots[1] : '{}-02-Transformed-{}.{}',
        cLNPlots[2] : '{}-03-Normalized-{}.{}',
        cLNPlots[3] : '{}-04-Imputed-{}.{}',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: wx.Window, cTitle: Optional[str]=None, 
        tSection: Optional[str]=None, tDate: Optional[str]=None,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cParent  = cParent
        self.rObj     = self.cParent.rObj
        self.cTitle   = cTitle
        self.tSection = tSection
        self.tDate    = tDate
        self.SetWindow(tSection, tDate)
        #--------------> menuData here because it is not needed to save it
        cMenuData = None if self.rDate is None else {'menudate': self.rDate}
        #------------------------------> 
        super().__init__(cParent=cParent, cMenuData=cMenuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu
        
        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind

        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        date = None if self.rDate is None else self.rDate[0]
        self.UpdateDisplayedData(date)
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Close window and uncheck section in UMSAPFile window. Assumes 
            self.parent is an instance of UMSAPControl.
            Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #region -----------------------------------------------> Update parent
        if self.rFromUMSAPFile:
            self.cParent.UnCheckSection(self.cSection, self)		
        else:
            pass
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def OnListSelect(self, event: wx.CommandEvent) -> bool:
        """Plot data for the selected column
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        #region ------------------------------------------------> Get Selected
        idx = self.wLC.wLCS.lc.GetFirstSelected()
        #endregion ---------------------------------------------> Get Selected
        
        #region ---------------------------------------------------------> dfS
        try:
            self.PlotdfS(idx)
        except Exception as e:
            #------------------------------> 
            msg = (
                f'It was not possible to build the histograms for the selected '
                f'column.')
            dtscore.Notification('errorU', msg=msg, tException=e, parent=self)
            #------------------------------> 
            for p in self.cLNPlots:
                self.wPlots.dPlot[p].axes.clear()
                self.wPlots.dPlot[p].canvas.draw()
            #------------------------------> 
            return False
        #endregion ------------------------------------------------------> dfS
        
        #region ---------------------------------------------------------> dfT
        self.PlotdfT(idx)
        #endregion ------------------------------------------------------> dfT
        
        #region ---------------------------------------------------------> dfN
        self.PlotdfN(idx)
        #endregion ------------------------------------------------------> dfN
        
        #region --------------------------------------------------------> dfIm
        self.PlotdfIm(idx)
        #endregion -----------------------------------------------------> dfIm
        
        #region --------------------------------------------------------> Text
        self.SetText(idx)
        #endregion -----------------------------------------------------> Text
        
        return True
    #---
    
    def OnDupWin(self) -> bool:
        """Duplicate window.
    
            Returns
            -------
            True
        """
        #------------------------------> 
        if self.rFromUMSAPFile:
            super().OnDupWin()
        else:
            CheckDataPrep(
                self.cParent, 
                cTitle   = self.cTitle,
                tSection = self.tSection,
                tDate    = self.tDate,
            )
        #------------------------------> 
        return True
    #---
    
    def OnExportPlotData(self) -> bool:
        """ Export data to a csv file """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.DirSelectDialog(parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            col = self.wLC.wLCS.lc.GetFirstSelected()
            #------------------------------> Export
            try:
                for k, v in self.rDpDF.items():
                    #------------------------------> file path
                    fPath = p/self.cFileName[k].format(self.rDateC, col, 'txt')
                    #------------------------------> Write
                    dtsFF.WriteDF2CSV(fPath, v)
            except Exception as e:
                dtscore.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
    
    def OnPlotSaveImageOne(self) -> bool:
        """ Export all plots to a pdf image"""
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.DirSelectDialog(parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p = Path(dlg.GetPath())
            col = self.wLC.wLCS.lc.GetFirstSelected()
            #------------------------------> Export
            try:
                for k, v in self.wPlots.dPlot.items():
                    #------------------------------> file path
                    fPath = p / self.cImgName[k].format(self.rDateC, col, 'pdf')
                    #------------------------------> Write
                    v.figure.savefig(fPath)
            except Exception as e:
                dtscore.Notification(
                    'errorF',
                    msg        = self.cMsgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        return True	
    #---
    #endregion ------------------------------------------------> Event Methods
    
    #region --------------------------------------------------> Manage Methods
    def SetWindow(
        self, tSection: Optional[str]=None, tDate: Optional[str]=None,
        ) -> bool:
        """Configure the window. 
        
            See Notes below
    
            Returns
            -------
            bool
            
            Notes
            -----
            If self.cTitle is None the window is invoked from the main Data 
            Preparation section of a UMSAP File window
        """
        #------------------------------> Set Variables 
        if self.cTitle is None:
            self.rFromUMSAPFile = True 
            self.rData  = self.rObj.dConfigure[self.cSection]()
            self.rDate  = [k for k in self.rData.keys()]
            self.rDateC = self.rDate[0]
            self.cTitle = (
                f"{self.cParent.cTitle} - {self.cSection} - {self.rDateC}")
        else:
            self.rFromUMSAPFile = False
            self.rData = self.rObj.dConfigure[self.cSection](tSection, tDate)
            self.rDate = None
            self.rDateC = self.cParent.rDateC
        #------------------------------> 
        
        return True
    #---
    
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.
        """
        #region ---------------------------------------------------> Variables
        info = super().WinPos()
        #endregion ------------------------------------------------> Variables
                
        #region ------------------------------------------------> Set Position
        # x = info['D']['xo'] + info['W']['N']*config.deltaWin
        # y = (
        #     ((info['D']['h']/2) - (info['W']['h']/2)) 
        #     + info['W']['N']*config.deltaWin
        # )
        # self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---

    def FillListCtrl(self) -> bool:
        """Update the column names for the given analysis.
    
            Returns
            -------
            bool
            
            Notes
            -----
            Entries are read from self.ddDF['dfS']
        """
        #region --------------------------------------------------> Delete old
        self.wLC.wLCS.lc.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old
        
        #region ----------------------------------------------------> Get Data
        data = [[str(k), n] for k,n in enumerate(self.rDpDF['dfS'].columns.values.tolist())]
        #endregion -------------------------------------------------> Get Data
        
        #region ------------------------------------------> Set in wx.ListCtrl
        self.wLC.wLCS.lc.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl
        
        #region ----------------------------------------> Update Column Number
        self._mgr.GetPane(self.wLC).Caption(f'{self.cTList} ({len(data)})')
        self._mgr.Update()
        #endregion -------------------------------------> Update Column Number
        
        return True
    #---
    
    def PlotdfS(self, col:int) -> bool:
        """Plot the histograms for dfS
    
            Parameters
            ----------
            col : int
                Column to plot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        #------------------------------> 
        x = self.rDpDF['dfS'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Plot
        #------------------------------> 
        self.wPlots.dPlot['Init'].axes.clear()
        #------------------------------> title
        self.wPlots.dPlot['Init'].axes.set_title("Filtered")
        #------------------------------> 
        a = self.wPlots.dPlot['Init'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        self.wPlots.dPlot['Init'].axes.set_xlim(*dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin']))
        self.wPlots.dPlot['Init'].ZoomResetSetValues()
        #------------------------------> 
        self.wPlots.dPlot['Init'].canvas.draw()
        #endregion -----------------------------------------------------> Plot
        
        return True
    #---
    
    def PlotdfT(self, col:int) -> bool:
        """Plot the histograms for dfT
    
            Parameters
            ----------
            col : int
                Column to plot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        #------------------------------> 
        x = self.rDpDF['dfT'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.wPlots.dPlot['Transf'].axes.clear()
        #------------------------------> title
        self.wPlots.dPlot['Transf'].axes.set_title("Transformed")
        #------------------------------> 
        a = self.wPlots.dPlot['Transf'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.wPlots.dPlot['Transf'].axes.set_xlim(*xRange)
        self.wPlots.dPlot['Transf'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.wPlots.dPlot['Transf'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlots.dPlot['Transf'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        self.wPlots.dPlot['Transf'].canvas.draw()
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def PlotdfN(self, col:int) -> bool:
        """Plot the histograms for dfN
    
            Parameters
            ----------
            col : int
                Column to plot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        #------------------------------> 
        x = self.rDpDF['dfN'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.wPlots.dPlot['Norm'].axes.clear()
        #------------------------------> title
        self.wPlots.dPlot['Norm'].axes.set_title("Normalized")
        #------------------------------> 
        a = self.wPlots.dPlot['Norm'].axes.hist(x, bins=nBin, density=True)
        #------------------------------>
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.wPlots.dPlot['Norm'].axes.set_xlim(*xRange)
        self.wPlots.dPlot['Norm'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.wPlots.dPlot['Norm'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlots.dPlot['Norm'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        self.wPlots.dPlot['Norm'].canvas.draw()
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def PlotdfIm(self, col:int) -> bool:
        """Plot the histograms for dfIm
    
            Parameters
            ----------
            col : int
                Column to plot
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        #------------------------------> 
        x = self.rDpDF['dfIm'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.wPlots.dPlot['Imp'].axes.clear()
        #------------------------------> title
        self.wPlots.dPlot['Imp'].axes.set_title("Imputed")
        #------------------------------> 
        a = self.wPlots.dPlot['Imp'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.wPlots.dPlot['Imp'].axes.set_xlim(*xRange)
        self.wPlots.dPlot['Imp'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.wPlots.dPlot['Imp'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.wPlots.dPlot['Imp'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        idx = list(map(int, self.rDpDF['dfS'][self.rDpDF['dfS'].iloc[:,col].isnull()].index.tolist()))
        y = self.rDpDF['dfIm'].iloc[idx,col]
        if not y.empty:
            yBin = dtsStatistic.HistBin(y)[0]
            self.wPlots.dPlot['Imp'].axes.hist(y, bins=yBin, density=False)
        else:
            pass
        #------------------------------> 
        self.wPlots.dPlot['Imp'].canvas.draw()
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def SetText(self, col: int) -> bool:
        """Set the text with the descriptive statistics about the data prepara
            tion steps.
    
            Parameters
            ----------
            col : int
                Column to plot
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(columns=self.cLdfCol)
        df['Data'] = self.cLDFData
        #endregion -------------------------------------------------> Empty DF
        
        #region --------------------------------------------> Calculate values
        for r,k in enumerate(self.rDpDF):
            #------------------------------> N
            df.iat[r,1] = self.rDpDF[k].shape[0]
            #------------------------------> NA
            df.iat[r,2] = self.rDpDF[k].iloc[:,col].isnull().sum()
            #------------------------------> Mean
            df.iat[r,3] = self.rDpDF[k].iloc[:,col].mean()
            #------------------------------> Median
            df.iat[r,4] = self.rDpDF[k].iloc[:,col].median()
            # #------------------------------> SD
            df.iat[r,5] = self.rDpDF[k].iloc[:,col].std()
            # #------------------------------> Kurtosis
            df.iat[r,6] = self.rDpDF[k].iloc[:,col].kurt()
            # #------------------------------> Skewness
            df.iat[r,7] = self.rDpDF[k].iloc[:,col].skew()
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
    
    def UpdateDisplayedData(self, date: Optional[str]=None) -> bool:
        """Update window when a new date is selected.
    
            Parameters
            ----------
            date : str or None
                Given date to plot.
    
            Returns
            -------
            bool
    
            Raise
            -----
            
        """
        #region ---------------------------------------------------> Variables
        if date is not None:
            self.rDpDF = self.rData[date]['DP']
            self.rDateC = date
        else:
            self.rDpDF = self.rData[self.rDateC]['DP']
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl

        #region --------------------------------------------------------> Plot
        for k in self.wPlots.dPlot.keys():
            self.wPlots.dPlot[k].axes.clear()
            self.wPlots.dPlot[k].canvas.draw()
        #endregion -----------------------------------------------------> Plot

        #region ---------------------------------------------------> Text
        self.wText.Clear()
        #endregion ------------------------------------------------> Text

        #region ---------------------------------------------------> Title
        if self.rFromUMSAPFile:
            self.PlotTitle()
        else:
            pass
        #endregion ------------------------------------------------> Title

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---


class UMSAPControl(BaseWindow):
    """Control for an umsap file. 

        Parameters
        ----------
        fileP : Path
            Path to the UMSAP file
        cParent : wx.Window or None
            Parent of the window.

        Attributes
        ----------
        dPlotMethod : dict
            Keys are section names and values the Window to plot the results
        dSectionTab : dict
            Keys are section names and values the corresponding config.name
        rObj : file.UMSAPFile
            Object to handle UMSAP files
        rSection : dict
            Keys are section names and values a reference to the object in the
            tree control.
        rWindow : list[wx.Window]
            List of plot windows associated with this window.
    """
    #region -----------------------------------------------------> Class setup
    cName = config.nwUMSAPControl
    #------------------------------> 
    cSWindow = (400, 700)
    #------------------------------> 
    cFileLabelCheck = ['Data']
    #------------------------------> 
    dPlotMethod = { # Methods to create plot windows
        config.nuCorrA   : CorrAPlot,
        config.nuDataPrep: CheckDataPrep,
        config.nmProtProf: ProtProfPlot,
        config.nmLimProt : LimProtPlot, 
        config.nmTarProt : TarProtPlot,
    }
    #------------------------------> 
    dSectionTab = { # Section name and Tab name correlation
        config.nuCorrA   : config.ntCorrA,
        config.nuDataPrep: config.ntDataPrep,
        config.nmProtProf: config.ntProtProf,
        config.nmLimProt : config.ntLimProt,
        config.nmTarProt : config.ntTarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: Path, cParent: Optional[wx.Window]=None) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        try:
            self.rObj = file.UMSAPFile(fileP)
        except Exception as e:
            raise e
        
        self.cTitle = self.rObj.rFileP.name
        self.rDataInitPath = self.rObj.rFileP.parent / config.fnDataInit
        self.rDataStepPath = self.rObj.rFileP.parent / config.fnDataSteps
        #-------------->  Reference to section items in wxCT.CustomTreeCtrl
        self.rSection = {}
        #------------------------------> Reference to plot windows
        self.rWindow = {}

        super().__init__(cParent=cParent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wTrc = wxCT.CustomTreeCtrl(self)
        self.wTrc.SetFont(config.font['TreeItem'])
        self.SetTree()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer.Add(self.wTrc, 1, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wTrc.Bind(wxCT.EVT_TREE_ITEM_CHECKING, self.OnCheckItem)
        self.wTrc.Bind(wxCT.EVT_TREE_ITEM_HYPERLINK, self.OnHyperLink)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    def OnHyperLink(self, event) -> bool:
        """ Setup analysis.
    
            Parameters
            ----------
            event : wxCT.Event
                Information about the event
    
            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> DateI
        dateI   = event.GetItem()
        section = dateI.GetParent().GetText()
        #endregion ----------------------------------------------------> DateI
        
        #region -------------------------------------------------------> DataI
        dataI = self.rObj.GetDataUser(section, dateI.GetText())
        #endregion ----------------------------------------------------> DataI
        
        #region --------------------------------------------------> Create Tab
        #------------------------------> 
        if config.winMain is None:
            config.winMain = MainWindow()
        else:
            pass
        #------------------------------> 
        config.winMain.OnCreateTab(self.dSectionTab[section], dataI)
        #endregion -----------------------------------------------> Create Tab
        
        return True
    #---
    
    def OnCheckItem(self, event) -> bool:
        """Show window when section is checked
    
            Parameters
            ----------
            event : wxCT.Event
                Information about the event
                
            Returns
            -------
            bool
        """
        #region ------------------------------------------> Get Item & Section
        item    = event.GetItem()
        section = self.wTrc.GetItemText(item)
        #endregion ---------------------------------------> Get Item & Section

        #region ----------------------------------------------> Destroy window
        #------------------------------> Event trigers before checkbox changes
        if self.wTrc.IsItemChecked(item):
            [x.Destroy() for x in self.rWindow[section]]
            event.Skip()
            return True
        else:
            pass
        #endregion -------------------------------------------> Destroy window
        
        #region -----------------------------------------------> Create window
        try:
            self.rWindow[section] = [self.dPlotMethod[section](self)]
        except Exception as e:
            dtscore.Notification('errorU', msg=str(e), tException=e)
            return False
        #endregion --------------------------------------------> Create window
        
        event.Skip()
        return True
    #---
    
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Destroy window and remove reference from config.umsapW
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
                
            Returns
            -------
            bool
        """
        #region -----------------------------------> Update list of open files
        del(config.winUMSAP[self.rObj.rFileP])
        #endregion --------------------------------> Update list of open files
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        #------------------------------> Childs
        for child in dtsGenerator.FindTopLevelChildren(self):
            child.Destroy()
        #------------------------------> Self
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Manage Methods
    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows
            
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        info = method.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables
                
        #region ------------------------------------------------> Set Position
        self.SetPosition(pt=(
            info['D']['xo'] + info['W']['N']*self.cSDeltaWin,
            info['D']['yo'] + info['W']['N']*self.cSDeltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---

    def SetTree(self) -> bool:
        """Set the elements of the wx.TreeCtrl 
        
            Returns
            -------
            bool
        
            Notes
            -----
            See data.file.UMSAPFile for the structure of obj.confTree.
        """
        #region ----------------------------------------------------> Add root
        root = self.wTrc.AddRoot(self.rObj.rFileP.name)
        #endregion -------------------------------------------------> Add root
        
        #region ------------------------------------------------> Add elements
        for a, b in self.rObj.rData.items():
            #------------------------------> Add section node
            childa = self.wTrc.AppendItem(root, a, ct_type=1)
            #------------------------------> Keep reference
            self.rSection[a] = childa
            
            for c, d in b.items():
                #------------------------------> Add date node
                childb = self.wTrc.AppendItem(childa, c)
                self.wTrc.SetItemHyperText(childb, True)

                for e, f in d['I'].items():
                    #------------------------------> Add date items
                    childc = self.wTrc.AppendItem(childb, f"{e}: {f}")
                    #------------------------------> Set font
                    if e.strip() in self.cFileLabelCheck:
                        fileP = self.rDataInitPath/f
                        if fileP.exists():
                            self.wTrc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFile']
                        )
                        else:
                            self.wTrc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFileFalse']
                        )
                    else:		
                        self.wTrc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFile']
                        )
        #endregion ---------------------------------------------> Add elements
        
        #region -------------------------------------------------> Expand root
        self.wTrc.Expand(root)		
        #endregion ----------------------------------------------> Expand root
        
        return True
    #---
    
    def UnCheckSection(self, sectionName: str, win: wx.Window) -> bool:
        """Method to uncheck a section when the plot window is closed by the 
            user
    
            Parameters
            ----------
            sectionName : str
                Section name like in config.nameModules config.nameUtilities
            win : wx.Window
                Window that was closed
                
            Returns
            -------
            bool
        """
        #region --------------------------------------------> Remove from list
        self.rWindow[sectionName].remove(win)
        #endregion -----------------------------------------> Remove from list
        
        #region --------------------------------------------------> Update GUI
        if len(self.rWindow[sectionName]) > 0:
            return True
        else:
            #------------------------------> Remove check
            self.wTrc.SetItem3StateValue(
                self.rSection[sectionName],
                wx.CHK_UNCHECKED,
            )		
            #------------------------------> Repaint
            self.Update()
            self.Refresh()		
            #------------------------------> 
            return True
        #endregion -----------------------------------------------> Update GUI
    #---
    
    def UpdateFileContent(self) -> Literal[True]:
        """Update the content of the file. """
        #region ---------------------------------------------------> Read file
        try:
            self.rObj = file.UMSAPFile(self.rObj.rFileP)
        except Exception as e:
            raise e
        #endregion ------------------------------------------------> Read file

        #region ---------------------------------------------------> 
        self.rSection = {}
        #------------------------------> 
        self.wTrc.DeleteAllItems()
        #------------------------------> 
        self.SetTree()
        #endregion ------------------------------------------------> 

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region -----------------------------------------------------> Get Methods
    def GetCheckedSection(self) -> list[str]:
        """Get a list with the name of all checked sections 
        
            Returns
            -------
            bool
        """
        return [k for k, v in self.rSection.items() if v.IsChecked()]
    #---
    #endregion --------------------------------------------------> Get Methods
#---
#endregion ----------------------------------------------------------> Classes


#region -----------------------------------------------------------> wx.Dialog
class CheckUpdateResult(wx.Dialog):
    """Show a dialog with the result of the check for update operation.
    
        Parameters
        ----------
        cParent : wx widget or None
            To center the dialog in parent. Default None.
        cCheckRes : str or None
            Internet lastest version. Default None.
    """
    #region -----------------------------------------------------> Class setup
    cName = config.ndCheckUpdateResDialog
    #------------------------------> Style
    cStyle = wx.CAPTION|wx.CLOSE_BOX
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: Optional[wx.Window]=None, cCheckRes: Optional[str]=None,
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(cParent, title=config.t[self.cName], style=self.cStyle)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Msg
        if cCheckRes is None:
            msg = 'You are using the latest version of UMSAP.'
        else:
            msg = (f'UMSAP {cCheckRes} is already available.\nYou are '
                f'currently using UMSAP {config.version}.')
        self.wStMsg = wx.StaticText(self, label=msg, style=wx.ALIGN_LEFT)
        #------------------------------> Link	
        if cCheckRes is not None:
            self.wStLink = adv.HyperlinkCtrl(
                self, label='Read the Release Notes.', url=config.urlUpdate)
        else:
            pass
        #------------------------------> Img
        self.wImg = wx.StaticBitmap(
            self, bitmap=wx.Bitmap(str(config.fImgIcon), wx.BITMAP_TYPE_PNG))
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Button Sizers
        self.sBtn = self.CreateStdDialogButtonSizer(wx.OK)
        #------------------------------> TextSizer
        self.sText = wx.BoxSizer(wx.VERTICAL)
        
        self.sText.Add(self.wStMsg, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        if cCheckRes is not None:
            self.sText.Add(self.wStLink, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        else:
            pass
        #------------------------------> Image Sizer
        self.sImg = wx.BoxSizer(wx.HORIZONTAL)
        
        self.sImg.Add(self.wImg, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sImg.Add(
            self.sText, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        #------------------------------> Main Sizer
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sSizer.Add(
            self.sImg, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(
            self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        if cCheckRes is not None:
            self.wStLink.Bind(adv.EVT_HYPERLINK, self.OnLink)
        else:
            pass
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Position & Show
        self.CentreOnParent()
        self.ShowModal()
        self.Destroy()
        #endregion ------------------------------------------> Position & Show
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #------------------------------> Class Methods
    #region ---------------------------------------------------> Event Methods
    def OnLink(self, event: wx.Event) -> Literal[True]:
        """Process the link event.
        
            Parameters
            ----------
            event : wx.adv.HyperlinkEvent
                Information about the event
        """
        #------------------------------> 
        event.Skip()
        self.EndModal(1)
        self.Destroy()
        #------------------------------> 
        return True
    #endregion ------------------------------------------------> Event Methods
#---


class ResControlExp(wx.Dialog):
    """Creates the dialog to type values for Results - Control Experiments

        Parameters
        ----------
        cParent : wx.Panel
            This is the pane calling the dialog.
    """
    #region -----------------------------------------------------> Class setup
    cName = config.ndResControlExp
    #------------------------------> 
    cSize = (900, 580)
    #------------------------------> 
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent:wx.Window):
        """ """
        #region -------------------------------------------------> Check Input
        if (iFile := cParent.wIFile.tc.GetValue())  == '':
            dlg = dtsWindow.FileSelectDialog(
                'openO', config.elData, parent=cParent)
            if dlg.ShowModal() == wx.ID_OK:
                iFile = dlg.GetPath()
                cParent.wIFile.tc.SetValue(iFile)
                dlg.Destroy()
            else:
                dlg.Destroy()
                raise Exception
        else:
            pass
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(
            config.winMain, 
            title = config.t[self.cName],
            style = self.cStyle,
            size  = self.cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.wConf = tab.ResControlExp(self, iFile, cParent)
        #------------------------------> Buttons
        self.sBtn = self.CreateStdDialogButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(self.wConf, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(self.sSizer)
        #endregion ----------------------------------------------------> Sizer
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class Methods
    #region ---------------------------------------------------> Event methods
    def OnOK(self, event: wx.CommandEvent) -> Literal[True]:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
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


class FilterRemoveAny(wx.Dialog):
    """Dialog to select Filters to remove in ProtProfPlot

        Parameters
        ----------
        cFilterList : list
            List of already applied filter, e.g.:
            [['Text', {kwargs} ], ...]
        cParent : wx.Window
            Parent of the window.

        Attributes
        ----------
        rCheckB: list[wx.CheckBox]
            List of wx.CheckBox to show in the window
    """
    #region -----------------------------------------------------> Class setup
    cName = config.ndFilterRemoveAny
    #------------------------------> 
    cSize = (900, 580)
    #------------------------------> 
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cFilterList: list, cParent: Optional[wx.Window]=None) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.rCheckB = []
        
        super().__init__(
            cParent, 
            title = config.t[self.cName],
            style = self.cStyle,
            size  = self.cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(self, label='Select Filters to remove.')
        #------------------------------> 
        for k in cFilterList:
            self.rCheckB.append(wx.CheckBox(
                self, label=f'{k[0]} {k[1].get("gText", "")}'))
        #------------------------------> Buttons
        self.sBtn = self.CreateStdDialogButtonSizer(wx.CANCEL|wx.OK)
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
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        self.EndModal(1)
        self.Close()
    
        return True
    #---
    
    def OnCancel(self, event: wx.CommandEvent) -> bool:
        """The macOs implementation has a bug here that does not discriminate
            between the Cancel and Ok button and always return self.EndModal(1).
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        self.EndModal(0)
        self.Close()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
    
    #region --------------------------------------------------> Manage methods
    def GetChecked(self) -> list[int]:
        """Get the number of the checked wx.CheckBox
    
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


class FilterPValue(dtsWindow.UserInput1Text):
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
        self, cTitle: str, cLabel: str, cHint: str, cParent: wx.Window=None,
        cValidator: wx.Validator=wx.DefaultValidator, cSize: wx.Size=(420, 170),
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(
            title     = cTitle,
            label     = cLabel,
            hint      = cHint,
            parent    = cParent,
            validator = cValidator,
            size      = cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wCbAbs = wx.CheckBox(self, label='Absolute P Value')
        self.wCbLog = wx.CheckBox(self, label='-Log10(P) Value')
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.sCheck = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.sCheck.Add(self.wCbAbs, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sCheck.Add(self.wCbLog, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------> 
        self.Sizer.Detach(self.sizerBtn)
        #------------------------------> 
        self.Sizer.Add(self.sCheck, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.input.tc.Bind(wx.EVT_TEXT, self.OnTextChange)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnTextChange(self, event) -> bool:
        """Select -log10P if the given value is > 1.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Check
        if self.input.tc.GetValidator().Validate()[0]:
            #------------------------------> Get val
            val = float(self.input.tc.GetValue().strip().split(' ')[1])
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
    
    def OnOK(self, event: wx.CommandEvent) -> Literal[True]:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region ----------------------------------------------------> Validate
        #------------------------------> Operand and Value
        tca = self.input.tc.GetValidator().Validate()[0]
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
            self.input.tc.SetValue('')
        #endregion -------------------------------------------------> Validate
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---
#endregion --------------------------------------------------------> wx.Dialog












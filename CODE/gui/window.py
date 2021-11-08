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
import dat4s_core.generator.generator as dtsGenerator
import dat4s_core.data.method as dtsMethod
import dat4s_core.data.statistic as dtsStatistic
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
import gui.menu as menu
import gui.tab as tab
import gui.dtscore as dtscore
import gui.method as method
import gui.pane as pane
import gui.window as window
from data.file import UMSAPFile
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def UpdateCheck(ori: str, win: Optional[wx.Window]=None) -> bool:
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
    #region -------------------------------------------------------> Variables
    url = config.urlUpdate
    msg = f"Check for Updates failed. Please try again later."
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------> Get web page text from Internet
    try:
        r = requests.get(url)
    except Exception as e:
        wx.CallAfter(dtscore.Notification, 'errorU', msg=msg, tException=e)
        return False
    #endregion ------------------------------> Get web page text from Internet
    
    #region --------------------------------------------> Get Internet version
    if r.status_code == requests.codes.ok:
        #------------------------------> 
        text = r.text.split('\n')
        #------------------------------> 
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
        wx.CallAfter(dtscore.Notification, 'errorU', msg=msg)
        return False
    #endregion -----------------------------------------> Get Internet version

    #region -----------------------------------------------> Compare & message
    #--> Compare
    updateAvail = dtsCheck.VersionCompare(versionI, config.version)[0]
    #--> Message
    if updateAvail:
        wx.CallAfter(CheckUpdateResult, parent=win, checkRes=versionI)
    elif not updateAvail and ori == 'menu':
        wx.CallAfter(CheckUpdateResult, parent=win, checkRes=None)
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
        parent : wx.Window or None
            Parent of the window
        menuData : dict
            Data to build the Tool menu of the window. See structure in child 
            class.

        Attributes
        ----------
        parent : wx.Window or None
            Parent of the window
        #------------------------------> Configuration
        name : str
            Unique name of the window. Default is config.nDefName.
        cTitle : str
            Title for the window. Default is config.tdW.
        cSWindow : wx.Size
            Size of the window. Default is config.sWinRegular
        cMsgExportFailed : str
            Error message.
        #------------------------------> Widgets
        statusbar : wx.StatusBar
            Windows statusbar
        menubar : menu.ToolMenuBar
            Menubar for the window with a Tool menu if applicable.
        Sizer : wx.BoxSizer
            Main sizer of the window
    """
    #region -----------------------------------------------------> Class setup
    cMsgExportFailed = (
        f"It was not possible to write the data to the selected file."
    )
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, 
        menuData: Optional[dict]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.parent = parent
        #------------------------------> Def values if not given in child class
        self.cSWindow = getattr(self, 'cSWindow', config.sWinRegular)
        self.cTitle = getattr(
            self, 'cTitle', config.t.get(self.name, config.tdW)
        )
        self.name = getattr(self, 'name', config.nDefName)
        #------------------------------> 
        super().__init__(
            parent, size=self.cSWindow, title=self.cTitle, name=self.name,
        )
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------------------> Widgets
        self.statusbar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.menubar = menu.ToolMenuBar(self.name, menuData)
        self.SetMenuBar(self.menubar)		
        #endregion -----------------------------------------------------> Menu
        
        #region ------------------------------------------------------> Sizers
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Destroy window. Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #region -------------------------------------------> Reduce win number
        try:
            config.winNumber[self.name] -= 1
        except Exception:
            pass
        #endregion ----------------------------------------> Reduce win number
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def OnDupWin(self) -> Literal[True]:
        """Duplicate window. Used by Result windows. Override as needed.
    
            Returns
            -------
            True
        """
        #------------------------------> 
        self.parent.cWindow[self.cSection].append(
            self.parent.cPlotMethod[self.cSection](self.parent)
        )
        #------------------------------> 
        return True
    #---
    
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
        config.winNumber[self.name] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return info
    #---
    
    def OnExportPlotData(self) -> Literal[True]:
        """ Export data to a csv file """
        #region --------------------------------------------------> Dlg window
        dlg = dtsWindow.FileSelectDialog('save', config.elData, parent=self)
        #endregion -----------------------------------------------> Dlg window
        
        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            #------------------------------> Variables
            p     = Path(dlg.GetPath())
            tDate = self.statusbar.GetStatusText(1)
            #------------------------------> Export
            try:
                self.obj.ExportPlotData(self.cSection, tDate, p)
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
    
    def OnExportFilteredData(self) -> Literal[True]:
        """ Export filtered data to a csv file. 
        
            Notes
            -----
            Assumes filtered data is in self.df 
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
                dtsFF.WriteDF2CSV(p, self.df)
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
    
    def OnCheckDataPrep(self, tDate: str) -> bool:
        """Launch the Check Data Preparation Window.
    
            Parameters
            ----------
            
    
            Returns
            -------
            bool
    
            Raise
            -----
            
        """
        CheckDataPrep(f'{self.cSection} - {tDate}', self.data[tDate]['DP'])
        return True
    #---	
    #endregion ------------------------------------------------> Class methods
#---


class BaseWindowPlot(BaseWindow):
    """Base class for windows showing only a plot.

        Parameters
        ----------
        parent : 'UMSAPControl'
            Parent of the window.
        menuData : dict
            Data to build the Tool menu of the window. See structure in child 
            class.
            
        Attributes
        ----------
        cSWindow : wx.Size
            Size of the window.
            
        Notes
        -----
        - Method OnSavePlot assumes that this window has an attribute
        plot (dtsWidget.MatPlotPanel). Override as needed.
        - Method OnClose assumes the parent is an instance of UMSAPControl. 
        Override as needed.
    """
    #region -----------------------------------------------------> Class setup
    cSWindow = config.sWinPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, 
        menuData: Optional[dict]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent, menuData=menuData)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.statusbar.SetFieldsCount(2, config.sbPlot2Fields)
        #endregion --------------------------------------------------> Widgets
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnSavePlot(self) -> bool:
        """Save an image of the plot. Override as needed. 
        
            Notes
            -----
            Assumes window has a plot attribute as in dtsWidget.MatPlotPanel.
        """
        try:
            #------------------------------> 
            self.plot.SaveImage(ext=config.elMatPlotSaveI, parent=self)
            #------------------------------> 
            return True
        except Exception as e:
            #------------------------------> 
            dtscore.Notification(
                'errorF', msg=str(e), tException=e, parent=self,
            )
            #------------------------------> 
            return False
    #---

    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Close window and uncheck section in UMSAPFile window. Assumes 
            self.parent is an instance of UMSAPControl.
            Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #region -----------------------------------------------> Update parent
        self.parent.UnCheckSection(self.cSection, self)		
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.name] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    
    def WinPos(self):
        """Just return base class method result"""
        return super().WinPos()
    #---
    #endregion ------------------------------------------------> Class methods
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
        self, parent: Optional[wx.Window]=None, menuData: Optional[dict]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, menuData=menuData)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> 
        self.statusbar.SetFieldsCount(3, config.sbPlot3Fields)
        #------------------------------>  Plot
        self.plots = dtsWindow.NPlots(
            self, self.cLNPlots, self.cNPlotsCol, statusbar=self.statusbar)
        #------------------------------> Text details
        self.text = wx.TextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.text.SetFont(config.font['SeqAlign'])
        #------------------------------> wx.ListCtrl
        self.lc = pane.ListCtrlSearchPlot(
            self, 
            colLabel = self.cLCol,
            colSize  = self.cSCol,
            style    = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_SINGLE_SEL, 
            tcHint   = f'Search {self.cHSearch}'
        )
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.plots, 
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
            self.text, 
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
            self.lc, 
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

    #region ---------------------------------------------------> Class methods
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
        tStr = self.lc.lcs.search.GetValue()
        iEqual, iSimilar = self.lc.lcs.lc.Search(tStr)
        #endregion ------------------------------------------------> Get index
        
        #region ----------------------------------------------> Show 1 Results
        if len(iEqual) == 1:
            #------------------------------> 
            self.lc.lcs.lc.Select(iEqual[0], on=1)
            self.lc.lcs.lc.EnsureVisible(iEqual[0])
            self.lc.lcs.lc.SetFocus()
            #------------------------------> 
            return True
        elif len(iSimilar) == 1:
            #------------------------------> 
            self.lc.lcs.lc.Select(iSimilar[0], on=1)
            self.lc.lcs.lc.EnsureVisible(iSimilar[0])
            self.lc.lcs.lc.SetFocus()
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
    #endregion ------------------------------------------------> Class methods
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class MainWindow(BaseWindow):
    """Creates the main window of the App.
    
        Parameters
        ----------
        parent : wx widget or None
            Parent of the main window.
        
        Attributes
        ----------
        name : str
            Name to id the window
        tabMethods: dict
            Methods to create the tabs.
        notebook : wx.lib.agw.aui.auibook.AuiNotebook
            Notebook associated with the window
    """
    #region -----------------------------------------------------> Class Setup
    name = config.nwMain
    
    tabMethods = { # Keys are the unique names of the tabs
        config.ntStart   : tab.Start,
        config.ntCorrA   : tab.BaseConfTab,
        config.ntProtProf: tab.BaseConfListTab,
    }
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: Optional[wx.Window]=None) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> StatusBar fields
        self.statusbar.SetFieldsCount(2, config.sSbarFieldSizeI)
        self.statusbar.SetStatusText(f"{config.softwareF} {config.version}", 1)
        #------------------------------> Notebook
        self.notebook = aui.auibook.AuiNotebook(
            self,
            agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------> Create Start Tab
        self.CreateTab(config.ntStart)
        self.notebook.SetCloseButton(0, False)
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
        self.notebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ----------------------------------------------------> Menu methods
    def OnTabClose(self, event: wx.Event) -> Literal[True]:
        """Make sure to show the Start Tab if no other tab exists
        
            Parameters
            ----------
            event : wx.aui.Event
                Information about the event
        """
        #------------------------------> Close Tab
        event.Skip()
        #------------------------------> Number of tabs
        pageC = self.notebook.GetPageCount() - 1
        #------------------------------> Update tabs & close buttons
        if pageC == 1:
            #------------------------------> Remove close button from Start tab
            if (win := self.FindWindowByName(config.ntStart)) is not None:
                self.notebook.SetCloseButton(
                    self.notebook.GetPageIndex(win), 
                    False,
                )
            else:
                pass
        elif pageC == 0:
            #------------------------------> Show Start Tab with close button
            self.CreateTab(config.ntStart)
            self.notebook.SetCloseButton(
                self.notebook.GetPageIndex(
                    self.FindWindowByName(config.ntStart)
                ), 
                False,
            )
        else:
            pass
        
        return True
    #---

    def CreateTab(self, name: str, dataI: Optional[dict]=None) -> Literal[True]:
        """Create a tab.
        
            Parameters
            ----------
            name : str
                One of the values in config.name for tabs
            dataI: dict or None
                Initial data for the tab
        """
        #region -----------------------------------------------------> Get tab
        win = self.FindWindowByName(name)
        #endregion --------------------------------------------------> Get tab
        
        #region ------------------------------------------> Find/Create & Show
        if win is None:
            #------------------------------> Create tab
            self.notebook.AddPage(
                self.tabMethods[name](self.notebook, name, dataI),
                config.t.get(name, config.tdT),
                select = True,
            )
        else:
            #------------------------------> Focus
            self.notebook.SetSelection(self.notebook.GetPageIndex(win))
            #------------------------------> Initial Data
            win.conf.SetInitialData(dataI)
        #endregion ---------------------------------------> Find/Create & Show

        #region ---------------------------------------------------> Start Tab
        if self.notebook.GetPageCount() > 1:
            winS = self.FindWindowByName(config.ntStart)
            if winS is not None:
                self.notebook.SetCloseButton(
                    self.notebook.GetPageIndex(winS), 
                    True,
                )
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> Start Tab
        
        return True
    #---

    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Destroy window and set config.winMain to None.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #------------------------------> 
        self.Destroy()
        #------------------------------> 
        config.winMain = None
        #------------------------------> 
        return True
    #---
    #endregion -------------------------------------------------> Menu methods
#---


class CorrAPlot(BaseWindowPlot):
    """Creates the window showing the results of a correlation analysis.
    
        See Notes below for more details.

        Parameters
        ----------
        parent : 'UMSAPControl'
            Parent of the window

        Attributes
        ----------
        cmap : Matplotlib cmap
            CMAP to use in the plot
        cSection : str
            Section used as source of the data to plot here.
        cTitle : str
            Title of the window.
        data : parent.obj.confData[Section]
            Data for the Correlation Analysis section.
        date : [parent.obj.confData[Section].keys()]
            List of dates availables for plotting.
        name : str
            Unique name of the window.
        obj : parent.obj
            Pointer to the UMSAPFile object in parent. Instead of modifying this
            object here, modify the configure step or add a Get method.
        plot : dtsWidget.MatPlotPanel
            Main plot of the window
            
        Notes
        -----
        The structure of menuData is:
        {
            'menudate' : [list of dates in the section],
        }
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> To id the window
    name = config.nwCorrAPlot
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nuCorrA
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle  = f"{parent.cTitle} - {self.cSection}"
        self.obj     = parent.obj
        self.data    = self.obj.confData[self.cSection]
        self.date    = [x for x in self.data.keys()]
        self.cmap    = dtsMethod.MatplotLibCmap(
            N   = config.color[self.cSection]['CMAP']['N'],
            c1  = config.color[self.cSection]['CMAP']['c1'],
            c2  = config.color[self.cSection]['CMAP']['c2'],
            c3  = config.color[self.cSection]['CMAP']['c3'],
            bad = config.color[self.cSection]['CMAP']['NA'],
        )

        super().__init__(parent, {'menudate' : self.date})
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.plot = dtsWidget.MatPlotPanel(
            self, 
            statusbar    = self.statusbar,
            statusMethod = self.UpdateStatusBar,
            dpi          = config.general['DPI'],
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer.Add(self.plot, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ----------------------------------------------------> Position
        self.Draw(self.date[0], 'Name')
        self.WinPos()
        self.Show()
        #endregion -------------------------------------------------> Position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def WinPos(self) -> Literal[True]:
        """Set the position on the screen and adjust the total number of
            shown windows.
        """
        #region --------------------------------------------------------> Super
        info = super().WinPos()
        #endregion -----------------------------------------------------> Super
        
        #region ------------------------------------------------> Set Position
        self.SetPosition(pt=(
            info['D']['w'] - (info['W']['N']*config.deltaWin + info['W']['w']),
            info['D']['yo'] + info['W']['N']*config.deltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def Draw(self, tDate: str, col: Literal['Name', 'Number']) -> Literal[True]:
        """ Plot data from a given date.
        
            Paramenters
            -----------
            tDate : str
                A date in the section e.g. 20210129-094504
            col: One of Name or Number
                Set the information to display in the axis
        """
        #region --------------------------------------------------------> Plot
        self.plot.axes.pcolormesh(
            self.data[tDate]['DF'], 
            cmap        = self.cmap,
            vmin        = -1,
            vmax        = 1,
            antialiased = True,
            edgecolors  = 'k',
            lw          = 0.005,
        )		
        #endregion -----------------------------------------------------> Plot
        
        #region -------------------------------------------------> Axis & Plot
        #------------------------------> Axis properties
        self.SetAxis(tDate, col)
        #------------------------------> Zoom Out level
        self.plot.ZoomResetSetValues()
        #------------------------------> Draw
        self.plot.canvas.draw()
        #endregion ----------------------------------------------> Axis & Plot

        #region ---------------------------------------------------> Statusbar
        self.statusbar.SetStatusText(tDate, 1)
        #endregion ------------------------------------------------> Statusbar
        
        return True
    #---

    def SetAxis(
        self, tDate: str, col: Literal['Name', 'Number']
        ) -> Literal[True]:
        """ General details of the plot area 
        
            Parameters
            ----------
            tDate : str
                A date in the section e.g. 20210129-094504
            col: One of Name or Number
                Set the information to display in the axis
        """
        #region --------------------------------------------------------> Grid
        self.plot.axes.grid(True)		
        #endregion -----------------------------------------------------> Grid
        
        #region --------------------------------------------------> Axis range
        self.plot.axes.set_xlim(0, self.data[tDate]['NumCol'])
        self.plot.axes.set_ylim(0, self.data[tDate]['NumCol']) 
        #endregion -----------------------------------------------> Axis range
        
        #region ---------------------------------------------------> Variables
        xlabel    = []
        xticksloc = []
        
        if (self.data[tDate]['NumCol']) <= 30:
            step = 1
        elif self.data[tDate]['NumCol'] > 30 and self.data[tDate]['NumCol'] <= 60:
            step = 2
        else:
            step = 3		
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Set ticks
        if col == 'Name':
            for i in range(0, self.data[tDate]['NumCol'], step):
                xticksloc.append(i + 0.5)		
                xlabel.append(self.data[tDate]['DF'].columns[i])
        else:
            for i in range(0, self.data[tDate]['NumCol'], step):
                xticksloc.append(i + 0.5)
                xlabel.append(self.data[tDate]['NumColList'][i])

        self.plot.axes.set_xticks(xticksloc)
        self.plot.axes.set_xticklabels(xlabel, rotation=90)

        self.plot.axes.set_yticks(xticksloc)
        self.plot.axes.set_yticklabels(xlabel)
        #endregion ------------------------------------------------> Set ticks
        
        #region -----------------------------------------------> Adjust figure
        self.plot.figure.subplots_adjust(bottom=0.13)
        #endregion --------------------------------------------> Adjust figure

        return True
    #---

    def UpdateStatusBar(self, event) -> Literal[True]:
        """Update the statusbar info
    
            Parameters
            ----------
            event: matplotlib event
                Information about the event
        """
        #region ---------------------------------------------------> Variables
        tDate = self.statusbar.GetStatusText(1)
        #endregion ------------------------------------------------> Variables
        
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            try:
                #------------------------------> Set variables
                x, y = event.xdata, event.ydata
                xf = int(x)
                xs = self.data[tDate]['DF'].columns[xf]
                yf = int(y)
                ys = self.data[tDate]['DF'].columns[yf]
                zf = '{:.2f}'.format(self.data[tDate]['DF'].iat[yf,xf])
                #------------------------------> Print
                self.statusbar.SetStatusText(
                    f"x = '{str(xs)}'   y = '{str(ys)}'   cc = {str(zf)}"
                )
            except Exception:
                self.statusbar.SetStatusText('')
        else:
            self.statusbar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ProtProfPlot(BaseWindowNPlotLT):
    """Plot results in the Proteome Profiling section of an UMSAP file.

        Parameters
        ----------
        parent : UMSAPControl

        Attributes
        ----------
        name: str
            Name of the window. Default is config.nwProtProf.
        autoFilter : bool
            Apply defined filters (True) when changing date or not (False).
            Default is False. 
        CI : dict
            CI dict for the current date.
        condC : str
            Condiction currently selected.
        corrP : bool
            Use corrected P values (True) or not (False). Default is False. 
        data : dict
            Dict with the configured data for this section from UMSAPFile.
        date : list of str
            List of available dates in the section.
        dateC : str
            Currently seclected date.
        df : pd.DataFrame
            DF with the data currently display in the window.
        fcXLabel : list of str
            List of labels for the x axis in the FC plot.
        fcXRange : list of float
            Min and Max value for the x axis in the FC plot.
        fcYMax : list of float
            Max log2FC value on all conditions for the relevant points.
        fcYMin : list of float
            Min log2FC value on all conditions for the relevant points.
        fcYRange : list of float
            Min and Max value for the y axis in the FC Plot including the CI.
        filterList : list
            List of applied filters. e.g. [['StatusBarText', {kwargs}], ...]
        filterMethod : dict
            Keys are the StatusBar text and values the methods to apply the
            filter.
        getDF4TextInt : dict
            Keys are the type of Control and values methods to create the df
            with the intensities shown in the text region.
        greenP : matplotlib object
            Reference to the green dot shown in the Volcano plot after selecting
            a protein in the wx.ListCtrl.
        lockScale : str
            Lock plot scale to No, Date or Project.
        log10alpha : float
            -log10(alpha) value to plot in the Volcano plot.
        obj : UMSAPFile
            Refernece to the UMSAPFile object.
        protLine : matplotlib object
            Protein line drawn in the FC plot after selecting a protein in the
            wx.ListCtrl.
        rpC : str
            Currently selected relevant point.
        setRange : dict
            Keys are the lockScale values and values methods to set the range.
        showAll : bool
            Show (True) fcYMax and fcYMin in the FC plot or not (False).
            Default is True.
        vXRange : list of float
            Min and Max values for the x axis in the Vol plot.
        vYRange : list of float
            Min and Max values for the y axis in the Vol plot.
        zScore : float
            Z score as absolut value.
        zScoreL : str
            Z score value as percent.
        #------------------------------> Configuration
        cLCol : list of str
            Label for the columns in the wx.ListCtrl
        cLFDiv : str
            StatusBar text for filter Divergent.
        cLFLog2Fc : str
            StatusBar text for filter Log2FC.
        cLFFCUp : str
            Id for the FC Change Above 0 filter.     
        cLFFCUpL : str
            StatusBar text for filter FC Change Above 0.
        cLFFCUpAbs : str
            Id for the FC Change Absolutely Increasing filter.       
        cLFFCUpAbsL : str
            StatusBar text for filter FC Change Absolutely Increasing filter. 
        cLFFCUpMon : str
            Id for the FC Change Monotonically Increasing filter.       
        cLFFCUpMonL  : str
            StatusBar text for filter FC Change Monotonically Increasingly.
        cLFFCDown : str
            Id for the FC Change Below 0 filter.        
        cLFFCDownL : str
            StatusBar text for filter FC Change Below 0.  
        cLFFCDownAbs : str
            Id for the FC Change Absolutely Decreasing filter.     
        cLFFCDownAbsL : str
            StatusBar text for filter FC Change Decreasing Absolutely.
        cLFFCDownMon : str
            Id for the FC Change Decreasing Monotonically filter.     
        cLFFCDownMonL : str
            StatusBar text for filter FC Change Decreasing Monotonically.
        cLFFCBoth : str
            Id for the FC Change Up/Down filter.        
        cLFFCBothL : str
            StatusBar text for filter FC Change Up/Down  
        cLFFCBothAbs : str
            Id for the FC Change Absolutely Up/Down filter.     
        cLFFCBothAbsL : str
            StatusBar text for filter FC Change Absolutely Up/Down
        cLFFCBothMon : str
            Id for the FC Change Monotonically Up/Down filter.     
        cLFFCBothMonL : str
            StatusBar text for filter FC Change Monotonically Up/Down
        cLFFCDict : dict
            Keys are cLFFCUp like and values are cLFFCUpL like
        cLFFCNo : str
            StatusBar text for filter FC No.
        cLFPValAbs : str
            StatusBar Text for filter P values when absolute values are used.
        cLFPValLog : str
            StatusBar Text for filter P values when -log10 values are used.
        cLFZscore : str
            StatusBar text for filter Z Score.
        cSCol : list of int
            Size of the columns in the wx.ListCtrl.
        cSection : str
            Section name. Default is config.nmProtProf.
        cSWindow : wx.Size
            Window size. Default is config.sWinModPlot
        cTitle : str
            Title of the window.
        cTList : str
            Title for the pane showing the wx.ListCtrl and wx.SearchCtrl.
        cTText : str
            Title for the text pane.
        cHSearch : str
            text for the hint in wx.SearchCtrl
        cNPlotsCol : int
            Number of columns in the wx.FlexGrid to distribute the plots.
        cLNPlots : list of str
            IDs of the plots.
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> To id the window
    name = config.nwProtProf
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection      = config.nmProtProf
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
    cLFFCDict = {
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
    cLFFCNo       = 'FC No Change'
    cLFDiv        = 'FC Diverge'
    cLCol         = ['#', 'Gene', 'Protein']
    #--------------> Id of the plots
    cLNPlots      = ['Vol', 'FC']
    #------------------------------> Title
    cTList        = 'Protein List'
    cTText        = 'Profiling details'
    #------------------------------> Sizes
    cSWindow      = config.sWinModPlot
    cSCol         = [45, 70, 100]
    #------------------------------> Hints
    cHSearch      = 'Protein List'
    #------------------------------> Other
    cNPlotsCol    = 2
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: 'UMSAPControl') -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle      = f"{parent.cTitle} - {self.cSection}"
        self.obj         = parent.obj
        self.data        = self.obj.confData[self.cSection]
        self.df          = None
        self.log10alpha  = None
        self.zScore      = stats.norm.ppf(0.9)
        self.zScoreL     = '10%'
        self.dateC       = None
        self.condC       = None
        self.rpC         = None
        self.greenP      = None
        self.corrP       = False
        self.showAll     = True
        self.autoFilter  = False
        self.CI          = None
        self.fcYMax      = None
        self.fcYMin      = None
        self.lockScale   = None
        self.vXRange     = []
        self.vYRange     = []
        self.fcXRange    = []
        self.fcYRange    = []
        self.fcXLabel    = []
        self.protLine    = []
        self.filterList  = []
        self.date, menuData = self.SetDateMenuDate()
        #------------------------------> Methods
        self.setRange = {
            'No'     : self.SetRangeNo,
            'Date'   : self.SetRangeDate,
            'Project': self.SetRangeProject,
        }
        
        self.getDF4TextInt = {
            config.oControlTypeProtProf['OC']   : self.GetDF4TextInt_OC,
            config.oControlTypeProtProf['OCC']  : self.GetDF4TextInt_OCC,
            config.oControlTypeProtProf['OCR']  : self.GetDF4TextInt_OCR,
            config.oControlTypeProtProf['Ratio']: self.GetDF4TextInt_RatioI,
        }
        
        self.cLFFCMode = {
            'Up'  : self.cLFFCUp,
            'Down': self.cLFFCDown,
            'Both': self.cLFFCBoth,
            'No'  : self.cLFFCNo,
        }
        
        self.filterMethod = {
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
        }
        #------------------------------> 
        super().__init__(parent, menuData=menuData, )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        
        #endregion ----------------------------------------------> Aui control

        #region --------------------------------------------------------> Bind
        self.plots.dPlot['Vol'].canvas.mpl_connect('pick_event', self.OnPick)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        #------------------------------> 
        self.OnDateChange(
            self.date[0], 
            menuData['crp'][self.date[0]]['C'][0],
            menuData['crp'][self.date[0]]['RP'][0],
            self.corrP,
            self.showAll,
        )
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    #------------------------------> Filters
    def FilterApply(self) -> bool:
        """Apply all filter to the current date.
    
            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Apply Filters
        for k in self.filterList:
            self.filterMethod[k[0]](**k[1])
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
        self.filterList = []
        self.df = self.data[self.dateC]['DF'].copy()
        self.statusbar.SetStatusText('', 1)
        #endregion ----------------------------------------> Update Attributes
        
        #region --------------------------------------------------> Update GUI
        self.OnDateChange(
            self.dateC, self.condC, self.rpC, self.corrP, self.showAll)
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
        if not self.filterList:
            return True
        else:
            pass
        #endregion --------------------------------> Check Something to Delete
        
        #region -------------------------------------------> Update Attributes
        #------------------------------> 
        del self.filterList[-1]
        self.df = self.data[self.dateC]['DF'].copy()
        #------------------------------> 
        text = self.statusbar.GetStatusText(1)
        text = text.split("|")[0:-1]
        text = [x.strip() for x in text if x.strip() != '']
        if text:
            text = f' | {" | ".join(text)}'
        else:
            text = ''
        self.statusbar.SetStatusText(text, 1)
        #endregion ----------------------------------------> Update Attributes
        
        #region --------------------------------------------------> Update GUI
        self.OnDateChange(
            self.dateC, self.condC, self.rpC, self.corrP, self.showAll)
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
        if not self.filterList:
            return True
        else:
            pass
        #endregion --------------------------------> Check Something to Delete
        
        #region ------------------------------------------------------> Dialog
        dlg = window.FilterRemoveAny(self.filterList, self.plots.dPlot['Vol'])
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
            del self.filterList[k]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------> Update GUI
        if self.filterList:
            #------------------------------> 
            self.df = self.data[self.dateC]['DF'].copy()
            #------------------------------> 
            self.FilterApply()
            #------------------------------> 
            for k in self.filterList:
                #------------------------------> 
                gText = k[1].get("gText", "")
                #------------------------------> 
                if gText:
                    text = f'{text} | {k[0]} {gText}'
                else:
                    text = f'{text} | {k[0]}'
            #------------------------------> 
            self.statusbar.SetStatusText(text, 1)
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
                self.plots.dPlot['Vol'],
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
            self.df = self.df[(
                (self.df.loc[:,col] >= zVal) | (self.df.loc[:,col] <= -zVal)
            ).any(axis=1)]
        else:
            self.df = self.df[(
                (self.df.loc[:,col] <= zVal) | (self.df.loc[:,col] >= -zVal)
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
            self.filterList.append(
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
                self.plots.dPlot['Vol'],
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
            self.df = self.df[(
                (self.df.loc[:,col] <= val) & (self.df.loc[:,col] >= -val)
            ).any(axis=1)]
        else:
            self.df = self.df[(
                (self.df.loc[:,col] >= val) | (self.df.loc[:,col] <= -val)
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
            self.filterList.append(
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
                self.plots.dPlot['Vol'],
                dtsValidator.Comparison(numType='float', op=['<', '>'], vMin=0),
            )
            #------------------------------> 
            if dlg.ShowModal():
                #------------------------------>
                uText = dlg.input.tc.GetValue()
                absB  = dlg.cbAbs.IsChecked()
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
        if self.corrP:
            col = idx[:,:,'Pc']
        else:
            col = idx[:,:,'P']
        #------------------------------> Given value is abs or -log10 P value
        df = self.df.copy()
        if absB:
            pass
        else:
            df.loc[:,col] = -np.log10(df.loc[:,col])
        #------------------------------> 
        if op == '<':
            self.df = self.df[(df.loc[:,col] <= val).any(axis=1)]
        else:
            self.df = self.df[(df.loc[:,col] >= val).any(axis=1)]
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
            self.filterList.append(
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
        df = self.df.loc[:,idx[:,:,'FC']]
        #endregion -------------------------------------------------------> DF
        
        #region ------------------------------------------> Get Value and Plot
        self.df = self.df[df.apply(
            lambda x: any([(x.loc[idx[y,:,'FC']] == 0).all() for y in self.CI['Cond']]), axis=1
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
            self.filterList.append(
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
                parent=self.plots.dPlot['FC'],
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
        df = self.df.loc[:,idx[:,:,'FC']]
        #------------------------------> 
        if choice == self.cLFFCUp:
            self.df = self.df[df.apply(
                lambda x: any([(x.loc[idx[y,:,'FC']] > 0).all() for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCUpAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any([np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) > 0) for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCUpMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any([x.loc[idx[['C',y],:,'FC']].is_monotonic_increasing for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDown:
            self.df = self.df[df.apply(
                lambda x: any([(x.loc[idx[y,:,'FC']] < 0).all() for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDownAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any([np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) < 0) for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCDownMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any([x.loc[idx[['C',y],:,'FC']].is_monotonic_decreasing for y in self.CI['Cond']]), axis=1
            )]
        elif choice == self.cLFFCBoth:
            self.df = self.df[df.apply(
                lambda x: any(
                    [(x.loc[idx[y:,:'FC']] > 0).all() for y in self.CI['Cond']] + 
                    [(x.loc[idx[y:,:'FC']] < 0).all() for y in self.CI['Cond']]
                ), 
                axis=1,
            )]
        elif choice == self.cLFFCBothAbs:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any(
                    [np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) > 0) for y in self.CI['Cond']] + 
                    [np.all(np.diff(x.loc[idx[['C',y],:,'FC']]) < 0) for y in self.CI['Cond']]
                ), 
                axis=1,
            )]
        elif choice == self.cLFFCBothMon:
            df.insert(0, ('C', 'C', 'FC'), 0)
            self.df = self.df[df.apply(
                lambda x: any(
                    [x.loc[idx[['C',y],:,'FC']].is_monotonic_increasing for y in self.CI['Cond']] +
                    [x.loc[idx[['C',y],:,'FC']].is_monotonic_decreasing for y in self.CI['Cond']] 
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
            self.filterList.append(
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
        df = self.df.loc[:,idx[:,:,'FC']]
        #endregion -------------------------------------------------------> DF
        
        #region ------------------------------------------> Get Value and Plot
        self.df = self.df[df.apply(self.Filter_Divergent_Helper, axis=1)]
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
            self.filterList.append(
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
                Row in self.df
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        idx = pd.IndexSlice
        res = []
        #endregion ------------------------------------------------> Variables
        
        #region -----------------------------------------------------> Compare
        for y in self.CI['Cond']:
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
    #------------------------------> 
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
        text_now = self.statusbar.GetStatusText(1)
        #endregion -------------------------------------------------> Old Text
        
        #region ----------------------------------------------------> Add Text
        text_new = f'{text_now} | {text}'
        #endregion -------------------------------------------------> Add Text
        
        #region ------------------------------------------> Add to wx.StatusBar
        self.statusbar.SetStatusText(text_new, 1)
        #endregion ---------------------------------------> Add to wx.StatusBar
        
        return True
    #---
    
    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.date list and the menuData dict needed to build the Tool
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
        for k in self.data.keys():
            #------------------------------> 
            date.append(k)
            #------------------------------> 
            menuData['crp'][k] = {
                'C' : self.obj.data[self.cSection][k]['CI']['Cond'],
                'RP': self.obj.data[self.cSection][k]['CI']['RP']
            }
        #------------------------------> 
        menuData['menudate'] = date
        #endregion ------------------------------------------------> Fill dict
        
        return (date, menuData)
    #---
    
    def WinPos(self) -> Literal[True]:
        """Set the position on the screen and adjust the total number of
            shown windows.
        """
        #region ---------------------------------------------------> Variables
        info = super().WinPos()
        #endregion ------------------------------------------------> Variables
                
        #region ------------------------------------------------> Set Position
        x = info['D']['xo'] + info['W']['N']*config.deltaWin
        y = (
            ((info['D']['h']/2) - (info['W']['h']/2)) 
            + info['W']['N']*config.deltaWin
        )
        self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.name] = info['W']['N'] + 1
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
            Entries are read from self.df
        """
        #region --------------------------------------------------> Delete old
        self.lc.lcs.lc.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old
        
        #region ----------------------------------------------------> Get Data
        data = self.df.iloc[:,0:2]
        data.insert(0, 'kbr', self.df.index.values.tolist())
        data = data.astype(str)
        data = data.values.tolist()
        #endregion -------------------------------------------------> Get Data
        
        #region ------------------------------------------> Set in wx.ListCtrl
        self.lc.lcs.lc.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl
        
        #region ---------------------------------------> Update Protein Number
        self._mgr.GetPane(self.lc).Caption(f'{self.cTList} ({len(data)})')
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
        for c in self.CI['RP']:
            #------------------------------> 
            df = self.data[self.dateC]['DF'].loc[:,idx[:,c,'FC']]
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
        x = self.df.loc[:,[(self.condC,self.rpC,'FC')]]
        #------------------------------> 
        if self.corrP:
            y = -np.log10(
                self.df.loc[:,[(self.condC,self.rpC,'Pc')]])
        else:
            y = -np.log10(
                self.df.loc[:,[(self.condC,self.rpC,'P')]])
        #------------------------------> 
        zFC = self.df.loc[:,[(self.condC,self.rpC,'FCz')]]
        zFC = zFC.squeeze().tolist()
        #-------------->  One item series squeeze to float
        zFC = zFC if type(zFC) == list else [zFC]
        #------------------------------> 
        color = dtsMethod.AssignProperty(
            zFC, config.color[self.name]['Vol'], [-self.zScore, self.zScore])
        #endregion -----------------------------------------------------> Data
        
        #region --------------------------------------------------------> Plot
        self.plots.dPlot['Vol'].axes.scatter(
            x, y, 
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = color,
            picker    = True,
        )
        #------------------------------> Lock Scale or Set it manually
        if self.vXRange and self.vYRange:
            self.plots.dPlot['Vol'].axes.set_xlim(*self.vXRange)
            self.plots.dPlot['Vol'].axes.set_ylim(*self.vYRange)
        else:
            self.VolXYRange(x.squeeze(), y.squeeze())
        #------------------------------> Zoom level
        self.plots.dPlot['Vol'].ZoomResetSetValues()
        #------------------------------> Show
        self.plots.dPlot['Vol'].canvas.draw()
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
        self.plots.dPlot['Vol'].axes.clear()
        #------------------------------> 
        self.plots.dPlot['Vol'].axes.grid(True, linestyle=":")
        self.plots.dPlot['Vol'].axes.axhline(
            y=self.log10alpha, color="black", dashes=(5, 2, 1, 2), alpha=0.5)
        #------------------------------> Labels
        self.plots.dPlot['Vol'].axes.set_title(
            f'C: {self.condC} RP: {self.rpC} ' + 'Z$_{score}$: ' + f'{self.zScoreL}')
        self.plots.dPlot['Vol'].axes.set_xlabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        self.plots.dPlot['Vol'].axes.set_ylabel(
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
        if (idx := self.lc.lcs.lc.GetFirstSelected()) < 0:
            #------------------------------> 
            if self.greenP is None:
                pass
            else:
                self.greenP.remove()
                self.greenP = None
            #------------------------------> 
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index
        
        #region ------------------------------------------------> Volcano Plot
        #------------------------------> Get new data
        x = self.df.at[self.df.index[idx], (self.condC, self.rpC, 'FC')]
        
        if self.corrP:
            y = -np.log10(
                self.df.at[self.df.index[idx], (self.condC, self.rpC, 'Pc')])
        else:
            y = -np.log10(
                self.df.at[self.df.index[idx], (self.condC, self.rpC, 'P')])
        #------------------------------> Remove old point
        if self.greenP is None:
            pass
        else:
            self.greenP.remove()
        #------------------------------> Add new one
        self.greenP = self.plots.dPlot['Vol'].axes.scatter(
            x, y, 
            alpha     = 1,
            edgecolor = 'black',
            linewidth = 1,
            color     = config.color[self.name]['VolSel'],
        )
        #------------------------------> Draw
        self.plots.dPlot['Vol'].canvas.draw()
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
        if self.showAll:
            #------------------------------> 
            color = config.color[self.name]['FCAll']
            x = list(range(0,len(self.fcYMin)))
            #------------------------------> 
            self.plots.dPlot['FC'].axes.plot(self.fcYMax, color=color)
            self.plots.dPlot['FC'].axes.plot(self.fcYMin, color=color)
            #------------------------------> 
            self.plots.dPlot['FC'].axes.fill_between(
                x, self.fcYMax, self.fcYMin, color=color, alpha=0.2)
        else:
            pass
        #------------------------------> Lock Scale
        if self.fcXRange and self.fcYRange:
            self.plots.dPlot['FC'].axes.set_xlim(*self.fcXRange)
            self.plots.dPlot['FC'].axes.set_ylim(*self.fcYRange)
        else:
            xRange, yRange = self.GetFCXYRange(self.dateC)
            self.plots.dPlot['FC'].axes.set_xlim(*xRange)
            self.plots.dPlot['FC'].axes.set_ylim(*yRange)
        #------------------------------> Zoom level
        self.plots.dPlot['FC'].ZoomResetSetValues()
        #------------------------------> 
        self.plots.dPlot['FC'].canvas.draw()
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
        self.plots.dPlot['FC'].axes.clear()
        #endregion ----------------------------------------------------> Clear
        
        #region ------------------------------------------------------> Labels
        self.plots.dPlot['FC'].axes.grid(True, linestyle=":")
        self.plots.dPlot['FC'].axes.set_xlabel('Relevant Points', fontweight="bold")
        self.plots.dPlot['FC'].axes.set_ylabel("log$_{2}$[Fold Change]", fontweight="bold")
        #endregion ---------------------------------------------------> Labels

        #region ---------------------------------------------------> X - Axis
        self.plots.dPlot['FC'].axes.set_xticks(range(0, len(self.fcXLabel), 1))
        self.plots.dPlot['FC'].axes.set_xticklabels(self.fcXLabel)
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
        if (idxl := self.lc.lcs.lc.GetFirstSelected()) < 0:
            #------------------------------> 
            if not self.protLine:
                pass
            else:
                #------------------------------> 
                for k in self.protLine:
                    k[0].remove()
                #------------------------------> 
                self.protLine = []
            #------------------------------> 
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index
        
        #region --------------------------------------------> Remove Old Lines
        #------------------------------> 
        for k in self.protLine:
            k.remove()
        #------------------------------> 
        self.protLine = []
        legend = []
        #endregion -----------------------------------------> Remove Old Lines
        
        #region -----------------------------------------------------> FC Plot
        #------------------------------> Variables
        idx = pd.IndexSlice
        colorN = len(config.color['Main'])
        x = list(range(0, len(self.CI['RP'])+1))
        #------------------------------> 
        for k,c in enumerate(self.CI['Cond']):
            #------------------------------> FC values
            y = self.df.loc[self.df.index[[idxl]],idx[c,:,'FC']]
            y = [0.0] + y.values.tolist()[0]
            #------------------------------> Errors
            yError = self.df.loc[self.df.index[[idxl]],idx[c,:,'CI']]
            yError = [0] + yError.values.tolist()[0]
            #------------------------------> Colors
            color = config.color['Main'][k%colorN]
            #------------------------------> Plot line
            self.protLine.append(
                self.plots.dPlot['FC'].axes.errorbar(
                    x, y, yerr=yError, color=color, fmt='o-', capsize=5
            ))
            #------------------------------> Legend
            legend.append(mpatches.Patch(color=color, label=c))
        #endregion --------------------------------------------------> FC Plot
        
        #region -------------------------------------------------------> Title
        self.plots.dPlot['FC'].axes.set_title(f'Protein {idxl}')
        #endregion ----------------------------------------------------> Title
        
        #region ------------------------------------------------------> Legend
        self.plots.dPlot['FC'].axes.legend(handles=legend, loc='upper left')
        #endregion ---------------------------------------------------> Legend
        
        #region --------------------------------------------------------> Draw
        self.plots.dPlot['FC'].canvas.draw()
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
        if (idx := self.lc.lcs.lc.GetFirstSelected()) < 0:
            #------------------------------> 
            self.text.Freeze()
            self.text.SetValue('')
            self.text.Thaw()
            #------------------------------> 
            return False
        else:
            pass
        #endregion ----------------------------------------------------> Index
        
        #region ---------------------------------------------------> Add Text
        #------------------------------> Delete all
        self.Freeze()
        self.text.SetValue('')
        #------------------------------> Protein ID
        number = self.lc.lcs.lc.GetItemText(idx, col=0)
        gene = self.lc.lcs.lc.GetItemText(idx, col=1)
        name = self.lc.lcs.lc.GetItemText(idx, col=2)
        self.text.AppendText(
            f'--> Selected Protein:\n\n#: {number}, Gene: {gene}, '
            f'Protein ID: {name}\n\n'
        )
        #------------------------------> P and FC values
        self.text.AppendText('--> P and Log2(FC) values:\n\n')
        self.text.AppendText(self.GetDF4TextPFC(idx).to_string(index=False))
        self.text.AppendText('\n\n')
        #------------------------------> Ave and st for intensity values
        self.text.AppendText('--> Intensity values after data preparation:\n\n')
        dfList = self.getDF4TextInt[self.CI['ControlT']](idx)
        for df in dfList:
            self.text.AppendText(df.to_string(index=False))
            self.text.AppendText('\n\n')
        #------------------------------> Go back to begining
        self.text.SetInsertionPoint(0)
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
                To select the protein in self.df
            
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
        dfo = self.GetDF4Text(['FC (CI)', 'P'], self.CI['RP'], self.CI['Cond'])
        #endregion -------------------------------------------------------> DF
        
        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.CI['Cond']):
            for t in self.CI['RP']:
                #------------------------------> Get Values
                p = self.df.at[self.df.index[pID],(c,t,'P')]
                fc = self.df.at[self.df.index[pID],(c,t,'FC')]
                ci = self.df.at[self.df.index[pID],(c,t,'CI')]
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
                To select the protein in self.df
            
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
        aveC = self.df.at[
            self.df.index[pID],(self.CI['Cond'][0], self.CI['RP'][0], 'aveC')]
        stdC = self.df.at[
            self.df.index[pID], (self.CI['Cond'][0], self.CI['RP'][0], 'stdC')]
        #------------------------------> 
        dfc = pd.DataFrame({
            'Condition': self.CI['ControlL'],
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
                To select the protein in self.df
            
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
            ['Ave', 'Std'], self.CI['RP'], self.CI['ControlL']+self.CI['Cond'])
        #endregion -------------------------------------------------------> DF
        
        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for c in self.CI['Cond']:
            for t in self.CI['RP']:
                #------------------------------> Get Values
                aveC = self.df.at[self.df.index[pID],(c,t,'aveC')]
                stdC = self.df.at[self.df.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[0], (t,'Ave')] = aveC
                dfo.at[dfo.index[0], (t,'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.CI['Cond'], start=1):
            for t in self.CI['RP']:
                #------------------------------> Get Values
                ave = self.df.at[self.df.index[pID],(c,t,'ave')]
                std = self.df.at[self.df.index[pID],(c,t,'std')]
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
                To select the protein in self.df
            
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
            ['Ave', 'Std'], self.CI['ControlL']+self.CI['RP'], self.CI['Cond'])
        #endregion -------------------------------------------------------> DF
        
        #region --------------------------------------------------> Add Values
        #------------------------------> Control
        for k,c in enumerate(self.CI['Cond']):
            for t in self.CI['RP']:
                #------------------------------> Get Values
                aveC = self.df.at[self.df.index[pID],(c,t,'aveC')]
                stdC = self.df.at[self.df.index[pID],(c,t,'stdC')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (self.CI['ControlL'],'Ave')] = aveC
                dfo.at[dfo.index[k], (self.CI['ControlL'],'Std')] = stdC
        #------------------------------> Conditions
        for k,c in enumerate(self.CI['Cond']):
            for t in self.CI['RP']:
                #------------------------------> Get Values
                ave = self.df.at[self.df.index[pID],(c,t,'ave')]
                std = self.df.at[self.df.index[pID],(c,t,'std')]
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
                To select the protein in self.df
            
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
        dfo = self.GetDF4Text(['Ave', 'Std'], self.CI['RP'], self.CI['Cond'])
        #endregion -------------------------------------------------------> DF
        
        #region --------------------------------------------------> Add Values
        for k,c in enumerate(self.CI['Cond']):
            for t in self.CI['RP']:
                #------------------------------> Get Values
                ave = self.df.at[self.df.index[pID],(c,t,'ave')]
                std = self.df.at[self.df.index[pID],(c,t,'std')]
                #------------------------------> Assign
                dfo.at[dfo.index[k], (t,'Ave')] = ave
                dfo.at[dfo.index[k], (t,'Std')] = std
        #endregion -----------------------------------------------> Add Values
        
        return [dfo]
    #---
    
    def SetRangeNo(self) -> bool:
        """Do nothing. Just to make the dict self.setRange work.
    
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
        self.vXRange, self.vYRange = self.GetVolXYRange(self.dateC)
        #endregion ------------------------------------------------> Vol Range
        
        #region ----------------------------------------------------> FC Range
        self.fcXRange, self.fcYRange = self.GetFCXYRange(self.dateC)
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
        for date in self.date:
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
        self.vXRange = [-vXLim, vXLim]
        self.vYRange = [vYMin, vYMax]
        
        self.fcXRange = [fcXMin, fcXMax]
        self.fcYRange = [fcYMin, fcYMax]
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
        x = self.data[date]['DF'].loc[:, idx[:,:,'FC']]
        #------------------------------> 
        if self.corrP:
            y = self.data[date]['DF'].loc[:, idx[:,:,'Pc']]
        else:
            y = self.data[date]['DF'].loc[:, idx[:,:,'P']]
        
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
        y = self.data[date]['DF'].loc[:, idx[:,:,'FC']]
        yCI = self.data[date]['DF'].loc[:, idx[:,:,'CI']]
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Get Range
        #------------------------------> X
        #--------------> 
        dm = len(self.CI['RP']) * config.general['MatPlotMargin']
        #--------------> 
        xRange = [-dm, len(self.CI['RP'])+dm]
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
        self.plots.dPlot['Vol'].axes.set_xlim(*xR)
        self.plots.dPlot['Vol'].axes.set_ylim(*yR)
        #endregion ------------------------------------------------> Set Range
        
        return True
    #---
    
    def OnDateChange(
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
        self.dateC   = tDate
        self.condC   = cond
        self.rpC     = rp
        self.corrP   = corrP
        self.showAll = showAll
        self.CI      = self.obj.data[self.cSection][self.dateC]['CI']
        self.df      = self.data[self.dateC]['DF'].copy()
        #endregion -----------------------------------------> Update variables
        
        #region --------------------------------------------------> Update GUI
        if self.autoFilter:
            self.FilterApply()
        else:
            pass
        #------------------------------> Clean & Reload Protein List
        self.FillListCtrl()
        #------------------------------> Alpha
        self.log10alpha = -np.log10(float(self.CI['Alpha']))
        #------------------------------> Update StatusBar
        self.statusbar.SetStatusText(tDate, 2)
        #------------------------------> Clean text
        self.text.SetValue('')
        #endregion -----------------------------------------------> Update GUI
        
        #region -------------------------------------------> Update FC x label
        self.fcXLabel = self.CI['ControlL'] + self.CI['RP']        
        #endregion ----------------------------------------> Update FC x label
        
        #region ---------------------------------------------------> FC minmax
        self.fcYMax, self.fcYMin = self.GetFCMinMax()
        #endregion ------------------------------------------------> FC minmax
        
        #region --------------------------------------------------> Lock Scale
        if self.lockScale is not None:
            self.OnLockScale(self.lockScale)
        else:
            pass
        #endregion -----------------------------------------------> Lock Scale
        
        #region ---------------------------------------------------------> Vol
        self.VolDraw()
        #endregion ------------------------------------------------------> Vol
        
        #region ----------------------------------------------------------> FC
        self.FCDraw()
        #endregion -------------------------------------------------------> FC
        
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
        self.condC   = cond
        self.rpC     = rp
        self.corrP   = corrP
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
        self.showAll = showAll
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
            self.plots.dPlot['Vol'],
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
            self.zScoreL = f'{val}%'
            self.zScore = stats.norm.ppf(1.0-(val/100.0))
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
        return self.plots.dPlot['Vol'].SaveImage(
            config.elMatPlotSaveI, parent=self.plots.dPlot['Vol']
        )
    #---
    
    def OnSaveFCImage(self) -> bool:
        """Save an image of the volcano plot.
    
            Returns
            -------
            bool
        """
        return self.plots.dPlot['FC'].SaveImage(
            config.elMatPlotSaveI, parent=self.plots.dPlot['FC']
        )
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
            self.lc.lcs.lc.Select(ind[0], on=1)
            self.lc.lcs.lc.EnsureVisible(ind[0])
            self.lc.lcs.lc.SetFocus()
        else:
            #------------------------------> Disconnect events to avoid zoom in
            # while interacting with the modal window
            self.plots.dPlot['Vol'].DisconnectEvent()
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
                parent     = self.plots.dPlot['Vol'],
            )
            #------------------------------> Reconnect event
            self.plots.dPlot['Vol'].ConnectEvent()
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
        return self.plots.dPlot['Vol'].ZoomResetPlot()
    #---
    
    def OnZoomResetFC(self) -> bool:
        """Reset the zoom level in the FC plot.
    
            Returns
            -------
            bool
        """
        return self.plots.dPlot['FC'].ZoomResetPlot()
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
        self.lockScale = mode
        self.vXRange   = []
        self.vYRange   = []
        self.fcXRange  = []
        self.fcYRange  = []
        #endregion ----------------------------------------------> Update Attr
        
        #region ---------------------------------------------------> Get Range
        self.setRange[mode]()
        #endregion ------------------------------------------------> Get Range
        
        #region ---------------------------------------------------> Set Range
        if updatePlot:
            #------------------------------> Vol
            #--------------> 
            self.plots.dPlot['Vol'].axes.set_xlim(*self.vXRange)
            self.plots.dPlot['Vol'].axes.set_ylim(*self.vYRange)
            #--------------> 
            self.plots.dPlot['Vol'].canvas.draw()
            #--------------> 
            self.plots.dPlot['Vol'].ZoomResetSetValues()
            #------------------------------> FC
            #--------------> 
            self.plots.dPlot['FC'].axes.set_xlim(*self.fcXRange)
            self.plots.dPlot['FC'].axes.set_ylim(*self.fcYRange)
            #--------------> 
            self.plots.dPlot['FC'].canvas.draw()
            #--------------> 
            self.plots.dPlot['FC'].ZoomResetSetValues()
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
        self.autoFilter = mode
        return True
    #---
    
    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Close window and uncheck section in UMSAPFile window. Assumes 
            self.parent is an instance of UMSAPControl.
            Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #region -----------------------------------------------> Update parent
        self.parent.UnCheckSection(self.cSection, self)		
        #endregion --------------------------------------------> Update parent
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.name] -= 1
        #endregion ---------------------------------> Reduce number of windows
        
        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class CheckDataPrep(BaseWindowNPlotLT):
    """window to check the data preparation steps

        Parameters
        ----------
        title : str
            Title of the window

        Attributes
        ----------
        

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = config.nwCheckDataPrep
    #------------------------------> Label
    cLNPlots = ['Init', 'Transf', 'Norm', 'Imp']
    cLCol = ['#', 'Name']
    cLdfCol = config.dfcolDataCheck
    cTList = 'Column names'
    cTText = 'Statistic information'
    #------------------------------> Size
    cSCol = [45, 100]
    #------------------------------> Hint
    cHSearch = 'Colum names'
    #------------------------------> Lists
    ltDFData = ['Filtered', 'Transformed', 'Normalized', 'Imputed']
    #------------------------------> Other
    cNPlotsCol = 2
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, title, dpDF):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.cTitle = title
        self.dpDF = dpDF
        
        # if config.development:
        #     for k,v in self.dpDF.items():
        #         print(f'{k}:\n{v.head()}')
        #------------------------------> 
        super().__init__()
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
        self.FillListCtrl()
        #------------------------------> 
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def WinPos(self) -> Literal[True]:
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
        config.winNumber[self.name] = info['W']['N'] + 1
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
            Entries are read from self.df
        """
        #region --------------------------------------------------> Delete old
        self.lc.lcs.lc.DeleteAllItems()
        #endregion -----------------------------------------------> Delete old
        
        #region ----------------------------------------------------> Get Data
        data = [[str(k), n] for k,n in enumerate(self.dpDF['dfS'].columns.values.tolist())]
        #endregion -------------------------------------------------> Get Data
        
        #region ------------------------------------------> Set in wx.ListCtrl
        self.lc.lcs.lc.SetNewData(data)
        #endregion ---------------------------------------> Set in wx.ListCtrl
        
        #region ---------------------------------------> Update Protein Number
        self._mgr.GetPane(self.lc).Caption(f'{self.cTList} ({len(data)})')
        self._mgr.Update()
        #endregion ------------------------------------> Update Protein Number
        
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
        x = self.dpDF['dfS'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Plot
        #------------------------------> 
        self.plots.dPlot['Init'].axes.clear()
        #------------------------------> title
        self.plots.dPlot['Init'].axes.set_title("Filtered")
        #------------------------------> 
        a = self.plots.dPlot['Init'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        self.plots.dPlot['Init'].axes.set_xlim(*dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin']))
        self.plots.dPlot['Init'].ZoomResetSetValues()
        #------------------------------> 
        self.plots.dPlot['Init'].canvas.draw()
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
        x = self.dpDF['dfT'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.plots.dPlot['Transf'].axes.clear()
        #------------------------------> title
        self.plots.dPlot['Transf'].axes.set_title("Transformed")
        #------------------------------> 
        a = self.plots.dPlot['Transf'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.plots.dPlot['Transf'].axes.set_xlim(*xRange)
        self.plots.dPlot['Transf'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.plots.dPlot['Transf'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.plots.dPlot['Transf'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        self.plots.dPlot['Transf'].canvas.draw()
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
        x = self.dpDF['dfN'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.plots.dPlot['Norm'].axes.clear()
        #------------------------------> title
        self.plots.dPlot['Norm'].axes.set_title("Normalized")
        #------------------------------> 
        a = self.plots.dPlot['Norm'].axes.hist(x, bins=nBin, density=True)
        #------------------------------>
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.plots.dPlot['Norm'].axes.set_xlim(*xRange)
        self.plots.dPlot['Norm'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.plots.dPlot['Norm'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.plots.dPlot['Norm'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        self.plots.dPlot['Norm'].canvas.draw()
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
        x = self.dpDF['dfIm'].iloc[:,col]
        x = x[np.isfinite(x)]        
        #------------------------------> 
        nBin = dtsStatistic.HistBin(x)[0]
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------------> Draw
        #------------------------------> 
        self.plots.dPlot['Imp'].axes.clear()
        #------------------------------> title
        self.plots.dPlot['Imp'].axes.set_title("Imputed")
        #------------------------------> 
        a = self.plots.dPlot['Imp'].axes.hist(x, bins=nBin, density=True)
        #------------------------------> 
        xRange = dtsStatistic.DataRange(
            a[1], margin=config.general['MatPlotMargin'])
        self.plots.dPlot['Imp'].axes.set_xlim(*xRange)
        self.plots.dPlot['Imp'].axes.set_ylim(*dtsStatistic.DataRange(
            a[0], margin=config.general['MatPlotMargin']))
        self.plots.dPlot['Imp'].ZoomResetSetValues()
        #------------------------------> 
        gausX = np.linspace(xRange[0], xRange[1], 300)
        gausY = stats.gaussian_kde(x)
        self.plots.dPlot['Imp'].axes.plot(gausX, gausY.pdf(gausX))
        #------------------------------> 
        idx = list(map(int, self.dpDF['dfS'][self.dpDF['dfS'].iloc[:,col].isnull()].index.tolist()))
        y = self.dpDF['dfIm'].iloc[idx,col]
        if not y.empty:
            yBin = dtsStatistic.HistBin(y)[0]
            self.plots.dPlot['Imp'].axes.hist(y, bins=yBin, density=False)
        else:
            pass
        #------------------------------> 
        self.plots.dPlot['Imp'].canvas.draw()
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def SetText(self, col: int) -> bool:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(columns=self.cLdfCol)
        df['Data'] = self.ltDFData
        #endregion -------------------------------------------------> Empty DF
        
        #region --------------------------------------------> Calculate values
        for r,k in enumerate(self.dpDF):
            #------------------------------> N
            df.iat[r,1] = self.dpDF[k].shape[0]
            #------------------------------> NA
            df.iat[r,2] = self.dpDF[k].iloc[:,col].isnull().sum()
            #------------------------------> Mean
            df.iat[r,3] = self.dpDF[k].iloc[:,col].mean()
            #------------------------------> Median
            df.iat[r,4] = self.dpDF[k].iloc[:,col].median()
            # #------------------------------> SD
            df.iat[r,5] = self.dpDF[k].iloc[:,col].std()
            # #------------------------------> Kurtosis
            df.iat[r,6] = self.dpDF[k].iloc[:,col].kurt()
            # #------------------------------> Skewness
            df.iat[r,7] = self.dpDF[k].iloc[:,col].skew()
        #endregion -----------------------------------------> Calculate values
        
        #region ---------------------------------------------> Remove Old Text
        self.text.Clear()
        #endregion ------------------------------------------> Remove Old Text
        
        #region ------------------------------------------------> Add New Text
        self.text.AppendText(df.to_string(index=False))
        self.text.SetInsertionPoint(0)
        #endregion ---------------------------------------------> Add New Text
        
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
            
    
            Raise
            -----
            
        """
        #region ------------------------------------------------> Get Selected
        idx = self.lc.lcs.lc.GetFirstSelected()
        #endregion ---------------------------------------------> Get Selected
        
        #region ---------------------------------------------------------> dfS
        try:
            self.PlotdfS(idx)
        except Exception as e:
            #------------------------------> 
            msg = (
                f'It was not possible to build the histograms for the selected '
                f'columns.')
            dtscore.Notification('errorU', msg=msg, tException=e, parent=self)
            #------------------------------> 
            for p in self.cLNPlots:
                self.plots.dPlot[p].axes.clear()
                self.plots.dPlot[p].canvas.draw()
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
    #endregion ------------------------------------------------> Class methods
#---


class UMSAPControl(BaseWindow):
    """Control for an umsap file. 

        Parameters
        ----------
        obj : file.UMSAPFile
            UMSAP File obj for the window
        shownSection : list of str or None
            If called from Update File Content menu list the sections that were
            checked when starting the update
        parent : wx.Window or None
            Parent of the window.

        Attributes
        ----------
        cFileLabelCheck : list[str]
            Elements are keys in the user input dictionary of the section of the 
            UMSAP file being shown in the window. The corresponding values
            will be check as valid path to files when filing the tree in the 
            window.
        cPlotMethod : dict
            Keys are section names and values the Window to plot the results
        cSection : dict
            Keys are section names and values a reference to the object in the
            tree control.
        cSectionTab : dict
            Keys are section names and values the corresponding config.name
        cSWindow : wx.Size
            Size of the window.
        cTitle: str
            Title of the window.
        cWindow : list[wx.Window]
            List of plot windows associated with this window.
        name : str
            Name of the window. Basically fileP.name
        obj : file.UMSAPFile
            Object to handle UMSAP files
        trc : wxCT.CustomTreeCtrl
            Tree control to show the content of the umsap file.
    """
    #region -----------------------------------------------------> Class setup
    name = config.nwUMSAPControl
    
    cSWindow = (400, 700)
    
    cPlotMethod = { # Methods to create plot windows
        config.nuCorrA   : CorrAPlot,
        config.nmProtProf: ProtProfPlot,
    }
    
    cFileLabelCheck = ['Data File']
    
    cSectionTab = { # Section name and Tab name correlation
        config.nuCorrA   : config.ntCorrA,
        config.nmProtProf: config.ntProtProf,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, obj: UMSAPFile, shownSection: Optional[list[str]]=None, 
        parent: Optional[wx.Window]=None,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.obj    = obj
        self.cTitle = self.obj.fileP.name
        #-------------->  Reference to section items in wxCT.CustomTreeCtrl
        self.cSection = {}
        #------------------------------> Reference to plot windows
        self.cWindow = {}

        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.trc = wxCT.CustomTreeCtrl(self)
        self.trc.SetFont(config.font['TreeItem'])
        self.SetTree()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer.Add(self.trc, 1, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.trc.Bind(wxCT.EVT_TREE_ITEM_CHECKING, self.OnCheckItem)
        self.trc.Bind(wxCT.EVT_TREE_ITEM_HYPERLINK, self.OnHyperLink)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position

        #region ----------------------------------------> Show opened Sections
        if shownSection is not None:
            for k in shownSection:
                try:
                    self.trc.CheckItem(self.cSection[k], checked=True)
                except Exception:
                    pass
        else:
            pass
        #endregion -------------------------------------> Show opened Sections
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def WinPos(self) -> Literal[True]:
        """Set the position on the screen and adjust the total number of
            shown windows
        """
        #region ---------------------------------------------------> Variables
        info = method.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables
                
        #region ------------------------------------------------> Set Position
        self.SetPosition(pt=(
            info['D']['xo'] + info['W']['N']*config.deltaWin,
            info['D']['yo'] + info['W']['N']*config.deltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.name] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---

    def SetTree(self) -> Literal[True]:
        """Set the elements of the wx.TreeCtrl 
        
            Notes
            -----
            See data.file.UMSAPFile for the structure of obj.confTree.
        """
        #region ----------------------------------------------------> Add root
        root = self.trc.AddRoot(self.obj.fileP.name)
        #endregion -------------------------------------------------> Add root
        
        #region ------------------------------------------------> Add elements
        for a, b in self.obj.data.items():
            #------------------------------> Add section node
            if self.obj.confTree['Sections'][a]:
                childa = self.trc.AppendItem(root, a, ct_type=1)
            else:
                childa = self.trc.AppendItem(root, a, ct_type=0)
                self.trc.SetItemFont(childa, config.font['TreeItemFalse'])
            #------------------------------> Keep reference
            self.cSection[a] = childa
            
            for c, d in b.items():
                #------------------------------> Add date node
                childb = self.trc.AppendItem(childa, c)
                self.trc.SetItemHyperText(childb, True)
                #------------------------------> Set font
                if self.obj.confTree[a][c]:
                    pass
                else:
                    self.trc.SetItemFont(childb, config.font['TreeItemFalse'])

                for e, f in d['I'].items():
                    #------------------------------> Add date items
                    childc = self.trc.AppendItem(childb, f"{e}: {f}")
                    #------------------------------> Set font
                    if e.strip() in self.cFileLabelCheck:
                        if Path(f).exists():
                            self.trc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFile']
                        )
                        else:
                            self.trc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFileFalse']
                        )
                    else:		
                        self.trc.SetItemFont(
                            childc, 
                            config.font['TreeItemDataFile']
                        )
        #endregion ---------------------------------------------> Add elements
        
        #region -------------------------------------------------> Expand root
        self.trc.Expand(root)		
        #endregion ----------------------------------------------> Expand root
        
        return True
    #---
    
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
        dataI = self.obj.GetDataUser(section, dateI.GetText())
        #endregion ----------------------------------------------------> DataI
        
        #region --------------------------------------------------> Create Tab
        #------------------------------> 
        if config.winMain is None:
            config.winMain = MainWindow()
        else:
            pass
        #------------------------------> 
        config.winMain.CreateTab(self.cSectionTab[section], dataI)
        #endregion -----------------------------------------------> Create Tab
        
        return True
    #---

    def OnCheckItem(self, event) -> bool:
        """Show window when section is checked
    
            Parameters
            ----------
            event : wxCT.Event
                Information about the event
        """
        #region ------------------------------------------> Get Item & Section
        item    = event.GetItem()
        section = self.trc.GetItemText(item)
        #endregion ---------------------------------------> Get Item & Section

        #region ----------------------------------------------> Destroy window
        #------------------------------> Event trigers before checkbox changes
        if self.trc.IsItemChecked(item):
            [x.Destroy() for x in self.cWindow[section]]
            event.Skip()
            return True
        else:
            pass
        #endregion -------------------------------------------> Destroy window
        
        #region -----------------------------------------------> Create window
        try:
            self.cWindow[section] = [self.cPlotMethod[section](self)]
        except Exception as e:
            dtscore.Notification('errorU', msg=str(e), tException=e)
            return False
        #endregion --------------------------------------------> Create window
        
        event.Skip()
        return True
    #---

    def UnCheckSection(self, sectionName: str, win: wx.Window) -> Literal[True]:
        """Method to uncheck a section when the plot window is closed by the 
            user
    
            Parameters
            ----------
            sectionName : str
                Section name like in config.nameModules config.nameUtilities
            win : wx.Window
                Window that was closed
        """
        #region --------------------------------------------> Remove from list
        self.cWindow[sectionName].remove(win)
        #endregion -----------------------------------------> Remove from list
        
        #region --------------------------------------------------> Update GUI
        if len(self.cWindow[sectionName]) > 0:
            return True
        else:
            #------------------------------> Remove check
            self.trc.SetItem3StateValue(
                self.cSection[sectionName],
                wx.CHK_UNCHECKED,
            )		
            #------------------------------> Repaint
            self.Update()
            self.Refresh()		
            #------------------------------> 
            return True
        #endregion -----------------------------------------------> Update GUI
    #---

    def GetCheckedSection(self) -> list[str]:
        """Get a list with the name of all checked sections """
        return [k for k, v in self.cSection.items() if v.IsChecked()]
    #---
    
    def OnClose(self, event: wx.CloseEvent) -> Literal[True]:
        """Destroy window and remove reference from config.umsapW
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
        """
        #region -----------------------------------> Update list of open files
        del(config.winUMSAP[self.obj.fileP])
        #endregion --------------------------------> Update list of open files
        
        #region ------------------------------------> Reduce number of windows
        config.winNumber[self.name] -= 1
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

    def UpdateFileContent(self) -> Literal[True]:
        """Update the content of the file. """
        #------------------------------> 
        method.LoadUMSAPFile(
            fileP        = self.obj.fileP,
            shownSection = self.GetCheckedSection(),
        )
        #------------------------------> 
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


#region -----------------------------------------------------------> wx.Dialog
class CheckUpdateResult(wx.Dialog):
    """Show a dialog with the result of the check for update operation.
    
        Parameters
        ----------
        parent : wx widget or None
            To center the dialog in parent. Default None
        checkRes : str or None
            Internet lastest version. Default None

        Attributes
        ----------
        name : str
            Unique window id
    """
    #region -----------------------------------------------------> Class setup
    name = config.ndCheckUpdateResDialog
    #------------------------------> Style
    cStyle = wx.CAPTION|wx.CLOSE_BOX
    #------------------------------> Label
    clLatest = "You are using the latest version of UMSAP."
    clLink   = 'Read the Release Notes.'
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, checkRes: Optional[str]=None,
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent, title=config.t[self.name], style=self.cStyle)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Msg
        if checkRes is None:
            msg = self.clLatest
        else:
            msg = (
                f"UMSAP {checkRes} is already available.\n"
                f"You are currently using UMSAP {config.version}."
            )
        self.stMsg = wx.StaticText(
            self, 
            label = msg,
            style = wx.ALIGN_LEFT,
        )
        #------------------------------> Link	
        if checkRes is not None:
            self.stLink = adv.HyperlinkCtrl(
                self,
                label = self.clLink,
                url   = config.urlUpdate,
            )
        else:
            pass
        #------------------------------> Img
        self.img = wx.StaticBitmap(
            self,
            bitmap = wx.Bitmap(str(config.fImgIcon), wx.BITMAP_TYPE_PNG),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Button Sizers
        self.btnSizer = self.CreateStdDialogButtonSizer(wx.OK)
        #------------------------------> TextSizer
        self.tSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tSizer.Add(self.stMsg, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        if checkRes is not None:
            self.tSizer.Add(self.stLink, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        else:
            pass
        #------------------------------> Image Sizer
        self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.imgSizer.Add(self.img, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.imgSizer.Add(self.tSizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        #------------------------------> Main Sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.Sizer.Add(self.imgSizer, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.SetSizer(self.Sizer)
        self.Sizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        if checkRes is not None:
            self.stLink.Bind(adv.EVT_HYPERLINK, self.OnLink)
        else:
            pass
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Position & Show
        if parent is None:
            self.CenterOnScreen()
        else:
            self.CentreOnParent()
        self.ShowModal()
        self.Destroy()
        #endregion ------------------------------------------> Position & Show
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #region ---------------------------------------------------> Class Methods
    def OnLink(self, event) -> Literal[True]:
        """Process the link event.
        
            Parameters
            ----------
            event : wx.adv.Event
                Information about the event
        """
        #------------------------------> 
        event.Skip()
        self.EndModal(1)
        self.Destroy()
        #------------------------------> 
        return True
    #endregion ------------------------------------------------> Class Methods
#---


class ResControlExp(wx.Dialog):
    """Creates the dialog to type values for Results - Control Experiments

        Parameters
        ----------
        parent : wx.Panel
            This is the pane calling the dialog.

        Attributes
        ----------
        name : str
            Name of the window
        conf :  pane.ResControlExp
            Contains all widgets except the Ok, Cancel buttons.

        Raises
        ------
        Exception
            - When no Data file is selected.
    """
    #region -----------------------------------------------------> Class setup
    name = config.ndResControlExp
    #------------------------------> 
    cSize = (900, 580)
    #------------------------------> 
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window):
        """ """
        #region -------------------------------------------------> Check Input
        if (iFile := parent.iFile.tc.GetValue())  == '':
            dlg = dtsWindow.FileSelectDialog(
                'openO', config.elData, parent=parent,
            )
            if dlg.ShowModal() == wx.ID_OK:
                iFile = dlg.GetPath()
                parent.iFile.tc.SetValue(iFile)
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
            title = config.t[self.name],
            style = self.cStyle,
            size  = self.cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.conf = tab.ResControlExp(self, iFile, parent)
        #------------------------------> Buttons
        self.sizerBtn = self.CreateStdDialogButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.conf, 1, wx.EXPAND|wx.ALL, 5)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #endregion ----------------------------------------------------> Sizer
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
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
        if self.conf.conf.OnOK():
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion ------------------------------------------------> 
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FilterRemoveAny(wx.Dialog):
    """Dialog to select Filters to remove in ProtProfPlot

        Parameters
        ----------
        filterList : list
            List of already applied filter, e.g.:
            [['Text', {kwargs} ], ...]
        parent : wx.Window
            Parent of the window.

        Attributes
        ----------
        name : str
            Name of the window. Default is config.ndFilterRemoveAny.
        #------------------------------> Configuration
        cSize : wx.Size
            Size of the wx.Dialog
        cStyle : wx.Style
            Style of the wx.Dialog.
        #------------------------------> Widgets
        checkB : list of wx.CheckBox
            Checkboxes with the applied filters.
    """
    #region -----------------------------------------------------> Class setup
    name = config.ndFilterRemoveAny
    #------------------------------> 
    cSize = (900, 580)
    #------------------------------> 
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, filterList: list, parent: Optional[wx.Window]=None) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        self.checkB = []
        
        super().__init__(
            parent, 
            title = config.t[self.name],
            style = self.cStyle,
            size  = self.cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.st = wx.StaticText(self, label='Select Filters to remove.')
        #------------------------------> 
        for k in filterList:
            self.checkB.append(wx.CheckBox(
                self, label=f'{k[0]} {k[1].get("gText", "")}'))
        #------------------------------> Buttons
        self.sizerBtn = self.CreateStdDialogButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        #------------------------------> 
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        #------------------------------> 
        self.Sizer.Add(self.st, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        for k in self.checkB:
            self.Sizer.Add(k, 0 , wx.ALIGN_LEFT|wx.ALL, 5)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------> 
        self.SetSizer(self.Sizer)
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

    #region ---------------------------------------------------> Class methods
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
        self.EndModal(1)
        self.Close()
    
        return True
    #---
    
    def OnCancel(self, event: wx.CommandEvent) -> Literal[True]:
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
        for k,cb in enumerate(self.checkB):
            lo.append(k) if cb.IsChecked() else None
        #endregion ----------------------------------------------> Get Checked
        
        return lo
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FilterPValue(dtsWindow.UserInput1Text):
    """Dialog to filter values by P value.

        Parameters
        ----------
        title : str
            Title of the wx.Dialog
        label : str
            Label for the wx.StaticText
        hint : str
            Hint for the wx.TextCtrl.
        parent : wx.Window
            Parent of the wx.Dialog
        validator : wx.Validator
            Validator for the wx.TextCtrl
        size : wx.Size
            Size of the wx.Dialog. Default is (420, 170) 
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, title: str, label: str, hint: str, parent: wx.Window=None,
        validator: wx.Validator=wx.DefaultValidator, size: wx.Size=(420, 170),
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(title=title, label=label, hint=hint, parent=parent,
            validator=validator, size=size
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.cbAbs = wx.CheckBox(self, label='Absolute P Value')
        self.cbLog = wx.CheckBox(self, label='-Log10(P) Value')
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.checkSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.checkSizer.Add(self.cbAbs, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.checkSizer.Add(self.cbLog, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------> 
        self.Sizer.Detach(self.sizerBtn)
        #------------------------------> 
        self.Sizer.Add(self.checkSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.input.tc.Bind(wx.EVT_TEXT, self.OnTextChange)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
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
                self.cbAbs.SetValue(False)
                self.cbLog.SetValue(True)
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
        absB = self.cbAbs.IsChecked()
        logB = self.cbLog.IsChecked()
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
    #endregion ------------------------------------------------> Class methods
#---
#endregion --------------------------------------------------------> wx.Dialog












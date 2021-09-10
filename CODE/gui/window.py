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

import numpy as np
import requests
from scipy import stats
import wx
import wx.adv as adv
import wx.lib.agw.aui as aui
import wx.lib.agw.customtreectrl as wxCT

import dat4s_core.data.check as dtsCheck
import dat4s_core.generator.generator as dtsGenerator
import dat4s_core.data.method as dtsMethod
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
from data.file import UMSAPFile
import gui.menu as menu
import gui.tab as tab
import gui.dtscore as dtscore
import gui.method as method
import gui.pane as pane
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
        #------------------------------> Widgets
        statusbar : wx.StatusBar
            Windows statusbar
        menubar : menu.ToolMenuBar
            Menubar for the window with a Tool menu if applicable.
        Sizer : wx.BoxSizer
            Main sizer of the window
    """
    #region -----------------------------------------------------> Class setup
    
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
        self.statusbar.SetFieldsCount(2, config.sbPlot)
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
        msgExportFailed : str
            Error message.
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
    #------------------------------> 
    msgExportFailed = (
        f"It was not possible to write the data to the selected file."
    )
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
            N  = config.color[self.cSection]['CMAP']['N'],
            c1 = config.color[self.cSection]['CMAP']['c1'],
            c2 = config.color[self.cSection]['CMAP']['c2'],
            c3 = config.color[self.cSection]['CMAP']['c3'],
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
        #region ---------------------------------------------------> Variables
        info = method.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables
                
        #region ------------------------------------------------> Set Position
        self.SetPosition(pt=(
            info['D']['w'] - (info['W']['N']*config.deltaWin + info['W']['w']),
            info['D']['yo'] + info['W']['N']*config.deltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.name] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

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
                    msg        = self.msgExportFailed,
                    tException = e,
                    parent     = self,
                )
        else:
            pass
        #endregion ------------------------------------------------> Get Path
     
        dlg.Destroy()
        
        return True	
     #---
    #---	
    #endregion ------------------------------------------------> Class methods
#---


class ProtProfPlot(BaseWindow):
    """Plot results in the Proteome Profiling section of an UMSAP file.

        Parameters
        ----------
        

        Attributes
        ----------
        

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> To id the window
    name = config.nwProtProf
    #------------------------------> To id the section in the umsap file 
    # shown in the window
    cSection = config.nmProtProf
    cSWindow = config.sWinModPlot
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
        self.log10alpha  = None
        self.zScore      = stats.norm.ppf(0.9)
        self.zScoreL     = '10%'
        self.dateC       = None
        self.condC       = None
        self.rpC         = None
        self.corrP       = False
        self.date, menuData = self.SetDateMenuDate()
        #------------------------------> Configuration
        self.cLCol = ['#', 'Gene', 'Protein']
        self.cSCol = [45, 70, 100]
        
        super().__init__(parent, menuData=menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> 
        self.statusbar.SetFieldsCount(2, config.sbPlot)
        #------------------------------>  Plot
        self.plots = dtsWindow.NPlots(self, ['Vol', 'FC'], 2)
        #------------------------------> Text details
        self.text = wx.TextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        #------------------------------> wx.ListCtrl
        #--------------> Protein list that will not change for this analysis.
        data = self.data[self.date[0]]['DF'].iloc[:,0:2]
        data.insert(0, 'kbr', range(0,data.shape[0]))
        data = data.astype(str)
        data = data.values.tolist()
        #--------------> Build and fill wx.ListCtrl
        self.lc = pane.ListCtrlSearchPlot(
            self, 
            colLabel = self.cLCol,
            colSize  = self.cSCol,
            data     = data,
            style    = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_SINGLE_SEL, 
        )
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
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
                    'Profiling details'
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
                    'Protein list'
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
        #endregion ----------------------------------------------> Aui control

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        #------------------------------> 
        self.Draw(
            self.date[0], 
            menuData['crp'][self.date[0]]['C'][0],
            menuData['crp'][self.date[0]]['RP'][0],
            self.corrP,
            newDate=True,
        )
        #------------------------------> 
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.date list and the menuData dict needed to build the Tool
            menu.

            Returns
            -------
            dict:
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
    
    def Draw(
        self, tDate: str, cond: str, rp:str, corrP: bool, newDate: bool=False
        ) -> bool:
        """Volcano plot for the given data, condition and relevant point.
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        #region --------------------------------------------> Update variables
        self.dateC = tDate
        self.condC = cond
        self.rpC   = rp
        self.corrP = corrP
        #endregion -----------------------------------------> Update variables
        
        #region --------------------------------------------------> Update GUI
        if newDate:
            #------------------------------> Clean & Reload Protein List
            
            #------------------------------> Clean FC Evolution plot
            
            #------------------------------> Alpha
            self.log10alpha = -np.log10(
                float(self.obj.data[self.cSection][tDate]['CI']['Alpha']))
            #------------------------------> Update StatusBar
            self.statusbar.SetStatusText(tDate, 1) 
        else:
            pass
        #endregion -----------------------------------------------> Update GUI
        
        #region --------------------------------------------------------> Axes
        self.SetAxis(cond, rp)
        #endregion -----------------------------------------------------> Axes
        
        #region --------------------------------------------------------> Data
        x = self.data[tDate]['DF'].loc[:,[(cond,rp,'FC')]]
        
        if self.corrP:
            y = -np.log10(self.data[tDate]['DF'].loc[:,[(cond,rp,'Pc')]])
        else:
            y = -np.log10(self.data[tDate]['DF'].loc[:,[(cond,rp,'P')]])
            
        zFC = self.data[tDate]['DF'].loc[:,[(cond,rp,'FCz')]].squeeze().tolist()
        color = dtsMethod.AssignProperty(
            zFC, config.color[self.name]['Vol'], [-self.zScore, self.zScore])
        #endregion -----------------------------------------------------> Data
        
        #region --------------------------------------------------------> Plot
        self.plots.dPlot['Vol'].axes.scatter(
            x, y, alpha=1, edgecolor='black', linewidth=1, color=color,
        )
        #------------------------------> Zoom level
        self.plots.dPlot['Vol'].ZoomResetSetValues()
        #------------------------------> Show
        self.plots.dPlot['Vol'].canvas.draw()
        #endregion -----------------------------------------------------> Plot
    
        return True
    #---
    
    def SetAxis(self, cond, rp) -> bool:
        """Set the axis in the volcano plot
        
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #------------------------------> Clear
        self.plots.dPlot['Vol'].axes.clear()
        #------------------------------> 
        self.plots.dPlot['Vol'].axes.grid(True, linestyle=":")
        self.plots.dPlot['Vol'].axes.axhline(
            y=self.log10alpha, color="black", dashes=(5, 2, 1, 2), alpha=0.5)
        #------------------------------> Labels
        self.plots.dPlot['Vol'].axes.set_title(
            f'C: {cond} RP: {rp} ' + 'Z$_{score}$: ' + f'{self.zScoreL}')
        self.plots.dPlot['Vol'].axes.set_xlabel(
            "log$_{2}$[Fold Change]", fontweight="bold")
        self.plots.dPlot['Vol'].axes.set_ylabel(
            "-log$_{10}$[P values]", fontweight="bold")
        #------------------------------>
        return True
    #---
    
    def OnZScore(self):
        """Change Z score to plot
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
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
            self.Draw(self.dateC, self.condC, self.rpC, self.corrP)
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
#endregion --------------------------------------------------------> wx.Dialog












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

import requests
import wx
import wx.adv as adv
import wx.lib.agw.aui as aui
import wx.lib.agw.customtreectrl as wxCT

import dat4s_core.data.method as dtsMethod
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow
import dat4s_core.generator.generator as dtsGenerator

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
        text = r.text.split('\n')
        for i in text:
            if '<h1>UMSAP' in i:
                versionI = i
                break
        versionI = versionI.split('UMSAP')[1].split('</h1>')[0]
        versionI = versionI.strip()
    else:
        wx.CallAfter(dtscore.Notification, 'errorU', msg=msg)
        return False
    #endregion -----------------------------------------> Get Internet version

    #region -----------------------------------------------> Compare & message
    #--> Compare
    updateAvail = dtsMethod.VersionCompare(versionI, config.version)
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
    """Base window for UMSAP

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window
        menuDate : list of str or None
            Date entries for menu of plotting windows e.g. 20210220-104527

        Attributes
        ----------
        parent : wx.Window or None
            Parent of the window
        #------------------------------> Must be set by Child
        name : str
            Unique name of the window
        cTitle : str
            Title for the window
        #------------------------------> Configuration
        cSizeWindow : wx.Size
            Size of the window. Default is config.sWinRegular
        #------------------------------> Widgets
        statusbar : wx.StatusBar
            Windows statusbar
        cSizeWindow : wx.Size
            Size of the window. Default is (900, 620)
        Sizer : wx.BoxSizer
            Main sizer of the window
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, 
        menuDate: Optional[list[str]]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.parent: Optional[wx.Window] = parent
        
        self.cSizeWindow: wx.Size = getattr(
            self, 'cSizeWindow', config.sWinRegular
        )

        super().__init__(
            parent,
            size   = self.cSizeWindow,
            title  = self.cTitle,
            name   = self.name,
        )
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------------------> Widgets
        self.statusbar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.menubar = menu.ToolMenuBar(self.name, menuDate)
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
        """Destroy window. Override as needed
    
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
    #endregion ------------------------------------------------> Class methods
#---


class BaseWindowPlot(BaseWindow):
    """Base class for windows showing only plot with common methods

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window
        menuDate : list of str or None
            Date entries for menu of plotting windows e.g. 20210220-104527
            
        Notes
        -----
        - Method OnSavePlot assumes that this window has an attribute
        plot (dtsWidget.MatPlotPanel). Override as needed
        - Method OnClose assumes the parent is an instance of UMSAPControl. 
        Override as needed.
    """
    #region -----------------------------------------------------> Class setup
    cSizeWindow = config.sWinPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, 
        menuDate: Optional[list[str]]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup

        super().__init__(parent=parent, menuDate=menuDate)
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
        """Save an image of the plot. Override as needed. """
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
        """Close window and uncheck section in UMSAPFile window. 
        Override as needed.
    
            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event
        """
        #region -----------------------------------------------> Update parent
        self.parent.UnCheckSection(self.cSection)		
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
    """Creates the main window of the App 
    
        Parameters
        ----------
        parent : wx widget or None
            parent of the main window
        
        Attributes
        ----------
        name : str
            Name to id the window
        tabMethods: dict
            Methods to create the tabs
        cTitle : str
            Title of the window
        cTitleTab : dict
            Keys are Tab names & values are Tab titles
        menubar : wx.MenuBar
            wx.Menubar associated with the window
        statusbar : wx.StatusBar
            wx.StatusBar associated with the window
        notebook : wx.lib.agw.aui.auibook.AuiNotebook
            Notebook associated with the window
        Sizer : wx.BoxSizer
            Sizer for the window
    """
    #region -----------------------------------------------------> Class Setup
    name = 'MainW'
    
    tabMethods = { # Keys are the unique names of the tabs
        'StartTab'   : tab.Start,
        'CorrATab'   : tab.BaseConfTab,
        'ProtProfTab': tab.BaseConfListTab,
    }
    
    cTitle = "Analysis Setup"
    
    cTitleTab = {
        'StartTab'   : 'Start',
        'CorrATab'   : 'CorrA',
        'ProtProfTab': 'ProtProf',
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
        self.CreateTab('StartTab')
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
            if (win := self.FindWindowByName('StartTab')) is not None:
                self.notebook.SetCloseButton(
                    self.notebook.GetPageIndex(win), 
                    False,
                )
            else:
                pass
        elif pageC == 0:
            #------------------------------> Show Start Tab with close button
            self.CreateTab('StartTab')
            self.notebook.SetCloseButton(
                self.notebook.GetPageIndex(self.FindWindowByName('StartTab')), 
                False,
            )
        else:
            pass
        
        return True
    #---

    def CreateTab(self, name: str) -> Literal[True]:
        """Create a tab
        
            Parameters
            ----------
            name : str
                One of the values in config.name for tabs
        """
        #region -----------------------------------------------------> Get tab
        win = self.FindWindowByName(name)
        #endregion --------------------------------------------------> Get tab
        
        #region ------------------------------------------> Find/Create & Show
        if win is None:
            #------------------------------> Create tab
            self.notebook.AddPage(
                self.tabMethods[name](
                    self.notebook,
                    name,
                ),
                self.cTitleTab[name],
                select = True,
            )
        else:
            #------------------------------> Focus
            self.notebook.SetSelection(self.notebook.GetPageIndex(win))
        #endregion ---------------------------------------> Find/Create & Show

        #region ---------------------------------------------------> Start Tab
        if self.notebook.GetPageCount() > 1:
            winS = self.FindWindowByName('StartTab')
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
        """Destroy window and set config.MainW
    
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
    """Creates the window showing the results of a correlation analysis

        Parameters
        ----------
        obj : data.fileUMSAPFile
            Reference to the UMSAP file object created in UMSAPControl
        parent : wx Widget or None
            Parent of the window

        Attributes
        ----------
        name : str
            Unique name of the window
        parent : wx Widget or None
            Parent of the window
        obj : parent.obj
            Pointer to the UMSAPFile object in parent. Instead of modifying this
            object here, modify the configure step or add a Get method
        data : parent.obj.confData[Section]
            Data for the Correlation Analysis section
        date : parent.obj.confData[Section].keys()
            List of dates availables for plotting
        cmap : Matplotlib cmap
            CMAP to use in the plot
        plot : dtsWidget.MatPlotPanel
            Main plot of the window
    """
    #region -----------------------------------------------------> Class setup
    name = 'CorrAPlot'
    
    cSection = config.nUCorrA

    msgExportFailed = (
        f"It was not possible to write the data to the selected file"
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

        super().__init__(parent, self.date)
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
        self.Draw(self.date[0])
        self.WinPos()
        self.Show()
        #endregion -------------------------------------------------> Position
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
            info['D']['w'] - (info['W']['N']*config.deltaWin + info['W']['w']),
            info['D']['yo'] + info['W']['N']*config.deltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        #region ----------------------------------------------------> Update N
        config.winNumber[self.name] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return True
    #---

    def Draw(self, tDate: str) -> Literal[True]:
        """ Plot data from a given date.
        
            Paramenters
            -----------
            tDate : str
                A date in the section e.g. 20210129-094504
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
        self.SetAxis(tDate)
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

    def SetAxis(self, tDate: str) -> Literal[True]:
        """ General details of the plot area 
        
            Parameters
            ----------
            tDate : str
                A date in the section e.g. 20210129-094504
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
        for i in range(0, self.data[tDate]['NumCol'], step):
            xticksloc.append(i + 0.5)		
            xlabel.append(self.data[tDate]['DF'].columns[i])

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
        dlg = dtsWindow.FileSelectDialog(
            'save',
            config.elData,
            parent = self,
        )
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
            Parent of the window

        Attributes
        ----------
        name : str
            Name of the window. Basically fileP.name
        obj : file.UMSAPFile
            Object to handle UMSAP files

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = 'UMSAPF'
    
    cSizeWindow = (400, 700)
    cPlotMethod = { # Methods to create plot windows
        config.nUCorrA : CorrAPlot
    }
    cFileLabelCheck = ['Data File']
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, obj: UMSAPFile, shownSection: Optional[list[str]]=None, 
        parent: Optional[wx.Window]=None) -> None:
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
        """Set the elements of the wx.TreeCtrl """
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
            self.cWindow[section].Destroy()
            event.Skip()
            return True
        else:
            pass
        #endregion -------------------------------------------> Destroy window
        
        #region -----------------------------------------------> Create window
        try:
            self.cWindow[section] = self.cPlotMethod[section](self)
        except Exception as e:
            dtscore.Notification('errorU', msg=str(e), tException=e)
            return False
        #endregion --------------------------------------------> Create window
        
        event.Skip()
        return True
    #---

    def UnCheckSection(self, sectionName: str) -> Literal[True]:
        """Method to uncheck a section when the plot window is closed by the 
            user
    
            Parameters
            ----------
            sectionName : str
                Section name like in config.nameModules config.nameUtilities
        """
        #region -----------------------------------------------------> Uncheck
        self.trc.SetItem3StateValue(
            self.cSection[sectionName],
            wx.CHK_UNCHECKED,
        )		
        #endregion --------------------------------------------------> Uncheck
        
        #region -----------------------------------------------------> Repaint
        self.Update()
        self.Refresh()		
        #endregion --------------------------------------------------> Repaint
        
        return True
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
            child.Close()
        #------------------------------> Self
        self.Destroy()
        #endregion --------------------------------------------------> Destroy
        
        return True
    #---

    def UpdateFileContent(self) -> Literal[True]:
        """Update the content of the file. """
        method.LoadUMSAPFile(
            fileP        = self.obj.fileP,
            shownSection = self.GetCheckedSection(),
        )

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

        Attributes:
        confOpt : dict
            Dict with configuration options
        name : str
            Unique window id
    """
    #region -----------------------------------------------------> Class setup
    name = 'CheckUpdateResDialog'
    #------------------------------> Title
    cTitle = f"Check for Updates"
    #------------------------------> Style
    cStyle = wx.CAPTION|wx.CLOSE_BOX
    #------------------------------> Label
    clLatest = "You are using the latest version of UMSAP."
    clLink   = 'Read the Release Notes.'
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: Optional[wx.Window]=None, 
        checkRes: Optional[str]=None) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent, title=self.cTitle, style=self.cStyle)
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
        """Process the link event 
        
            Parameters
            ----------
            event : wx.adv.Event
                Information about the event
        """
        event.Skip()
        self.EndModal(1)
        self.Destroy()
        
        return True
    #endregion ------------------------------------------------> Class Methods
#---


class ResControlExp(wx.Dialog):
    """Creates the dialog to type values for Results - Control Experiments

        Parameters
        ----------
        parent : wx.Panel
            This is the pane calling the dialog

        Attributes
        ----------
        

        Raises
        ------
        Exception
            - When no Data file is selected

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = 'ResControlExp'
    #------------------------------> 
    cTitle = f"Results - Control Experiments"
    #------------------------------> 
    cSize = (900, 620)
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
                iFile = Path(dlg.GetPath()[0])
                dlg.Destroy()
            else:
                dlg.Destroy()
                raise Exception
        else:
            pass
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(
            parent, 
            title = self.cTitle,
            style = self.cStyle,
            size  = self.cSize,
        )
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.conf = pane.ResControlExp(self, iFile, parent)
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
            
    
            Raise
            -----
            
        """
        if self.conf.conf.OnOK():
            self.EndModal(1)
            self.Close()
        else:
            pass
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion --------------------------------------------------------> wx.Dialog












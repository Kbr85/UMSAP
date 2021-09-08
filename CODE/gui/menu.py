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


""" Menus of the application"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Literal, Optional

import wx

import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
import gui.window as window
import gui.method as method
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class MenuMethods():
    """Base class to hold common methods to the menus """

    #region ---------------------------------------------------> Class Methods
    def OnCreateTab(self, event:wx.CommandEvent) -> Literal[True]:
        """Creates a new tab in the main window
        
            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event
        """
        #region -------------------------------------------------> Check MainW
        if config.winMain is None:
            config.winMain = window.MainWindow()
        else:
            pass
        #endregion ----------------------------------------------> Check MainW
        
        #region --------------------------------------------------> Create Tab
        config.winMain.CreateTab(self.nameID[event.GetId()])		
        #endregion -----------------------------------------------> Create Tab
        
        return True
    #---

    def OnZoomReset(self, event: wx.CommandEvent) -> Literal[True]:
        """Reset the zoom level of a matlibplot. Assumes the plot comes from
            dtsWidget.MatPlotPanel and it is called plot in the window.
    
            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event
        """
        win = self.GetWindow()
        win.plot.ZoomResetPlot()
        return True
    #---

    def AddDateItems(self, menuDate: list[str]) -> Literal[True]:
        """Add and bind the date to plot. Based class need to have a plotDate
            list
    
            Parameters
            ----------
            menuDate: list of str
                Available dates to plot e.g. 20210324-123456
        """
        #region ---------------------------------------------------> Add items
        for k in menuDate:
            #------------------------------> Add item
            i = self.AppendRadioItem(-1, k)
            #------------------------------> Add to plotDate
            self.plotDate.append(i)
            #------------------------------> Bind
            self.Bind(wx.EVT_MENU, self.OnPlotDate, source=i)
        #endregion ------------------------------------------------> Add items
        
        #region -----------------------------------------------> Add Separator
        self.AppendSeparator()
        #endregion --------------------------------------------> Add Separator
        
        return True
    #---

    def OnPlotDate(self, event: wx.CommandEvent) -> Literal[True]:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        
        """
        win = self.GetWindow()
        win.Draw(self.GetLabelText(event.GetId()))
        return True
    #---

    def OnExportPlotData(self, event: wx.CommandEvent) -> Literal[True]:
        """Export plotted data 

            Parameters
            ----------
            event : wx.Event
                Information about the event
        """
        win = self.GetWindow()
        win.OnExportPlotData()
        return True
    #---

    def OnSavePlot(self, event: wx.CommandEvent) -> Literal[True]:
        """Save an image of a plot
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        """
        win = self.GetWindow()
        win.OnSavePlot()
        return True
    #---
    
    def OnDupWin(self, event: wx.CommandEvent) -> Literal[True]:
        """Duplicate window for better data comparison
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        """
        win = self.GetWindow()
        win.OnDupWin()
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class PlotMenu(wx.Menu, MenuMethods):
    """Menu for a window plotting results, like Correlation Analysis
    
        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu of the window. See structure in window 
            class.
            
        Attributes
        ----------
        menuData : dict
            Data to build the Tool menu of the window. See structure in window 
            class.
        plotDate : list[wx.MenuItems]
            List of available dates menu items.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.menuData = menuData
        self.plotDate = []
        #------------------------------> 
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.menuData['menudate'])
        #------------------------------> Other items
        self.dupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        self.saveD = self.Append(-1, 'Export Data\tCtrl+E')
        self.saveI = self.Append(-1, 'Save Image\tCtrl+I')
        self.AppendSeparator()
        self.zoomR = self.Append(-1, 'Reset Zoom\tCtrl+Z')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnDupWin,         source=self.dupWin)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.zoomR)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.saveD)
        self.Bind(wx.EVT_MENU, self.OnSavePlot,       source=self.saveI)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---	
#endregion -----------------------------------------------------> Base Classes


#region ----------------------------------------------------> Individual menus
class Module(wx.Menu, MenuMethods):
    """Menu with module entries
    
        Attributes
        ----------
        name : str
            Unique name of the menu
        cName : dict
            Name of the modules
        nameID : dict
            Keys are the menu ids and values the tab's unique names
    """
    #region -----------------------------------------------------> Class setup
    name = 'ModuleMenu'

    cName = {
        'LimProt' : config.nmLimProt,
        'TarProt' : config.nmTarProt,
        'ProtProf': config.nmProtProf,
    }
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.limprot  = self.Append(-1, self.cName['LimProt']+'\tALT+Ctrl+L')
        self.protprof = self.Append(-1, self.cName['ProtProf']+'\tALT+Ctrl+P')
        self.tarprot  = self.Append(-1, self.cName['TarProt']+'\tALT+Ctrl+T')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.nameID = { # Associate IDs with Tab names. Avoid manual IDs
            self.limprot.GetId() : 'LimProtTab',
            self.protprof.GetId(): 'ProtProfTab',
            self.tarprot.GetId() : 'TarProtTab',
        }
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.limprot)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.protprof)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.tarprot)
        #endregion -----------------------------------------------------> Bind
    #endregion ------------------------------------------------ Instance Setup
#---


class Utility(wx.Menu, MenuMethods):
    """Utilites menu
    
        Attributes
        ----------
        name : str
            Unique name of the menu
        cName : dict
            Name of the modules
        nameID : dict
            Keys are the menu ids and values the tab's unique names
    """
    #region -----------------------------------------------------> Class setup
    name = 'UtilityMenu'
    
    cName = {
        'CorrA' : config.nuCorrA,
        'ReadF' : config.nuReadF,
    }
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance Setup
    def __init__(self):
        """"""
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.corrA   = self.Append(-1, self.cName['CorrA'])
        self.AppendSeparator()
        self.readFile = self.Append(-1, self.cName['ReadF']+'\tCtrl+R')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.nameID = { # Associate IDs with Tab names. Avoid manual IDs
            self.corrA.GetId() : 'CorrATab',
        }
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnReadFile,  source=self.readFile)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.corrA)
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance Setup

    #region ---------------------------------------------------> Class Methods
    def OnReadFile(self, event):
        """Read an UMSAP output file
    
            Parameters
            ----------
            event : wx.EVENT
                Information about the event

        """
        #region ------------------------------------------------------> Window
        win = self.GetWindow()        
        #endregion ---------------------------------------------------> Window
        
        #region ---------------------------------------------------> Get fileP
        with dtsWindow.FileSelectDialog(
            'openO', config.elUMSAP, parent=win,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                fileP = Path(dlg.GetPath())
            else:
                return False
        #endregion ------------------------------------------------> Get fileP
        
        #region ---------------------------------------------------> Load file
        method.LoadUMSAPFile(fileP=fileP)
        #endregion ------------------------------------------------> Load file
        
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class FileControlToolMenu(wx.Menu):
    """Tool menu for the UMSAP file control window """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, *args, **kwargs) -> None:
        """*args and **kwargs are needed to use this menu with ToolMenuBar.
            All of them are ignored here.
        """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.updateFile = self.Append(-1, 'Update File Content')
        self.AppendSeparator()
        self.exportData = self.Append(-1, 'Export Data')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnUpdateFileContent, source=self.updateFile)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnUpdateFileContent(self, event: wx.CommandEvent) -> Literal[True]:
        """Update the file content shown in the window
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
        """
        win = self.GetWindow()
        win.UpdateFileContent()
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class CorrAPlotToolMenu(PlotMenu):
    """Creates the Tools menu for a Correlation Analysis Plot window 
    
        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu of the window. See structure in window
            class.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> 
        pos = self.FindChildItem(self.dupWin.GetId())[1]
        #------------------------------> 
        self.Insert(pos, -1, kind=wx.ITEM_SEPARATOR)
        self.colName   = self.Insert(
            pos, -1, "Column Names", kind=wx.ITEM_RADIO,
        )
        self.colNumber = self.Insert(
            pos+1, -1, "Column Numbers (0 based)",kind=wx.ITEM_RADIO,
        )
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnColType, source=self.colName)
        self.Bind(wx.EVT_MENU, self.OnColType, source=self.colNumber)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnColType(self, event: wx.CommandEvent) -> Literal[True]:
        """Use either the name of the columns or the 0 based number of the 
            column for the axes
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
        """
        #region ----------------------------------------------------> Get Date
        for k in self.plotDate:
            #------------------------------> 
            iD = k.GetId()
            #------------------------------> 
            if self.IsChecked(iD):
                date = self.GetLabelText(iD)
                break
            else:
                pass
        #endregion -------------------------------------------------> Get Date
        
        #region -----------------------------------------------------> Get Col
        col = 'Name' if self.IsChecked(self.colName.GetId()) else 'Number'
        #endregion --------------------------------------------------> Get Col
        
        #region --------------------------------------------------------> Plot
        win = self.GetWindow()
        win.Draw(date, col)
        #endregion -----------------------------------------------------> Plot
        
        return True
    #---
    
    def OnPlotDate(self, event: wx.CommandEvent) -> Literal[True]:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        
        """
        #region -----------------------------------------------------> Get Col
        col = 'Name' if self.IsChecked(self.colName.GetId()) else 'Number'
        #endregion --------------------------------------------------> Get Col
        
        #region --------------------------------------------------------> Plot
        win = self.GetWindow()
        win.Draw(self.GetLabelText(event.GetId()), col)
        #endregion -----------------------------------------------------> Plot
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus
class VolcanoPlot(wx.Menu):
    """Menu for a Volcano Plot """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, crp: dict, iDate: str):
        """ """
        #region -----------------------------------------------> Initial Setup
        self.crp = crp
        #------------------------------> Menu items for cond & relevant points
        self.cond, self.rp = self.SetCondRPMenuItems(iDate)
        #------------------------------> Cond - RP separator
        self.sep = None
        #------------------------------> 
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddCondRPMenuItems2Menus()
        self.AppendSeparator()
        self.zScore = self.Append(-1, 'Z score')
        self.AppendSeparator()
        self.pCorr = self.Append(-1, 'Corrected P Values', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.saveI = self.Append(-1, 'Save Plot Image')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetCondRPMenuItems(
        self, tDate: str
        ) -> tuple[list[wx.MenuItem], list[wx.MenuItem]]:
        """Set the menu items for conditions and relevant points as defined for 
            the current analysis.
    
            Parameters
            ----------
            tDate : str
    
            Returns
            -------
            tuple:
                First element is the condition menu items and second relevant 
                point menu items.
        """
        #region -------------------------------------------------> Empty lists
        cond = []
        rp = []
        #endregion ----------------------------------------------> Empty lists
        
        #region ------------------------------------------------> Add elements
        #------------------------------> Conditions
        for c in self.crp[tDate]['C']:
            cond.append(wx.MenuItem(None, -1, text=c, kind=wx.ITEM_RADIO))
        #------------------------------> Relevant Points
        for t in self.crp[tDate]['RP']:
            rp.append(wx.MenuItem(None, -1, text=t, kind=wx.ITEM_RADIO))
        #endregion ---------------------------------------------> Add elements
        
        return (cond, rp)
    #---
    
    def AddCondRPMenuItems2Menus(self) -> bool:
        """Add the menu items in self.cond and self.rp to the menu"""
        #region ---------------------------------------------------> Add items
        #------------------------------> Conditions
        for k,c in enumerate(self.cond):
            self.Insert(k,c)
        #------------------------------> Separator
        self.sep = wx.MenuItem(None)
        self.Insert(k+1, self.sep)
        #------------------------------> Relevant Points
        for j,t in enumerate(self.rp, k+2):
            self.Insert(j, t)
        #endregion ------------------------------------------------> Add items
        
        return True
    #---
    
    def UpdateCondRP(self, tDate) -> bool:
        """Update the conditions and relevant points when date changes.
    
            Parameters
            ----------
            tDate : str
                Selected date
    
            Returns
            -------
            bool
            
            Notes
            -----
            Date changes in ProtProfToolMenu
        """
        #region ---------------------------------------------> Delete Elements
        #------------------------------> Conditions
        for c in self.cond:
            self.Delete(c)
        #------------------------------> Separators
        self.Delete(self.sep)
        self.sep = None
        #------------------------------> RP
        for rp in self.rp:
            self.Delete(rp)
        #endregion ------------------------------------------> Delete Elements
        
        #region -----------------------------------> Create & Add New Elements
        #------------------------------> 
        self.cond, self.rp = self.SetCondRPMenuItems(tDate)
        #------------------------------> 
        self.AddCondRPMenuItems2Menus()
        #endregion --------------------------------> Create & Add New Elements
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FCEvolution(wx.Menu):
    """Menu for a log2FC evolution along relevant points """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.showAll = self.Append(-1, 'Show All')
        self.AppendSeparator()
        self.saveI = self.Append(-1, 'Save Plot Image')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---


class FiltersProtProf(wx.Menu):
    """Menu for the ProtProfPlot Filters """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.add = self.Append(-1, 'Add')
        self.remove = self.Append(-1, 'Remove')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---


class ProtProfToolMenu(wx.Menu, MenuMethods):
    """ """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict):
        """ """
        #region -----------------------------------------------> Initial Setup
        self.menuData = menuData
        self.plotDate = []
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.menuData['menudate'])
        self.AppendSeparator()
        #------------------------------> Volcano Plot
        self.volcano =  VolcanoPlot(
                self.menuData['crp'], self.plotDate[0].GetItemLabelText()
        )
        self.AppendSubMenu(self.volcano, 'Volcano Plot',)
        self.AppendSeparator()
        #------------------------------> Relevant Points
        self.AppendSubMenu(FCEvolution(), 'FC Evolution')
        self.AppendSeparator()
        #------------------------------> Filter
        self.AppendSubMenu(FiltersProtProf(), 'Filters')
        self.AppendSeparator()
        #------------------------------> Export Data
        self.expD = self.Append(-1, 'Export Data')
        self.AppendSeparator()
        #------------------------------> Reset
        self.reset = self.Append(-1, 'Reset View')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnPlotDate(self, event: wx.CommandEvent) -> Literal[True]:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        
        """
        #region --------------------------------------------------------> Date
        tDate = self.GetLabelText(event.GetId())
        #endregion -----------------------------------------------------> Date
        
        #region -----------------------------------------> Update Volcano menu
        self.volcano.UpdateCondRP(tDate)
        #endregion --------------------------------------> Update Volcano menu
        
        
        # win = self.GetWindow()
        # win.Draw(self.GetLabelText(event.GetId()))
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion --------------------------------------------------------> Mix menus


#region -------------------------------------------------------------> Menubar
class MainMenuBar(wx.MenuBar):
    """ Creates the application menu bar"""
    
    #region --------------------------------------------------- Instance Setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
        
        #region --------------------------------------------------> Menu items
        self.Module  = Module()
        self.Utility = Utility()
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------> Append to menubar
        self.Append(self.Module, '&Modules')
        self.Append(self.Utility, '&Utilities')
        #endregion ----------------------------------------> Append to menubar
    #endregion ------------------------------------------------ Instance Setup
#---


class ToolMenuBar(MainMenuBar):
    """Menu bar for a window showing the corresponding tool menu
    
        Parameters
        ----------
        name : str
            Unique name of the window/tab for which the Tool menu will be 
            created
        menuData : dict
            Data to build the Tool menu of the window. See structure in the
            window class.
    """

    #region -----------------------------------------------------> Class Setup
    toolClass = { # Key are window name
        config.nwMain        : None,
        config.nwUMSAPControl: FileControlToolMenu,
        config.nwCorrAPlot   : CorrAPlotToolMenu,
        config.nwProtProf    : ProtProfToolMenu,
    }
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------- Instance Setup
    def __init__(self, name: str, menuData: Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------> Menu items & Append
        if self.toolClass[name] is not None:
            self.Tool  = self.toolClass[name](menuData)
            self.Insert(config.toolsMenuIdx, self.Tool, 'Tools')
        else:
            pass
        #endregion --------------------------------------> Menu items & Append
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar
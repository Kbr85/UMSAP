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
from typing import Literal, Optional

import wx

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
        """Add and bind the date to plot
    
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
            self.plotDate[i.GetId()] = k
            #------------------------------> Bind
            self.Bind(wx.EVT_MENU, self.OnPlotDate, source=i)
        #endregion ------------------------------------------------> Add items
        
        #region -----------------------------------------------> Add Separator
        self.AppendSeparator()
        #endregion --------------------------------------------> Add Separator
        
        return True
    #---

    def OnPlotDate(self, event: wx.CommandEvent) -> Literal[True]:
        """Plot a date of a section in an UMSAP file. Assumes the Tools menu
            creates a self.plotDate dict (keys are menu item id and values
            the available dates) 
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        
        """
        win = self.GetWindow()
        win.Draw(self.plotDate[event.GetId()])
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
    #endregion ------------------------------------------------> Class Methods
#---


# class PlotMenu(wx.Menu, MenuMethods):
#     """Menu for a window plotting results, like Correlation Analysis
    
#         Parameters
#         ----------
#         menuDate : list of str
#             List of available dates for the menu
    
#     """
#     #region -----------------------------------------------------> Class setup
    
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, menuDate: list[str]) -> None:
#         """ """
#         #region -----------------------------------------------> Initial Setup
#         super().__init__()
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------> Menu Items
#         #------------------------------> Add Dates
#         self.AddDateItems(menuDate)
#         #------------------------------> Other items
#         self.saveD = self.Append(-1, 'Export Data\tCtrl+E')
#         self.saveI = self.Append(-1, 'Save Image\tCtrl+I')
#         self.AppendSeparator()
#         self.zoomR = self.Append(-1, 'Reset Zoom\tCtrl+Z')
#         #endregion -----------------------------------------------> Menu Items

#         #region --------------------------------------------------------> Bind
#         self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.zoomR)
#         self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.saveD)
#         self.Bind(wx.EVT_MENU, self.OnSavePlot,       source=self.saveI)
#         #endregion -----------------------------------------------------> Bind
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---	
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
        'LimProt' : config.nameModules['LimProt'],
        'TarProt' : config.nameModules['TarProt'],
        'ProtProf': config.nameModules['ProtProf'],
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
    
        Parameters
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
        'CorrA' : config.nameUtilities['CorrA'],
        'ReadF' : config.nameUtilities['ReadF'],
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
        win = self.GetWindow()
        method.LoadUMSAPFile(win=win)

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


# class FileControlToolMenu(wx.Menu):
#     """Tool menu for the UMSAP file control window """
#     #region -----------------------------------------------------> Class setup
    
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, *args, **kwargs) -> None:
#         """*args and **kwargs are needed to use this menu with ToolMenuBar
#             All of them are ignored here.
#         """
#         #region -----------------------------------------------> Initial Setup
#         super().__init__()
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------> Menu Items
#         self.updateFile = self.Append(-1, 'Update File Content')
#         self.AppendSeparator()
#         self.exportData = self.Append(-1, 'Export Data')
#         #endregion -----------------------------------------------> Menu Items

#         #region --------------------------------------------------------> Bind
#         self.Bind(wx.EVT_MENU, self.OnUpdateFileContent, source=self.updateFile)
#         #endregion -----------------------------------------------------> Bind
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
#     def OnUpdateFileContent(self, event: wx.CommandEvent) -> Literal[True]:
#         """Update the file content shown in the window
    
#             Parameters
#             ----------
#             event: wx.Event
#                 Information about the event
#         """
#         win = self.GetWindow()
#         win.UpdateFileContent()
#         return True
#     #---
#     #endregion ------------------------------------------------> Class methods
# #---


# class CorrAPlotToolMenu(PlotMenu):
#     """Creates the Tools menu for a Corelation Analysis Plot window 
    
#         Parameters
#         ----------
#         menuDate : list of str
#             Available dates to plot e.g. 20210304-053517
#     """
#     #region -----------------------------------------------------> Class setup
    
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, menuDate: list[str]) -> None:
#         """ """
#         #region -----------------------------------------------> Initial Setup
#         super().__init__(menuDate)
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------> Menu Items

#         #endregion -----------------------------------------------> Menu Items

#         #region --------------------------------------------------------> Bind

#         #endregion -----------------------------------------------------> Bind
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---
#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus

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
        menuDate : list of str or None
            Available dates to plot e.g. 20210304-053517. Default is None
    """

    #region -----------------------------------------------------> Class Setup
    toolClass = { # Key are window name
        'MainW'    : None,
        # 'UMSAPF'   : FileControlToolMenu,
        # 'CorrAPlot': CorrAPlotToolMenu,
    }
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------- Instance Setup
    def __init__(self, name: str, menuDate: Optional[list[str]]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------> Menu items & Append
        if self.toolClass[name] is not None:
            self.Tool  = self.toolClass[name](menuDate)
            self.Insert(config.toolsMenuIdx, self.Tool, 'Tools')
        else:
            pass
        #endregion --------------------------------------> Menu items & Append
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar
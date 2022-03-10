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


"""Menus of the application"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Optional, Union

import wx

import dat4s_core.gui.wx.method as dtsGwxMethod

import config.config as config
import gui.dtscore as dtscore
import gui.method as method
import gui.window as window
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class MenuMethods():
    """Base class to hold common methods to the menus"""
    
    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    def OnCreateTab(self, event:wx.CommandEvent) -> bool:
        """Creates a new tab in the main window
        
            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event
                
            Returns
            -------
            True
                
            Notes
            -----
            Assumes child class has a self.nameID dict with event's id as keys
            and tab's ids as values.
        """
        #region -------------------------------------------------> Check MainW
        if config.winMain is None:
            config.winMain = window.MainWindow()
        else:
            pass
        #endregion ----------------------------------------------> Check MainW
        
        #region --------------------------------------------------> Create Tab
        config.winMain.OnCreateTab(self.rKeyID[event.GetId()])
        #endregion -----------------------------------------------> Create Tab
        
        return True
    #---    

    def OnDupWin(self, event: wx.CommandEvent) -> bool:
        """Duplicate window for better data comparison
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            True
        """
        win = self.GetWindow() 
        win.OnDupWin()
        
        return True
    #---

    def OnZoomReset(self, event: wx.CommandEvent) -> bool:
        """Reset the zoom level of a matlibplot. 
    
            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event
                
            Returns
            -------
            True
                
            Notes
            -----
            Useful for windows showing only one plot.
        """
        #region ---------------------------------------------------> Variables
        win = self.GetWindow()
        tKey = self.rKeyID[event.GetId()]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Run
        win.dKeyMethod[tKey]()
        #endregion ------------------------------------------------> Run

        return True
    #---
    
    def OnExportPlotData(self, event: wx.CommandEvent) -> bool:
        """Export plotted data 

            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            True
        """
        win = self.GetWindow()
        win.OnExportPlotData()
        
        return True
    #---
    
    def OnSavePlotImage(self, event: wx.CommandEvent) -> bool:
        """Save an image of a single pane showing a plot
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Variables
        win = self.GetWindow()
        tKey = self.rKeyID[event.GetId()]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Run
        win.dKeyMethod[tKey]()
        #endregion ------------------------------------------------> Run

        return True
    #---
    
    def OnCheckDataPrep(self, event: wx.CommandEvent) -> bool:
        """Launch the Check Data Preparation window.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
    
            Returns
            -------
            True
        """
        win = self.GetWindow() 
        win.OnCheckDataPrep(self.GetCheckedRadiodItem(self.rPlotDate))
        
        return True
    #---
        
    def OnPlotDate(self, event: wx.CommandEvent) -> bool:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Date
        tDate = self.GetLabelText(event.GetId())
        #endregion -----------------------------------------------------> Date

        #region --------------------------------------------------------> Draw
        win = self.GetWindow()
        win.UpdateDisplayedData(tDate)
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def OnExportFilteredData(self, event: wx.CommandEvent) -> bool:
        """Export filtered data 

            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            True
        """
        win = self.GetWindow() 
        win.OnExportFilteredData()
        
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
    
    #region --------------------------------------------------> Manage Methods
    def AddDateItems(self, menuDate: list[str]) -> bool:
        """Add and bind the date to plot. 
    
            Parameters
            ----------
            menuDate: list of str
                Available dates to plot e.g. '20210324-123456 - bla'
                  
            Returns
            -------
            True
              
            Notes
            -----
            Base class needs to have a empty self.plotDate list. The filled list
            will be used by other menu methods.
        """
        #region ---------------------------------------------------> Add items
        for k in menuDate:
            #------------------------------> Add item
            i = self.AppendRadioItem(-1, k)
            #------------------------------> Add to plotDate
            self.rPlotDate.append(i)
            #------------------------------> Bind
            self.Bind(wx.EVT_MENU, self.OnPlotDate, source=i)
        #endregion ------------------------------------------------> Add items
        
        #region -----------------------------------------------> Add Separator
        self.AppendSeparator()
        #endregion --------------------------------------------> Add Separator
        
        return True
    #---
    
    def GetCheckedRadiodItem(
        self, lMenuItem: list[wx.MenuItem], getVal: str='Label',
        ) -> Union[str, int]:
        """Get the checked item in a list of radio menu items.
    
            Parameters
            ----------
            lMenuItem: list of wx.MenuItems
                Items are expected to be radio items from the same group.
            getVal: str
                wx.MenuItem property to return. 'Id' or 'Label'. Defauls is 
                'Label'.
    
            Returns
            -------
            str
                Label of the checked item
            
            Notes
            -----
            If getVal is not known the Id is returned
        """
        #region -----------------------------------------------------> Checked
        for k in lMenuItem:
            if k.IsChecked():
                if getVal == 'Label':
                    return k.GetItemLabelText()
                else:
                    return k.GetId()
            else:
                pass
        #endregion --------------------------------------------------> Checked
    #---
    #endregion -----------------------------------------------> Manage Methods
#---


class PlotMenu(wx.Menu, MenuMethods):
    """Menu for a window plotting results, like Correlation Analysis
    
        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu of the window. It must contain at least
            a key - value pair like:
            'menudate' : ['20210324-123456 - bla',..., '20220730-105402 - bla2']
            See other key - value pairs in the window class.
            
        Attributes
        ----------
        menuData : dict
            Data to build the Tool menu of the window. It must contain at least
            a key - value pair like:
            'menudate' : ['20210324-123456 - bla',..., '20220730-105402 - bla2']
            See other key - value pairs in the window class.
        plotDate : list[wx.MenuItems]
            List of available dates menu items.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = cMenuData
        self.rPlotDate = []
        #------------------------------> 
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.cMenuData['menudate'])
        #------------------------------> Other items
        self.miCheckDP = self.Append(-1, 'Data Preparation\tCtrl+P')
        self.AppendSeparator()
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        self.miSaveD = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI = self.Append(-1, 'Export Image\tCtrl+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, 'Reset Zoom\tCtrl+Z')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnDupWin,         source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnCheckDataPrep,  source=self.miCheckDP)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---	


class PlotSubMenu(wx.Menu, MenuMethods):
    """Sub menu items for a plot region
    
        Parameters
        ----------
        tKey: str
            For keyboard binding. Shift, Ctrl or Alt.
    """
    #region -----------------------------------------------------> Class setup
    rKeys = {
        'Shift': 'Main',
        'Alt'  : 'Bottom'
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, tKey: str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miSaveI = self.Append(-1, f'Save Image\t{tKey}+I')
        self.miZoomR = self.Append(-1, f'Reset Zoom\t{tKey}+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): f'{self.rKeys[tKey]}Img',
            self.miZoomR.GetId(): f'{self.rKeys[tKey]}Zoom',
        }
        #endregion ------------------------------------------------> rKeyID
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnZoomReset,     source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage, source=self.miSaveI)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion -----------------------------------------------------> Base Classes


#region ----------------------------------------------------> Individual menus
class Module(wx.Menu, MenuMethods):
    """Menu with module entries
    
        Attributes
        ----------
        rKeyID : dict
            Link wx.MenuItems.Id with keywords used by methods in the window
            owning the wx.Menu
    """
    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.miLimProt  = self.Append(-1, f'{config.nmLimProt}\tAlt+Ctrl+L')
        self.miProtProf = self.Append(-1, f'{config.nmProtProf}\tAlt+Ctrl+P')
        self.miTarProt  = self.Append(-1, f'{config.nmTarProt}\tAlt+Ctrl+T')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.rKeyID = { # Associate IDs with Tab names. Avoid manual IDs
            self.miLimProt.GetId() : config.ntLimProt,
            self.miProtProf.GetId(): config.ntProtProf,
            self.miTarProt.GetId() : config.ntTarProt,
        }
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miLimProt)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miProtProf)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miTarProt)
        #endregion -----------------------------------------------------> Bind
    #endregion ------------------------------------------------ Instance Setup
#---


class Utility(wx.Menu, MenuMethods):
    """Utilites menu
    
        Attributes
        ----------
        rrKeyID : dict
            Link wx.MenuItems.Id with keywords used by methods in the window
            owning the wx.Menu
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup
    
    #region --------------------------------------------------> Instance Setup
    def __init__(self) -> None:
        """"""
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.miCorrA   = self.Append(-1, config.nuCorrA)
        self.miDataPrep = self.Append(-1, config.nuDataPrep)
        self.AppendSeparator()
        self.miReadFile = self.Append(-1, f'{config.nuReadF}\tCtrl+R')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.rKeyID = { # Associate IDs with Tab names. Avoid manual IDs
            self.miCorrA.GetId()   : config.ntCorrA,
            self.miDataPrep.GetId(): config.ntDataPrep,
        }
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnReadFile,  source=self.miReadFile)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miCorrA)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miDataPrep)
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance Setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event Methods
    #------------------------------> Event Methods
    def OnReadFile(self, event: wx.CommandEvent) -> bool:
        """Read an UMSAP output file.
    
            Parameters
            ----------
            event : wx.EVENT
                Information about the event
                
            Returns
            -------
            True
        """
        #region ------------------------------------------------------> Window
        win = self.GetWindow()        
        #endregion ---------------------------------------------------> Window
        
        #region ---------------------------------------------------> Get fileP
        try:
            fileP = dtsGwxMethod.GetFilePath(
                'openO', 
                ext    = config.elUMSAP,
                parent = win,
                msg    = config.mFileSelUMSAP,
            )
            if fileP is None:
                return False
            else:
                fileP = Path(fileP[0])
        except Exception as e:      
            dtscore.Notification(
                'errorF', 
                msg        = config.mFileSelector,
                tException = e,
                parent     = win,
            )
            return False
        #endregion ------------------------------------------------> Get fileP
        
        #region ---------------------------------------------------> Load file
        method.LoadUMSAPFile(fileP=fileP)
        #endregion ------------------------------------------------> Load file
        
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
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
        self.miExpData = self.Append(-1, 'Export Data\tCtrl+E')
        self.AppendSeparator()
        self.miUpdateFile = self.Append(-1, 'Reload File\tCtrl+U')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------------> Bind
        self.Bind(
            wx.EVT_MENU, self.OnUpdateFileContent, source=self.miUpdateFile)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    def OnUpdateFileContent(self, event: wx.CommandEvent) -> bool:
        """Update the file content shown in the window
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
            
            Returns
            -------
            True
        """
        win = self.GetWindow()
        win.UpdateFileContent()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class CorrAPlotToolMenu(PlotMenu):
    """Creates the Tools menu for a Correlation Analysis Plot window 
    
        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu. See Notes for more details.
            
        Attributes
        ----------
        rKeyID : dict
            Link wx.MenuItems.Id with keywords used by methods in the window
            owning the wx.Menu
        rCol: list[wx.MenuItems]
            List of wx.MenuItems with the options for the 
            
        Notes
        -----
        menuData has the following structure:
        {
            'menudate' : ['dateA',....,'dateN'],
        }
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
        pos = self.FindChildItem(self.miCheckDP.GetId())[1]
        #------------------------------> 
        self.Insert(pos, -1, kind=wx.ITEM_SEPARATOR)
        self.miColName   = self.Insert(
            pos, -1, "Column Names", kind=wx.ITEM_RADIO,
        )
        self.miColNumber = self.Insert(
            pos+1, -1, "Column Numbers (0 based)",kind=wx.ITEM_RADIO,
        )
        #------------------------------> 
        self.Insert(pos+2, -1, kind=wx.ITEM_SEPARATOR)
        self.miAllCol = self.Insert(pos+3, -1, "All Columns")
        self.miSelCol = self.Insert(pos+4, -1, "Select Columns")
        #------------------------------> 
        self.Insert(pos+5, -1, kind=wx.ITEM_SEPARATOR)
        self.miColBar = self.Insert(
            pos+6, -1, "Show ColorBar",kind=wx.ITEM_CHECK,
        )
        self.miColBar.Check(check=False)
        #endregion -----------------------------------------------> Menu Items
        
        #region -------------------------------------------------------> Names
        self.rKeyID = { # Associate IDs with Tab names. Avoid manual IDs
            self.miColName.GetId()  : 'Name',
            self.miColNumber.GetId(): 'Number',
            self.miSaveI.GetId()    : 'PlotImageOne',
            self.miZoomR.GetId()    : 'PlotZoomResetOne',
            self.miAllCol.GetId()   : True,
            self.miSelCol.GetId()   : False,
            
        }
        self.rCol = [self.miColName, self.miColNumber]
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnPlotData, source=self.miColName)
        self.Bind(wx.EVT_MENU, self.OnPlotData, source=self.miColNumber)
        self.Bind(wx.EVT_MENU, self.OnPlotData, source=self.miColBar)
        self.Bind(wx.EVT_MENU, self.OnSelCol,   source=self.miSelCol)
        self.Bind(wx.EVT_MENU, self.OnSelCol,   source=self.miAllCol)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    def OnPlotDate(self, event: wx.CommandEvent) -> bool:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event

            Returns
            -------
            True
        """
        return self.OnPlotData('fEvent')
    #---
    
    def OnPlotData(self, event: Union[wx.CommandEvent, str]) -> bool:
        """Plot a date of a section in an UMSAP file.
        
            Parameters
            ----------
            event : wx.Event
                Information about the event
    
            Returns
            -------
            True
        """
        #region -----------------------------------------------------> Get Col
        col    = self.rKeyID[self.GetCheckedRadiodItem(self.rCol,getVal='Id')]
        date   = self.GetCheckedRadiodItem(self.rPlotDate)
        colBar = self.miColBar.IsChecked()
        win    = self.GetWindow()
        #endregion --------------------------------------------------> Get Col
        
        #region --------------------------------------------------------> Plot
        win.UpdateDisplayedData(date, col, colBar)
        #endregion -----------------------------------------------------> Plot
        
        return True
    #---
    
    def OnSelCol(self, event: wx.CommandEvent) -> bool:
        """Plot only the selected columns
    
            Parameters
            ----------
            event : wx.Event
                Information about the event

            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Plot
        win = self.GetWindow()
        win.OnSelectColumns(self.rKeyID[event.GetId()])
        #endregion ------------------------------------------------> Plot
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class DataPrepToolMenu(wx.Menu, MenuMethods):
    """Tool menu for the Data Preparation Plot window.
        
        Parameters
        ----------
        menuData: dict
            Data needed to build the menu. See Notes for more details.
        
        Attributes
        ----------
        rPlotDate : list of wx.MenuItems
            Available dates in the analysis.
        rKeyID : dict
            Link wx.MenuItems.Id with keywords used by methods in the window
            owning the wx.Menu
            
        Notes
        -----
        menuData has the following structure:
        {
            'menudate' : [List of dates as str],
        }
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = cMenuData
        self.rPlotDate = []
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        if cMenuData is not None:
            self.AddDateItems(self.cMenuData['menudate'])
            self.AppendSeparator()
        else:
            pass
        #------------------------------> Duplicate Window
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        #------------------------------> Export Data
        self.miSaveD = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI = self.Append(-1, 'Export Image\tShift+I')
        self.AppendSeparator()
        #------------------------------> 
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'PlotImageOne',
            self.miZoomR.GetId(): 'PlotZoomResetAllinOne',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnDupWin,         source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind    
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class VolcanoPlot(wx.Menu, MenuMethods):
    """Menu for a Volcano Plot.
    
        Parameters
        ----------
        cCrp: dict
            Available conditions and relevant point for the analysis. 
            See Notes for more details.
        ciDate : str
            Initially selected date
            
        Attributes
        ----------
        rCond : list of wx.MenuItems
            Available conditions as wx.MenuItems for the current date.
        rCrp : dict
            Available conditions and relevant point for the analysis. 
            See Notes for more details.
        rRp : list of wx.MenuItems
            Available relevant points as wx.MenuItems for the current date.
        rSep : wx.MenuItem
            Separator between conditions and relevant points.
            
        Notes
        -----
        rCrp has the following structure
            {
                    'date1' : {
                        'C' : [List of conditions as str],
                        'RP': [List of relevant points as str],
                    }
                    .......
                    'dateN' : {}
            }
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cCrp: dict, ciDate: str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCrp = cCrp
        #------------------------------> Cond - RP separator. To remove/create.
        self.rSep = None
        #------------------------------> 
        super().__init__()
        #------------------------------> Menu items for cond & relevant points
        self.rCond, self.rRp = self.SetCondRPMenuItems(ciDate)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddCondRPMenuItems2Menus()
        self.AppendSeparator()
        self.miColor = self.Append(-1, 'Color Scheme')
        self.AppendSeparator()
        self.miPCorr = self.Append(-1, 'Corrected P Values', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, 'Export Image\tShift+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'VolcanoImg',
            self.miZoomR.GetId(): 'VolcanoZoom',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnColor,          source=self.miColor)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnUpdatePlot,     source=self.miPCorr)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class method
    #region ---------------------------------------------------> Event methods
    def OnUpdatePlot(self, event: wx.CommandEvent) -> bool:
        """Update volcano plot.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Draw
        win = self.GetWindow()
        win.OnVolChange(*self.GetData4Draw())
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    
    def OnColor(self, event: wx.CommandEvent) -> bool:
        """Adjust the Color Scheme for proteins.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnVolColorScheme()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
    
    #region --------------------------------------------------> Manage methods
    def AddCondRPMenuItems2Menus(self) -> bool:
        """Add the menu items in self.cond and self.rp to the menu
        
            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Add items
        #------------------------------> Conditions
        for k,c in enumerate(self.rCond):
            self.Insert(k,c)
        #------------------------------> Separator
        self.rSep = wx.MenuItem(None)
        self.Insert(k+1, self.rSep)
        #------------------------------> Relevant Points
        for j,t in enumerate(self.rRp, k+2):
            self.Insert(j, t)
        #endregion ------------------------------------------------> Add items
        
        return True
    #---
    
    def GetData4Draw(self) -> tuple[str, str, bool]:
        """Return the current selected cond, rp and corrP.
    
            Returns
            -------
            Data needed for the volcano plot
                (cond, rp, bool)
        """
        #region ---------------------------------------------------> Varaibles
        cond = self.GetCheckedRadiodItem(self.rCond)
        rp   = self.GetCheckedRadiodItem(self.rRp)
        corrP = self.miPCorr.IsChecked()
        #endregion ------------------------------------------------> Varaibles
        
        return (cond, rp, corrP)
    #---
    
    def SetCondRPMenuItems(
        self, tDate: str
        ) -> tuple[list[wx.MenuItem], list[wx.MenuItem]]:
        """Set the menu items for conditions and relevant points as defined for 
            the current analysis date.
    
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
        for c in self.rCrp[tDate]['C']:
            #------------------------------> 
            i = wx.MenuItem(None, -1, text=c, kind=wx.ITEM_RADIO)
            #------------------------------> 
            cond.append(i)
            #------------------------------> 
            self.Bind(wx.EVT_MENU, self.OnUpdatePlot, source=i)
        #------------------------------> Relevant Points
        for t in self.rCrp[tDate]['RP']:
            #------------------------------> 
            i = wx.MenuItem(None, -1, text=t, kind=wx.ITEM_RADIO)
            #------------------------------> 
            rp.append(i)
            #------------------------------> 
            self.Bind(wx.EVT_MENU, self.OnUpdatePlot, source=i)
        #endregion ---------------------------------------------> Add elements
        
        return (cond, rp)
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
        for c in self.rCond:
            self.Delete(c)
        #------------------------------> Separators
        self.Delete(self.rSep)
        self.sep = None
        #------------------------------> RP
        for rp in self.rRp:
            self.Delete(rp)
        #endregion ------------------------------------------> Delete Elements
        
        #region -----------------------------------> Create & Add New Elements
        #------------------------------> 
        self.rCond, self.rRp = self.SetCondRPMenuItems(tDate)
        #------------------------------> 
        self.AddCondRPMenuItems2Menus()
        #endregion --------------------------------> Create & Add New Elements
        
        return True
    #---
    #endregion -----------------------------------------------> Manage methods
#---


class FCEvolution(wx.Menu, MenuMethods):
    """Menu for a log2FC evolution along relevant points """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miShowAll = self.Append(-1, 'Show All', kind=wx.ITEM_CHECK)
        self.Check(self.miShowAll.GetId(), True)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, 'Export Image\tAlt+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, 'Reset Zoom\tAlt+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'FCImage',
            self.miZoomR.GetId(): 'FCZoom',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnShowAll,       source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage, source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,     source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class method
    #region ---------------------------------------------------> Event methods
    def OnShowAll(self, event: wx.CommandEvent) -> bool:
        """Show the interval cover by all FC values in the data.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnFCChange(*self.GetData4Draw())
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
    
    #region --------------------------------------------------> Manage methods
    def GetData4Draw(self) -> tuple[bool]:
        """Get the data needed to draw the FC evolution in window.          
    
            Returns
            -------
            tuple[bool]
                Return tuple to match similar data from VolcanoPlot
        """
        return (self.miShowAll.IsChecked(),)
    #---
    #endregion ------------------------------------------------> Manage methods
#---


class FiltersProtProf(wx.Menu):
    """Menu for the ProtProfPlot Filters"""
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miFcChange = self.Append(-1, 'FC Evolution')
        self.miHypCurve = self.Append(-1, 'Hyperbolic Curve')
        self.miLog2FC   = self.Append(-1, 'Log2(FC)')
        self.miPValue   = self.Append(-1, 'P Value')
        self.miZScore   = self.Append(-1, 'Z Score')
        self.AppendSeparator()
        self.miApply = self.Append(-1, 'Apply All\tCtrl+Shift+A')
        self.miUpdate = self.Append(-1, 'Auto Apply\tCtrl-Shift+F', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miRemoveAny  = self.Append(-1, 'Remove\tCtrl+Shift+R')
        self.miRemoveLast = self.Append(-1, 'Remove Last\tCtrl+Shift+Z')
        self.miRemoveAll  = self.Append(-1, 'Remove All\tCtrl+Shift+X')
        self.AppendSeparator()
        self.miCopy = self.Append(-1, 'Copy\tCtrl+Shift+C')
        self.miPaste = self.Append(-1, 'Paste\tCtrl+Shift+P')
        self.AppendSeparator()
        self.miSave = self.Append(-1, 'Save\tCtrl+Shift+S')
        self.miLoad = self.Append(-1, 'Load\tCtrl+Shift+L')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miFcChange.GetId():  config.lFilFCEvol,
            self.miHypCurve.GetId():  config.lFilHypCurve,
            self.miLog2FC.GetId():    config.lFilFCLog,
            self.miPValue.GetId():    config.lFilPVal,
            self.miZScore.GetId():    config.lFilZScore,
            self.miApply.GetId():     'Apply All',
            self.miRemoveLast.GetId():'Remove Last',
            self.miRemoveAny.GetId(): 'Remove Any',
            self.miRemoveAll.GetId(): 'Remove All',
            self.miCopy.GetId():      'Copy',
            self.miPaste.GetId():     'Paste',
            self.miSave.GetId():      'Save Filter',
            self.miLoad.GetId():      'Load Filter',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miFcChange)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miLog2FC)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miPValue)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miZScore)        
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miApply)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miRemoveLast)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miRemoveAny)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miRemoveAll)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miCopy)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miPaste)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miSave)
        self.Bind(wx.EVT_MENU, self.OnFilter,      source=self.miLoad)
        self.Bind(wx.EVT_MENU, self.OnAutoFilter,  source=self.miUpdate)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    #------------------------------> Event Methods
    def OnAutoFilter(self, event: wx.CommandEvent) -> bool:
        """Filter results by Z score.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnAutoFilter(self.IsChecked(event.GetId()))
        
        return True
    #---

    def OnFilter(self, event: wx.CommandEvent) -> bool:
        """Perform selected action.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.dKeyMethod[self.rKeyID[event.GetId()]]()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class LockPlotScale(wx.Menu):
    """Lock the plots scale to the selected option
    
        Attributes
        ----------
        nameID : dict
            To map menu items to the Lock type. Keys are MenuItems.GetId() and 
            values are str. 
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNo      = self.Append(-1, 'No',         kind=wx.ITEM_RADIO)
        self.miDate    = self.Append(-1, 'To Date',    kind=wx.ITEM_RADIO)
        self.miProject = self.Append(-1, 'To Project', kind=wx.ITEM_RADIO)
        
        self.miDate.Check()
        #endregion -----------------------------------------------> Menu Items
        
        #region ------------------------------------------------------> nameID
        self.rKeyID = { # Associate IDs with Tab names. Avoid manual IDs
            self.miNo.GetId()     : 'No',
            self.miDate.GetId()   : 'Date',
            self.miProject.GetId(): 'Project',
        }
        #endregion ---------------------------------------------------> nameID
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnLockScale, source=self.miNo)
        self.Bind(wx.EVT_MENU, self.OnLockScale, source=self.miDate)
        self.Bind(wx.EVT_MENU, self.OnLockScale, source=self.miProject)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    def OnLockScale(self, event: wx.CommandEvent) -> bool:
        """Lock or unlock the scale of the plots.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnLockScale(self.rKeyID[event.GetId()])
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class ClearSelLimProt(wx.Menu):
    """Clear the selection in a LimProtRes Window
    
        Attributes
        ----------
        rKeyID : dict
            To map menu items to the Clear type. Keys are MenuItems.GetId() and 
            values are str. 
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNoPept = self.Append(-1, 'Peptide')
        self.miNoFrag = self.Append(-1, 'Fragment')
        self.miNoGel  = self.Append(-1, 'Gel Spot')
        self.miNoBL   = self.Append(-1, 'Band/Lane')
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, 'All')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> 
        self.rKeyID = {
            self.miNoPept.GetId(): 'Peptide',
            self.miNoFrag.GetId(): 'Fragment',
            self.miNoGel.GetId() : 'Gel Spot',
            self.miNoBL.GetId()  : 'Band/Lane',
            self.miNoSel.GetId() : 'All',
        }
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoPept)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoFrag)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoGel)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoBL)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class method
    #region ---------------------------------------------------> Event methods
    def OnClearSelection(self, event: wx.CommandEvent) -> bool:
        """Clear the selection in a LimProt Res Window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        win = self.GetWindow()
        tKey = self.rKeyID[event.GetId()]
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Run
        win.dKeyMethod[tKey]()
        #endregion ------------------------------------------------> Run

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class MainPlotProt(PlotSubMenu):
    """Menu for the Main plot in a Proteolysis Window"""
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__('Shift')
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class BottomPlotProt(PlotSubMenu):
    """Menu for the Bottom plot in a Proteolysis Window"""
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__('Alt')
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ClearSelTarProt(wx.Menu):
    """Clear the selection in a TarProtRes Window
    
        Attributes
        ----------
        rKeyID : dict
            To map menu items to the Clear type. Keys are MenuItems.GetId() and 
            values are str. 
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNoPept = self.Append(-1, 'Peptide')
        self.miNoFrag = self.Append(-1, 'Fragment')
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, 'All')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> 
        self.rKeyID = {
            self.miNoPept.GetId(): 'Peptide',
            self.miNoFrag.GetId(): 'Fragment',
            self.miNoSel.GetId() : 'All',
        }
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoPept)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoFrag)
        self.Bind(wx.EVT_MENU, self.OnClearSelection, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class method
    #region ---------------------------------------------------> Event methods
    def OnClearSelection(self, event: wx.CommandEvent) -> bool:
        """Clear the selection in a LimProt Res Window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        win = self.GetWindow()
        tKey = self.rKeyID[event.GetId()]
        #endregion ------------------------------------------------> Variables
        
        #region ---------------------------------------------------> Run
        win.dKeyMethod[tKey]()
        #endregion ------------------------------------------------> Run

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---

#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus
class ProtProfToolMenu(wx.Menu, MenuMethods):
    """Tool menu for the Proteome Profiling Plot window.
        
        Parameters
        ----------
        cMenuData: dict
            Data needed to build the menu. See Notes below.
        
        Attributes
        ----------
        rPlotdate : list of wx.MenuItems
            Available dates in the analysis.
        
        Notes
        -----
        cMenuData has the following structure:
            {
                'menudate' : [List of dates as str],
                'crp' : {
                    'date1' : {
                        'C' : [List of conditions as str],
                        'RP': [List of relevant points as str],
                    }
                    .......
                    'dateN'
                }
            }    
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = cMenuData
        self.rPlotDate = []
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.cMenuData['menudate'])
        self.AppendSeparator()
        #------------------------------> Volcano Plot
        self.mVolcano =  VolcanoPlot(
                self.cMenuData['crp'], self.rPlotDate[0].GetItemLabelText()
        )
        self.AppendSubMenu(self.mVolcano, 'Volcano Plot',)
        self.AppendSeparator()
        #------------------------------> Relevant Points
        self.mFc = FCEvolution()
        self.AppendSubMenu(self.mFc, 'FC Evolution')
        self.AppendSeparator()
        #------------------------------> Filter
        self.mFilter = FiltersProtProf()
        self.AppendSubMenu(self.mFilter, 'Filters')
        self.AppendSeparator()
        #------------------------------> Lock scale
        self.mLockScale = LockPlotScale()
        self.AppendSubMenu(self.mLockScale, 'Lock Plot Scale')
        self.AppendSeparator()
        #------------------------------> Duplicate Window
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        #------------------------------> 
        self.miDataPrep = self.Append(-1, 'Data Preparation\tCtrl+P')
        self.AppendSeparator()
        #------------------------------> Export Data
        self.miSaveD  = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveFD = self.Append(-1, 'Export Data Filtered\tShift+Ctrl+E')
        self.miSaveI  = self.Append(-1, 'Export Images\tShift+Alt+I')
        self.AppendSeparator()
        #------------------------------> 
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Alt+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'AllImg',
            self.miZoomR.GetId(): 'AllZoom',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnDupWin,            source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData,    source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnExportFilteredData,source=self.miSaveFD)
        self.Bind(wx.EVT_MENU, self.OnCheckDataPrep,     source=self.miDataPrep)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,         source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,     source=self.miSaveI)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    #------------------------------> Event Methods
    def OnPlotDate(self, event: wx.CommandEvent) -> bool:
        """Plot a date of a section in an UMSAP file.
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
                
            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Date
        tDate = self.GetLabelText(event.GetId())
        #endregion -----------------------------------------------------> Date
        
        #region -----------------------------------------> Update Volcano menu
        self.mVolcano.UpdateCondRP(tDate)
        #endregion --------------------------------------> Update Volcano menu
        
        #region --------------------------------------------------------> Draw
        win = self.GetWindow()
        win.UpdateDisplayedData(
            tDate,
            *self.mVolcano.GetData4Draw(),
            *self.mFc.GetData4Draw(),
        )
        #endregion -----------------------------------------------------> Draw
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class LimProtToolMenu(wx.Menu, MenuMethods):
    """Tool menu for the Limited Proteolysis window
    
        Parameters
        ----------
        cMenuData: dict
            Data needed to build the menu. See Notes below.
            
        Attributes
        ----------
        rPlotdate : list of wx.MenuItems
            Available dates in the analysis.
        
        Notes
        -----
        menuData has the following structure:
            {
                'menudate' : [List of dates as str],
            }    
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = cMenuData
        self.rPlotDate = []
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.cMenuData['menudate'])
        self.AppendSeparator()
        #------------------------------> 
        self.miBandLane = self.Append(
            -1, 'Lane Selection Mode\tCtrl+L', kind=wx.ITEM_CHECK)
        self.AppendSeparator()    
        #------------------------------> 
        self.miShowAll = self.Append(-1, 'Show All\tCtrl+A')
        self.AppendSeparator()
        #------------------------------> 
        self.mFragmentMenu = MainPlotProt()
        self.AppendSubMenu(self.mFragmentMenu, 'Fragments')
        self.AppendSeparator()
        #------------------------------> 
        self.mGelMenu = BottomPlotProt()
        self.AppendSubMenu(self.mGelMenu, 'Gel')
        self.AppendSeparator()
        #------------------------------> 
        self.mClearMenu = ClearSelLimProt()
        self.AppendSubMenu(self.mClearMenu, 'Clear Selection')
        self.AppendSeparator()
        #------------------------------> Duplicate Window
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        #------------------------------> 
        self.miDataPrep = self.Append(-1, 'Data Preparation')
        self.AppendSeparator()
        #------------------------------> Export Data
        self.miSaveD  = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI  = self.Append(-1, 'Export Images\tShift+Alt+I')
        self.miSaveS  = self.Append(-1, 'Export Sequences\tCtrl+S')
        self.AppendSeparator()
        #------------------------------>
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Alt+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'AllImg',
            self.miZoomR.GetId(): 'AllZoom',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnLaneBand,       source=self.miBandLane)
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnDupWin,         source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnCheckDataPrep,  source=self.miDataPrep)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnShowAll,        source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnExportSeq,      source=self.miSaveS)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    def OnLaneBand(self, event: wx.CommandEvent) -> bool:
        """Change between Lane and Band selection mode.

            Parameters
            ----------
            event:wx.Event
                Information about the event


            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnLaneBand(self.miBandLane.IsChecked())
        
        return True
    #---
        
    def OnShowAll(self, event: wx.CommandEvent) -> bool:
        """Show all fragments
    
            Parameters
            ----------
            event:wx.Event
                Information about the event

    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.OnShowAll()
        
        return True
    #---
    
    def OnExportSeq(self, event: wx.CommandEvent) -> bool:
        """Export Sequences to pdf
    
            Parameters
            ----------
            event:wx.Event
                Information about the event

    
            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.ExportSeq()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class TarProtToolMenu(wx.Menu, MenuMethods):
    """Tool menu for the Targeted Proteolysis window
    
        Parameters
        ----------
        cMenuData: dict
            Data needed to build the menu. See Notes below.
            
        Attributes
        ----------
        rPlotdate : list of wx.MenuItems
            Available dates in the analysis.
        
        Notes
        -----
        menuData has the following structure:
            {
                'menudate' : [List of dates as str],
            }    
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = cMenuData
        self.rPlotDate = []
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Add Dates
        self.AddDateItems(self.cMenuData['menudate'])
        self.AppendSeparator()
        #------------------------------> 
        self.mFragmentMenu = MainPlotProt()
        self.AppendSubMenu(self.mFragmentMenu, 'Fragments')
        self.AppendSeparator()
        #------------------------------> 
        self.mGelMenu = BottomPlotProt()
        self.AppendSubMenu(self.mGelMenu, 'Intensities')
        self.AppendSeparator()
        #------------------------------> 
        self.mClear = ClearSelTarProt()
        self.AppendSubMenu(self.mClear, 'Clear Selection')
        self.AppendSeparator()
        #------------------------------> Duplicate Window
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        #------------------------------> 
        self.miDataPrep = self.Append(-1, 'Data Preparation')
        self.AppendSeparator()
        #------------------------------> Export Data
        self.miSaveD  = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI  = self.Append(-1, 'Export Images\tShift+Alt+I')
        self.AppendSeparator()
        #------------------------------>
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Alt+Z')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        self.rKeyID = {
            self.miSaveI.GetId(): 'AllImg',
            self.miZoomR.GetId(): 'AllZoom',
        }
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnSavePlotImage,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnDupWin,         source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnCheckDataPrep,  source=self.miDataPrep)
        self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.miSaveD)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class methods
    #region ---------------------------------------------------> Event methods
    
    #endregion ------------------------------------------------> Event methods
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
        self.mModule  = Module()
        self.mUtility = Utility()
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------> Append to menubar
        self.Append(self.mModule, '&Modules')
        self.Append(self.mUtility, '&Utilities')
        #endregion ----------------------------------------> Append to menubar
    #endregion ------------------------------------------------ Instance Setup
#---


class ToolMenuBar(MainMenuBar):
    """Menu bar for a window showing the corresponding tool menu
    
        Parameters
        ----------
        cName : str
            Unique name of the window/tab for which the Tool menu will be 
            created
        cMenuData : dict
            Data to build the Tool menu of the window. See structure in the
            window or menu class.
        dTool: dict
            Methods to create the Tool Menu
    """

    #region -----------------------------------------------------> Class Setup
    dTool = { # Key are window name
        config.nwUMSAPControl : FileControlToolMenu,
        config.nwCorrAPlot    : CorrAPlotToolMenu,
        config.nwCheckDataPrep: DataPrepToolMenu,
        config.nwProtProf     : ProtProfToolMenu,
        config.nwLimProt      : LimProtToolMenu,
        config.nwTarProt      : TarProtToolMenu,
    }
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------- Instance Setup
    def __init__(self, cName: str, cMenuData: Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------> Menu items & Append
        if cName in self.dTool:
            self.mTool = self.dTool[cName](cMenuData)
            self.Insert(config.toolsMenuIdx, self.mTool, 'Tools')
        else:
            pass
        #endregion --------------------------------------> Menu items & Append
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar
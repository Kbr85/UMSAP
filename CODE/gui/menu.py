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


"""Menus of the application"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Callable, Optional

import wx

import config.config as config
import dtscore.window as dtsWindow
import gui.method as method
import gui.window as window
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class BaseMenu(wx.Menu):
    """Base class for the menus in the app.

        Attributes
        ----------
        rIDMap: dict
            Maps menu item's ID with function in window, e.g.
            {self.miSaveI.GetId() : config.klToolExpImgAll,}
        rKeyMap : dict
            Maps menu items's ID with the keywords of the corresponding
            functions in the win, e.g.
            {self.miMon.GetId(): 'mon',}

        Notes
        -----
        Methods in the class assumes the window related to the menu has a dict
        win.dKeyMethod. Values in win.dKeyMethod are methods in the window
        while keys are the values in self.rIDMap. This allows binding a 
        wx.MenuItem directly to the method in the window. Look at self.OnMethod
        for an example and self.OnMethodKey for an example using keyword 
        arguments.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #------------------------------>
        self.rIDMap  = {}
        self.rKeyMap = {}
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnCreateTab(self, event:wx.CommandEvent) -> bool:
        """Creates a new tab in the main window.

            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Check MainW
        if config.winMain is None:
            config.winMain = window.MainWindow()
        else:
            pass
        #endregion ----------------------------------------------> Check MainW

        #region --------------------------------------------------> Create Tab
        config.winMain.OnCreateTab(self.rIDMap[event.GetId()])
        #endregion -----------------------------------------------> Create Tab
        
        return True
    #---

    def OnMethod(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with no arguments or
            keyword arguments.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        win = self.GetWindow()
        win.dKeyMethod[self.rIDMap[event.GetId()]]()
        return True
    #---

    def OnMethodLabel(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with the text of the menu
            item as argument.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        tID = event.GetId()
        win = self.GetWindow()
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[self.rIDMap[tID]](self.GetLabelText(tID))
        #endregion ----------------------------------------------> Call Method

        return True
    #---
    
    def OnMethodLabelBool(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with the boolean of the
            menu item as argument.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
            
            Notes
            -----
            Method assumes the wx.MenuItem is a radio or check item that will
            be True if checked or False if not checked.
        """
        #region ---------------------------------------------------> Variables
        tID = event.GetId()
        win = self.GetWindow()
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[self.rIDMap[tID]](self.IsChecked(tID))
        #endregion ----------------------------------------------> Call Method

        return True
    #---
    
    def OnMethodKey(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with a keyword argument.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        tID = event.GetId()
        win = self.GetWindow()
        tFunctionKey = self.rIDMap[tID]
        tDict = {self.rKeyMap[tID] : self.GetLabelText(tID)}
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[tFunctionKey](**tDict)
        #endregion ----------------------------------------------> Call Method

        return True
    #---
    
    def OnMethodKeyBool(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with a keyword argument 
            with boolean value.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
            
            Notes
            -----
            Method assumes the wx.MenuItem is a radio or check item that will
            be True if checked or False if not checked.
        """
        #region ---------------------------------------------------> Variables
        tID = event.GetId()
        win = self.GetWindow()
        tFunctionKey = self.rIDMap[tID]
        tDict = {self.rKeyMap[tID] : self.IsChecked(tID)}
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[tFunctionKey](**tDict)
        #endregion ----------------------------------------------> Call Method

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class BaseMenuMainResult(BaseMenu):
    """Menu for a window plotting results with a list of available analysis IDs
        as first items, e.g. Correlation Analysis

        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu of the window. It must contain at least
            a key - value pair like:
            'MenuDate' : ['20210324-123456 - bla',..., '20220730-105402 - bla2']

        Attributes
        ----------
        cMenuData : dict
            Data to build the Tool menu of the window. It must contain at least
            a key - value pair like:
            'MenuDate' : ['20210324-123456 - bla',..., '20220730-105402 - bla2']
        rPlotDate : list[wx.MenuItems]
            List of available menu items representing the analysis IDs.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData = menuData
        self.rPlotDate = []
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddDateItems(self.cMenuData['MenuDate'])
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #region ---------------------------------------------------> Class Methods
    def AddDateItems(self, menuDate: list[str]) -> bool:
        """Add and bind the analysis ID items. 

            Parameters
            ----------
            menuDate: list of str.
                Available dates to plot e.g. '20210324-123456 - bla'

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Add items
        for k in menuDate:
            #------------------------------> Item
            self.rPlotDate.append(self.AppendRadioItem(-1, k))
            #------------------------------> Add to dict
            self.rIDMap[self.rPlotDate[-1].GetId()]  = config.klToolGuiUpdate
            self.rKeyMap[self.rPlotDate[-1].GetId()] = 'tDate'
            #------------------------------> Bind
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.rPlotDate[-1])
        #endregion ------------------------------------------------> Add items

        #region -----------------------------------------------> Add Separator
        self.AppendSeparator()
        #endregion --------------------------------------------> Add Separator

        return True
    #---

    def AddLastItems(self, onePlot:bool=True) -> bool:
        """Add the last items to the Tool menu of a window showing results.

            Parameters
            ----------
            onePlot: bool
                Configure the keyboard shortcut depending on the number of plots
                on the window.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        shortCut = 'Ctrl' if onePlot else 'Shift+Alt'
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Add Items
        self.miCheckDP = self.Append(-1, 'Data Preparation\tCtrl+P')
        self.AppendSeparator()
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        self.miSaveD = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI = self.Append(-1, f'Export Image\t{shortCut}+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'Reset Zoom\t{shortCut}+Z')
        #endregion ------------------------------------------------> Add Items

        #region --------------------------------------------------> Add rIDMap
        rIDMap = {
            self.miDupWin.GetId()  : config.klToolDupWin,
            self.miZoomR.GetId()   : config.klToolZoomResetAll,
            self.miSaveD.GetId()   : config.klToolExpData,
            self.miSaveI.GetId()   : config.klToolExpImgAll,
            self.miCheckDP.GetId() : config.klToolCheckDP,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion -----------------------------------------------> Add rIDMap

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miCheckDP)
        #endregion -----------------------------------------------------> Bind

        return True
    #---

    def UpdateDateItems(self, menuData: dict) -> bool:
        """Update the Analysis ID items when the analyses are modified. 

            Parameters
            ----------
            menuData : dict
                Data to build the Tool menu of the window. It must contain at 
                least a key - value pair like:
                'MenuDate' : ['20210324-123456 - bla',...,]

            Returns
            -------
            bool
            
            Notes
            -----
            Menu Further Analysis, if present, is expected to be at 
            self.mFurtherA and implement the method
            UpdateFurtherAnalysis(date, menuData['FA']) to handle the update of
            the Further Analysis menu.
        """
        #region ---------------------------------------------------> Variables
        checked      = self.GetCheckedRadioItem(self.rPlotDate)
        checkedLabel = checked.GetItemLabelText()
        checkedFound = False
        #------------------------------> 
        for k in self.rPlotDate:
            del self.rIDMap[k.GetId()]
            del self.rKeyMap[k.GetId()]
            self.Delete(k)
        self.rPlotDate = []
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Dates
        #------------------------------> Add new items
        for k in reversed(menuData['MenuDate']):
            self.rPlotDate.insert(0, self.InsertRadioItem(0,-1,k))
            self.rIDMap[self.rPlotDate[0].GetId()] = config.klToolGuiUpdate
            self.rKeyMap[self.rPlotDate[0].GetId()] = 'tDate'
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.rPlotDate[0])
        #------------------------------> Search for previously checked item
        for k in self.rPlotDate:
            if k.GetItemLabelText() == checkedLabel:
                k.Check(check=True)
                checkedFound = True
                break
            else:
                pass
        #------------------------------> Check first if not found
        if checkedFound:
            pass
        else:
            self.rPlotDate[0].Check(check=True)
            checked = self.rPlotDate[0]
        #endregion ----------------------------------------------------> Dates

        #region ------------------------------------------> Update Other Items
        # Update menu specific items, e.g. Further Analysis or Cond, RP in 
        # ProtProf - Volcano Plot. Also update GUI if checked is not the 
        # analysis currently displayed.
        self.__UpdateOtherItems(checked, not checkedFound)
        #endregion ---------------------------------------> Update Other Items

        return True
    #---

    def __UpdateOtherItems(self, tDate: wx.MenuItem, updateGUI: bool) -> bool:
        """Update specific items in the menu after the Analysis IDs were 
            updated. Override as needed.
    
            Parameters
            ----------
            tDate: wx.MenuItem
                Currently selected Analysis ID
            updateGUI: bool
                Update (True) the data displayed or not (False).
    
            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Update GUI
        if updateGUI:
            self.OnMethodKey(wx.CommandEvent(id=tDate.GetId()))
        else:
            pass
        #endregion ------------------------------------------------> Update GUI

        return True
    #---

    def GetCheckedRadioItem(self, lMenuItem: list[wx.MenuItem]) -> wx.MenuItem: # type: ignore
        """Get the checked item in a list of radio menu items.

            Parameters
            ----------
            lMenuItem: list of wx.MenuItems
                Items are expected to be radio items from the same group.

            Returns
            -------
            str
                Label of the checked item
        """
        #region -----------------------------------------------------> Checked
        for k in lMenuItem:
            if k.IsChecked():
                return k
            else:
                pass
        #endregion --------------------------------------------------> Checked
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class BaseMenuMainResultSubMenu(BaseMenu):
    """Sub menu items for a plot region. 

        Parameters
        ----------
        tKey: str
            For keyboard binding. Shift or Alt.
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
        self.rIDMap = {
            self.miSaveI.GetId(): f'{self.rKeys[tKey]}-Img',
            self.miZoomR.GetId(): f'{self.rKeys[tKey]}-Zoom',
        }
        #endregion ------------------------------------------------> rKeyID
        
        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSaveI)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class BaseMenuFurtherAnalysis(BaseMenu):
    """Base Menu for Further Analysis windows, e.g. AA
    
        Parameters
        ----------
        menuData: dict
            Information for the menu items. See Child class for details about
            the content.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rMenuData = menuData
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def AddNatRecSeqEntry(
        self, tMethod: Callable, idMap: str='', idKey: str='') -> bool:
        """Add the Native Sequence entry to the menu.

            Parameters
            ----------
            tMethod: Callable
                Method to call when the menu is selected.
            idMap : str
                Value for the self.rIDMap entry
            idKey: str
                Value for the self.rKeyMap entry

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Add Entry
        if self.rMenuData['Nat']:
            #------------------------------> Add Item
            self.miNat = self.Append(-1, config.lmNatSeq, kind=wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, tMethod, source=self.miNat)
            #------------------------------> IDMap
            if idMap:
                rIDMap = {self.miNat.GetId():idMap}
                self.rIDMap = self.rIDMap | rIDMap
            else:
                pass
            #------------------------------> KeyMap
            if idKey:
                rKeyMap = {self.miNat.GetId(): idKey}
                self.rKeyMap = self.rKeyMap | rKeyMap
            else:
                pass
        else:
            pass
        #endregion ------------------------------------------------> Add Entry

        return True
    #---

    def AddLastItems(self, onePlot:bool=True) -> bool:
        """Add the last items to the Tool menu of a window showing results.

            Parameters
            ----------
            onePlot: bool
                Configure the keyboard shortcut depending on the number of plots
                on the window.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        shortCut = 'Ctrl' if onePlot else 'Shift+Alt'
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Add Items
        self.miClear = self.Append(-1, 'Clear Selections\tCtrl+K')
        self.AppendSeparator()
        self.miDupWin = self.Append(-1, 'Duplicate Window\tCtrl+D')
        self.AppendSeparator()
        self.miSaveD = self.Append(-1, 'Export Data\tCtrl+E')
        self.miSaveI = self.Append(-1, f'Export Image\t{shortCut}+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'Reset Zoom\t{shortCut}+Z')
        #endregion ------------------------------------------------> Add Items

        #region --------------------------------------------------> Add rIDMap
        self.rIDMap[self.miDupWin.GetId()]  = config.klToolDupWin
        self.rIDMap[self.miZoomR.GetId()]   = config.klToolZoomResetAll
        self.rIDMap[self.miSaveD.GetId()]   = config.klToolExpData
        self.rIDMap[self.miSaveI.GetId()]   = config.klToolExpImgAll
        #endregion -----------------------------------------------> Add rIDMap

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miDupWin)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miSaveD)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnClear,       source=self.miClear)
        #endregion -----------------------------------------------------> Bind

        return True
    #---

    def OnClear(self, event:wx.CommandEvent) -> bool:
        """Override as needed.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event

            Returns
            -------
            bool
        """
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseMenuFurtherAnalysisEntry(BaseMenu):
    """Base Menu for Further Analysis submenu, e.g. in TarProt result window.

        Parameters
        ----------
        menuData: dict
            Information for menu entries.
            {
                'Date' : {'dictKey': ['E1', 'E2',...]},
                'DateN': {'dictKey': ['E1', 'E2',...]},
            }
        ciDate: str
            Currently selected date
        dictKey: str
            Prefix for the key in self.rIDMap
        itemLabel: str
            Label for New Analysis entry.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, menuData: dict, ciDate: str, dictKey: str, itemLabel: str
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cMenuData  = menuData
        self.rDictKey   = dictKey
        self.rItemLabel = itemLabel
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.rItemList = self.SetItems(ciDate)
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetItems(self, tDate: str) -> list[wx.MenuItem]:
        """Set the menu items.

            Parameters
            ----------
            tDate: str
                Currently selected date.

            Returns
            -------
            list[wx.MenuItem]
        """
        #region ---------------------------------------------------> Variables
        itemList = []
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        #------------------------------> Available Date
        for v in self.cMenuData[tDate][self.rDictKey]:
            itemList.append(self.Append(-1, v))
            self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=itemList[-1])
            self.rIDMap[itemList[-1].GetId()] = f'{self.rDictKey}-Item'
        #------------------------------> Separator
        if self.cMenuData[tDate][self.rDictKey]:
            self.rSep = self.AppendSeparator()
        else:
            self.rSep = None
        #------------------------------> New Analysis
        itemList.append(self.Append(-1, self.rItemLabel))
        self.Bind(wx.EVT_MENU, self.OnMethod, source=itemList[-1])
        self.rIDMap[itemList[-1].GetId()] = f'{self.rDictKey}-New'
        #endregion ------------------------------------------------>

        return itemList
    #---

    def Update(self, tDate: str, menuData: dict={}) -> bool:
        """Update the menu items.
    
            Parameters
            ----------
            tDate: str
                Currently selected date.
            menuDate: dict
                New menuData dict.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> 
        for x in self.rItemList:
            self.Delete(x)

        if self.rSep is not None:
            self.Delete(self.rSep)
        else:
            pass
        #endregion -----------------------------------------------------> 

        #region ---------------------------------------------------> 
        self.cMenuData = menuData if menuData else self.cMenuData
        self.rItemList = self.SetItems(tDate)
        #endregion ------------------------------------------------> 

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion -----------------------------------------------------> Base Classes


#region ----------------------------------------------------> Individual menus
class MenuModule(BaseMenu):
    """Menu with module entries."""
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
        self.rIDMap = { # Associate IDs with Tab names. Avoid manual IDs
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
    #---
    #endregion ------------------------------------------------ Instance Setup
#---


class MenuUtility(BaseMenu):
    """Menu with the utilities entries."""
    #region --------------------------------------------------> Instance Setup
    def __init__(self) -> None:
        """"""
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.miCorrA    = self.Append(-1, config.nuCorrA)
        self.miDataPrep = self.Append(-1, config.nuDataPrep)
        self.AppendSeparator()
        self.miReadFile = self.Append(-1, f'{config.nuReadF}\tCtrl+R')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.rIDMap = {
            self.miCorrA.GetId()   : config.ntCorrA,
            self.miDataPrep.GetId(): config.ntDataPrep,
        }
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnReadFile,  source=self.miReadFile)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miCorrA)
        self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.miDataPrep)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance Setup

    #region ---------------------------------------------------> Event Methods
    def OnReadFile(self, event: wx.CommandEvent) -> bool:
        """Read an UMSAP output file.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Window
        win = self.GetWindow()
        #endregion ---------------------------------------------------> Window

        #region ---------------------------------------------------> Get fileP
        try:
            #------------------------------> 
            dlg = dtsWindow.FileSelectDialog(
                'openO', 
                ext    = config.elUMSAP,
                parent = win,
                msg    = config.mFileSelUMSAP,
            )
            #------------------------------> 
            if dlg.ShowModal() == wx.ID_OK:
                fileP = Path(dlg.GetPath())
            else:
                return False
        except Exception as e:
            dtsWindow.NotificationDialog(
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

        dlg.Destroy()
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class MenuHelp(BaseMenu):
    """Menu with the help entries."""
    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miAbout    = self.Append(-1, config.klHelpAbout)
        self.AppendSeparator()
        self.miManual   = self.Append(-1, config.klHelpManual)
        self.miTutorial = self.Append(-1, config.klHelpTutorial)
        self.AppendSeparator()
        self.miCheckUpd = self.Append(-1, config.klHelpCheckUpd)
        self.AppendSeparator()
        self.miPref     = self.Append(-1, config.klHelpPref)
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> Links
        self.rIDMap = {
            self.miAbout.GetId   (): config.klHelpAbout,
            self.miManual.GetId  (): config.klHelpManual,
            self.miTutorial.GetId(): config.klHelpTutorial,
            self.miCheckUpd.GetId(): config.klHelpCheckUpd,
            self.miPref.GetId    (): config.klHelpPref,
        }
        #endregion ------------------------------------------------> Links

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miAbout)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miManual)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miTutorial)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miCheckUpd)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miPref)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolFileControl(BaseMenu):
    """Tool menu for the UMSAP file control window"""
    #region --------------------------------------------------> Instance setup
    def __init__(self, *args, **kwargs) -> None:
        """*args and **kwargs are needed to use this menu with ToolMenuBar.
            All of them are ignored here.
        """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miAddData = self.Append(-1, f'{config.klToolUMSAPCtrlAdd}\tCtrl+A')
        self.AppendSeparator()
        self.miDelData = self.Append(-1, f'{config.klToolUMSAPCtrlDel}\tCtrl+X')
        self.AppendSeparator()
        self.miExpData = self.Append(-1, f'{config.klToolUMSAPCtrlExp}\tCtrl+E')
        self.AppendSeparator()
        self.miUpdateFile = self.Append(-1, 'Reload File\tCtrl+U')
        #endregion -----------------------------------------------> Menu Items

        #region -------------------------------------------------------> Links
        self.rIDMap = {
            self.miAddData.GetId()   : config.klToolUMSAPCtrlAddDelExp,
            self.miDelData.GetId()   : config.klToolUMSAPCtrlAddDelExp,
            self.miExpData.GetId()   : config.klToolUMSAPCtrlAddDelExp,
            self.miUpdateFile.GetId(): config.klToolUMSAPCtrlReload,
        }
        #endregion ----------------------------------------------------> Links

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miAddData)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miDelData)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miExpData)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miUpdateFile)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolCorrA(BaseMenuMainResult):
    """Creates the Tools menu for a Correlation Analysis Plot window 

        Parameters
        ----------
        menuData : dict
            Data to build the Tool menu. See Notes for more details.

        Notes
        -----
        menuData has the following structure:
        {
            'MenuDate' : ['dateA',....,'dateN'],
        }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miColName  = self.Append(
            -1, config.lmCorrAColName, kind=wx.ITEM_RADIO)
        self.miColNumber = self.Append(
            -1, config.lmCorrAColNum,kind=wx.ITEM_RADIO)
        #------------------------------>
        self.AppendSeparator()
        self.miAllCol = self.Append(-1, config.lmCorrAAllCol)
        self.miSelCol = self.Append(-1, config.lmCorrASelCol)
        #------------------------------>
        self.AppendSeparator()
        self.miColBar = self.Append(-1, "Show ColorBar",kind=wx.ITEM_CHECK)
        self.miColBar.Check(check=False)
        #------------------------------>
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region -------------------------------------------------------> Names
        rIDMap = {
            self.miColName.GetId()  : config.klToolGuiUpdate,
            self.miColNumber.GetId(): config.klToolGuiUpdate,
            self.miColBar.GetId()   : config.klToolGuiUpdate,
            self.miSelCol.GetId()   : config.klToolCorrASelCol,
            self.miAllCol.GetId()   : config.klToolCorrASelCol,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miColName.GetId()  : 'col',
            self.miColNumber.GetId(): 'col',
            self.miColBar.GetId()   : 'bar',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKey,     source=self.miColName)
        self.Bind(wx.EVT_MENU, self.OnMethodKey,     source=self.miColNumber)
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miColBar)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel,   source=self.miSelCol)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel,   source=self.miAllCol)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolDataPrep(BaseMenuMainResult):
    """Tool menu for the Data Preparation Plot window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu. See Notes for more details.

        Notes
        -----
        menuData has the following structure:
        {
            'MenuDate' : [List of dates as str],
        }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict={}) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddLastItems(False)
        #------------------------------> Remove Check Data Prep
        self.DestroyItem(self.miCheckDP)
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuFCEvolution(BaseMenu):
    """Menu for a log2FC evolution along relevant points."""
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
        rIDMap = {
            self.miSaveI.GetId()  : 'FCImage',
            self.miZoomR.GetId()  : 'FCZoom',
            self.miShowAll.GetId(): 'FCShowAll',
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuFiltersProtProf(BaseMenu):
    """Menu for the ProtProfPlot Filters"""
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
        self.miUpdate = self.Append(
            -1, 'Auto Apply\tCtrl-Shift+F', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miRemoveAny  = self.Append(-1, 'Remove\tCtrl+Shift+R')
        self.miRemoveLast = self.Append(-1, 'Remove Last\tCtrl+Shift+Z')
        self.miRemoveAll  = self.Append(-1, 'Remove All\tCtrl+Shift+X')
        self.AppendSeparator()
        self.miCopy = self.Append(-1, 'Copy\tCtrl+Shift+C')
        self.miPaste = self.Append(-1, 'Paste\tCtrl+Shift+V')
        self.AppendSeparator()
        self.miSave = self.Append(-1, 'Save\tCtrl+Shift+S')
        self.miLoad = self.Append(-1, 'Load\tCtrl+Shift+L')
        #endregion -----------------------------------------------> Menu Items
        
        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miFcChange.GetId():  config.lFilFCEvol,
            self.miHypCurve.GetId():  config.lFilHypCurve,
            self.miLog2FC.GetId():    config.lFilFCLog,
            self.miPValue.GetId():    config.lFilPVal,
            self.miZScore.GetId():    f'{config.lFilZScore} F',
            self.miApply.GetId():     'Apply All',
            self.miRemoveLast.GetId():'Remove Last',
            self.miRemoveAny.GetId(): 'Remove Any',
            self.miRemoveAll.GetId(): 'Remove All',
            self.miCopy.GetId():      'Copy',
            self.miPaste.GetId():     'Paste',
            self.miSave.GetId():      'Save Filter',
            self.miLoad.GetId():      'Load Filter',
            self.miUpdate.GetId():    'AutoApplyFilter',
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miFcChange)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miLog2FC)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miPValue)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miApply)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miRemoveLast)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miRemoveAny)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miRemoveAll)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miCopy)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miPaste)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miSave)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miLoad)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miUpdate)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuLockPlotScale(BaseMenu):
    """Lock the plots scale to the selected option."""
    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNo      = self.Append(-1, 'No',         kind=wx.ITEM_RADIO)
        self.miDate    = self.Append(-1, 'Analysis',   kind=wx.ITEM_RADIO)
        self.miProject = self.Append(-1, 'Project',    kind=wx.ITEM_RADIO)
        self.miDate.Check()
        #endregion -----------------------------------------------> Menu Items

        #region ------------------------------------------------------> nameID
        rIDMap = {
            self.miNo.GetId()     : 'No',
            self.miDate.GetId()   : 'Analysis',
            self.miProject.GetId(): 'Project',
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miNo.GetId()     : 'mode',
            self.miDate.GetId()   : 'mode',
            self.miProject.GetId(): 'mode',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ---------------------------------------------------> nameID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miNo)
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miDate)
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miProject)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuClearSelLimProt(BaseMenu):
    """Clear the selection in a LimProtRes Window."""
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
        self.miNoSel  = self.Append(-1, 'All\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> 
        self.rIDMap = {
            self.miNoPept.GetId(): 'Peptide',
            self.miNoFrag.GetId(): 'Fragment',
            self.miNoGel.GetId() : 'Gel Spot',
            self.miNoBL.GetId()  : 'Band/Lane',
            self.miNoSel.GetId() : 'All',
        }
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoPept)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoFrag)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoGel)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoBL)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuClearSelTarProt(BaseMenu):
    """Clear the selection in a TarProtRes Window."""
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
        self.miNoSel  = self.Append(-1, 'All\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> 
        self.rIDMap = {
            self.miNoPept.GetId(): 'Peptide',
            self.miNoFrag.GetId(): 'Fragment',
            self.miNoSel.GetId() : 'All',
        }
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoPept)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoFrag)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuClearSelProtProf(BaseMenu):
    """Clear the selection in a ProtProf Res Window."""
    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miLabel = self.Append(-1, 'Labels')
        self.miSel   = self.Append(-1, 'Selection')
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, 'All\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> 
        rIDMap = {
            self.miLabel.GetId(): 'Labels',
            self.miSel.GetId(): 'Selection',
            self.miNoSel.GetId() : 'AllClear',
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miLabel)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSel)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolAA(BaseMenuFurtherAnalysis):
    """Tool menu for the AA result window.

        Parameters
        ----------
        menuData: dict
            Dict with the data for the menu with the following two entries:
            {
                'Label' : ['L1', 'L2',....],
                'Pos'   : ['P1', 'P2',....],
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rItems = []
        rIDMap = {}
        #------------------------------>
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Labels
        for k in menuData['Label']:
            self.rItems.append(self.Append(-1, k, kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.rItems[-1])
            rIDMap[self.rItems[-1].GetId()] = config.klToolAAExp
        self.rItems[0].Check()
        #------------------------------> Positions
        self.AppendSeparator()
        for k in menuData['Pos']:
            self.rItems.append(self.Append(-1, k, kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.rItems[-1])
            rIDMap[self.rItems[-1].GetId()] = config.klToolAAPos
        #------------------------------> Last Items
        self.AppendSeparator()
        self.AddLastItems()
        self.DestroyItem(self.miClear.GetId())
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------>
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnLabel(self, event: wx.CommandEvent) -> bool:
        """Change between Experiments.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        [x.Check(check=False) for x in self.rItems]
        tID = event.GetId()
        self.Check(tID, True)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.OnMethodLabel(event)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class MenuToolHist(BaseMenuFurtherAnalysis):
    """Tool menu for the Histogram result window.

        Parameters
        ----------
        menuData: dict
            Dict with the data for the menu with the following two entries:
            {
                'Label': ['L1', 'L2',....],
                'Nat: bool,
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddNatRecSeqEntry(
            self.OnMethodKeyBool, idMap=config.klToolGuiUpdate, idKey='nat')
        self.AppendSeparator()
        self.miUnique = self.Append(-1, 'Unique Cleavages', kind=wx.ITEM_CHECK)
        self.miUnique.Check(check=False)
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        rIDMap = {
            self.miUnique.GetId(): config.klToolGuiUpdate,
            
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------> 
        rKeyMap = {
            self.miUnique.GetId() : 'allC',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miUnique)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnClear(self, event: wx.CommandEvent)-> bool:
        """Clear all selections.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            self.miNat.Check(False)
        except AttributeError:
            pass
        #------------------------------>
        self.miUnique.Check(check=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = self.GetWindow()
        win.UpdatePlot(nat=False, allC=False)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class MenuToolCpR(BaseMenuFurtherAnalysis):
    """Tool menu for the Cleavage per Residue result window.

        Parameters
        ----------
        menuData: dict
            Dict with the data for the menu with the following two entries:
            {
                'Label': ['L1', 'L2',....],
                'Nat: bool,
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------>
        self.rItems = []
        for k in menuData['Label']:
            self.rItems.append(self.Append(-1, k, kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.rItems[-1])
        self.rItems[0].Check()
        self.AppendSeparator()
        #------------------------------>
        self.AddNatRecSeqEntry(self.OnLabel)
        self.AppendSeparator()
        #------------------------------>
        self.miSel = self.Append(
            -1, 'Single Selection\tCtrl+S', kind=wx.ITEM_CHECK)
        self.miSel.Check(True)
        #------------------------------> 
        if menuData['Nat']:
            self.miProtLoc = self.Append(
                -1, 'Show Native Protein Location', kind=wx.ITEM_CHECK)
            self.miProtLoc.Check(True)
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.miProtLoc)
        else:
            pass
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnLabel(self, event: wx.CommandEvent) -> bool:
        """Change between Experiments.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        try:
            nat = self.miNat.IsChecked()
        except AttributeError:
            nat = False
        #------------------------------> 
        try:
            show = self.miProtLoc.IsChecked()
        except AttributeError:
            show = False
        #------------------------------> 
        sel = self.miSel.IsChecked()
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        #------------------------------> Selection mode
        if sel and self.GetLabelText(event.GetId()) != config.lmNatSeq:
            [x.Check(False) for x in self.rItems]
            self.Check(event.GetId(), True)
        else:
            pass
        #------------------------------> Labels
        label = [x.GetItemLabel() for x in self.rItems if x.IsChecked()]
        if label:
            pass
        else:
            self.rItems[0].Check()
            label = [self.rItems[0].GetItemLabel()]
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        win = self.GetWindow()
        win.UpdatePlot(nat, label, show)
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def OnClear(self, event: wx.CommandEvent) -> bool:
        """Change between Experiments.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        #------------------------------>
        self.rItems[0].Check()
        [x.Check(False) for x in self.rItems[1:]]
        #------------------------------>
        try:
            self.miNat.Check(False)
        except AttributeError:
            pass
        #------------------------------>
        try:
            self.miProtLoc.Check(True)
        except AttributeError:
            pass
        #------------------------------>
        self.miSel.Check(True)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = self.GetWindow()
        win.UpdatePlot(False, [self.rItems[0].GetItemLabel()], True)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class MenuToolCleavageEvol(BaseMenuFurtherAnalysis):
    """Tool menu for the Cleavage Evolution.

        Parameters
        ----------
        menuData: dict
            Dict with the data for the menu with the following two entries:
            {
                'Label': ['L1', 'L2',....],
                'Nat: bool,
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddNatRecSeqEntry(
            self.OnMethodKeyBool, idMap=config.klToolGuiUpdate, idKey='nat')
        self.AppendSeparator()
        self.miMon = self.Append(-1, 'Monotonic', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> 
        rIDMap = {
            self.miMon.GetId() : config.klToolGuiUpdate,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miMon.GetId() : 'mon',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miMon)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnClear(self, event:wx.CommandEvent) -> bool:
        """Clear selections.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            self.miNat.Check(check=False)
        except AttributeError:
            pass
        #------------------------------>
        self.miMon.Check(check=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = self.GetWindow()
        win.UpdatePlot(nat=False, mon=False)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class MenuVolcanoPlotColorScheme(BaseMenu):
    """Menu for Color Scheme in the Volcano Plot menu of ProtProf result window.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miHypCurve = self.Append(
            -1, config.klToolVolPlotColorHypCurve, kind=wx.ITEM_RADIO)
        self.miPLogFC   = self.Append(
            -1, config.klToolVolPlotColorPFC, kind=wx.ITEM_RADIO)
        self.miZScore   = self.Append(
            -1, config.klToolVolPlotColorZ, kind=wx.ITEM_RADIO)
        self.AppendSeparator()
        self.miConfigure= self.Append(-1, 'Configure')
        #endregion -----------------------------------------------> Menu Items
        
        #region ------------------------------------------------------> rKeyID
        rIDMap = {
            self.miHypCurve.GetId() : config.klToolVolPlotColorHypCurve,
            self.miPLogFC.GetId  () : config.klToolVolPlotColorPFC,
            self.miZScore.GetId  () : config.klToolVolPlotColorZ,
            self.miConfigure.GetId(): config.klToolVolPlotColorConf,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ---------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miPLogFC)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miConfigure)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus
class MixMenuToolLimProt(BaseMenuMainResult):
    """Tool menu for the Limited Proteolysis window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu. 
            {'MenuDate' : [List of dates as str],}
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miBandLane = self.Append(
            -1, 'Lane Selection Mode\tCtrl+L', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        #------------------------------> 
        self.miShowAll = self.Append(-1, 'Show All\tCtrl+A')
        self.AppendSeparator()
        #------------------------------> 
        self.mFragmentMenu = BaseMenuMainResultSubMenu('Shift')
        self.AppendSubMenu(self.mFragmentMenu, 'Fragments')
        self.AppendSeparator()
        #------------------------------> 
        self.mGelMenu = BaseMenuMainResultSubMenu('Alt')
        self.AppendSubMenu(self.mGelMenu, 'Gel')
        self.AppendSeparator()
        #------------------------------> 
        self.mClearMenu = MenuClearSelLimProt()
        self.AppendSubMenu(self.mClearMenu, 'Clear Selection')
        self.AppendSeparator()
        #------------------------------> Last Items
        self.AddLastItems(False)
        #------------------------------> Add Export Sequence
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveSeq = self.Insert(pos+2, -1, "Export Sequences")
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miBandLane.GetId(): config.klToolLimProtBandLane,
            self.miShowAll.GetId() : config.klToolLimProtShowAll,
            self.miSaveSeq.GetId() : config.klToolExpSeq,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miBandLane)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miSaveSeq)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MixMenuToolTarProt(BaseMenuMainResult):
    """Tool menu for the Targeted Proteolysis window

        Parameters
        ----------
        cMenuData: dict
            Data needed to build the menu. 
            {'MenuDate' : [List of dates as str],}
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, cMenuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(cMenuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mFragmentMenu = BaseMenuMainResultSubMenu('Shift')
        self.AppendSubMenu(self.mFragmentMenu, 'Fragments')
        self.AppendSeparator()
        #------------------------------> 
        self.mGelMenu = BaseMenuMainResultSubMenu('Alt')
        self.AppendSubMenu(self.mGelMenu, 'Intensities')
        self.AppendSeparator()
        #------------------------------> 
        self.mFurtherA = MixMenuFurtherAnalysisTarProt(
            self.cMenuData['FA'], self.rPlotDate[0].GetItemLabelText())
        self.AppendSubMenu(self.mFurtherA, 'Further Analysis')
        self.AppendSeparator()
        #------------------------------> 
        self.mClear = MenuClearSelTarProt()
        self.AppendSubMenu(self.mClear, 'Clear Selection')
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems(False)
        #------------------------------> 
        #------------------------------> Add Export Sequence
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveSeq = self.Insert(pos+2, -1, "Export Sequences")
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveSeq.GetId() : config.klToolExpSeq,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSaveSeq)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #region ---------------------------------------------------> Class Methods
    def OnMethodKey(self, event) -> bool:
        """Call the corresponding method in the window with no arguments or
            keyword arguments

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> 
        super().OnMethodKey(event)
        #endregion ------------------------------------------------> 
        
        #region --------------------------------------------------------> 
        tID      = event.GetId()
        menuItem = self.FindItem(tID)[0]
        label    = self.GetLabelText(tID)
        #endregion -----------------------------------------------------> 

        #region --------------------------------------------------->
        if menuItem in self.rPlotDate:
            self.mFurtherA.UpdateFurtherAnalysis(label)
        else:
            pass
        #endregion ------------------------------------------------>
        
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class MixMenuVolcanoPlot(BaseMenu):
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
        rCrp has the following structure:
            {
                    'date1' : {
                        'C' : [List of conditions as str],
                        'RP': [List of relevant points as str],
                    }
                    .......
                    'dateN' : {}
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, cCrp: dict, ciDate: str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCrp = cCrp
        #------------------------------> Cond - RP separator. To remove/create.
        self.rSep = None
        #------------------------------> 
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.rCond, self.rRp = self.SetCondRPMenuItems(ciDate)
        self.AppendSeparator()
        self.miLabelProt = self.Append(-1, 'Add Label\tShift+A')
        self.miLabelPick = self.Append(
            -1, 'Pick Label\tShift+P', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.mColor = MenuVolcanoPlotColorScheme()
        self.AppendSubMenu(self.mColor, 'Color Scheme')
        self.AppendSeparator()
        self.miPCorr = self.Append(-1, 'Corrected P Values', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, 'Export Image\tShift+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, 'Reset Zoom\tShift+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miLabelPick.GetId() : config.klToolVolPlotLabelPick,
            self.miLabelProt.GetId() : config.klToolVolPlotLabelProt,
            self.miPCorr.GetId(): config.klToolGuiUpdate,
            self.miSaveI.GetId(): config.klToolVolPlotSaveI,
            self.miZoomR.GetId(): config.klToolVolPlotZoom,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------> 
        rKeyMap = {
            self.miPCorr.GetId() : 'corrP',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,        source=self.miLabelProt)
        self.Bind(wx.EVT_MENU, self.OnMethod,        source=self.miLabelPick)
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miPCorr)
        self.Bind(wx.EVT_MENU, self.OnMethod,        source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethod,        source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage methods
    def SetCondRPMenuItems(
        self, tDate: str
        ) -> tuple[list[wx.MenuItem], list[wx.MenuItem]]:
        """Set the menu items for conditions and relevant points as defined for 
            the current analysis date.

            Parameters
            ----------
            tDate : str
                Currently selected date.

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
            cond.append(wx.MenuItem(None, -1, text=c, kind=wx.ITEM_RADIO))
            #------------------------------> 
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=cond[-1])
            #------------------------------> 
            self.rIDMap[cond[-1].GetId()] = config.klToolVolPlot
            self.rKeyMap[cond[-1].GetId()] = 'cond'
        #------------------------------> Relevant Points
        for t in self.rCrp[tDate]['RP']:
            #------------------------------> 
            rp.append(wx.MenuItem(None, -1, text=t, kind=wx.ITEM_RADIO))
            #------------------------------> 
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=rp[-1])
            #------------------------------> 
            self.rIDMap[rp[-1].GetId()] = config.klToolVolPlot
            self.rKeyMap[rp[-1].GetId()] = 'rp'
        #endregion ---------------------------------------------> Add elements

        #region ---------------------------------------------------> Add items
        k = 0
        #------------------------------> Conditions
        for k,c in enumerate(cond):
            self.Insert(k,c)
        #------------------------------> Separator
        self.rSep = wx.MenuItem(None)
        self.Insert(k+1, self.rSep)
        #------------------------------> Relevant Points
        for j,t in enumerate(rp, k+2):
            self.Insert(j, t)
        #endregion ------------------------------------------------> Add items

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
        #------------------------------> RP
        for rp in self.rRp:
            self.Delete(rp)
        #endregion ------------------------------------------> Delete Elements

        #region -----------------------------------> Create & Add New Elements
        self.rCond, self.rRp = self.SetCondRPMenuItems(tDate)
        #endregion --------------------------------> Create & Add New Elements

        return True
    #---
    #endregion -----------------------------------------------> Manage methods
#---


class MixMenuFurtherAnalysisTarProt(BaseMenu):
    """Further Analysis menu for the TarProt result window

        Parameters
        ----------
        menuData: dict
            Information for menu items
            {
                'Date':{'FA1':['FA11', 'FA12',...],'FA2':['FA21', 'FA22',...],},
            }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict, ciDate:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #------------------------------> 
        self.mAA = BaseMenuFurtherAnalysisEntry(
            menuData, ciDate, 'AA', 'New AA Analysis')
        self.AppendSubMenu(self.mAA, 'AA Distribution')
        self.AppendSeparator()
        self.miCEvol = self.Append(-1, 'Cleavage Evolution')
        self.mHist   = BaseMenuFurtherAnalysisEntry(
            menuData, ciDate, 'Hist', 'New Histogram')
        self.AppendSubMenu(self.mHist, 'Cleavage Histograms')
        self.miCpR = self.Append(-1, 'Cleavage per Residue')
        self.AppendSeparator()
        self.miPDB = self.Append(-1, 'PDB Mapping')
        #endregion --------------------------------------------> Initial Setup
        
        #region ---------------------------------------------------> 
        rIDMap = {
            self.miCEvol.GetId() : config.klFACleavageEvol,
            self.miCpR.GetId()   : config.klFACleavagePerRes,
            self.miPDB.GetId()   : config.klFAPDBMap,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> 

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miCpR)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miCEvol)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miPDB)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def UpdateFurtherAnalysis(self, tDate: str, menuData: dict={}) -> bool:
        """Update Further Analysis.

            Parameters
            ----------
            tDate: str
                Currently selected date.
            menuData: dict
                Information for the menu items.

            Returns
            -------
            bool
        """
        self.mAA.Update(tDate, menuData)
        self.mHist.Update(tDate, menuData)

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class MixMenuToolProtProf(BaseMenuMainResult):
    """Tool menu for the Proteome Profiling Plot window.
        
        Parameters
        ----------
        menuData: dict
            Data needed to build the menu.
            {
                'MenuDate' : [List of dates as str],
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
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mVolcano =  MixMenuVolcanoPlot(
                self.cMenuData['crp'], self.rPlotDate[0].GetItemLabelText()
        )
        self.AppendSubMenu(self.mVolcano, 'Volcano Plot')
        self.AppendSeparator()
        #------------------------------> Relevant Points
        self.mFc = MenuFCEvolution()
        self.AppendSubMenu(self.mFc, 'FC Evolution')
        self.AppendSeparator()
        #------------------------------> Filter
        self.mFilter = MenuFiltersProtProf()
        self.AppendSubMenu(self.mFilter, 'Filters')
        self.AppendSeparator()
        #------------------------------> Lock scale
        self.mLockScale = MenuLockPlotScale()
        self.AppendSubMenu(self.mLockScale, 'Lock Plot Scale')
        self.AppendSeparator()
        #------------------------------> Clear Selection
        self.mClearSel = MenuClearSelProtProf()
        self.AppendSubMenu(self.mClearSel, 'Clear Selection')
        self.AppendSeparator()
        #------------------------------> 
        self.AddLastItems(False)
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnMethodKey(self, event):
        """Call the corresponding method in the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> 
        tID      = event.GetId()
        menuItem = self.FindItem(tID)[0]
        label    = self.GetLabelText(tID)
        #endregion -----------------------------------------------------> 

        #region --------------------------------------------------->
        if menuItem in self.rPlotDate:
            #------------------------------> Update Menu
            self.mVolcano.UpdateCondRP(label)
            #------------------------------> Update Plot
            win = self.GetWindow()
            win.UpdateDisplayedData(
                tDate = label,
                cond  = self.mVolcano.rCond[0].GetItemLabelText(),
                rp    = self.mVolcano.rRp[0].GetItemLabelText(),
            )
        else:
            super().OnMethodKey(event)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---
#endregion --------------------------------------------------------> Mix menus


#region -------------------------------------------------------------> Menubar
class MenuBarMain(wx.MenuBar):
    """Creates the application menu bar"""
    #region --------------------------------------------------- Instance Setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.mModule  = MenuModule()
        self.mUtility = MenuUtility()
        self.mHelp    = MenuHelp()
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------> Append to menubar
        self.Append(self.mModule,  '&Modules')
        self.Append(self.mUtility, '&Utilities')
        self.Append(self.mHelp,    '&Help')
        #endregion ----------------------------------------> Append to menubar
    #---
    #endregion ------------------------------------------------ Instance Setup
#---


class MenuBarTool(MenuBarMain):
    """Menu bar for a window showing the corresponding tool menu

        Parameters
        ----------
        cName : str
            Unique name of the window/tab for which the Tool menu will be 
            created
        menuData : dict
            Data to build the Tool menu of the window. See structure in the
            window or menu class.

        Attributes
        ----------
        dTool: dict
            Methods to create the Tool Menu
    """
    #region -----------------------------------------------------> Class Setup
    dTool = { # Key are window name and values the corresponding tool menu
        config.nwUMSAPControl : MenuToolFileControl,
        config.nwCorrAPlot    : MenuToolCorrA,
        config.nwCheckDataPrep: MenuToolDataPrep,
        config.nwProtProf     : MixMenuToolProtProf,
        config.nwLimProt      : MixMenuToolLimProt,
        config.nwTarProt      : MixMenuToolTarProt,
        config.nwAAPlot       : MenuToolAA,
        config.nwHistPlot     : MenuToolHist,
        config.nwCpRPlot      : MenuToolCpR,
        config.nwCEvolPlot    : MenuToolCleavageEvol,
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
    #---
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar
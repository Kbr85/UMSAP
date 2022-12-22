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


"""Core Menu methods and classes of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Callable

import wx

from config.config import config as mConfig
from core import window as cWindow
from main import window as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class BaseMenu(wx.Menu):
    """Base class for the menus in the app.

        Attributes
        ----------
        rIDMap: dict
            Maps menu item's ID with function in window, e.g.
            {self.miSaveI.GetId() : mConfig.klToolExpImgAll,}
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
        if mConfig.main.mainWin is None:
            mConfig.main.mainWin = mWindow.WindowMain()
        else:
            pass
        #endregion ----------------------------------------------> Check MainW

        #region --------------------------------------------------> Create Tab
        mConfig.main.mainWin.CreateTab(self.rIDMap[event.GetId()])
        #endregion -----------------------------------------------> Create Tab

        return True
    #---

    def OnMethod(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with no arguments or
            keyword arguments.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        win = self.GetWindow()
        win.dKeyMethod[self.rIDMap[event.GetId()]]()
        #endregion ------------------------------------------------>

        return True
    #---

    def OnMethodLabel(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with the text of the menu
            item as argument.

            Parameters
            ----------
            event: wx.CommandEvent
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

    def OnMethodLabelKey(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with the value associated
            with the menu item as argument.

            Parameters
            ----------
            event: wx.CommandEvent
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
        win.dKeyMethod[self.rIDMap[tID]](self.rKeyMap[tID])
        #endregion ----------------------------------------------> Call Method

        return True
    #---

    def OnMethodLabelBool(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with the boolean of the
            menu item as argument.

            Parameters
            ----------
            event: wx.CommandEvent
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
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        tID   = event.GetId()
        win   = self.GetWindow()
        tDict = {self.rKeyMap[tID] : self.GetLabelText(tID)}
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[self.rIDMap[tID]](**tDict)
        #endregion ----------------------------------------------> Call Method

        return True
    #---

    def OnMethodKeyBool(self, event:wx.CommandEvent) -> bool:
        """Call the corresponding method in the window with a keyword argument
            with boolean value.

            Parameters
            ----------
            event: wx.CommandEvent
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
        tID   = event.GetId()
        win   = self.GetWindow()
        tDict = {self.rKeyMap[tID] : self.IsChecked(tID)}
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Call Method
        win.dKeyMethod[self.rIDMap[tID]](**tDict)
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
    #region -----------------------------------------------------> Class Setup
    cLDataPrep  = 'Data Preparation'
    cLDupWin    = 'Duplicate Window'
    cLExpData   = 'Export Data'
    cLExpImg    = 'Export Image'
    cLZoomReset = 'Reset Zoom'
    #------------------------------>
    cVWinUpdate    = mConfig.core.kwWinUpdate
    cVDupWin       = mConfig.core.kwDupWin
    cVZoomResetAll = mConfig.core.kwZoomResetAll
    cVExpData      = mConfig.core.kwExpData
    cVExpImgAll    = mConfig.core.kwExpImgAll
    cVCheckDP      = mConfig.core.kwCheckDP
    #------------------------------>
    cVtDate = 'tDate'
    #endregion --------------------------------------------------> Class Setup

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
            self.rIDMap[self.rPlotDate[-1].GetId()]  = self.cVWinUpdate
            self.rKeyMap[self.rPlotDate[-1].GetId()] = self.cVtDate
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
        # pylint: disable=attribute-defined-outside-init
        self.miCheckDP = self.Append(-1, f'{self.cLDataPrep}\tCtrl+P')
        self.AppendSeparator()
        self.miDupWin = self.Append(-1, f'{self.cLDupWin}\tCtrl+D')
        self.AppendSeparator()
        self.miSaveD = self.Append(-1, f'{self.cLExpData}\tCtrl+E')
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\t{shortCut}+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\t{shortCut}+Z')
        #endregion ------------------------------------------------> Add Items

        #region --------------------------------------------------> Add rIDMap
        rIDMap = {
            self.miDupWin.GetId()  : self.cVDupWin,
            self.miZoomR.GetId()   : self.cVZoomResetAll,
            self.miSaveD.GetId()   : self.cVExpData,
            self.miSaveI.GetId()   : self.cVExpImgAll,
            self.miCheckDP.GetId() : self.cVCheckDP,
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
        self.cMenuData = menuData
        dateC = self.GetCheckedRadioItem(self.rPlotDate).GetItemLabelText()
        checkedFound   = False
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
            self.rIDMap[self.rPlotDate[0].GetId()] = mConfig.core.kwWinUpdate
            self.rKeyMap[self.rPlotDate[0].GetId()] = self.cVtDate
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.rPlotDate[0])
        #------------------------------> Search for previously checked item
        for k in self.rPlotDate:
            if k.GetItemLabelText() == dateC:
                k.Check(check=True)
                checkedFound = True
                menuItem = k
                break
            else:
                pass
        #------------------------------> Check first if not found
        if checkedFound:
            pass
        else:
            self.rPlotDate[0].Check(check=True)
            menuItem = self.rPlotDate[0]
        #endregion ----------------------------------------------------> Dates

        #region ------------------------------------------> Update Other Items
        # Update menu specific items, e.g. Further Analysis or Cond, RP in
        # ProtProf - Volcano Plot. Also update GUI if checked is not the
        # analysis currently displayed.
        self.UpdateOtherItems(menuItem, not checkedFound) # type: ignore
        #endregion ---------------------------------------> Update Other Items

        return True
    #---

    def UpdateOtherItems(self, tDate: wx.MenuItem, updateGUI: bool) -> bool:
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

        Attributes
        ----------
        rKeys: dict
            Map keyboard key to Main and Sec keywords.
    """
    #region -----------------------------------------------------> Class setup
    rKeys = {
        'Shift': 'Main',
        'Alt'  : 'Sec',
    }
    #------------------------------>
    cLExpImg    = 'Export Image'
    cLZoomReset = 'Reset Zoom'
    #------------------------------>
    cVExpImg    = mConfig.core.kwExpImg
    cVZoomReset = mConfig.core.kwZoomReset
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, tKey: str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\t{tKey}+I')
        self.miZoomR = self.Append(-1, f'{self.cVZoomReset}\t{tKey}+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveI.GetId(): self.cVExpImg,
            self.miZoomR.GetId(): self.cVZoomReset,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miSaveI.GetId(): self.rKeys[tKey],
            self.miZoomR.GetId(): self.rKeys[tKey],
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miZoomR)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miSaveI)
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

        Attributes
        ----------
        rMenuData: dict
            Information for the menu items. See Child class for details about
            the content.
    """
    #region -----------------------------------------------------> Class Setup
    cLClearSel  = 'Clear Selections'
    cLDupWin    = 'Duplicate Window'
    cLExpData   = 'Export Data'
    cLExpImg    = 'Export Image'
    cLZoomReset = 'Reset Zoom'
    #------------------------------>
    cVDupWin       = mConfig.core.kwDupWin
    cVZoomResetAll = mConfig.core.kwZoomResetAll
    cVExpData      = mConfig.core.kwExpData
    cVExpImg       = mConfig.core.kwExpImg
    #endregion --------------------------------------------------> Class Setup

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
        self,
        tMethod: Callable,
        idMap  : str='',
        idKey  : str='',
        ) -> bool:
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
            # pylint: disable=attribute-defined-outside-init
            self.miNat = self.Append(
                -1, mConfig.core.lmNatSeq, kind=wx.ITEM_CHECK)
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
        # pylint: disable=attribute-defined-outside-init
        self.miClear = self.Append(-1, f'{self.cLClearSel}\tCtrl+K')
        self.AppendSeparator()
        self.miDupWin = self.Append(-1, f'{self.cLDupWin}\tCtrl+D')
        self.AppendSeparator()
        self.miSaveD = self.Append(-1, f'{self.cLExpData}\tCtrl+E')
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\t{shortCut}+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\t{shortCut}+Z')
        #endregion ------------------------------------------------> Add Items

        #region --------------------------------------------------> Add rIDMap
        rIDMap = {
            self.miDupWin.GetId(): self.cVDupWin,
            self.miZoomR.GetId() : self.cVZoomResetAll,
            self.miSaveD.GetId() : self.cVExpData,
            self.miSaveI.GetId() : self.cVExpImg,
        }
        self.rIDMap = self.rIDMap | rIDMap
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

    def OnClear(self, event:wx.CommandEvent) -> bool:                           # pylint: disable=unused-argument
        """Override as needed.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

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

        Attributes
        ----------
        cMenuData: dict
            Information for menu entries.
            {
                'Date' : {'dictKey': ['E1', 'E2',...]},
                'DateN': {'dictKey': ['E1', 'E2',...]},
            }
        rDictKey: str
            Prefix for the key in self.rIDMap
        rItemLabel: str
            Label for New Analysis entry.
        rItemList: list
            List of wx.MenuItems
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        menuData : dict,
        ciDate   : str,
        dictKey  : str,
        itemLabel: str,
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

    def Update(self, tDate: str, menuData: dict={}) -> bool:                    # pylint: disable=dangerous-default-value
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
#endregion ----------------------------------------------------------> Classes


#region ----------------------------------------------------------------> Menu
class MenuModule(BaseMenu):
    """Menu with module entries."""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Labels
    cLLimProt  = mConfig.core.nmLimProt
    cLProtProf = mConfig.core.nmProtProf
    cLTarProt  = mConfig.core.nmTarProt
    #------------------------------> Key - Values
    cVLimProt  = mConfig.core.tLimProt
    cVProtProf = mConfig.core.tProtProf
    cVTarProt  = mConfig.core.tTarProt
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.miLimProt  = self.Append(-1, f'{self.cLLimProt}\tAlt+Ctrl+L')
        self.miProtProf = self.Append(-1, f'{self.cLProtProf}\tAlt+Ctrl+P')
        self.miTarProt  = self.Append(-1, f'{self.cLTarProt}\tAlt+Ctrl+T')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.rIDMap = { # Associate IDs with Tab names. Avoid manual IDs
            self.miLimProt.GetId() : self.cVLimProt,
            self.miProtProf.GetId(): self.cVProtProf,
            self.miTarProt.GetId() : self.cVTarProt,
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
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Labels
    cLCorrA    = mConfig.core.nuCorrA
    cLDataPrep = mConfig.core.nuDataPrep
    cLReadF    = mConfig.core.nuReadF
    #------------------------------> Key - Values
    cVCorrA    = mConfig.core.tCorrA
    cVDataPrep = mConfig.core.tDataPrep
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance Setup
    def __init__(self) -> None:
        """"""
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu items
        self.miCorrA    = self.Append(-1, self.cLCorrA)
        self.miDataPrep = self.Append(-1, self.cLDataPrep)
        self.AppendSeparator()
        self.miReadFile = self.Append(-1, f'{self.cLReadF}\tCtrl+R')
        #endregion -----------------------------------------------> Menu items

        #region -------------------------------------------------------> Names
        self.rIDMap = {
            self.miCorrA.GetId()   : self.cVCorrA,
            self.miDataPrep.GetId(): self.cVDataPrep,
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
    def OnReadFile(self, event: wx.CommandEvent) -> bool:                       # pylint: disable=unused-argument
        """Read an UMSAP output file.

            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Window
        win = self.GetWindow()
        #endregion ---------------------------------------------------> Window

        #region ---------------------------------------------------> Get fileP
        # dlg = cWindow.DialogFileSelect(
        #     'openO',
        #     ext    = mConfig.core.elUMSAP,
        #     parent = win,
        #     msg    = mConfig.core.mFileSelUMSAP,
        # )
        #------------------------------>
        # if dlg.ShowModal() == wx.ID_OK:
        #     fileP = Path(dlg.GetPath())
        # else:
        #     return False
        #endregion ------------------------------------------------> Get fileP

        #region ---------------------------------------------------> Load file
        # gMethod.LoadUMSAPFile(fileP=fileP)
        #endregion ------------------------------------------------> Load file

        # dlg.Destroy()
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class MenuHelp(BaseMenu):
    """Menu with the help entries."""
    #region ---------------------------------------------------> Class Setup
    #------------------------------> Label
    cLAbout       = 'About UMSAP'
    cLCheckUpdate = 'Check for Updates'
    cLManual      = 'Manual'
    cLPreference  = 'Preferences'
    cLTutorial    = 'Tutorial'
    #------------------------------> Key
    cVAbout       = mConfig.main.kwAbout
    cVCheckUpdate = mConfig.main.kwCheckUpd
    cVManual      = mConfig.main.kwManual
    cVPreference  = mConfig.main.kwPref
    cVTutorial    = mConfig.main.kwTutorial
    #endregion ------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miAbout    = self.Append(-1, self.cLAbout)
        self.AppendSeparator()
        self.miManual   = self.Append(-1, self.cLManual)
        self.miTutorial = self.Append(-1, self.cLTutorial)
        self.AppendSeparator()
        self.miCheckUpd = self.Append(-1, self.cLCheckUpdate)
        self.AppendSeparator()
        self.miPref     = self.Append(-1, self.cLPreference)
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> Links
        self.rIDMap = {
            self.miAbout.GetId()   : self.cVAbout,
            self.miManual.GetId()  : self.cVManual,
            self.miTutorial.GetId(): self.cVTutorial,
            self.miCheckUpd.GetId(): self.cVCheckUpdate,
            self.miPref.GetId()    : self.cVPreference,
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
#endregion -------------------------------------------------------------> Menu


#region -------------------------------------------------------------> MenuBar
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
        # mConfig.nwUMSAPControl : MenuToolFileControl,
        # mConfig.nwCorrAPlot    : MenuToolCorrA,
        # mConfig.nwCheckDataPrep: MenuToolDataPrep,
        # mConfig.nwProtProf     : MenuToolProtProf,
        # mConfig.nwLimProt      : MenuToolLimProt,
        # mConfig.nwTarProt      : MenuToolTarProt,
        # mConfig.nwAAPlot       : MenuToolAA,
        # mConfig.nwHistPlot     : MenuToolHist,
        # mConfig.nwCpRPlot      : MenuToolCpR,
        # mConfig.nwCEvolPlot    : MenuToolCleavageEvol,
    }
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------- Instance Setup
    def __init__(self, cName: str, menuData: dict={}) -> None:                  # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------> Menu items & Append
        if cName in self.dTool:
            self.mTool = self.dTool[cName](menuData)
            self.Insert(mConfig.core.toolMenuIdx, self.mTool, '&Tools')
        #endregion --------------------------------------> Menu items & Append
    #---
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> MenuBar

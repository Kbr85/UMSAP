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


"""Menu for the main module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolClearSel(cMenu.BaseMenu):
    """Clear the selection in a TarProtRes Window."""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Label
    cLPept = mConfig.tarp.lmClearPeptide
    cLFrag = mConfig.tarp.lmClearFragment
    cLAll  = mConfig.tarp.lmClearAll
    #------------------------------> Keyword value
    cVPept = mConfig.tarp.kwClearPeptide
    cVFrag = mConfig.tarp.kwClearFragment
    cVAll  = mConfig.tarp.kwClearAll
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNoPept = self.Append(-1, self.cLPept)
        self.miNoFrag = self.Append(-1, self.cLFrag)
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, f'{self.cLAll}\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        self.rIDMap = {
            self.miNoPept.GetId(): self.cVPept,
            self.miNoFrag.GetId(): self.cVFrag,
            self.miNoSel.GetId() : self.cVAll,
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


class ToolAA(cMenu.BaseMenuFurtherAnalysis):
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
    #region -----------------------------------------------------> Class Setup
    cVExp = mConfig.tarp.kwAAExp
    cVPos = mConfig.tarp.kwAAPos
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rItems = []
        rIDMap      = {}
        #------------------------------>
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        #------------------------------> Labels
        for k in menuData['Label']:
            self.rItems.append(self.Append(-1, k, kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.rItems[-1])
            rIDMap[self.rItems[-1].GetId()] = self.cVExp
        self.rItems[0].Check()
        #------------------------------> Positions
        self.AppendSeparator()
        for k in menuData['Pos']:
            self.rItems.append(self.Append(-1, k, kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.rItems[-1])
            rIDMap[self.rItems[-1].GetId()] = self.cVPos
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
    def OnLabel(self, event:wx.MenuEvent) -> bool:
        """Change between Experiments.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        #------------------------------> Set check mark to false
        [x.Check(check=False) for x in self.rItems]                             # pylint: disable=expression-not-assigned
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


class ToolHist(cMenu.BaseMenuFurtherAnalysis):
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
    #region -----------------------------------------------------> Class Setup
    cLUniqCleavage = 'Unique Cleavages'
    #------------------------------>
    cVWinUpdate = mConfig.core.kwWinUpdate
    cVNatKey    = 'nat'
    cVAllC      = 'allC'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddNatRecSeqEntry(
            self.OnMethodKeyBool, idMap=self.cVWinUpdate, idKey=self.cVNatKey)
        self.AppendSeparator()
        self.miUnique = self.Append(-1, self.cLUniqCleavage, kind=wx.ITEM_CHECK)
        self.miUnique.Check(check=False)
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        rIDMap = {
            self.miUnique.GetId(): self.cVWinUpdate,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miUnique.GetId() : self.cVAllC,
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
        win.UpdateResultWindow(nat=False, allC=False)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class ToolCpR(cMenu.BaseMenuFurtherAnalysis):
    """Tool menu for the Cleavage per Residue result window.

        Parameters
        ----------
        menuData: dict
            Dict with the data for the menu with the following two entries:
            {
                'Label': ['L1', 'L2',....],
                'Nat: bool,
            }

        Attributes
        ----------
        rItems: list
            List of wx.MenuItems
    """
    #region -----------------------------------------------------> Class Setup
    cLSingleSel  = 'Single Selection'
    cLNatProtLoc = 'Show Native Protein Location'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict):
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
            -1, f'{self.cLSingleSel}\tCtrl+S', kind=wx.ITEM_CHECK)
        self.miSel.Check(True)
        #------------------------------>
        if menuData['Nat']:
            self.miProtLoc = self.Append(
                -1, self.cLNatProtLoc, kind=wx.ITEM_CHECK)
            self.miProtLoc.Check(True)
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnLabel, source=self.miProtLoc)
        #------------------------------>
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnLabel(self, event:wx.CommandEvent) -> bool:
        """Change between Experiments.

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
        eventLabel = self.GetLabelText(event.GetId())
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        #------------------------------> Selection mode
        if sel and eventLabel not in [self.cLNatProt, self.cLNatProtLoc]:
            #------------------------------> Check mark set to false
            _ = [x.Check(False) for x in self.rItems]
            self.Check(event.GetId(), True)
        #------------------------------> Labels
        label = [x.GetItemLabel() for x in self.rItems if x.IsChecked()]
        if not label:
            self.rItems[0].Check()
            label = [self.rItems[0].GetItemLabel()]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = self.GetWindow()
        win.UpdateResultWindow(nat, label, show)
        #endregion ------------------------------------------------>

        return True
    #---

    def OnClear(self, event:wx.CommandEvent) -> bool:
        """Change between Experiments.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        #------------------------------>
        self.rItems[0].Check()
        #------------------------------> Uncheck all items
        _ = [x.Check(False) for x in self.rItems[1:]]
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
        win.UpdateResultWindow(False, [self.rItems[0].GetItemLabel()], True)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ToolCleavageEvol(cMenu.BaseMenuFurtherAnalysis):
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
    #region -----------------------------------------------------> Class Setup
    cLMon = 'Monotonic'
    #------------------------------>
    cVWinUpdate = mConfig.core.kwWinUpdate
    #------------------------------>
    cVMon = 'mon'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddNatRecSeqEntry(
            self.OnMethodKeyBool, idMap=self.cVWinUpdate, idKey='nat')
        self.AppendSeparator()
        self.miMon = self.Append(-1, self.cLMon, kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        rIDMap = {
            self.miMon.GetId() : self.cVWinUpdate,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miMon.GetId() : self.cVMon,
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
                Information about the event.

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
        win.UpdateResultWindow(nat=False, mon=False)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class ToolTarProt(cMenu.BaseMenuMainResult):
    """Tool menu for the Targeted Proteolysis window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu.
            {
                'MenuDate' : [List of dates as str],
                'FA' : {'Date': {'FA1': [], 'FA2':[]}, 'DateN':{},},
            }
    """
    #region -----------------------------------------------------> Class Setup
    cLFrag      = 'Fragments'
    cLIntensity = 'Intensities'
    cLFurtherA  = 'Further Analysis'
    cLClearSel  = 'Clear Selection'
    cLExportSeq = 'Export Sequences'
    #------------------------------>
    cVExportSeq = mConfig.core.kwExpSeq
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mFragmentMenu = cMenu.BaseMenuMainResultSubMenu('Shift')
        self.AppendSubMenu(self.mFragmentMenu, self.cLFrag)
        self.AppendSeparator()
        #------------------------------>
        self.mGelMenu = cMenu.BaseMenuMainResultSubMenu('Alt')
        self.AppendSubMenu(self.mGelMenu, self.cLIntensity)
        self.AppendSeparator()
        #------------------------------>
        self.mFurtherA = ToolFurtherAnalysis(
            self.cMenuData['FA'], self.rPlotDate[0].GetItemLabelText())
        self.AppendSubMenu(self.mFurtherA, self.cLFurtherA)
        self.AppendSeparator()
        #------------------------------>
        self.mClear = ToolClearSel()
        self.AppendSubMenu(self.mClear, self.cLClearSel)
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems(False)
        #------------------------------> Add Export Sequence
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveSeq = self.Insert(pos+2, -1, self.cLExportSeq)
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveSeq.GetId() : self.cVExportSeq,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSaveSeq)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnMethodKey(self, event:wx.MenuEvent) -> bool:
        """Call the corresponding method in the window with no arguments or
            keyword arguments.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

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
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class ToolFurtherAnalysis(cMenu.BaseMenu):
    """Further Analysis menu for the TarProt result window.

        Parameters
        ----------
        menuData: dict
            Information for menu items
            {
                'Date':{'FA1':['FA11', 'FA12',...],'FA2':['FA21', 'FA22',...],},
            }
    """
    #region -----------------------------------------------------> Class Setup
    cLAANew        = 'New AA Analysis'
    cLAADist       = 'AA Distribution'
    cLCleavageEvol = 'Cleavage Evolution'
    cLHistNew      = 'New Histogram'
    cLHistCleavage = 'Cleavage Histograms'
    cLCpR          = 'Cleavage per Residue'
    cLPDBMap       = 'PDB Mapping'
    #------------------------------>
    cVCEvol = mConfig.tarp.kwFACleavageEvol
    cVCpR   = mConfig.tarp.kwFACleavagePerRes
    cVPDB   = mConfig.tarp.kwFAPDBMap
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict, ciDate:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #------------------------------>
        self.mAA = cMenu.BaseMenuFurtherAnalysisEntry(
            menuData, ciDate, 'AA', self.cLAANew)
        self.AppendSubMenu(self.mAA, self.cLAADist)
        self.AppendSeparator()
        self.miCEvol = self.Append(-1, self.cLCleavageEvol)
        self.mHist   = cMenu.BaseMenuFurtherAnalysisEntry(
            menuData, ciDate, 'Hist', self.cLHistNew)
        self.AppendSubMenu(self.mHist, self.cLHistCleavage)
        self.miCpR = self.Append(-1, self.cLCpR)
        self.AppendSeparator()
        self.miPDB = self.Append(-1, self.cLPDBMap)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------->
        rIDMap = {
            self.miCEvol.GetId() : self.cVCEvol,
            self.miCpR.GetId()   : self.cVCpR,
            self.miPDB.GetId()   : self.cVPDB,
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
    def UpdateFurtherAnalysis(self, tDate:str, menuData:dict={}) -> bool:       # pylint: disable=dangerous-default-value
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
#endregion ----------------------------------------------------------> Classes

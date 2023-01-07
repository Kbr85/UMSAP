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
from typing  import Callable

import wx

import config.config as mConfig
import gui.window    as mWindow
import gui.method    as gMethod
#endregion ----------------------------------------------------------> Imports


#region ----------------------------------------------------> Individual menus
class MenuToolProtProfFCEvolution(BaseMenu):
    """Menu for a log2FC evolution along relevant points."""
    #region -----------------------------------------------------> Class Setup
    cLShowAll   = 'Show All'
    cLExpImg    = 'Export Image'
    cLZoomReset = 'Reset Zoom'
    #------------------------------>
    cVExpImg    = mConfig.kwToolExpImg
    cVZoomReset = mConfig.kwToolZoomReset
    cVFCShowAll = mConfig.kwToolFCShowAll
    #------------------------------>
    cVFC = 'FC'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miShowAll = self.Append(-1, self.cLShowAll, kind=wx.ITEM_CHECK)
        self.Check(self.miShowAll.GetId(), True)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\tAlt+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\tAlt+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveI.GetId()  : self.cVExpImg,
            self.miZoomR.GetId()  : self.cVZoomReset,
            self.miShowAll.GetId(): self.cVFCShowAll,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miSaveI.GetId()  : self.cVFC,
            self.miZoomR.GetId()  : self.cVFC,
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey,  source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolProtProfFilters(BaseMenu):
    """Menu for the ProtProfPlot Filters"""
    #region -----------------------------------------------------> Class Setup
    cLFCEvol    = 'FC Evolution'
    cLHypCurve  = 'Hyperbolic Curve'
    cLLog2FC    = 'Log2(FC)'
    cLPVal      = 'P Value'
    cLZScore    = 'Z Score'
    cLApplyAll  = 'Apply All'
    cLAutoApply = 'Auto Apply'
    cLRemove    = 'Remove'
    cLRemoveL   = 'Remove Last'
    cLRemoveA   = 'Remove All'
    cLCopy      = 'Copy'
    cLPaste     = 'Paste'
    cLSave      = 'Save'
    cLLoad      = 'Load'
    #------------------------------>
    cVFCEvol          = mConfig.lFilFCEvol
    cVHypCurve        = mConfig.lFilHypCurve
    cVFCLog           = mConfig.lFilFCLog
    cVPVal            = mConfig.lFilPVal
    cVZScore          = mConfig.lFilZScore
    cVApplyAll        = 'Apply All'
    cVRemL            = 'Remove Last'
    cVRemAny          = 'Remove Any'
    cVRemAll          = 'Remove All'
    cVCopy            = 'Copy'
    cVPaste           = 'Paste'
    cVSave            = 'Save Filter'
    cVLoad            = 'Load Filter'
    cVAutoApplyFilter = 'AutoApplyFilter'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miFcChange = self.Append(-1, self.cLFCEvol)
        self.miHypCurve = self.Append(-1, self.cLHypCurve)
        self.miLog2FC   = self.Append(-1, self.cLLog2FC)
        self.miPValue   = self.Append(-1, self.cLPVal)
        self.miZScore   = self.Append(-1, self.cLZScore)
        self.AppendSeparator()
        self.miApply = self.Append(-1, f'{self.cLApplyAll}\tCtrl+Shift+A')
        self.miUpdate = self.Append(
            -1, f'{self.cLAutoApply}\tCtrl-Shift+F', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miRemoveAny  = self.Append(-1, f'{self.cLRemove}\tCtrl+Shift+R')
        self.miRemoveLast = self.Append(-1, f'{self.cLRemoveL}\tCtrl+Shift+Z')
        self.miRemoveAll  = self.Append(-1, f'{self.cLRemoveA}\tCtrl+Shift+X')
        self.AppendSeparator()
        self.miCopy = self.Append(-1,  f'{self.cLCopy}\tCtrl+Shift+C')
        self.miPaste = self.Append(-1, f'{self.cLPaste}\tCtrl+Shift+V')
        self.AppendSeparator()
        self.miSave = self.Append(-1, f'{self.cLSave}\tCtrl+Shift+S')
        self.miLoad = self.Append(-1, f'{self.cLLoad}\tCtrl+Shift+L')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miFcChange.GetId()  : self.cVFCEvol,
            self.miHypCurve.GetId()  : self.cVHypCurve,
            self.miLog2FC.GetId()    : self.cVFCLog,
            self.miPValue.GetId()    : self.cVPVal,
            self.miZScore.GetId()    : self.cVZScore,
            self.miApply.GetId()     : self.cVApplyAll,
            self.miRemoveLast.GetId(): self.cVRemL,
            self.miRemoveAny.GetId() : self.cVRemAny,
            self.miRemoveAll.GetId() : self.cVRemAll,
            self.miCopy.GetId()      : self.cVCopy,
            self.miPaste.GetId()     : self.cVPaste,
            self.miSave.GetId()      : self.cVSave,
            self.miLoad.GetId()      : self.cVLoad,
            self.miUpdate.GetId()    : self.cVAutoApplyFilter,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miFcChange)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miLog2FC)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miPValue)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miApply)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveLast)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveAny)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveAll)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miCopy)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miPaste)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miSave)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miLoad)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miUpdate)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MenuToolProtProfLockPlotScale(BaseMenu):
    """Lock the plots scale to the selected option."""
    #region -----------------------------------------------------> Class Setup
    cLNo       = cVNo       = 'No'
    cLAnalysis = cVAnalysis = 'Analysis'
    cLProject  = cVProject  = 'Project'
    #------------------------------>
    cVMode     = 'mode'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNo      = self.Append(-1, self.cLNo,       kind=wx.ITEM_RADIO)
        self.miDate    = self.Append(-1, self.cLAnalysis, kind=wx.ITEM_RADIO)
        self.miProject = self.Append(-1, self.cLProject,  kind=wx.ITEM_RADIO)
        self.miDate.Check()
        #endregion -----------------------------------------------> Menu Items

        #region ------------------------------------------------------> nameID
        rIDMap = {
            self.miNo.GetId()     : self.cVNo,
            self.miDate.GetId()   : self.cVAnalysis,
            self.miProject.GetId(): self.cVProject,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miNo.GetId()     : self.cVMode,
            self.miDate.GetId()   : self.cVMode,
            self.miProject.GetId(): self.cVMode,
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


class MenuToolTarProtClearSel(BaseMenu):
    """Clear the selection in a TarProtRes Window."""
    #region -----------------------------------------------------> Class Setup
    cLPept    = cVPept    = 'Peptide'
    cLFrag    = cVFrag    = 'Fragment'
    cLAll     = cVAll     = 'All'
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


class MenuToolProtProfClearSel(BaseMenu):
    """Clear the selection in a ProtProf Res Window."""
    #region -----------------------------------------------------> Class Setup
    cLLabel = cVLabel = 'Labels'
    cLSel   = cVSel   = 'Selection'
    cLAll   = cVAll   = 'All'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miLabel = self.Append(-1, self.cLLabel)
        self.miSel   = self.Append(-1, self.cLSel)
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, f'{self.cLAll}\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        rIDMap = {
            self.miLabel.GetId(): self.cVLabel,
            self.miSel.GetId()  : self.cVSel,
            self.miNoSel.GetId(): self.cVAll,
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
    #region -----------------------------------------------------> Class Setup
    cVExp = mConfig.kwToolAAExp
    cVPos = mConfig.kwToolAAPos
    #endregion --------------------------------------------------> Class Setup

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
    def OnLabel(self, event: wx.CommandEvent) -> bool:
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
    #region -----------------------------------------------------> Class Setup
    cLUniqCleavage = 'Unique Cleavages'
    #------------------------------>
    cVWinUpdate = mConfig.kwToolWinUpdate
    cVNatKey    = 'nat'
    cVAllC      = 'allC'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData) -> None:
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
            -1, f'{self.cLSingleSel}\tCtrl+S', kind=wx.ITEM_CHECK)
        self.miSel.Check(True)
        #------------------------------>
        if menuData['Nat']:
            self.miProtLoc = self.Append(
                -1, self.cLNatProtLoc, kind=wx.ITEM_CHECK)
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
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        #------------------------------> Selection mode
        if sel and self.GetLabelText(event.GetId()) != mConfig.lmNatSeq:
            #------------------------------> Check mark set to false
            [x.Check(False) for x in self.rItems]                               # pylint: disable=expression-not-assigned
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
        win.UpdateResultWindow(nat, label, show)
        #endregion ------------------------------------------------>

        return True
    #---

    def OnClear(self, event: wx.CommandEvent) -> bool:
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
        [x.Check(False) for x in self.rItems[1:]]                               # pylint: disable=expression-not-assigned
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
    #region -----------------------------------------------------> Class Setup
    cLMon = 'Monotonic'
    #------------------------------>
    cVWinUpdate = mConfig.kwToolWinUpdate
    #------------------------------>
    cVMon = 'mon'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData):
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


class MenuToolProtProfVolcanoPlotColorScheme(BaseMenu):
    """Menu for Color Scheme in the Volcano Plot menu of ProtProf result window.
    """
    #region -----------------------------------------------------> Class Setup
    cLHypCurve = 'Hyperbolic Curve'
    cLPLog2FC  = 'P - Log2FC'
    cLZScore   = 'Z Score'
    cLConf     = 'Configure'
    #------------------------------>
    cVHypCurve = mConfig.kwToolVolPlotColorScheme
    cVPLog2FC  = mConfig.kwToolVolPlotColorScheme
    cVZScore   = mConfig.kwToolVolPlotColorScheme
    cVConf     = mConfig.kwToolVolPlotColorConf
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miHypCurve = self.Append(
            -1, self.cLHypCurve, kind=wx.ITEM_RADIO)
        self.miPLogFC   = self.Append(
            -1, self.cLPLog2FC, kind=wx.ITEM_RADIO)
        self.miZScore   = self.Append(
            -1, self.cLZScore, kind=wx.ITEM_RADIO)
        self.AppendSeparator()
        self.miConfigure= self.Append(-1, self.cLConf)
        #endregion -----------------------------------------------> Menu Items

        #region ------------------------------------------------------> rKeyID
        rIDMap = {
            self.miHypCurve.GetId() : self.cVHypCurve,
            self.miPLogFC.GetId  () : self.cVPLog2FC,
            self.miZScore.GetId  () : self.cVZScore,
            self.miConfigure.GetId(): self.cVConf,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ---------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miPLogFC)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miConfigure)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus
class MenuToolTarProt(BaseMenuMainResult):
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
    cVExportSeq = mConfig.kwToolExpSeq
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mFragmentMenu = BaseMenuMainResultSubMenu('Shift')
        self.AppendSubMenu(self.mFragmentMenu, self.cLFrag)
        self.AppendSeparator()
        #------------------------------>
        self.mGelMenu = BaseMenuMainResultSubMenu('Alt')
        self.AppendSubMenu(self.mGelMenu, self.cLIntensity)
        self.AppendSeparator()
        #------------------------------>
        self.mFurtherA = MenuToolTarProtFurtherAnalysis(
            self.cMenuData['FA'], self.rPlotDate[0].GetItemLabelText())
        self.AppendSubMenu(self.mFurtherA, self.cLFurtherA)
        self.AppendSeparator()
        #------------------------------>
        self.mClear = MenuToolTarProtClearSel()
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
    def OnMethodKey(self, event: wx.CommandEvent) -> bool:
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


class MenuToolProtProfVolcanoPlot(BaseMenu):
    """Menu for a Volcano Plot.

        Parameters
        ----------
        menuData: dict
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
    #region -----------------------------------------------------> Class Setup
    cLAddLabel    = 'Add Label'
    cLPickLabel   = 'Pick Label'
    cLColorScheme = 'Color Scheme'
    cLCorrP       = 'Corrected P Values'
    cLExpImg      = 'Export Image'
    cLZoomReset   = 'Reset Zoom'
    #------------------------------>
    cVWinUpdate = mConfig.kwToolWinUpdate
    cVLabelPick = mConfig.kwToolVolPlotLabelPick
    cVLabelProt = mConfig.kwToolVolPlotLabelProt
    cVPCorr     = mConfig.kwToolWinUpdate
    cVExpImg    = mConfig.kwToolExpImg
    cVZoomReset = mConfig.kwToolZoomReset
    #------------------------------>
    cVPCorrKey = 'corrP'
    cVMenuKey  = 'Vol'
    cVCond     = 'cond'
    cVRP       = 'rp'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict, ciDate: str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCrp = menuData
        #------------------------------> Cond - RP separator. To remove/create.
        self.rSep = None
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.rCond, self.rRp = self.SetCondRPMenuItems(ciDate)
        self.AppendSeparator()
        self.miLabelProt = self.Append(-1, f'{self.cLAddLabel}\tShift+A')
        self.miLabelPick = self.Append(
            -1, f'{self.cLPickLabel}\tShift+P', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.mColor = MenuToolProtProfVolcanoPlotColorScheme()
        self.AppendSubMenu(self.mColor, self.cLColorScheme)
        self.AppendSeparator()
        self.miPCorr = self.Append(-1, self.cLCorrP, kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\tShift+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\tShift+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miLabelPick.GetId(): self.cVLabelPick,
            self.miLabelProt.GetId(): self.cVLabelProt,
            self.miPCorr.GetId    (): self.cVPCorr,
            self.miSaveI.GetId    (): self.cVExpImg,
            self.miZoomR.GetId    (): self.cVZoomReset,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miPCorr.GetId() : self.cVPCorrKey,
            self.miSaveI.GetId() : self.cVMenuKey,
            self.miZoomR.GetId() : self.cVMenuKey,
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,         source=self.miLabelProt)
        self.Bind(wx.EVT_MENU, self.OnMethod,         source=self.miLabelPick)
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool,  source=self.miPCorr)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage methods
    def SetCondRPMenuItems(
        self,
        tDate: str,
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
        k = 0
        for c in self.rCrp[tDate]['C']:
            #------------------------------>
            cond.append(self.Insert(k, -1, item=c, kind=wx.ITEM_RADIO))
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=cond[-1])
            #------------------------------>
            self.rIDMap[cond[-1].GetId()]  = self.cVWinUpdate
            self.rKeyMap[cond[-1].GetId()] = self.cVCond
            #------------------------------>
            k = k + 1
        #------------------------------>
        self.rSep = self.Insert(k, -1, kind=wx.ITEM_SEPARATOR)
        k = k + 1
        #------------------------------> Relevant Points
        for t in self.rCrp[tDate]['RP']:
            #------------------------------>
            rp.append(self.Insert(k, -1, item=t, kind=wx.ITEM_RADIO))
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=rp[-1])
            #------------------------------>
            self.rIDMap[rp[-1].GetId()]  = self.cVWinUpdate
            self.rKeyMap[rp[-1].GetId()] = self.cVRP
            #------------------------------>
            k = k + 1
        #endregion ---------------------------------------------> Add elements

        return (cond, rp)
    #---

    def UpdateCondRP(self, tDate: str, menuData: dict={}) -> bool:              # pylint: disable=dangerous-default-value
        """Update the conditions and relevant points when date changes.

            Parameters
            ----------
            tDate : str
                Selected date
            menuData: dict
                Information for the menu item.

            Returns
            -------
            bool

            Notes
            -----
            Date changes in ProtProfToolMenu
        """
        #region --------------------------------------------------->
        self.rCrp = menuData if menuData else self.rCrp
        #endregion ------------------------------------------------>

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


class MenuToolTarProtFurtherAnalysis(BaseMenu):
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
    cVCEvol = mConfig.kwToolFACleavageEvol
    cVCpR   = mConfig.kwToolFACleavagePerRes
    cVPDB   = mConfig.kwToolFAPDBMap
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict, ciDate:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #------------------------------>
        self.mAA = BaseMenuFurtherAnalysisEntry(
            menuData, ciDate, 'AA', self.cLAANew)
        self.AppendSubMenu(self.mAA, self.cLAADist)
        self.AppendSeparator()
        self.miCEvol = self.Append(-1, self.cLCleavageEvol)
        self.mHist   = BaseMenuFurtherAnalysisEntry(
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
    def UpdateFurtherAnalysis(self, tDate: str, menuData: dict={}) -> bool:     # pylint: disable=dangerous-default-value
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


class MenuToolProtProf(BaseMenuMainResult):
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
    #region -----------------------------------------------------> Class Setup
    cLVol           = 'Volcano Plot'
    cLFC            = 'FC Evolution'
    cLFilter        = 'Filters'
    cLLock          = 'Lock Plot Scale'
    cLCLear         = 'Clear Selection'
    cLExpDataFilter = 'Export Filtered Data'
    #------------------------------>
    cVExpDataFilter = mConfig.kwToolExportDataFiltered
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mVolcano =  MenuToolProtProfVolcanoPlot(
                self.cMenuData['crp'], self.rPlotDate[0].GetItemLabelText()
        )
        self.AppendSubMenu(self.mVolcano, self.cLVol)
        self.AppendSeparator()
        #------------------------------> Relevant Points
        self.mFc = MenuToolProtProfFCEvolution()
        self.AppendSubMenu(self.mFc, self.cLFC)
        self.AppendSeparator()
        #------------------------------> Filter
        self.mFilter = MenuToolProtProfFilters()
        self.AppendSubMenu(self.mFilter, self.cLFilter)
        self.AppendSeparator()
        #------------------------------> Lock scale
        self.mLockScale = MenuToolProtProfLockPlotScale()
        self.AppendSubMenu(self.mLockScale, self.cLLock)
        self.AppendSeparator()
        #------------------------------> Clear Selection
        self.mClearSel = MenuToolProtProfClearSel()
        self.AppendSubMenu(self.mClearSel, self.cLCLear)
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems(False)
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveDataFiltered = self.Insert(
            pos+1, -1, f'{self.cLExpDataFilter}\tShift+Ctrl+E')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveDataFiltered.GetId() : self.cVExpDataFilter,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region ---------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSaveDataFiltered)
        #endregion ------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnMethodKey(self, event: wx.CommandEvent):
        """Call the corresponding method in the window.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

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
            win.UpdateResultWindow(
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
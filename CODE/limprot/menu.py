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


"""Menu for the limprot module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolLimProtClearSel(cMenu.BaseMenu):
    """Clear the selection in a LimProt Result Window."""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Label
    cLPept    = mConfig.limp.lmClearPeptide
    cLFrag    = mConfig.limp.lmClearFragment
    cLGelSpot = mConfig.limp.lmClearGelSpot
    cLBL      = mConfig.limp.lmClearBandLane
    cLAll     = mConfig.limp.lmClearAll
    #------------------------------> Values
    cVPept    = mConfig.limp.kwClearPeptide
    cVFrag    = mConfig.limp.kwClearFragment
    cVGelSpot = mConfig.limp.kwClearGelSpot
    cVBL      = mConfig.limp.kwClearBandLane
    cVAll     = mConfig.limp.kwClearAll
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
        self.miNoGel  = self.Append(-1, self.cLGelSpot)
        self.miNoBL   = self.Append(-1, self.cLBL)
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, f'{self.cLAll}\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        self.rIDMap = {
            self.miNoPept.GetId(): self.cVPept,
            self.miNoFrag.GetId(): self.cVFrag,
            self.miNoGel.GetId() : self.cVGelSpot,
            self.miNoBL.GetId()  : self.cVBL,
            self.miNoSel.GetId() : self.cVAll,
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


class ToolLimProt(cMenu.BaseMenuMainResult):
    """Tool menu for the Limited Proteolysis window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu.
            {'MenuDate' : [List of dates as str],}
    """
    #region ------------------------------------------------------> Class Setup
    cLLaneSel   = mConfig.limp.lmToolLaneSel
    cLShowAll   = mConfig.limp.lmToolShowAll
    cLFrag      = mConfig.limp.lmToolFrag
    cLGel       = mConfig.limp.lmToolGel
    cLClearSel  = mConfig.limp.lmToolClearSel
    cLExportSeq = mConfig.limp.lmToolExportSeq
    #------------------------------>
    cVBandLane  = mConfig.limp.kwBandLane
    cVShowAll   = mConfig.limp.kwShowAll
    cVExportSeq = mConfig.core.kwExpSeq
    #endregion ---------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData: dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miBandLane = self.Append(
            -1, f'{self.cLLaneSel}\tCtrl+L', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        #------------------------------>
        self.miShowAll = self.Append(-1, f'{self.cLShowAll}\tCtrl+A')
        self.AppendSeparator()
        #------------------------------>
        self.mFragmentMenu = cMenu.BaseMenuMainResultSubMenu('Shift')
        self.AppendSubMenu(self.mFragmentMenu, self.cLFrag)
        self.AppendSeparator()
        #------------------------------>
        self.mGelMenu = cMenu.BaseMenuMainResultSubMenu('Alt')
        self.AppendSubMenu(self.mGelMenu, self.cLGel)
        self.AppendSeparator()
        #------------------------------>
        self.mClearMenu = ToolLimProtClearSel()
        self.AppendSubMenu(self.mClearMenu, self.cLClearSel)
        self.AppendSeparator()
        #------------------------------> Last Items
        self.AddLastItems(False)
        #------------------------------> Add Export Sequence
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveSeq = self.Insert(pos+2, -1, self.cLExportSeq)
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miBandLane.GetId(): self.cVBandLane ,
            self.miShowAll.GetId() : self.cVShowAll  ,
            self.miSaveSeq.GetId() : self.cVExportSeq,
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
#endregion ----------------------------------------------------------> Classes

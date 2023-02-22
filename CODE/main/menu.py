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
from core     import menu   as cMenu
from corr     import menu   as corrMenu
from dataprep import menu   as dataMenu
from help     import menu   as hMenu
from limprot  import menu   as limpMenu
from main     import window as mWindow
from protprof import menu   as protMenu
from result   import menu   as resMenu
from result   import method as resMethod
from tarprot  import menu   as tarpMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
#region ----------------------------------------------------------------> Menu
class MenuModule(cMenu.BaseMenu):
    """Menu with module entries."""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Labels
    cLLimProt  = mConfig.limp.nMod
    cLProtProf = mConfig.prot.nMod
    cLTarProt  = mConfig.tarp.nMod
    #------------------------------> Key - Values
    cVLimProt  = mConfig.limp.nTab
    cVProtProf = mConfig.prot.nTab
    cVTarProt  = mConfig.tarp.nTab
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

    #region ---------------------------------------------------> Class Methods
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
        #endregion ----------------------------------------------> Check MainW

        #region --------------------------------------------------> Create Tab
        mConfig.main.mainWin.CreateTab(self.rIDMap[event.GetId()])
        #endregion -----------------------------------------------> Create Tab

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class MenuUtility(cMenu.BaseMenu):
    """Menu with the utilities entries."""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Labels
    cLCorrA    = mConfig.corr.nUtil
    cLDataPrep = mConfig.data.nUtil
    cLReadF    = mConfig.res.nUtil
    #------------------------------> Key - Values
    cVCorrA    = mConfig.corr.nTab
    cVDataPrep = mConfig.data.nTab
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
        #endregion ----------------------------------------------> Check MainW

        #region --------------------------------------------------> Create Tab
        mConfig.main.mainWin.CreateTab(self.rIDMap[event.GetId()])
        #endregion -----------------------------------------------> Create Tab

        return True
    #---

    def OnReadFile(self, event:wx.CommandEvent) -> bool:                        # pylint: disable=unused-argument
        """Read an UMSAP output file.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Load file
        resMethod.LoadUMSAPFile()
        #endregion ------------------------------------------------> Load file

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
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
        self.mHelp    = hMenu.MenuHelp()
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
        mConfig.res.nwUMSAPControl: resMenu.ToolUmsapControl,
        mConfig.corr.nwRes        : corrMenu.ToolCorrA,
        mConfig.data.nwRes        : dataMenu.ToolDataPrep,
        mConfig.limp.nwRes        : limpMenu.ToolLimProt,
        mConfig.tarp.nwRes        : tarpMenu.ToolTarProt,
        mConfig.tarp.nwAAPlot     : tarpMenu.ToolAA,
        mConfig.tarp.nwHistPlot   : tarpMenu.ToolHist,
        mConfig.tarp.nwCpRPlot    : tarpMenu.ToolCpR,
        mConfig.tarp.nwCEvolPlot  : tarpMenu.ToolCleavageEvol,
        mConfig.prot.nwRes        : protMenu.ToolProtProf,
    }
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------- Instance Setup
    def __init__(self, cName:str, menuData:dict={}) -> None:                    # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------> Menu items & Append
        if cName in self.dTool:
            self.mTool = self.dTool[cName](menuData)
            #------------------------------>
            self.Insert(
                mConfig.core.toolMenuIdx,
                self.mTool,
                f'&{mConfig.core.lmTools}'
            )
        #endregion --------------------------------------> Menu items & Append
    #---
    #endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> MenuBar
#endregion ----------------------------------------------------------> Classes

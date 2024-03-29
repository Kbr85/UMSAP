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


"""Windows for the main module of the app"""


#region -------------------------------------------------------------> Imports
import _thread
from typing import Optional

import wx
from wx.lib.agw import aui

from config.config import config as mConfig
from core     import method as cMethod
from core     import window as cWindow
from corr     import tab    as corrTab
from dataprep import tab    as dataTab
from help     import method as hMethod
from limprot  import tab    as limpTab
from main     import menu   as mMenu
from main     import method as mMethod
from main     import tab    as mTab
from protprof import tab    as protTab
from tarprot  import tab    as tarpTab
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class WindowMain(cWindow.BaseWindow):
    """Creates the main window of the App.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the main window.

        Attributes
        ----------
        dTab: dict
            Methods to create the tabs.
    """
    #region -----------------------------------------------------> Class Setup
    cName  = mConfig.main.nwMain
    cTitle = mConfig.main.twMain
    #------------------------------>
    dTab = {
        mConfig.corr.nTab    : corrTab.CorrA,
        mConfig.data.nTab    : dataTab.DataPrep,
        mConfig.limp.nTab    : limpTab.LimProt,
        mConfig.main.ntStart : mTab.Start,
        mConfig.prot.nTab    : protTab.ProtProf,
        mConfig.tarp.nTab    : tarpTab.TarProt,
    }
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:Optional[wx.Window]=None) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent=parent)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> StatusBar fields
        self.wStatBar.SetStatusText(
            f"{mConfig.core.softwareF} {mConfig.core.version}", 0)
        #------------------------------> Notebook
        self.wNotebook = aui.auibook.AuiNotebook(                               # type: ignore
            self,
            agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer.Add(self.wNotebook, 1, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region --------------------------------------------> Create Start Tab
        self.CreateTab(mConfig.main.ntStart)
        self.wNotebook.SetCloseButton(0, False)
        #endregion -----------------------------------------> Create Start Tab

        #region ---------------------------------------------> Position & Show
        self.Center()
        self.Show()
        #endregion ------------------------------------------> Position & Show

        #region --------------------------------------------------------> Bind
        self.wNotebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
        #endregion -----------------------------------------------------> Bind

        #region	------------------------------------------------------> Update
        if mConfig.core.checkUpdate:
            _thread.start_new_thread(hMethod.UpdateCheck, ("main", self))
        #endregion ---------------------------------------------------> Update

        #region -------------------------------------> User Configuration File
        if not mConfig.core.confUserFile:
            _thread.start_new_thread(
                mMethod.BadUserConfFile, (mConfig.core.confUserFileException,))
        if mConfig.core.confUserWrongOptions:
            _thread.start_new_thread(
                mMethod.BadUserConfOptions, (mConfig.core.confUserWrongOptions,))
        #endregion ----------------------------------> User Configuration File
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnTabClose(self, event:wx.Event) -> bool:
        """Make sure to show the Start Tab if no other tab exists.

            Parameters
            ----------
            event: wx.aui.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        event.Skip()
        #------------------------------>
        return cMethod.OnGUIMethod(self.TabClose)
        #endregion ------------------------------------------------>
    #---

    def OnCreateTab(
        self,
        name:str,
        dataI:Optional[cMethod.BaseUserData]=None,) -> bool:
        """Create the Tabs from the button in Start.

            Parameters
            ----------
            name: str
                One of the values in section Names of config for tabs
            dataI: cMethod.BaseUserData or None
                Data class representation of user input. Default is None.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        return cMethod.OnGUIMethod(self.CreateTab, name, dataI=dataI)
        #endregion ------------------------------------------------>
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def CreateTab(
        self,
        name:str,
        dataI:Optional[cMethod.BaseUserData]=None,
        ) -> bool:
        """Create a tab.

            Parameters
            ----------
            name: str
                One of the values in section Names of config for tabs
            dataI: cMethod.BaseUserData or None
                Data class representation of user input. Default is None.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Get tab
        win = self.FindWindowByName(name)
        #endregion --------------------------------------------------> Get tab

        #region ------------------------------------------> Find/Create & Show
        if win is None:
            #------------------------------> Create tab
            tab = self.dTab[name](self.wNotebook)
            #------------------------------> Initial Data
            if name != mConfig.main.ntStart:
                tab.wConf.SetInitialData(dataI)                                 # Tab needs to be fully created before adding initial data
            #------------------------------> Add
            self.wNotebook.AddPage(tab, tab.tTitle, select=True)
        else:
            #------------------------------> Focus
            self.wNotebook.SetSelection(self.wNotebook.GetPageIndex(win))
            #------------------------------> Initial Data
            win.wConf.SetInitialData(dataI)
        #endregion ---------------------------------------> Find/Create & Show

        #region ---------------------------------------------------> Start Tab
        if self.wNotebook.GetPageCount() > 1:
            winS = self.FindWindowByName(mConfig.main.ntStart)
            if winS is not None:
                self.wNotebook.SetCloseButton(
                    self.wNotebook.GetPageIndex(winS),
                    True,
                )
        #endregion ------------------------------------------------> Start Tab

        #region -------------------------------------------------------> Raise
        self.Raise()
        #endregion ----------------------------------------------------> Raise

        return True
    #---

    def TabClose(self) -> bool:
        """Make sure to show the Start Tab if no other tab exists.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        pageC = self.wNotebook.GetPageCount() - 1
        #------------------------------> Update tabs & close buttons
        if pageC == 1:
            #-----------------------------> Remove close button from Start tab
            if (win := self.FindWindowByName(mConfig.main.ntStart)) is not None:
                self.wNotebook.SetCloseButton(
                    self.wNotebook.GetPageIndex(win),
                    False,
                )
        elif pageC == 0:
            #------------------------------> Show Start Tab with close button
            self.CreateTab(mConfig.main.ntStart)
            self.wNotebook.SetCloseButton(
                self.wNotebook.GetPageIndex(
                    self.FindWindowByName(mConfig.main.ntStart)),
                False,
            )
        #endregion ------------------------------------------------>

        return True
    #---

    def Close(self) -> bool:
        """Destroy window and set config.winMain to None.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.Destroy()
        #------------------------------>
        mConfig.main.mainWin = None
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes

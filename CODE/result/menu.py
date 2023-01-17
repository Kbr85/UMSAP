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


"""Menu for the result module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolUmsapControl(cMenu.BaseMenu):
    """Tool menu for the UMSAP file control window"""
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Label
    cLAdd    = mConfig.res.lmToolAdd
    cLDel    = mConfig.res.lmToolDel
    cLExp    = mConfig.res.lmToolExp
    cLUpdate = mConfig.res.lmToolReload
    #------------------------------> Values
    cVAddDelExp = mConfig.res.kwToolAddDelExp
    cVUpdate    = mConfig.res.kwToolReload
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, *args, **kwargs) -> None:                                # pylint: disable=unused-argument
        """*args and **kwargs are needed to use this menu with ToolMenuBar.
            All of them are ignored here.
        """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miAddData = self.Append(-1, f'{self.cLAdd}\tCtrl+A')
        self.AppendSeparator()
        self.miDelData = self.Append(-1, f'{self.cLDel}\tCtrl+X')
        self.AppendSeparator()
        self.miExpData = self.Append(-1, f'{self.cLExp}\tCtrl+E')
        self.AppendSeparator()
        self.miUpdateFile = self.Append(-1, f'{self.cLUpdate}\tCtrl+U')
        #endregion -----------------------------------------------> Menu Items

        #region -------------------------------------------------------> Links
        self.rIDMap = {
            self.miAddData.GetId()   : self.cVAddDelExp,
            self.miDelData.GetId()   : self.cVAddDelExp,
            self.miExpData.GetId()   : self.cVAddDelExp,
            self.miUpdateFile.GetId(): self.cVUpdate,
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
#endregion ----------------------------------------------------------> Classes

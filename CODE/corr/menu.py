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


"""Menu for the corr module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolCorrA(cMenu.BaseMenuMainResult):
    """Creates the Tools menu for a Correlation Analysis Plot window.

        Parameters
        ----------
        menuData: dict
            Data to build the Tool menu. See Notes for more details.

        Notes
        -----
        menuData has the following structure:
        {
            'MenuDate' : ['dateA',....,'dateN'],
        }
    """
    #region -----------------------------------------------------> Class Setup
    cLAllCol   = mConfig.corr.lmAllCol
    cLSelCol   = mConfig.corr.lmSelCol
    cLColName  = 'Column Names'
    cLColorBar = 'Show ColorBar'
    #------------------------------>
    cVWinUpdate = mConfig.core.kwWinUpdate
    cVCorrACol  = mConfig.corr.kwCol
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance Setup
    def __init__(self, menuData:dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miColName = self.Append(-1, self.cLColName, kind=wx.ITEM_CHECK)
        self.miColName.Check(check=True)
        #------------------------------>
        self.AppendSeparator()
        self.miAllCol = self.Append(-1, self.cLAllCol)
        self.miSelCol = self.Append(-1, self.cLSelCol)
        #------------------------------>
        self.AppendSeparator()
        self.miColBar = self.Append(-1, self.cLColorBar, kind=wx.ITEM_CHECK)
        self.miColBar.Check(check=False)
        #------------------------------>
        self.AppendSeparator()
        self.AddLastItems()
        #endregion -----------------------------------------------> Menu Items

        #region -------------------------------------------------------> Names
        rIDMap = {
            self.miColName.GetId(): self.cVWinUpdate,
            self.miColBar.GetId() : self.cVWinUpdate,
            self.miSelCol.GetId() : self.cVCorrACol,
            self.miAllCol.GetId() : self.cVCorrACol,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miColName.GetId(): 'col',
            self.miColBar.GetId() : 'bar',
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ----------------------------------------------------> Names

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miColName)
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool, source=self.miColBar)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel,   source=self.miSelCol)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel,   source=self.miAllCol)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance Setup
#---
#endregion ----------------------------------------------------------> Classes

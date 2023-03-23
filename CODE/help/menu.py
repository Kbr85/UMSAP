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


"""Menu methods and classes for the help module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu   as cMenu
#endregion ----------------------------------------------------------> Imports


#region ----------------------------------------------------------------> Menu
class MenuHelp(cMenu.BaseMenu):
    """Menu with the help entries."""
    #region ---------------------------------------------------> Class Setup
    #------------------------------> Label
    cLAbout       = 'About UMSAP'
    cLCheckUpdate = 'Check for Updates'
    cLManual      = 'Manual'
    cLPreference  = 'Preferences'
    cLTutorial    = 'Tutorial'
    #------------------------------> Values
    cVAbout    = mConfig.help.kwPubAbout
    cVManual   = mConfig.help.kwPubManual
    cVTutorial = mConfig.help.kwPubTutorial
    cVCheckUp  = mConfig.help.kwPubCheckUp
    cVPref     = mConfig.help.kwPubPreference
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

        #region -------------------------------------------------------> Dicts
        rPubSub = {
            self.miAbout.GetId()   : self.cVAbout,
            self.miManual.GetId()  : self.cVManual,
            self.miTutorial.GetId(): self.cVTutorial,
            self.miCheckUpd.GetId(): self.cVCheckUp,
            self.miPref.GetId()    : self.cVPref,
        }
        self.rPubSub = self.rPubSub | rPubSub
        #endregion ----------------------------------------------------> Dicts

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnPubSub, source=self.miAbout)
        self.Bind(wx.EVT_MENU, self.OnPubSub, source=self.miManual)
        self.Bind(wx.EVT_MENU, self.OnPubSub, source=self.miTutorial)
        self.Bind(wx.EVT_MENU, self.OnPubSub, source=self.miCheckUpd)
        self.Bind(wx.EVT_MENU, self.OnPubSub, source=self.miPref)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion -------------------------------------------------------------> Menu

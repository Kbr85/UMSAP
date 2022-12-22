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


"""Panes for the help module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class PanePrefUpdate(wx.Panel):
    """Panel for the Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npPrefUpdate
    #------------------------------>
    cLTab = mConfig.help.ntPrefUpdate
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wRBox = wx.RadioBox(
            self,
            label   = 'Check for Updates',
            choices = ['Always', 'Never'],
         )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.sSizer.Add(self.wRBox, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

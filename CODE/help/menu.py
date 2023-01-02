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
import _thread
import os
import webbrowser

import wx

from config.config import config as mConfig
from core import menu   as cMenu
from core import window as cWindow
from help import method as hMethod
from help import window as hWindow
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

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnAbout,       source=self.miAbout)
        self.Bind(wx.EVT_MENU, self.OnManual,      source=self.miManual)
        self.Bind(wx.EVT_MENU, self.OnTutorial,    source=self.miTutorial)
        self.Bind(wx.EVT_MENU, self.OnCheckUpdate, source=self.miCheckUpd)
        self.Bind(wx.EVT_MENU, self.OnPreference,  source=self.miPref)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ----------------------------------------------------> Class Method
    def OnAbout(self, event:wx.MenuEvent) -> bool:                              # pylint: disable=unused-argument
        """Show the About UMSAP window.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        win = self.GetWindow()
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        try:
            hWindow.WindowAbout()
        except Exception as e:
            msg = 'Failed to show the About UMSAP window.'
            cWindow.Notification('errorU', msg=msg, tException=e, parent=win)
            return False
        #endregion ------------------------------------------------>

        return True
    #---

    def OnManual(self, event:wx.MenuEvent) -> bool:                             # pylint: disable=unused-argument
        """Show the About UMSAP window.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        win = self.GetWindow()
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        try:
            os.system(f'{mConfig.core.commOpen} {mConfig.core.fManual}')
        except Exception as e:
            msg = 'Failed to open the manual of UMSAP.'
            cWindow.Notification('errorU', msg=msg, tException=e, parent=win)
            return False
        #endregion ----------------------------------------------------->

        return True
    #---

    def OnTutorial(self, event:wx.MenuEvent) -> bool:                           # pylint: disable=unused-argument
        """Show the tutorial.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        win = self.GetWindow()
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        try:
            webbrowser.open_new(f'{mConfig.core.urlTutorial}/start')
        except Exception as e:
            msg = 'Failed to open the url with the tutorials for UMSAP.'
            cWindow.Notification('errorU', msg=msg, tException=e, parent=win)
            return False
        #endregion ------------------------------------------------>

        return True
    #---

    def OnCheckUpdate(self, event:wx.MenuEvent) -> bool:                        # pylint: disable=unused-argument
        """Check for updates.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

            Returns
            -------
            bool
        """
        _thread.start_new_thread(hMethod.UpdateCheck, ('menu',))
        return True
    #---

    def OnPreference(self, event:wx.MenuEvent) -> bool:                         # pylint: disable=unused-argument
        """Set UMSAP preferences.

            Parameters
            ----------
            event: wx.MenuEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        win = self.GetWindow()
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        try:
            hWindow.Preference()
        except Exception as e:
            msg = 'Failed to show the Preferences window.'
            cWindow.Notification('errorU', msg=msg, tException=e, parent=win)
            return False
        #endregion ----------------------------------------------------->

        return True
    #---
    #endregion -------------------------------------------------> Class Method
#---
#endregion -------------------------------------------------------------> Menu

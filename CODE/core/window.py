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


"""Bases Windows for the app"""


#region -------------------------------------------------------------> Imports
from typing import Optional

import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default None
        menuData : dict
            Data to build the Tool menu of the window. See structure in child
            class.

        Attributes
        ----------
        dKeyMethod : dict
            Keys are str and values classes or methods. Link menu items to
            windows methods.
    """
    #region -----------------------------------------------------> Class setup
    cSDeltaWin = mConfig.core.deltaWin
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent  : Optional[wx.Window]=None,
        menuData: dict={},
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------> Def values if not given in child class
        self.cName    = getattr(self, 'cName',    mConfig.core.nwDef)
        self.cSWindow = getattr(self, 'cSWindow', mConfig.core.sWinFull)
        self.cTitle   = getattr(self, 'cTitle',   self.cName)
        #------------------------------>
        self.dKeyMethod = {
            #------------------------------> Help Menu
            # mConfig.kwHelpAbout   : self.UMSAPAbout,
            # mConfig.kwHelpManual  : self.UMSAPManual,
            # mConfig.kwHelpTutorial: self.UMSAPTutorial,
            # mConfig.kwHelpCheckUpd: self.CheckUpdate,
            # mConfig.kwHelpPref    : self.Preference,
        }
        #------------------------------>
        super().__init__(
            parent, size=self.cSWindow, title=self.cTitle, name=self.cName,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wStatBar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Menu
        self.mBar = cMenu.MenuBarTool(self.cName, menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        # self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    # def UMSAPAbout(self) -> bool:
    #     """Show the About UMSAP window.

    #         Returns
    #         -------
    #         bool
    #     """
    #     try:
    #         WindowAbout()
    #         return True
    #     except Exception as e:
    #         msg = 'Failed to show the About UMSAP window.'
    #         DialogNotification('errorU', msg=msg, tException=e, parent=self)
    #         return False
    # #---

    # def UMSAPManual(self) -> bool:
    #     """Show the Manual of UMSAP.

    #         Returns
    #         -------
    #         bool
    #     """
    #     try:
    #         os.system(f'{mConfig.commOpen} {mConfig.fManual}')
    #         return True
    #     except Exception as e:
    #         msg = 'Failed to open the manual of UMSAP.'
    #         DialogNotification('errorU', msg=msg, tException=e, parent=self)
    #         return False
    # #---

    # def UMSAPTutorial(self) -> bool:
    #     """Show the tutorial for UMSAP.

    #         Returns
    #         -------
    #         bool
    #     """
    #     try:
    #         webbrowser.open_new(f'{mConfig.urlTutorial}/start')
    #         return True
    #     except Exception as e:
    #         msg = 'Failed to open the url with the tutorials for UMSAP.'
    #         DialogNotification('errorU', msg=msg, tException=e, parent=self)
    #         return False
    # #---

    # def CheckUpdate(self) -> bool:
    #     """Check for updates.

    #         Returns
    #         -------
    #         bool
    #     """
    #     _thread.start_new_thread(UpdateCheck, ('menu',))
    #     return True
    # #---

    # def Preference(self) -> bool:
    #     """Set UMSAP preferences.

    #         Returns
    #         -------
    #         bool
    #     """
    #     try:
    #         DialogPreference()
    #         return True
    #     except Exception as e:
    #         msg = 'Failed to show the Preferences window.'
    #         DialogNotification('errorU', msg=msg, tException=e, parent=self)
    #         return False
    # #---
    #endregion ------------------------------------------------> Class Methods

    #region ---------------------------------------------------> Event Methods
    # def OnClose(self, event: wx.CloseEvent) -> bool:                            # pylint: disable=unused-argument
    #     """Destroy window. Override as needed.

    #         Parameters
    #         ----------
    #         event: wx.CloseEvent
    #             Information about the event.

    #         Returns
    #         -------
    #         bool
    #     """
    #     #region -------------------------------------------> Reduce win number
    #     try:
    #         mConfig.winNumber[self.cName] -= 1
    #     except Exception:
    #         pass
    #     #endregion ----------------------------------------> Reduce win number

    #     #region -----------------------------------------------------> Destroy
    #     self.Destroy()
    #     #endregion --------------------------------------------------> Destroy

    #     return True
    # #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Manage Methods
    # def WinPos(self) -> dict:
    #     """Adjust win number and return information about the size of the
    #         window.

    #         Return
    #         ------
    #         dict
    #             Information about the size of the window and display and number
    #             of windows. See also data.method.GetDisplayInfo

    #         Notes
    #         -----
    #         Final position of the window on the display must be set in child
    #         class.
    #     """
    #     #region ---------------------------------------------------> Variables
    #     info = gMethod.GetDisplayInfo(self)
    #     #endregion ------------------------------------------------> Variables

    #     #region ----------------------------------------------------> Update N
    #     mConfig.winNumber[self.cName] = info['W']['N'] + 1
    #     #endregion -------------------------------------------------> Update N

    #     return info
    # #---
    #endregion ------------------------------------------------> Manage Methods
#---
#endregion ----------------------------------------------------------> Classes

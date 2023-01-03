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


"""This module contains the wx.App instance starting the application."""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path

import wx
import wx.adv
#endregion ----------------------------------------------------------> Imports


DEVELOPMENT = True                                                              # Development (True) or Production (False)


#region -------------------------------------------------------------> Classes
class UmsapApp(wx.App):
    """Start the UMSAP app."""
    #region ----------------------------------------------> Overridden methods
    def OnInit(self) -> bool:
        """Initialize the app.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        os = platform.system()
        #------------------------------> image_loc
        imgPath = '/RESOURCES/IMAGES/SPLASHSCREEN/splash.png'
        if os == 'Darwin':
            fileRoot = Path(__file__).parent.parent
        elif os == 'Windows':
            fileRoot = Path(__file__).parent
        else:
            fileRoot = Path(__file__).parent
        imgFullPath = f'{fileRoot}{imgPath}'
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Development
        if DEVELOPMENT:
            imgPath     = '/Resources/IMAGES/SPLASHSCREEN/splash.png'
            fileRoot    = Path(__file__).parent.parent
            imgFullPath = f'{fileRoot}{imgPath}'
        #endregion ----------------------------------------------> Development

        #region ------------------------------------------------> SplashScreen
        SplashWindow(str(imgFullPath))
        #endregion ---------------------------------------------> SplashScreen

        return True
    #---
    #endregion -------------------------------------------> Overridden methods
#---


class SplashWindow(wx.adv.SplashScreen):
    """Create the Splash Screen.

        Parameters
        ----------
        imgPath: str
            Path to the image used in the splash window.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, imgPath:str) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(
            wx.Bitmap(imgPath, type=wx.BITMAP_TYPE_PNG),
            wx.adv.SPLASH_CENTER_ON_SCREEN|wx.adv.SPLASH_TIMEOUT,
            1500,
            None,
        )
        #endregion --------------------------------------------> Initial setup

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind

        #region --------------------------------------------------------> Show
        self.Show()
        #endregion -----------------------------------------------------> Show
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnClose(self, event:wx.CloseEvent) -> bool:                             # pylint: disable=unused-argument
        """Finish app configuration (parameters that need a running wx.App) &
            launch main window.

            Parameters
            ----------
            event: wx.CloseEvent
                Information regarding the event.
        """
        #region	-----------------------------------------------------> Imports
        # pylint: disable=import-outside-toplevel
        from config.config import config as mConfig                             # Import here to speed up the creation of the splash window
        from main import menu   as mMenu
        from main import window as mWindow
        #endregion---------------------------------------------------> Imports

        #region -------------------------------------------------------> Fonts
        #------------------------------> Fonts
        fSeqAlignFont = wx.Font(
            14,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        fTreeItem = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Arial",
        )
        fTreeItemFileData = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        fTreeItemFileDataFalse = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_ITALIC,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        #------------------------------> Adapt to Win/Linux
        if mConfig.core.os == "Windows":
            fSeqAlignFont     = fSeqAlignFont.SetPointSize(12)
            fTreeItemFileData = fTreeItemFileData.SetPointSize(10)
        if mConfig.core.os not in ['Windows', 'Darwin']:
            fSeqAlignFont = fSeqAlignFont.SetPointSize(11)
        #------------------------------> Add to config
        mConfig.core.fSeqAlign              = fSeqAlignFont
        mConfig.core.fTreeItem              = fTreeItem
        mConfig.core.fTreeItemDataFile      = fTreeItemFileData
        mConfig.core.fTreeItemDataFileFalse = fTreeItemFileDataFalse
        #endregion ----------------------------------------------------> Fonts

        #region ------------------------------------------> User Configuration
        mConfig.LoadUserConfig()                                                # After fonts were created and assigned to config, load user values
        #endregion ---------------------------------------> User Configuration

        #region --------------------------------------------------------> Menu
        if mConfig.core.os == "Darwin":
            wx.MenuBar.MacSetCommonMenuBar(mMenu.MenuBarMain())
        #endregion -----------------------------------------------------> Menu

        #region ------------------------------------------> Create main window
        mConfig.main.mainWin = mWindow.WindowMain()
        #endregion ---------------------------------------> Create main window

        #region --------------------------------------------> Destroy & Return
        self.Destroy()
        return True
        #endregion -----------------------------------------> Destroy & Return
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


#region -----------------------------------------------------------> Start App
if __name__ == "__main__":
    app = UmsapApp()
    app.MainLoop()
#endregion --------------------------------------------------------> Start App

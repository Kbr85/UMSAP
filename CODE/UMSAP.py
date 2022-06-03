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


"""Utilities for Mass Spectrometry Analysis of Proteins (UMSAP).
    This module contains the wx.App instance starting the application.
"""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path

import wx
import wx.adv
#endregion ----------------------------------------------------------> Imports


DEVELOPMENT = True # Track state, development (True) or production (False)


#region -------------------------------------------------------------> Classes
class UmsapApp(wx.App):
    """Start the UMSAP app"""
    #region ----------------------------------------------> Overridden methods
    def OnInit(self) -> bool:
        """Initialize the app

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        os = platform.system()
        #------------------------------> image_loc
        if DEVELOPMENT:
            imgPath     = '/Resources/IMAGES/SPLASHSCREEN/splash.png'
            fileRoot    = Path(__file__).parent.parent
            imgFullPath = f'{fileRoot}{imgPath}'
        else:
            imgPath = '/RESOURCES/IMAGES/SPLASHSCREEN/splash.png'
            if os == 'Darwin':
                fileRoot = Path(__file__).parent.parent
            elif os == 'Windows':
                fileRoot = Path(__file__).parent
            else:
                fileRoot = Path(__file__).parent
            imgFullPath = f'{fileRoot}{imgPath}'
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> SplashScreen
        SplashWindow(str(imgFullPath))
        #endregion ---------------------------------------------> SplashScreen

        return True
    #---
    #endregion -------------------------------------------> Overridden methods
#---


class SplashWindow(wx.adv.SplashScreen):
    """Create the Splash Screen 

        Parameters
        ----------
        imgPath : str
            Path to the image used in the splash window
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, imgPath: str) -> None:
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
    def OnClose(self, event: wx.CloseEvent) -> bool:
        """Finish app configuration (parameters that need a running wx.App) &
            launch main window

            Parameters
            ----------
            rEvent : wx.CloseEvent
                Information regarding the event
        """
        #region	-----------------------------------------------------> Imports
        import config.config as config
        import dtscore.file as dtsFF
        import gui.menu as menu
        import gui.window as window
        #endregion---------------------------------------------------> Imports

        #region -------------------------------------------------------> Fonts
        #------------------------------> Sequence alignments in a panel
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
        if config.os == "Darwin":
            config.font['SeqAlign']              = fSeqAlignFont
            config.font['TreeItem']              = fTreeItem
            config.font['TreeItemDataFile']      = fTreeItemFileData
            config.font['TreeItemDataFileFalse'] = fTreeItemFileDataFalse
        elif config.os == "Windows":
            config.font['SeqAlign']             = fSeqAlignFont.SetPointSize(12)
            config.font['TreeItem']             = fTreeItem
            config.font['TreeItemDataFileFalse']= fTreeItemFileDataFalse
            config.font['TreeItemDataFile'] = fTreeItemFileData.SetPointSize(10)
        else:
            config.font['SeqAlign']             = fSeqAlignFont.SetPointSize(11)
            config.font['TreeItem']             = fTreeItem
            config.font['TreeItemDataFile']     = fTreeItemFileData
            config.font['TreeItemDataFileFalse']= fTreeItemFileDataFalse
        #endregion ----------------------------------------------------> Fonts

        #region ------------------------------------------> User Configuration
        # After fonts were created and assign to config, load user values
        try:
            data = dtsFF.ReadJSON(config.fConfig)
        except FileNotFoundError:
            data = {}
        except Exception as e:
            config.confUserFile = False
            config.confUserFileException = e
            data = {}
        #------------------------------>
        if data:
            #------------------------------> General
            config.general['checkUpdate'] = data['general'].get(
                'checkUpdate', config.general['checkUpdate'])
        else:
            pass
        #endregion ---------------------------------------> User Configuration

        #region --------------------------------------------------------> Menu
        if config.os == "Darwin":
            wx.MenuBar.MacSetCommonMenuBar(menu.MenuBarMain())
        else:
            pass
        #endregion -----------------------------------------------------> Menu

        #region ------------------------------------------> Create main window
        config.winMain = window.MainWindow()
        #endregion ---------------------------------------> Create main window

        #region --------------------------------------------> Destroy & Return
        self.Destroy()
        return True
        #endregion -----------------------------------------> Destroy & Return
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


if __name__ == "__main__":
    app = UmsapApp()
    app.MainLoop()
else:
    pass
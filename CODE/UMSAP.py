# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
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
    def OnInit(self):
        """ Initialize the app """

        #region ------------------------------------------------> SplashScreen
        cOS = platform.system()
        #--> Set location of splash image
        root = str(Path(__file__).parent.parent)
        if cOS == 'Darwin':
            if DEVELOPMENT:
                image_loc = root + '/Resources/IMAGES/SPLASHSCREEN/splash.png'
            else:
                image_loc = (
                    root +
                  '/UMSAP.app/Contents/Resources/IMAGES/SPLASHSCREEN/splash.png'
                )
        else:
            image_loc = root + '/Resources/IMAGES/SPLASHSCREEN/splash.png'
        #--> Launch splash window
        SplashWindow(image_loc)
        #endregion ---------------------------------------------> SplashScreen

        return True
    #---
    #endregion -------------------------------------------> Overridden methods
#---


class SplashWindow(wx.adv.SplashScreen):
    """ Create splash screen 
    
        Parameters
        ----------
        imgPath : str
            Path to the image to use in the splash window
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, imgPath):
        """		"""
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

    #region ---------------------------------------------------> Class methods
    def OnClose(self, event):
        """Finish app configuration (parameters that need a running wx.App) & 
            launch main window

            Parameters
            ----------
            event : wx.Event
                Information regarding the event
        """
        #region	-----------------------------------------------------> Imports
        import config.config as config
        import gui.menu as menu
        import gui.window as window
        #endregion---------------------------------------------------> Imports

        #region -------------------------------------------------------> Fonts
        #------------------------------> Sequence alignments in a panel
        SeqAlignFont = wx.Font(
            14,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        TreeItem = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Arial",
        )
        TreeItemFalse = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_ITALIC,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Arial",
        )
        TreeItemFileData = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        TreeItemFileDataFalse = wx.Font(
            12,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_ITALIC,
            wx.FONTWEIGHT_NORMAL,
            False,
            faceName="Courier",
        )
        if config.cOS == "Darwin":
            config.font['SeqAlign']              = SeqAlignFont
            config.font['TreeItem']              = TreeItem
            config.font['TreeItemFalse']         = TreeItemFalse
            config.font['TreeItemDataFile']      = TreeItemFileData
            config.font['TreeItemDataFileFalse'] = TreeItemFileDataFalse
        elif config.cOS == "Windows":
            config.font['SeqAlign']              = SeqAlignFont.SetPointSize(12)
            config.font['TreeItem']              = TreeItem
            config.font['TreeItemFalse']         = TreeItemFalse
            config.font['TreeItemDataFile']      = TreeItemFileData
            config.font['TreeItemDataFileFalse'] = TreeItemFileDataFalse
        elif config.cOS == "Linux":
            config.font['SeqAlign']              = SeqAlignFont.SetPointSize(11)
            config.font['TreeItem']              = TreeItem
            config.font['TreeItemFalse']         = TreeItemFalse
            config.font['TreeItemDataFile']      = TreeItemFileData
            config.font['TreeItemDataFileFalse'] = TreeItemFileDataFalse
        else:
            config.font['SeqAlign']              = SeqAlignFont
            config.font['TreeItem']              = TreeItem
            config.font['TreeItemDataFile']      = TreeItemFileData
            config.font['TreeItemDataFileFalse'] = TreeItemFileDataFalse
        #endregion ----------------------------------------------------> Fonts

        #region --------------------------------------------------------> Menu
        if config.cOS == "Darwin":
            wx.MenuBar.MacSetCommonMenuBar(menu.MainMenuBar())
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
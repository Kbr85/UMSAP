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


"""Tabs for the main module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class Start(wx.Panel):
    """Start tab.

        Parameters
        ----------
        parent: wx.Window
            Direct parent of the widgets in the tab.
    """
    #region -----------------------------------------------------> Class setup
    cName  = mConfig.main.ntStart
    tTitle = mConfig.main.ttStart
    #------------------------------> Files
    cImg = mConfig.core.fImgStart
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, *args, **kwargs) -> None:              # pylint: disable=unused-argument
        """"""
        #region -----------------------------------------------> Initial setup
        self.cParent = parent
        #------------------------------>
        super().__init__(parent=parent, name=self.cName)
        #------------------------------>
        self.SetBackgroundColour('white')
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------>  Images
        self.wImg = wx.StaticBitmap(
            self,bitmap=wx.Bitmap(str(self.cImg), wx.BITMAP_TYPE_ANY))
        #------------------------------> Buttons
        self.wBtnCorrA    = wx.Button(self, label=mConfig.corr.tUtil)
        self.wBtnDataPrep = wx.Button(self, label=mConfig.data.nUtil)
        self.wBtnLimProt  = wx.Button(self, label=mConfig.limp.nMod)
        self.wBtnProtProf = wx.Button(self, label=mConfig.prot.nMod)
        self.wBtnTarProt  = wx.Button(self, label=mConfig.tarp.nMod)
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        self.wBtnCorrA.SetToolTip(f'Start the utility {mConfig.corr.tUtil}')
        self.wBtnDataPrep.SetToolTip(f'Start the utility {mConfig.data.nUtil}')
        self.wBtnLimProt.SetToolTip (f'Start the module {mConfig.limp.nMod}')
        self.wBtnProtProf.SetToolTip(f'Start the module {mConfig.prot.nMod}')
        self.wBtnTarProt.SetToolTip (f'Start the module {mConfig.tarp.nMod}')
        #endregion -------------------------------------------------> Tooltips

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizers
        self.sSizer	 = wx.BoxSizer(wx.VERTICAL)
        #------------------------------>  Add widgets
        self.sBtn  = wx.BoxSizer(wx.VERTICAL)
        self.sBtn.Add(self.wBtnCorrA, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnDataPrep, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnLimProt, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnProtProf, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnTarProt, 0, wx.EXPAND|wx.ALL, 5)
        #--------------> GridSizer
        self.sGrid = wx.BoxSizer(wx.HORIZONTAL)
        self.sGrid.Add(self.wImg, 0, wx.EXPAND|wx.RIGHT, 25)
        self.sGrid.Add(self.sBtn, 0, wx.ALIGN_CENTRE_VERTICAL|wx.LEFT, 25)
        #--------------> Main Sizer
        self.sSizer.AddStretchSpacer(1)
        self.sSizer.Add(self.sGrid, 0, wx.CENTER|wx.ALL, 5)
        self.sSizer.AddStretchSpacer(1)
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wBtnCorrA.Bind(
            wx.EVT_BUTTON,
            lambda event: mConfig.main.mainWin.CreateTab(mConfig.corr.nTab)     # type: ignore
        )
        self.wBtnDataPrep.Bind(
            wx.EVT_BUTTON,
            lambda event: mConfig.main.mainWin.CreateTab(mConfig.data.nTab)     # type: ignore
        )
        self.wBtnLimProt.Bind(
            wx.EVT_BUTTON,
            lambda event: mConfig.main.mainWin.CreateTab(mConfig.limp.nTab)     # type: ignore
        )
        self.wBtnProtProf.Bind(
            wx.EVT_BUTTON,
            lambda event: mConfig.main.mainWin.CreateTab(mConfig.prot.nTab)     # type: ignore
        )
        self.wBtnTarProt.Bind(
            wx.EVT_BUTTON,
            lambda event: mConfig.main.mainWin.CreateTab(mConfig.tarp.nTab)     # type: ignore
        )
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

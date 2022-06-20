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


"""Tabs of the application"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Union

import wx
import wx.lib.agw.aui as aui

import config.config as mConfig
import data.method as mMethod
import gui.pane as mPane
import gui.widget as mWidget
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class BaseConfTab(wx.Panel):
    """Base class for a Tab containing only a configuration panel. 

        Parameters
        ----------
        parent : wx.Window
            Parent of the tab.
        name: str
            Name of the tab.
        dataI : dict
            Initial data provided by the user to performed a previous analysis.

        Attributes
        ----------
        dConfPanel : dict
            Classes to create the configuration panel in the Tab. Keys are
            config.ntNAMES and values the corresponding method.
    """
    #region -----------------------------------------------------> Class setup
    dConfPanel = {
        mConfig.ntCorrA   : mPane.PaneCorrA,
        mConfig.ntDataPrep: mPane.PaneDataPrep,
        mConfig.ntLimProt : mPane.PaneLimProt,
        mConfig.ntProtProf: mPane.PaneProtProf,
        # mConfig.ntTarProt : mPane.PaneTarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, name: str='', dataI: dict={}) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent    = parent
        self.cName      = name
        self.clPaneConf = getattr(self, 'clPaneConf', mConfig.lnPaneConf)
        #------------------------------> 
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wConf = self.dConfPanel[self.cName](self, dataI)
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.wConf, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.clPaneConf
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------> 
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class BaseConfListTab(BaseConfTab):
    """Base class for a Tab containing a configuration panel and a right list
        panel. 

        Parameters
        ----------
        parent : wx.Window
            Parent of the tab
        name: str or None
            Unique name of the Tab
        dataI : dict or None
            Initial data provided by the user to performed a previous analysis
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, name: str='', dataI:dict={}) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCColLabel  = getattr(self, 'cLCColLabel', mConfig.lLCtrlColNameI)
        self.cSColSize    = getattr(self, 'cLCColSize',  mConfig.sLCtrlColI)
        self.cLCPaneTitle = getattr(self, 'cLCPaneTitle',mConfig.lnListPane)
        
        super().__init__(parent, name=name, dataI=dataI)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCtrl = mWidget.MyListCtrlZebraMaxWidth(
            self, colLabel=self.cLCColLabel, colSize=self.cSColSize)
        #----------------------------> Pointer to lc to load data file content
        self.wConf.wLCtrlI = self.wLCtrl
        self.wConf.rLCtrlL = [self.wLCtrl]
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------> Aui control
        self._mgr.AddPane(
            self.wLCtrl, 
            aui.AuiPaneInfo(
                ).Right(
                ).Caption(
                    self.cLCPaneTitle
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------>
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control

        #region --------------------------------------------------------> TEST
        if mConfig.development:
            self.wConf.OnIFileLoad('fEvent')
        else:
            pass
        #endregion -----------------------------------------------------> TEST
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ResControlExp(wx.Panel):
    """Creates the panel containing the panes for the dialog Results - Control
        Experiments.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel
        iFile : Path
            Path to the Data File already selected in the parent window
        topParent : wx.Widget
            Window calling the dialog.

        Attributes
        ----------
        dWidget : dict of methods
            Methods to create the configuration panel
    """
    #region -----------------------------------------------------> Class setup
    cName = 'ResControlExpPane'

    dWidget = {
        mConfig.npProtProf : mPane.PaneResControlExpConfProtProf,
        # config.npLimProt  : pane.LimProtResControlExp,
        # config.npTarProt  : pane.TarProtResControlExp,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: 'wx.Window',
        iFile: Union[Path, str],
        topParent: 'wx.Window',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Label
        self.cLLCtrlColName = getattr(
            self, 'cLLCtrlColName', mConfig.lLCtrlColNameI)
        self.cLPaneConf = getattr(self, 'cLPaneConf', mConfig.lnPaneConf)
        self.cLPaneList = getattr(self, 'cLPaneList', mConfig.lnListPane)
        #------------------------------> Size
        self.cSLCTrlCol = getattr(self, 'cSLCTrlCol', mConfig.sLCtrlColI)
        #------------------------------> 
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> ListCtrl and fill it
        self.wLCtrl = mWidget.MyListCtrlZebraMaxWidth(
            self, 
            colLabel = self.cLLCtrlColName,
            colSize  = self.cSLCTrlCol,
        )
        mMethod.LCtrlFillColNames(self.wLCtrl, iFile)
        #------------------------------> Conf panel here to read NRow in lc
        self.wConf = self.dWidget[topParent.cName]( # type: ignore
            self, topParent, self.wLCtrl.GetItemCount())
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------> Aui control
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.wConf, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.cLPaneConf
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        self._mgr.AddPane(
            self.wLCtrl, 
            aui.AuiPaneInfo(
                ).Right(
                ).Caption(
                    self.cLPaneList
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class TabStart(wx.Panel):
    """Start tab

        Parameters
        ----------
        parent : wx.Window
            Direct parent of the widgets in the tab.
        args : extra arguments
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.ntStart
    #------------------------------> Files
    cImg = mConfig.fImgStart
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, *args, **kwargs) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.cParent = parent
        #------------------------------>
        super().__init__(parent=parent, name=self.cName)
        self.SetBackgroundColour('white')
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------>  Images
        self.wImg = wx.StaticBitmap(
            self,bitmap=wx.Bitmap(str(self.cImg), wx.BITMAP_TYPE_ANY))
        #------------------------------> Buttons
        self.wBtnCorrA    = wx.Button(self, label=mConfig.nuCorrA)
        self.wBtnDataPrep = wx.Button(self, label=mConfig.nuDataPrep)
        self.wBtnLimProt  = wx.Button(self, label=mConfig.nmLimProt)
        self.wBtnProtProf = wx.Button(self, label=mConfig.nmProtProf)
        self.wBtnTarProt  = wx.Button(self, label=mConfig.nmTarProt)
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        self.wBtnDataPrep.SetToolTip(f'Start the utility {mConfig.nuDataPrep}')
        self.wBtnCorrA.SetToolTip(f'Start the utility {mConfig.nuCorrA}')
        self.wBtnLimProt.SetToolTip (f'Start the module {mConfig.nmLimProt}')
        self.wBtnProtProf.SetToolTip(f'Start the module {mConfig.nmProtProf}')
        self.wBtnTarProt.SetToolTip (f'Start the module {mConfig.nmTarProt}')
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
            lambda event: mConfig.winMain.CreateTab(mConfig.ntCorrA) # type: ignore
        )
        self.wBtnDataPrep.Bind(
            wx.EVT_BUTTON, 
            lambda event: mConfig.winMain.CreateTab(mConfig.ntDataPrep) # type: ignore
        )
        self.wBtnLimProt.Bind(
            wx.EVT_BUTTON, 
            lambda event: mConfig.winMain.CreateTab(mConfig.ntLimProt) # type: ignore
        )
        self.wBtnProtProf.Bind(
            wx.EVT_BUTTON, 
            lambda event: mConfig.winMain.CreateTab(mConfig.ntProtProf) # type: ignore
        )
        self.wBtnTarProt.Bind(
            wx.EVT_BUTTON, 
            lambda event: mConfig.winMain.CreateTab(mConfig.ntTarProt) # type: ignore
        )
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

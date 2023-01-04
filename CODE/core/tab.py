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


"""Base Tabs for the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Union

import wx
from wx import aui

from config.config import config as mConfig
from core     import method as cMethod
from core     import widget as cWidget
from corr     import pane   as corrPane
from dataprep import pane   as dataPane
from protprof import pane   as protPane
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class BaseConfTab(wx.Panel):
    """Base class for a Tab containing only a configuration panel.

        Parameters
        ----------
        parent: wx.Window
            Parent of the tab.
        dataI: dict
            Initial data provided by the user to redo a previous analysis.

        Attributes
        ----------
        dConfPanel : dict
            Classes to create the configuration panel in the Tab. Keys are
            config.ntNAMES and values the corresponding method.
    """
    #region -----------------------------------------------------> Class setup
    dConfPanel = {
        mConfig.corr.nTab : corrPane.CorrA,
        mConfig.data.nTab : dataPane.DataPrep,
        # mConfig.ntLimProt : mPane.PaneLimProt,
        mConfig.prot.nTab : protPane.ProtProf,
        # mConfig.ntTarProt : mPane.PaneTarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, dataI:dict={}) -> None:                # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent    = parent
        self.cName      = getattr(self, 'cName',      mConfig.core.ntDef)
        self.tTitle     = getattr(self, 'cTitle',     mConfig.core.tTabDef)
        self.clPaneConf = getattr(self, 'clPaneConf', mConfig.core.tPaneConf)
        #------------------------------>
        super().__init__(parent, name=self.cName, size=(500,500))
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
        parent: wx.Window
            Parent of the tab.
        dataI: dict or None
            Initial data provided by the user to performed a previous analysis.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, dataI:dict={}) -> None:                # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCColLabel  = getattr(self, 'cLCColLabel',  mConfig.core.lLCtrlColNameI)
        self.cSColSize    = getattr(self, 'cLCColSize',   mConfig.core.sLCtrlColI)
        self.cLCPaneTitle = getattr(self, 'cLCPaneTitle', mConfig.core.tListPane)
        #------------------------------>
        super().__init__(parent, dataI=dataI)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCtrl = cWidget.MyListCtrlZebraMaxWidth(
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
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ResControlExp(wx.Panel):
    """Creates the panel containing the panes for the dialog Results - Control
        Experiments.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel.
        iFile: Path
            Path to the Data File already selected in the parent window.
        topParent: wx.Window
            Window calling the dialog.

        Attributes
        ----------
        dWidget: dict of methods
            Methods to create the configuration panel.
    """
    #region -----------------------------------------------------> Class setup
    cName = 'ResControlExpPane'

    dWidget = {
        mConfig.prot.nPane : protPane.ResControlExpConf,
        # mConfig.npLimProt  : mPane.PaneResControlExpConfLimProt,
        # mConfig.npTarProt  : mPane.PaneResControlExpConfTarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        iFile:Union[Path, str],
        topParent:wx.Window,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Label
        self.cLLCtrlColName = getattr(
            self, 'cLLCtrlColName', mConfig.core.lLCtrlColNameI)
        self.cLPaneConf = getattr(self, 'cLPaneConf', mConfig.core.tPaneConf)
        self.cLPaneList = getattr(self, 'cLPaneList', mConfig.core.tListPane)
        #------------------------------> Size
        self.cSLCTrlCol = getattr(self, 'cSLCTrlCol', mConfig.core.sLCtrlColI)
        #------------------------------>
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> ListCtrl and fill it
        self.wLCtrl = cWidget.MyListCtrlZebraMaxWidth(
            self,
            colLabel = self.cLLCtrlColName,
            colSize  = self.cSLCTrlCol,
        )
        cMethod.LCtrlFillColNames(self.wLCtrl, iFile)
        #------------------------------> Conf panel here to read NRow in lc
        self.wConf = self.dWidget[topParent.cName](                             # type: ignore
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
                ).BestSize(
                    (100,100)
            )
        )
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

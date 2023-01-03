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
from typing  import Union

import wx
import wx.lib.agw.aui as aui

import config.config as mConfig
import gui.method    as gMethod
import gui.pane      as mPane
import gui.widget    as mWidget
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class ResControlExp(wx.Panel):
    """Creates the panel containing the panes for the dialog Results - Control
        Experiments.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel.
        iFile : Path
            Path to the Data File already selected in the parent window.
        topParent : wx.Widget
            Window calling the dialog.

        Attributes
        ----------
        dWidget : dict of methods
            Methods to create the configuration panel.
    """
    #region -----------------------------------------------------> Class setup
    cName = 'ResControlExpPane'

    dWidget = {
        mConfig.npProtProf : mPane.PaneResControlExpConfProtProf,
        mConfig.npLimProt  : mPane.PaneResControlExpConfLimProt,
        mConfig.npTarProt  : mPane.PaneResControlExpConfTarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent   : 'wx.Window',
        iFile    : Union[Path, str],
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
        gMethod.LCtrlFillColNames(self.wLCtrl, iFile)
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



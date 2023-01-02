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
import wx
from wx import aui

from config.config import config as mConfig
from corr import pane as corrPane
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
        mConfig.corr.nTab : corrPane.PaneCorrA,
        # mConfig.ntDataPrep: mPane.PaneDataPrep,
        # mConfig.ntLimProt : mPane.PaneLimProt,
        # mConfig.ntProtProf: mPane.PaneProtProf,
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
#endregion ----------------------------------------------------------> Classes

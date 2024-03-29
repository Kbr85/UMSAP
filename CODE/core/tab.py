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


"""Core Tabs for the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Union

import wx
from wx import aui

from config.config import config as mConfig
from core     import method as cMethod
from core     import pane   as cPane
from core     import widget as cWidget
from corr     import pane   as corrPane
from dataprep import pane   as dataPane
from limprot  import pane   as limpPane
from protprof import pane   as protPane
from tarprot  import pane   as tarpPane
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class BaseConfTab(wx.Panel):
    """Base class for a Tab containing only a configuration panel.

        Parameters
        ----------
        parent: wx.Window
            Parent of the tab.

        Attributes
        ----------
        dConfPanel : dict
            Classes to create the configuration panel in the Tab. Keys are
            config.ntNAMES and values the corresponding method.
    """
    #region -----------------------------------------------------> Class setup
    dConfPanel = {
        mConfig.corr.nTab: corrPane.CorrA,
        mConfig.data.nTab: dataPane.DataPrep,
        mConfig.limp.nTab: limpPane.LimProt,
        mConfig.prot.nTab: protPane.ProtProf,
        mConfig.tarp.nTab: tarpPane.TarProt,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent    = parent
        self.cName      = getattr(self, 'cName',      mConfig.core.ntDef)
        self.tTitle     = getattr(self, 'cTitle',     mConfig.core.ttDef)
        self.clPaneConf = getattr(self, 'clPaneConf', mConfig.core.tpConf)
        #------------------------------>
        super().__init__(parent, name=self.cName, size=(500,500))
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wConf = self.dConfPanel[self.cName](self)
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
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCColLabel  = getattr(self, 'cLCColLabel',  mConfig.core.lLCtrlColNameI)
        self.cSColSize    = getattr(self, 'cLCColSize',   mConfig.core.sLCtrlColI)
        self.cLCPaneTitle = getattr(self, 'cLCPaneTitle', mConfig.core.tpList)
        #------------------------------>
        super().__init__(parent)
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
        mConfig.corr.nPane : cPane.ResControlExpConfGroups,
        mConfig.data.nPane : cPane.ResControlExpConfGroups,
        mConfig.prot.nPane : protPane.ResControlExpConf,
        mConfig.limp.nPane : limpPane.ResControlExpConf,
        mConfig.tarp.nPane : tarpPane.ResControlExpConf,
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
        self.cLPaneConf = getattr(self, 'cLPaneConf', mConfig.core.tpConf)
        self.cLPaneList = getattr(self, 'cLPaneList', mConfig.core.tpList)
        #------------------------------> Size
        self.cSLCTrlCol = getattr(self, 'cSLCTrlCol', mConfig.core.sLCtrlColI)
        #------------------------------>
        super().__init__(parent, name=self.cName, size=(500,500))
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
                    (200,100)
            )
        )
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

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


"""Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread
import shutil
from math    import ceil
from pathlib import Path
from typing  import Union, Optional

import pandas as pd

import wx
import wx.lib.scrolledpanel as scrolled

import config.config  as mConfig
import data.check     as mCheck
import data.method    as mMethod
import data.exception as mException
import data.file      as mFile
import data.statistic as mStatistic
import gui.method     as gMethod
import gui.validator  as mValidator
import gui.widget     as mWidget
import gui.window     as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class PaneListCtrlSearchPlot(wx.Panel):
    """Creates a panel with a wx.ListCtrl and below it a wx.SearchCtrl.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel
        colLabel : list of str or None
            Name of the columns in the wx.ListCtrl. Default is None
        colSize : list of int or None
            Size of the columns in the wx.ListCtrl. Default is None
        data : list[list]
            Initial Data for the wx.ListCtrl.
        style : wx.Style
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        tcHint : str
            Hint for the wx.SearchCtrl. Default is ''.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npListCtrlSearchPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent  : wx.Window,
        colLabel: list[str]=[],
        colSize : list[int]=[],
        data    : list[list]=[],
        style   : int=wx.LC_REPORT,
        tcHint  : str='',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCS = mWidget.ListCtrlSearch(
            self,
            listT    = 2,
            colLabel = colLabel,
            colSize  = colSize,
            canCut   = False,
            canPaste = False,
            style    = style,
            data     = data,
            tcHint   = tcHint,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.SetSizer(self.wLCS.sSizer)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class NPlots(wx.Panel):
    """The panel will contain N plots distributed in a wx.FlexGridSizer.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.Panel holding the plots.
        tKeys : list of str
            Keys for a dict holding a reference to the plots
        nCol : int
            Number of columns in the wx.FlexGridSizer holding the plots.
            Number of needed rows will be automatically calculated.
        dpi : int
            DPI value for the Matplot plots.
        statusbar : wx.StatusBar or None
            StatusBar to display information about the plots.

        Attributes
        ----------
        dPlot : dict
            Keys are tKeys and values mWidget.MatPlotPanel
        cName : str
            Name of the panel holding the plots.
        nCol : int
            Number of columns in the sizer
        nRow: int
            Number of rows in the sizer.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npNPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent   : wx.Window,
        tKeys    : list[str],
        nCol     : int,
        dpi      : int=mConfig.confGeneral['DPI'],
        statusbar: Optional[wx.StatusBar]=None,
        ) -> None  :
        """ """
        #region -----------------------------------------------> Initial Setup
        self.nCol = nCol
        self.nRow = ceil(len(tKeys)/nCol)
        #------------------------------>
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region ------------------------------------------------------> Sizers
        #------------------------------>
        self.sSizer = wx.FlexGridSizer(self.nRow, self.nCol, 1,1)
        #------------------------------>
        for k in range(0, self.nCol):
            self.sSizer.AddGrowableCol(k,1)
        for k in range(0, self.nRow):
            self.sSizer.AddGrowableRow(k,1)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------------> Widgets
        self.dPlot = {}
        for k in tKeys:
            #------------------------------> Create
            self.dPlot[k] = mWidget.MatPlotPanel(
                self, dpi=dpi, statusbar=statusbar)
            #------------------------------> Add to sizer
            self.sSizer.Add(self.dPlot[k], 1, wx.EXPAND|wx.ALL, 5)
        #endregion --------------------------------------------------> Widgets
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

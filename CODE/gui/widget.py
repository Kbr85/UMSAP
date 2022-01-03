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


""" Widgets of the application"""


#region -------------------------------------------------------------> Imports
import wx

import dat4s_core.gui.wx.validator as dtsValidator

import config.config as config
import gui.window as window
#endregion ----------------------------------------------------------> Imports


class ResControl():
    """Creates the Results - Control experiment widgets.

        Parameters
        ----------
        parent : wx widget
            Parent of the widgets

        Attributes
        ----------
        cLResControl : str
            Label for the wx.StaticText. Default to config.lStResultCtrl.
        btnResultsW: wx.Button 
        stResults: wx.StaticText
        tcResults: wx.TextCtrl
        
        Notes
        -----
        Several configuration options are taken from parent.
        Used as parent class.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window):
        """ """
        self.cLResControl = config.lStResultCtrl
        #region -----------------------------------------------------> Widgets
        self.tcResults = wx.TextCtrl(
            parent    = parent,
            style     = wx.TE_READONLY,
            value     = "",
            size      = config.sTc,
            validator = dtsValidator.IsNotEmpty(),
        )

        self.stResults = wx.StaticText(
            parent = parent,
            label  = self.cLResControl,
            style  = wx.ALIGN_RIGHT
        )

        self.btnResultsW = wx.Button(
            parent = parent,
            label  = config.lBtnTypeResCtrl,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.sizerRes = wx.GridBagSizer(1,1)
        #------------------------------> 
        self.sizerRes.Add(
            self.stResults,
            pos    = (0,0),
            flag   = wx.ALIGN_LEFT|wx.ALL,
            border = 5,
            span   = (0,2),
        )
        self.sizerRes.Add(
            self.btnResultsW,
            pos    = (1,0),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5
        )
        self.sizerRes.Add(
            self.tcResults,
            pos    = (1,1),
            flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5,
        )
        #------------------------------> 
        self.sizerRes.AddGrowableCol(1,1)
        #endregion ---------------------------------------------------> Sizers
        
        #region -----------------------------------------------------> Tooltip
        self.btnResultsW.SetToolTip(
            f"Type the column numbers in a helper window."
        )
        self.stResults.SetToolTip(
            f"Set the column numbers containing the control and experiment "
            f"results."
        )
        #endregion --------------------------------------------------> Tooltip
        
        #region --------------------------------------------------------> Bind
        self.btnResultsW.Bind(wx.EVT_BUTTON, self.OnResW)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnResW(self, event):
        """ Open the window to write the results columns. """
        #------------------------------> 
        with window.ResControlExp(self) as dlg:
            dlg.ShowModal()
        #------------------------------> 
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---



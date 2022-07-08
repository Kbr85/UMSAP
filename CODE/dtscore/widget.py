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


#region -------------------------------------------------------------> Imports
import _thread
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, Union, Callable

import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import wx
import wx.lib.mixins.listctrl as listmix

import config.config as config
import dtscore.check as dtsCheck
import dtscore.exception as dtsException
import dtscore.file as dtsFF
import dtscore.generator as dtsGenerator
import dtscore.window as dtsWindow
#endregion ----------------------------------------------------------> Imports


#region ------------------------------------------------------> Single widgets

#endregion ---------------------------------------------------> Single widgets


#region ---------------------------------------------------------> Mix widgets
class ListCtrlSearch():
    """Creates a wx.ListCtrl with a wx.SearchCtrl beneath it.
    
        See Notes below for more details

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        listT : 0, 1 or 2
            Type of wx.ListCtrl. 
        setSizer : bool
            Arrange widgets in self.Sizer. Default is True.
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color : str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        tcHint : str
            Hint for the wx.TextCtrl

        Attributes
        ----------
        listTDict: dict
            Keys are 0,1,2 and methods the class for the wx.ListCtrl.
        lc : wx.ListCtrl
        search : wx.SearchCtrl
    """
    #region -----------------------------------------------------> Class setup
    listTDict = {
        0: MyListCtrl,
        1: ListZebra,
        2: ListZebraMaxWidth,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, listT: int=1, setSizer=True, 
        color: str=config.color['Zebra'], colLabel: Optional[list[str]]=None, 
        colSize: Optional[list[int]]=None, canCopy: bool=True, 
        canCut: bool=False, canPaste: bool=False, copyFullContent: bool=False, 
        sep: str=' ', pasteUnique: bool=True, selAll: bool=True, 
        style=wx.LC_REPORT, data: list[list]=[], tcHint: str='',
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
            
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ListCtrl
        self.lc = self.listTDict[listT](
            parent,
            color           = color,
            colLabel        = colLabel,
            colSize         = colSize,
            canCopy         = canCopy,
            canCut          = canCut,
            canPaste        = canPaste,
            copyFullContent = copyFullContent,
            sep             = sep,
            pasteUnique     = pasteUnique,
            selAll          = selAll,
            style           = style,
            data            = data,
        )
        #------------------------------> wx.SearchCtrl
        self.search = wx.SearchCtrl(parent)
        self.search.SetHint(tcHint) if tcHint != '' else ''
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            #------------------------------> 
            self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
            #------------------------------> 
            self.Sizer.Add(self.lc, 1, wx.EXPAND|wx.ALL, 5)
            self.Sizer.Add(self.search, 0, wx.EXPAND|wx.ALL, 5)
        else:
            pass
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods

    #endregion ------------------------------------------------> Class methods
#---
#endregion ------------------------------------------------------> Mix widgets




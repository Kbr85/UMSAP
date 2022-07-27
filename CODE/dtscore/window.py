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
from math import ceil
from pathlib import Path
from typing import Optional, Literal, Union

import wx

import config.config as config
import dtscore.data_method as dtsMethod
import dtscore.exception as dtsException
import dtscore.file as dtsFF
import dtscore.widget as dtsWidget
#endregion ----------------------------------------------------------> Imports


#region ---------------------------------------------------> Frames and panels
class TxtContentWin(wx.Panel):
    """ Creates a window that show the content of a plain text file.

        See Notes below for more details.
    
        Parameters
        ----------
        parent : wx widget or None
            Parent of the widgets
        name : str
            To id the panel in the application. Default values is 'LicAgr'
        fileP : path
            Location of file containing license text
        
        Attributes
        ----------
        confMsg : dict
            Message for users
        name : str
            To id the panel in the application
        fileP : path
            Location of the file containing the text of the license
        confMsg : dict
            Message for users
        tc : wx.TextCtrl
            wx.TextCtrl to show the text of the license
        Sizer : wx.BoxSizer

        Raises
        ------
        InputError:
            - When fileP is not a valid path
            - When fileP cannot be read
            
        Notes
        -----
        This is a wx.Panel with a wx.TextCtrl to show the license of the 
        project. Custom licenses can be provided with the path to a plain text 
        file.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, fileP: Path, name: str='LicAgr'
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.name = name

        super().__init__(parent=parent, name=name)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.tc = wx.TextCtrl(
            self,
            style = wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.TE_READONLY,
        )
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------> Fill text
        for k in dtsFF.ReadFile(self.fileP, char=None, empty=True):
            self.tc.AppendText(k[0]+'\n')
        self.tc.SetInsertionPoint(0)
        #endregion ------------------------------------------------> Fill text

        #region ------------------------------------------------------- Sizers
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.tc, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------- Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ------------------------------------------------> Frames and panels
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


""" GUI common methods """


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Optional

import wx

import config.config as config
import dtscore.window as dtsWindow
import gui.window as window
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def LoadUMSAPFile(
    fileP: Optional[Path]=None, win: Optional[wx.Window]=None,
    ) -> bool:
    """Load an UMSAP File either from Read UMSAP File menu, LoadResults
        method in Tab or Update File Content menu.

        Parameters
        ----------
        fileP : Path or None
            If None, it is assumed the method is called from Read UMSAP File
            menu. Default is None.
        win : wx.Window or None
            If called from menu it is used to center the Select File wx.Dialog.
            Default is None.

        Return
        ------
        bool
    """
    #region --------------------------------------------> Get file from Dialog
    if fileP is None:
        try:
            #------------------------------>
            dlg = dtsWindow.FileSelectDialog(
                'openO',
                ext    = config.elUMSAP,
                parent = win,
                msg    = config.mFileSelUMSAP,
            )
            #------------------------------>
            if dlg.ShowModal() == wx.ID_OK:
                tFileP = Path(dlg.GetPath())
            else:
                return False
        except Exception as e:      
            dtsWindow.NotificationDialog(
                'errorF', 
                msg        = config.mFileSelector,
                tException = e,
                parent     = win,
            )
            return False
    else:
        tFileP = fileP
    #endregion -----------------------------------------> Get file from Dialog

    #region ----------------------------> Raise window if file is already open
    if config.winUMSAP.get(tFileP, '') != '':
        config.winUMSAP[tFileP].UpdateFileContent()
        config.winUMSAP[tFileP].Raise()
        return True
    else:
        config.winUMSAP[tFileP] = window.UMSAPControl(tFileP)
    #endregion -------------------------> Raise window if file is already open

    return True
#---


def GetDisplayInfo(win: wx.Frame) -> dict[str, dict[str, int]]:
    """This will get the information needed to set the position of a window.
        Should be called after Fitting sizers for accurate window size 
        information.

        Parameters
        ----------
        win : wx.Frame
            Window to be positioned

        Returns
        -------
        dict
            {
                'D' : {'xo':X, 'yo':Y, 'w':W, 'h':h}, Info about display
                'W' : {'N': N, 'w':W, 'h', H},        Info about win
            }
    """
    #region ----------------------------------------------------> Display info
    xd, yd, wd, hd =  wx.Display(win).GetClientArea()
    #endregion -------------------------------------------------> Display info

    #region -----------------------------------------------------> Window info
    nw = config.winNumber.get(win.cName, 0) #type: ignore
    ww, hw = win.GetSize()
    #endregion --------------------------------------------------> Window info

    #region ------------------------------------------------------------> Dict
    data = {
        'D' : {
            'xo' : xd,
            'yo' : yd,
            'w'  : wd,
            'h'  : hd,
        },
        'W' : {
            'N' : nw,
            'w' : ww,
            'h' : hw,
        },
    }
    #endregion ---------------------------------------------------------> Dict

    return data
#---
#endregion ----------------------------------------------------------> Methods
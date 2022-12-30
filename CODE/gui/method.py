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
from typing  import Optional, Union

import wx

import config.config as mConfig
import gui.window    as mWindow
import data.file     as mFile
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def LoadUMSAPFile(
    fileP: Optional[Path]      = None,
    win  : Optional[wx.Window] = None,
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
        dlg = mWindow.DialogFileSelect(
            'openO',
            ext    = mConfig.elUMSAP,
            parent = win,
            msg    = mConfig.mFileSelUMSAP,
        )
        #------------------------------>
        if dlg.ShowModal() == wx.ID_OK:
            tFileP = Path(dlg.GetPath())
        else:
            return False
    else:
        tFileP = fileP
    #endregion -----------------------------------------> Get file from Dialog

    #region ----------------------------> Raise window if file is already open
    if mConfig.winUMSAP.get(tFileP, '') != '':
        #------------------------------>
        try:
            mConfig.winUMSAP[tFileP].UpdateFileContent()
        except Exception as e:
            msg = mConfig.mFileRead.format(tFileP)
            mWindow.DialogNotification('errorU', msg=msg, tException=e)
            return False
        #------------------------------>
        mConfig.winUMSAP[tFileP].Raise()
        #------------------------------>
        return True
    else:
        try:
            mConfig.winUMSAP[tFileP] = mWindow.WindowUMSAPControl(tFileP)
        except Exception as e:
            msg = mConfig.mFileRead.format(tFileP)
            mWindow.DialogNotification('errorU', msg=msg, tException=e)
            return False
    #endregion -------------------------> Raise window if file is already open

    return True
#---


def LCtrlFillColNames(lc: wx.ListCtrl, fileP: Union[Path, str]) -> bool:
    """Fill the wx.ListCtrl with the name of the columns in fileP.

        Parameters
        ----------
        lc : wx.ListCtrl
            wx.ListCtrl to fill info into
        fileP : Path
            Path to the file from which to read the column names

        Notes
        -----
        This will delete the wx.ListCtrl before adding the new names.
        wx.ListCtrl is assumed to have at least two columns [#, Name,]
    """
    #region -------------------------------------------------------> Read file
    colNames = mFile.ReadFileFirstLine(fileP)
    #endregion ----------------------------------------------------> Read file

    #region -------------------------------------------------------> Fill List
    #------------------------------> Del items
    lc.DeleteAllItems()
    #------------------------------> Fill
    for k, v in enumerate(colNames):
        index = lc.InsertItem(k, " " + str(k))
        lc.SetItem(index, 1, v)
    #endregion ----------------------------------------------------> Fill List

    return True
#---
#endregion ----------------------------------------------------------> Methods

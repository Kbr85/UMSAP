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
from typing import Literal, Optional

import wx

import dtscore.window as dtsWindow
#endregion ----------------------------------------------------------> Imports


def GetFilePath(
    mode: Literal['openO', 'openM', 'save'], ext: str,
    parent: Optional[wx.Window]=None, msg: Optional[str]=None,
    ) -> list[str]:
    """Open the dtsWindow.FileSelectDialog to select files.

        Parameters
        ----------
        mode : str
            One of 'openO', 'openM', 'save'. The same values are used in
            dat4s_core.widget.wx_widget.ButtonTextCtrlFF.mode
        ext : str
            File extensions, 'txt files (*.txt)|*.txt'
        parent : wx.Window or None
            Parent of the window. If given modal window will be centered on it
        msg : str or None
            Message to show in the window

        Returns
        -------
        list
            List of selected file paths as str or empty list
    """
    #region ------------------------------------------------> Create wx.Dialog
    try:
        dlg = dtsWindow.FileSelectDialog(mode, ext, parent=parent, message=msg)
    except Exception as e:
        raise e
    #endregion ---------------------------------------------> Create wx.Dialog

    #region ---------------------------------------------------> Get File Path
    if dlg.ShowModal() == wx.ID_OK:
        if mode == 'openM':
            fileP = dlg.GetPaths()
        else:
            fileP = [dlg.GetPath()]
    else:
        fileP = []
    #endregion ------------------------------------------------> Get File Path

    dlg.Destroy()
    return fileP
#---


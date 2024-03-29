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


"""Methods for the result module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Optional

from pubsub import pub
import wx

from config.config import config as mConfig
from core   import method as cMethod
from core   import window as cWindow
from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def OnLoadUMSAPFile(
    fileP:Optional[Path]    = None,
    win:Optional[wx.Window] = None,
    ) -> bool:
    """Load an UMSAP File either from Read UMSAP File menu, LoadResults
        method in Tab or Update File Content menu.

        Parameters
        ----------
        fileP: Path or None
            If None, it is assumed the method is called from Read UMSAP File
            menu. Default is None.
        win: wx.Window or None
            If called from menu it is used to center the Select File wx.Dialog.
            Default is None.

        Return
        ------
        bool
    """
    return cMethod.OnGUIMethod(LoadUMSAPFile, fileP=fileP, win=win)
#---

def LoadUMSAPFile(
    fileP:Optional[Path]    = None,
    win:Optional[wx.Window] = None,
    ) -> bool:
    """Load an UMSAP File either from Read UMSAP File menu, LoadResults
        method in Tab or Update File Content menu.

        Parameters
        ----------
        fileP: Path or None
            If None, it is assumed the method is called from Read UMSAP File
            menu. Default is None.
        win: wx.Window or None
            If called from menu it is used to center the Select File wx.Dialog.
            Default is None.

        Return
        ------
        bool
    """
    # No Test
    #region --------------------------------------------> Get file from Dialog
    if fileP is None:
        dlg = cWindow.FileSelect(
            'openO',
            ext    = mConfig.core.elUMSAP,
            parent = win,
            msg    = mConfig.core.mFileSelUMSAP,
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
    if mConfig.res.winUMSAP.get(tFileP, '') != '':
        #------------------------------>
        mConfig.res.winUMSAP[tFileP].UpdateFileContent()
        #------------------------------>
        mConfig.res.winUMSAP[tFileP].Raise()
        #------------------------------>
        return True
    #------------------------------>
    mConfig.res.winUMSAP[tFileP] = resWindow.UMSAPControl(tFileP)
    #endregion -------------------------> Raise window if file is already open

    return True
#---
#endregion ----------------------------------------------------------> Methods

#region -------------------------------------------------> PubSub Subscription
pub.subscribe(OnLoadUMSAPFile,   mConfig.core.kwPubLoadUmsap)
#endregion ----------------------------------------------> PubSub Subscription

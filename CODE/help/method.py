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


"""Methods for the help module of the app"""


#region -------------------------------------------------------------> Imports
from typing import Literal, Optional

import requests

import wx

from config.config import config as mConfig
from core import window as cWindow
from core import check  as cCheck
from help import window as hWindow
#endregion ----------------------------------------------------------> Imports


LIT_Origin = Literal['menu', 'main']


#region -------------------------------------------------------------> Methods
def UpdateCheck(
    ori:LIT_Origin,
    win:Optional[wx.Window] = None,
    ) -> bool:
    """Check for updates for UMSAP.

        Parameters
        ----------
        ori: str
            Origin of the request, 'menu' or 'main'
        win : wx widget
            To center the result window in this widget

        Return
        ------
        bool

        Notes
        -----
        Always called from another thread.
    """
    #region ---------------------------------> Get web page text from Internet
    try:
        r = requests.get(mConfig.core.urlUpdate, timeout=10)
    except Exception as e:
        msg = 'Check for Updates failed. Please try again later.'
        wx.CallAfter(
            cWindow.DialogNotification,
            'errorU',
            msg        = msg,
            tException = e,
            parent     = win,
        )
        return False
    #endregion ------------------------------> Get web page text from Internet

    #region --------------------------------------------> Get Internet version
    if r.status_code == requests.codes.ok:                                      # pylint: disable=no-member
        #------------------------------>
        text = r.text.split('\n')
        #------------------------------>
        versionI = ''
        for i in text:
            if '<h1>UMSAP' in i:
                versionI = i
                break
        #------------------------------>
        versionI = versionI.split('UMSAP')[1].split('</h1>')[0]
        versionI = versionI.strip()
    else:
        msg = 'Check for Updates failed. Please try again later.'
        e = f'Web page returned code was: {r.status_code}.'
        wx.CallAfter(
            cWindow.DialogNotification,
            'errorU',
            msg        = msg,
            tException = e,
            parent     = win,
        )
        return False
    #endregion -----------------------------------------> Get Internet version

    #region -----------------------------------------------> Compare & message
    #------------------------------> Compare
    try:
        updateAvail = cCheck.VersionCompare(versionI, mConfig.core.version)[0]
    except Exception as e:
        msg = 'Check for Updates failed. Please try again later.'
        wx.CallAfter(
            cWindow.DialogNotification,
            'errorU',
            msg        = msg,
            tException = e,
            parent     = win,
        )
        return False
    #------------------------------> Message
    if updateAvail:
        wx.CallAfter(
            hWindow.DialogCheckUpdateResult, parent=win, checkRes=versionI)
    elif not updateAvail and ori == 'menu':
        wx.CallAfter(
            hWindow.DialogCheckUpdateResult, parent=win, checkRes=None)
    else:
        pass
    #endregion --------------------------------------------> Compare & message

    return True
#---
#endregion ----------------------------------------------------------> Methods

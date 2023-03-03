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
import _thread
import os
import webbrowser
from dataclasses import dataclass
from typing      import Literal, Optional

import requests
from pubsub import pub

import wx

from config.config import config as mConfig
from core import check  as cCheck
from core import window as cWindow
from help import window as hWindow
#endregion ----------------------------------------------------------> Imports


LIT_Origin = Literal['menu', 'main']


#region -------------------------------------------------------------> Classes
@dataclass
class Core():
    """User defined options for core"""
    #region ---------------------------------------------------------> Options
    checkUpdate:bool
    DPI:int
    imgFormat:str
    cZebra: str
    cRecProt:str
    cNatProt:str
    cFragment:list[str]
    cBarColor:dict
    #endregion ------------------------------------------------------> Options
#---


@dataclass
class CorrA():
    """User defined options for correlation analysis"""
    #region ---------------------------------------------------------> Options
    CMAP:dict
    corrMethod:str
    axisLabel:str
    showBar:bool
    #endregion ------------------------------------------------------> Options
#---


@dataclass
class Data():
    """User defined options for data preparation"""
    #region ---------------------------------------------------------> Options
    ceroT:str
    tranMethod:str
    normMethod:str
    impMethod:str
    shift:str
    width:str
    cBar:str
    cBarI:str
    cPDF:str
    #endregion ------------------------------------------------------> Options
#---


@dataclass
class UserConfig():
    """User defined configuration options"""
    core:Core
    corr:CorrA
    data:Data
#---
#endregion ----------------------------------------------------------> Classes


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
        win: wx.Window or None
            To center the result window in this widget. Default is None.

        Return
        ------
        bool

        Notes
        -----
        Always called from another thread.
    """
    # No Test
    #region ---------------------------------> Get web page text from Internet
    try:
        r = requests.get(mConfig.core.urlUpdate, timeout=10)
    except Exception as e:
        msg = 'Check for Updates failed. Please try again later.'
        wx.CallAfter(
            cWindow.Notification,
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
            cWindow.Notification,
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
            cWindow.Notification,
            'errorU',
            msg        = msg,
            tException = e,
            parent     = win,
        )
        return False
    #------------------------------> Message
    if updateAvail:
        wx.CallAfter(
            hWindow.CheckUpdateResult, parent=win, checkRes=versionI)
    elif not updateAvail and ori == 'menu':
        wx.CallAfter(
            hWindow.CheckUpdateResult, parent=win, checkRes=None)
    #endregion --------------------------------------------> Compare & message

    return True
#---


def About() -> bool:
    """Show the About UMSAP window.

        Returns
        -------
        bool
    """
    #region --------------------------------------------------->
    try:
        hWindow.WindowAbout()
    except Exception as e:
        msg = 'Failed to show the About UMSAP window.'
        cWindow.Notification('errorU', msg=msg, tException=e)
        return False
    #endregion ------------------------------------------------>

    return True
#---


def Manual() -> bool:
    """Show the About UMSAP window.

        Returns
        -------
        bool
    """
    #region -------------------------------------------------------->
    try:
        os.system(f'{mConfig.core.commOpen} {mConfig.core.fManual}')
    except Exception as e:
        msg = 'Failed to open the manual of UMSAP.'
        cWindow.Notification('errorU', msg=msg, tException=e)
        return False
    #endregion ----------------------------------------------------->

    return True
#---


def Tutorial() -> bool:
    """Show the tutorial.

        Returns
        -------
        bool
    """
    #region --------------------------------------------------->
    try:
        webbrowser.open_new(f'{mConfig.core.urlTutorial}/start')
    except Exception as e:
        msg = 'Failed to open the url with the tutorials for UMSAP.'
        cWindow.Notification('errorU', msg=msg, tException=e)
        return False
    #endregion ------------------------------------------------>

    return True
#---


def CheckUpdate() -> bool:
    """Check for updates.

        Parameters
        ----------
        event: wx.MenuEvent
            Information about the event.

        Returns
        -------
        bool
    """
    _thread.start_new_thread(UpdateCheck, ('menu',))
    return True
#---


def Preference() -> bool:
    """Set UMSAP preferences.

        Returns
        -------
        bool
    """
    #region -------------------------------------------------------->
    try:
        hWindow.Preference()
    except Exception as e:
        msg = 'Failed to show the Preferences window.'
        cWindow.Notification('errorU', msg=msg, tException=e)
        return False
    #endregion ----------------------------------------------------->

    return True
#---


def RGB2Hex(rgb:wx.Colour) -> str:
    """Convert wx.Colour to hex.

        Parameters
        ----------
        rgb: wx.Colour

        Returns
        -------
        str
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb.Red(), rgb.Green() , rgb.Blue())
#---


def RGB(rgb:wx.Colour) -> list[int]:
    """Get RGB as a list.

        Parameters
        ----------
        rgb: wx.Colour

        Returns
        -------
        list[int]
            [255,255,255]
    """
    return [rgb.Red(), rgb.Green(), rgb.Blue()]
#---
#endregion ----------------------------------------------------------> Methods


#region ------------------------------------------------> PubSub Subscriptions
pub.subscribe(About, mConfig.help.kwAbout)
pub.subscribe(Manual, mConfig.help.kwManual)
pub.subscribe(Preference, mConfig.help.kwPreference)
pub.subscribe(Tutorial, mConfig.help.kwTutorial)
pub.subscribe(CheckUpdate, mConfig.help.kwCheckUp)
#endregion ---------------------------------------------> PubSub Subscriptions

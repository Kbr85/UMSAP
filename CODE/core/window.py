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


"""Bases Windows for the app"""


#region -------------------------------------------------------------> Imports
from typing import Optional, Union, Literal

import wx

from config.config import config as mConfig
from core import method as cMethod
#endregion ----------------------------------------------------------> Imports


LIT_Notification = Literal['errorF', 'errorU', 'warning', 'success', 'question']


#region --------------------------------------------------------------> Frames
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default None
        # menuData : dict
        #     Data to build the Tool menu of the window. See structure in child
        #     class.

        Attributes
        ----------
        dKeyMethod : dict
            Keys are str and values classes or methods. Link menu items to
            windows methods.
    """
    #region -----------------------------------------------------> Class setup
    cSDeltaWin = mConfig.core.deltaWin
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent:Optional[wx.Window] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------> Def values if not given in child class
        self.cName    = getattr(self, 'cName',    mConfig.core.nwDef)
        self.cSWindow = getattr(self, 'cSWindow', mConfig.core.sWinFull)
        self.cTitle   = getattr(self, 'cTitle',   self.cName)
        #------------------------------>
        self.dKeyMethod = {}
        #------------------------------>
        super().__init__(
            parent, size=self.cSWindow, title=self.cTitle, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wStatBar = self.CreateStatusBar()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnClose(self, event: wx.CloseEvent) -> bool:                            # pylint: disable=unused-argument
        """Destroy window.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------> Reduce win number
        try:
            mConfig.core.winNumber[self.cName] -= 1
        except Exception:
            pass
        #endregion ----------------------------------------> Reduce win number

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Manage Methods
    def WinPos(self) -> dict:
        """Adjust win number and return information about the size of the
            window.

            Return
            ------
            dict
                Information about the size of the window and display and number
                of windows. See also data.method.GetDisplayInfo

            Notes
            -----
            Final position of the window on the display must be set in child
            class.
        """
        #region ---------------------------------------------------> Variables
        info = cMethod.GetDisplayInfo(self)
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Update N
        mConfig.core.winNumber[self.cName] = info['W']['N'] + 1
        #endregion -------------------------------------------------> Update N

        return info
    #---
    #endregion ------------------------------------------------> Manage Methods
#---
#endregion -----------------------------------------------------------> Frames


#region -------------------------------------------------------------> Dialogs
class Notification(wx.Dialog):
    """Show a custom notification dialog.

        Parameters
        ----------
        mode : str
            One of 'errorF', 'errorU', 'warning', 'success', 'question'
        msg : str
            General message to place below the Notification type. This cannot be
            copied by the user.
        tException : str, Exception or None
            The message and traceback to place in the wx.TextCtrl. This
            can be copied by the user. If str then only an error message will
            be placed in the wx.TextCtrl.
        parent : wx widget or None
            Parent of the dialog.
        button : int
            Kind of buttons to show. 1 is wx.OK else wx.OK|wx.CANCEL
        setText : bool
            Set wx.TextCtrl for message independently of the mode of the window.
            Default is False.
    """
    #region -----------------------------------------------------> Class setup
    style = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    error = ['errorF', 'errorU']
    img   = mConfig.core.fImgIcon
    #------------------------------>
    cTitle = 'UMSAP - Notification'
    #------------------------------>
    oNotification = {
        'errorF' : 'Fatal Error',
        'errorU' : 'Unexpected Error',
        'warning': 'Warning',
        'success': 'Success',
        'question':'Please answer the following question:',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        mode:LIT_Notification,
        msg:str                          = '',
        tException:Union[Exception, str] = '',
        parent:Optional[wx.Window]       = None,
        button:int                       = 1,
        setText:bool                     = False,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        if not msg and not tException:
            msg = "The message and exception received were both empty."
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=self.cTitle, style=self.style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wType = wx.StaticText(
            self,
            label = self.oNotification[mode],
        )
        self.wType.SetFont(self.wType.GetFont().MakeBold())

        if msg:
            self.wMsg = wx.StaticText(self, label=msg)
        else:
            self.wMsg = None

        if mode in self.error or setText:
            self.wError = wx.TextCtrl(
                self,
                size  = (565, 100),
                style = wx.TE_READONLY|wx.TE_MULTILINE,
            )
            self.SetErrorText(msg, tException)

        self.wImg = wx.StaticBitmap(
            self,
            bitmap = wx.Bitmap(str(self.img), wx.BITMAP_TYPE_PNG),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Create Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sTop   = wx.GridBagSizer(1,1)
        if button == 1:
            self.sBtn = self.CreateButtonSizer(wx.OK)
        else:
            self.sBtn = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        #------------------------------> Top Sizer
        self.sTop.Add(
            self.wImg,
            pos    = (0,0),
            flag   = wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
            border = 5,
            span   = (3,0),
        )
        self.sTop.Add(
            self.wType,
            pos    = (0,1),
            flag   = wx.ALIGN_LEFT|wx.ALL,
            border = 5
        )
        if self.wMsg is not None:
            self.sTop.Add(
                self.wMsg,
                pos    = (1,1),
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )

        if getattr(self, 'wError', False):
            #------------------------------>
            if self.wMsg is not None:
                pos = (2,1)
            else:
                pos = (1,1)
            #------------------------------>
            self.sTop.Add(
                self.wError,
                pos    = pos,
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )
        #--------------> Add Grow Col to Top Sizer
        self.sTop.AddGrowableCol(1,1)
        if getattr(self, 'wError', False):
            if self.wMsg is not None:
                self.sTop.AddGrowableRow(2,1)
            else:
                self.sTop.AddGrowableRow(1,1)
        #------------------------------> Main Sizer
        self.sSizer.Add(self.sTop, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        self.CenterOnParent()
        self.ShowModal()
        self.Destroy()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetErrorText(
        self,
        msg:str                          = '',
        tException:Union[Exception, str] = '',
        ) -> bool:
        """Set the error text in the wx.TextCtrl.

            Parameters
            ----------
            msg : str
                Error message.
            tException : Exception, str
                To display full traceback or a custom further details message.
        """
        #region -----------------------------------------------------> Message
        if msg:
            self.wError.AppendText(msg)
        #endregion --------------------------------------------------> Message

        #region ---------------------------------------------------> Exception
        if tException:
            if msg:
                self.wError.AppendText('\n\nFurther details:\n\n')
            else:
                pass
            if isinstance(tException, str):
                self.wError.AppendText(tException)
            else:
                self.wError.AppendText(cMethod.StrException(tException))
        #endregion ------------------------------------------------> Exception

        self.wError.SetInsertionPoint(0)
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Dialogs

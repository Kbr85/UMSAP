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
from pathlib import Path
from typing  import Optional, Union, Literal

import wx

from config.config import config as mConfig
from core import method as cMethod
from core import tab    as cTab
#endregion ----------------------------------------------------------> Imports


LIT_Notification = Literal['errorF', 'errorU', 'warning', 'success', 'question']
LIT_FSelect      = Literal['openO', 'openM', 'save']


#region --------------------------------------------------------------> Frames
class BaseWindow(wx.Frame):
    """Base window for UMSAP.

        Parameters
        ----------
        parent : wx.Window or None
            Parent of the window. Default None.

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
class BaseDialogOkCancel(wx.Dialog):
    """Basic wx.Dialog with a Cancel Ok Button.

        Parameters
        ----------
        title: str
            Title of the wx.Dialog.
        parent: wx.Window or None
            To center the dialog on the parent.
        size: wx.Size
            Size of the wx.Dialog.

        Attributes
        ----------
        sBtn: wx.Sizer
            Sizer with the Cancel, OK buttons.
        sSizer: wx.BoxSizer(wx.Vertical)
            Main Sizer of the wx.Dialog
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        title:str                  = '',
        parent:Optional[wx.Window] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cStyle = getattr(
            self, 'cStyle', wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER)
        self.cSize = getattr(self, 'cSize', (600, 900))
        #------------------------------>
        super().__init__(
            parent, title=title, style=self.cStyle, size=self.cSize)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.sBtn = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK,     id = wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id = wx.ID_CANCEL)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event:wx.CommandEvent) -> bool:                              # pylint: disable=unused-argument
        """Validate user information and close the window.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool

            Notes
            -----
            Basic implementation. Override as needed.
        """
        self.EndModal(1)
        self.Close()
        return True
    #---

    def OnCancel(self, event: wx.CommandEvent) -> bool:                         # pylint: disable=unused-argument
        """The macOs implementation has a bug here that does not discriminate
            between the Cancel and Ok button and always return self.EndModal(1).

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            True
        """
        self.EndModal(0)
        self.Close()
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class Progress(wx.Dialog):
    """Custom progress dialog.

        Parameters
        ----------
        parent: wx.Window
            Parent of the dialogue.
        title: str
            Title of the dialogue.
        count: int
            Number of steps for the wx.Gauge
        img: Path, str or None
            Image to show in the dialogue.
        style: wx style
            Style of the dialogue.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window],
        title:str,
        count:int,
        img:Path  = mConfig.core.fImgIcon,
        style:int = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=title, style=style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(self, label='')
        self.wG  = wx.Gauge(self, range=count, size=(400, 10))
        self.wStTime = wx.StaticText(self, label='')
        self.wStLabel = wx.StaticText(self, label='')
        self.wStLabel.SetFont(self.wStLabel.GetFont().MakeBold())
        self.wTcError = wx.TextCtrl(
            self,
            size  = (565, 100),
            style = wx.TE_READONLY|wx.TE_MULTILINE,
        )
        if img is not None:
            self.img = wx.StaticBitmap(
                self,
                bitmap = wx.Bitmap(str(img), wx.BITMAP_TYPE_PNG),
            )
        else:
            self.img = None
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sBtn = self.CreateButtonSizer(wx.OK)

        self.sStG = wx.BoxSizer(wx.VERTICAL)
        self.sStG.Add(self.wSt, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 5)
        self.sStG.Add(self.wG, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sStG.Add(self.wStTime, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)

        self.sProgress = wx.GridBagSizer(1,1)
        if self.img is not None:
            self.sProgress.Add(
                self.img,
                pos    = (0,0),
                flag   = wx.ALIGN_CENTER|wx.ALL,
                border = 5,
            )

        if self.img is not None:
            pos = (0,1)
        else:
            pos = (0,0)

        self.sProgress.Add(
            self.sStG,
            pos    = pos,
            flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5
        )
        self.sProgress.AddGrowableCol(pos[1],1)

        self.sError = wx.BoxSizer(wx.VERTICAL)
        self.sError.Add(self.wStLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sError.Add(self.wTcError, 1, wx.EXPAND|wx.ALL, 5)

        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(self.sProgress, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sError, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)

        self.sSizer.Hide(self.sError, recursive=True)
        self.sSizer.Hide(self.sBtn, recursive=True)

        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        self.CenterOnParent()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def UpdateStG(self, text:str, step:int=1) -> bool:
        """Update the step message and the gauge step.

            Parameters
            ----------
            text: str
                Text for the wx.StaticText.
            step: int
                Number of steps to increase the gauge.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update values
        self.wG.SetValue(self.wG.GetValue()+step)
        self.wSt.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def UpdateG(self, step:int=1) -> bool:
        """Update only the gauge of the dialogue.

            Parameters
            ----------
            step: int
                Number of steps to increase the gauge.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update values
        self.wG.SetValue(self.wG.GetValue()+step)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def UpdateSt(self, text:str) -> bool:
        """Update the step message.

            Parameters
            ----------
            text : str
                Text for the wx.StaticText
        """
        #region -----------------------------------------------> Update values
        self.wSt.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window

        return True
    #---

    def SuccessMessage(self, label:str, eTime:str='') -> bool:
        """Show a Success message.

            Parameters
            ----------
            label: str
                All done message.
            eTime: str
                Secondary message to display below the gauge. e.g. Elapsed time.
        """
        #region ------------------------------------------------------> Labels
        self.wSt.SetLabel(label)
        self.wSt.SetFont(self.wSt.GetFont().MakeBold())
        if eTime:
            self.wStTime.SetLabel(eTime)
        #endregion ---------------------------------------------------> Labels

        #region -------------------------------------------------------> Sizer
        #------------------------------> Center Success message
        self.sStG.GetItem(self.wSt).SetFlag(wx.ALIGN_CENTRE|wx.TOP|wx.LEFT)
        #------------------------------> Show buttons
        self.sSizer.Show(self.sBtn, recursive=True)
        #------------------------------> Layout & Show
        self.sSizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer

        return True
    #---

    def ErrorMessage(
        self,
        label:str,
        error:str                      = '',
        tException:Optional[Exception] = None,
        ) -> bool:
        """Show error message.

            Parameters
            ----------
            label: str
                Label to show.
            error: str
                Error message.
            tException : Exception or None
                Exception raised to offer full traceback.
        """
        #region -------------------------------------------------> Check input
        if not error and tException is None:
            msg = ("Both error and tException cannot be None")
            raise ValueError(msg)
        #endregion ----------------------------------------------> Check input

        #region ------------------------------------------------------> Labels
        self.wStLabel.SetLabel(label)
        #------------------------------>
        if error:
            self.wTcError.SetValue(error)
        #------------------------------>
        if tException is not None:
            if error:
                self.wTcError.AppendText('\n\nFurther details:\n')
            self.wTcError.AppendText(cMethod.StrException(tException))
        #------------------------------>
        self.wTcError.SetInsertionPoint(0)
        #endregion ---------------------------------------------------> Labels

        #region -------------------------------------------------------> Sizer
        self.sSizer.Show(self.sError, recursive=True)
        self.sSizer.Show(self.sBtn, recursive=True)

        self.sSizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


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
            msg: str
                Error message.
            tException: Exception, str
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


class ResControlExp(BaseDialogOkCancel):
    """Creates the dialog to type values for Results - Control Experiments.

        Parameters
        ----------
        parent: wx.Window
            This is the pane calling the dialog.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.core.ndResControlExp
    #------------------------------>
    cSize = (900, 580)
    #------------------------------>
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        if (iFile := parent.wIFile.wTc.GetValue())  == '': # type: ignore
            #------------------------------>
            dlg = FileSelect('openO', mConfig.core.elData, parent=parent)
            #------------------------------>
            if dlg.ShowModal() == wx.ID_OK:
                iFile = dlg.GetPath()
                parent.wIFile.wTc.SetValue(iFile) # type: ignore
                dlg.Destroy()
            else:
                dlg.Destroy()
                raise RuntimeError("No input file selected.")
        else:
            pass
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(title=self.cName, parent=mConfig.main.mainWin)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wConf = cTab.ResControlExp(self, iFile, parent)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------------> Sizer
        self.sSizer.Add(self.wConf, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ----------------------------------------------------> Sizer

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.wConf.wConf.OnOK():
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class FileSelect(wx.FileDialog):
    """Creates a dialog to select a file to read/save content from/into.

        Parameters
        ----------
        mode: str
            One of 'openO', 'openM', 'save'.
        wildcard: str
            File extensions, 'txt files (*.txt)|*.txt'.
        parent: wx.Window or None
            Parent of the window. If given modal window will be centered on it.
        message: str
            Message to show in the window.
        defPath: Path, str or None
            Default value for opening wx.FileDialog.

        Attributes
        ----------
        rTitle: dict
            Default titles for the dialog.
        rStyle: dict
            Style for the dialog.
    """
    #region -----------------------------------------------------> Class setup
    rTitle = {
        'openO': 'Select a file',
        'openM': 'Select files',
        'save' : 'Select a file',
    }

    rStyle = {
        'openO': wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW,
        'openM': wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW|wx.FD_MULTIPLE,
        'save' : wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        mode:LIT_FSelect,
        ext:str,
        parent:Optional['wx.Window']   = None,
        msg:str                        = '',
        defPath:Union[Path, str, None] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------------> Message
        msg = self.rTitle[mode] if msg is None else msg
        #endregion --------------------------------------------------> Message

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent,
            message    = msg,
            wildcard   = ext,
            style      = self.rStyle[mode],
            defaultDir = '' if defPath is None else str(defPath),
        )

        self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class DirSelect(wx.DirDialog):
    """Creates a dialog to select a folder.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the window. If given modal window will be centered on it.
        message: str
            Message to show in the window.
        defPath: Path or str
            Default value for opening wx.DirDialog.
    """
    #region -----------------------------------------------------> Class setup
    title = 'Select a folder'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window] = None,
        message:str                = '',
        defPath:Union[str,Path]    = '',
        ) -> None:
        """ """
        #region -------------------------------------------------> Check input
        msg = self.title if message else message
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent,
            message     = msg,
            defaultPath = str(defPath),
        )

        self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Dialogs

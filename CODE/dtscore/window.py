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
from pathlib import Path
from typing import Optional, Literal, Union

import wx

import config.config as config
import dtscore.data_method as dtsMethod
import dtscore.exception as dtsException
#endregion ----------------------------------------------------------> Imports


#region ----------------------------------------------------------> wx.Dialogs
class MessageDialog(wx.MessageDialog):
    """Show a message to the user.
    
        Parameters
        ----------
        mode : str
            One of 'errorF', 'errorU', 'success', 'warning'
        message : str
            Text of the message to show
        parent : wx widget or None
            Parent of the dialog. Used to center the dialog
        nothing : boolean or None
            To add a default last sentence to the message:
            (True) Nothing will be done
            (False) Nothing else will be done
            (None) ''
        
        Attributes
        ----------
        caption : dict
            Caption for the dialog
        style : dict
            Style for the dailog

        Raises
        ------
        InputError:
            When mode is not one of 'errorF', 'errorU' or 'success'
    """

    #region -----------------------------------------------------> Class setup
    caption = {
        'errorF' : 'Fatal Error',
        'errorU' : 'Unexpected Error',
        'warning': 'Warning',
        'success': 'All Done',
    }
    
    style = {
        'errorF' : wx.OK|wx.CENTRE|wx.ICON_ERROR,
        'errorU' : wx.OK|wx.CENTRE|wx.ICON_ERROR,
        'warning': wx.OK|wx.CENTRE|wx.ICON_WARNING,
        'success': wx.OK|wx.CENTRE|wx.ICON_INFORMATION,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, mode, message, parent=None, nothing=True):
        """ """
        #region -------------------------------------------------> Check input
        if mode not in config.oMsgType:
            raise dtsException.InputError(config.mMsgTypeIE[mode])
        else:
            pass
        #endregion ----------------------------------------------> Check input

        #region -----------------------------------------------------> Message
        if mode == 'success' or nothing is None:
            msg = message
        elif nothing:
            msg = message + '\nNothing will be done.'
        else:
            msg = message + '\nNothing else will be done.'
        #endregion --------------------------------------------------> Message
        
        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent, 
            message = msg,
            caption = self.caption[mode],
            style   = self.style[mode],
        )

        self.CenterOnParent()
        #endregion ------------------------------------------> Create & Center

        #region ----------------------------------------------> Show & Destroy
        self.ShowModal()
        self.Destroy()
        #endregion -------------------------------------------> Show & Destroy
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ProgressDialog(wx.Dialog):
    """Custom progress dialog

        Parameters
        ----------
        parent : wx Widget
            Parent of the dialogue
        title : str
            Title of the dialogue
        count : int
            Number of steps for the wx.Gauge
        img : Path, str or None
            Image to show in the dialogue.
        style : wx style
            Style of the dialogue

        Attributes
        ----------
        st: wx.StaticText
            To show current step or success message
        g : wx.Gauge
            To show progress
        stTime : wx.StaticTime
            For Elapsed time message
        stLabel : wx.StaticText
            Error title
        stError : wx.StaticText
            Error description
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window], title: str, count: int, 
        img: Path=config.fImgIcon,
        style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=title, style=style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.st = wx.StaticText(self, label='')
        self.g  = wx.Gauge(self, range=count, size=(400, 10))
        self.stTime = wx.StaticText(self, label='')
        self.stLabel = wx.StaticText(self, label='')
        self.stLabel.SetFont(self.stLabel.GetFont().MakeBold())
        self.tcError = wx.TextCtrl(
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
        self.sizerBtn = self.CreateButtonSizer(wx.OK)

        self.sizerStG = wx.BoxSizer(wx.VERTICAL)
        self.sizerStG.Add(self.st, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 5)
        self.sizerStG.Add(self.g, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sizerStG.Add(self.stTime, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5)

        self.sizerProgress = wx.GridBagSizer(1,1)
        if self.img is not None:
            self.sizerProgress.Add(
                self.img,
                pos    = (0,0),
                flag   = wx.ALIGN_CENTER|wx.ALL,
                border = 5,
            )
        else:
            pass

        if self.img is not None:
            pos = (0,1)
        else:
            pos = (0,0)
        self.sizerProgress.Add(
            self.sizerStG,
            pos    = pos,
            flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5
        )
        self.sizerProgress.AddGrowableCol(pos[1],1)

        self.sizerError = wx.BoxSizer(wx.VERTICAL)
        self.sizerError.Add(self.stLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sizerError.Add(self.tcError, 1, wx.EXPAND|wx.ALL, 5)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.sizerProgress, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.Sizer.Add(self.sizerError, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 25)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)
        
        self.Sizer.Hide(self.sizerError, recursive=True)
        self.Sizer.Hide(self.sizerBtn, recursive=True)

        self.SetSizer(self.Sizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        self.CenterOnParent()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def UpdateStG(self, text:str, step: Optional[int]=None) -> Literal[True]:
        """Update the step message and the gauge step. If step is None increase 
            gauge in one unit.
    
            Parameters
            ----------
            text : str
                Text for the wx.StaticText
            step : int or None
                Number of steps to increase the gauge

        """
        #region -----------------------------------------------> Update values
        gIncr = 1 if step is None else step
        self.g.SetValue(self.g.GetValue()+gIncr)

        self.st.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window
        
        return True
    #---

    def UpdateG(self, step: Optional[int]=None) -> Literal[True]:
        """Update only the gauge of the dialogue
    
            Parameters
            ----------
            step: int or None
                Number of steps to increase the gauge
        """
        #region -----------------------------------------------> Update values
        gIncr = 1 if step is None else step
        self.g.SetValue(self.g.GetValue()+gIncr)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window
        
        return True
    #---

    def UpdateSt(self, text: str) -> Literal[True]:
        """Update the step message
    
            Parameters
            ----------
            text : str
                Text for the wx.StaticText
        """
        #region -----------------------------------------------> Update values
        self.st.SetLabel(text)
        #endregion --------------------------------------------> Update values

        #region -----------------------------------------------> Update window
        self.Refresh()
        self.Update()
        #endregion --------------------------------------------> Update window
        
        return True
    #---
    
    def SuccessMessage(
        self, label: str, eTime: Optional[str]=None
        ) -> Literal[True]:
        """Show a Success message
    
            Parameters
            ----------
            label : str
                All done message
            eTime : str or None
                Secondary mensage to display below the gauge. e.g. Elapsed time
        """
        #region ------------------------------------------------------> Labels
        self.st.SetLabel(label)
        self.st.SetFont(self.st.GetFont().MakeBold())
        if eTime is not None:
            self.stTime.SetLabel(eTime)
        else:
            pass
        #endregion ---------------------------------------------------> Labels
        
        #region -------------------------------------------------------> Sizer
        #------------------------------> Center Success message
        self.sizerStG.GetItem(self.st).SetFlag(wx.ALIGN_CENTRE|wx.TOP|wx.LEFT)
        #------------------------------> Show buttons
        self.Sizer.Show(self.sizerBtn, recursive=True)
        #------------------------------> Layout & Show
        self.Sizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer
        
        return True
    #---

    def ErrorMessage(
        self, label: str, error: Optional[str]=None, 
        tException: Optional[Exception]=None,
        ) -> Literal[True]:
        """Show error message
    
            Parameters
            ----------
            label : str
                Label to show
            error : str or None
                Error message
            tException : Exception or None
                Exception raised to offer full traceback
        """
        #region -------------------------------------------------> Check input
        if error is None and tException is None:
            msg = ("Both error and tException cannot be None")
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input

        #region ------------------------------------------------------> Labels
        self.stLabel.SetLabel(label)
        #--> 
        if error is not None:
            self.tcError.SetValue(error)
        else:
            pass
        #--> 
        if tException is None:
            pass
        else:
            if error is not None:
                self.tcError.AppendText('\n\nFurther details:\n')
            else:
                pass
            self.tcError.AppendText(dtsMethod.StrException(tException))
        #--> 
        self.tcError.SetInsertionPoint(0)
        #endregion ---------------------------------------------------> Labels
        
        #region -------------------------------------------------------> Sizer
        self.Sizer.Show(self.sizerError, recursive=True)
        self.Sizer.Show(self.sizerBtn, recursive=True)

        self.Sizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        #endregion ----------------------------------------------------> Sizer
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class NotificationDialog(wx.Dialog):
    """Show a custom notification dialog.

        Parameters
        ----------
        mode : str
            One of 'errorF', 'errorU', 'warning', 'success', 'question'
        msg : str or None
            General message to place below the Notification type. This cannot be
            copied by the user.
        tException : str, Exception or None
            The message and traceback to place in the wx.TextCtrl. This 
            can be copied by the user. If str then only an error message will 
            be placed in the wx.TextCtrl.
        parent : wx widget or None
            Parent of the dialog.
        img : Path, str or None
            Path to an image to show in the dialog.
        button : int
            Kind of buttons to show. 1 is wx.OK else wx.OK|wx.CANCEL
        title : str
            Title of the dialog
        setText : bool
            Set wx.TextCtrl for message independently of the mode of the window.
            Default is False.

        Attributes
        ----------
        style : wx.Style
            Style of the dialog
        error : list of str
            List of error modes
        stType: wx.StaticText
            Notification type
        stMsg : wx.StaticText
            Message below Notification text
        tcError: wx.TextCtrl
            For full details about the notification
        img : wx.StaticBitmap
            Image to show in the dialog

        Raises
        ------
        InputError:
            - When mode not in dtsConfig.varOpt['NotificationDialog']['Mode']
    """
    #region -----------------------------------------------------> Class setup
    style = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    error = ['errorF', 'errorU']
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, 
        mode: Literal['errorF', 'errorU', 'warning', 'success', 'question'],
        msg: Optional[str]=None, tException: Union[Exception, str, None]=None, 
        parent: Optional[wx.Window]=None, img: Path=config.fImgIcon, 
        button: int=1, title: str='UMSAP - Notification', setText=False,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=title, style=self.style)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.stType = wx.StaticText(
            self, 
            label = config.oNotification[mode],
        )
        self.stType.SetFont(self.stType.GetFont().MakeBold())

        if msg is not None:
            self.stMsg = wx.StaticText(self, label=msg)
        else:
            self.stMsg = None

        if mode in self.error or setText:
            self.tcError = wx.TextCtrl(
                self, 
                size  = (565, 100),
                style = wx.TE_READONLY|wx.TE_MULTILINE,
            )
            self.SetErrorText(msg, tException)
        else:
            self.tcError = None

        if img is not None:
            self.img = wx.StaticBitmap(
                self,
                bitmap = wx.Bitmap(str(img), wx.BITMAP_TYPE_PNG),
            )
        else:
            self.img = None
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if button == 1:
            self.sizerBtn = self.CreateButtonSizer(wx.OK)
        else:
            self.sizerBtn = self.CreateButtonSizer(wx.OK|wx.CANCEL)

        self.sizerTop = wx.GridBagSizer(1,1)
        if self.img is not None:
            self.sizerTop.Add(
                self.img,
                pos    = (0,0),
                flag   = wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                border = 5,
                span   = (3,0),
            )
        else:
            self.sizerTop.Add(
                (0,0),
                pos    = (0,0),
                flag   = wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                border = 5,
                span   = (3,0),
            )
        
        self.sizerTop.Add(
            self.stType,
            pos    = (0,1),
            flag   = wx.ALIGN_LEFT|wx.ALL,
            border = 5
        )

        if self.stMsg is not None:
            self.sizerTop.Add(
                self.stMsg,
                pos    = (1,1),
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )
        else:
            pass

        if self.tcError is not None:
            #-->
            if self.stMsg is not None:
                pos = (2,1)
            else:
                pos = (1,1)
            #-->
            self.sizerTop.Add(
                self.tcError,
                pos    = pos,
                flag   = wx.EXPAND|wx.ALL,
                border = 5
            )
        else:
            pass

        self.sizerTop.AddGrowableCol(1,1)
        if self.tcError is not None:
            if self.stMsg is not None:
                self.sizerTop.AddGrowableRow(2,1)
            else:
                self.sizerTop.AddGrowableRow(1,1)
        else:
            pass

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.sizerTop, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 25)
        
        self.SetSizer(self.Sizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        self.CenterOnParent()
        self.ShowModal()
        self.Destroy()
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetErrorText(
        self, msg: Optional[str]=None, 
        tException: Union[Exception, str, None]=None
        ) -> Literal[True]:
        """Set the error text in the wx.TextCtrl
        
            Parameters
            ----------
            msg : str or None
                Error message
            tException : Exception, str or None
                To display full traceback or a custom further details message.
            
            Raise
            -----
            - InputError:
                When msg and tException are both None
            
        """
        #region -------------------------------------------------> Check input
        if msg is None and tException is None:
            msg = "Both msg and tException cannot be None."
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input
        
        #region -----------------------------------------------------> Message
        if msg is not None:
            self.tcError.AppendText(msg)
        else:
            pass
        #endregion --------------------------------------------------> Message
        
        #region ---------------------------------------------------> Exception  
        if tException is None:
            pass
        else:
            if msg is not None:
                self.tcError.AppendText('\n\nFurther details:\n\n')
            else:
                pass
            if isinstance(tException, str):
                self.tcError.AppendText(
                    dtsMethod.StrException(
                        tException, tRepr=False, trace=False,
                ))
            else:
                self.tcError.AppendText(dtsMethod.StrException(tException))
        #endregion ------------------------------------------------> Exception  
        
        self.tcError.SetInsertionPoint(0)	
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion -------------------------------------------------------> wx.Dialogs


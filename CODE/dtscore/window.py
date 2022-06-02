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


class NPlots(wx.Panel):
    """The panel will contain N plots distributed in a wx.FlexGridSizer.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.Panel holding the plots.
        tKeys : list of str
            Keys for a dict holding a reference to the plots
        nCol : int
            Number of columns in the wx.FlexGridSizer holding the plots.
            Number of needed rows will be automatically calculated.
        name : str
            To id the panel. Default is NPlot.
        dpi : int
            DPI value for the matplot plots.
        statusbar : wx.StatusBar or None
            StatusBar to display information about the plots.
        
        Attributes
        ----------
        dPlot : dict
            Keys are tKeys and values dtsWidget.MatPlotPanel
        name : str
            Name of the panel holding the plots.
        nCol : int
            Number of columns in the sizer
        nRow: int
            Number of rows in the sizer.

        Raises
        ------
        InputError:
            - When tKeys holds values that cannot be turned into str by str().
            - When nCol is not an integer greater than 0.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent:wx.Window, tKeys: list[str], nCol: int, name: str='NPlot',
        dpi: Optional[int]=None, statusbar: Optional[wx.StatusBar]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.nCol = nCol
        self.nRow = ceil(len(tKeys)/nCol)
        self.name = name
        
        super().__init__(parent, name=name)
        #endregion --------------------------------------------> Initial Setup
        
        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.Sizer = wx.FlexGridSizer(self.nRow, self.nCol, 1,1)
        #------------------------------> 
        for k in range(0, self.nCol):
            self.Sizer.AddGrowableCol(k,1)
        for k in range(0, self.nRow):
            self.Sizer.AddGrowableRow(k,1)
        #------------------------------> 
        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------------> Widgets
        self.dPlot = {}
        for k in tKeys:
            #------------------------------> Create
            self.dPlot[k] = dtsWidget.MatPlotPanel(
                self, dpi=dpi, statusbar=statusbar)
            #------------------------------> Add to sizer
            self.Sizer.Add(self.dPlot[k], 1, wx.EXPAND|wx.ALL, 5)
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---
#endregion ------------------------------------------------> Frames and panels


#region ----------------------------------------------------------> wx.Dialogs
class OkCancel(wx.Dialog):
    """Basic wx.Dialog with a Cancel Ok Button

        Parameters
        ----------
        

        Attributes
        ----------
        

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, title: str='', parent: Optional[wx.Window]=None, 
        size: wx.Size=wx.DefaultSize,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cStyle = getattr(
            self, 'cStyle', wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER)
        #------------------------------> 
        super().__init__(parent, title=title, style=self.cStyle, size=size)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.sBtn = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position

        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
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
    
    def OnCancel(self, event: wx.CommandEvent) -> Literal[True]:
        """The macOs implementation has a bug here that does not discriminate
            between the Cancel and Ok button and always return self.EndModal(1).
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
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

#------------------------------> 
class FileSelectDialog(wx.FileDialog):
    """Creates a dialog to select a file to read/save content from/into

        Parameters
        ----------
        mode : str
            One of 'openO', 'openM', 'save'. The same values are used in
            dat4s_core.widget.wx_widget.ButtonTextCtrlFF.mode
        wildcard : str
            File extensions, 'txt files (*.txt)|*.txt'
        parent : wx widget or None
            Parent of the window. If given modal window will be centered on it.
        message : str or None
            Message to show in the window
        defPath: Path, str or None
            Default value for opening wx.FileDialog.
         
        Attributes
        ----------
        rTitle : dict
            Default titles for the dialog
        rStyle : dict
            Style for the dialog
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
        self, mode: Literal['openO', 'openM', 'save'], 
        wildcard: str, parent: Optional['wx.Window']=None, 
        message: Optional[str]=None, 
        defPath: Union[Path, str, None]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------------> Message
        msg = self.rTitle[mode] if message is None else message
        #endregion --------------------------------------------------> Message

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent, 
            message    = msg,
            wildcard   = wildcard,
            style      = self.rStyle[mode],
            defaultDir = '' if defPath is None else str(defPath),
        )

        self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class DirSelectDialog(wx.DirDialog):
    """Creates a dialog to select a folder

        Parameters
        ----------
        parent : wx widget or None
            Parent of the window. If given modal window will be centered on it
        message : str or None
            Message to show in the window
        defPath: Path, str or None
            Default value for opnening wx.FileDialog.
    """

    #region -----------------------------------------------------> Class setup
    title = 'Select a folder'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: Optional[wx.Window]=None, message: Optional[str]=None,
        defPath: Union[str,Path,None]=None,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check input
        msg = self.title if message is None else message
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------> Create & Center
        super().__init__(
            parent, 
            message     = msg,
            defaultPath = '' if defPath is None else str(defPath),
        )

        self.CenterOnParent()
         #endregion ------------------------------------------> Create & Center
    #---
    #endregion -----------------------------------------------> Instance setup
#---


#------------------------------> 
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
            - When mode not in config.varOpt['NotificationDialog']['Mode']
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


class ListSelect(OkCancel):
    """Select values from a list of options

        Parameters
        ----------
        color: str
            Alternating color for the wx.ListCtrl
        parent: wx.Window
            Parent of the window
        rightDelete: bool
            Delete content of the right wx.ListCtrl with a right click
        tBtnLabel: str
            Label for the Add wx.Button
        tColLabel: list[str]
            Label for the name of the columns in the wx.ListCtrl. It is assumed
            both wx.ListCtrl have the same column labels.
        tColSize: list[int]
            Size of the columns in the wx.ListCtrl. It is assumed both 
            wx.ListCtrl have the same size.
        title: str
            Title of the window
        tOptions: list[list[str]]
            Available options.
        tSelOptions: list[list[str]]
            Already selected options. Optional
        tStLabel: list[str]
            Label to show on top of the wx.ListCtrl.
    """
    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, tOptions: list[list[str]], tColLabel: list[str], 
        tColSize: list[int], tSelOptions: list[list[str]]= [],
        title: Optional[str]=None, tStLabel:Optional[list[str]]=None, 
        tBtnLabel: Optional[str]=None, parent: Optional[wx.Window]=None, 
        color: str=config.color['Zebra'], rightDelete: bool=True, 
        style=wx.LC_REPORT|wx.LC_VIRTUAL,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        if tStLabel is not None:
            self.cStLabel = tStLabel
        else:
            self.cStLabel = ['Available options', 'Selected options']
        if tBtnLabel is not None:
            self.cBtnLabel = tBtnLabel
        else:
            self.cBtnLabel = 'Add options'
        if title is not None:
            pass
        else:
            title = 'Select options'
        #------------------------------> 
        super().__init__(parent=parent, title=title)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.StaticText
        self.wStListI = wx.StaticText(self, label=self.cStLabel[0])
        self.wStListO = wx.StaticText(self, label=self.cStLabel[1])
        #------------------------------> dtsWidget.ListZebra
        self.wLCtrlI = dtsWidget.ListZebra(self, 
            color           = color,
            colLabel        = tColLabel,
            colSize         = tColSize,
            copyFullContent = True,
            style           = style,
            
        )
        self.wLCtrlI.SetNewData(tOptions)
        
        self.wLCtrlO = dtsWidget.ListZebra(self, 
            color           = color,
            colLabel        = tColLabel,
            colSize         = tColSize,
            canPaste        = True,
            canCut          = True,
            copyFullContent = True,
            # style           = style,
        )
        for r in tSelOptions:
            self.wLCtrlO.Append(r)
        #------------------------------> wx.Button
        self.wAddCol = wx.Button(self, label=self.cBtnLabel)
        self.wAddCol.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), dir = wx.RIGHT)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sList = wx.FlexGridSizer(2,3,5,5)
        self.sList.Add(self.wStListI, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.AddStretchSpacer(1)
        self.sList.Add(self.wStListO, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.Add(self.wLCtrlI,  0, wx.EXPAND|wx.ALL,       5)
        self.sList.Add(self.wAddCol,  0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sList.Add(self.wLCtrlO,  0, wx.EXPAND|wx.ALL,       5)
        self.sList.AddGrowableCol(0,1)
        self.sList.AddGrowableCol(2,1)
        self.sList.AddGrowableRow(1,1)
        
        self.sSizer.Add(self.sList, 1, wx.EXPAND|wx.ALL,      5)
        self.sSizer.Add(self.sBtn,  0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers
        
        #region ----------------------------------------------------> Tooltips
        self.wStListI.SetToolTip(
            f"Selected rows can be copied ({config.copyShortCut}+C) but "
            f"the list cannot be modified.")
        self.wStListO.SetToolTip(
            f"New rows can be pasted ({config.copyShortCut}+V) after the "
            f"last selected element and existing ones cut/deleted "
            f"({config.copyShortCut}+X) or copied "
            f"({config.copyShortCut}+C)." )
        self.wAddCol.SetToolTip(f'Add selected rows in the left list to the '
            f'right list. New columns will be added after the last selected '
            f'row in the right list. Duplicate columns are discarded.')
        #endregion -------------------------------------------------> Tooltips


        #region --------------------------------------------------------> Bind
        self.wAddCol.Bind(wx.EVT_BUTTON, self.OnAdd)
        if rightDelete:
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wLCtrlO.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
        else:
            pass
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Validate
        if self.wLCtrlO.GetItemCount() > 0:
            self.EndModal(1)
            self.Close()
        else:
            return False
        #endregion -------------------------------------------------> Validate
        
        return True
    #---
    
    
    def OnAdd(self, event: Union[wx.Event, str]) -> bool:
        """Add columns to analyse using the button.
    
            Parameters
            ----------
            event : wx.Event
                Event information
                
            Returns
            -------
            bool
        """
        self.wLCtrlI.OnCopy('')
        self.wLCtrlO.OnPaste('')
        
        return True
    #---
    
    def OnRightDelete(self, event: Union[wx.Event, str]) -> bool:
        """Add columns to analyse using the button.
    
            Parameters
            ----------
            event : wx.Event
                Event information
                
            Returns
            -------
            bool
        """
        self.wLCtrlO.DeleteAllItems()
        
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class MultipleCheckBox(OkCancel):
    """Present multiple choices as checkboxes.

        Parameters
        ----------
        title : str
            Title for the wx.Dialog
        items : dict
            Keys are the name of the wx.CheckBox and values the label.
            Keys are also used to return the checked elements.
        nCol : int
            wx.CheckBox will be distributed in a grid of nCol and as many as 
            needed rows.
        label : str
            Label for the wx.StaticBox
        multiChoice : bool
            More than one wx.Checkbox can be selected (True) or not (False).
        parent : wx.Window
            Parent of the wx.Dialog

        Attributes
        ----------
        rDict: dict
            Keys are 0 to N where N is the number of elements in items, nCol,
            label and multiChoice.
            {
                0: {
                    stBox  : wx.StaticBox,
                    checkB : [wx.CheckBox],
                    sFlex  : wx.FlexGridSizer,
                    sStBox : wx.StaticBoxSizer,
                },
            }
        checked : dict
            Keys are int 0 to N and values the names of the checked wx.CheckBox 
            after pressing the OK button. The names are the keys in the 
            corresponding item group.
            
        Notes
        -----
        At least one option must be selected for the OK button to close the 
        wx.Dialog.

    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, title: str, items: list[dict[str, str]], nCol: list[int], 
        label: list[str]=['Options'], multiChoice: list[bool]=[False], 
        parent: Optional[wx.Window]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> 
        self.rDict = {}
        self.checked = {}
        #------------------------------> 
        super().__init__(title=title, parent=parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        try:
            for k,v in enumerate(label):
                self.rDict[k] = {}
                #------------------------------> wx.StaticBox
                self.rDict[k]['stBox'] = wx.StaticBox(self, label=v)
                #------------------------------> wx.CheckBox
                self.rDict[k]['checkB'] = []
                for j,i in items[k].items():
                    self.rDict[k]['checkB'].append(
                        wx.CheckBox(self.rDict[k]['stBox'], 
                                    label=i, 
                                    name=f'{j}-{k}'))
                #------------------------------> wx.Sizer
                self.rDict[k]['sFlex'] =(
                    wx.FlexGridSizer(ceil(len(items[k])/nCol[k]), nCol[k], 1,1))
                self.rDict[k]['sStBox'] = wx.StaticBoxSizer(
                    self.rDict[k]['stBox'], orient=wx.VERTICAL)
                #------------------------------> Bind
                if not multiChoice[k]:
                    [x.Bind(wx.EVT_CHECKBOX, self.OnCheck) for x in self.rDict[k]['checkB']]
                else:
                    pass   
        except IndexError:
            msg = ('items, nCol, label and multiChoice must have the same '
                   'number of elements.')
            raise dtsException.InputError(msg)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        for k,v in self.rDict.items():
            #------------------------------> Add check to Flex
            for c in v['checkB']:
                v['sFlex'].Add(c, 0, wx.ALIGN_LEFT|wx.ALL, 7)
            #------------------------------> Add Flex to StaticBox
            v['sStBox'].Add(v['sFlex'], 0, wx.ALIGN_CENTER|wx.ALL, 5)
            #------------------------------> Add to Sizer
            self.sSizer.Add(v['sStBox'], 0, wx.EXPAND|wx.ALL, 5)
        
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(self.sSizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind

        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnCheck(self, event:wx.CommandEvent):
        """Deselect all other seleced options.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Deselect
        if event.IsChecked():
            #------------------------------> 
            tCheck = event.GetEventObject()
            group = int(tCheck.GetName().split('-')[1])
            #------------------------------> 
            [k.SetValue(False) for k in self.rDict[group]['checkB']]
            #------------------------------> 
            tCheck.SetValue(True)
        else:
            pass
        #endregion -------------------------------------------------> Deselect
        
        return True
    #---
    
    def OnOK(self, event: wx.CommandEvent) -> Literal[True]:
        """Validate user information and close the window.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region ----------------------------------------------------> Validate
        #------------------------------> 
        for k in self.rDict:
            for c in self.rDict[k]['checkB']:
                if c.IsChecked():
                    self.checked[k] = c.GetName().split('-')[0]
                else:
                    pass
        #------------------------------> 
        if self.checked and len(self.checked) == len(self.rDict):
            self.EndModal(1)
            self.Close()
        else:
            pass
        #endregion -------------------------------------------------> Validate
        
        return True
    #---
    
    def GetChoice(self) -> dict:
        """Get the selected checkbox
    
            Returns
            -------
            dict
                The keys are 0 to N and values the items corresponding to the 
                checked wx.CheckBox in each group.
        """
        return self.checked
    #---
    #endregion ------------------------------------------------> Class methods
#---


class UserInput1Text(wx.Dialog):
    """Present a modal window with one wx.TextCtrl for user input.

        Parameters
        ----------
        title : str
            Title of the dialog.
        label : str
            Label for the wx.StaticText in the dialog.
        hint : str
            Hint for the wx.TextCtrl in the dialog.
        parent : wx.Window or None
            To center the dialog on the parent.
        validator : wx.Validator
            The validator is expected to comply with the return of validators in
            dts.Validator
        size : wx.Size
            Size of the window. Default is (100, 70)
        
        Attributes
        ----------
        input : wx.StaticTextCtrl
        
        Notes
        -----
        A valid input must be given for the wx.Dialog to be closed after
        pressing the OK button.
    """
    #region -----------------------------------------------------> Class setup
    style = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, title: str, label: str, hint: str, parent: wx.Window=None,
        validator: wx.Validator=wx.DefaultValidator, size: wx.Size=(420, 120),
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, title=title, style=self.style, size=size)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.input = dtsWidget.StaticTextCtrl(
            self,
            stLabel   = label,
            tcHint    = hint,
            validator = validator,
        )
        
        self.sizerBtn = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        self.Sizer.Add(
            self.input.st, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(
            self.input.tc, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(self.sizerBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> Literal[True]:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region ----------------------------------------------------> Validate
        if self.input.tc.GetValidator().Validate()[0]:
            self.EndModal(1)
            self.Close()
        else:
            self.input.tc.SetValue('')
        #endregion -------------------------------------------------> Validate
        
        return True
    #---
    
    def OnCancel(self, event: wx.CommandEvent) -> Literal[True]:
        """The macOs implementation has a bug here that does not discriminate
            between the Cancel and Ok button and always return self.EndModal(1).
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        self.EndModal(0)
        self.Close()
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class UserInputText(OkCancel):
    """Present a modal window with N wx.TextCtrl for user input.

        Parameters
        ----------
        title : str
            Title of the dialog.
        label : list[str]
            Labels for the wx.StaticText in the dialog.
        hint : list[str]
            Hint for the wx.TextCtrl in the dialog.
        parent : wx.Window or None
            To center the dialog on the parent.
        validator : list[wx.Validator]
            The validator is expected to comply with the return of validators in
            dts.Validator
        size : wx.Size
            Size of the window. Default is (100, 70)
        
        Attributes
        ----------
        rInput : list[dtsWidget.StaticTextCtrl]
        
        Raise
        -----
        dtsException.InputError:
            - When label, hint, validator do not have the same length
        
        Notes
        -----
        A valid input must be given for the wx.Dialog to be closed after
        pressing the OK button.
        The number of dtsWidget.StaticTextCtrl to be created is taken from
        the label parameter.
    """
    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, title: str, label: list[str], hint: list[str], 
        validator: list[wx.Validator], parent: wx.Window=None, 
        values: list[str]=[]
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent=parent, title=title)
        #------------------------------> 
        self.rInput = []
        if values:
            self.rValues = values
        else:
            self.rValues = ['' for x in label]
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        for k,v in enumerate(label):
            self.rInput.append(dtsWidget.StaticTextCtrl(
                self,
                stLabel   = v,
                tcHint    = hint[k],
                validator = validator[k],
            ))
            self.rInput[k].tc.SetValue(self.rValues[k])
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        for k in self.rInput:
            self.Sizer.Add(k.st, 0, wx.ALIGN_LEFT|wx.UP|wx.LEFT|wx.RIGHT, 5)
            self.Sizer.Add(k.tc, 0, wx.EXPAND|wx.DOWN|wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        self.SetSizer(self.Sizer)
        self.Fit()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind

        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.CenterOnParent()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Validate user information and close the window
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Variables
        wrong = []
        #endregion ------------------------------------------------> Variables

        
        #region ----------------------------------------------------> Validate
        for k in self.rInput:
            if k.tc.GetValidator().Validate()[0]:
                pass
            else:
                wrong.append(k)
                k.tc.SetValue('')
        #endregion -------------------------------------------------> Validate
        
        #region ---------------------------------------------------> Return
        if not wrong:
            self.EndModal(1)
            self.Close()
            return True
        else:
            return False
        #endregion ------------------------------------------------> Return
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion -------------------------------------------------------> wx.Dialogs


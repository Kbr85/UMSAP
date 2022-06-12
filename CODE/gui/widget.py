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


""" Widgets of the application"""


#region -------------------------------------------------------------> Imports
import _thread
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Union

import webbrowser
import wx

import config.config as mConfig
import data.generator as mGenerator
# import dtscore.validator as dtsValidator
import gui.window as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def StatusBarUpdate(statusbar: wx.StatusBar, msg: str, field: int=0) -> bool:
    """Updates the text in a field of a statusbar.

        Parameters
        ----------
        statusbar : wx.StatusBar
        msg : str
            New text to show
        field : int
            Field in the statusbar. Default is 0.
    """
    statusbar.SetStatusText(msg, i=field)
    return True
#---


def ClearInput(parent: wx.Window) -> bool:
    """Set all user input to '' and delete all items in wx.ListCtrl

        Parameters
        ----------
        parent : wx.Window
            All child widgets of parent will be clear.
    """
    #region -----------------------------------------------------------> Clear
    for child in mGenerator.FindChildren(parent):
        if isinstance(child, wx.TextCtrl) or isinstance(child, wx.ComboBox):
            child.SetValue("")
        elif isinstance(child, wx.CheckBox):
            child.SetValue(False)
        elif  isinstance(child, wx.ListCtrl):
            child.DeleteAllItems()
        else:
            pass
    #endregion --------------------------------------------------------> Clear

    return True
#---
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
class StaticBoxes():
    """Creates the three main static boxes Files, User values and Columns.

        Parameters
        ----------
        parent: wx widget
            Parent of the widgets.
        rightDelete : Boolean
            Delete user input with right click (True) or not.
        labelF : str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelD : str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelV : str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelC : str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.

        Attributes
        ----------
        Depending on the values of labelF, labelV and labelC, the corresponding
        attributes may not be created

        wSbFile : wx.StaticBox
            StaticBox to contain the input/output file information
        wSbData : wx.StaticBox
            StaticBox to contain the data preparation information.
        wSbValue : wx.StaticBox
            StaticBox to contain the user-defined values
        wSbColumn : wx.StaticBox
            StaticBox to contain the column numbers in the input files
        sSbFile : wx.StaticBoxSizer
            StaticBoxSizer for sbFile
        sSbData : wx.StaticBoxSizer
            StaticBoxSizer for sbData
        sSbValue : wx.StaticBoxSizer
            StaticBoxSizer for sbValue
        sSbColumn : wx.StaticBoxSizer
            StaticBoxSizer for sbColumn
        sSbFileWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbFile
        sSbDataWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbData
        sSbValueWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbValue
        sSbColumnWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbColumn
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, rightDelete: bool=True,
        labelF: str='Files',
        labelD: str='Data Preparation',
        labelV: str='User-defined Values',
        labelC: str="Column Numbers",
        ) -> None:
        """"""
        #region ----------------------------------------------> File & Folders
        if labelF:
            #------------------------------> 
            self.wSbFile = wx.StaticBox(parent, label=labelF)
            #------------------------------> 
            self.sSbFile    = wx.StaticBoxSizer(self.wSbFile, wx.VERTICAL)
            self.sSbFileWid = wx.GridBagSizer(1, 1)
            self.sSbFile.Add(self.sSbFileWid, border=2,flag=wx.EXPAND|wx.ALL)
            #------------------------------> 
            if rightDelete:
                self.wSbFile.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbFile.SetToolTip(mConfig.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion -------------------------------------------> File & Folders

        #region --------------------------------------------> Data Preparation
        if labelD:
            #------------------------------> 
            self.wSbData = wx.StaticBox(parent, label=labelD)
            #------------------------------> 
            self.sSbData    = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
            self.sSbDataWid = wx.GridBagSizer(1, 1)
            self.sSbData.Add(self.sSbDataWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------> 
            if rightDelete:
                self.wSbData.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbData.SetToolTip(mConfig.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion -----------------------------------------> Data Preparation

        #region ------------------------------------------------------> Values
        if labelV:
            #------------------------------> 
            self.wSbValue  = wx.StaticBox(parent, label=labelV)
            #------------------------------> 
            self.sSbValue    = wx.StaticBoxSizer(self.wSbValue, wx.VERTICAL)
            self.sSbValueWid = wx.GridBagSizer(1, 1)
            self.sSbValue.Add(self.sSbValueWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------> 
            if rightDelete:
                self.wSbValue.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbValue.SetToolTip(mConfig.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion ---------------------------------------------------> Values

        #region -----------------------------------------------------> Columns
        if labelC:
            #------------------------------> 
            self.wSbColumn = wx.StaticBox(parent, label=labelC)
            #------------------------------> 
            self.sSbColumn = wx.StaticBoxSizer(self.wSbColumn, wx.VERTICAL)
            self.sSbColumnWid = wx.GridBagSizer(1, 1)
            self.sSbColumn.Add(
                self.sSbColumnWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------> 
            if rightDelete:
                self.wSbColumn.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbColumn.SetToolTip(mConfig.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion --------------------------------------------------> Columns
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnRightDelete(self, event: wx.MouseEvent) -> bool:
        """Reset content of all children of the widgets calling the event.

            Parameters
            ----------
            event : wx.Event
                Information about the event
        """
        return ClearInput(event.GetEventObject())
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class ButtonClearAll():
    """wx.Button to set the values of all child widget of a parent to an empty
        value. All elements of wx.ListCtrl children will be deleted.

        Parameters
        ----------
        parent : wx.Window
            Parent of the widget to properly placed the button and get the child
            whose values will be clear.
        label : str
            Label of the button
        tooltip : str or None
            Tooltip for the wx.Button. Default is None.
        delParent: wx.Window or None 
            If not None, then child widgets will be taken from here instead of 
            parent.

        Attributes
        ----------
        wBtnClearAll : wx.Button
            Button to clear all user input
        rDelParent: wx.Window
            This is the widget whose children values will be set to ''
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, delParent: Optional[wx.Window]=None, 
        label: str='Clear All', tooltip: str='',
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.rDelParent = parent if delParent is None else delParent
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.wBtnClearAll = wx.Button(parent, label=label)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        if tooltip:
            self.wBtnClearAll.SetToolTip(tooltip)
        else:
            pass
        #endregion --------------------------------------------------> Tooltip

        #region --------------------------------------------------------> Bind
        self.wBtnClearAll.Bind(wx.EVT_BUTTON, self.OnClear)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnClear(self, event: wx.CommandEvent) -> bool:
        """Set the values of all child widgets of delParent to '' and delete
            all items of wx.ListCtrl.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.
        """
        ClearInput(self.rDelParent)
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class ButtonRun():
    """Creates the Button to start an analysis. It contains the methods for the
        individual steps of the analysis that are performed in another thread.

        Parameters
        ----------
        parent: wx Widget
            Parent of the button
        label : str
            Label of the button. Default is Run.
        tooltip : str or None
            Tooltip for the wx.Button. Default is None.

        Attributes
        ----------
        rDeltaT : str
            Time used by the analysis.
        wBtnRun : wx.Button
            The button

        Methods
        -------
        OnRun(event)
            Start new thread to run the analysis
        Run(test)
            Run the steps of the analysis
        CheckInput()
            Check user input. Override as needed.
        PrepareRun()
            Set variables and prepare data for analysis. Override as needed.
        ReadInputFiles()
            Read the input files. Override as needed.
        RunAnalysis()
            Run the actual analysis. Override as needed.
        WriteOutput()
            Write output files. Override as needed.
        LoadResults()
            Load results. Override as needed.
        EndRun()
            Restart GUI and variables. Override as needed.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, label: str='Run', tooltip: str='',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rDeltaT = ''
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnRun = wx.Button(parent, label=label)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        if tooltip:
            self.wBtnRun.SetToolTip(tooltip)
        else:
            pass
        #endregion --------------------------------------------------> Tooltip

        #region --------------------------------------------------------> Bind
        self.wBtnRun.Bind(wx.EVT_BUTTON, self.OnRun)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnRun(self, event: wx.CommandEvent) -> bool:
        """Start new thread to run the analysis. Override as needed.

            Parameter
            ---------
            event : wx.Event
                Receive the button event
        """
        #region ------------------------------------------------------> Thread
        _thread.start_new_thread(self.Run, ('test',))
        #endregion ---------------------------------------------------> Thread

        return True
    #---
    #endregion ------------------------------------------------> Event methods

    #region ---------------------------------------------------> Class methods
    def Run(self, *args) -> bool:
        """Run the analysis's steps

            Parameters
            ----------
            Just needed by _thread.start_new_thread

            Notes
            -----
            Messages to the status bar of the app can be set in the individual
            step methods.
        """
        start = datetime.now()
        #region -------------------------------------------------> Check input
        if self.CheckInput():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ----------------------------------------------> Check input

        #region -------------------------------------------------> Prepare run
        if self.PrepareRun():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ----------------------------------------------> Prepare run

        #region ---------------------------------------------> Read input file
        if self.ReadInputFiles():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ------------------------------------------> Read input file

        #region ------------------------------------------------> Run analysis
        if self.RunAnalysis():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ---------------------------------------------> Run analysis

        #region ------------------------------------------------> Write output
        if self.WriteOutput():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ---------------------------------------------> Write output

        #region ------------------------------------------------> Load results
        if self.LoadResults():
            pass
        else:
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ---------------------------------------------> Load results

        #region --------------------------------------------------> Delta Time
        end = datetime.now()
        self.rDeltaT = datetime.utcfromtimestamp(
            (end-start).total_seconds()
        ).strftime("%H:%M:%S")
        #endregion -----------------------------------------------> Delta Time

        #region -------------------------------------------------> Restart GUI
        wx.CallAfter(self.RunEnd)
        return True
        #endregion ----------------------------------------------> Restart GUI
    #---

    def CheckInput(self) -> bool:
        """Check user input. Override as needed """
        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis. Override as needed """
        return True
    #---

    def ReadInputFiles(self) -> bool:
        """Read the input files. Override as needed"""
        return True
    #---

    def RunAnalysis(self) -> bool:
        """Run the actual analysis. Override as needed """
        return True
    #---

    def WriteOutput(self) -> bool:
        """Write output. Override as needed """
        return True
    #---

    def LoadResults(self) -> bool:
        """Load results. Override as needed """
        return True
    #---

    def RunEnd(self) -> bool:
        """Restart GUI and needed variables. This is a minimal implementation. 
            Override as needed 
        """
        #region -------------------------------------------> Restart variables
        self.deltaT = None
        #endregion ----------------------------------------> Restart variables

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ButtonOnlineHelp():
    """Creates the Help button. The button leads to an online resource.

        Parameters
        ----------
        parent : wx Widget
            Parent of the button
        url : str
            URL to show
        label : str
            Label of the button. Default is Help
        tooltip : str or None
            Tooltip for the wx.Button. Default is None.

        Attributes
        ----------
        url : str
            URL to show
        btnHelp : wx.Button
            Help button
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, url: str, label: str='Help', tooltip: str='',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rUrl = url
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnHelp = wx.Button(parent, label=label)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        if tooltip is not None:
            self.wBtnHelp.SetToolTip(tooltip)
        else:
            pass
        #endregion --------------------------------------------------> Tooltip

        #region --------------------------------------------------------> Bind
        self.wBtnHelp.Bind(wx.EVT_BUTTON, self.OnHelp)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnHelp(self, event: wx.CommandEvent) -> bool:
        """Leads to self.url

            Parameters
            ----------
            event : wx.CommandEvent
                Information about the event.
        """
        #region ----------------------------------------------------> Open web
        try:
            webbrowser.open_new_tab(self.rUrl)
        except Exception as e:
            raise e        
        #endregion -------------------------------------------------> Open web

        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class ButtonOnlineHelpClearAllRun(ButtonRun, ButtonClearAll, ButtonOnlineHelp):
    """Group of three buttons at the bottom of a pane to show online help, 
        clear the input in the pane and to perform the main action of the panel.
        
        Parameters
        ----------
        parent : wx widget
            Parent of the widgets
        url : str
            URL for the help button
        labelH : str
            Label for the Help button
        tooltipH : str or None
            Tooltip for the help wx.Button. Default is None.
        labelC : str
            Label for the Clear button
        tooltipC : str or None
            Tooltip for the Clear wx.Button. Default is None.
        delParent: wx widget or None
            This is the widgets whose children values will be set to ''. If None
            then the child will be searched in parent
        labelR : str
            Label for the Run button
        tooltipR : str or None
            Tooltip for the Run wx.Button. Default is None.
        setSizer : Boolean
            Set (True) or not the sizer for the buttons

        Attributes
        ----------
        sBtnSizer: wx.FlexGridSizer
            Sizer for the buttons. It is created only if setSizer is True.

        Notes
        -----
        If setSizer is True, buttons are arranged horizontally in a 
        wx.FlexGridSizer
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, url: str, labelH: str='Help', tooltipH: str='',
        labelC: str='Clear All', tooltipC: str='', 
        delParent: Optional[wx.Window]=None, labelR: str='Start Analysis',
        tooltipR: str='', setSizer: bool=True,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial setup
        ButtonOnlineHelp.__init__(
            self, parent, url, label=labelH, tooltip=tooltipH)
        
        ButtonClearAll.__init__(
            self, parent, delParent=delParent, label=labelC, tooltip=tooltipC)
        
        ButtonRun.__init__(self, parent, label=labelR, tooltip=tooltipR)
        #endregion --------------------------------------------> Initial setup

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.sBtnSizer = wx.FlexGridSizer(1, 3, 1, 1)
            self.sBtnSizer.Add(
                self.wBtnHelp,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
            self.sBtnSizer.Add(
                self.wBtnClearAll,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
            self.sBtnSizer.Add(
                self.wBtnRun,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
        else:
            self.btnSizer = None
        #endregion ---------------------------------------------------> Sizers
    #endregion -----------------------------------------------> Instance setup
#---


class ButtonTextCtrlFF():
    """Creates a wx.Button and wx.TextCtrl to select input/output files.

        Parameters
        ----------
        parent : wx widget or None
            Parent of the widgets
        afterBtn: Callable
            Method to execute after self.OnBtn finishes.
        btnLabel : str
            Label for the button. Default is 'Button'
        btnTooltip : str or None
            Tooltip for the wx.Button. Default is None.
        ext: str
            File extension. Default is '' to select folder.
        mode: str
            One of 'openO', 'openM', 'save', 'folder'.
        ownCopyCut : boolean
            Use own implementation of Copy (Ctrl/Cmd C) and Cut (Ctrl/Cmd X) 
            methods. Useful to delete wx.TextCtrl when style is wx.TE_READONLY.
        setSizer : boolean
            Set (True) or not (False) a sizer for the widgets.
        tcHint: str
            Hint for the wx.TextCtrl. Default is ''.
        tcSize : wx.Size
            Size of the wx.TextCtrl. Default is (300, 22).
        tcStyle : wx style
            Default is wx.TE_PROCESS_ENTER|wx.TE_READONLY.
        validator : wx.Validator or None
            To validate input for wx.TexCtrl.

        Attributes
        ----------
        wBtn  : wx.Button
        wTc   : wx.TextCtrl
        sSizer: wx.BoxSizer. Only set if setSizer is True.

        Shortcuts
        ---------
        If ownCopyCut is True:
            Ctrl/Cmd + C Copy
            Ctrl/Cmd + X Cut

        Notes
        -----
        The wx.TextCtrl is placed to the right of the wx.Button if a sizer is
        created. 

        ownCopyCut is meant to bypass the restrictions when the style of the 
        wx.TextCtrl is wx.TE_READONLY
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, 
        parent: wx.Window,
        ext: str = '',
        setSizer: bool=False, 
        btnLabel: str='Button', 
        btnTooltip: str='', 
        tcStyle=wx.TE_PROCESS_ENTER|wx.TE_READONLY,
        tcHint: str='', 
        tcSize: Union[wx.Size,tuple[int, int]]=(300, 22),
        validator: Optional[wx.Validator]=None, 
        ownCopyCut: bool=False,
        mode: mConfig.litFFSelect='openO',
        afterBtn: Optional[Callable]=None,
        ) -> None:
        """	"""
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------> 
        self.rMode: mConfig.litFFSelect = mode
        self.rExt      = ext
        self.rAfterBtn = afterBtn
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtn = wx.Button(
            parent = parent,
            label  = btnLabel,
        )
        self.wTc = wx.TextCtrl(
            parent    = parent,
            value     = "",
            style     = tcStyle,
            size      = tcSize,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        self.wTc.SetHint(tcHint)
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        if btnTooltip is not None:
            self.wBtn.SetToolTip(btnTooltip)
        else:
            pass
        #endregion -------------------------------------------------> Tooltips

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.sSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.sSizer.Add(self.wBtn, 0, wx.EXPAND|wx.ALL, 5)
            self.sSizer.Add(self.wTc, 1, wx.EXPAND|wx.ALL, 5)
        else:
            self.sSizer = None
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wBtn.Bind(wx.EVT_BUTTON, self.OnBtn)
        #------------------------------> 
        if ownCopyCut:
            #------------------------------> 
            accel = {
                'Copy' : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('C'), wx.NewId()),
                'Cut'  : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('X'), wx.NewId()),
            }
            #------------------------------> 
            self.wTc.Bind(wx.EVT_MENU, self.OnCopy, id=accel['Copy'].GetCommand())
            self.wTc.Bind(wx.EVT_MENU, self.OnCut,  id=accel['Cut'].GetCommand())
            #------------------------------> 
            self.wTc.SetAcceleratorTable(
                wx.AcceleratorTable([x for x in accel.values()])
            )
        else:
            pass
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnBtn(self, event: wx.CommandEvent) -> bool:
        """Action to perform when button is clicked.

            Parameter
            ---------
            event : wx.CommandEvent
                Event information.
        """
        #region ------------------------------------------> Select file/folder
        if self.rMode != 'folder':
            dlg = mWindow.DialogFileSelect(
                self.rMode, self.rExt, parent=self.cParent)
        else:
            dlg = mWindow.DialogDirSelect(parent=self.cParent)
        #------------------------------> 
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.wTc.SetValue(path)
        else:
            dlg.Destroy()
            return False
        #endregion ---------------------------------------> Select file/folder

        #region ---------------------------------------------> After selection
        if self.rAfterBtn is not None:
            try:
                self.rAfterBtn(Path(path))
            except Exception as e:
                raise e
        #endregion ------------------------------------------> After selection

        dlg.Destroy()
        return True
    #---

    def OnCopy(self, event: wx.Event) -> bool:
        """Copy wx.TextCtrl content.

            Parameters
            ----------
            event: wx.Event
                Information about the event.
        """
        #region ----------------------------------------------------> Get data
        data = self.wTc.GetValue()
        dataObj = wx.TextDataObject(data)
        #endregion -------------------------------------------------> Get data

        #region -------------------------------------------> Copy to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        else:
            mWindow.DialogNotification(
                'warning', 
                msg    = mConfig.mCopyFailedW,
                parent = self.cParent,
            )
            return False
        #endregion ----------------------------------------> Copy to clipboard

        return True
    #---

    def OnCut(self, event: 'wx.Event') -> bool:
        """Cut wx.TextCtrl content

            Parameters
            ----------
            event: wx.Event
                Information about the event
        """
        #region -------------------------------------------> Copy to clipboard
        try:
            self.OnCopy(event)
        except Exception:
            return False
        #endregion ----------------------------------------> Copy to clipboard

        #region -------------------------------------------------------> Clear
        self.wTc.SetValue('')
        #endregion ----------------------------------------------------> Clear

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes



# class ResControl():
#     """Creates the Results - Control experiment widgets.

#         Parameters
#         ----------
#         cParent : wx widget
#             Parent of the widgets
#     """
#     #region -----------------------------------------------------> Class setup
#     cLResControl     = config.lStResultCtrl
#     cLBtnTypeResCtrl = config.lBtnTypeResCtrl
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, cParent: wx.Window) -> None:
#         """ """
#         #region -----------------------------------------------------> Widgets
#         self.wTcResults = wx.TextCtrl(
#             parent    = cParent,
#             style     = wx.TE_READONLY,
#             value     = "",
#             size      = config.sTc,
#             validator = dtsValidator.IsNotEmpty(),
#         )

#         self.wStResults = wx.StaticText(
#             parent = cParent,
#             label  = self.cLResControl,
#             style  = wx.ALIGN_RIGHT
#         )

#         self.wBtnResultsW = wx.Button(
#             parent = cParent,
#             label  = self.cLBtnTypeResCtrl,
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region ------------------------------------------------------> Sizers
#         #------------------------------> 
#         self.sRes = wx.GridBagSizer(1,1)
#         #------------------------------> 
#         self.sRes.Add(
#             self.wStResults,
#             pos    = (0,0),
#             flag   = wx.ALIGN_LEFT|wx.ALL,
#             border = 5,
#             span   = (0,2),
#         )
#         self.sRes.Add(
#             self.wBtnResultsW,
#             pos    = (1,0),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             border = 5
#         )
#         self.sRes.Add(
#             self.wTcResults,
#             pos    = (1,1),
#             flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             border = 5,
#         )
#         #------------------------------> 
#         self.sRes.AddGrowableCol(1,1)
#         #endregion ---------------------------------------------------> Sizers
        
#         #region -----------------------------------------------------> Tooltip
#         self.wBtnResultsW.SetToolTip(
#             'Type the column numbers in a helper window.')
#         self.wStResults.SetToolTip(
#             f'Set the column numbers containing the control and experiment '
#             f'results.')
#         #endregion --------------------------------------------------> Tooltip
        
#         #region --------------------------------------------------------> Bind
#         self.wBtnResultsW.Bind(wx.EVT_BUTTON, self.OnResW)
#         #endregion -----------------------------------------------------> Bind
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #------------------------------> Class method
#     #region ---------------------------------------------------> Event methods
#     def OnResW(self, event: wx.CommandEvent) -> bool:
#         """ Open the window to write the results columns. 
        
#             Parameters
#             ----------
#             event: wx.Event
#                 Information about the event
            
#             Returns
#             -------
#             bool
#         """
#         #------------------------------> 
#         with window.ResControlExp(self) as dlg:
#             dlg.ShowModal()
#         #------------------------------> 
#         return True
#     #---
#     #endregion ------------------------------------------------> Event methods
# #---



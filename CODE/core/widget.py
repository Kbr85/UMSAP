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


"""Core Widgets of the app"""


#region -------------------------------------------------------------> Imports
import _thread
import json
import math
from datetime import datetime
from pathlib  import Path
from typing   import Optional, Callable, Union, Literal

import webbrowser

import wx
import wx.lib.mixins.listctrl as listmix

import matplotlib as mpl
from matplotlib                        import patches
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from config.config import config as mConfig
from core import generator as cGenerator
from core import validator as cValidator
from core import window    as cWindow
#endregion ----------------------------------------------------------> Imports


LIT_FFSelect = Literal['openO', 'openM', 'save', 'folder']


#region -------------------------------------------------------------> Methods
def StatusBarUpdate(statusbar:wx.StatusBar, msg:str, field:int=0) -> bool:
    """Updates the text in a field of a statusbar.

        Parameters
        ----------
        statusbar: wx.StatusBar
        msg: str
            New text to show.
        field: int
            Field in the statusbar. Default is 0.
    """
    statusbar.SetStatusText(msg, i=field)
    return True
#---


def ClearInput(parent:wx.Window) -> bool:
    """Set all user input to '' and delete all items in wx.ListCtrl.

        Parameters
        ----------
        parent: wx.Window
            All child widgets of parent will be clear.
    """
    #region -----------------------------------------------------------> Clear
    for child in cGenerator.FindChildren(parent):
        if isinstance(child, wx.TextCtrl) or isinstance(child, wx.ComboBox):
            child.SetValue("")
        elif isinstance(child, wx.CheckBox):
            child.SetValue(False)
        elif isinstance(child, wx.ListCtrl):
            child.DeleteAllItems()
    #endregion --------------------------------------------------------> Clear

    return True
#---
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
class StaticBoxes():
    """Creates the three main static boxes Files, User values and Columns.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.
        rightDelete: Boolean
            Delete user input with right click (True) or not.
        labelF: str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelD: str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelV: str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.
        labelC: str
            Label of the wx.StaticBox. If empty the wx.StaticBox and associated
            sizers will not be created.

        Attributes
        ----------
        Depending on the values of labelF, labelV and labelC, the corresponding
        attributes may not be created.

        wSbFile: wx.StaticBox
            StaticBox to contain the input/output file information.
        wSbData: wx.StaticBox
            StaticBox to contain the data preparation information.
        wSbValue: wx.StaticBox
            StaticBox to contain the user-defined values.
        wSbColumn: wx.StaticBox
            StaticBox to contain the column numbers in the input files.
        sSbFile: wx.StaticBoxSizer
            StaticBoxSizer for sbFile.
        sSbData: wx.StaticBoxSizer
            StaticBoxSizer for sbData.
        sSbValue: wx.StaticBoxSizer
            StaticBoxSizer for sbValue.
        sSbColumn: wx.StaticBoxSizer
            StaticBoxSizer for sbColumn.
        sSbFileWid: wx.GridBagSizer
            FlexGridSizer for widgets in sbFile.
        sSbDataWid: wx.GridBagSizer
            FlexGridSizer for widgets in sbData.
        sSbValueWid: wx.GridBagSizer
            FlexGridSizer for widgets in sbValue.
        sSbColumnWid: wx.GridBagSizer
            FlexGridSizer for widgets in sbColumn.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        rightDelete:bool  = True,
        labelF:str        = 'Files',
        labelD:str        = 'Data Preparation',
        labelV:str        = 'User-defined Values',
        labelC:str        = "Column Numbers",
        ) -> None:
        """"""
        #region ----------------------------------------------> File & Folders
        if labelF:
            self.wSbFile = wx.StaticBox(parent, label=labelF)
            #------------------------------>
            self.sSbFile    = wx.StaticBoxSizer(self.wSbFile, wx.VERTICAL)
            self.sSbFileWid = wx.GridBagSizer(1, 1)
            self.sSbFile.Add(self.sSbFileWid, border=2,flag=wx.EXPAND|wx.ALL)
            #------------------------------>
            if rightDelete:
                self.wSbFile.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbFile.SetToolTip(mConfig.core.ttSectionRightClick)
        #endregion -------------------------------------------> File & Folders

        #region --------------------------------------------> Data Preparation
        if labelD:
            self.wSbData = wx.StaticBox(parent, label=labelD)
            #------------------------------>
            self.sSbData    = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
            self.sSbDataWid = wx.GridBagSizer(1, 1)
            self.sSbData.Add(self.sSbDataWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------>
            if rightDelete:
                self.wSbData.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbData.SetToolTip(mConfig.core.ttSectionRightClick)
        #endregion -----------------------------------------> Data Preparation

        #region ------------------------------------------------------> Values
        if labelV:
            self.wSbValue  = wx.StaticBox(parent, label=labelV)
            #------------------------------>
            self.sSbValue    = wx.StaticBoxSizer(self.wSbValue, wx.VERTICAL)
            self.sSbValueWid = wx.GridBagSizer(1, 1)
            self.sSbValue.Add(self.sSbValueWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------>
            if rightDelete:
                self.wSbValue.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbValue.SetToolTip(mConfig.core.ttSectionRightClick)
        #endregion ---------------------------------------------------> Values

        #region -----------------------------------------------------> Columns
        if labelC:
            self.wSbColumn = wx.StaticBox(parent, label=labelC)
            #------------------------------>
            self.sSbColumn = wx.StaticBoxSizer(self.wSbColumn, wx.VERTICAL)
            self.sSbColumnWid = wx.GridBagSizer(1, 1)
            self.sSbColumn.Add(
                self.sSbColumnWid, border=2, flag=wx.EXPAND|wx.ALL)
            #------------------------------>
            if rightDelete:
                self.wSbColumn.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.wSbColumn.SetToolTip(mConfig.core.ttSectionRightClick)
        #endregion --------------------------------------------------> Columns
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnRightDelete(self, event:wx.MouseEvent) -> bool:
        """Reset content of all children of the widgets calling the event.

            Parameters
            ----------
            event: wx.MouseEvent
                Information about the event
        """
        return ClearInput(event.GetEventObject())
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class StaticTextCtrl():
    """Creates a wx.StaticText and a wx.TextCtrl.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the widgets.
        setSizer: boolean
            Set (True) or not (False) a sizer for the widgets.
        stLabel: str
            Label for the wx.StaticText. Default is 'Text'.
        stTooltip: str or None
            Tooltip for the wx.StaticText. Default is None.
        tcSize: wx.Size
            Size of the wx.TextCtrl. Default is (300, 22).
        tcStyle: wxPython style
            Style of the wx.TextCtrl.
        tcHint: str
            Hint for the wx.TextCtrl. Default is ''.
        tcName: str
            Name for the wx.TextCtrl.
        validator: wx.Validator or None
            To validate input for wx.TexCtrl.

        Attributes
        ----------
        wSt: wx.StaticText
            The wx.StaticText.
        wTc: wx.TextCtrl
            The wx.TextCtrl.
        Sizer: wx.BoxSizer or None

        Notes
        -----
        The wx.TextCtrl is placed to the right of the wx.StaticText if a sizer
        is created.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        setSizer:bool                          = False,
        stLabel:str                            = 'Text',
        stTooltip:str                          = '',
        tcSize:Union[wx.Size, tuple[int, int]] = (300, 22),
        tcHint:str                             = '',
        tcStyle:int                            =  0,
        tcName:str                             = '',
        validator:Optional[wx.Validator]       = None,
        ) -> None:
        """"""
        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(
            parent = parent,
            label  = stLabel,
        )
        #-------------->
        self.wTc = wx.TextCtrl(
            parent    = parent,
            name      = tcName,
            value     = "",
            size      = tcSize,
            style     = tcStyle,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        self.wTc.SetHint(tcHint)
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------> Tooltips
        if stTooltip:
            self.wSt.SetToolTip(stTooltip)
        #endregion ------------------------------------------------> Tooltips

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.wSt, 0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.Sizer.Add(self.wTc, 1, wx.EXPAND|wx.ALL, 5)
        else:
            self.Sizer = None
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class StaticTextColor():
    """Creates a wx.StaticText and a wx.ColourPickerCtrl.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the widgets.
        setSizer: boolean
            Set (True) or not (False) a sizer for the widgets.
        stLabel: str
            Label for the wx.StaticText. Default is 'Text'.
        stTooltip: str or None
            Tooltip for the wx.StaticText. Default is None.
        cSize: wx.Size
            Size of the wx.ColourPickerCtrl. Default is (30, 30).
        cStyle: wxPython style
            Style of the wx.ColourPickerCtrl.
        cColor: wx.Colour
            Initial color of the wx.ColourPickerCtrl.

        Attributes
        ----------
        wSt: wx.StaticText
            The wx.StaticText.
        wC: wx.ColourPickerCtrl
            The wx.ColourPickerCtrl.
        Sizer: wx.BoxSizer or None

        Notes
        -----
        The wx.ColourPickerCtrl is placed to the right of the wx.StaticText if
        a sizer is created.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        setSizer:bool                          = False,
        stLabel:str                            = 'Text',
        stTooltip:str                          = '',
        cSize:Union[wx.Size, tuple[int, int]]  = (30, 30),
        cStyle:int                             = 0,
        cColor:Union[wx.Colour,str]            = 'white',
        ) -> None:
        """"""
        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(parent=parent, label=stLabel)
        #-------------->
        self.wC = wx.ColourPickerCtrl(
            parent    = parent,
            size      = cSize,
            style     = cStyle,
            colour    = cColor,
        )
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------> Tooltips
        if stTooltip:
            self.wSt.SetToolTip(stTooltip)
        #endregion ------------------------------------------------> Tooltips

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.wSt, 0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.Sizer.Add(self.wC,  0, wx.ALIGN_CENTER|wx.ALL, 5)
        else:
            self.Sizer = None
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class StaticTextComboBox():
    """Creates a wx.StaticText and wx.ComboBox.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.
        label: str
            Text for the wx.StaticText.
        tooltip: str
            Tooltip for the wx.StaticText. Default is ''.
        choices: list of str
            Options for the wx.ComboBox.
        validator: wx.Validator or None
            Validator for the wx.ComboBox. Default is wx.DefaultValidator.
        setSizer: boolean
            Set (True) or not (False) a sizer for the widgets.
        styleCB: wx.Style
            Style of the wx.ComboBox.
        value: str
            Initial selected value for wx.ComboBox.

        Attributes
        ----------
        wSt: wx.StaticText
            Label for the wx.ComboBox.
        wCb: wx.ComboBox
            wx.ComboBox.
        Sizer: wx.BoxSizer or None

        Notes
        -----
        The wx.ComboBox is placed to the right of the wx.StaticText if a sizer
        is created.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        label:str,
        choices:list[str],
        value:str                        = '',
        tooltip:str                      = '',
        styleCB:int                      = wx.CB_READONLY,
        setSizer:bool                    = False,
        validator:Optional[wx.Validator] = None,
        ) -> None:
        """ """
        #region -----------------------------------------------------> Widgets
        self.wSt = wx.StaticText(parent, label=label)
        self.wSt.SetToolTip(tooltip)
        #-------------->
        self.wCb = wx.ComboBox(parent,
            value     = value,
            choices   = choices,
            style     = styleCB,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.wSt, 0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.Sizer.Add(self.wCb, 1, wx.EXPAND|wx.ALL, 5)
        else:
            self.Sizer = None
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ButtonClearAll():
    """wx.Button to set the values of all child widget of a parent to an empty
        value. All elements of wx.ListCtrl children will be deleted.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widget to properly placed the button and get the child
            whose values will be clear.
        label: str
            Label of the button.
        tooltip: str
            Tooltip for the wx.Button. Default is ''.
        delParent: wx.Window or None
            If not None, then child widgets will be taken from here instead of
            parent.

        Attributes
        ----------
        wBtnClearAll: wx.Button
            Button to clear all user input.
        rDelParent: wx.Window
            This is the widget whose children values will be set to ''.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        delParent:Optional[wx.Window] = None,
        label:str                     = 'Clear All',
        tooltip:str                   = '',
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.rDelParent = parent if delParent is None else delParent
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.wBtnClearAll = wx.Button(parent, label=label)
        self.wBtnClearAll.SetToolTip(tooltip)
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.wBtnClearAll.Bind(wx.EVT_BUTTON, self.OnClear)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnClear(self, event:wx.CommandEvent) -> bool:                           # pylint: disable=unused-argument
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
    #endregion ------------------------------------------------> Event Methods
#---


class ButtonRun():
    """Creates the Button to start an analysis. It contains the methods for the
        individual steps of the analysis that are performed in another thread.

        Parameters
        ----------
        parent: wx.Window
            Parent of the button.
        label: str
            Label of the button. Default is Run.
        tooltip: str
            Tooltip for the wx.Button. Default is ''.

        Attributes
        ----------
        rDeltaT: str
            Time used by the analysis.
        wBtnRun: wx.Button
            The button.

        Methods
        -------
        OnRun(event)
            Start new thread to run the analysis.
        Run(test)
            Run the steps of the analysis.
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
        EndRun()
            Restart GUI and variables. Override as needed.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        label:   str = 'Run',
        tooltip: str = '',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rDeltaT = ''
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnRun = wx.Button(parent, label=label)
        self.wBtnRun.SetToolTip(tooltip)
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.wBtnRun.Bind(wx.EVT_BUTTON, self.OnRun)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnRun(self, event:wx.CommandEvent) -> bool:                            # pylint: disable=unused-argument
        """Start new thread to run the analysis. Override as needed.

            Parameter
            ---------
            event: wx.CommandEvent
                Receive the button event.
        """
        #region ------------------------------------------------------> Thread
        _thread.start_new_thread(self.Run, ('test',))
        #endregion ---------------------------------------------------> Thread

        return True
    #---
    #endregion ------------------------------------------------> Event methods

    #region ---------------------------------------------------> Class methods
    def Run(self, *args) -> bool:                                               # pylint: disable=unused-argument
        """Run the analysis's steps.

            Parameters
            ----------
            *args is needed by _thread.start_new_thread.

            Notes
            -----
            - Messages to the Progress dialog of the app can be set in the
            individual step methods.
            - Function self.RunEnd should load the calculated results to avoid
            circular import errors and thread safety issues in pubsub.
        """
        #region --------------------------------------------------->
        start = datetime.now()
        #endregion ------------------------------------------------>

        #region -------------------------------------------------> Check input
        if not self.CheckInput():
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ----------------------------------------------> Check input

        #region -------------------------------------------------> Prepare run
        if not self.PrepareRun():
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ----------------------------------------------> Prepare run

        #region ---------------------------------------------> Read input file
        if not self.ReadInputFiles():
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ------------------------------------------> Read input file

        #region ------------------------------------------------> Run analysis
        if not self.RunAnalysis():
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ---------------------------------------------> Run analysis

        #region ------------------------------------------------> Write output
        if not self.WriteOutput():
            wx.CallAfter(self.RunEnd)
            return False
        #endregion ---------------------------------------------> Write output

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
        """Check user input."""
        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis."""
        return True
    #---

    def ReadInputFiles(self) -> bool:
        """Read the input files."""
        return True
    #---

    def RunAnalysis(self) -> bool:
        """Run the actual analysis."""
        return True
    #---

    def WriteOutput(self) -> bool:
        """Write output."""
        return True
    #---

    def RunEnd(self) -> bool:
        """Restart GUI and needed variables."""
        #region -------------------------------------------> Restart variables
        self.rDeltaT = None
        #endregion ----------------------------------------> Restart variables

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ButtonOnlineHelp():
    """Creates the Help button. The button leads to an online resource.

        Parameters
        ----------
        parent: wx.Window
            Parent of the button.
        url: str
            URL to show.
        label: str
            Label of the button. Default is Help.
        tooltip: str
            Tooltip for the wx.Button. Default is ''.

        Attributes
        ----------
        rUrl: str
            URL to show.
        wBtnHelp: wx.Button
            Help button.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        url:str,
        label:   str = 'Help',
        tooltip: str = '',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rUrl = url
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtnHelp = wx.Button(parent, label=label)
        self.wBtnHelp.SetToolTip(tooltip)
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.wBtnHelp.Bind(wx.EVT_BUTTON, self.OnHelp)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnHelp(self, event:wx.CommandEvent) -> bool:                            # pylint: disable=unused-argument
        """Leads to self.rUrl

            Parameters
            ----------
            event: wx.CommandEvent
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
    #endregion ------------------------------------------------> Event Methods
#---


class ButtonOnlineHelpClearAllRun(ButtonRun, ButtonClearAll, ButtonOnlineHelp):
    """Group of three buttons at the bottom of a pane to show online help,
        clear the input in the pane and to perform the main action of the panel.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.
        url: str
            URL for the help button.
        labelH: str
            Label for the Help button.
        tooltipH: str
            Tooltip for the help wx.Button. Default is ''.
        labelC: str
            Label for the Clear button.
        tooltipC: str
            Tooltip for the Clear wx.Button. Default is ''.
        delParent: wx.Window or None
            This is the widgets whose children values will be set to ''. If None
            then the child will be searched in parent.
        labelR: str
            Label for the Run button.
        tooltipR: str
            Tooltip for the Run wx.Button. Default is ''.
        setSizer: Boolean
            Set (True) or not the sizer for the buttons.

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
        self,
        parent:wx.Window,
        url:str,
        labelH:str                    = 'Help',
        tooltipH:str                  = '',
        labelC:str                    = 'Clear All',
        tooltipC:str                  = '',
        delParent:Optional[wx.Window] = None,
        labelR:str                    = 'Start Analysis',
        tooltipR:str                  = '',
        setSizer:bool                 = True,
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
        parent: wx.Window
            Parent of the widgets
        afterBtn: Callable
            Method to execute after self.OnBtn finishes.
        btnLabel: str
            Label for the button. Default is 'Button'.
        btnTooltip: str
            Tooltip for the wx.Button. Default is ''.
        ext: str
            File extension. Default is '' to select folder.
        mode: str
            One of 'openO', 'openM', 'save', 'folder'.
        ownCopyCut: boolean
            Use own implementation of Copy (Ctrl/Cmd C) and Cut (Ctrl/Cmd X)
            methods. Useful to delete wx.TextCtrl when style is wx.TE_READONLY.
        setSizer: boolean
            Set (True) or not (False) a sizer for the widgets.
        tcHint: str
            Hint for the wx.TextCtrl. Default is ''.
        tcSize: wx.Size
            Size of the wx.TextCtrl. Default is (300, 22).
        tcStyle: wx style
            Default is wx.TE_PROCESS_ENTER|wx.TE_READONLY.
        validator: wx.Validator or None
            To validate input for wx.TexCtrl.

        Attributes
        ----------
        wBtn: wx.Button
        wTc: wx.TextCtrl
        rMode: str
            One of 'openO', 'openM', 'save', 'folder'.
        rExt: str
            File extension. Default is '' to select folder.
        rAfterBtn: Callable
            Method to execute after self.OnBtn finishes.
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
        parent:wx.Window,
        ext:str                          =  '',
        setSizer:bool                    = False,
        btnLabel:str                     = 'Button',
        btnTooltip:str                   = '',
        tcStyle:int                      = wx.TE_PROCESS_ENTER|wx.TE_READONLY,
        tcHint:str                       = '',
        tcSize:tuple[int, int]           = (300, 22),
        validator:Optional[wx.Validator] = None,
        ownCopyCut:bool                  = False,
        mode:LIT_FFSelect                = 'openO',
        afterBtn:Optional[Callable]      = None,
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------>
        self.rMode:LIT_FFSelect = mode
        self.rExt               = ext
        self.rAfterBtn          = afterBtn
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wBtn = wx.Button(parent=parent, label=btnLabel)
        self.wBtn.SetToolTip(btnTooltip)
        #------------------------------>
        self.wTc = wx.TextCtrl(
            parent    = parent,
            value     = "",
            style     = tcStyle,
            size      = tcSize,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        self.wTc.SetHint(tcHint)
        #endregion --------------------------------------------------> Widgets

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
                wx.AcceleratorTable(list(accel.values()))
            )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnBtn(self, event:wx.CommandEvent) -> bool:                             # pylint: disable=unused-argument
        """Action to perform when button is clicked.

            Parameter
            ---------
            event: wx.CommandEvent
                Event information.
        """
        #region ------------------------------------------> Select file/folder
        if self.rMode != 'folder':
            dlg = cWindow.FileSelect(
                self.rMode, self.rExt, parent=self.cParent)
        else:
            dlg = cWindow.DirSelect(parent=self.cParent)
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

    def OnCopy(self, event:wx.Event) -> bool:                                   # pylint: disable=unused-argument
        """Copy wx.TextCtrl content.

            Parameters
            ----------
            event: wx.Event
                Information about the event.
        """
        #region ----------------------------------------------------> Get data
        data    = self.wTc.GetValue()
        dataObj = wx.TextDataObject(data)
        #endregion -------------------------------------------------> Get data

        #region -------------------------------------------> Copy to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        else:
            cWindow.Notification(
                'warning', msg=mConfig.core.mCopyFailedW, parent=self.cParent)
            return False
        #endregion ----------------------------------------> Copy to clipboard

        return True
    #---

    def OnCut(self, event:wx.Event) -> bool:
        """Cut wx.TextCtrl content.

            Parameters
            ----------
            event: wx.Event
                Information about the event.
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
    #endregion ------------------------------------------------> Event Methods
#---


class MyListCtrl(wx.ListCtrl):
    """Add several methods to the standard wx.ListCtrl.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.ListCtrl.
        colLabel: list of str
            Label for the columns in the wx.ListCtrl.
        colSize: list of int
            Width of the columns in the wx.ListCtrl.
        canCopy: Boolean
            Row content can be copied. Default is True.
        canCut: Boolean
            Row content can be copied and the selected rows deleted.
            Default is False.
        canPaste: Boolean
            New rows can be added at the end of the list or after the last
            selected row if nothing is selected.
        copyFullContent: Boolean
            Copy full rows's content or just rows's numbers. Default is False.
        sep: str
            String used to join column numbers. Default is ','.
        pasteUnique: Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll: Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False).
            For performance reasons this should not be used if
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style: wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data: list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color: str
            Row color for zebra style when wx.ListCtrl is in virtual mode.

        Attributes
        ----------
        rCanCopy: Boolean
            Row content can be copied. Default is True.
        rCanCut: Boolean
            Row content can be copied and the selected rows deleted.
            Default is False.
        rCanPaste: Boolean
            New rows can be added at the end of the list or after the last
            selected row if nothing is selected.
        rCopyFullContent: Boolean
            Copy full rows's content or just rows's numbers. Default is False.
        rPasteUnique: Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True.
        rSep: str
            String used to join column numbers. Default is ','.
        rData: list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        rColor: str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        attr1: wx.ItemAttr
            For zebra style when in virtual mode.
        rSearchMode: dict
            Keys are True/False and values methods to search in virtual or
            normal mode.

        ShortCuts
        ---------
        Ctrl/Cmd + C Copy
        Ctrl/Cmd + X Cut
        Ctrl/Cmd + P Paste
        Ctrl/Cmd + A Select All

        Notes
        -----
        - When the lengths of colLabel and colSize are different, elements in
        colSize are used as needed. Extra elements are discarded and missing
        elements are ignored.
        - canCopy is set to True if canCut is True.
        - Only rows with the same number of columns as the list can be pasted.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,                                                                   # pylint: disable=unused-argument
        parent:wx.Window,
        colLabel:list[str]   = [],
        colSize:list[int]    = [],
        canCopy:bool         = True,
        canCut:bool          = False,
        canPaste:bool        = False,
        copyFullContent:bool = False,
        sep:str              = ' ',
        pasteUnique:bool     = True,
        selAll:bool          = True,
        style:int            =  wx.LC_REPORT,
        size:tuple[int,int]  = (200, 200),
        data:list[list]      = [],
        color:str            = mConfig.core.cZebra,
        **kwargs,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCanCut          = canCut
        self.rCanCopy         = True if self.rCanCut else canCopy               # Avoid cut to fail if cut is True but copy is False
        self.rCanPaste        = canPaste
        self.rCopyFullContent = copyFullContent
        self.rPasteUnique     = pasteUnique
        self.rSep             = ' ' if sep == ' ' else f"{sep} "
        self.rData            = data
        self.rColor           = color
        #------------------------------>
        self.rSearchMode = {
            True : self.SearchVirtual,
            False: self.SearchReport,
        }
        #------------------------------>
        wx.ListCtrl.__init__(self, parent, style=style, size=size)
        #------------------------------> Set Item Count if virtual
        if self.IsVirtual():
            #------------------------------>
            self.SetItemCount(len(self.rData))
            #------------------------------>
            self.attr1 = wx.ItemAttr()
            self.attr1.SetBackgroundColour(self.rColor)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Columns
        if colLabel:
            for k, v in enumerate(colLabel):
                try:
                    self.AppendColumn(v, width=colSize[k])
                except (IndexError, TypeError):
                    self.AppendColumn(v)
        #endregion --------------------------------------------------> Columns

        #region --------------------------------------------------------> Bind
        #------------------------------> Accelerator entries
        accel = {
            'Copy' : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('C'), wx.NewId()),
            'Cut'  : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('X'), wx.NewId()),
            'Paste': wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('V'), wx.NewId()),
        }
        #------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnCopy,  id=accel['Copy'].GetCommand())
        self.Bind(wx.EVT_MENU, self.OnCut,   id=accel['Cut'].GetCommand())
        self.Bind(wx.EVT_MENU, self.OnPaste, id=accel['Paste'].GetCommand())
        #------------------------------> Special cases
        if selAll:
            #------------------------------>
            accel['SellAll'] = wx.AcceleratorEntry(
                wx.ACCEL_CTRL, ord('A'), wx.NewId()
            )
            #------------------------------>
            self.Bind(
                wx.EVT_MENU, self.OnAll, id=accel['SellAll'].GetCommand()
            )
        #------------------------------>
        self.SetAcceleratorTable(
            wx.AcceleratorTable(list(x for x in accel.values()))
        )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnAll(self, event:wx.Event) -> bool:                                    # pylint: disable=unused-argument
        """Select all rows.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Notes
            -----
            If the wx.EVT_LIST_ITEM_SELECTED is used then it will be better to
            do this where the event handler can be temporarily disabled.
        """
        #region --------------------------------------------------> Select all
        #------------------------------> Prevent
        self.Freeze()
        self.SelectAll()
        self.Thaw()
        #endregion -----------------------------------------------> Select all

        return True
    #---

    def OnCopy(self, event:Union[wx.Event, str]) -> bool:                      # pylint: disable=unused-argument
        """Copy selected rows in the wx.ListCtrl to the clipboard.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Notes
            -----
            If self.copyFullContent, then data is dict with keys being the
            selected row indexes and values a list with the rows's content from
            left to right.
            If not, then data is a string with comma-separated selected row's
            indexes
        """
        #region ----------------------------------------------> Check can copy
        if not self.rCanCopy:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mLCtrNoCopy)
            return False
        #endregion -------------------------------------------> Check can copy

        #region ----------------------------------------------------> Get data
        if self.rCopyFullContent:
            data = json.dumps(
                self.GetSelectedRows(content=self.rCopyFullContent))
        else:
            data = self.GetSelectedRows(content=self.rCopyFullContent)
            data = self.rSep.join(map(str, list(data)))
        dataObj = wx.TextDataObject(data)
        #endregion -------------------------------------------------> Get data

        #region -------------------------------------------> Copy to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        else:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mCopyFailedW)
            return False
        #endregion ----------------------------------------> Copy to clipboard

        return True
    #---

    def OnCut(self, event:wx.Event) -> bool:
        """Cut selected rows in the wx.ListCtrl to the clipboard.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Notes
            -----
            See also self.OnCopy
        """
        #region -----------------------------------------------> Check can cut
        if not self.rCanCut:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mLCtrNoChange)
            return False
        #endregion --------------------------------------------> Check can cut

        #region --------------------------------------------------------> Copy
        try:
            self.OnCopy(event)
        except Exception as e:
            raise e
        #endregion -----------------------------------------------------> Copy

        #region ------------------------------------------------------> Delete
        self.DeleteSelected()
        #endregion ---------------------------------------------------> Delete

        return True
    #---

    def OnPaste(self, event:Union[wx.Event, str]) -> bool:                      # pylint: disable=unused-argument
        """Paste selected rows in the wx.ListCtrl from the clipboard.

            Parameters
            ----------
            event: wx.Event, str
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------> Check can paste
        if not self.rCanPaste:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mLCtrNoChange)
            return False
        #endregion ------------------------------------------> Check can paste

        #region ------------------------------------------> Get Clipboard data
        #------------------------------> DataObj
        dataObj = wx.TextDataObject()
        #------------------------------> Get from clipboard
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(dataObj)
            wx.TheClipboard.Close()
        else:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mPasteFailedW)
            return False
        #------------------------------> Check success
        if not success:
            cWindow.Notification(
                'warning', parent=self, msg=mConfig.core.mNothing2PasteW)
            return False
        #------------------------------> Data
        data = json.loads(dataObj.GetText())
        #endregion ---------------------------------------> Get clipboard data

        #region --------------------------------------------------> Check Data
        if data is not None:
            for v in data.values():
                if len(v) == self.GetColumnCount():
                    continue
                #------------------------------>
                cWindow.Notification(
                    'warning', parent=self, msg=mConfig.core.mLCtrlNColPaste)
                return False
        else:
            return False
        #endregion -----------------------------------------------> Check Data

        #region ------------------------------------> Get item to insert after
        if self.GetSelectedItemCount() > 0:
            pos = self.GetLastSelected() + 1
        else:
            pos = self.GetItemCount()
        #endregion ---------------------------------> Get item to insert after

        #region -------------------------------------------------> Paste items
        for row in data.values():
            #--> Check if the row already is the wx.ListCtrl
            if self.rPasteUnique:
                if self.RowInList(row):
                    continue
            #--> Paste
            for colNum, colVal in enumerate(row):
                if colNum == 0:
                    self.InsertItem(pos, colVal)
                else:
                    self.SetItem(pos, colNum, colVal)
            #--> Increase position
            pos += 1
        #endregion ----------------------------------------------> Paste items

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class methods
    def Search(self, tStr:str) -> list[list[int]]:
        """Search tStr in the content of the wx.ListCtrl.

            Parameters
            ----------
            tStr: str
                String to search for.

            Returns
            -------
            list of list of int
                List with index of the row in which the tStr was exactly found
                or empty list and list with the index of the rows in which the
                Str is contained or empty list.

            Notes
            -----
            All occurrence of tStr are found.
        """
        return self.rSearchMode[self.IsVirtual()](tStr)
    #---

    def SearchVirtual(self, tStr:str) -> list[list[int]]:
        """Search the tStr in a virtual wx.ListCtrl.

            Parameters
            ----------
            tStr: str
                String to look for.

            Returns
            -------
            list of list of int
                List with index of the row in which the tStr was exactly found
                or empty list and list with the index of the rows in which the
                Str is contained or empty list.

            Notes
            -----
            All rows containing tStr are found.
        """
        #region ---------------------------------------------------> Variables
        iEqual   = []
        iSimilar = []
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------------> Search
        for k,row in enumerate(self.rData):
            for col in row:
                #------------------------------>
                if tStr == col:
                    iEqual.append(k)
                    iSimilar.append(k)
                    break
                #------------------------------>
                if tStr in col:
                    iSimilar.append(k)
                    break
        #endregion ---------------------------------------------------> Search

        return [iEqual, iSimilar]
    #---

    def SearchReport(self, tStr:str) -> list[list[int]]:
        """Search a non virtual wx.ListCtrl for the given string.

            Parameters
            ----------
            tStr: str
                String to look for.

            Returns
            -------
            list of list of int
                List with index of the row in which the tStr was exactly found
                or empty list and list with the index of the rows in which the
                Str is contained or empty list.

            Notes
            -----
            All rows containing tStr are found.
        """
        #region ---------------------------------------------------> Variables
        iEqual   = []
        iSimilar = []
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------------> Search
        for r in range(0, self.GetItemCount()):
            for c in range(0, self.GetColumnCount()):
                #------------------------------>
                cellText = self.GetItemText(r, c)
                #------------------------------>
                if tStr == cellText:
                    iEqual.append(r)
                    iSimilar.append(r)
                    break
                #------------------------------>
                if tStr in cellText:
                    iSimilar.append(r)
                    break
        #endregion ---------------------------------------------------> Search

        return [iEqual, iSimilar]
    #---

    def SelectAll(self) -> bool:
        """Select all rows in the wx.ListCtrl.

            Notes
            -----
            If the wx.EVT_LIST_ITEM_SELECTED is used then it will be better to
            do this where the event handler can be temporarily disabled.
        """
        #------------------------------>
        for k in range(0, self.GetItemCount()):
            self.Select(k, on=1)
        #------------------------------>
        return True
    #---

    def GetSelectedRows(self, content:bool=False) -> dict:
        """Get all selected rows in the wx.ListCtrl. If content is True then
            the content of the rows will also be retrieved.

            Parameters
            ----------
            content: Boolean
                Retrieve row content (True) or not (False). Default is False.

            Returns
            -------
            dict
                The keys are the selected row indexes added in ascending order.
                Values are a list with the row content added from left to right.
                Return empty dict if nothing is selected in the wx.ListCtrl.
        """
        #region -------------------------------------------------------> Setup
        sel = {}
        #endregion ----------------------------------------------------> Setup

        #region -----------------------------------------------> Get selection
        item = self.GetFirstSelected()
        #------------------------------>
        if content:
            while item > -1:
                sel[item] = self.GetRowContent(item)
                item = self.GetNextSelected(item)
        else:
            while item > -1:
                sel[item] = ''
                item = self.GetNextSelected(item)
        #endregion --------------------------------------------> Get selection

        return sel
    #---

    def GetRowContent(self, row:int) -> list[str]:
        """Get the content of a row in a wx.ListCtrl.

            Parameters
            ----------
            row: int
                The row index.

            Returns
            -------
            list
                List with the column content added from left to right.
        """
        #region -------------------------------------------------> Row content
        outL = [
            self.GetItemText(row, c)
            for c in range(0, self.GetColumnCount())
        ]
        #endregion ----------------------------------------------> Row content

        return outL
    #---

    def DeleteSelected(self) -> bool:
        """Delete all selected rows.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Delete rows
        for row in reversed(list(self.GetSelectedRows().keys())):
            #------------------------------> First deselect
            self.Select(row, on=0)
            #------------------------------> Delete
            self.DeleteItem(row)
        #endregion ----------------------------------------------> Delete rows

        #region -----------------------------------------------> Refresh color
        if isinstance(self, listmix.ListRowHighlighter):
            self.RefreshRows()
        #endregion --------------------------------------------> Refresh color

        return True
    #---

    def GetLastSelected(self) -> int:
        """Get the last selected item in the list.

            Returns
            -------
            int
                The last selected index or -1 if nothing is selected
        """
        #region ------------------------------------------------------> Search
        if (item := self.GetFirstSelected()) > -1:
            while (nItem := self.GetNextSelected(item)) > -1:
                item = nItem
        #endregion ---------------------------------------------------> Search

        return item
    #---

    def RowInList(self, row:list) -> bool:
        """Check if row is already in the wx.ListCtrl.

            Parameters
            ----------
            row: list of str
                One str for each column in the list. It is assumed the rows
                elements and the columns in the wx.ListCtrl have the same order.

            Returns
            -------
            Boolean
                True if row is found at least one time in the wx.ListCtrl,
                False otherwise.
        """
        #region ---------------------------------------------------> Variables
        rowC = list(map(str, row))
        item = 0
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> Search items
        while item > -1:
            #------------------------------> # Find row in wx.ListCtrl containing the first element in row
            item = self.FindItem(item, row[0])
            #------------------------------> # Check the rest of elements in the row
            if item > -1:
                rowList = self.GetRowContent(item)
                #------------------------------>
                if rowList == rowC:
                    return True
            else:
                break
            #------------------------------> Find starting in the next item
            item += 1
        #endregion ---------------------------------------------> Search items

        return False
    #---

    def SelectList(self, listC:list[int]) -> bool:
        """Select all items in the list of rows. Silently ignores wrong indexes.

            Parameters
            ----------
            listC: list[int]
                List of row indexes.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Select
        for k in listC:
            try:
                self.Select(k, on=1)
            except Exception:
                pass
        #endregion ---------------------------------------------------> Select

        return True
    #---

    def GetColContent(self, col:int) -> list[str]:
        """Get the content of a column.

            Parameters
            ----------
            col: int
                Column index

            Returns
            -------
            list
                List with the column content from top to bottom
        """
        #region ----------------------------------------------> Column content
        outL = [self.GetItemText(c, col) for c in range(0, self.GetItemCount())]
        #endregion -------------------------------------------> Column content

        return outL
    #---

    def OnGetItemText(self, row:int, column:int) -> str:
        """Get cell value for virtual mode. Needed by wxPython.

            Parameters
            ----------
            row: int
                Row number. 0-based.
            column: int
                Colum number. 0-based.

            Returns
            -------
            str
                Cell value
        """
        return self.rData[row][column]
    #---

    def OnGetItemAttr(self, item:int) -> Optional[wx.ItemAttr]:
        """Get row attributes in a virtual list. Needed by wxPython.

            Parameters
            ----------
            item: int
                Row index. 0-based.

            Return
            ------
            wx.ItemAttr
        """
        if item % 2 == 0:
            return self.attr1
        #------------------------------>
        return None
    #---

    def SetNewData(self, data:list[list[str]]) -> bool:
        """Set new data for a virtual wx.ListCtrl.

            Parameters
            ----------
            data: list of list of str
                One str field for each column in the wx.ListCtrl.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Set Data
        self.rData = data
        #------------------------------>
        self.SetItemCount(len(self.rData))
        #endregion ------------------------------------------------> Set Data

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class MyListCtrlZebra(MyListCtrl, listmix.ListRowHighlighter):
    """A wx.ListCtrl with the zebra style and extra methods.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.ListCtrl.
        color: str
            Color for the zebra style.
        colLabel: list of str
            Label for the columns in the wx.ListCtrl.
        colSize: list of int
            Width of the columns in the wx.ListCtrl.
        canCopy: Boolean
            Row content can be copied. Default is True.
        canCut: Boolean
            Row content can be copied and the selected rows deleted.
            Default is False.
        canPaste: Boolean
            New rows can be added at the end of the list or after the last
            selected row if nothing is selected.
        copyFullContent: Boolean
            Copy full rows's content or just rows's numbers. Default is False.
        sep: str
            String used to join column numbers. Default is ','.
        pasteUnique: Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True.
        selAll: Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False).
            For performance reasons this should not be used if
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style: wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data: list of list of str
            Data for the wx.ListCtrl when in virtual mode.

        Notes
        -----
        See MyListCtrl for more details.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent:wx.Window,
        color:str            = mConfig.core.cZebra,
        colLabel:list[str]   = [],
        colSize:list[int]    = [],
        canCopy:bool         = True,
        canCut:bool          = False,
        canPaste:bool        = False,
        copyFullContent:bool = False,
        sep:str              = ' ',
        pasteUnique:bool     = True,
        selAll:bool          = True,
        style:int            = wx.LC_REPORT,
        size:tuple[int,int]  = (200, 200),
        data:list[list]      = [],
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        MyListCtrl.__init__(
            self,
            parent,
            colLabel        = colLabel,
            colSize         = colSize,
            canCopy         = canCopy,
            canCut          = canCut,
            canPaste        = canPaste,
            copyFullContent = copyFullContent,
            sep             = sep,
            pasteUnique     = pasteUnique,
            selAll          = selAll,
            style           = style,
            size            = size,
            data            = data,
            color           = color,
        )

        listmix.ListRowHighlighter.__init__(self, color)
        #endregion --------------------------------------------> Initial setup
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class MyListCtrlZebraMaxWidth(MyListCtrlZebra, listmix.ListCtrlAutoWidthMixin):
    """A wx.ListCtrl with the zebra style and expanding last column.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the wx.ListCtrl.
        color: str
            Color for the zebra style.
        colLabel: list of str
            Label for the columns in the wx.ListCtrl.
        colSize: list of int
            Width of the columns in the wx.ListCtrl.
        canCopy: Boolean
            Row content can be copied. Default is True.
        canCut: Boolean
            Row content can be copied and the selected rows deleted.
            Default is False.
        canPaste: Boolean
            New rows can be added at the end of the list or after the last
            selected row if nothing is selected.
        copyFullContent: Boolean
            Copy full rows's content or just rows's numbers. Default is False.
        sep: str
            String used to join column numbers. Default is ','.
        pasteUnique: Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True.
        selAll: Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False).
            For performance reasons this should not be used if
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style: wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data: list of list of str
            Data for the wx.ListCtrl when in virtual mode.

        Notes
        -----
        See MyListCtrl for more details.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent:wx.Window,
        color:str            = mConfig.core.cZebra,
        colLabel:list[str]   = [],
        colSize:list[int]    = [],
        canCopy:bool         = True,
        canCut:bool          = False,
        canPaste:bool        = False,
        copyFullContent:bool = False,
        sep:str              = ' ',
        pasteUnique:bool     = True,
        selAll:bool          = True,
        style:int            = wx.LC_REPORT,
        size:tuple[int,int]  = (200, 200),
        data:list[list]      = [],
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        MyListCtrlZebra.__init__(
            self,
            parent,
            color           = color,
            colLabel        = colLabel,
            colSize         = colSize,
            canCopy         = canCopy,
            canCut          = canCut,
            canPaste        = canPaste,
            copyFullContent = copyFullContent,
            sep             = sep,
            pasteUnique     = pasteUnique,
            selAll          = selAll,
            style           = style,
            size            = size,
            data            = data,
        )

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        #endregion --------------------------------------------> Initial setup
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ResControl():
    """Creates the Results - Control experiment widgets.

        Parameters
        ----------
        parent : wx widget
            Parent of the widgets.
    """
    #region -----------------------------------------------------> Class setup
    cLResControl     = mConfig.core.lStResCtrl
    cLBtnTypeResCtrl = mConfig.core.lBtnTypeResCtrl
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -------------------------------------------------------->
        self.cParent = parent.GetParent()
        #endregion ----------------------------------------------------->

        #region -----------------------------------------------------> Widgets
        self.wTcResults = wx.TextCtrl(
            parent    = parent,
            style     = wx.TE_READONLY,
            value     = "",
            size      = mConfig.core.sTc,
            validator = cValidator.IsNotEmpty(),
        )
        self.wStResults = wx.StaticText(
            parent = parent,
            label  = self.cLResControl,
            style  = wx.ALIGN_RIGHT
        )
        self.wBtnResultsW = wx.Button(
            parent = parent,
            label  = self.cLBtnTypeResCtrl,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sRes = wx.GridBagSizer(1,1)
        #------------------------------>
        self.sRes.Add(
            self.wStResults,
            pos    = (0,0),
            flag   = wx.ALIGN_LEFT|wx.ALL,
            border = 5,
            span   = (0,2),
        )
        self.sRes.Add(
            self.wBtnResultsW,
            pos    = (1,0),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5
        )
        self.sRes.Add(
            self.wTcResults,
            pos    = (1,1),
            flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            border = 5,
        )
        #------------------------------>
        self.sRes.AddGrowableCol(1,1)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------------> Tooltip
        self.wBtnResultsW.SetToolTip(
            'Type the column numbers in a helper window.')
        self.wStResults.SetToolTip(
            'Set the column numbers containing the control and experiment '
            'results.')
        #endregion --------------------------------------------------> Tooltip

        #region --------------------------------------------------------> Bind
        self.wBtnResultsW.Bind(wx.EVT_BUTTON, self.OnResW)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnResW(self, event:wx.CommandEvent) -> bool:                           # pylint: disable=unused-argument
        """Open the window to write the results columns.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #------------------------------>
        with cWindow.ResControlExp(self.cParent) as dlg:
            dlg.ShowModal()
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Event methods
#---


class MatPlotPanel(wx.Panel):
    """Panel with a matplotlib plot.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel.
        dpi: int
            DPI for the plot. Default is 100.
        statusbar: wx.StatusBar
            wx.StatusBar to display information about the graph.
        statusMethod: callable or None
            Method to print information to the statusbar. The method should
            accept only one parameter, the matplotlib event. Default is None.

        Attributes
        ----------
        rAxes:
            Axes in the canvas.
        rBindId: list
            List of bound events to connect and disconnect them.
        rCanvas: FigureCanvas
            Canvas in the panel.
        rDPI: int
            DPI for the plot. Default is 100.
        rFigure: mpl.Figure
            Figure in the panel.
        rFinalX: float
            x coordinate in the plot scale when drag is over.
        rFinalY: float
            y coordinate in the plot scale when drag is over.
        rInitX: float
            x coordinate in the plot scale when left click is pressed.
        rInitY: float
            y coordinate in the plot scale when left click is pressed.
        rZoomRect: mpl.patches.Rectangle or None
            Rectangle to show the zoom in area.
        rZoomReset: dict
            Cero zoom axes configuration. This will be used to reset the zoom
            level. {'x' : (xmin, xmax), 'y': (ymin, ymax)}.
        rStatusMethod: Callable or None
            Method to print information to the statusbar. The method should
            accept only one parameter, the matplotlib event. Default is None.
        wStatBar: wx.StatusBar
            wx.StatusBar to display information about the graph.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent: wx.Window,
        dpi:Optional[int]                = None,
        statusbar:Optional[wx.StatusBar] = None,
        statusMethod:Optional[Callable]  = None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rDPI          = mConfig.core.DPI if dpi is None else dpi
        self.wStatBar      = statusbar
        self.rStatusMethod = statusMethod
        self.rInitY        = float('inf')
        self.rInitX        = float('inf')
        self.rFinalX       = float('inf')
        self.rFinalY       = float('inf')
        self.rZoomRect     = None
        self.rZoomReset    = {}
        self.rBindId       = []
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.rFigure  = mpl.figure.Figure(                                      # type: ignore
            dpi          = self.rDPI,
            figsize      = (2, 2),
            tight_layout = True,
        )
        self.rCanvas  = FigureCanvas(self, -1, self.rFigure)
        self.rAxes    = self.rFigure.add_subplot(111)
        self.rAxes.set_axisbelow(True)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sPlot = wx.BoxSizer(wx.HORIZONTAL)
        self.sPlot.Add(self.rCanvas, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sPlot)
        self.sPlot.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.ConnectEvent()
        #------------------------------> Keyboard shortcut
        #--------------> Accelerator entries
        accel = {
            'Zoom' : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('Z'), wx.NewId()),
            'Img'  : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('I'), wx.NewId()),
        }
        #--------------> Bind
        self.Bind(
            wx.EVT_MENU, self.OnZoomResetPlot, id=accel['Zoom'].GetCommand())
        self.Bind(
            wx.EVT_MENU, self.OnSaveImage, id=accel['Img'].GetCommand())
        #--------------> Add
        self.SetAcceleratorTable(
            wx.AcceleratorTable([x for x in accel.values()])
        )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnSaveImage(self, event:wx.CommandEvent) -> bool:                       # pylint: disable=unused-argument
        """Save an image of the plot.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        return self.SaveImage(mConfig.core.elMatPlotSaveI, parent=self)
    #---

    def OnZoomResetPlot(self, event:wx.CommandEvent) -> bool:                   # pylint: disable=unused-argument
        """Reset the zoom level of the plot.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        return self.ZoomResetPlot()
    #---

    def OnKeyPress(self, event) -> bool:
        """Process a key press event.

            Parameter
            ---------
            event: mpl.KeyEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Event
        if event.key == 'escape':
            self.OnZoomInAbort(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnGetAxesXY(self, event) -> tuple[float, float]:
        """Get the x,y mouse coordinates.

            Parameters
            ----------
            event: mpl.event
                Information about the event.

            Returns
            -------
            tuple
                (X, Y) coordinates.
        """
        #region --------------------------------------------------->
        x = event.xdata
        #------------------------------>
        if getattr(self, 'rAxes2', None) is not None:
            _, y = self.rAxes.transData.inverted().transform((event.x,event.y))
        else:
            y = event.ydata
        #endregion ------------------------------------------------>

        return (x,y)
    #---

    def OnMotionMouse(self, event) -> bool:
        """Handle move mouse event.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Event
        if event.button == 1:
            self.OnDrawZoomRect(event)
        else:
            self.OnUpdateStatusBar(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnUpdateStatusBar(self, event):
        """To update status bar. Basic functionality.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Skip
        if self.wStatBar is None:
            return True
        #endregion ------------------------------------------------> Skip

        #region -------------------------------------------------------> Event
        if event.inaxes:
            if self.rStatusMethod is not None:
                self.rStatusMethod(event)
            else:
                x,y = self.OnGetAxesXY(event)
                self.wStatBar.SetStatusText(
                    f"x={x:.2f} y={y:.2f}"
                )
        else:
            self.wStatBar.SetStatusText('')
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnDrawZoomRect(self, event) -> bool:
        """Draw a rectangle to highlight area that will be zoomed in.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -----------------------------------------> Check event in axes
        if not event.inaxes:
            return False
        #endregion --------------------------------------> Check event in axes

        #region -----------------------------------------> Initial coordinates
        if math.isinf(self.rInitX):
            self.rInitX, self.rInitY = self.OnGetAxesXY(event)
        #endregion --------------------------------------> Initial coordinates

        #region -------------------------------------------> Final coordinates
        self.rFinalX, self.rFinalY = self.OnGetAxesXY(event)
        #endregion ----------------------------------------> Final coordinates

        #region ------------------------------------> Delete & Create zoomRect
        #------------------------------>
        if self.rZoomRect is not None:
            self.rZoomRect.remove()
        #------------------------------>
        self.rZoomRect = patches.Rectangle(
            (min(self.rInitX, self.rFinalX), min(self.rInitY, self.rFinalY)), # type: ignore
            abs(self.rInitX - self.rFinalX),
            abs(self.rInitY - self.rFinalY), # type: ignore
            fill      = False,
            linestyle = '--',
            linewidth = '0.5'
        )
        #endregion ---------------------------------> Delete & Create zoomRect

        #region --------------------------------------------------> Add & Draw
        self.rAxes.add_patch(
            self.rZoomRect
        )
        self.rCanvas.draw()
        #endregion -----------------------------------------------> Add & Draw

        return True
    #---

    def OnZoomInAbort(self, event) -> bool:
        """Abort a zoom in operation when Esc is pressed.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #------------------------------>
        self.rInitX  = float('inf')
        self.rInitY  = float('inf')
        self.rFinalX = float('inf')
        self.rFinalY = float('inf')
        #------------------------------>
        self.ZoomRectDelete()
        #------------------------------>
        self.OnUpdateStatusBar(event)

        return True
    #---

    def OnPressMouse(self, event) -> bool:
        """Process press mouse event.

            Parameter
            ---------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Event
        if event.inaxes and event.button == 1:
            self.OnLeftClick(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnLeftClick(self, event) -> bool:
        """Process left click event.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Event
        self.rInitX, self.rInitY = self.OnGetAxesXY(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnReleaseMouse(self, event) -> bool:
        """Process a release mouse event.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Event
        if event.button == 1:
            self.OnLeftRelease(event)
        #endregion ------------------------------------------------> Event

        return True
    #---

    def OnLeftRelease(self, event) -> bool:                                     # pylint: disable=unused-argument
        """Process a left button release event.

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Zoom in
        if not math.isinf(self.rFinalX):
            self.rAxes.set_xlim(
                min(self.rInitX, self.rFinalX),
                max(self.rInitX, self.rFinalX),
            )
            self.rAxes.set_ylim(
                min(self.rInitY, self.rFinalY),
                max(self.rInitY, self.rFinalY),
            )
        else:
            return True
        #endregion --------------------------------------------------> Zoom in

        #region -----------------------------------> Reset initial coordinates
        self.rInitY  = float('inf')
        self.rInitX  = float('inf')
        self.rFinalX = float('inf')
        self.rFinalY = float('inf')
        #endregion --------------------------------> Reset initial coordinates

        #region --------------------------------------------> Delete zoom rect
        self.ZoomRectDelete()
        #endregion -----------------------------------------> Delete zoom rect

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class methods
    def ConnectEvent(self) -> bool:
        """Connect all event handlers.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Connect events
        self.rBindId.append(
            self.rCanvas.mpl_connect('motion_notify_event', self.OnMotionMouse)
        )
        self.rBindId.append(
            self.rCanvas.mpl_connect('button_press_event', self.OnPressMouse)
        )
        self.rBindId.append(
            self.rCanvas.mpl_connect('button_release_event', self.OnReleaseMouse)
        )
        self.rBindId.append(
            self.rCanvas.mpl_connect('key_press_event', self.OnKeyPress)
        )
        #endregion --------------------------------------------> Connect events

        return True
    #---

    def DisconnectEvent(self) -> bool:
        """Disconnect the event defined in ConnectEvent.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Disconnect
        for k in self.rBindId:
            self.rCanvas.mpl_disconnect(k)
        #endregion -----------------------------------------------> Disconnect

        #region --------------------------------------------------> Reset list
        self.rBindId = []
        #endregion -----------------------------------------------> Reset list

        return True
    #---

    def ZoomResetSetValues(self) -> bool:
        """Set the axis limit in the cero zoom state. Should be called after all
            initial plotting and axis configuration is done.

            Returns
            -------
            bool
        """
        self.rZoomReset = {'x': self.rAxes.get_xlim(), 'y': self.rAxes.get_ylim()}
        #------------------------------>
        return True
    #---

    def ZoomResetPlot(self) -> bool:
        """Reset the zoom level of the plot.

            Return
            ------
            True
        """
        self.rAxes.set_xlim(self.rZoomReset['x'])
        self.rAxes.set_ylim(self.rZoomReset['y'])
        self.rCanvas.draw()
        #------------------------------>
        return True
    #---

    def ZoomRectDelete(self) -> bool:
        """Delete the zoom in rectangle"""
        #region --------------------------------------------------------> Rect
        if self.rZoomRect is not None:
            self.rZoomRect.remove()
            self.rCanvas.draw()
            self.rZoomRect = None
        #endregion -----------------------------------------------------> Rect

        return True
    #---

    def SaveImage(
        self,
        ext:str,
        parent:Optional[wx.Window] = None,
        msg:str                    = '',
        ) -> bool:
        """Save an image of the plot.

            Parameters
            ----------
            ext: file extension
                wxPython extension spec.
            parent: wx.Widget or None
                To center the save dialog. Default is None.
            msg: str or None
                Title for the save file window. Default is None.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Dialog
        dlg = cWindow.FileSelect('save', ext, parent=parent, msg=msg)
        #endregion ---------------------------------------------------> Dialog

        #region ----------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.rFigure.savefig(path, dpi=self.rDPI)
        #endregion -------------------------------------------------> Get Path

        dlg.Destroy()
        return True
    #---

    def SetStatBar(
        self,
        statusbar:wx.StatusBar,
        method:Optional[Callable] = None
        ) -> bool:
        """Set the wx.StatusBar and StatusBar text update method after creating
            the widget.

            Parameters
            ----------
            statusbar: wx.StatusBar.
                wx.StatusBar
            method: Callable or None
                In the case of a Callable it must accept the event as first
                argument.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wStatBar      = statusbar
        self.rStatusMethod = method
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ListCtrlSearch():
    """Creates a wx.ListCtrl with a wx.SearchCtrl beneath it.

        Parameters
        ----------
        parent: wx.Window or None
            Parent of the wx.ListCtrl.
        listT: 0, 1 or 2
            Type of wx.ListCtrl.
        setSizer: bool
            Arrange widgets in self.Sizer. Default is True.
        colLabel: list of str
            Label for the columns in the wx.ListCtrl.
        colSize: list of int
            Width of the columns in the wx.ListCtrl.
        canCopy: Boolean
            Row content can be copied. Default is True.
        canCut: Boolean
            Row content can be copied and the selected rows deleted.
            Default is False.
        canPaste: Boolean
            New rows can be added at the end of the list or after the last
            selected row if nothing is selected.
        copyFullContent: Boolean
            Copy full rows's content or just rows's numbers. Default is False.
        sep: str
            String used to join column numbers. Default is ','.
        pasteUnique: Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True.
        selAll: Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False).
            For performance reasons this should not be used if
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style: wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data: list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color: str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        tcHint: str
            Hint for the wx.TextCtrl.

        Attributes
        ----------
        listTDict: dict
            Keys are 0,1,2 and methods the class for the wx.ListCtrl.
        wLC : wx.ListCtrl
        wSearch : wx.SearchCtrl
    """
    #region -----------------------------------------------------> Class setup
    listTDict = {
        0: MyListCtrl,
        1: MyListCtrlZebra,
        2: MyListCtrlZebraMaxWidth,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent:wx.Window,
        listT:int           = 1,
        setSizer:bool       = True,
        color:str           = mConfig.core.cZebra,
        colLabel:list[str]  = [],
        colSize:list[int]   = [],
        canCopy:bool        = True,
        canCut:bool         = False,
        canPaste:bool       = False,
        copyFullContent:bool= False,
        sep:str             = ' ',
        pasteUnique:bool    = True,
        selAll:bool         = True,
        style:int           = wx.LC_REPORT,
        data:list[list]     = [],
        tcHint:str          = '',
        ) -> None:
        """ """
        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ListCtrl
        self.wLC = self.listTDict[listT](
            parent,
            color           = color,
            colLabel        = colLabel,
            colSize         = colSize,
            canCopy         = canCopy,
            canCut          = canCut,
            canPaste        = canPaste,
            copyFullContent = copyFullContent,
            sep             = sep,
            pasteUnique     = pasteUnique,
            selAll          = selAll,
            style           = style,
            data            = data,
        )
        #------------------------------> wx.SearchCtrl
        self.wSearch = wx.SearchCtrl(parent)
        self.wSearch.SetHint(tcHint) if tcHint else ''                          # pylint: disable=expression-not-assigned
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            #------------------------------>
            self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
            #------------------------------>
            self.sSizer.Add(self.wLC, 1, wx.EXPAND|wx.ALL, 5)
            self.sSizer.Add(self.wSearch, 0, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes

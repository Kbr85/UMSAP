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


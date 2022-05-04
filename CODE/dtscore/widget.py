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
import _thread
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, Union, Callable

import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import wx
import wx.lib.mixins.listctrl as listmix

import config.config as config
import dtscore.check as dtsCheck
import dtscore.exception as dtsException
import dtscore.file as dtsFF
import dtscore.generator as dtsGenerator
import dtscore.window as dtsWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def StatusBarUpdate(
    statusbar: wx.StatusBar, msg: str, field: int=0
    ) -> Literal[True]:
    """Updates the text in field of a statusbar.

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

def ClearInput(parent: wx.Window) -> Literal[True]:
    """Set all user input to '' and delete all items in wx.ListCtrls

        Parameters
        ----------
        parent : wx.Window
            All child widgets of parent will be clear.
    """
    #region -----------------------------------------------------------> Clear
    for child in dtsGenerator.FindChildren(parent):
        #------------------------------> 
        tc     = isinstance(child, wx.TextCtrl)
        cb     = isinstance(child, wx.ComboBox)
        checkB = isinstance(child, wx.CheckBox)
        lc     = isinstance(child, wx.ListCtrl)
        #------------------------------> 
        if tc or cb:
            child.SetValue("")
        elif checkB:
            child.SetValue(False)
        elif lc:
            child.DeleteAllItems()
        else:
            pass
    #endregion --------------------------------------------------------> Clear
    
    return True
#---
#endregion ----------------------------------------------------------> Methods


#region ------------------------------------------------------> Single widgets
class MyListCtrl(wx.ListCtrl):
    """Add several methods to the standard wx.ListCtrl

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color : str
            Row color for zebra style when wx.ListCtrl is in virtual mode.

        Attributes
        ----------
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        sep : str
            String used to join column numbers. Default is ','
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color : str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        attr1 : wx.ItemAttr
            For zebra style when in virtual mode.
        searchMode : dict
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
    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, colLabel: Optional[list[str]]=None, 
        colSize: Optional[list[int]]=None, canCopy: bool=True, 
        canCut: bool=False, canPaste: bool=False, copyFullContent:bool=False, 
        sep: str=',', pasteUnique: bool=True, selAll: bool=True, 
        style=wx.LC_REPORT, data: list[list]=[], color=config.color['Zebra'], 
        **kwargs,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.canCopy         = canCopy
        self.canCut          = canCut
        #--> Avoid cut to fail if cut is True but copy is false
        self.canCopy = True if self.canCut else self.canCopy
        self.canPaste        = canPaste
        self.copyFullContent = copyFullContent
        self.pasteUnique     = pasteUnique
        self.sep             = ' ' if sep == ' ' else f"{sep} " 
        self.data            = data
        self.color           = color
        #------------------------------> 
        self.searchMode = {
            True : self.SearchVirtual,
            False: self.SearchReport,
        }
        #------------------------------> 
        wx.ListCtrl.__init__(self, parent, style=style)
        #------------------------------> Set Item Count if virtual
        if self.IsVirtual():
            #------------------------------> 
            self.SetItemCount(len(self.data))
            #------------------------------> 
            self.attr1 = wx.ItemAttr()
            self.attr1.SetBackgroundColour(self.color)
        else:
            pass
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Columns
        if colLabel is None:
            pass
        else:
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
        else:
            pass
        #------------------------------> 
        self.SetAcceleratorTable(
            wx.AcceleratorTable([x for x in accel.values()])
        )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnGetItemText(self, row, column) -> str:
        """Get cell value for virtual mode.
    
            Parameters
            ----------
            row : int
                Row number. 0-based
            column : int
                Colum number. 0-based 
    
            Returns
            -------
            str
                Cell value
        """
        return self.data[row][column]
    #---
    
    def OnGetItemAttr(self, item: int) -> Optional[wx.ItemAttr]:
        """Get row attributes. Needed by virtual lists.
        
            Parameters
            ----------
            item : int
                Row index. 0-based.
                
            Return
            ------
            wx.ItemAttr
        """
        if item % 2 == 0:
            return self.attr1
        else:
            return None
    #---

    def AddList(self, listV: list[list[str]], append: bool=False) -> bool:
        """Fill/Append values in listV to the wx.ListCtrl.
        
            See Notes below for more details
    
            Parameters
            ----------
            listV : list of str
                The number of elements in listV[k] and the number of columns in 
                wx.ListCtrl must match.
            append : bool
                Append to the end of the wx.ListCtrl (True) or delete current 
                values (False). Default is False.
    
            Returns
            -------
            bool
    
            Raise
            -----
            ExecutionError:
                - When elements in listV cannot be converted to str.
                - When the number of elements in listV[k] does not math the 
                number of columns in wx.ListCtrl
                
            Notes
            -----
            - If append is False existing elements in the wx.ListCtrl will 
            deleted before adding the new ones.
            - If and error occurs while adding new rows the already added new 
            rows will be deleted. Nevertheless, if append is False the result 
            will be an empty wx.ListCtrl.
            
        """
        #region ------------------------------------------------------> Append
        if append:
            pass
        else:
            self.DeleteAllItems()
        #endregion ---------------------------------------------------> Append
        
        #region ---------------------------------------------------> Variables
        lcRow = self.GetItemCount()
        #endregion ------------------------------------------------> Variables
        
        #region --------------------------------------------------> Add values
        for k in listV:
            try:
                self.Append(k)
            except Exception:
                #------------------------------> Delete already added rows
                self.DeleteRows(lcRow)
                #------------------------------> 
                msg = 'It was not possible to add new data to the wx.ListCtrl.'
                raise dtsException.ExecutionError(msg)
        #endregion -----------------------------------------------> Add values
        
        return True
    #---
    
    def SetNewData(self, data: list[list[str]]):
        """Set new data for a virtual wx.ListCtrl.
    
            Parameters
            ----------
            data : list of list of str
                One str field for each column in the wx.ListCtrl
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #region ---------------------------------------------------> Set Data
        #------------------------------> 
        self.data = data
        #------------------------------> 
        self.SetItemCount(len(self.data))
        #endregion ------------------------------------------------> Set Data
        
        return True
    #---
    
    def RowInList(self, row: list[str]) -> bool:
        """Check if row is already in the wx.ListCtrl
    
            Parameters
            ----------
            row : list of str
                One str for each column in the list. It is assumed the rows
                elements and the columns in the wx.ListCtrl have the same order.

            Returns
            -------
            Boolean
                True if row is found at least one time in the wx.ListCtrl, 
                False otherwise.

            Raise
            -----
            InputError
                - When len(row) > wx.ListCtrl.GetColumnCount()
        """
        #region ---------------------------------------------------> Variables
        lenRow = len(row)
        NCol = self.GetColumnCount()
        #endregion ------------------------------------------------> Variables
        
        #region -------------------------------------------------> Check input
        if lenRow > NCol:
            msg = (
                f"The number of elements to search for in the wx.ListCtrl is "
                f"larger than the number of columns in the wx.ListCtrl "
                f"({lenRow} > {NCol})."
            )
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input
        
        #region ---------------------------------------------------> Variables
        item = 0
        #endregion ------------------------------------------------> Variables
        
        #region ------------------------------------------------> Search items
        while item > -1:
            #------------------------------> Find item or not
            item = self.FindItem(item, row[0])
            if item > -1:
                #------------------------------> New row comparison
                comp = []
                #------------------------------> Check each element in row
                #--> Get elements
                for k,e in enumerate(row):
                    #-------------->  Make sure element in row is string like
                    try:
                        strE = str(e)
                    except Exception as e:
                        msg = (
                            f'row element ({e}) cannot be turned into string.'
                        )
                        raise dtsException.ExecutionError(msg)
                    #------------------------------> Compare
                    if strE == self.GetItemText(item, col=k): 
                        comp.append(True)
                    else:
                        comp.append(False)
                        break
                #--> Check all
                if all(comp):
                    return True
                else:
                    pass
            else:
                break
            #--> Find starting in the next item
            item += 1		
        #endregion ---------------------------------------------> Search items
        
        return False
    #---

    def SelectAll(self) -> Literal[True]:
        """Select all rows in the wx.ListCtrl
        
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
    
    def SelectList(self, listC: list[int]) -> bool:
        """Select all items in the list of rows. Silently ignores wrong indexes.
    
            Parameters
            ----------
            listC : list[int]
                List of row indexes
                
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
    
    def Search(self, tStr: str) -> list[int]:
        """Search tStr in the content of the wx.ListCtrl.
        
            See Notes below for more details.
    
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
        return self.searchMode[self.IsVirtual()](tStr)
    #---
    
    def SearchVirtual(self, tStr: str) -> list[list[int]]:
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
            All occurrence of tStr are found.
        """
        #region ---------------------------------------------------> Variables
        iEqual   = []
        iSimilar = []
        #endregion ------------------------------------------------> Variables
        
        #region ------------------------------------------------------> Search
        for k,row in enumerate(self.data):
            for col in row:
                #------------------------------> 
                if tStr == col:
                    iEqual.append(k)
                    iSimilar.append(k)
                    break
                elif tStr in col:
                    iSimilar.append(k)
                    break
                else:
                    pass
        #endregion ---------------------------------------------------> Search
        
        return [iEqual, iSimilar]
    #---
    
    def SearchReport(self, tStr: str) -> list[list[int]]:
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
            All occurrence of tStr are found.
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
                elif tStr in cellText:
                    iSimilar.append(r)
                    break
                else:
                    pass
        #endregion ---------------------------------------------------> Search
        
        return [iEqual, iSimilar]
    #---

    def GetColContent(self, col: int) -> list[str]:
        """Get the content of a column
    
            Parameters
            ----------
            col : int
                Column index
    
            Returns
            -------
            list
                List with the column content from top to bottom
    
            Raise
            -----
            InputError:
                - When col is not present in the wx.ListCtrl
        """
        #region ---------------------------------------------------> Variables
        NCol = self.GetColumnCount()
        #endregion ------------------------------------------------> Variables
        
        #region -------------------------------------------------> Check input
        if col >= NCol:
            msg = (
                f"The column number must be smaller than the total number of "
                f"columns in the ListCtrl ({col} >= {NCol})."
            )
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input
        
        #region ----------------------------------------------> Column content
        outL = [self.GetItemText(c, col) for c in range(0, self.GetItemCount())]
        #endregion -------------------------------------------> Column content

        return outL
    #---
    
    def GetRowContent(self, row: int) -> list[str]:
        """Get the content of a row in a wx.ListCtrl

            Parameters
            ----------
            row : int
                The row index

            Returns
            -------
            list
                List with the column content added from left to right

            Raise
            -----
            InputError
                - When row is not present in the wx.ListCtrl
        """
        #region ---------------------------------------------------> Variables
        NRow = self.GetItemCount()
        #endregion ------------------------------------------------> Variables
        
        #region -------------------------------------------------> Check input
        if row >= NRow:
            msg = (
                f"The row number must be lower than the total number of rows "
                f"in the wx.ListCtrl ({row} >= {NRow})."
            )
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input

        #region -------------------------------------------------> Row content
        outL = [
            self.GetItemText(row, c) 
            for c in range(0, self.GetColumnCount())
        ]
        #endregion ----------------------------------------------> Row content

        return outL
    #---

    def GetSelectedRows(self, content: bool=False) -> dict:
        """Get all selected rows in the wx.ListCtrl. If content is True then 
            the content of the rows will also be retrieved.

            Parameters
            ----------
            content : Boolean
                Retrieve row content (True) or not (False). Default is False

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
        if (item := self.GetFirstSelected()) > -1:
            #------------------------------> First selected item
            if content:
                sel[item] = self.GetRowContent(item)
            else:
                sel[item] = ''
            #------------------------------> All other selected items
            while (item := self.GetNextSelected(item)) > -1:
                if content:
                    sel[item] = self.GetRowContent(item)
                else:
                    sel[item] = ''
        else:
            pass
        #endregion --------------------------------------------> Get selection

        return sel
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
            while (nitem := self.GetNextSelected(item)) > -1:
                item = nitem
        else:
            pass		
        #endregion ---------------------------------------------------> Search
            
        return item
    #---
    
    def SetRowContent(self, rowL: list[str], rowInd: int) -> Literal[True]:
        """Edit the content of a row.
    
            Parameters
            ----------
            rowL : list of str
                List of the text to use for each column.
            rowInd : int
                Row index to edit elements
    
            Returns
            -------
            True
    
            Raise
            -----
            InputError:
                - When the number of columns and the number of items in rowL are
                different
                - When the row index does not exists
        """
        #region -------------------------------------------------> Check input
        if len(rowL) != self.GetColumnCount():
            msg = (
                f"The number of elements in rowL is different to the number of"
                f"columns in the wx.ListCtrl"
            )
            raise dtsException.InputError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check input
        
        #region ------------------------------------------------> Add elements
        for k, v in enumerate(rowL):
            try:
                self.SetItem(rowInd, k, v)
            except Exception:
                raise dtsException.InputError(f'Row {rowInd} does not exist.')
        #endregion ---------------------------------------------> Add elements
        
        return True
    #---

    def DeleteSelected(self) -> Literal[True]:
        """Delete all selected rows"""
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
        else:
            pass
        #endregion --------------------------------------------> Refresh color
        
        return True
    #---
    
    def DeleteRows(self, start: int, end: Optional[int]=None) -> bool:
        """Delete all rows in the given interval.
    
            Parameters
            ----------
            start: int
                First row to delete. 0 based row number.
            end : int
                Last row to delete. 0 based row number. Default is None, meaning 
                from start to the last row.
    
            Returns
            -------
            bool
    
            Raise
            -----
            InputError:
                - When start > end
                - When end > number of rows in self
        """
        #region -------------------------------------------------> Check input
        #------------------------------> There is something to delete
        if (rowN := self.GetItemCount()) == 0:
            return True
        else:
            pass
        #------------------------------> start, end
        if end is not None:
            #------------------------------> 
            msg = (
            f'Values for start ({start}), end ({end}) and number of rows '
            f'({rowN}) in the wx.ListCtrl must comply with start <= end < '
            f'nrows. In addition, start and end must be integer numbers.')
            #------------------------------> 
            try:
                if dtsCheck.AInRange(end, refMin=start, refMax=rowN-1)[0]:
                    pass
                else:
                    raise dtsException.InputError(msg)
            except Exception:
                raise dtsException.InputError(msg)
            #------------------------------> 
            try:
                end = int(end) + 1
                start = int(start)
            except Exception:
                raise dtsException.InputError(msg)
        else:
            #------------------------------> 
            msg = (
            f'Values for start ({start}) and number of rows ({rowN}) in the '
            f'wx.ListCtrl must comply with start < nrows. In addition, start '
            f'must be an integer number')
            #------------------------------> 
            try:
                if dtsCheck.AInRange(start, refMax=rowN-1)[0]:
                    pass
                else:
                    raise dtsException.InputError(msg)
            except Exception:
                raise dtsException.InputError(msg)
            #------------------------------> 
            try:
                end = rowN
                start = int(start)
            except Exception:
                raise dtsException.InputError(msg)
        #endregion ----------------------------------------------> Check input
        
        #region -------------------------------------------------> Remove rows
        for r in range(start,end,1):
            self.DeleteItem(r)
        #endregion ----------------------------------------------> Remove rows
        
        return True
    #---

    def OnAll(self, event: 'wx.Event') -> bool:
        """Select all rows.

            Parameters
            ----------
            event : wx.Event
                Information about the event
                
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

    def OnCopy(self, event) -> bool:
        """Copy selected rows in the wx.ListCtrl to the clipboard.

            Parameters
            ----------
            event: wx.Event
                Information about the event
        
            Notes
            -----
            If self.copyFullContent, then data is dict with keys being the 
            selected row indexes and values a list with the rows's content from 
            left to right.
            If not, then data is a string with comma-separated selected row's 
            indexes 
        
        """
        #region ----------------------------------------------> Check can copy
        if self.canCopy:
            pass
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mwxLCtrNoCopy,
                nothing = None,
            )
            return False
        #endregion -------------------------------------------> Check can copy
        
        #region ----------------------------------------------------> Get data
        if self.copyFullContent:
            data = json.dumps(self.GetSelectedRows(content=self.copyFullContent))
        else:
            data = self.GetSelectedRows(content=self.copyFullContent)
            data = self.sep.join(map(str, [x for x in data.keys()]))
        dataObj = wx.TextDataObject(data)
        #endregion -------------------------------------------------> Get data
        
        #region -------------------------------------------> Copy to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mCopyFailedW,
                nothing = None,
            )
            return False
        #endregion ----------------------------------------> Copy to clipboard
        
        return True
    #---

    def OnCut(self, event) -> bool:
        """Cut selected rows in the wx.ListCtrl to the clipboard.

            Parameters
            ----------
            event: wx.Event
                Information about the event
                
            Notes
            -----
            See also self.OnCopy
        """
        #region -----------------------------------------------> Check can cut
        if self.canCut:
            pass
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mwxLCtrNoChange,
                nothing = None,
            )
            return False
        #endregion --------------------------------------------> Check can cut
        
        #region --------------------------------------------------------> Copy
        try:
            self.OnCopy(event)
        except Exception:
            return False		
        #endregion -----------------------------------------------------> Copy
        
        #region ------------------------------------------------------> Delete
        self.DeleteSelected()
        #endregion ---------------------------------------------------> Delete
                
        return True
    #---

    def OnPaste(self, event) -> bool:
        """Paste selected rows in the wx.ListCtrl to the clipboard.
        
            Parameters
            ----------
            event:
                Information about the event
        """
        #region ---------------------------------------------> Check can paste
        if self.canPaste:
            pass
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mwxLCtrNoChange,
                nothing = None,
            )
            return False
        #endregion ------------------------------------------> Check can paste
        
        #region ------------------------------------------> Get clipboard data
        #------------------------------> DataObj
        dataObj = wx.TextDataObject()
        #------------------------------> Get from clipboard
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(dataObj)
            wx.TheClipboard.Close()
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mPasteFailedW,
                nothing = None,
            )
            return False
        #------------------------------> Check success
        if success:
            pass
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mNothingToPasteW,
                nothing = None,
            )
            return False
        #------------------------------> Data
        data = json.loads(dataObj.GetText())
        #endregion ---------------------------------------> Get clipboard data
        
        #region --------------------------------------------------> Check Data
        if data is not None:
            for v in data.values():
                if len(v) == self.GetColumnCount():
                    break
                else:
                    dtsWindow.MessageDialog(
                        'warning', 
                        message = config.mwxLCtrlNColPaste,
                        nothing = None,
                    )
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
            if self.pasteUnique:
                if self.RowInList(row):
                    continue
                else:
                    pass
            else:
                pass
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
    #endregion ------------------------------------------------> Class methods
#---


class ListZebra(MyListCtrl, listmix.ListRowHighlighter):
    """A wx.ListCtrl with the zebra style and extra methods.

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        color : str
            Color for the zebra style
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.

        Notes
        -----        
        See MyListCtrl for more details.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, color: str=config.color['Zebra'], 
        colLabel: Optional[list[str]]=None, colSize: Optional[list[int]]=None, 
        canCopy: bool=True, canCut: bool=False, canPaste: bool=False, 
        copyFullContent: bool=False, sep: str=',', pasteUnique: bool=True, 
        selAll: bool=True, style=wx.LC_REPORT, data: list[list]=[],
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        MyListCtrl.__init__(self, parent, colLabel=colLabel, colSize=colSize, 
            canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
            copyFullContent=copyFullContent, sep=sep, pasteUnique=pasteUnique, 
            selAll=selAll, style=style, data=data, color=color,
        )

        listmix.ListRowHighlighter.__init__(
            self, 
            color,
        )
        #endregion --------------------------------------------> Initial setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    #endregion ------------------------------------------------> Class Methods
#---


class ListZebraMaxWidth(ListZebra, listmix.ListCtrlAutoWidthMixin):
    """A wx.ListCtrl with the zebra style and expanding last column

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        color : str
            Color for the zebra style
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.

        Attributes
        ----------
        zebraColor : str
            Default color for the zebra style in the wx.ListCtrl

        Notes
        -----
        See MyListCtrl for more details.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, color: str=config.color['Zebra'], 
        colLabel: Optional[list[str]]=None, colSize: Optional[list[int]]=None, 
        canCopy: bool=True, canCut: bool=False, canPaste: bool=False, 
        copyFullContent: bool=False, sep: str=',', pasteUnique: bool=True, 
        selAll: bool=True, style=wx.LC_REPORT, data: list[list]=[],
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        ListZebra.__init__(self, parent, color=color, colLabel=colLabel, 
            colSize=colSize, canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
            copyFullContent=copyFullContent, sep=sep, pasteUnique=pasteUnique, 
            selAll=selAll, style=style, data=data,
        )

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        #endregion --------------------------------------------> Initial setup
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ButtonClearAll():
    """wx.Button to set the values of all child widget (wx.TextCtrl and 
        wx.ComboBox) of a parent to an empty string. All elements of 
        wx.ListCtrl childs will be deleted

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
            parent

        Attributes
        ----------
        btnClearAll : wx.Button
            Buton to clear all user input
        delParent: wx.Window
            This is the widget whose children values will be set to ''
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, delParent: Optional[wx.Window]=None, 
        label: str='Clear All', tooltip: Optional[str]=None,
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.delParent = parent if delParent is None else delParent
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.btnClearAll = wx.Button(parent, label=label)
        if tooltip is not None:
            self.btnClearAll.SetToolTip(tooltip)
        else:
            pass    
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.btnClearAll.Bind(wx.EVT_BUTTON, self.OnClear)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnClear(self, event: wx.CommandEvent) -> Literal[True]:
        """ Set the values of all child widgets of delParent to '' and delete
            all items of wx.ListCtrl.

            Parameters
            ----------
            event: wx.Event
                Information about the wx.EVT_BUTTON
        """
        ClearInput(self.delParent)
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ButtonRun():
    """Creates the button to start an analysis. It contains the methods for the
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
        deltaT : str or None
            Time used by the analysis
        btnRun : wx.Button
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
        RunAnalysis()
            Run the actual analysis. Override as needed.
        WriteOutput()
            Write output files. Override as needed.
        LoadResults()
            Load results. Override as needed.
        EndRun()
            Restart GUI and variables. Override as needed.
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, label: str='Run', 
        tooltip: Optional[str]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.deltaT = None
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.btnRun = wx.Button(parent, label=label)
        if tooltip is not None:
            self.btnRun.SetToolTip(tooltip)
        else:
            pass
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.btnRun.Bind(wx.EVT_BUTTON, self.OnRun)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnRun(self, event: wx.CommandEvent) -> Literal[True]:
        """ Start new thread to run the analysis. Override as needed.
        
            Parameter
            ---------
            event : wx.Event
                Receive the button event
        """
        #region -----------------------------------------------> Initial Setup
        #endregion --------------------------------------------> Initial Setup
        
        #region ------------------------------------------------------> Thread
        _thread.start_new_thread(self.Run, ('test',))
        #endregion ---------------------------------------------------> Thread

        return True
    #---

    def Run(self, test: str) -> bool:
        """Run the analysis's steps
        
            Parameters
            ----------
            test: str
                Just needed by _thread.start_new_thread
                
            Notes
            -----
            Messages to the status bar of the app can be set in the individual
            step methods
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

        end = datetime.now()
        self.deltaT = datetime.utcfromtimestamp(
            (end-start).total_seconds()
        ).strftime("%H:%M:%S")

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

    def RunEnd(self) -> Literal[True]:
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
    """Creates the Help button. The button leads to an online resource

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
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, url: str, label: str='Help',
        tooltip: Optional[str]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.url = url
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.btnHelp = wx.Button(parent, label=label)
        if tooltip is not None:
            self.btnHelp.SetToolTip(tooltip)
        else:
            pass
        #endregion --------------------------------------------------> Widgets

        #region --------------------------------------------------------> Bind
        self.btnHelp.Bind(wx.EVT_BUTTON, self.OnHelp)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnHelp(self, event: wx.CommandEvent) -> Literal[True]:
        """Leads to self.url

            Parameters
            ----------
            event : wx.EVENT
                Information about the event
        """
        #region ----------------------------------------------------> Open web
        try:
            webbrowser.open_new_tab(self.url)
        except Exception as e:
            raise e        
        #endregion -------------------------------------------------> Open web
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class MatPlotPanel(wx.Panel):
    """Panel with a matplotlib plot.

        Parameters
        ----------
        parent : wx widget or none
            Parent of the panel
        dpi : int
            DPI for the plot. Default is 300
        statusbar : wx.StatusBar
            wx.StatusBar to display information about the graph
        statusMethod: callable or None
            Method to print information to the statusbar. The method should 
            accept only one parameter, the matplotlib event. Default is None.

        Attributes
        ----------
        axes: 
            Axes in the canvas.
        canvas : FigureCanvas
            Canvas in the panel.
        dpi : int
            DPI for the plot. Default is 300
        figure: mpl.Figure
            Figure in the panel
        statusbar : wx.StatusBar
            wx.StatusBar to display information about the graph
        finalX : float
            x coordinate in the plot scale when drag is over
        finalY : float
            y coordinate in the plot scale when drag is over
        initX : float
            x coordinate in the plot scale when left click is pressed
        initY : float
            y coordinate in the plot scale when left click is pressed
        zoomRect : mpl.patches.Rectangle or None
            Rectangle to show the zoom in area
        zoomReset : dict
            Cero zoom axes configuration. This will be used to reset the zoom 
            level. {'x' : (xmin, xmax), 'y': (ymin, ymax)}
        statusMethod: callable or None
            Method to print information to the statusbar. The method should 
            accept only one parameter, the matplotlib event. Default is None
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, dpi: Optional[int]=None, 
        statusbar: Optional[wx.StatusBar]=None, 
        statusMethod: Optional[Callable]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.dpi          = 100 if dpi is None else dpi
        self.statusbar    = statusbar
        self.statusMethod = statusMethod
        self.initY        = None
        self.initX        = None
        self.finalX       = None
        self.finalY       = None
        self.zoomRect     = None
        self.zoomReset    = None
        self.cid          = []
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.figure  = mpl.figure.Figure(
            dpi          = self.dpi,
            figsize      = (2, 2),
            tight_layout = True,
        )
        self.axes    = self.figure.add_subplot(111)
        self.canvas  = FigureCanvas(self, -1, self.figure)
        self.axes.set_axisbelow(True)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sizerPlot = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerPlot.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizerPlot)
        self.sizerPlot.Fit(self)
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
            wx.EVT_MENU, self.ZoomResetPlot, id=accel['Zoom'].GetCommand())
        self.Bind(
            wx.EVT_MENU, self.OnSaveImage, id=accel['Img'].GetCommand())
        #--------------> Add 
        self.SetAcceleratorTable(
            wx.AcceleratorTable([x for x in accel.values()])
        )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def ConnectEvent(self) -> bool:
        """Connect or Disconnect all event handlers.
    
            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Connect events
        self.cid.append(
            self.canvas.mpl_connect('motion_notify_event', self.OnMotionMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('button_press_event', self.OnPressMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('button_release_event', self.OnReleaseMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('key_press_event', self.OnKeyPress)
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
        for k in self.cid:
            self.canvas.mpl_disconnect(k)
        #endregion -----------------------------------------------> Disconnect
        
        #region --------------------------------------------------> Reset list
        self.cid = []
        #endregion -----------------------------------------------> Reset list
        
        return True
    #---
    
    def GetAxesXY(self, event) -> tuple[float, float]:
        """"""
        x = event.xdata
        if getattr(self, 'axes2', None) is not None:
            _, y = self.axes.transData.inverted().transform((event.x,event.y))
        else:
            y = event.ydata
        
        return (x,y)
    #---
    
    #--------------------------------------------------------> Key press event
    def OnKeyPress(self, event) -> Literal[True]:
        """Process a key press event
    
            Parameter
            ---------
            event: mpl.KeyEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if (tKey:= event.key) == 'escape':
            self.ZoomInAbort(event) 
        else:
            pass
        #endregion ----------------------------------------------------> Event

        return True
    #---

    #-----------------------------------------------------> Press mouse button
    def OnPressMouse(self, event) -> Literal[True]:
        """Process press mouse event
        
            Parameter
            ---------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.inaxes:
            if event.button == 1:
                self.OnLeftClick(event)
            elif event.button == 3:
                self.OnRightClick(event)
            else:
                pass
        else:
            pass
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    def OnLeftClick(self, event) -> Literal[True]:
        """Process left click event. Override as needed.
            
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        self.initX, self.initY = self.GetAxesXY(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnRightClick(self, event) -> Literal[True]:
        """Process right click event. Override as needed
            
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        return True
    #---

    #------------------------------------------------------> Move mouse button
    def OnMotionMouse(self, event) -> Literal[True]:
        """Handle move mouse event

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.button == 1:
            self.DrawZoomRect(event)
        else:
            if self.statusbar is not None:
                self.UpdateStatusBar(event)
            else:
                pass        
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    def DrawZoomRect(self, event) -> bool:
        """Draw a rectangle to highlight area that will be zoomed in
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
    
        """
        #region -----------------------------------------> Check event in axes
        if event.inaxes:
            pass
        else:
            return False
        #endregion --------------------------------------> Check event in axes

        #region -----------------------------------------> Initial coordinates
        if self.initX is None:
            self.initX, self.initY = self.GetAxesXY(event)
        else:
            pass
        #endregion --------------------------------------> Initial coordinates
        
        #region -------------------------------------------> Final coordinates
        self.finalX, self.finalY = self.GetAxesXY(event)
        #endregion ----------------------------------------> Final coordinates

        #region ------------------------------------> Delete & Create zoomRect
        #------------------------------> 
        if self.zoomRect is not None:
            self.zoomRect.remove()
        else:
            pass
        #------------------------------> 
        self.zoomRect = patches.Rectangle(
            (min(self.initX, self.finalX), min(self.initY, self.finalY)),
            abs(self.initX - self.finalX),
            abs(self.initY - self.finalY),
            fill      = False,
            linestyle = '--',
            linewidth = '0.5'
        )
        #endregion ---------------------------------> Delete & Create zoomRect

        #region --------------------------------------------------> Add & Draw
        self.axes.add_patch(
            self.zoomRect
        )
        self.canvas.draw()
        #endregion -----------------------------------------------> Add & Draw

        return True
    #---

    def UpdateStatusBar(self, event):
        """To update status bar. Basic functionality. Override as needed 
        
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.inaxes:
            if self.statusMethod is not None:
                self.statusMethod(event)
            else:
                x,y = self.GetAxesXY(event)
                self.statusbar.SetStatusText(
                    f"x={x:.2f} y={y:.2f}"
                )
        else:
            self.statusbar.SetStatusText('') 
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    #---------------------------------------------------> Release mouse button
    def OnReleaseMouse(self, event) -> Literal[True]:
        """Process a release mouse event 
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region ---------------------------------------------------> Event
        if event.button == 1:
            self.OnLeftRelease(event)
        elif event.button == 3:
            self.OnRightRelease(event)
        else:
            pass
        #endregion ------------------------------------------------> Event
        
        return True
    #---

    def OnLeftRelease(self, event) -> Literal[True]:
        """Process a left button release event
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -----------------------------------------------------> Zoom in
        if self.finalX is not None:
            self.axes.set_xlim(
                min(self.initX, self.finalX), 
                max(self.initX, self.finalX),
            )
            self.axes.set_ylim(
                min(self.initY, self.finalY), 
                max(self.initY, self.finalY),
            )
        else:
            return True
        #endregion --------------------------------------------------> Zoom in
        
        #region -----------------------------------> Reset initial coordinates
        self.initY  = None
        self.initX  = None
        self.finalX = None
        self.finalY = None
        #endregion --------------------------------> Reset initial coordinates
        
        #region --------------------------------------------> Delete zoom rect
        self.ZoomRectDelete()
        #endregion -----------------------------------------> Delete zoom rect
        
        return True
    #---

    def OnRightRelease(self, event) -> Literal[True]:
        """Process a right button release event. Override as needed.
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        return True
    #---
    
    def OnSaveImage(self, event) -> bool:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        return self.SaveImage(config.elMatPlotSaveI, parent=self, message=None)
    #---

    #---------------------------------------------------> Zoom related methods
    def ZoomResetSetValues(self) -> Literal[True]:
        """Set the axis limit in the cero zoom state. Should be called after all 
            initial plotting and axis configuration is done.
        
            Returns
            -------
            dict:
                {'x' : (xmin, xmax), 'y': (ymin, ymax)}
        """
        self.zoomReset = {'x': self.axes.get_xlim(), 'y': self.axes.get_ylim()}

        return True
    #---

    def ZoomResetPlot(
        self, event:Optional[wx.CommandEvent]=None) -> Literal[True]:
        """Reset the zoom level of the plot 
        
            Parameters
            ----------
            event: wx.Event or None
                To call from keyboard shortcut or as regular function
                
            Return
            ------
            True
        """
        #------------------------------> 
        self.axes.set_xlim(self.zoomReset['x'])
        self.axes.set_ylim(self.zoomReset['y'])
        self.canvas.draw()
        
        return True
    #---

    def ZoomInAbort(self, event) -> Literal[True]:
        """Abort a zoom in operation when Esc is pressed 
        
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #------------------------------> 
        self.initX  = None
        self.initY  = None
        self.finalX = None
        self.finalY = None
        #------------------------------> 
        self.ZoomRectDelete()
        #------------------------------> 
        self.UpdateStatusBar(event)
        
        return True
    #---

    def ZoomRectDelete(self) -> Literal[True]:
        """Delete the zoom in rectangle"""
        #region --------------------------------------------------------> Rect
        if self.zoomRect is not None:
            self.zoomRect.remove()
            self.canvas.draw()
            self.zoomRect = None
        else:
            pass        
        #endregion -----------------------------------------------------> Rect
        
        return True
    #---
    
    def SaveImage(
        self, ext: str, parent: Optional[wx.Window]=None, 
        message: Optional[str]=None
        ) -> Literal[True]:
        """Save image of the plot
    
            Parameters
            ----------
            ext : file extension
                wxPython extension spec
            parent : wx.Widget or None
                To center the save dialog. Default is None
            message : str or None
                Title for the save file window. Default is None
        """
        #region ------------------------------------------------------> Dialog
        dlg = dtsWindow.FileSelectDialog(
            'save',
            ext,
            parent  = parent,
            message = message,
        )
        #endregion ---------------------------------------------------> Dialog
        
        #region ----------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                self.figure.savefig(path, dpi=self.dpi)
            except Exception:
                raise dtsException.ExecutionError(
                    f"The image of the plot could not be saved to file:\n"
                    f"{path}"
                )
        else:
            pass
        #endregion -------------------------------------------------> Get Path
        
        #region ---------------------------------------------------> Destroy
        dlg.Destroy()
        #endregion ------------------------------------------------> Destroy
        
        return True	
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ---------------------------------------------------> Single widgets


#region ---------------------------------------------------------> Mix widgets
class StaticBoxes():
    """Creates the three main static boxes Files, User values and Columns.

        Parameters
        ----------
        parent: wx widget
            Parent of the widgets.
        rightDelete : Boolean
            Delete user input with right click (True) or not.
        labelF : str or None
            Label of the wx.StaticBox. If None the wx.StaticBox and associated
            sizers will not be created.
        labelD : str or None
            Label of the wx.StaticBox. If None the wx.StaticBox and associated
            sizers will not be created.
        labelV : str or None
            Label of the wx.StaticBox. If None the wx.StaticBox and associated
            sizers will not be created.
        labelC : str or None
            Label of the wx.StaticBox. If None the wx.StaticBox and associated
            sizers will not be created.

        Attributes
        ----------
        Depending on the values of labelF, labelV and labelC, the corresponding
        attributes may not be created

        sbFile : wx.StaticBox
            StaticBox to contain the input/output file information
        sbData : wx.StaticBox
            StaticBox to contain the data preparation information.
        sbValue : wx.StaticBox
            StaticBox to contain the user-defined values
        sbColumn : wx.StaticBox
            StaticBox to contain the column numbers in the input files
        sizersbFile : wx.StaticBoxSizer
            StaticBoxSizer for sbFile
        sizersbData : wx.StaticBoxSizer
            StaticBoxSizer for sbData
        sizersbValue : wx.StaticBoxSizer
            StaticBoxSizer for sbValue
        sizersbColumn : wx.StaticBoxSizer
            StaticBoxSizer for sbColumn
        sizersbFileWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbFile
        sizersbDataWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbData
        sizersbValueWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbValue
        sizersbColumnWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbColumn
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup	

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, rightDelete: bool=True,
        labelF: Optional[str]='Files && Folders',
        labelD: Optional[str]='Data preparation',
        labelV: Optional[str]='User-defined values',
        labelC: Optional[str]="Columns in the main file",
        ) -> None:
        """"""
        #region ----------------------------------------------> File & Folders
        if labelF is not None:
            #------------------------------> 
            self.sbFile = wx.StaticBox(parent, label=labelF)
            #------------------------------> 
            self.sizersbFile    = wx.StaticBoxSizer(self.sbFile, wx.VERTICAL)
            self.sizersbFileWid = wx.GridBagSizer(1, 1)
            self.sizersbFile.Add(
                self.sizersbFileWid,  
                border = 2,
                flag   = wx.EXPAND|wx.ALL
            )
            #------------------------------> 
            if rightDelete:
                self.sbFile.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.sbFile.SetToolTip(config.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion -------------------------------------------> File & Folders
        
        #region --------------------------------------------> Data Preparation
        if labelD is not None:
            #------------------------------> 
            self.sbData = wx.StaticBox(parent, label=labelD)
            #------------------------------> 
            self.sizersbData    = wx.StaticBoxSizer(self.sbData, wx.VERTICAL)
            self.sizersbDataWid = wx.GridBagSizer(1, 1)
            self.sizersbData.Add(
                self.sizersbDataWid,  
                border = 2,
                flag   = wx.EXPAND|wx.ALL
            )
            #------------------------------> 
            if rightDelete:
                self.sbData.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.sbData.SetToolTip(config.ttSectionRightClick)
                
            else:
                pass
        else:
            pass
        #endregion -----------------------------------------> Data Preparation
        
        #region ------------------------------------------------------> Values
        if labelV is not None:
            #------------------------------> 
            self.sbValue  = wx.StaticBox(parent, label=labelV)
            #------------------------------> 
            self.sizersbValue    = wx.StaticBoxSizer(self.sbValue, wx.VERTICAL)
            self.sizersbValueWid = wx.GridBagSizer(1, 1)
            self.sizersbValue.Add(
                self.sizersbValueWid,  
                border = 2,
                flag   = wx.EXPAND|wx.ALL
            )
            #------------------------------> 
            if rightDelete:
                self.sbValue.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.sbValue.SetToolTip(config.ttSectionRightClick)
            else:
                pass
        else:
            pass
        #endregion ---------------------------------------------------> Values
        
        #region -----------------------------------------------------> Columns
        if labelC is not None:
            #------------------------------> 
            self.sbColumn = wx.StaticBox(parent, label=labelC)
            #------------------------------> 
            self.sizersbColumn = wx.StaticBoxSizer(self.sbColumn, wx.VERTICAL)
            self.sizersbColumnWid = wx.GridBagSizer(1, 1)
            self.sizersbColumn.Add(
                self.sizersbColumnWid,  
                border = 2,
                flag   = wx.EXPAND|wx.ALL
            )
            #------------------------------> 
            if rightDelete:
                self.sbColumn.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDelete)
                self.sbColumn.SetToolTip(config.ttSectionRightClick)
                
            else:
                pass
        else:
            pass
        #endregion --------------------------------------------------> Columns
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnRightDelete(self, event: wx.MouseEvent) -> Literal[True]:
        """Reset content of all childs of the widgets calling the event
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
        """
        return ClearInput(event.GetEventObject())
    #---
    #endregion ------------------------------------------------> Class Methods
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
        btnHelp : wx.Button
            Help button
        btnClearAll : wx.Button
            Button to clear the input in a pane
        btnRun : wx.Button
            Button to start the main action in a pane
        btnSizer : wx.FlexGridSizer
            To align the buttons
        url : str
            URL to show
            
        Notes
        -----
        If setSizer is True, buttons are arranged horizontally in a 
        wx.FlexGridSizer
    """

    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup	

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, url: str, labelH: str='Help',
        tooltipH: Optional[str]=None, labelC: str='Clear All', 
        tooltipC: Optional[str]=None, delParent: Optional[wx.Window]=None, 
        labelR: str='Run', tooltipR: Optional[str]=None, setSizer: bool=True
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
            self.btnSizer = wx.FlexGridSizer(1, 3, 1, 1)
            self.btnSizer.Add(
                self.btnHelp,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
            self.btnSizer.Add(
                self.btnClearAll,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
            self.btnSizer.Add(
                self.btnRun,
                border = 10,
                flag   = wx.EXPAND|wx.ALL
            )
        else:
            self.btnSizer = None
        #endregion ---------------------------------------------------> Sizers
    #endregion -----------------------------------------------> Instance setup
#---


class ButtonTextCtrl():
    """Creates a wx.Button and wx.TextCtrl

        Parameters
        ----------
        parent : wx widget or None
            Parent of the widgets
        setSizer : boolean
            Set (True) or not (False) a sizer for the widgets
        btnLabel : str
            Label for the button. Default is 'Button'
        btnTooltip : str or None
            Tooltip for the wx.Button. Default is None.
        tcSize : wx.Size
            Size of the wx.TextCtrl. Default is (300, 22)
        tcStyle : wx style
            Default to 0
        tcHint: str
            Hint for the wx.TextCtrl. Default is ''
        validator : wx.Validator or None
            To validate input for wx.TexCtrl
        ownCopyCut : boolean
            Use own implementation of Copy (Ctrl/Cmd C) and Cut (Ctrl/Cmd X) 
            methods. Usefull to delete wx.TextCtrl when style is wx.TE_READONLY 
        
        Attributes
        ----------
        btn : wx.Button
        tc : wx.TextCtrl
        Sizer : wx.BoxSizer or None
        
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
        self, parent: wx.Window, setSizer: bool=False, btnLabel: str='Button', 
        btnTooltip: Optional[str]=None, tcStyle=0, tcHint: str='', 
        tcSize: wx.Size=(300, 22), validator: Optional[wx.Validator]=None, 
        ownCopyCut: bool=False,
        ) -> None:
        """	"""
        #region -----------------------------------------------> Initial Setup
        self.parent = parent
        #endregion --------------------------------------------> Initial Setup
        
        #region -----------------------------------------------------> Widgets
        #--------------> 
        self.btn = wx.Button(
            parent = parent,
            label  = btnLabel,
        )
        if btnTooltip is not None:
            self.btn.SetToolTip(btnTooltip)
        else:
            pass
        #--------------> 
        self.tc = wx.TextCtrl(
            parent    = parent,
            value     = "",
            style     = tcStyle,
            size      = tcSize,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        self.tc.SetHint(tcHint)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.btn, 0, wx.EXPAND|wx.ALL, 5)
            self.Sizer.Add(self.tc, 1, wx.EXPAND|wx.ALL, 5)
        else:
            self.Sizer = None
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.btn.Bind(wx.EVT_BUTTON, self.OnBtn)
        #------------------------------> 
        if ownCopyCut:
            #------------------------------> 
            accel = {
                'Copy' : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('C'), wx.NewId()),
                'Cut'  : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('X'), wx.NewId()),
            }
            #------------------------------> 
            self.tc.Bind(wx.EVT_MENU, self.OnCopy,  id=accel['Copy'].GetCommand())
            self.tc.Bind(wx.EVT_MENU, self.OnCut,   id=accel['Cut'].GetCommand())    
            #------------------------------> 
            self.tc.SetAcceleratorTable(
                wx.AcceleratorTable([x for x in accel.values()])
            )
        else:
            pass
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnBtn(self, event:wx.CommandEvent) -> Literal[True]:
        """Action to perform when button is clicked.

            Override as needed

            Parameter
            ---------
            event : wx.Event
                Event information
        """
        return True
    #---

    def OnCopy(self, event: 'wx.Event') -> bool:
        """Copy wx.TextCtrl content
        
            Parameters
            ----------
            event: wx.Event
                Information about the event
        """
        #region ----------------------------------------------------> Get data
        data = self.tc.GetValue()
        dataObj = wx.TextDataObject(data)
        #endregion -------------------------------------------------> Get data

        #region -------------------------------------------> Copy to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        else:
            dtsWindow.MessageDialog(
                'warning', 
                message = config.mCopyFailedW,
                nothing = None,
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
        self.tc.SetValue('')
        #endregion ----------------------------------------------------> Clear
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ButtonTextCtrlFF(ButtonTextCtrl):
    """Creates a wx.Button and wx.TextCtrl

        Parameters
        ----------
        parent : wx widget or None
            Parent of the widgets
        setSizer : boolean
            Set (True) or not (False) a sizer for the widgets. Default is False
        btnLabel : str
            Label for the button. Default is 'Button'
        btnTooltip : str or None
            Tooltip for the wx.Button. Default is None.
        tcSize : wx.Size
            Size of the wx.TextCtrl. Default is (300, 22)
        tcStyle : wx style
            Default to wx.TE_PROCESS_ENTER
        tcHint: str
            Hint for the wx.TextCtrl. Default is ''
        mode : str
            One of 'openO', 'openM', 'save', 'folder'. The first three values 
            are used in dat4s_core.widget.wx_window.FileSelectDialog.mode.
            Default is 'openO'.
        ext : wx extension specification or None
            The extension of the file to open or save. In these cases it cannot 
            be None. Default is None
        validator : wx.Validator or None
            To validate input for wx.TexCtrl. Default is None
        ownCopyCut : Boolean
            Bind own Cut/Copy methods. Default is False.
        defPath: Path, str or None
            Folder path to look for files or folders.
        afterBtn : callable or None
            Method to call after FF is selected and wx.TexCtrl is filled. It
            must accept a fileP argument. Default is None
        
        Attributes
        ----------
        btn : wx.Button
        tc: wx.TextCtrl
        parent : wx widget or None
            Parent of the widgets
        mode : str
            One of 'openO', 'openM', 'save', 'folder'. The first three values 
            are used in dat4s_core.widget.wx_window.FileSelectDialog.mode
        ext : wxPython extension spec or None
        afterBtn : callable or None
            Method to call after FF is selected and wx.TexCtrl is filled. It
            must accept a fileP argument
        
        Raises
        ------
        InputError:
            - When mode is 'openO', 'openM' or 'save' and ext is None
            - When mode is not one of 'openO', 'openM', 'save', 'folderO' or
                'folderM'
                
        Notes
        -----
        The wx.TextCtrl is placed to the right of the wx.Button. The wx.Button 
        is used to select a file or folder for input or output. The path to the 
        selected item is shown in the wx.TextCtrl. After this the given afterBtn 
        method is executed
    """

    #region -----------------------------------------------------> Class setup

    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, setSizer: bool=False, btnLabel: str='Button',
        btnTooltip: Optional[str]=None, tcSize=(300, 22), 
        tcStyle=wx.TE_PROCESS_ENTER, tcHint: str='', 
        mode: Literal['openO', 'openM', 'save', 'folder']='openO', 
        ext: str=None, validator: Optional[wx.Validator]=None, 
        ownCopyCut: bool=False, afterBtn: Optional[Callable]=None,
        defPath: Union[Path, str, None]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial setup
        self.mode     = mode
        self.ext      = ext
        self.afterBtn = afterBtn
        self.defPath: Union[Path, str, None] = (
            str(defPath) if defPath is not None else defPath)

        super().__init__(parent=parent, setSizer=setSizer, btnLabel=btnLabel, 
            btnTooltip=btnTooltip, tcSize=tcSize, tcStyle=tcStyle, 
            tcHint=tcHint, validator=validator, ownCopyCut=ownCopyCut)
        #endregion --------------------------------------------> Initial setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnBtn(self, event: wx.CommandEvent) -> bool:
        """Action to perform when button is clicked.

            Parameter
            ---------
            event : wx.Event
                Event information
                
            Notes
            -----
            Overridden method.
        """
        #region ------------------------------------------> Select file/folder
        if self.mode != 'folder':
            dlg = dtsWindow.FileSelectDialog(
                self.mode, self.ext, parent=self.parent, defPath=self.defPath,
            )
        else:
            dlg = dtsWindow.DirSelectDialog(
                parent=self.parent, defPath=self.defPath,
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.tc.SetValue(path)
            dlg.Destroy()
        else:
            dlg.Destroy()
            return False
        #endregion ---------------------------------------> Select file/folder

        #region ---------------------------------------------> After selection
        if self.afterBtn is not None:
            try:
                self.afterBtn(Path(path))
            except Exception as e:
                raise e
        #endregion ------------------------------------------> After selection

        return True
    #---

    def OutputPath(
        self, out: Union[Path, str], defVal: str, unique: bool=True, 
        returnTimeStamp: bool=True
        ) -> Union[Path, tuple[Path, str]]:
        """Creates the path for the output file. 
        
            It is meant to be call from the input file widgets. If unique is 
            True and file/folder exists, then add current datetime to the name 
            to make it unique.
    
            Parameters
            ----------
            out: str
                If empty string '' then uses the self.tc value and defVal to 
                build the path to the output file
            defVal : str
                Default name for the output file or folder
            unique : boolean
                Check file or folder does not exist. If it does add the datetime
                to the name to make it unique.
            returnTimeStamp: bool    
                Return the timestamp used to create the unique name in the 
                outputpath.
    
            Returns
            -------
            str:
                Path to the output file or folder
                
            Raises
            ------
            See dtsFF.OutputPath
        """
        try:
            return dtsFF.OutputPath(
                self.tc.GetValue(), 
                out, 
                defVal, 
                unique          = unique,
                returnTimeStamp = returnTimeStamp,
            )
        except Exception as e:
            raise e
    #---
    #endregion ------------------------------------------------> Class methods
#---


class StaticTextCtrl():
    """Creates a wx.StaticText and a wx.TextCtrl.
    
        The wx.TextCtrl is placed to the right of the wx.StaticText if a sizer
        is created.
    
        Parameters
        ----------
        parent : wx widget or None
            Parent of the widgets
        setSizer : boolean
            Set (True) or not (False) a sizer for the widgets
        stLabel : str
            Label for the wx.StaticText. Default is 'Text'
        stTooltip : str or None
            Tooltip for the wx.StaticText. Default is None.
        tcSize : wx.Size
            Size of the wx.TextCtrl. Default is (300, 22)
        tcHint: str
            Hint for the wx.TextCtrl. Default is '' 
        validator : wx.Validator or None
            To validate input for wx.TexCtrl

        Attributes
        ----------
        st : wx.StaticText
            The wx.StaticText
        tc : wx.TextCtrl
            The wx.TextCtrl
        Sizer : wx.BoxSizer or None
        
        Notes
        -----
        If setSizer is True, buttons are arranged horizontally in a 
        wx.BoxSizer
    """

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, setSizer: bool=False, stLabel: str='Text', 
        stTooltip: Optional[str]=None, tcSize=(300, 22), tcHint: str='', 
        tcStyle = 0, validator: Optional[wx.Validator]=None,
        ) -> None:
        """"""
        #region -----------------------------------------------------> Widgets
        #--------------> 
        self.st = wx.StaticText(
            parent = parent,
            label  = stLabel,
        )
        if stTooltip is not None:
            self.st.SetToolTip(stTooltip)
        else:
            pass
        #--------------> 
        self.tc = wx.TextCtrl(
            parent    = parent,
            value     = "",
            size      = tcSize,
            style     = tcStyle,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        self.tc.SetHint(tcHint)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.st, 0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.Sizer.Add(self.tc, 1, wx.EXPAND|wx.ALL, 5)
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
        parent : wx Widget
            Parent of the widgets
        label : str
            Text for the wx.StaticText
        tooltip : str or None
            Tooltip for the wx.StaticText. Default is None.
        options : list of str
            Options for the wx.ComboBox
        validator : wx.Validator or None
            Validator for the wx.ComboBox. Default is wx.DefaultValidator
        setSizer : boolean
            Set (True) or not (False) a sizer for the widgets
        styleCB: wx.Style
            Style of the wx.ComboBox

        Attributes
        ----------
        st : wx.StaticText
            Label for the wx.ComboBox
        cb : wx.ComboBox
        
        Notes
        -----
        The wx.ComboBox is placed to the right of the wx.StaticText if a sizer
        is created
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, label: str, choices: list[str], value: str='',
        tooltip: Optional[str]=None, styleCB=wx.CB_READONLY, setSizer=False,
        validator: Optional[wx.Validator]=None,
        ) -> None:
        """ """
        #region -------------------------------------------------> Check input
        #endregion ----------------------------------------------> Check input

        #region -----------------------------------------------> Initial Setup
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #--------------> 
        self.st = wx.StaticText(parent, label=label)
        if tooltip is not None:
            self.st.SetToolTip(tooltip)
        else:
            pass
        #--------------> 
        self.cb = wx.ComboBox(parent, 
            value     = value,
            choices   = choices,
            style     = styleCB,
            validator = wx.DefaultValidator if validator is None else validator,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Sizer.Add(self.st, 0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.Sizer.Add(self.cb, 1, wx.EXPAND|wx.ALL, 5)
        else:
            self.Sizer = None
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ListCtrlSearch():
    """Creates a wx.ListCtrl with a wx.SearchCtrl beneath it.
    
        See Notes below for more details

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        listT : 0, 1 or 2
            Type of wx.ListCtrl. 
        setSizer : bool
            Arrange widgets in self.Sizer. Default is True.
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color : str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        tcHint : str
            Hint for the wx.TextCtrl

        Attributes
        ----------
        listTDict: dict
            Keys are 0,1,2 and methods the class for the wx.ListCtrl.
        lc : wx.ListCtrl
        search : wx.SearchCtrl
    """
    #region -----------------------------------------------------> Class setup
    listTDict = {
        0: MyListCtrl,
        1: ListZebra,
        2: ListZebraMaxWidth,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, listT: int=1, setSizer=True, 
        color: str=config.color['Zebra'], colLabel: Optional[list[str]]=None, 
        colSize: Optional[list[int]]=None, canCopy: bool=True, 
        canCut: bool=False, canPaste: bool=False, copyFullContent: bool=False, 
        sep: str=',', pasteUnique: bool=True, selAll: bool=True, 
        style=wx.LC_REPORT, data: list[list]=[], tcHint: str='',
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
            
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ListCtrl
        self.lc = self.listTDict[listT](
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
        self.search = wx.SearchCtrl(parent)
        self.search.SetHint(tcHint) if tcHint != '' else ''
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            #------------------------------> 
            self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
            #------------------------------> 
            self.Sizer.Add(self.lc, 1, wx.EXPAND|wx.ALL, 5)
            self.Sizer.Add(self.search, 0, wx.EXPAND|wx.ALL, 5)
        else:
            pass
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods

    #endregion ------------------------------------------------> Class methods
#---
#endregion ------------------------------------------------------> Mix widgets




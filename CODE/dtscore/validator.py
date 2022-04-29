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


"""Field validators for wxPython widgets. 
    The validators and methods return a tuple like: 
    (True, None)
    (False, None) when there is no single offending value or this makes no sense
        like in IsNotEmpty
    (False, (code, value/None, msg)) code indicates the section of the 
        validation that failed, value is the value raising the error and msg
        is a general msg about the error.
"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Literal, Optional, Union

import wx

import config.config as config
import dtscore.check as dtsCheck
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------------------------> Validator
class InputFF(wx.Validator):
    """Check widget holds the path to an input file/folder

        Parameters
        ----------
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'folder'.
        opt : Boolean
            Value is optional. Default is False.
        ext : list of str or None
            If fof is 'folder' then check if files with 'ext' are present inside
            the folder. ext must be like ['.corr', '.txt', ...]. 
            Default is None.

        Return by Validate method
        -------------------------
        tuple
            - (True, None)
            - (False, (code, path, msg))
                code is:
                - NotPath,   Input is not valid path
                - NotFile,   Input is not valid file
                - NotDir,    Input is not valid folder
                - NoRead,    Input cannot be read
                - FileExt,   Input does not have the required extension
                - FolderExt, Input does not contain any file with the given ext
                - (ExceptionRaised, ExceptionName): Check method raised an exception.

        Attributes
        ----------
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'folder'.
        opt : Boolean
            Value is optional. Default is False.
        ext : list of str or None
            If fof is 'folder' then check if files with 'ext' are present inside
            the folder. ext must be like ['.corr', '.txt', ...]. 
            Default is None.

        Raises
        ------
        InputError
            - When fof is not in config.oFoF
            - When ext is not list, tuple or None
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, fof: Literal['file', 'folder']='folder', opt: bool=False, 
        ext: Optional[list[str]]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.fof = fof
        self.opt = opt
        self.ext = ext

        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self) -> wx.Validator:
        """Overridden method"""
        return InputFF(
            fof = self.fof,
            opt = self.opt,
            ext = self.ext,
        )
    #---

    def Validate(self) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """Overridden method"""
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return dtsCheck.Path2FFInput(value, self.fof, self.opt, self.ext)
        except Exception as e:
            return (False, ('ExceptionRaised', type(e).__name__, str(e)))
        #endregion -------------------------------------------------> Validate
    #---
    
    def TransferToWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---

    def TransferFromWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---
    #endregion ---------------------------------------------> Override methods
#---


class OutputFF(wx.Validator):
    """Validates a widget holding the path to an output file/folder

        Parameters
        ----------
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'.
        opt : Boolean
            Value is optional. Default is True.
        ext : str or None
            If fof is 'folder' then check if files with 'ext' are present inside
            the folder. ext must be like '.corr'. Default is None.	

        Returns by Validate method
        --------------------------
        tuple
            - (True, None)
            - (False, (code, path, msg))
                code is:
                - NotPath,         Input is not a valid path
                - FileExt,         Incorrect file extension
                - NoWrite,         It is not possible to write	
                - (ExceptionRaised, ExceptionName): Check method raised an exception.
                
        Attributes
        ----------
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'
        opt : Boolean
            Value is optional. Default is True.
        ext : str or None
            File extension. ext must be like '.corr'. Default is None.
            
        Raises
        ------
        InputError
            - When fof is not in config.oFoF
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, fof: Literal['file', 'folder']='file', opt: bool=True, 
        ext: Optional[str]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.fof = fof
        self.opt = opt
        self.ext = ext

        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self) -> wx.Validator:
        """Overridden method"""
        return OutputFF(
            fof = self.fof,
            opt = self.opt,
            ext = self.ext,
        )
    #---

    def Validate(
        self, outP: Optional[Union[str, Path]]=None
        ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """Validate widget content.

            Parameter
            ---------
            outP : Path or None
                If outP is None then default to directly check the widget 
                content
        """
        #region ---------------------------------------------------> Get value
        if outP is None:
            value = self.GetWindow().GetValue()
        else:
            value = outP
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return dtsCheck.Path2FFOutput(value, self.fof, self.opt, self.ext)
        except Exception as e:
            return (False, ('ExceptionRaised', type(e).__name__, str(e)))
        #endregion -------------------------------------------------> Validate
    #---
    
    def TransferToWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---

    def TransferFromWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---
    #endregion ---------------------------------------------> Override methods
#---


class IsNotEmpty(wx.Validator):
    """Check wx widget has a value diferent than ''	"""
    #region --------------------------------------------------> Instance Setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance Setup

    #region ------------------------------------------------> Override Methods
    def Clone(self) -> wx.Validator:
        """ Overridden method """
        return IsNotEmpty()
    #---

    def Validate(self) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """ Overridden method """
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value
        
        #region ----------------------------------------------------> Validate
        if value != '':
            return (True, None)
        else:
            return (False, ('Empty', str(value), config.mEmpty))
        #endregion -------------------------------------------------> Validate
    #---
    
    def TransferToWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---

    def TransferFromWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---
    #endregion ---------------------------------------------> Override Methods
#---


class NumberList(wx.Validator):
    """Checks window holds a list of numbers or just one. Ranges (5-9) are 
        supported. Number of elements in the final list are checked after ranges
        are expanded.

        Parameters
        ----------
        numType : str
            One of 'int' or 'float'. Default is 'int'
        unique : boolean
            Elements must be unique (True) or not
        sep : str
            List elements are separated by sep. Default ' '
        opt : boolean
            To allow for empty fields
        vMin : float or None
            Elements in the list must be >= vMin
        vMax : float or None
            Elements in the list must be <= vMax
        nMin : int or None
            List must contain at least nMin elements
        nN : int or None
            List must contain exactle nN elements
        nMax : int or None
            List must contain maximun nMax elements
            
        Return by Validate method
        -------------------------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code val are:
                - (NotOptional, None) : Sting is not optional
                - (BadElement, str) : Value not valid
                - (ListLengthE, None) : Only x values are accepted
                - (ListLengthR, None) : Only x to y values are accepted
                - (NotUnique, list) : list is the list of repeated elements
                - (ExceptionRaised, ExceptionName): Check method raised an exception.

        Attributes
        ----------
        numType : str
            One of 'int' or 'float'. Default is 'int'
        unique : boolean
            Elements must be unique (True) or not
        sep : str
            List elements are separated by sep. Default ' '
        opt : boolean
            To allow for empty fields
        vMin : float or None
            Elements in the list must be >= vMin
        vMax : float or None
            Elements in the list must be <= vMax
        nMin : int or None
            List must contain at least nMin elements
        nN : int or None
            List must contain exactle nN elements
        nMax : int or None
            List must contain maximun nMax elements

        Raises
        ------
        InputError:
            - When numType is not in config.oNumType.keys()
    """
    #region --------------------------------------------------> Instance Setup
    def __init__(
        self, numType: Literal['int', 'float']='int', unique: bool=True, 
        sep: str=',', opt: bool=False, vMin: Optional[float]=None, 
        vMax: Optional[float]=None, nMin: Optional[int]=None, 
        nN: Optional[int]=None, nMax: Optional[int]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.numType = numType
        self.unique  = unique
        self.sep     = sep
        self.opt     = opt
        self.vMin    = vMin
        self.vMax    = vMax
        self.nMin    = nMin
        self.nN      = nN
        self.nMax    = nMax
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance Setup

    #region ------------------------------------------------> Override Methods
    def Clone(self) -> wx.Validator:
        """ Overridden method """
        return NumberList(
            numType = self.numType,
            unique  = self.unique,
            sep     = self.sep,
            opt     = self.opt,
            vMin    = self.vMin,
            vMax    = self.vMax,
            nMin    = self.nMin,
            nN      = self.nN,
            nMax    = self.nMax,
        )
    #---

    def Validate(
        self, vMin: Optional[float]=None, vMax: Optional[float]=None, 
        nMin: Optional[int]=None, nN: Optional[int]=None, 
        nMax: Optional[int]=None,
        ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """ Validate widget value.  Parameters allow to give these values just
            before validation.
            
            Parameters
            ----------
            vMin : float or None
                Elements in the list must be >= vMin
            vMax : float or None
                Elements in the list must be <= vMax
            nMin : int or None
                List must contain at least nMin elements
            nN : int or None
                List must contain exactle nN elements
            nMax : int or None
                List must contain maximun nMax elements
        """
        #region ---------------------------------------------------> Variables
        tvMin = vMin if vMin is not None else self.vMin
        tvMax = vMax if vMax is not None else self.vMax
        tnMin = nMin if nMin is not None else self.nMin
        tnN   = nN if nN is not None else self.nN
        tnMax = nMax if nMax is not None else self.nMax
        #------------------------------> 
        value    = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Variables
        
        #region ----------------------------------------------------> Validate
        try:
            return dtsCheck.NumberList(
                value,
                numType = self.numType,
                unique  = self.unique,
                sep     = self.sep,
                opt     = self.opt,
                vMin    = tvMin,
                vMax    = tvMax,
                nMin    = tnMin,
                nN      = tnN,
                nMax    = tnMax,
            )
        except Exception as e:
            return (False, ('ExceptionRaised', type(e).__name__, str(e)))
        #endregion -------------------------------------------------> Validate
    #---

    def TransferToWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---

    def TransferFromWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---
    #endregion ---------------------------------------------> Override Methods
#---


class Comparison(wx.Validator):
    """Check windows hold a value like 'operand value', e.g. '< 10.4'.

        Parameters
        ----------
        tStr: str
            String to check
        numType : One of int or float
            Number type in tStr.
        opt : bool
            Input is optional (True) or not (False). Default is False.
        vMin : float or None
            Minimum acceptable value in tStr
        vMax : float or None
            Maximum acceptable value in tStr
        op : list
            List of acceptable operand in front of value for tStr.

        Attributes
        ----------
        tStr: str
            String to check
        numType : One of int or float
            Number type in tStr.
        opt : bool
            Input is optional (True) or not (False). Default is False.
        vMin : float or None
            Minimum acceptable value in tStr
        vMax : float or None
            Maximum acceptable value in tStr
        op : list
            List of acceptable operand in front of value for tStr.

        Return by Validate method
        -------------------------
        tuple
            (True, None)
            (False, (code, val, msg))
            code val are:
                - (NotOptional, None) : tStr cannot be an empty string.
                - (BadElement, tStr) : Not a valid string
                - (FalseOperand, operand) : Operand is not in the list of valid operand.

        Raises
        ------
        InputError:
            - When numType is not in dtsConfig.oNumType.keys()
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, numType: Literal['int', 'float']='int', opt: bool=False, 
        vMin: Optional[float]=None, vMax: Optional[float]=None, 
        op: list[str]=['<', '>', '<=', '>='],
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.numType = numType
        self.opt     = opt
        self.vMin    = vMin
        self.vMax    = vMax
        self.op      = op
        
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self):
        """Overridden method"""
        return Comparison(
            numType = self.numType,
            opt     = self.opt,
            vMin    = self.vMin,
            vMax    = self.vMax,
            op      = self.op,
        )
    #---

    def Validate(self):
        """Overridden method"""
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return dtsCheck.Comparison(
                value,
                numType = self.numType,
                opt     = self.opt,
                vMin    = self.vMin,
                vMax    = self.vMax,
                op      = self.op
            )
        except Exception as e:
            return (False, ('ExceptionRaised', type(e).__name__, str(e)))
        #endregion -------------------------------------------------> Validate

        return (True, None)
    #---
    
    def TransferToWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---

    def TransferFromWindow(self):
        """To use it with wx.Dialog"""
        return True
    #---
    #endregion ---------------------------------------------> Override methods
#---
#endregion --------------------------------------------------------> Validator

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
from typing import Optional, Literal

import wx

from config.config import config as mConfig
from core import check as cCheck
#endregion ----------------------------------------------------------> Imports


LIT_FoF     = Literal['file', 'folder']
LIT_NumType = Literal['int', 'float']


#region -----------------------------------------------------------> Validator
class InputFF(wx.Validator):
    """Check widget holds the path to an input file/folder.

        Parameters
        ----------
        fof: str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'.
        opt: Boolean
            Value is optional. Default is False.

        Return by Validate method
        -------------------------
        tuple
            - (True, None)
            - (False, (code, path, msg))
                code is:
                - NotPath,         Input is not valid path
                - NotFile,         Input is not valid file
                - NotDir,          Input is not valid folder
                - NoRead,          Input cannot be read
                - ExceptionRaised, Check method raised an exception.

        Attributes
        ----------
        rFof: str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'folder'.
        rOpt: Boolean
            Value is optional. Default is False.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, fof:LIT_FoF='file', opt:bool=False) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFof:LIT_FoF = fof
        self.rOpt = opt
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self) -> wx.Validator:
        """Overridden method"""
        return InputFF(fof=self.rFof, opt=self.rOpt)
    #---

    def Validate(self) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """Overridden method"""
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return cCheck.Path2FFInput(value, self.rFof, self.rOpt)
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
    """Validates a widget holding the path to an output file/folder.

        Parameters
        ----------
        fof: str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'.
        opt: Boolean
            Value is optional. Default is True.

        Returns by Validate method
        --------------------------
        tuple
            - (True, None)
            - (False, (code, path, msg))
                code is:
                - NotPath,         Input is not a valid path.
                - NoWrite,         It is not possible to write.
                - ExceptionRaised, Check method raised an exception.

        Attributes
        ----------
        rFof: str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'.
        rOpt: Boolean
            Value is optional. Default is True.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, fof:LIT_FoF='file', opt:bool=False) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFof:LIT_FoF = fof
        self.rOpt = opt
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self) -> wx.Validator:
        """Overridden method"""
        return OutputFF(fof=self.rFof, opt=self.rOpt)
    #---

    def Validate(self) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """Validate widget content.

            Returns
            -------
            tuple[bool, Optional[tuple[str, Optional[str], str]]]
        """
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return cCheck.Path2FFOutput(value, self.rFof, self.rOpt)
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
    """Check wx widget has a value different than ''.

        Returns by Validate method
        --------------------------
        tuple
            - (True, None)
            - (False, (code, path, msg))
                code is:
                - Empty, Field is empty.
    """
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
        return (False, ('Empty', str(value), mConfig.core.mEmpty))
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
        numType: str
            One of 'int' or 'float'. Default is 'int'.
        unique: boolean
            Elements must be unique (True) or not.
        sep: str
            List elements are separated by sep. Default ' '.
        opt: boolean
            To allow for empty fields.
        vMin: float or None
            Elements in the list must be >= vMin.
        vMax: float or None
            Elements in the list must be <= vMax.
        nMin: int or None
            List must contain at least nMin elements.
        nN: int or None
            List must contain exactly nN elements.
        nMax: int or None
            List must contain maximum nMax elements.

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
                - (ExceptionRaised, Name): Check method raised an exception.

        Attributes
        ----------
        rNumType: str
            One of 'int' or 'float'. Default is 'int'.
        rUnique: boolean
            Elements must be unique (True) or not.
        rSep: str
            List elements are separated by sep. Default ' '.
        rOpt: boolean
            To allow for empty fields.
        rVMin: float or None
            Elements in the list must be >= vMin.
        rVMax: float or None
            Elements in the list must be <= vMax.
        rNMin: int or None
            List must contain at least nMin elements.
        rNN: int or None
            List must contain exactly nN elements.
        rNMax: int or None
            List must contain maximum nMax elements.
    """
    #region --------------------------------------------------> Instance Setup
    def __init__(
        self,
        numType:LIT_NumType  = 'int',
        unique:bool          = True,
        sep:str              = ',',
        opt:bool             = False,
        vMin:Optional[float] = None,
        vMax:Optional[float] = None,
        nMin:Optional[int]   = None,
        nN:Optional[int]     = None,
        nMax:Optional[int]   = None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rNumType:LIT_NumType = numType
        self.rUnique = unique
        self.rSep    = sep
        self.rOpt    = opt
        self.rVMin   = vMin
        self.rVMax   = vMax
        self.rNMin   = nMin
        self.rNN     = nN
        self.rNMax   = nMax
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance Setup

    #region ------------------------------------------------> Override Methods
    def Clone(self) -> wx.Validator:
        """ Overridden method """
        return NumberList(
            numType = self.rNumType,
            unique  = self.rUnique,
            sep     = self.rSep,
            opt     = self.rOpt,
            vMin    = self.rVMin,
            vMax    = self.rVMax,
            nMin    = self.rNMin,
            nN      = self.rNN,
            nMax    = self.rNMax,
        )
    #---

    def Validate(
        self,
        vMin:Optional[float] = None,
        vMax:Optional[float] = None,
        nMin:Optional[int]   = None,
        nN:Optional[int]     = None,
        nMax:Optional[int]   = None,
        ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
        """Validate widget value. Parameters allow to give these values just
            before validation.

            Parameters
            ----------
            vMin: float or None
                Elements in the list must be >= vMin.
            vMax: float or None
                Elements in the list must be <= vMax.
            nMin: int or None
                List must contain at least nMin elements.
            nN: int or None
                List must contain exactly nN elements.
            nMax: int or None
                List must contain maximum nMax elements.
        """
        #region ---------------------------------------------------> Variables
        tvMin = vMin if vMin is not None else self.rVMin
        tvMax = vMax if vMax is not None else self.rVMax
        tnMin = nMin if nMin is not None else self.rNMin
        tnN   = nN if nN is not None else self.rNN
        tnMax = nMax if nMax is not None else self.rNMax
        #------------------------------>
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Variables

        #region ----------------------------------------------------> Validate
        try:
            return cCheck.NumberList(
                value,
                numType = self.rNumType,
                unique  = self.rUnique,
                sep     = self.rSep,
                opt     = self.rOpt,
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
        numType: One of int or float
            Number type in tStr.
        opt: bool
            Input is optional (True) or not (False). Default is False.
        vMin: float or None
            Minimum acceptable value in tStr.
        vMax: float or None
            Maximum acceptable value in tStr.
        op: list
            List of acceptable operand in front of value for tStr.

        Attributes
        ----------
        rNumType: One of int or float
            Number type in tStr.
        rOpt: bool
            Input is optional (True) or not (False). Default is False.
        rVMin: float or None
            Minimum acceptable value in tStr.
        rVMax: float or None
            Maximum acceptable value in tStr.
        rOp: list
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
    """
    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        numType:LIT_NumType  = 'int',
        opt:bool             = False,
        vMin:Optional[float] = None,
        vMax:Optional[float] = None,
        op:list[str]         = ['<', '>', '<=', '>='],
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rNumType:LIT_NumType = numType
        self.rOpt  = opt
        self.rVMin = vMin
        self.rVMax = vMax
        self.rOp   = op
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ------------------------------------------------> Override methods
    def Clone(self):
        """Overridden method"""
        return Comparison(
            numType = self.rNumType,
            opt     = self.rOpt,
            vMin    = self.rVMin,
            vMax    = self.rVMax,
            op      = self.rOp,
        )
    #---

    def Validate(self):
        """Overridden method"""
        #region ---------------------------------------------------> Get value
        value = self.GetWindow().GetValue()
        #endregion ------------------------------------------------> Get value

        #region ----------------------------------------------------> Validate
        try:
            return cCheck.Comparison(
                value,
                numType = self.rNumType,
                opt     = self.rOpt,
                vMin    = self.rVMin,
                vMax    = self.rVMax,
                op      = self.rOp
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
    #endregion ---------------------------------------------> Override methods
#---
#endregion --------------------------------------------------------> Validator

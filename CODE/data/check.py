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


"""Classes and methods to check data"""


#region -------------------------------------------------------------> Imports
import os
from pathlib import Path
from typing import Optional, Union

import wx

import config.config as mConfig
import data.exception as mException
import data.method as mMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def VersionCompare(
    strA: str, strB: str,
    )-> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Basic version comparison.

        Parameters
        ----------
        strA : str
            Expected format is '2.3.4' or '2.3.4 (beta)'.
        strB : str
            Same format as strA is expected.

        Returns
        -------
        tuple
            (True, None)
            (False, ('', '', ''))

        Raise
        -----
        InputError
            When strA or strB cannot be converted to x,y,z integers

        Examples
        --------
        >>> VersionCompare('2.4.7 beta', '2.4.7')
        >>> False
        >>> VersionCompare('2.4.7', '2.4.1')
        >>> True
        >>> VersionCompare('3.4.7 beta', '5.4.1')
        >>> False
    """
    #region -------------------------------------------------> Get number list
    xA, yA, zA = map(int, strA.strip().split(" ")[0].split("."))
    xB, yB, zB = map(int, strB.strip().split(" ")[0].split("."))
    #endregion ----------------------------------------------> Get number list

    #region ---------------------------------------------------------> Compare
    if xA > xB:
        return (True, None)
    elif xA < xB:
        return (False, ('', '', ''))
    else:
        if yA > yB:
            return (True, None)
        elif yA < yB:
            return (False, ('', '', ''))
        else:
            if zA > zB:
                return (True, None)
            else:
                return (False, ('', '', ''))
    #endregion ------------------------------------------------------> Compare
#---


def Path2FFOutput(
    value: Union[str, Path],
    fof: mConfig.litFoF='file',
    opt: bool=False,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check if value holds a valid path that can be used for output data.

        Parameters
        ----------
        value: str or Path
            Path to the file or folder
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'file'.
        opt : Boolean
            Value is optional. Default is False.

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, value, msg))
                code is:
                - NotPath, Input is not a valid path.
                - NoWrite, It is not possible to write.

        Examples
        --------
        >>> Path2FFOutput('', 'file', opt=False)
        >>> (False, (NoPath, '', The path '' is not valid.))
    """
    #region --------------------------------------------------------> Optional
    if value == '':
        if opt:
            return (True, None)
        else:
            msg = f"The selected path is not valid.\nSelected path: '{value}'"
            return (False, ('NotPath', str(value), msg))
    else:
        pass
    #endregion -----------------------------------------------------> Optional
    
    #region ---------------------------------------------------> Is valid Path
    try:
        tPath = Path(value)
    except Exception:
        msg = f"The selected path is not valid.\nSelected path: '{value}'"
        return (False, ('NotPath', str(value), msg))
    #endregion ------------------------------------------------> Is valid Path

    #region -------------------------------------------------------> Can write
    tempFileName = 'kbr-'+mMethod.StrNow()+'.kbr'
    if fof == 'file':
        f = tPath.parent / tempFileName 
    else:
        f = tPath / tempFileName
    try:
        f.touch()
        f.unlink()
    except Exception:
        msg = f"{f} cannot be used for writing."
        return (False, ('NoWrite', str(value), msg))
    #endregion ----------------------------------------------------> Can write

    return (True, None)
#---


def Path2FFInput(
    value: Union[str, Path],
    fof: mConfig.litFoF='folder',
    opt: bool=False,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check that value is a valid path to a file or folder. 

        Parameters
        ----------
        value: str or Path
            Path to the file or folder
        fof : str
            One of 'file', 'folder'. Check widgets hold path to file or folder.
            Default is 'folder'
        opt : Boolean
            Value is optional. Default is False.

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, value, msg))
            code is:
                - NotPath,   Input is not valid path
                - NotFile,   Input is not valid file
                - NotDir,    Input is not valid folder
                - NoRead,    Input cannot be read

        Examples
        --------
        >>> Path2FFInput('', 'file', opt=True, ext=None)
        >>> (False, ('NotPath', '', 'The path "" is not valid.'))
        >>> Path2FFInput('/Users/DAT4S/test.py', 'file')
        >>> (True, None)
    """
    #region --------------------------------------------------------> Optional
    if value == '':
        if opt:
            return (True, None)
        else:
            msg = f"The selected path is not valid.\nSelected path: '{value}'"
            return (False, ('NotPath', str(value), msg))
    else:
        pass
    #endregion -----------------------------------------------------> Optional

    #region ---------------------------------------------------> Is valid Path
    try:
        tPath = Path(value)
    except Exception:
        msg = f"The selected path is not valid.\nSelected path: '{value}'"
        return (False, ('NotPath', str(value), msg))
    #endregion ------------------------------------------------> Is valid Path
    
    #region -------------------------------------------------------------> Fof
    if fof == 'file':
        if tPath.is_file():
            pass
        else:
            msg = (
                f"The selected path does not point to a file."
                f"\nSelected path:'{tPath}'")
            return (False, ('NotFile', str(value), msg))
    elif fof == 'folder':
        if tPath.is_dir():
            pass
        else:
            msg = (
                f"The selected path does not point to a folder.\n"
                f"Selected path: '{tPath}'")
            return (False, ('NotDir', str(value), msg))
    else:
        msg = mConfig.mNotSupported.format('fof', fof)
        raise mException.InputError(msg)
    #endregion ----------------------------------------------------------> Fof
    
    #region --------------------------------------------------------> Can read
    if os.access(tPath, os.R_OK):
        pass
    else:
        msg = f"The selected path cannot be read.\nSelected path: '{tPath}'"
        return (False, ('NoRead', str(value), msg))
    #endregion -----------------------------------------------------> Can read

    return (True, None)
#---


def NumberList(
    tStr: str,
    numType: mConfig.litNumType='int',
    unique: bool=True,
    sep: str=' ',
    opt: bool=False,
    vMin: Optional[float]=None,
    vMax: Optional[float]=None,
    nMin: Optional[int]=None,
    nN: Optional[int]=None,
    nMax: Optional[int]=None,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check tStr contains a list of numbers.

        Parameters
        ----------
        tStr: str
            String to check
        numType: str
            One of 'int' or 'float'. Default is 'int'
        unique: boolean
            Elements must be unique (True) or not (False)
        sep: str
            List elements are separated by sep. Default ' '
        opt: boolean
            To allow for empty fields
        vMin: float or None
            Elements in the list must be >= vMin
        vMax: float or None
            Elements in the list must be <= vMax
        nMin: int or None
            List must contain at least nMin elements
        nN: int or None
            List must contain exactly nN elements
        nMax: int or None
            List must contain maximum nMax elements

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code val are:
                - (NotOptional, None) : String is not optional
                - (BadElement, str) : Value not valid
                - (ListLength, length) : The length of the list is not equal to 
                    nN and it is not withing the range nMin - nMax
                - (NotUnique, list) : list is the list of repeated elements

        Notes
        -----
        Range in the tStr (4-8) are expanded before checking.

        Examples
        --------
        >>> NumberList('1,2,3, 4-10', numType='int', sep=',')
        >>> (True, None)
        >>> NumberList('1,2,3, 2-10', numType='int', sep=',', unique=True)
        >>> (False, (NotUnique, val, msg))
    """
    #region -------------------------------------------------------> Variables
    value    = ' '.join(tStr.split())
    elements = value.split(sep)
    numbers  = []
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------------> Optional
    if value == '':
        if opt:
            return (True, None)
        else:
            msg = "An empty string is not a valid input."
            return (False, ('NotOptional', str(value), msg))
    else:
        pass
    #endregion -----------------------------------------------------> Optional

    #region ----------------------------------------> numType, refMin & refMax
    for n in elements:
        #------------------------------> Expand range
        try:
            rN = mMethod.ExpandRange(n, numType)
        except Exception:
            msg = mConfig.mInvalidValue.format(n)
            return (False, ('BadElement', n, msg))
        #------------------------------> Compare
        if vMin is None and vMax is None:
            numbers = numbers + rN
        else:
            for tN in rN:
                #------------------------------> 
                if AInRange(tN, refMin=vMin, refMax=vMax)[0]:
                    pass
                else:
                    msg = mConfig.mInvalidValue.format(n)
                    return (False, ('BadElement', n, msg))
                #------------------------------> 
                numbers.append(tN)
    #endregion -------------------------------------> numType, refMin & refMax

    #region -----------------------------------------------------> List Length
    #------------------------------> Number of Elements
    lN = len(numbers)
    #------------------------------>
    if nN is not None:
        #------------------------------> Exact Number of Elements
        if lN == nN:
            pass
        else:
            msg = (f'The number of elements in tStr ({lN}), after expanding '
                f'ranges, is not equal to nN ({nN}).')
            return (False, ('ListLength', tStr, msg))
    elif nMin is not None or nMax is not None:
        #------------------------------> Number of Elements in range
        if AInRange(lN, refMin=nMin, refMax=nMax)[0]:
            pass
        else:
            msg = (f'The number of elements in tStr ({lN}), after expanding '
                f'ranges, is not in the [{nMin}, {nMax}] range.')
            return (False, ('ListLength', tStr, msg))
    else:
        pass
    #endregion --------------------------------------------------> List Length

    #region ----------------------------------------------------------> Unique
    if unique:
        return ListUnique(numbers)
    else:
        pass
    #endregion -------------------------------------------------------> Unique
    
    return (True, None)
#---


def AInRange(
    a: Union[str, int, float],
    refMin: Union[str, int, float, None]=None,
    refMax: Union[str, int, float, None]=None,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check if refMin <= a <= refMax.

        Parameters
        ----------
        a: str, int or float
            Number to check if it is within the given range
        refMin: str, int, float or None
            Lower end of range
        refMax: str, int, float or None
            Upper end of range

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code, val are:
                    - ('AInRange', a) : a is the given value to check
                
        Notes
        -----
        Leaving one range limit as None allows to check for open intervals.
        If both refMin and refMax are None it returns True.

        Examples
        --------
        >>> AInRange(6, refMin=None, refMax=None)
        >>> (True, None)
        >>> AInRange(6, refMin='3', refMax=10)
        >>> (True, None)
        >>> AInRange('0', refMin='3', refMax=10)
        >>> (False, ('AInRange), '0', '0 is not in the range: [3, 10].')
        >>> AInRange(6, refMin='3')
        >>> (True, None)
        >>> AInRange(-1, refMax='-3.9')
        >>> (False, ('AInRange', '-1', '-1 is not in the range: [None, -3.9].'))
        >>> AInRange('3', refMin=-10, refN=3, refMax=0)
        >>> (True, None)
    """
    #region -------------------------------------------------------> Variables
    a = float(a)
    b = float(refMin) if refMin is not None else float('-inf')
    c = float(refMax) if refMax is not None else float('inf')
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------------------------------> Compare
    if b <= a <= c:
        return (True, None)
    else:
        msg = (f'{a} is not in the range: [{refMin}, {refMax}].')
        return (False, ('AInRange', str(a), msg))
    #endregion ------------------------------------------------------> Compare
#---


def ListUnique(
    tList: Union[list, tuple],
    opt:bool=False,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check if tList contains unique elements or not.

        Parameters
        ----------
        tList: list or tuple
            The list or tuple to check for unique elements.
        opt: bool
            List can be empty (True) or not (False). Default is False.

        Return
        ------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code val are:
                    - (NotOptional, '')
                    - (NotUnique, list) : repeated elements

        Examples
        --------
        >>> ListUnique([1,2,3,4])
        >>> (True, None)
        >>> ListUnique([9,'A',1,2,6,'1','2','3',2,6,8,9])
        >>> (False, ('NotUnique', '9, 2, 6', 'Duplicated elements: 9, 2, 6'))
    """
    #region -------------------------------------------------------> Variables
    seen = set()
    dup  = []
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------------> Optional
    if not tList:
        if opt:
            return (True, None)
        else:
            return (False, ('NotOptional', '', f"tList cannot be empty."))
    else:
        pass
    #endregion -----------------------------------------------------> Optional

    #region ----------------------------------------------------------> Search
    #------------------------------>
    for x in tList:
        if x not in seen:
            seen.add(x)
        else:
            dup.append(x)
    #------------------------------>
    dup = list(set(dup))
    #endregion -------------------------------------------------------> Search

    #region ----------------------------------------------------------> Return
    if dup:
        #------------------------------> 
        dupE = ', '.join(map(str, dup))
        msg = f"List contains duplicated elements ({dupE})."
        #------------------------------> 
        return (False, ('NotUnique', dupE, msg))
    else:
        return (True, None)
    #endregion -------------------------------------------------------> Return
#---


def UniqueColNumbers(
    value: list[str],
    sepList: list[str]=[' ', ',', ';'],
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check value contains unique integers.

        Parameters
        ----------
        value : list[str]
            List of string with the values to check. The expected values are:
            ['1 3 4 5-10', '11-13, 14 15; ...', ...]. Only integers are allowed.
        sepList: list of str
            Separator used in values.
            sepList[0] : internal element separator
            sepList[1] : intra row separator
            sepList[2] : inter row separator

        Returns
        -------
        tuple:
            (True, None)
            (False, (NotUnique, repeated elements, msg))

        Notes
        -----
        - Both value and sepList will be map to str
        - Only integers and ranges (4-10) are expected in value.

        Examples
        --------
        >>> UniqueColNumbers(['1 2 3', '3-5'], sepList=[' ', ',', ';'])
        >>> (False, ('NotUnique', '3', 'Duplicated element: 3'))
    """
    # Test in test.unit.test_check.Test_UniqueColNumbers
    def _strip_split(tEle: Union[str, list[str]], sep: str) -> list[str]:
        """ """
        #------------------------------> 
        if isinstance(tEle, str):
            k = [tEle.strip()]
        else:
            k = tEle
        #------------------------------>
        out = []
        for v in k:
            for j in v.split(sep):
                out.append(j)
        #------------------------------> 
        return [x.strip() for x in out]
    #---
    #region -----------------------------------------------------> Check input
    #------------------------------> 
    try:
        value = list(map(str, value))
    except Exception as e:
        msg = ('value must be a list of strings.')
        raise mException.InputError(msg)
    #------------------------------> 
    try:
        sepList = list(map(str, sepList))
        if len(sepList) != 3:
            msg = (
            f'sepList "({sepList}" must be a list of three strings. '
            f'e.g. [" ", ",", ";"].')
            raise mException.InputError(msg)
        else:
            pass
    except Exception as e:
        msg = (
            f'sepList "({sepList}" must be a list of three strings. '
            f'e.g. [" ", ",", ";"].')
        raise mException.InputError(msg)
    #endregion --------------------------------------------------> Check input

    #region ----------------------------------------------------> Get Elements
    #------------------------------>
    values = []
    #------------------------------>
    for k in value:
        #------------------------------>
        for sep in reversed(sepList):
            k = _strip_split(k, sep)
        #------------------------------>
        values = values + k # type: ignore
    #------------------------------>
    values = sepList[0].join(values)
    #endregion -------------------------------------------------> Get Elements

    #region --------------------------------------------------> Check Elements
    #------------------------------>
    try:
        values = mMethod.Str2ListNumber(values, numType='int', sep=sepList[0])
    except Exception as e:
        raise e
    #------------------------------>
    try:
        return ListUnique(values)
    except Exception as e:
        raise e
    #endregion -----------------------------------------------> Check Elements
#---


def TcUniqueColNumbers(
    tcList: list[wx.TextCtrl],
    sepList: list[str]=[' ', ',', ';'],
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Checks that all elements in the wx.TextCtrl(s) are unique.

        Parameters
        ----------
        tcList : list of wx.TextCtrl
            List of wx.TextCtrl. Individual elements in each wx.TextCtrl value 
            are separated by sepList[0]. e.g. '1 2 3' if sepList[0] is ' '.
        sepList: list of str
            Separator used in tcList and resCtrl. Individual elements in tcList
            are separated by sepList[0] while elements in resCtrl are separated 
            by:
            sepList[0] : internal element separator
            sepList[1] : intra row separator
            sepList[2] : inter row separator

        Returns
        -------
        tuple:
            (True, None)
            (False, (NotUnique, repeated elements, msg))

        Notes
        -----
        Individual elements in tcList and resCtrl are expected to be integers.
    """
    #region -------------------------------------------------------> Variables
    values = []
    #endregion ----------------------------------------------------> Variables

    #region -------------------------------------------------------> Form list
    #------------------------------> tcList
    try:
        for tc in tcList:
            try:
                values.append(tc.GetValue())
            except Exception:
                msg = 'tcList must contain a list of wx.TextCtrl.'
                raise mException.InputError(msg)
    except TypeError:
        msg = f'tcList must be a list of wx.TextCtrl.'
        raise mException.InputError(msg)
    #endregion ----------------------------------------------------> Form list
    
    #region ----------------------------------------------------------> Return
    try:
        return UniqueColNumbers(values, sepList=sepList)
    except Exception as e:
        raise e
    #endregion -------------------------------------------------------> Return
#---


def AllTcEmpty(
    tcList: list[wx.TextCtrl],
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check that all values in tcList are empty.

        Parameters
        ----------
        tcList: list of wx.TextCtrl
            Widgets holding the values to check

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code, val are:
                    - ('NotEmpty', '')

        Notes
        -----
        If tcList is empty returns True.

        Examples
        --------
        >>> AllTcEmpty([])
        >>> (True, None)
    """
    # No Test
    #region -------------------------------------------------------> Variables
    values = []
    #endregion ----------------------------------------------------> Variables

    #region ------------------------------------------------------> Get values
    for k in tcList:
        values.append(k.GetValue())
    #endregion ---------------------------------------------------> Get values

    #region -----------------------------------------------------> Check empty
    if any(values):
        return (False, ('NotEmpty', '', 'Some wx.TextCtrl are not empty.'))
    else:
        return (True, None)
    #endregion --------------------------------------------------> Check empty
#---

def Comparison(
    tStr: str,
    numType: mConfig.litNumType='int',
    opt: bool=False,
    vMin: Optional[float]=None,
    vMax: Optional[float]=None, 
    op: list[str]=['<', '>', '<=', '>='],
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check tStr is like 'op val', e.g. '< 10.3'.

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

        Returns
        -------
        tuple
            (True, None)
            (False, (code, val, msg))
            code val are:
                - (NotOptional, None) : tStr cannot be an empty string.
                - (BadElement, tStr) : Not a valid string
                - (FalseOperand, operand) : Operand is not in the list of valid operand.

        Examples
        --------
        >>> Comparison('< 1.4', numType='float', opt=False, vMin=0, vMax=100, op=['<', '>', '<=', '>='])
        >>> (True, None)
    """
    #region -------------------------------------------------------> Variables
    value    = " ".join(tStr.split())
    elements = [x.strip() for x in value.split()]
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------------> Optional
    if value == '':
        if opt:
            return (True, None)
        else:
            msg = "An empty string is not a valid input."
            return (False, ('NotOptional', None, msg))
    else:
        pass
    #endregion -----------------------------------------------------> Optional

    #region ----------------------------------------------------------> Length
    if len(elements) != 2:
        msg = mConfig.mInvalidValue.format(tStr)
        return (False, ('BadElement', tStr, msg))
    else:
        pass
    #endregion -------------------------------------------------------> Length

    #region ---------------------------------------------------------> Operand
    if elements[0] in op:
        pass
    else:
        msg = (
            f'The given operand ({elements[0]}) is not valid '
            f'({str(op)[1:-1]}).')
        return (False, ('FalseOperand', str(elements[0]), msg))
    #endregion ------------------------------------------------------> Operand

    #region ---------------------------------------------------------> NumType
    try:
        mConfig.oNumType[numType](elements[1])
    except Exception:
        msg = mConfig.mInvalidValue.format(tStr)
        return (False, ('BadElement', tStr, msg))
    #endregion ------------------------------------------------------> NumType

    #region -----------------------------------------------------------> Range
    if vMin is None and vMax is None:
        pass
    else:
        try:
            if AInRange(elements[1], refMin=vMin, refMax=vMax)[0]:
                pass
            else:
                msg = mConfig.mInvalidValue.format(tStr)
                return (False, ('BadElement', tStr, msg))
        except Exception:
            msg = mConfig.mInvalidValue.format(tStr)
            return (False, ('BadElement', tStr, msg))
    #endregion --------------------------------------------------------> Range

    return (True, None)
#---
#endregion ----------------------------------------------------------> Methods

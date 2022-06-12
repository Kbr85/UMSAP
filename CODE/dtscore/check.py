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
import os
from pathlib import Path
from typing import Union, Optional, Callable, Literal

import wx

import config.config as config
import dtscore.data_method as dtsMethod
import dtscore.exception as dtsException
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def AInRange(
    a: Union[str, int, float], refMin: Union[str, int, float, None]=None,
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
        If both refMin and refMax are None it returns True
            
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

def UniqueNumbers(
    tcList: list['wx.TextCtrl'], numType: Literal['int', 'float']='int', 
    sep: str=',', opt:bool=False,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check if all values in tcList hold unique numbers after expanding ranges

        Parameters
        ----------
        tcList : list of wx.TextCtrl
            Widgets holding the values to check
        numType : str
            One of int, float. Default is int
        sep : str
            Character separating the values withing a wx.TextCtrl
        opt : bool
            Allow empty tcList (True) or not (False). Default is False.
            
        Raises
        ------
        InputError:
            - When tcList is not a list.
            - When failed to get the values of the elements in tcList.
        See also dtsMethod.Str2ListNumber and dtsCheck.ListUnique

        Returns
        -------
        tupple:
            (True, None)
            (False, (NotUnique, repeated elements, msg))
    """
    # Partial test in tests.unit.data.test_check.Test_UniqueNumbers 
    #region ------------------------------------------------------> Empty list
    if len(tcList) == 0:
        if opt:
            return (True, None)
        else:
            return (False, ('NotOptional', '', 'tcList cannot be empty.'))
    else:
        pass
    #endregion ---------------------------------------------------> Empty list
    
    #region -------------------------------------------------------> Form list
    #------------------------------>
    try:
        #------------------------------> 
        values = tcList[0].GetValue()
        #------------------------------> 
        for tc in tcList[1:]:
            values = f"{values}{sep} {tc.GetValue()}"
    except Exception as e:
        raise dtsException.InputError('tcList must be a list of wx.TextCtrl')
    #------------------------------> 
    try:
        values = dtsMethod.Str2ListNumber(values, numType=numType, sep=sep)
    except Exception as e:
        raise e
    #endregion ----------------------------------------------------> Form list

    #region ----------------------------------------------------> Check unique
    try:
        return ListUnique(values)
    except Exception as e:
        raise e
    #endregion -------------------------------------------------> Check unique
#---

def NumberList(
    tStr: str, numType: Literal['int', 'float']='int', unique: bool=True, 
    sep: str=',', opt: bool=False, vMin: Optional[float]=None, 
    vMax: Optional[float]=None, nMin: Optional[int]=None, 
    nN: Optional[int]=None, nMax: Optional[int]=None,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check tStr contains a list of numbers
    
        See Notes for more details

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
            List must contain exactle nN elements
        nMax: int or None
            List must contain maximun nMax elements

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
            rN = dtsMethod.ExpandRange(n, numType)
        except Exception:
            msg = config.mInvalidValue.format(n)
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
                    msg = config.mInvalidValue.format(n)
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

def ListUnique(
    tList: Union[list, tuple], opt:bool=False,
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

def ListContent(
    tList: list, nMin: Optional[int]=None, nN: Optional[int]=None, 
    nMax: Optional[int]=None, mapType: Optional[Callable]=None, 
    tType: Optional[Callable]=None, unique: bool=False, opt: bool=False,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check the content of a list.

        Parameters
        ----------
        tList: list or tuple
            The list or tuple to check for its content.
        nMin: int or None
            List must contain at least nMin elements. Default is None.
        nN: int or None
            List must contain exactly nN elements. Default is None.
        nMax: int or None
            List must contain maximun nMax elements. Default is None.
        mapType: callable or None
            Elements in tList can be mapped to mapType. 
            Default is None.
        tType: callable or None
            Elements in tList must be of type tType. It takes precedence over
            mapType. Default is None
        unique: bool
            Check elements are unique (True) or not (False). Default is False.
        opt: bool
            Allow (True) empty list or not (False). Default is False.

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code val are:
                - (NotOptional, '') : String is not optional
                - (BadElement, list) : list of elements that are not of tType or
                    cannot be mapped to mapType.
                - (ListLength, length) : The length of the list is not equal to 
                    nN and it is not withing the range nMin - nMax
                - (NotUnique, list) : list of repeated elements

        Examples
        --------
        >>> ListContent([1,2,3], nN=3, tType=int)
        >>> (True, None)
        >>> ListContent(['1','2','3'], nN=3, tType=int)
        >>> (False, ('BadElement', '[1, 2, 3]', ErrorMsg))
        >>> ListContent(['1','2','3'], nN=3, mapType=int)
        >>> (True, None)
    """
    #region --------------------------------------------------------> Optional
    if (nList := len(tList)) == 0:
        if opt:
            return (True, None)
        else:
            msg = 'An empty list cannot be accepted here.'
            return (False, ('NotOptional', '', msg))
    else:
        pass
    #endregion -----------------------------------------------------> Optional
    
    #region ----------------------------------------------------------> Length
    if nN is not None:
        #------------------------------> Exact number of elements
        if int(nN) == nList:
            pass
        else:
            msg = (f'The number of elements in tList ({nList}) is different '
                'to {nN}.')
            return (False, ('ListLength', str(nList), msg))
    elif nMin is not None or nMax is not None:
        #------------------------------> Number of elements in range
        if AInRange(nList, refMin=nMin, refMax=nMax)[0]:
            pass
        else:
            msg = (
                f'The number of elements in tList is not within the range: '
                f'[{nMin}, {nMax}].')
            return (False, ('ListLength', str(nList), msg))
    else:
        pass
    #endregion -------------------------------------------------------> Length
    
    #region ----------------------------------------------------------> Unique
    if unique:
        #------------------------------> 
        a, b = ListUnique(tList)
        #------------------------------> 
        if a:
            pass
        else:
            return (a, b)
    else:
        pass
    #endregion -------------------------------------------------------> Unique
    
    #region ------------------------------------------------------------> Type
    if tType is not None:
        #------------------------------> 
        noT = []
        #------------------------------> 
        for k in tList:
            if type(k) == tType:
                pass
            else:
                noT.append(k)
        #------------------------------> 
        if noT:
            #------> 
            noT = list(set(noT))
            noT = ", ".join(map(str, noT))
            #------> 
            msg = (f'tList contains elements ({noT}) that are not of type '
                   f'{tType}.')
            return (False, ('BadElement', str(noT), msg))
        else:
            pass
    elif mapType is not None:
        #------------------------------> 
        noT = []
        #------------------------------> 
        for k in tList:
            try:
                mapType(k)
            except Exception:
                noT.append(k)
        #------------------------------> 
        if noT:
            #------> 
            noT = list(set(noT))
            noT = ", ".join(map(str, noT))
            #------> 
            msg = (f'tList contains elements ({noT}) that cannot be map to '
                f'tType ({tType}).')
            return (False, ('BadElement', str(noT), msg))
        else:
            pass
    else:
        pass
    #endregion ---------------------------------------------------------> Type
    
    return (True, None)
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
        If tcList is empty returns True
        
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
    tStr: str, numType: Literal['int', 'float']='int', opt: bool=False, 
    vMin: Optional[float]=None, vMax: Optional[float]=None, 
    op: list=['<', '>', '<=', '>='],
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
        msg = config.mInvalidValue.format(tStr)
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
        config.oNumType[numType](elements[1])
    except Exception:
        msg = config.mInvalidValue.format(tStr)
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
                msg = config.mInvalidValue.format(tStr)
                return (False, ('BadElement', tStr, msg))
        except Exception:
            msg = config.mInvalidValue.format(tStr)
            return (False, ('BadElement', tStr, msg))
    #endregion --------------------------------------------------------> Range
    
    return (True, None)
#---
#endregion ----------------------------------------------------------> Methods

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


"""Methods for the app"""


#region -------------------------------------------------------------> Imports
import copy
import itertools
import traceback
from datetime import datetime
from pathlib  import Path
from typing   import TYPE_CHECKING, Literal, Union

import pandas as pd

import wx

from config.config import config as mConfig
from core import file as cFile

if TYPE_CHECKING:
    from core import window as cWindow
#endregion ----------------------------------------------------------> Imports


LIT_NumType = Literal['int', 'float']
LIT_CompEq  = Literal['e', 'ne']
LIT_Comp    = Literal['lt', 'le', 'e', 'ge', 'gt']


#region ------------------------------------------------------> String Methods
def StrNow(dtFormat:str=mConfig.core.dtFormat) -> str:
    """Get a formatted datetime.now() string.

        Parameters
        ----------
        dtFormat: str
            Format specification.

        Returns
        -------
        str:
            The now date time as 20210112-140137.

        Example
        -------
        >>> StrNow()
        >>> '20210112-140137'
    """
    # No test
    return datetime.now().strftime(dtFormat)
#---


def StrException(
    tException: Exception,
    tStr:bool  = True,
    tRepr:bool = True,
    trace:bool = True
    ) -> str:
    """Get a string to print information about tException.

        Parameters
        ----------
        tException: Exception
            Exception to print.
        tStr: boolean
            Include error message as return by str(tException). Default is True.
        tRepr: boolean
            Include error message as return by repr(tException).
            Default is True.
        trace: boolean
            Include the traceback. Default is True.

        Returns
        -------
        str
            Error message
    """
    # No test
    #region -------------------------------------------------------> Variables
    msg = ''
    #endregion ----------------------------------------------------> Variables

    #region ---------------------------------------------------------> Message
    #------------------------------> str(e)
    if tStr:
        msg = f"{msg}{str(tException)}\n\n"
    #------------------------------> repr(e)
    if tRepr:
        msg = f"{msg}{repr(tException)}\n\n"
    #------------------------------> traceback
    if trace:
        tTrace = "".join(
            traceback.format_exception(
                type(tException),
                tException,
                tException.__traceback__,
            )
        )
        msg = f"{msg}{tTrace}"
    #endregion ------------------------------------------------------> Message

    return msg
#---


def Str2ListNumber(
    tStr:str,
    numType:LIT_NumType = 'int',
    sep:str             = ',',
    unique:bool         = False
    ) -> Union[list[int], list[float]]:
    """Turn a string into a list of numbers. Ranges are expanded as integers.

        Parameters
        ----------
        tStr: str
            The string containing the numbers and/or range of numbers (4-8)
        numType: str
            One of int, float
        sep: str
            The character to separate numbers in the string
        unique: boolean
            Return only unique values. Order is kept. Default is False.

        Returns
        -------
        list of numbers.

        Examples
        --------
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',')
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5, 6, 7]
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',', unique=True)
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5]
    """
    # Test in test.unit.test_method.Test_Str2ListNumber
    #region -------------------------------------------------------> Variables
    lN = []
    values = tStr.strip().split(sep)
    #endregion ----------------------------------------------------> Variables

    #region -----------------------------------------------------> Get numbers
    for k in values:
        if k.strip() != '':
            #------------------------------> Expand ranges
            lK = ExpandRange(k, numType)
            #------------------------------> Get list of numbers
            lN = lN + lK
    #endregion --------------------------------------------------> Get numbers

    #region ----------------------------------------------------------> Unique
    if unique:
        lo = list(dict.fromkeys(lN))
    else:
        lo = lN
    #endregion -------------------------------------------------------> Unique

    return lo
#---


def StrSetMessage(start:str, end:str, link:str='\n\nFurther details:\n') -> str:
    """Creates a message by concatenating start and end with link.

        Parameters
        ----------
        start: str
            Start of the message.
        end: str
            End of the message.
        link: str
            Link between start and end.

        Returns
        -------
        str:
            Full message

        Examples
        --------
        >>> StrSetMessage('Start', 'End', link=' - ')
        >>> 'Start - End'
    """
    # No test
    if link:
        return f"{start}{link}{end}"
    #------------------------------>
    return f"{start} {end}"
#---


def ResControl2ListNumber(                                                      # pylint: disable=dangerous-default-value
    val:str,
    sep:list[str]       = [' ', ',', ';'],
    numType:LIT_NumType = 'int',
    ) -> list[list[list[int]]]:
    """Return a list from a Result - Control string.

        Parameters
        ----------
        val: str
            String with the numbers. e.g. '0-4 6, 7 8 9; 10 13-15, ""; ...'.
        sep: list of str
            Separators used in the string e.g. [' ', ',', ';'].
        numType: str
            To convert to numbers.

        Returns
        -------
        list of list of list of str
        [[[0 1 2 3 4], [7 8 9]], [[10 13 14 15], []], ...]

        Examples
        --------
        >>> ResControl2ListNumber(
            '0 1 2, 3 4 5; 6 7 8, 9 10 11', sep=[' ', ',', ';'], numType='int')
        >>> [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]
    """
    # Test in test.unit.test_method.Test_ResControl2ListNumber
    #region -------------------------------------------------------> Variables
    l = []
    #endregion ----------------------------------------------------> Variables

    #region -------------------------------------------------------> Form list
    for k in val.split(sep[2]):
        #------------------------------>
        lRow = []
        #------------------------------>
        for j in k.split(sep[1]):
            colVal = Str2ListNumber(j, numType=numType, sep=sep[0])
            lRow.append(colVal)
        #------------------------------>
        l.append(lRow)
    #endregion ----------------------------------------------------> Form list

    return l
#---


def ResControl2Flat(val:list[list[list[int]]]) -> list[int]:
    """Result - Control list as a flat list.

        Parameters
        ----------
        val: list of list of list of int
            Result - Control as a list of list of list of int.

        Returns
        -------
        list of int
            Flat Result - Control list

        Examples
        --------
        >>> ResControl2Flat([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]])
        >>> [0,1,2,3,4,5,6,7,8,9,10,11])
    """
    # Test in test.unit.test_method.Test_ResControl2Flat
    return list(itertools.chain(*(itertools.chain(*val))))
#---


def ResControl2DF(
    val:list[list[list[int]]],
    start:int,
    ) -> list[list[list[int]]]:
    """Convert the Result - Control column numbers in the original file to the
        column numbers of the initial dataframe used in the analysis.

        Parameters
        ----------
        val: list of list of list of int
            Result - Control as a list of list of list of int
        start: int
            Column index start of the Result - Control columns in the initial
            dataframe

        Returns
        -------
        list[list[list[int]]]
            The list has the same order as the input val but the column index
            are adjusted.

        Notes
        -----
        It is assumed columns in the DF have the same order as in val.
        Empty list are possible to mimic empty conditions in an experiment.

        Examples
        --------
        >>> ResControl2DF([[[0,1,2], []], [[6,7,8], []]], 1)
        >>> [[[1,2,3],[]], [[4,5,6],[]]]
    """
    # Test in test.unit.test_method.Test_ResControl2DF
    #region -------------------------------------------------------> Variables
    idx  = start
    outL = []
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------> Adjust col idx
    for row in val:
        #------------------------------>
        outR = []
        #------------------------------>
        for col in row:
            #------------------------------>
            outC = []
            #------------------------------>
            for _ in col:
                outC.append(idx)
                idx += 1
            #------------------------------>
            outR.append(outC)
        #------------------------------>
        outL.append(outR)
    #endregion -----------------------------------------------> Adjust col idx

    return outL
#---
#endregion ---------------------------------------------------> String Methods


#region ------------------------------------------------------> Number methods
def ExpandRange(
    r:str,
    numType:LIT_NumType = 'int',
    ) -> Union[list[int], list[float]]:
    """Expand a range of numbers: '4-7' --> [4,5,6,7]. Only positive integers
        are supported.

        Parameters
        ----------
        r: str
            String containing the range.
        numType: str
            One of 'int', 'float'. For the case where r is not a range.

        Returns
        -------
        list of int

        Notes
        -----
        Ranges are interpreted as closed ranges.

        Examples
        --------
        >>> ExpandRange('0-15', 'int')
        >>> [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        >>> ExpandRange('-5.4', 'float')
        >>> [-5.4]
    """
    # Test in test.unit.test_method.Test_ExpandRange
    #region -------------------------------------------------> Expand & Return
    tr = r.strip()
    #------------------------------> Expand
    if '-' in tr:
        #------------------------------> Catch more than one - in range
        a,b = tr.split('-')
        #------------------------------> Negative value
        if a == '':
            return [mConfig.core.oNumType[numType](tr)]
        #------------------------------> Range like 4-
        if b == '':
            raise ValueError(mConfig.core.mRangeNumIE.format(r))
        #------------------------------> Expand range
        a = int(a)
        b = int(b)
        if a < b:
            return [x for x in range(a, b+1, 1)]
        #------------------------------> Bad Input
        raise ValueError(mConfig.core.mRangeNumIE.format(r))
    #------------------------------> Positive number
    return [mConfig.core.oNumType[numType](tr)]
    #endregion ----------------------------------------------> Expand & Return
#---
#endregion ---------------------------------------------------> Number methods


#region ----------------------------------------------------------------> Dict
def DictVal2Str(                                                                # pylint: disable=dangerous-default-value
    iDict:dict,
    changeKey:list = [],
    new:bool       = False,
    ) -> dict:
    """Returns a dict with values turn to str for all keys or only those in
        changeKey.

        Parameters
        ----------
        iDict: dict
            Initial dict.
        changeKey: list of keys
            Only modify this keys.
        new: boolean
            Do not modify iDict (True) or modify in place (False).
            Default is False.

        Returns
        -------
        dict:
            with the corresponding values turned to str.

        Examples
        --------
        >>> DictVal2Str({1:Path('/k/d/c'), 'B':3})
        >>> {1: '/k/d/c', 'B': '3'}
        >>> DictVal2Str({1:Path('/k/d/c'), 'B':3}, changeKey=[1])
        >>> {1: '/k/d/c', 'B': 3}
    """
    # Test in test.unit.test_method.Test_DictVal2Str
    #region -------------------------------------------------------> Variables
    if new:
        oDict = copy.deepcopy(iDict)
    else:
        oDict = iDict
    #endregion ----------------------------------------------------> Variables

    #region ---------------------------------------------------> Change values
    for k in changeKey:
        oDict[k] = str(oDict[k])
    #endregion ------------------------------------------------> Change values

    return oDict
#---
#endregion -------------------------------------------------------------> Dict


#region --------------------------------------------------------> pd.DataFrame
def DFFilterByColS(
    df:pd.DataFrame,
    col:int,
    refStr:str,
    comp:LIT_CompEq,
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the string values present in
        col.

        Parameters
        ----------
        df: pd.DataFrame
        col: int
            The column index used to filter rows.
        refStr: string
            Reference string.
        comp: str
            Numeric comparison to use in the filter. One of: 'e', 'ne.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        - Rows with values in col that do not comply with c[x] comp refStr are
        discarded, e.g. c[x] == 'refString'
        - Assumes all values in col are strings.
    """
    # Test in test.unit.test_method.Test_DFFilterByColS
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'e':
        dfo = df.loc[df.iloc[:,col] == refStr]
    elif comp == 'ne':
        dfo = df.loc[df.iloc[:,col] != refStr]
    else:
        msg = mConfig.core.mNotImplementedFull.format(
            comp, 'comp', LIT_CompEq)
        raise ValueError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---


def DFExclude(df:pd.DataFrame, col:list[int]) -> 'pd.DataFrame':
    """Exclude rows in the pd.DataFrame based on the values present in col.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the data.
        col: list[int]
            Column numbers to look for rows to exclude.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with at least one value other than NA in the given columns are
        discarded.
    """
    # Test in test.unit.test_method.Test_DFExclude
    #region ----------------------------------------------------------> Exclude
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Exclude
    a = dfo.iloc[:,col].notna()
    a = a.loc[(a==True).any(axis=1)]                                            # pylint: disable=singleton-comparison
    idx = a.index
    dfo = dfo.drop(index=idx)                                                   # type: ignore
    #endregion -------------------------------------------------------> Exclude

    return dfo
#---


def DFFilterByColN(
    df:pd.DataFrame,
    col:list[int],
    refVal:float,
    comp:LIT_Comp,
    ) -> pd.DataFrame:
    """Filter rows in the pd.DataFrame based on the numeric values present in
        col.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the data.
        col: list of int
            The column indexes used to filter rows.
        refVal: float
            Reference value.
        comp: str
            Numeric comparison to use in the filter. One of:
            'lt', 'le', 'e', 'ge', 'gt'

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with values in col that do not comply with c[x] comp refVal are
        discarded, e.g. c[x] > 3,45

        Assumes all values in col are numbers.
    """
    # Test in test.unit.test_method.Test_DFFilterByColN
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'lt':
        dfo = df.loc[(df.iloc[:,col] < refVal).any(axis=1)]                     # type: ignore
    elif comp == 'le':
        dfo = df.loc[(df.iloc[:,col] <= refVal).any(axis=1)]                    # type: ignore
    elif comp == 'e':
        dfo = df.loc[(df.iloc[:,col] == refVal).any(axis=1)]                    # type: ignore
    elif comp == 'ge':
        dfo = df.loc[(df.iloc[:,col] >= refVal).any(axis=1)]                    # type: ignore
    elif comp == 'gt':
        dfo = df.loc[(df.iloc[:,col] > refVal).any(axis=1)]                     # type: ignore
    else:
        msg = mConfig.core.mNotImplementedFull.format(comp, 'comp', LIT_Comp)
        raise ValueError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---


def DFReplace(                                                                  # pylint: disable=dangerous-default-value
    df:Union[pd.DataFrame, pd.Series],
    oriVal:list,
    repVal:Union[list, tuple, str, float, int],
    sel:list[int] = [],
    ) -> Union[pd.DataFrame, pd.Series]:
    """Replace values in the dataframe.

        Parameters
        ----------
        df: pd.DataFrame or pd.Series
            Dataframe with the data.
        oriVal: list
            List of values to search and replace.
        repVal: list or single value
            List of values to use as replacement. When only one value is given
            all oriVal are replace with the given value.
        sel: list of int
            Column indexes.

        Returns
        -------
        pd.DataFrame or pd.Series
            With replaced values

        Raise
        -----
        ValueError :
            - When selection is not found in df
            - When oriVal and repVal have different length
        RuntimeError :
            - When the replacement procedure does not finish correctly

        Notes
        -----
        Column selection in the df is done by column number.
    """
    # Test in test.unit.test_method.Test_DFReplace
    #region ---------------------------------------------------------> Replace
    #------------------------------> Copy
    dfo = df.copy()
    #------------------------------> Replace
    if sel:
        dfo.iloc[:,sel] = dfo.iloc[:,sel].replace(oriVal, repVal)               # type: ignore
    else:
        dfo = dfo.replace(oriVal, repVal)                                       # type: ignore
    #endregion ------------------------------------------------------> Replace

    return dfo
#---
#endregion -----------------------------------------------------> pd.DataFrame


#region -------------------------------------------------------------> Methods
def GetDisplayInfo(win: 'cWindow.BaseWindow') -> dict[str, dict[str, int]]:
    """This will get the information needed to set the position of a window.
        Should be called after Fitting sizers for accurate window size
        information.

        Parameters
        ----------
        win : wx.Frame
            Window to be positioned

        Returns
        -------
        dict
            {
                'D' : {'xo':X, 'yo':Y, 'w':W, 'h':h}, Info about display
                'W' : {'N': N, 'w':W, 'h', H},        Info about win
            }
    """
    #region ----------------------------------------------------> Display info
    xd, yd, wd, hd =  wx.Display(win).GetClientArea()
    #endregion -------------------------------------------------> Display info

    #region -----------------------------------------------------> Window info
    nw = mConfig.core.winNumber.get(win.cName, 0)
    ww, hw = win.GetSize()
    #endregion --------------------------------------------------> Window info

    #region ------------------------------------------------------------> Dict
    data = {
        'D' : {
            'xo' : xd,
            'yo' : yd,
            'w'  : wd,
            'h'  : hd,
        },
        'W' : {
            'N' : nw,
            'w' : ww,
            'h' : hw,
        },
    }
    #endregion ---------------------------------------------------------> Dict

    return data
#---


def LCtrlFillColNames(lc:wx.ListCtrl, fileP:Union[Path, str]) -> bool:
    """Fill the wx.ListCtrl with the name of the columns in fileP.

        Parameters
        ----------
        lc: wx.ListCtrl
            wx.ListCtrl to fill info into.
        fileP: Path
            Path to the file from which to read the column names.

        Notes
        -----
        This will delete the wx.ListCtrl before adding the new names.
        wx.ListCtrl is assumed to have at least two columns [#, Name,]
    """
    #region -------------------------------------------------------> Read file
    colNames = cFile.ReadFileFirstLine(fileP)
    #endregion ----------------------------------------------------> Read file

    #region -------------------------------------------------------> Fill List
    #------------------------------> Del items
    lc.DeleteAllItems()
    #------------------------------> Fill
    for k, v in enumerate(colNames):
        index = lc.InsertItem(k, " " + str(k))
        lc.SetItem(index, 1, v)
    #endregion ----------------------------------------------------> Fill List

    return True
#---
#endregion ----------------------------------------------------------> Methods
